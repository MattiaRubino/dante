import { Temporal, type PlainDateTime } from '@dante/time';
import { useEffect, useRef } from 'react';

import { useTemporalTimelineRuntime } from '../../../temporal/timeline-runtime-boundary';
import type { TemporalTimelineScheduledActivityItem } from '../../../temporal/timeline-read';
import type {
  TimelineAllDayItem,
  TimelineCanonicalSchedulePlacement,
  TimelineEvent,
} from './model/timeline-types';

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

function canonicalPlacement(
  item: TemporalTimelineScheduledActivityItem,
): TimelineCanonicalSchedulePlacement {
  switch (item.temporalForm) {
    case 'date-span':
      return Object.freeze({
        kind: 'date-span' as const,
        startDate: item.startDate,
        endDateExclusive: item.endDateExclusive,
      });
    case 'floating-local':
      return Object.freeze({
        kind: 'floating-local' as const,
        startsLocalAt: item.startsLocalAt,
        endsLocalAt: item.endsLocalAt,
      });
    case 'named-zone-local':
      return Object.freeze({
        kind: 'named-zone-local' as const,
        startsLocalAt: item.startsLocalAt,
        endsLocalAt: item.endsLocalAt,
        zoneId: item.zoneId,
        resolvedStartAt: item.resolvedStartAt,
        resolvedEndAt: item.resolvedEndAt,
      });
    case 'absolute':
      return Object.freeze({
        kind: 'absolute' as const,
        startsAt: item.startsAt,
        endsAt: item.endsAt,
      });
    case 'coarse-local-period':
      return Object.freeze({
        kind: 'coarse-local-period' as const,
        localDate: item.localDate,
        period: item.period,
      });
  }
}

function canonicalBasis(item: TemporalTimelineScheduledActivityItem) {
  return Object.freeze({
    kind: 'scheduled-activity' as const,
    activityRef: item.activityRef,
    scheduleRef: item.scheduleRef,
    placementMaterialStateRef: item.placementMaterialStateRef,
    placement: canonicalPlacement(item),
  });
}

export function canonicalScheduledActivityDateLaneItem(
  item: TemporalTimelineScheduledActivityItem,
): TimelineAllDayItem | null {
  if (item.temporalForm === 'date-span') {
    return Object.freeze({
      id: item.scheduleRef,
      startDateKey: item.startDate.toString(),
      endDateExclusiveKey: item.endDateExclusive.toString(),
      title: item.title,
      groupId: 'personale',
      appearanceTone: 'personal',
      canonicalBasis: canonicalBasis(item),
      laneKind: 'all-day' as const,
    });
  }
  if (item.temporalForm === 'coarse-local-period') {
    return Object.freeze({
      id: item.scheduleRef,
      startDateKey: item.localDate.toString(),
      endDateExclusiveKey: item.localDate.add({ days: 1 }).toString(),
      title: item.title,
      groupId: 'personale',
      appearanceTone: 'personal',
      canonicalBasis: canonicalBasis(item),
      laneKind: 'coarse' as const,
      coarsePeriod: item.period,
    });
  }
  return null;
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
          canonicalBasis: canonicalBasis(item),
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
 * Reconcile the complete authoritative Schedule window into presentation-only
 * Timeline projections. Exact forms enter the time grid; date-span and coarse
 * forms enter the date lane and never receive manufactured clock geometry.
 */
export function useAuthoritativeTimelineHydration(
  onReconcileEvents: (
    projections: readonly Readonly<{
      dateKey: string;
      event: TimelineEvent;
    }>[],
  ) => void,
  onReconcileDateLane: (items: readonly TimelineAllDayItem[]) => void,
): void {
  const { state } = useTemporalTimelineRuntime();
  const reconcileEventsRef = useRef(onReconcileEvents);
  const reconcileDateLaneRef = useRef(onReconcileDateLane);

  useEffect(() => {
    reconcileEventsRef.current = onReconcileEvents;
  }, [onReconcileEvents]);

  useEffect(() => {
    reconcileDateLaneRef.current = onReconcileDateLane;
  }, [onReconcileDateLane]);

  useEffect(() => {
    if (state.status !== 'ready' || state.window === null) {
      return;
    }

    const items = state.window.kind === 'window' ? state.window.items : [];
    reconcileEventsRef.current(
      Object.freeze(items.flatMap(canonicalScheduledActivityTimelineEvents)),
    );
    reconcileDateLaneRef.current(
      Object.freeze(
        items.flatMap((item) => {
          const projected = canonicalScheduledActivityDateLaneItem(item);
          return projected === null ? [] : [projected];
        }),
      ),
    );
  }, [state]);
}
