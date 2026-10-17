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

  // Reserve room before Play for the planned time, actual time and optional
  // Session count. The card's runtime state never dictates this floor.
  if (event.canonicalBasis?.kind === 'scheduled-activity') {
    height = Math.max(height, eventPolicy.activityMinimumHeightPx);
  } else {
    height = Math.max(height, eventPolicy.eventMinimumHeightPx);
  }
  height = Math.max(height, event.visualMinimumHeightPx ?? 0);
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
  // Reserve short spans first. Previously each long interval was expanded
  // independently despite already containing the readable short interval,
  // doubling the same minute in overlapping cards.
  const byDuration = [...events].sort(
    (left, right) =>
      eventDurationMinutes(left) - eventDurationMinutes(right) ||
      left.startMinute - right.startMinute ||
      left.id.localeCompare(right.id),
  );
  for (const event of byDuration) {
    const exactDuration = event.endMinute - event.startMinute;
    // Fractional-minute factual intervals receive their own localized
    // expansion below; never expand an entire minute for a five-second Stop.
    if (exactDuration < 1) continue;
    const from = Math.max(
      0,
      Math.min(minuteCount, Math.floor(event.startMinute)),
    );
    const to = Math.max(
      0,
      Math.min(minuteCount, Math.ceil(event.endMinute)),
    );
    let alreadyReservedPx = 0;
    for (let minute = from; minute < to; minute += 1) {
      const overlap = Math.max(
        0,
        Math.min(event.endMinute, minute + 1) -
          Math.max(event.startMinute, minute),
      );
      alreadyReservedPx +=
        Math.max(
          valueAt(smoothScale, minute),
          valueAt(requiredScale, minute),
        ) * overlap;
    }
    const missingPx = Math.max(
      0,
      timelineEventReadableHeight(event) - alreadyReservedPx,
    );
    if (missingPx <= 0) continue;
    const increasePerMinute = missingPx / exactDuration;
    for (let minute = from; minute < to; minute += 1) {
      requiredScale[minute] =
        Math.max(
          valueAt(smoothScale, minute),
          valueAt(requiredScale, minute),
        ) + increasePerMinute;
    }

    for (
      let shoulder = 1;
      shoulder <= policy.readableHeightShoulderMinutes;
      shoulder += 1
    ) {
      const edgeScale = Math.max(
        valueAt(requiredScale, from),
        valueAt(requiredScale, Math.max(from, to - 1)),
      );
      const eased =
        Math.min(edgeScale, policy.maxLocalScale) *
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
  // An execution shorter than one minute needs enough space within its
  // exact fractional clock bounds, not an enormous scale for all 60 seconds.
  // The knot also keeps a stopped card above the real now line.
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
              Math.max(Number.EPSILON, stretch.end - stretch.start);
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
  zoom = 1,
): readonly Readonly<{ minute: number; minor: boolean }>[] {
  const labels: Array<{ minute: number; minor: boolean }> = [];
  const locallyStretched = (minute: number) => {
    const from = Math.max(0, minute - 10);
    const to = Math.min(TIMELINE_MINUTES_PER_DAY, minute + 10);
    return (
      mapper.map(to) - mapper.map(from) >
      mapper.pxPerMinute * (to - from) * 1.35
    );
  };
  const canPlace = (minute: number) =>
    labels.every(
      (label) => Math.abs(mapper.map(label.minute) - mapper.map(minute)) >= 28,
    );
  for (let minute = 0; minute <= TIMELINE_MINUTES_PER_DAY; minute += 60)
    labels.push({ minute, minor: false });
  for (const offset of [30, 15, 45]) {
    for (let hour = 0; hour < TIMELINE_MINUTES_PER_DAY; hour += 60) {
      const minute = hour + offset;
      if ((zoom > 1.25 || locallyStretched(minute)) && canPlace(minute))
        labels.push({ minute, minor: true });
    }
  }
  return labels.sort((a, b) => a.minute - b.minute);
}
