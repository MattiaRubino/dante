import {
  Temporal,
  moveCivilStartPreservingDuration,
  moveAllDayRangePreservingDays,
  projectElapsedEndToZone,
  elapsedMinutesBetweenZonedBounds,
} from '@dante/time';

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
  endZoneId?: string | null;
  disambiguation: 'reject' | 'earlier' | 'later';
  original?: Readonly<{
    start: string; end: string; zoneId: string; endZoneId?: string | null;
  }>;
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
      const end = placement.endsLocalAt.toZonedDateTime(
        placement.endZoneId ?? placement.zoneId, {
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
    endZoneId: placement.kind === 'named-zone-local'
      ? placement.endZoneId ?? null : null,
    disambiguation,
    ...(placement.kind === 'named-zone-local'
      ? {
          original: {
            start: start.toString(),
            end: end.toString(),
            zoneId: placement.zoneId,
            endZoneId: placement.endZoneId ?? null,
          },
        }
      : {}),
  };
}

export function eventSchedulePlacementFromDraft(
  draft: EventScheduleDraft,
): EventSchedulePlacementInput {
  if (draft.kind === 'all-day') {
    if (draft.endZoneId && draft.endZoneId !== draft.zoneId) {
      throw new Error('Seleziona un fuso unico prima di passare a Tutto il giorno.');
    }
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
  const customZone = !!draft.zoneId &&
    !!draft.endZoneId && draft.endZoneId !== draft.zoneId;
  if (!customZone && Temporal.PlainDateTime.compare(end, start) <= 0) {
    throw new Error('La fine deve essere successiva all’inizio.');
  }
  if (!draft.zoneId) {
    return {
      kind: 'floating_local_interval',
      starts_local_at: start.toString(),
      ends_local_at: end.toString(),
    };
  }
  for (const [local, originalValue, boundaryZone, originalZone] of [
    [start, draft.original?.start, draft.zoneId, draft.original?.zoneId],
    [end, draft.original?.end, draft.endZoneId ?? draft.zoneId,
      draft.original?.endZoneId ?? draft.original?.zoneId],
  ] as const) {
    if (originalZone === boundaryZone && local.toString() === originalValue)
      continue;
    const earlier = local.toZonedDateTime(boundaryZone, {
      disambiguation: 'earlier',
    });
    const later = local.toZonedDateTime(boundaryZone, {
      disambiguation: 'later',
    });
    if (
      !earlier.toPlainDateTime().equals(local) &&
      !later.toPlainDateTime().equals(local)
    ) {
      throw new Error(
        'Questo orario non esiste nel fuso scelto: scegline uno valido.',
      );
    }
  }
  if (customZone) {
    // The local end may be numerically before the local start.
    elapsedMinutesBetweenZonedBounds(
      start.toString(), draft.zoneId,
      end.toString(), draft.endZoneId!,
      draft.disambiguation === 'reject' ? 'earlier' : draft.disambiguation,
    );
  }
  return {
    kind: 'named_zone_local_interval',
    starts_local_at: start.toString(),
    ends_local_at: end.toString(),
    zone_id: draft.zoneId,
    ...(customZone ? { end_zone_id: draft.endZoneId! } : {}),
    disambiguation: draft.disambiguation,
  };
}

export function isValidEventScheduleDraft(draft: EventScheduleDraft): boolean {
  try {
    eventSchedulePlacementFromDraft(draft);
    return true;
  } catch {
    return false;
  }
}

export function EventScheduleEditor({
  draft,
  onChange,
  disabled,
  error,
  allowBoundaryZones = true,
}: Readonly<{
  draft: EventScheduleDraft;
  onChange: (draft: EventScheduleDraft) => void;
  disabled: boolean;
  error: string;
  allowBoundaryZones?: boolean;
}>) {
  const update = (change: Partial<EventScheduleDraft>) =>
    onChange({ ...draft, ...change });
  const endZone = draft.endZoneId ?? draft.zoneId;
  const customZone = draft.kind === 'timed' && !!draft.zoneId &&
    !!draft.endZoneId && draft.endZoneId !== draft.zoneId;
  const previousDuration = (): number => {
    if (draft.kind !== 'timed') return 0;
    if (draft.zoneId && endZone) {
      return elapsedMinutesBetweenZonedBounds(
        `${draft.startDate}T${draft.startTime}`, draft.zoneId,
        `${draft.endDate}T${draft.endTime}`, endZone,
        draft.disambiguation === 'reject' ? 'earlier' : draft.disambiguation,
      );
    }
    return Temporal.PlainDateTime.from(`${draft.startDate}T${draft.startTime}`)
      .until(Temporal.PlainDateTime.from(`${draft.endDate}T${draft.endTime}`))
      .total({ unit: 'minutes' });
  };
  const applyTimeZones = (startZone: string | null, endZone: string | null) => {
    // One atomic change from the shared timezone dialog. Preserve the actual
    // duration, and never erase a selected end zone between independent clicks.
    const resolvedEndZone =
      startZone && endZone && startZone !== endZone ? endZone : null;
    let movedEnd: string | null = null;
    if (draft.kind === 'timed') {
      try {
        const start = `${draft.startDate}T${draft.startTime}`;
        const duration = previousDuration();
        movedEnd = startZone
          ? projectElapsedEndToZone(
              start,
              startZone,
              duration,
              resolvedEndZone ?? startZone,
              draft.disambiguation === 'reject' ? 'earlier' : draft.disambiguation,
            )
          : Temporal.PlainDateTime.from(start)
              .add({ minutes: duration })
              .toString({ smallestUnit: 'minute' });
      } catch {
        // Preserve invalid drafts; the existing validation continues to block Save.
      }
    }
    update({
      zoneId: startZone,
      endZoneId: resolvedEndZone,
      ...(movedEnd ? {
        endDate: movedEnd.slice(0, 10),
        endTime: movedEnd.slice(11, 16),
      } : {}),
    });
  };
  const moveStart = (nextDate: string, nextTime: string) => {
    if (draft.kind === 'all-day') {
      update({
        startDate: nextDate,
        endDate: moveAllDayRangePreservingDays(draft.startDate, draft.endDate, nextDate),
      });
      return;
    }
    try {
      const movedEnd = customZone
        ? projectElapsedEndToZone(
            `${nextDate}T${nextTime}`, draft.zoneId!,
            previousDuration(), draft.endZoneId!,
            draft.disambiguation === 'reject' ? 'earlier' : draft.disambiguation,
          )
        : moveCivilStartPreservingDuration(
            `${draft.startDate}T${draft.startTime}`,
            `${draft.endDate}T${draft.endTime}`,
            `${nextDate}T${nextTime}`,
          );
      update({
        startDate: nextDate, startTime: nextTime,
        endDate: movedEnd.slice(0, 10),
        endTime: movedEnd.slice(11, 16),
      });
    } catch {
      // Keep an already-invalid draft editable without synthesizing an end.
      update({ startDate: nextDate, startTime: nextTime });
    }
  };
  const timingInvalid = !isValidEventScheduleDraft(draft);
  return (
    <fieldset
      className="timeline-event-schedule-editor"
      aria-label="Orario Evento"
      data-edit-invalid={!!error || timingInvalid}
      disabled={disabled}
    >
      <div className="temporal-time-mode-toolbar">
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
            className={draft.kind === 'all-day' ? 'is-active' : ''}
            disabled={disabled || customZone}
            title={customZone
              ? 'Seleziona un fuso unico prima di passare a Tutto il giorno'
              : undefined}
            onClick={() => update({ kind: 'all-day' })}
          >
            Tutto il giorno
          </button>
        </div>
        {draft.kind === 'timed' ? (
          <TemporalTimeZoneControl
            zoneId={draft.zoneId}
            endZoneId={draft.endZoneId}
            date={draft.startDate}
            displayLabel={customZone ? 'Personalizzato' : undefined}
            allowDistinctZones={allowBoundaryZones}
            disabled={disabled}
            onChange={(zone) => applyTimeZones(zone, null)}
            onZonesChange={applyTimeZones}
          />
        ) : null}
      </div>
      {draft.kind === 'timed' ? (
        <>
          <div className="temporal-create-activity-interval__fields timeline-activity-editor__interval-fields">
            <TemporalCreateDatePicker
              label="Data inizio"
              locale="it"
              value={draft.startDate}
              onChange={(startDate) => moveStart(startDate, draft.startTime)}
            />
            <TimeControl
              label="Inizio"
              value={draft.startTime}
              dataPath="event.edit.start"
              onChange={(startTime) => moveStart(draft.startDate, startTime)}
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
              invalid={timingInvalid}
              dataPath="event.edit.end"
              onChange={(endTime) => update({ endTime })}
            />
            <TemporalCreateDatePicker
              label="Data fine"
              locale="it"
              value={draft.endDate}
              min={customZone ? undefined : draft.startDate}
              invalid={timingInvalid}
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
            onChange={(startDate) => moveStart(startDate, draft.startTime)}
          />
          <TemporalCreateDatePicker
            label="Data fine"
            locale="it"
            value={draft.endDate}
            min={draft.startDate}
            invalid={timingInvalid}
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
