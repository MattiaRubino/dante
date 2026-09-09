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
 * B02-A is append-only from the Timeline UI perspective: establish + read.
 * Replacing/removing already materialized cards belongs to later Schedule
 * mutation slices, so this hook only materializes authoritative current items.
 * The Timeline reducer remains the sole owner of UI state.
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
