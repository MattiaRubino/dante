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
  if (!sameJson(confirmationWithoutReminder, defaults.confirmation)) return false;

  if (fields.kind === 'event') {
    const event = fields.event;
    const baseline = defaults.event;
    if (event.availability !== baseline.availability) return false;
    if (event.visibility !== baseline.visibility) return false;
    if (event.purpose !== baseline.purpose) return false;
    if (event.expectedOutcome !== baseline.expectedOutcome) return false;
    if (event.decisionRequired !== baseline.decisionRequired) return false;
    if (event.requiredParticipants !== baseline.requiredParticipants) return false;
    if (event.optionalParticipants !== baseline.optionalParticipants) return false;
    if (event.resources !== baseline.resources) return false;
    if (event.preRead !== baseline.preRead) return false;
    if (event.preparationMinutes !== baseline.preparationMinutes) return false;
    if (event.recoveryMinutes !== baseline.recoveryMinutes) return false;
    if (event.conferenceMode !== baseline.conferenceMode) return false;
  }

  return true;
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
    // Quick Activity currently exposes one all-day date, therefore its
    // canonical placement must be exactly that day. Event exposes an explicit
    // end date and may intentionally span multiple days.
    const inclusiveEnd = Temporal.PlainDate.from(
      fields.kind === 'event' ? fields.event.allDayEndDate : fields.date,
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
        startsLocalAt: placement.sourceStartsLocalAt ?? placement.start.toPlainDateTime(),
        endsLocalAt: placement.sourceEndsLocalAt ?? placement.end.toPlainDateTime(),
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
    request: Object.freeze(base),
  });
}
