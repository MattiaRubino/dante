import { Temporal } from '@dante/time';

import type {
  TemporalAuthorActivityRequest,
  TemporalAuthorEventRequest,
  TemporalAuthoringLifeAreaInput,
} from '../../temporal/authoring-data-source';
import type { TemporalSchedulePlacementInput } from '../../temporal/schedule-data-source';
import type { TemporalValidationIssue } from '../../temporal';
import {
  buildTemporalCreatePlacement,
  createTemporalCreateFields,
  validateTemporalCreateFields,
  type TemporalCreateFields,
} from '../model/temporal-create-session';
import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import type { TemporalCreatePlannedSliceDraft } from '../model/temporal-create-u2-authoring';

export type TemporalCreateU2Request =
  | Readonly<{ kind: 'activity'; request: TemporalAuthorActivityRequest }>
  | Readonly<{ kind: 'event'; request: TemporalAuthorEventRequest }>;

function optionalText(value: string): string | undefined {
  const normalized = value.trim();
  return normalized.length > 0 ? normalized : undefined;
}

function sameJson(left: unknown, right: unknown): boolean {
  return JSON.stringify(left) === JSON.stringify(right);
}

function defaultFieldsFor(fields: TemporalCreateFields): TemporalCreateFields {
  return createTemporalCreateFields({
    kind: fields.kind,
    date: fields.date,
    timeZoneId: fields.timeZoneId,
  });
}

/**
 * U2 owns the product Quick Create contract. Rich historical authoring remains
 * on the established runtime until each advanced capability is migrated to an
 * equivalent canonical endpoint; unsupported intent must never be silently
 * dropped by the U2 request mapper.
 */
export function temporalCreateU2QuickIntentSupported(
  fields: TemporalCreateFields,
): boolean {
  if (fields.timeSemantics === 'coarse') return false;
  if (fields.appearanceTone !== null) return false;
  if (fields.eventRecurrence.patternKind !== 'none') return false;

  const defaults = defaultFieldsFor(fields);
  if (!sameJson(fields.scheduling, defaults.scheduling)) return false;
  if (!sameJson(fields.execution, defaults.execution)) return false;

  // Reminder is a Schedule capability applied immediately after U2 authoring;
  // every other Confirmation field still belongs to the historical Advanced
  // runtime and therefore must stay at its default here.
  const confirmationWithoutReminder = {
    ...fields.confirmation,
    reminderLeadMinutes: defaults.confirmation.reminderLeadMinutes,
  };
  if (!sameJson(confirmationWithoutReminder, defaults.confirmation))
    return false;

  if (fields.kind === 'event') {
    const event = fields.event;
    const baseline = defaults.event;
    if (event.availability !== baseline.availability) return false;
    if (event.visibility !== baseline.visibility) return false;
    if (event.purpose !== baseline.purpose) return false;
    if (event.expectedOutcome !== baseline.expectedOutcome) return false;
    if (event.decisionRequired !== baseline.decisionRequired) return false;
    if (event.requiredParticipants !== baseline.requiredParticipants)
      return false;
    if (event.optionalParticipants !== baseline.optionalParticipants)
      return false;
    if (event.resources !== baseline.resources) return false;
    if (event.preRead !== baseline.preRead) return false;
    if (event.preparationMinutes !== baseline.preparationMinutes) return false;
    if (event.recoveryMinutes !== baseline.recoveryMinutes) return false;
    if (event.conferenceMode !== baseline.conferenceMode) return false;
  }

  return true;
}

export function temporalCreateHasU6Structure(
  draft: TemporalCreateU2AuthoringDraft,
): boolean {
  const structure = draft.activityStructure;
  return (
    structure.captureMode !== 'disabled' ||
    structure.childGuardMode !== 'none' ||
    structure.children.length > 0 ||
    structure.plannedSlices.length > 0
  );
}

export function validateTemporalCreateU6Structure(
  fields: TemporalCreateFields,
  draft: TemporalCreateU2AuthoringDraft,
): string | null {
  const structure = draft.activityStructure;
  if (fields.kind !== 'activity' && temporalCreateHasU6Structure(draft)) {
    return 'Only an Activity can own Sub-Activities and planned Sessions.';
  }
  if (structure.children.length > 100 || structure.plannedSlices.length > 100) {
    return 'An Activity can contain at most 100 direct children and 100 planned Sessions.';
  }
  if (
    structure.children.some(
      (child) => !child.title.trim() || child.plannedSlices.length > 100,
    )
  ) {
    return 'Every Sub-Activity requires a title and at most 100 planned Sessions.';
  }
  const allSlices = [
    ...structure.plannedSlices,
    ...structure.children.flatMap((child) => child.plannedSlices),
  ];
  try {
    for (const slice of allSlices) {
      const start = Temporal.PlainDateTime.from(
        `${slice.date}T${slice.startTime}`,
      );
      const end = Temporal.PlainDateTime.from(`${slice.date}T${slice.endTime}`);
      if (Temporal.PlainDateTime.compare(start, end) >= 0) {
        return 'A planned Session must end after it starts on the selected date.';
      }
    }
  } catch {
    return 'Complete each planned Session date, start and end time.';
  }
  if (
    structure.children.some((child) => child.plannedSlices.length > 0) &&
    (fields.timeSemantics !== 'timed' || fields.timeMode !== 'zoned')
  ) {
    return 'Place the parent Activity in a named time zone before planning a child Session.';
  }
  return null;
}

function plannedSliceInput(
  fields: TemporalCreateFields,
  slice: TemporalCreatePlannedSliceDraft,
): TemporalSchedulePlacementInput {
  const startsLocalAt = Temporal.PlainDateTime.from(
    `${slice.date}T${slice.startTime}`,
  );
  const endsLocalAt = Temporal.PlainDateTime.from(
    `${slice.date}T${slice.endTime}`,
  );
  if (fields.timeMode === 'zoned') {
    return Object.freeze({
      kind: 'named-zone-local-interval' as const,
      startsLocalAt,
      endsLocalAt,
      zoneId: fields.timeZoneId,
      disambiguation: fields.timeDisambiguation,
    });
  }
  return Object.freeze({
    kind: 'floating-local-interval' as const,
    startsLocalAt,
    endsLocalAt,
  });
}

/** U2 deliberately supersedes the B05 requirement that contextId be non-empty. */
export function validateTemporalCreateU2QuickFields(
  fields: TemporalCreateFields,
): readonly TemporalValidationIssue[] {
  return Object.freeze(
    validateTemporalCreateFields(fields).filter(
      (issue) => issue.code !== 'temporal.create.context.required',
    ),
  );
}

function lifeAreaInput(
  draft: TemporalCreateU2AuthoringDraft,
): TemporalAuthoringLifeAreaInput | undefined {
  switch (draft.lifeArea.kind) {
    case 'none':
      return undefined;
    case 'new':
      return Object.freeze({
        newName: draft.lifeArea.name,
        ...(draft.lifeArea.colorCode
          ? { colorCode: draft.lifeArea.colorCode }
          : {}),
      });
    case 'existing':
      return Object.freeze({
        lifeAreaRef: draft.lifeArea.lifeAreaRef,
        ...(draft.lifeArea.colorChanged
          ? {
              expectedRevision: draft.lifeArea.expectedRevision,
              ...(draft.lifeArea.colorCode
                ? { colorCode: draft.lifeArea.colorCode }
                : {}),
            }
          : {}),
      });
  }
}

function placementInput(
  fields: TemporalCreateFields,
  draft: TemporalCreateU2AuthoringDraft,
): TemporalSchedulePlacementInput | undefined {
  if (fields.timeSemantics === 'unscheduled') return undefined;

  if (fields.timeSemantics === 'all-day') {
    const startDate = Temporal.PlainDate.from(fields.date);
    // Quick exposes the same explicit inclusive start/end date range for both
    // Activity and Event. The canonical Schedule stores an exclusive end.
    const inclusiveEnd = Temporal.PlainDate.from(
      fields.kind === 'event' ? fields.event.allDayEndDate : draft.endDate,
    );
    return Object.freeze({
      kind: 'date-span' as const,
      startDate,
      endDateExclusive: inclusiveEnd.add({ days: 1 }),
    });
  }

  const placement = buildTemporalCreatePlacement(fields);
  if (placement === null) return undefined;

  switch (placement.kind) {
    case 'date-span':
      return Object.freeze({
        kind: 'date-span' as const,
        startDate: placement.startDate,
        endDateExclusive: placement.endDateExclusive,
      });
    case 'floating-local':
      return Object.freeze({
        kind: 'floating-local-interval' as const,
        startsLocalAt: placement.start,
        endsLocalAt: placement.end,
      });
    case 'zoned':
      return Object.freeze({
        kind: 'named-zone-local-interval' as const,
        startsLocalAt:
          placement.sourceStartsLocalAt ?? placement.start.toPlainDateTime(),
        endsLocalAt:
          placement.sourceEndsLocalAt ?? placement.end.toPlainDateTime(),
        zoneId: fields.timeZoneId,
        disambiguation: fields.timeDisambiguation,
      });
    case 'absolute':
      return Object.freeze({
        kind: 'absolute-interval' as const,
        startsAt: placement.start,
        endsAt: placement.end,
      });
    case 'coarse-local-period':
      return Object.freeze({
        kind: 'coarse-local-period' as const,
        localDate: placement.localDate,
        period: placement.period,
      });
  }
}

export function buildTemporalCreateU2Request(
  fields: TemporalCreateFields,
  draft: TemporalCreateU2AuthoringDraft,
  operationId: string,
): TemporalCreateU2Request {
  const lifeArea = lifeAreaInput(draft);
  const description = optionalText(fields.notes);
  const location = optionalText(fields.event.location);
  const placement = placementInput(fields, draft);
  const base = {
    operationId,
    title: fields.title.trim(),
    ...(description ? { description } : {}),
    ...(location ? { location } : {}),
    ...(draft.lifeArea.kind === 'none' && draft.itemColorCode
      ? { itemColorCode: draft.itemColorCode }
      : {}),
    ...(lifeArea ? { lifeArea } : {}),
    ...(placement ? { placement } : {}),
  } as const;

  if (fields.kind === 'event') {
    return Object.freeze({
      kind: 'event' as const,
      request: Object.freeze({
        ...base,
        agendaParts: Object.freeze([...fields.event.agendaParts]),
      }),
    });
  }

  return Object.freeze({
    kind: 'activity' as const,
    request: Object.freeze({
      ...base,
      ...(temporalCreateHasU6Structure(draft)
        ? {
            sessionCaptureMode: draft.activityStructure.captureMode,
            childGuardMode: draft.activityStructure.childGuardMode,
            plannedSlices: draft.activityStructure.plannedSlices.map((slice) =>
              plannedSliceInput(fields, slice),
            ),
            children: draft.activityStructure.children.map((child, index) => ({
              title: child.title.trim(),
              requirementCode: child.requirementCode,
              presentationOrder: index + 1,
              sessionCaptureMode: child.captureMode,
              plannedSlices: child.plannedSlices.map((slice) =>
                plannedSliceInput(fields, slice),
              ),
            })),
          }
        : {}),
    }),
  });
}
