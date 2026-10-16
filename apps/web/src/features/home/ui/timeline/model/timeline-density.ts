import {
  TIMELINE_MINUTES_PER_DAY,
  TIMELINE_POLICY,
  clampTimelineZoom,
} from './timeline-policy';
import type {
  TimelineDensityMetrics,
  TimelineEvent,
  TimelineEventId,
  TimelineTimeMapper,
} from './timeline-types';

function valueAt(values: ArrayLike<number>, index: number): number {
  return values[index] ?? 0;
}

function incrementAt(
  values: Int16Array | Uint16Array,
  index: number,
  delta: number,
): void {
  values[index] = valueAt(values, index) + delta;
}

function eventDurationMinutes(event: TimelineEvent): number {
  return Math.max(1, event.endMinute - event.startMinute);
}

export function timelineEventReadableHeight(event: TimelineEvent): number {
  const duration = eventDurationMinutes(event);
  const baseMap = (minute: number): number => {
    const position = Math.max(0, Math.min(minuteCount, minute));
    const whole = Math.floor(position);
    const fraction = position - whole;
    if (whole >= minuteCount) {
      return valueAt(cumulative, minuteCount);
    }
    return valueAt(cumulative, whole) + valueAt(minuteScale, whole) * fraction;
  };

  const eventPolicy = TIMELINE_POLICY.event;
  // Sub-minute executions need a precise, localized expansion between
  // fractional timestamps. Multiplying the *entire* 60-second minute by
  // 60/duration creates enormous scroll jumps; padding only the DOM card
  // instead makes the Stop paint beyond the real clock line. A local knot
  // satisfies both the card minimum and actual start/end coordinates.
  const stretches = events.flatMap((event) => {
    const start = event.startMinute;
    const end = event.endMinute;
    const microExtra =
      end > start && end - start < 1
        ? Math.max(
            0,
            timelineEventReadableHeight(event) -
              (baseMap(end) - baseMap(start)),
          )
        : 0;
    const isExpanded = options.expandedEventIds?.has(event.id) ?? false;
    const expandedExtra =
      isExpanded && event.subitems?.length
        ? eventPolicy.expandedSubitemsBaseExtraHeightPx +
          event.subitems.length * eventPolicy.expandedSubitemExtraHeightPx
        : 0;
    if (microExtra <= 0 && expandedExtra <= 0) return [];
    return [{ start, end, extra: microExtra + expandedExtra }];
  });

  const map = (minute: number): number => {
    let pixel = baseMap(minute);
    for (const stretch of stretches) {
      const progress =
        minute <= stretch.start
          ? 0
          : minute >= stretch.end
            ? 1
            : (minute - stretch.start) /
              Math.max(1, stretch.end - stretch.start);
      pixel += stretch.extra * progress;
    }
    return pixel;
  };

  const height = map(minuteCount);
  const inv = (pixel: number): number => {
    const target = Math.max(0, Math.min(height, pixel));
    let low = 0;
    let high = minuteCount;
    for (let iteration = 0; iteration < 28; iteration += 1) {
      const middle = (low + high) / 2;
      if (map(middle) < target) {
        low = middle;
      } else {
        high = middle;
      }
    }
    return (low + high) / 2;
  };

  return { height, map, inv, pxPerMinute };
}

/** Keep hours legible first, then fill genuinely free ruler space with half-
 * and quarter-hour labels. Positions use the same non-linear map as cards. */
export function timelineRulerLabels(
  mapper: TimelineTimeMapper,
): readonly Readonly<{ minute: number; minor: boolean }>[] {
  const labels: Array<{ minute: number; minor: boolean }> = [];
  const canPlace = (minute: number) =>
    labels.every(
      (label) => Math.abs(mapper.map(label.minute) - mapper.map(minute)) >= 28,
    );
  for (let minute = 0; minute <= TIMELINE_MINUTES_PER_DAY; minute += 60)
    labels.push({ minute, minor: false });
  for (const offset of [30, 15, 45]) {
    for (let hour = 0; hour < TIMELINE_MINUTES_PER_DAY; hour += 60) {
      const minute = hour + offset;
      if (canPlace(minute)) labels.push({ minute, minor: true });
    }
  }
  return labels.sort((a, b) => a.minute - b.minute);
}
