import { Temporal } from '@dante/time';

import type {
  RecurringActivityTemplate,
  RecurringObjectiveTemplate,
} from './remote-recurring-authoring';
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
import type {
  TemporalCreateActivityChildDraft,
  TemporalCreatePlannedSliceDraft,
  TemporalCreateU2AuthoringDraft,
} from '../model/temporal-create-u2-authoring';

export type TemporalCreateU2Request =
  | Readonly<{ kind: 'activity'; request: TemporalAuthorActivityRequest }>
  | Readonly<{ kind: 'event'; request: TemporalAuthorEventRequest }>;

export function buildTemporalCreateObjectiveTemplates(
  draft: TemporalCreateU2AuthoringDraft,
): readonly RecurringObjectiveTemplate[] {
  return Object.freeze(
    draft.objectives.map((objective, index) => {
      const label = objective.label.trim();
      if (!label) {
        throw new Error(`Obiettivo ${index + 1}: inserisci una descrizione.`);
      }
      const unit = objective.unitCode.trim() || null;
      if (unit !== null && unit.length > 40) {
        throw new Error(`Obiettivo ${index + 1}: l’unità è troppo lunga.`);
      }

      if (objective.resultKind === 'boolean') {
        return Object.freeze({
          label,
          result_kind: 'boolean' as const,
          comparator_code: null,
          target_value: null,
          target_min: null,
          target_max: null,
          unit_code: null,
          presentation_order: index,
        });
      }

      if (objective.resultKind === 'qualitative') {
        return Object.freeze({
          label,
          result_kind: 'qualitative' as const,
          comparator_code: null,
          target_value: null,
          target_min: null,
          target_max: null,
          unit_code: null,
          presentation_order: index,
        });
      }

      if (objective.resultKind === 'quantity') {
        const targetText = objective.targetValue.trim();
        const target = Number(targetText);
        if (!targetText || !Number.isFinite(target)) {
          throw new Error(`Obiettivo ${index + 1}: inserisci un target numerico valido.`);
        }
        const comparator = objective.comparatorCode;
        if (comparator !== 'eq' && comparator !== 'gte' && comparator !== 'lte') {
          throw new Error(`Obiettivo ${index + 1}: seleziona una regola valida.`);
        }
        return Object.freeze({
          label,
          result_kind: 'quantity' as const,
          comparator_code: comparator,
          target_value: target,
          target_min: null,
          target_max: null,
          unit_code: unit,
          presentation_order: index,
        });
      }

      const minimumText = objective.targetMin.trim();
      const maximumText = objective.targetMax.trim();
      const minimum = Number(minimumText);
      const maximum = Number(maximumText);
      if (
        !minimumText ||
        !maximumText ||
        !Number.isFinite(minimum) ||
        !Number.isFinite(maximum) ||
        minimum > maximum
      ) {
        throw new Error(
          `Obiettivo ${index + 1}: inserisci un intervallo numerico valido.`,
        );
      }
      return Object.freeze({
        label,
        result_kind: 'range' as const,
        comparator_code: 'between' as const,
        target_value: null,
        target_min: minimum,
        target_max: maximum,
        unit_code: unit,
        presentation_order: index,
      });
    }),
  );
}

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
  if (
    fields.execution.sessionMode === 'indivisible' &&
    fields.execution.minSessionMinutes !== defaults.execution.minSessionMinutes
  )
    return false;
  if (
    !sameJson(
      {
        ...fields.execution,
        sessionMode: defaults.execution.sessionMode,
        minSessionMinutes: defaults.execution.minSessionMinutes,
      },
      defaults.execution,
    )
  )
    return false;
  if (
    fields.execution.sessionMode === 'splittable' &&
    fields.kind !== 'activity'
  )
    return false;

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

export function temporalCreateRecurringEventSharedIntentSupported(
  fields: TemporalCreateFields,
): boolean {
  if (fields.kind !== 'event') return false;
  if (fields.appearanceTone !== null) return false;

  const defaults = defaultFieldsFor(fields);
  if (!sameJson(fields.scheduling, defaults.scheduling)) return false;
  if (!sameJson(fields.execution, defaults.execution)) return false;

  const confirmationWithoutReminder = {
    ...fields.confirmation,
    reminderLeadMinutes: defaults.confirmation.reminderLeadMinutes,
  };
  if (!sameJson(confirmationWithoutReminder, defaults.confirmation)) return false;

  const event = fields.event;
  const baseline = defaults.event;
  return (
    event.availability === baseline.availability &&
    event.visibility === baseline.visibility &&
    event.purpose === baseline.purpose &&
    event.expectedOutcome === baseline.expectedOutcome &&
    event.decisionRequired === baseline.decisionRequired &&
    event.requiredParticipants === baseline.requiredParticipants &&
    event.optionalParticipants === baseline.optionalParticipants &&
    event.resources === baseline.resources &&
    event.preRead === baseline.preRead &&
    event.preparationMinutes === baseline.preparationMinutes &&
    event.recoveryMinutes === baseline.recoveryMinutes &&
    event.conferenceMode === baseline.conferenceMode
  );
}

export function temporalCreateHasU6Structure(
  draft: TemporalCreateU2AuthoringDraft,
): boolean {
  const structure = draft.activityStructure;
  return (
    structure.captureMode !== 'disabled' ||
    structure.childGuardMode !== 'none' ||
    structure.children.length > 0 ||
    structure.plannedSlices.length > 0 ||
    structure.activityIntervals.length > 0
  );
}

function activityLocalWindow(fields: TemporalCreateFields): Readonly<{
  start: Temporal.PlainDateTime;
  end: Temporal.PlainDateTime;
}> | null {
  if (fields.timeSemantics !== 'timed') return null;
  try {
    const start = Temporal.PlainDateTime.from(
      `${fields.date}T${fields.startTime}`,
    );
    return Object.freeze({
      start,
      end: start.add({ minutes: fields.durationMinutes }),
    });
  } catch {
    return null;
  }
}

function activityBands(
  fields: TemporalCreateFields,
  draft: TemporalCreateU2AuthoringDraft,
):
  | readonly Readonly<{
      start: Temporal.PlainDateTime;
      end: Temporal.PlainDateTime;
    }>[]
  | null {
  const first = activityLocalWindow(fields);
  if (first === null) return null;
  try {
    return [
      first,
      ...draft.activityStructure.activityIntervals.map((interval) => ({
        start: Temporal.PlainDateTime.from(
          `${interval.date}T${interval.startTime}`,
        ),
        end: Temporal.PlainDateTime.from(
          `${interval.endDate}T${interval.endTime}`,
        ),
      })),
    ].sort((left, right) =>
      Temporal.PlainDateTime.compare(left.start, right.start),
    );
  } catch {
    return null;
  }
}

function childLocalWindow(child: TemporalCreateActivityChildDraft): Readonly<{
  start: Temporal.PlainDateTime;
  end: Temporal.PlainDateTime;
}> | null {
  if (!child.scheduleEnabled) return null;
  try {
    return Object.freeze({
      start: Temporal.PlainDateTime.from(
        `${child.startDate}T${child.startTime}`,
      ),
      end: Temporal.PlainDateTime.from(`${child.endDate}T${child.endTime}`),
    });
  } catch {
    return null;
  }
}

function sliceLocalWindow(slice: TemporalCreatePlannedSliceDraft): Readonly<{
  start: Temporal.PlainDateTime;
  end: Temporal.PlainDateTime;
}> | null {
  try {
    return Object.freeze({
      start: Temporal.PlainDateTime.from(`${slice.date}T${slice.startTime}`),
      end: Temporal.PlainDateTime.from(`${slice.date}T${slice.endTime}`),
    });
  } catch {
    return null;
  }
}

function contained(
  inner: Readonly<{
    start: Temporal.PlainDateTime;
    end: Temporal.PlainDateTime;
  }>,
  outer: Readonly<{
    start: Temporal.PlainDateTime;
    end: Temporal.PlainDateTime;
  }>,
): boolean {
  return (
    Temporal.PlainDateTime.compare(inner.start, inner.end) < 0 &&
    Temporal.PlainDateTime.compare(inner.start, outer.start) >= 0 &&
    Temporal.PlainDateTime.compare(inner.end, outer.end) <= 0
  );
}

export function validateTemporalCreateU6Structure(
  fields: TemporalCreateFields,
  draft: TemporalCreateU2AuthoringDraft,
): string | null {
  const structure = draft.activityStructure;
  if (fields.kind !== 'activity' && temporalCreateHasU6Structure(draft)) {
    return 'Only an Activity can own planned Sessions and internal decomposition.';
  }
  if (
    structure.children.length > 100 ||
    structure.plannedSlices.length > 100 ||
    structure.activityIntervals.length > 99
  ) {
    return 'Activity structure exceeds the supported planning limits.';
  }
  if (
    structure.children.some(
      (child) => !child.title.trim() || child.plannedSlices.length > 100,
    )
  ) {
    return 'Internal Activity decomposition is invalid.';
  }

  const bands = activityBands(fields, draft);
  if (
    structure.activityIntervals.length > 0 &&
    (fields.timeSemantics !== 'timed' || bands === null)
  ) {
    return 'Complete each Activity interval date, start and end time.';
  }
  if (
    bands !== null &&
    bands.some(
      (band, index) =>
        Temporal.PlainDateTime.compare(band.start, band.end) >= 0 ||
        (index > 0 &&
          Temporal.PlainDateTime.compare(band.start, bands[index - 1]!.end) <
            0),
    )
  ) {
    return 'Activity intervals must have a valid duration and must not overlap.';
  }
  const parent =
    bands === null
      ? null
      : { start: bands[0]!.start, end: bands[bands.length - 1]!.end };
  if (
    (structure.plannedSlices.length > 0 ||
      structure.children.some(
        (child) => child.scheduleEnabled || child.plannedSlices.length > 0,
      )) &&
    parent === null
  ) {
    return 'Place the Activity before assigning times to planned Sessions.';
  }

  for (const slice of structure.plannedSlices) {
    const window = sliceLocalWindow(slice);
    if (window === null || parent === null) {
      return 'Complete each Session date, start and end time.';
    }
    if (!contained(window, parent)) {
      return 'Every Activity Session must stay inside the parent Activity time range.';
    }
  }

  for (const child of structure.children) {
    const childWindow = childLocalWindow(child);
    if (child.scheduleEnabled) {
      if (childWindow === null || parent === null) {
        return 'Internal Activity decomposition has an incomplete time range.';
      }
      if (!contained(childWindow, parent)) {
        return 'Internal Activity decomposition must stay inside the Activity time range.';
      }
    }
    for (const slice of child.plannedSlices) {
      const window = sliceLocalWindow(slice);
      if (window === null || parent === null) {
        return 'Complete each Session date, start and end time.';
      }
      const ownerWindow = childWindow ?? parent;
      if (!contained(window, ownerWindow)) {
        return child.scheduleEnabled
          ? 'An internal planned Session must stay inside its owner time range.'
          : 'An internal planned Session must stay inside the Activity time range.';
      }
    }
  }

  return null;
}

function localIntervalPlacement(
  fields: TemporalCreateFields,
  start: Temporal.PlainDateTime,
  end: Temporal.PlainDateTime,
): TemporalSchedulePlacementInput {
  if (fields.timeMode === 'zoned') {
    return Object.freeze({
      kind: 'named-zone-local-interval' as const,
      startsLocalAt: start,
      endsLocalAt: end,
      zoneId: fields.timeZoneId,
      disambiguation: fields.timeDisambiguation,
    });
  }
  return Object.freeze({
    kind: 'floating-local-interval' as const,
    startsLocalAt: start,
    endsLocalAt: end,
  });
}

function plannedSliceInput(
  fields: TemporalCreateFields,
  slice: TemporalCreatePlannedSliceDraft,
): TemporalSchedulePlacementInput {
  return localIntervalPlacement(
    fields,
    Temporal.PlainDateTime.from(`${slice.date}T${slice.startTime}`),
    Temporal.PlainDateTime.from(`${slice.date}T${slice.endTime}`),
  );
}

function childPlacementInput(
  fields: TemporalCreateFields,
  child: TemporalCreateActivityChildDraft,
): TemporalSchedulePlacementInput | undefined {
  if (!child.scheduleEnabled) return undefined;
  return localIntervalPlacement(
    fields,
    Temporal.PlainDateTime.from(`${child.startDate}T${child.startTime}`),
    Temporal.PlainDateTime.from(`${child.endDate}T${child.endTime}`),
  );
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

export function buildTemporalCreateLifeAreaInput(
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

function localMinutesBetween(
  start: Temporal.PlainDateTime,
  end: Temporal.PlainDateTime,
): number {
  return Math.round(end.since(start).total({ unit: 'minutes' }));
}

export function buildTemporalCreateRecurringActivityTemplate(
  fields: TemporalCreateFields,
  draft: TemporalCreateU2AuthoringDraft,
): Readonly<{ durationMinutes: number; template: RecurringActivityTemplate }> {
  const bands = activityBands(fields, draft);
  if (fields.kind !== 'activity' || fields.timeSemantics !== 'timed' || bands === null) {
    throw new Error('Recurring Activity template requires a timed Activity.');
  }
  const recurrenceAnchor = Temporal.PlainDateTime.from(
    `${fields.date}T${fields.startTime}`,
  );
  const envelopeStart = bands[0]!.start;
  const envelopeEnd = bands[bands.length - 1]!.end;
  const window = (
    start: Temporal.PlainDateTime,
    end: Temporal.PlainDateTime,
  ) =>
    Object.freeze({
      start_offset_minutes: localMinutesBetween(recurrenceAnchor, start),
      duration_minutes: localMinutesBetween(start, end),
    });

  const structure = draft.activityStructure;
  const template: RecurringActivityTemplate = Object.freeze({
    version: 1 as const,
    root_window: window(envelopeStart, envelopeEnd),
    description: optionalText(fields.notes) ?? null,
    location: optionalText(fields.event.location) ?? null,
    item_color_code:
      draft.lifeArea.kind === 'none' ? draft.itemColorCode : null,
    session_capture_mode: structure.captureMode,
    minimum_session_duration_microseconds:
      fields.execution.sessionMode === 'splittable'
        ? fields.execution.minSessionMinutes * 60 * 1_000_000
        : null,
    child_guard_mode: structure.childGuardMode,
    reality_mode: draft.realityMode,
    placement_protected: structure.placementProtected,
    objectives: buildTemporalCreateObjectiveTemplates(draft),
    activity_intervals:
      structure.activityIntervals.length === 0
        ? Object.freeze([])
        : Object.freeze(
            bands.map((band) => window(band.start, band.end)),
          ),
    planned_slices: Object.freeze(
      structure.plannedSlices.map((slice) => {
        const value = sliceLocalWindow(slice);
        if (value === null) {
          throw new Error('Recurring Activity Session has an invalid time.');
        }
        return Object.freeze({
          ...window(value.start, value.end),
          name: slice.title.trim(),
        });
      }),
    ),
    children: Object.freeze(
      structure.children.map((child) => {
        const placement = childLocalWindow(child);
        return Object.freeze({
          title: child.title.trim(),
          requirement_code: child.requirementCode,
          session_capture_mode: child.captureMode,
          reality_mode: child.realityMode ?? 'manual',
          placement:
            placement === null
              ? null
              : window(placement.start, placement.end),
          planned_slices: Object.freeze(
            child.plannedSlices.map((slice) => {
              const value = sliceLocalWindow(slice);
              if (value === null) {
                throw new Error(
                  'Recurring internal Activity Session has an invalid time.',
                );
              }
              return Object.freeze({
                ...window(value.start, value.end),
                name: slice.title.trim(),
              });
            }),
          ),
        });
      }),
    ),
  });

  return Object.freeze({
    durationMinutes: localMinutesBetween(envelopeStart, envelopeEnd),
    template,
  });
}

export function buildTemporalCreateU2Request(
  fields: TemporalCreateFields,
  draft: TemporalCreateU2AuthoringDraft,
  operationId: string,
): TemporalCreateU2Request {
  const lifeArea = buildTemporalCreateLifeAreaInput(draft);
  const description = optionalText(fields.notes);
  const location = optionalText(fields.event.location);
  const bands = activityBands(fields, draft);
  const placement =
    fields.kind === 'activity' &&
    draft.activityStructure.activityIntervals.length > 0 &&
    bands !== null
      ? localIntervalPlacement(
          fields,
          bands[0]!.start,
          bands[bands.length - 1]!.end,
        )
      : placementInput(fields, draft);
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
        agendaParts: Object.freeze(
          fields.event.agendaParts
            .map((part) => part.trim())
            .filter((part) => part.length > 0),
        ),
      }),
    });
  }

  return Object.freeze({
    kind: 'activity' as const,
    request: Object.freeze({
      ...base,
      ...(fields.execution.sessionMode === 'splittable'
        ? {
            minimumSessionDurationMicroseconds:
              fields.execution.minSessionMinutes * 60 * 1_000_000,
          }
        : {}),
      ...(temporalCreateHasU6Structure(draft)
        ? {
            sessionCaptureMode: draft.activityStructure.captureMode,
            childGuardMode: draft.activityStructure.childGuardMode,
            plannedSlices: draft.activityStructure.plannedSlices.map((slice) =>
              plannedSliceInput(fields, slice),
            ),
            ...(draft.activityStructure.activityIntervals.length > 0 &&
            bands !== null
              ? {
                  activityIntervals: bands.map((band) =>
                    localIntervalPlacement(fields, band.start, band.end),
                  ),
                }
              : {}),
            plannedSliceNames: draft.activityStructure.plannedSlices.map(
              (slice) => slice.title.trim(),
            ),
            children: draft.activityStructure.children.map((child, index) => ({
              title: child.title.trim(),
              requirementCode: child.requirementCode,
              presentationOrder: index + 1,
              sessionCaptureMode: child.captureMode,
              ...(childPlacementInput(fields, child)
                ? { placement: childPlacementInput(fields, child) }
                : {}),
              plannedSlices: child.plannedSlices.map((slice) =>
                plannedSliceInput(fields, slice),
              ),
              plannedSliceNames: child.plannedSlices.map((slice) =>
                slice.title.trim(),
              ),
            })),
          }
        : {}),
    }),
  });
}
