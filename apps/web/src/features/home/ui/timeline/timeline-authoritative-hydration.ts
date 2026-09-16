import { Temporal, type PlainDateTime } from '@dante/time';
import { useEffect, useRef } from 'react';

import { useTemporalTimelineRuntime } from '../../../temporal/timeline-runtime-boundary';
import type { TemporalTimelineScheduledActivityItem } from '../../../temporal/timeline-read';
import type { TimelineEvent } from './model/timeline-types';

function minuteOfLocalDay(value: PlainDateTime): number {
  return (
    value.hour * 60 +
    value.minute +
    value.second / 60 +
    value.millisecond / 60_000 +
    value.microsecond / 60_000_000 +
    value.nanosecond / 60_000_000_000
  );
}

function displayedInterval(
  item: TemporalTimelineScheduledActivityItem,
): Readonly<{ start: PlainDateTime; end: PlainDateTime }> | null {
  switch (item.temporalForm) {
    case 'floating-local':
      return Object.freeze({ start: item.startsLocalAt, end: item.endsLocalAt });
    case 'named-zone-local':
    case 'absolute':
      return Object.freeze({
        start: item.displayStartsLocalAt,
        end: item.displayEndsLocalAt,
      });
    case 'date-span':
    case 'coarse-local-period':
      return null;
  }
}

function eventMeta(item: TemporalTimelineScheduledActivityItem): string | undefined {
  if (item.temporalForm === 'named-zone-local') {
    return item.zoneId;
  }
  if (item.temporalForm === 'absolute') {
    return 'absolute';
  }
  return undefined;
}

export function canonicalScheduledActivityTimelineEvents(
  item: TemporalTimelineScheduledActivityItem,
): readonly Readonly<{ dateKey: string; event: TimelineEvent }>[] {
  const interval = displayedInterval(item);
  if (interval === null) {
    return Object.freeze([]);
  }

  const startDate = interval.start.toPlainDate();
  const endDate = interval.end.toPlainDate();
  const multiDay = !startDate.equals(endDate);
  const projections: Readonly<{ dateKey: string; event: TimelineEvent }>[] = [];

  for (
    let date = startDate;
    Temporal.PlainDate.compare(date, endDate) <= 0;
    date = date.add({ days: 1 })
  ) {
    const dateKey = date.toString();
    const startMinute = date.equals(startDate)
      ? minuteOfLocalDay(interval.start)
      : 0;
    const endMinute = date.equals(endDate)
      ? minuteOfLocalDay(interval.end)
      : 1440;
    if (endMinute <= startMinute) {
      continue;
    }

    projections.push(
      Object.freeze({
        dateKey,
        event: Object.freeze({
          id: multiDay ? `${item.scheduleRef}@${dateKey}` : item.scheduleRef,
          startMinute,
          endMinute,
          title: item.title,
          groupId: 'personale',
          appearanceTone: 'personal',
          canonicalBasis: Object.freeze({
            kind: 'scheduled-activity' as const,
            activityRef: item.activityRef,
            scheduleRef: item.scheduleRef,
            placementMaterialStateRef: item.placementMaterialStateRef,
          }),
          ...(eventMeta(item) === undefined ? {} : { meta: eventMeta(item) }),
        }),
      }),
    );
  }

  return Object.freeze(projections);
}

/** Compatibility helper retained for existing single-card tests and callers. */
export function canonicalScheduledActivityTimelineEvent(
  item: TemporalTimelineScheduledActivityItem,
): Readonly<{ dateKey: string; event: TimelineEvent }> {
  const [projection] = canonicalScheduledActivityTimelineEvents(item);
  if (projection === undefined) {
    throw new TypeError('Date-lane Schedule placement is not a time-grid event.');
  }
  return projection;
}

/**
 * Reconcile the complete authoritative exact-time window into the UI reducer.
 * Date-span and coarse placements are deliberately excluded here: they belong
 * to the date/coarse lane and must never receive manufactured clock geometry.
 */
export function useAuthoritativeTimelineHydration(
  onReconcile: (
    projections: readonly Readonly<{
      dateKey: string;
      event: TimelineEvent;
    }>[],
  ) => void,
): void {
  const { state } = useTemporalTimelineRuntime();
  const reconcileRef = useRef(onReconcile);

  useEffect(() => {
    reconcileRef.current = onReconcile;
  }, [onReconcile]);

  useEffect(() => {
    if (state.status !== 'ready' || state.window === null) {
      return;
    }

    reconcileRef.current(
      state.window.kind === 'window'
        ? Object.freeze(
            state.window.items.flatMap(canonicalScheduledActivityTimelineEvents),
          )
        : Object.freeze([]),
    );
  }, [state]);
}
