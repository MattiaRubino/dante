import { Temporal } from '@dante/time';

import { TimeControl } from '../../../temporal-create/ui/temporal-create-core-u2';
import { TemporalCreateDatePicker } from '../../../temporal-create/ui/temporal-create-date-picker';
import { TemporalTimeZoneControl } from '../../../temporal-create/ui/temporal-time-zone-control';
import type { TimelineCanonicalSchedulePlacement } from './model/timeline-types';
import type { EventSchedulePlacementInput } from '../../../temporal/remote-event-profile-data-source';

export type EventScheduleDraft = Readonly<{
  kind: 'timed' | 'all-day';
  startDate: string;
  endDate: string;
  startTime: string;
  endTime: string;
  zoneId: string | null;
  disambiguation: 'reject' | 'earlier' | 'later';
  original?: Readonly<{ start: string; end: string; zoneId: string }>;
}>;

function savedEventDisambiguation(
  placement: Extract<
    TimelineCanonicalSchedulePlacement,
    { kind: 'named-zone-local' }
  >,
): EventScheduleDraft['disambiguation'] | null {
  try {
    for (const disambiguation of ['earlier', 'later'] as const) {
      const start = placement.startsLocalAt.toZonedDateTime(placement.zoneId, {
        disambiguation,
      });
      const end = placement.endsLocalAt.toZonedDateTime(placement.zoneId, {
        disambiguation,
      });
      if (
        start.toInstant().equals(placement.resolvedStartAt) &&
        end.toInstant().equals(placement.resolvedEndAt)
      ) {
        return disambiguation;
      }
    }
  } catch {
    return null;
  }
  return null;
}

export function eventScheduleDraftFromPlacement(
  placement: TimelineCanonicalSchedulePlacement,
): EventScheduleDraft | null {
  if (
    placement.kind === 'absolute' ||
    placement.kind === 'coarse-local-period'
  ) {
    return null;
  }
  if (placement.kind === 'date-span') {
    return {
      kind: 'all-day',
      startDate: placement.startDate.toString(),
      endDate: placement.endDateExclusive.subtract({ days: 1 }).toString(),
      startTime: '09:00',
      endTime: '09:30',
      zoneId: null,
      disambiguation: 'earlier',
    };
  }
  const start = placement.startsLocalAt;
  const end = placement.endsLocalAt;
  if (
    start.second ||
    end.second ||
    start.millisecond ||
    end.millisecond ||
    start.microsecond ||
    end.microsecond ||
    start.nanosecond ||
    end.nanosecond
  ) {
    return null;
  }
  const disambiguation =
    placement.kind === 'named-zone-local'
      ? savedEventDisambiguation(placement)
      : 'earlier';
  if (disambiguation === null) return null;
  return {
    kind: 'timed',
    startDate: start.toPlainDate().toString(),
    endDate: end.toPlainDate().toString(),
    startTime: start.toPlainTime().toString({ smallestUnit: 'minute' }),
    endTime: end.toPlainTime().toString({ smallestUnit: 'minute' }),
    zoneId: placement.kind === 'named-zone-local' ? placement.zoneId : null,
    disambiguation,
    ...(placement.kind === 'named-zone-local'
      ? {
          original: {
            start: start.toString(),
            end: end.toString(),
            zoneId: placement.zoneId,
          },
        }
      : {}),
  };
}

export function eventSchedulePlacementFromDraft(
  draft: EventScheduleDraft,
): EventSchedulePlacementInput {
  if (draft.kind === 'all-day') {
    const start = Temporal.PlainDate.from(draft.startDate);
    const end = Temporal.PlainDate.from(draft.endDate);
    if (Temporal.PlainDate.compare(end, start) < 0) {
      throw new Error(
        'La data di fine deve essere uguale o successiva all’inizio.',
      );
    }
    return {
      kind: 'date_span',
      start_date: start.toString(),
      end_date_exclusive: end.add({ days: 1 }).toString(),
    };
  }
  const start = Temporal.PlainDateTime.from(
    `${draft.startDate}T${draft.startTime}`,
  );
  const end = Temporal.PlainDateTime.from(`${draft.endDate}T${draft.endTime}`);
  if (Temporal.PlainDateTime.compare(end, start) <= 0) {
    throw new Error('La fine deve essere successiva all’inizio.');
  }
  if (!draft.zoneId) {
    return {
      kind: 'floating_local_interval',
      starts_local_at: start.toString(),
      ends_local_at: end.toString(),
    };
  }
  for (const [local, originalValue] of [
    [start, draft.original?.start],
    [end, draft.original?.end],
  ] as const) {
    const original = draft.original;
    if (original?.zoneId === draft.zoneId && local.toString() === originalValue)
      continue;
    const earlier = local.toZonedDateTime(draft.zoneId, {
      disambiguation: 'earlier',
    });
    const later = local.toZonedDateTime(draft.zoneId, { disambiguation: 'later' });
    if (
      !earlier.toPlainDateTime().equals(local) &&
      !later.toPlainDateTime().equals(local)
    ) {
      throw new Error('Questo orario non esiste nel fuso scelto: scegline uno valido.');
    }
  }
  return {
    kind: 'named_zone_local_interval',
    starts_local_at: start.toString(),
    ends_local_at: end.toString(),
    zone_id: draft.zoneId,
    disambiguation: draft.disambiguation,
  };
}

export function EventScheduleEditor({
  draft,
  onChange,
  disabled,
  error,
}: Readonly<{
  draft: EventScheduleDraft;
  onChange: (draft: EventScheduleDraft) => void;
  disabled: boolean;
  error: string;
}>) {
  const update = (change: Partial<EventScheduleDraft>) =>
    onChange({ ...draft, ...change });
  return (
    <fieldset
      className="timeline-event-schedule-editor"
      aria-label="Orario Evento"
      data-edit-invalid={!!error}
      disabled={disabled}
    >
      <div className="timeline-event-schedule-editor__modes">
        <button
          type="button"
          disabled={disabled}
          className={draft.kind === 'timed' ? 'is-active' : ''}
          onClick={() => update({ kind: 'timed' })}
        >
          Orario
        </button>
        <button
          type="button"
          disabled={disabled}
          className={draft.kind === 'all-day' ? 'is-active' : ''}
          onClick={() => update({ kind: 'all-day' })}
        >
          Tutto il giorno
        </button>
      </div>
      {draft.kind === 'timed' ? (
        <>
          <TemporalTimeZoneControl
            zoneId={draft.zoneId}
            disabled={disabled}
            onChange={(zoneId) => update({ zoneId })}
          />
          <div className="temporal-create-activity-interval__fields timeline-activity-editor__interval-fields">
            <TemporalCreateDatePicker
              label="Data inizio"
              locale="it"
              value={draft.startDate}
              onChange={(startDate) => update({ startDate })}
            />
            <TimeControl
              label="Inizio"
              value={draft.startTime}
              dataPath="event.edit.start"
              onChange={(startTime) => update({ startTime })}
            />
            <span
              className="temporal-create-activity-interval__arrow"
              aria-hidden="true"
            >
              →
            </span>
            <TimeControl
              label="Fine"
              value={draft.endTime}
              dataPath="event.edit.end"
              onChange={(endTime) => update({ endTime })}
            />
            <TemporalCreateDatePicker
              label="Data fine"
              locale="it"
              value={draft.endDate}
              align="end"
              onChange={(endDate) => update({ endDate })}
            />
          </div>
        </>
      ) : (
        <div className="timeline-event-schedule-editor__dates">
          <TemporalCreateDatePicker
            label="Data inizio"
            locale="it"
            value={draft.startDate}
            onChange={(startDate) => update({ startDate })}
          />
          <TemporalCreateDatePicker
            label="Data fine"
            locale="it"
            value={draft.endDate}
            onChange={(endDate) => update({ endDate })}
          />
        </div>
      )}
      {error ? (
        <small className="temporal-create-field-error" role="alert">
          {error}
        </small>
      ) : null}
    </fieldset>
  );
}
