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
 * Structured prefill accepted by the manual Temporal Create flow before its
 * draft is opened.
 *
 * The seed lets deterministic manual entry points such as Timeline gestures
 * preserve known date/time/range/context without scripting UI controls. It is
 * deliberately not an AI, natural-language, or voice input contract. Those
 * future verticals remain separate and may reuse downstream application/domain
 * commands only when their own contracts justify it.
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
