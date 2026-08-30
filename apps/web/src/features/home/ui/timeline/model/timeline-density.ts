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
  const eventPolicy = TIMELINE_POLICY.event;
  const thresholds = eventPolicy.readableHeightThresholdMinutes;
  const heights = eventPolicy.readableHeightPx;

  let height: number =
    duration <= thresholds.upTo5Minutes
      ? heights.upTo5Minutes
      : duration <= thresholds.upTo15Minutes
        ? heights.upTo15Minutes
        : duration <= thresholds.upTo30Minutes
          ? heights.upTo30Minutes
          : duration <= thresholds.upTo45Minutes
            ? heights.upTo45Minutes
            : duration <= thresholds.upTo60Minutes
              ? heights.upTo60Minutes
              : duration <= thresholds.upTo90Minutes
                ? heights.upTo90Minutes
                : heights.longer;

  if (event.subitems?.length) {
    height = Math.max(height, eventPolicy.subitemsMinimumHeightPx);
  }

  if (
    event.title.length > eventPolicy.longTitleThreshold &&
    duration <= eventPolicy.longTitleMaxDurationMinutes
  ) {
    height += eventPolicy.longTitleExtraHeightPx;
  }

  return height;
}

export function computeTimelineDensityMetrics(
  events: readonly TimelineEvent[],
): TimelineDensityMetrics {
  const policy = TIMELINE_POLICY.density;
  const slotMinutes = policy.slotMinutes;
  const bins = new Uint16Array(
    Math.ceil(TIMELINE_MINUTES_PER_DAY / slotMinutes),
  );
  const starts = events.map((event) => event.startMinute).sort((a, b) => a - b);
  let shortCount = 0;

  for (const event of events) {
    const duration = eventDurationMinutes(event);
    if (duration <= policy.shortEventThresholdMinutes) {
      shortCount += 1;
    }

    const first = Math.max(
      0,
      Math.min(bins.length - 1, Math.floor(event.startMinute / slotMinutes)),
    );
    const last = Math.max(
      first,
      Math.min(bins.length - 1, Math.ceil(event.endMinute / slotMinutes) - 1),
    );

    for (let index = first; index <= last; index += 1) {
      incrementAt(bins, index, 1);
    }
  }

  let maxConcurrent = 0;
  let overlapLoad = 0;
  for (const count of bins) {
    maxConcurrent = Math.max(maxConcurrent, count);
    overlapLoad += Math.max(0, count - 1);
  }

  let burst = 0;
  let left = 0;
  for (let right = 0; right < starts.length; right += 1) {
    const rightStart = starts[right];
    if (rightStart === undefined) {
      continue;
    }

    while (left < right) {
      const leftStart = starts[left];
      if (
        leftStart === undefined ||
        rightStart - leftStart < policy.burstWindowMinutes
      ) {
        break;
      }
      left += 1;
    }
    burst = Math.max(burst, right - left + 1);
  }

  return {
    count: events.length,
    shortCount,
    maxConcurrent,
    overlapRatio: overlapLoad / Math.max(1, bins.length),
    burst,
  };
}

export function computeTimelineBaseScale(
  events: readonly TimelineEvent[],
): number {
  if (events.length === 0) {
    return TIMELINE_POLICY.density.baseScale;
  }

  const density = computeTimelineDensityMetrics(events);
  const policy = TIMELINE_POLICY.density;
  const eventPressure =
    Math.max(0, density.count - policy.eventPressureBaselineCount) *
    policy.eventPressurePerItem;
  const concurrencyPressure =
    Math.max(
      0,
      density.maxConcurrent - policy.concurrencyPressureBaselineCount,
    ) * policy.concurrencyPressurePerItem;
  const overlapPressure = density.overlapRatio * policy.overlapPressureFactor;
  const shortPressure = density.shortCount * policy.shortEventPressurePerItem;
  const burstPressure =
    Math.max(0, density.burst - policy.burstPressureBaselineCount) *
    policy.burstPressurePerItem;

  return Math.max(
    policy.minScale,
    Math.min(
      policy.maxScale,
      policy.baseScale +
        eventPressure +
        concurrencyPressure +
        overlapPressure +
        shortPressure +
        burstPressure,
    ),
  );
}

type TimelineMapperOptions = Readonly<{
  expandedEventIds?: ReadonlySet<TimelineEventId>;
}>;

export function createTimelineTimeMapper(
  events: readonly TimelineEvent[],
  zoom: number,
  options: TimelineMapperOptions = {},
): TimelineTimeMapper {
  const policy = TIMELINE_POLICY.density;
  const normalizedZoom = clampTimelineZoom(zoom);
  const pxPerMinute = computeTimelineBaseScale(events) * normalizedZoom;
  const minuteCount = TIMELINE_MINUTES_PER_DAY;
  const activeDiff = new Int16Array(minuteCount + 2);
  const shortActiveDiff = new Int16Array(minuteCount + 2);
  const nearbyStartDiff = new Int16Array(minuteCount + 2);

  for (const event of events) {
    const start = Math.max(
      0,
      Math.min(minuteCount - 1, Math.floor(event.startMinute)),
    );
    const end = Math.max(
      start + 1,
      Math.min(minuteCount, Math.ceil(event.endMinute)),
    );
    incrementAt(activeDiff, start, 1);
    incrementAt(activeDiff, end, -1);

    if (eventDurationMinutes(event) <= policy.shortEventThresholdMinutes) {
      incrementAt(shortActiveDiff, start, 1);
      incrementAt(shortActiveDiff, end, -1);
    }

    const nearbyFrom = Math.max(
      0,
      Math.floor(event.startMinute - policy.nearbyStartWindowMinutes),
    );
    const nearbyTo = Math.min(
      minuteCount + 1,
      Math.ceil(event.startMinute + policy.nearbyStartWindowMinutes + 1),
    );
    incrementAt(nearbyStartDiff, nearbyFrom, 1);
    incrementAt(nearbyStartDiff, nearbyTo, -1);
  }

  const localScale = new Float64Array(minuteCount + 1);
  let active = 0;
  let shortActive = 0;
  let nearbyStarts = 0;

  for (let minute = 0; minute <= minuteCount; minute += 1) {
    active += valueAt(activeDiff, minute);
    shortActive += valueAt(shortActiveDiff, minute);
    nearbyStarts += valueAt(nearbyStartDiff, minute);
    const localFactor =
      1 +
      Math.max(0, active - policy.activeOverlapBaselineCount) *
        policy.activeOverlapFactor +
      Math.max(0, nearbyStarts - policy.nearbyStartBaselineCount) *
        policy.nearbyStartFactor +
      shortActive * policy.shortActiveFactor;
    localScale[minute] = Math.max(
      pxPerMinute,
      Math.min(policy.maxLocalScale, pxPerMinute * localFactor),
    );
  }

  const smoothScale = new Float64Array(minuteCount + 1);
  const prefix = new Float64Array(minuteCount + 2);
  for (let minute = 0; minute <= minuteCount; minute += 1) {
    prefix[minute + 1] = valueAt(prefix, minute) + valueAt(localScale, minute);
  }

  const radius = policy.smoothingRadiusMinutes;
  for (let minute = 0; minute <= minuteCount; minute += 1) {
    const from = Math.max(0, minute - radius);
    const to = Math.min(minuteCount, minute + radius);
    smoothScale[minute] =
      (valueAt(prefix, to + 1) - valueAt(prefix, from)) / (to - from + 1);
  }

  const requiredScale = new Float64Array(minuteCount + 1);
  for (const event of events) {
    const duration = eventDurationMinutes(event);
    const requiredPerMinute = timelineEventReadableHeight(event) / duration;
    const from = Math.max(
      0,
      Math.min(minuteCount, Math.floor(event.startMinute)),
    );
    const to = Math.max(0, Math.min(minuteCount, Math.ceil(event.endMinute)));

    for (let minute = from; minute < to; minute += 1) {
      requiredScale[minute] = Math.max(
        valueAt(requiredScale, minute),
        requiredPerMinute,
      );
    }

    for (
      let shoulder = 1;
      shoulder <= policy.readableHeightShoulderMinutes;
      shoulder += 1
    ) {
      const eased =
        requiredPerMinute *
        (1 -
          shoulder /
            (policy.readableHeightShoulderMinutes +
              policy.readableHeightShoulderEasePadding));
      if (from - shoulder >= 0) {
        requiredScale[from - shoulder] = Math.max(
          valueAt(requiredScale, from - shoulder),
          eased,
        );
      }
      if (to - 1 + shoulder <= minuteCount) {
        requiredScale[to - 1 + shoulder] = Math.max(
          valueAt(requiredScale, to - 1 + shoulder),
          eased,
        );
      }
    }
  }

  const minuteScale = new Float64Array(minuteCount + 1);
  const cumulative = new Float64Array(minuteCount + 1);
  for (let minute = 0; minute <= minuteCount; minute += 1) {
    minuteScale[minute] = Math.max(
      valueAt(smoothScale, minute),
      valueAt(requiredScale, minute),
    );
    if (minute > 0) {
      cumulative[minute] =
        valueAt(cumulative, minute - 1) + valueAt(minuteScale, minute - 1);
    }
  }

  const eventPolicy = TIMELINE_POLICY.event;
  const stretches = events.flatMap((event) => {
    const isExpanded = options.expandedEventIds?.has(event.id) ?? false;
    if (!isExpanded || !event.subitems?.length) {
      return [];
    }

    return [
      {
        start: event.startMinute,
        end: event.endMinute,
        extra:
          eventPolicy.expandedSubitemsBaseExtraHeightPx +
          event.subitems.length * eventPolicy.expandedSubitemExtraHeightPx,
      },
    ];
  });

  const baseMap = (minute: number): number => {
    const position = Math.max(0, Math.min(minuteCount, minute));
    const whole = Math.floor(position);
    const fraction = position - whole;
    if (whole >= minuteCount) {
      return valueAt(cumulative, minuteCount);
    }
    return valueAt(cumulative, whole) + valueAt(minuteScale, whole) * fraction;
  };

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
