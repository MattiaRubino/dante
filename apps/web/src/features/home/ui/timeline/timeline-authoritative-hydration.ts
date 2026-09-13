import type { PlainDateTime } from '@dante/time';
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

export function canonicalScheduledActivityTimelineEvent(
  item: TemporalTimelineScheduledActivityItem,
): Readonly<{ dateKey: string; event: TimelineEvent }> {
  return Object.freeze({
    dateKey: item.startsLocalAt.toPlainDate().toString(),
    event: Object.freeze({
      // One Activity may have 0..N Schedule records. The visible scheduled
      // projection therefore keys on Schedule identity, not Activity identity.
      id: item.scheduleRef,
      startMinute: minuteOfLocalDay(item.startsLocalAt),
      endMinute: minuteOfLocalDay(item.endsLocalAt),
      title: item.title,
      // B02-A's activated C1 path has only the existing personal authoring
      // context. Calendar/Life Area persistence remains a later explicit slice.
      groupId: 'personale',
      appearanceTone: 'personal',
      canonicalBasis: Object.freeze({
        kind: 'scheduled-activity' as const,
        activityRef: item.activityRef,
        scheduleRef: item.scheduleRef,
        placementMaterialStateRef: item.placementMaterialStateRef,
      }),
    }),
  });
}

/**
 * Materialize each authoritative current projection into the UI reducer.
 * The reducer reconciles by ScheduleRef, so a B02-C refetch replaces the prior
 * placement basis without treating the optimistic client as canonical truth.
 */
export function useAuthoritativeTimelineHydration(
  onMaterialize: (dateKey: string, event: TimelineEvent) => void,
): void {
  const { state } = useTemporalTimelineRuntime();
  const materializeRef = useRef(onMaterialize);

  useEffect(() => {
    materializeRef.current = onMaterialize;
  }, [onMaterialize]);

  useEffect(() => {
    if (
      state.status !== 'ready' ||
      state.window === null ||
      state.window.kind !== 'window'
    ) {
      return;
    }

    for (const item of state.window.items) {
      const projection = canonicalScheduledActivityTimelineEvent(item);
      materializeRef.current(projection.dateKey, projection.event);
    }
  }, [state]);
}
