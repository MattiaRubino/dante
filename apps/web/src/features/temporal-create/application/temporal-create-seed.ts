import {
  createTemporalCreateFields,
  type TemporalCreateConfirmationIntent,
  type TemporalCreateEventIntent,
  type TemporalCreateEventRecurrenceIntent,
  type TemporalCreateExecutionIntent,
  type TemporalCreateFields,
  type TemporalCreateSchedulingIntent,
} from '../model/temporal-create-session';

/**
 * Structured prefill accepted by Temporal Create before a draft is opened.
 *
 * The seed is intentionally source-neutral: Timeline gestures, a future global
 * Create command, keyboard workflows, imports, or a governed DANTE
 * interpretation can all prepare the same semantic draft without scripting the
 * UI. Provenance and authoritative execution remain separate contracts.
 */
export type TemporalCreateFieldSeed = Readonly<{
  title?: TemporalCreateFields['title'];
  kind?: TemporalCreateFields['kind'];
  date?: TemporalCreateFields['date'];
  timeSemantics?: TemporalCreateFields['timeSemantics'];
  startTime?: TemporalCreateFields['startTime'];
  durationMinutes?: TemporalCreateFields['durationMinutes'];
  timeMode?: TemporalCreateFields['timeMode'];
  timeZoneId?: TemporalCreateFields['timeZoneId'];
  contextId?: TemporalCreateFields['contextId'];
  notes?: TemporalCreateFields['notes'];
  scheduling?: Partial<TemporalCreateSchedulingIntent>;
  execution?: Partial<TemporalCreateExecutionIntent>;
  eventRecurrence?: Partial<TemporalCreateEventRecurrenceIntent>;
  confirmation?: Partial<TemporalCreateConfirmationIntent>;
  event?: Partial<TemporalCreateEventIntent>;
}>;

export function applyTemporalCreateFieldSeed(
  base: TemporalCreateFields,
  seed: TemporalCreateFieldSeed,
): TemporalCreateFields {
  return createTemporalCreateFields({
    title: seed.title ?? base.title,
    kind: seed.kind ?? base.kind,
    date: seed.date ?? base.date,
    timeSemantics: seed.timeSemantics ?? base.timeSemantics,
    startTime: seed.startTime ?? base.startTime,
    durationMinutes: seed.durationMinutes ?? base.durationMinutes,
    timeMode: seed.timeMode ?? base.timeMode,
    timeZoneId: seed.timeZoneId ?? base.timeZoneId,
    contextId: seed.contextId ?? base.contextId,
    notes: seed.notes ?? base.notes,
    scheduling: {
      ...base.scheduling,
      ...seed.scheduling,
    },
    execution: {
      ...base.execution,
      ...seed.execution,
    },
    eventRecurrence: {
      ...base.eventRecurrence,
      ...seed.eventRecurrence,
    },
    confirmation: {
      ...base.confirmation,
      ...seed.confirmation,
    },
    event: {
      ...base.event,
      ...seed.event,
    },
  });
}
