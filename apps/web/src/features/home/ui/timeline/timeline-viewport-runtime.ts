import type { PlainDate } from '@dante/time';

import { createTimelineTimeMapper } from './model/timeline-density';
import { createTimelinePrototypeEventsForDate } from './model/timeline-fixtures';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import {
  TIMELINE_MINUTES_PER_DAY,
  TIMELINE_POLICY,
  timelineSupportsExpandedLayout,
} from './model/timeline-policy';
import type { TimelineState } from './model/timeline-state';
import {
  addTimelineDays,
  buildIsoWeek,
  parseTimelineDate,
  timelineDateKey,
} from './model/timeline-temporal';
import type {
  TimelineEvent,
  TimelineEventId,
  TimelineEventLayout,
  TimelineGroup,
  TimelineTimeMapper,
} from './model/timeline-types';

export type TimelineRenderedDay = Readonly<{
  date: PlainDate;
  dateKey: string;
  events: readonly TimelineEvent[];
  mapper: TimelineTimeMapper;
  layouts: readonly TimelineEventLayout[];
  offsetTop: number;
  height: number;
}>;

type TimelineRenderedDayInputs = Readonly<{
  eventsByDate: TimelineState['eventsByDate'];
  groups: readonly TimelineGroup[];
  zoom: number;
  expandedEventIds: ReadonlySet<TimelineEventId>;
}>;

type TimelineCardGeometry = Readonly<{
  card: HTMLElement;
  left: number;
  width: number;
}>;

export type TimelineExpandedTrackGeometry = Readonly<{
  chromeWidth: number;
  expandedTrackWidth: number;
  expandedInnerWidth: number;
  groupWidth: number;
  groupHeaderTrackWidth: number;
}>;

export function clampTimelineRuntime(
  value: number,
  min: number,
  max: number,
): number {
  return Math.max(min, Math.min(max, value));
}

export function timelineNowViewportOffset(gridHeight: number): number {
  return Math.max(
    TIMELINE_POLICY.viewport.nowOffsetMinPx,
    gridHeight * TIMELINE_POLICY.viewport.nowOffsetRatio,
  );
}

export function timelineIntrinsicCardWidth(
  renderedContentWidth: number,
  availableWidth: number,
): number {
  const layout = TIMELINE_POLICY.layout;
  const safeAvailableWidth = Number.isFinite(availableWidth)
    ? Math.max(1, availableWidth)
    : 1;
  const safeContentWidth = Number.isFinite(renderedContentWidth)
    ? Math.max(0, renderedContentWidth)
    : 0;
  const responsiveMaximum = Math.max(
    layout.compactIntrinsicResponsiveMaxFloorPx,
    safeAvailableWidth * layout.compactIntrinsicMaxViewportRatio,
  );
  const maximum = Math.min(
    safeAvailableWidth,
    layout.compactIntrinsicMaxWidthPx,
    responsiveMaximum,
  );
  const minimum = Math.min(layout.compactIntrinsicMinWidthPx, maximum);

  return clampTimelineRuntime(
    safeContentWidth + layout.compactIntrinsicHorizontalBreathingPx,
    minimum,
    maximum,
  );
}

/**
 * Compatibility helper for compact intrinsic widths: an overlap lane may
 * increase track scroll width, but must never shrink an individual card.
 * The production renderer uses the stricter identity-derived width above.
 */
export function timelineCompactCardWidth(
  renderedContentWidth: number,
  availableWidth: number,
  slotMaximumWidth: number | null,
): number {
  // The lane is a positioning constraint; it is not a card-size constraint.
  void slotMaximumWidth;
  return timelineIntrinsicCardWidth(renderedContentWidth, availableWidth);
}

/**
 * One geometry contract owns the expanded event canvas and the group header.
 * The group scroller starts after the left event inset and carries the right
 * event gutter inside its track, so its horizontal scroll range is exactly the
 * same as the expanded timeline grid.
 */
export function timelineExpandedTrackGeometry(
  viewportWidth: number,
  groupCount: number,
  minimumGroupWidth: number = TIMELINE_POLICY.layout.groupMinWidthPx,
): TimelineExpandedTrackGeometry {
  const layout = TIMELINE_POLICY.layout;
  const safeViewportWidth = Number.isFinite(viewportWidth)
    ? Math.max(1, viewportWidth)
    : 1;
  const safeGroupCount = Number.isFinite(groupCount)
    ? Math.max(1, Math.floor(groupCount))
    : 1;
  const chromeWidth = layout.eventsLeftInsetPx + layout.eventsRightInsetPx;
  const compactInnerWidth = Math.max(1, safeViewportWidth - chromeWidth);
  const expandedInnerWidth = Math.max(
    compactInnerWidth,
    safeGroupCount * Math.max(layout.groupMinWidthPx, minimumGroupWidth),
  );
  const expandedTrackWidth = chromeWidth + expandedInnerWidth;
  const groupWidth = expandedInnerWidth / safeGroupCount;
  const groupHeaderTrackWidth = expandedInnerWidth + layout.eventsRightInsetPx;

  return {
    chromeWidth,
    expandedTrackWidth,
    expandedInnerWidth,
    groupWidth,
    groupHeaderTrackWidth,
  };
}

export function parseTimelineViewedDate(
  value: string | undefined,
): PlainDate | null {
  if (!value) {
    return null;
  }

  try {
    return parseTimelineDate(value);
  } catch {
    return null;
  }
}

export function buildTimelineRenderedDays(
  anchor: PlainDate,
  pastDays: number,
  futureDays: number,
  inputs: TimelineRenderedDayInputs,
): readonly TimelineRenderedDay[] {
  const days: TimelineRenderedDay[] = [];
  let offsetTop = 0;

  for (let offset = -pastDays; offset <= futureDays; offset += 1) {
    const date = addTimelineDays(anchor, offset);
    const dateKey = timelineDateKey(date);
    const events =
      inputs.eventsByDate[dateKey] ??
      createTimelinePrototypeEventsForDate(dateKey);
    const mapper = createTimelineTimeMapper(events, inputs.zoom, {
      expandedEventIds: inputs.expandedEventIds,
    });
    const layouts = computeTimelineEventLayouts(events, inputs.groups, mapper);

    days.push({
      date,
      dateKey,
      events,
      mapper,
      layouts,
      offsetTop,
      height: mapper.height,
    });
    offsetTop += mapper.height;
  }

  return days;
}

/** The week shares one elastic minute scale so 10:30 aligns in all columns. */
export function buildTimelineRenderedWeek(
  selected: PlainDate,
  inputs: TimelineRenderedDayInputs,
): readonly TimelineRenderedDay[] {
  const dates = buildIsoWeek(selected);
  const contents = dates.map((date) => {
    const dateKey = timelineDateKey(date);
    return {
      date,
      dateKey,
      events:
        inputs.eventsByDate[dateKey] ??
        createTimelinePrototypeEventsForDate(dateKey),
    };
  });
  const mapper = createTimelineSharedWeekMapper(
    contents.map((day) => day.events),
    inputs.zoom,
    inputs.expandedEventIds,
  );
  return contents.map((day) => ({
    ...day,
    mapper,
    layouts: computeTimelineEventLayouts(day.events, inputs.groups, mapper),
    offsetTop: 0,
    height: mapper.height,
  }));
}

export function createTimelineSharedWeekMapper(
  dailyEvents: readonly (readonly TimelineEvent[])[],
  zoom: number,
  expandedEventIds: ReadonlySet<TimelineEventId>,
): TimelineTimeMapper {
  const dailyMappers = dailyEvents.map((events) =>
    createTimelineTimeMapper(events, zoom, { expandedEventIds }),
  );
  // The seven dates must align, but seven independent days must not count as
  // seven simultaneous crowds. At each minute use the most spacious day's
  // local slope, preserving readable card bounds without multiplying density.
  const cumulative = new Float64Array(TIMELINE_MINUTES_PER_DAY + 1);
  for (let minute = 0; minute < TIMELINE_MINUTES_PER_DAY; minute += 1) {
    const slope = Math.max(
      ...dailyMappers.map(
        (candidate) => candidate.map(minute + 1) - candidate.map(minute),
      ),
    );
    cumulative[minute + 1] = (cumulative[minute] ?? 0) + slope;
  }
  const map = (minute: number): number => {
    const bounded = clampTimelineRuntime(minute, 0, TIMELINE_MINUTES_PER_DAY);
    const whole = Math.floor(bounded);
    if (whole === TIMELINE_MINUTES_PER_DAY)
      return cumulative[TIMELINE_MINUTES_PER_DAY] ?? 0;
    return (
      (cumulative[whole] ?? 0) +
      (bounded % 1) * ((cumulative[whole + 1] ?? 0) - (cumulative[whole] ?? 0))
    );
  };
  const mapper: TimelineTimeMapper = {
    height: map(TIMELINE_MINUTES_PER_DAY),
    map,
    inv: (pixel) => {
      let low = 0;
      let high = TIMELINE_MINUTES_PER_DAY;
      for (let i = 0; i < 28; i += 1) {
        const middle = (low + high) / 2;
        if (map(middle) < pixel) low = middle;
        else high = middle;
      }
      return (low + high) / 2;
    },
    pxPerMinute: Math.max(...dailyMappers.map((day) => day.pxPerMinute)),
  };
  return mapper;
}

export function findTimelineDayAtOffset(
  days: readonly TimelineRenderedDay[],
  offset: number,
): TimelineRenderedDay | null {
  return (
    days.find(
      (day) => offset >= day.offsetTop && offset < day.offsetTop + day.height,
    ) ??
    (offset < (days[0]?.offsetTop ?? 0)
      ? (days[0] ?? null)
      : (days.at(-1) ?? null))
  );
}

export type TimelineViewportAnchor = Readonly<{
  dateKey: string;
  minute: number;
  viewportOffset: number;
}>;

export function captureTimelineViewportAnchor(
  days: readonly TimelineRenderedDay[],
  scrollTop: number,
  viewportOffset = 0,
): TimelineViewportAnchor | null {
  if (days.length === 0) {
    return null;
  }

  const safeScrollTop = Number.isFinite(scrollTop) ? Math.max(0, scrollTop) : 0;
  const safeViewportOffset = Number.isFinite(viewportOffset)
    ? Math.max(0, viewportOffset)
    : 0;
  const contentOffset = safeScrollTop + safeViewportOffset;
  const day = findTimelineDayAtOffset(days, contentOffset);
  if (!day) {
    return null;
  }

  const localOffset = clampTimelineRuntime(
    contentOffset - day.offsetTop,
    0,
    day.height,
  );
  const minute = clampTimelineRuntime(
    day.mapper.inv(localOffset),
    0,
    TIMELINE_MINUTES_PER_DAY,
  );

  return {
    dateKey: day.dateKey,
    minute,
    viewportOffset: safeViewportOffset,
  };
}

export function timelineScrollTopForViewportAnchor(
  days: readonly TimelineRenderedDay[],
  anchor: TimelineViewportAnchor,
): number | null {
  const day = days.find((candidate) => candidate.dateKey === anchor.dateKey);
  if (!day) {
    return null;
  }

  const minute = clampTimelineRuntime(
    Number.isFinite(anchor.minute) ? anchor.minute : 0,
    0,
    TIMELINE_MINUTES_PER_DAY,
  );
  const viewportOffset = Number.isFinite(anchor.viewportOffset)
    ? Math.max(0, anchor.viewportOffset)
    : 0;

  return Math.max(0, day.offsetTop + day.mapper.map(minute) - viewportOffset);
}

/**
 * Independent of card content measurement and runtime states: each card gets
 * its immutable authored width, while the cluster/group determines only X.
 * Both endpoints have a collision-free ordering for cards that overlap in
 * painted time; linear interpolation preserves their left-to-right ordering.
 */
export function timelinePackedCardGeometry(
  stableWidth: number,
  compactLane: number,
  groupIndex: number,
  groupLane: number,
  lanePitch: number,
  groupWidth: number,
  progress: number,
): Readonly<{ left: number; width: number }> {
  const factor = clampTimelineRuntime(progress, 0, 1);
  const compactLeft = compactLane * lanePitch;
  const groupedLeft = groupIndex * groupWidth + groupLane * lanePitch;
  return {
    left: compactLeft + (groupedLeft - compactLeft) * factor,
    width: stableWidth,
  };
}

function setPixelStyle(
  element: HTMLElement,
  property: 'left' | 'width' | 'minWidth',
  value: number,
): void {
  const next = `${value}px`;
  if (element.style[property] !== next) {
    element.style[property] = next;
  }
}

export function applyTimelineExpansion(
  root: HTMLElement | null,
  grid: HTMLDivElement | null,
  groupScroller: HTMLDivElement | null,
  groupCount: number,
  progress: number,
): void {
  if (!root || !grid) {
    return;
  }

  const expansion = TIMELINE_POLICY.expansion;
  const layout = TIMELINE_POLICY.layout;
  const syncTolerance = TIMELINE_POLICY.viewport.horizontalSyncTolerancePx;
  const normalizedProgress = timelineSupportsExpandedLayout(window.innerWidth)
    ? clampTimelineRuntime(progress, 0, 1)
    : 0;
  const viewportWidth = Math.max(1, grid.clientWidth);
  const cards = Array.from(
    root.querySelectorAll<HTMLElement>('.timeline-event-card'),
  );
  // Measurements of rendered text are not stable when Session controls come
  // and go (and can form a width feedback loop with scrollWidth). Identity
  // dimensions are fixed on the card when it is rendered.
  const stableWidths = cards.map((card) => {
    const raw = Number(card.dataset.stableWidth);
    return Number.isFinite(raw) && raw > 0
      ? raw
      : layout.activityCardMinimumWidthPx;
  });
  const maxStableWidth = Math.max(
    layout.activityCardMinimumWidthPx,
    ...stableWidths,
  );
  const lanePitch = maxStableWidth + layout.cardLaneGapPx;
  const maxCompactLane = Math.max(
    0,
    ...cards.map((card) => Math.max(0, Number(card.dataset.compactLane ?? 0))),
  );
  const maxGroupLaneCount = Math.max(
    1,
    ...cards.map((card) => Math.max(1, Number(card.dataset.groupLanes ?? 1))),
  );
  // Never squeeze overlapping cards into the same physical space. More lanes
  // mean more horizontal scrollable track, not smaller, colliding rectangles.
  const expanded = timelineExpandedTrackGeometry(
    viewportWidth,
    groupCount,
    Math.max(layout.groupMinWidthPx, maxGroupLaneCount * lanePitch),
  );
  const compactTrackWidth =
    expanded.chromeWidth +
    maxCompactLane * lanePitch +
    maxStableWidth +
    expansion.cardInsetPx * 2;
  const trackWidth = Math.max(
    viewportWidth,
    compactTrackWidth +
      (expanded.expandedTrackWidth - compactTrackWidth) * normalizedProgress,
  );
  const safeGroupCount = Number.isFinite(groupCount)
    ? Math.max(1, Math.floor(groupCount))
    : 1;
  const week = root.dataset.timelineView === 'week';
  const maxWeekLanes = Math.max(
    1,
    ...cards.map((card) => Math.max(1, Number(card.dataset.compactLanes ?? 1))),
  );
  const weekPitch = layout.weekCardMinimumWidthPx + layout.cardLaneGapPx;
  const weekTrackWidth = week
    ? Math.max(
        viewportWidth,
        7 * (maxWeekLanes * weekPitch + expansion.cardInsetPx * 2),
      )
    : trackWidth;
  // Compact mode normally hides horizontal scrolling. Crowded lanes are
  // different: clipping the extra fixed-width track would hide real cards.
  // Expose horizontal scroll only while the current geometry needs it.
  grid.classList.toggle(
    'is-overflowing',
    (week ? weekTrackWidth : trackWidth) >
      viewportWidth + syncTolerance,
  );
  root.style.setProperty(
    '--timeline-group-opacity',
    String(
      clampTimelineRuntime(
        (normalizedProgress - expansion.groupOpacityStart) /
          expansion.groupOpacityRange,
        0,
        1,
      ),
    ),
  );
  root.style.setProperty(
    '--timeline-expansion-progress',
    String(normalizedProgress),
  );
  root.style.setProperty('--timeline-group-count', String(safeGroupCount));
  root.style.setProperty(
    '--timeline-events-left-inset',
    `${layout.eventsLeftInsetPx}px`,
  );
  root.style.setProperty(
    '--timeline-events-right-inset',
    `${layout.eventsRightInsetPx}px`,
  );
  root.style.setProperty(
    '--timeline-expanded-group-width',
    `${expanded.groupWidth}px`,
  );
  root.style.setProperty(
    '--timeline-expanded-group-track-width',
    `${expanded.groupHeaderTrackWidth}px`,
  );

  const nextTrackWidth = `${trackWidth}px`;
  const stream = root.querySelector<HTMLElement>('.timeline-day-stream');
  if (
    stream &&
    stream.style.minWidth !== (week ? `${weekTrackWidth}px` : nextTrackWidth)
  ) {
    stream.style.minWidth = week ? `${weekTrackWidth}px` : nextTrackWidth;
  }
  root
    .querySelectorAll<HTMLElement>('.timeline-day-section')
    .forEach((section) => {
      const width = week ? `${weekTrackWidth / 7}px` : nextTrackWidth;
      if (section.style.minWidth !== width) {
        section.style.minWidth = width;
      }
    });

  // Geometry reads immutable data attributes, not computed DOM widths;
  // calculate every card first, then apply all coordinate/width writes.
  const geometries: TimelineCardGeometry[] = [];
  for (const card of cards) {
    if (week) {
      const lane = Math.max(0, Number(card.dataset.compactLane ?? 0));
      geometries.push({
        card,
        left: expansion.cardInsetPx + lane * weekPitch,
        width: layout.weekCardMinimumWidthPx,
      });
      continue;
    }
    const width = Number(card.dataset.stableWidth);
    const stableWidth =
      Number.isFinite(width) && width > 0
        ? width
        : layout.activityCardMinimumWidthPx;
    const lane = Math.max(0, Number(card.dataset.compactLane ?? 0));
    const groupIndex = Math.max(0, Number(card.dataset.groupIndex ?? 0));
    const groupLane = Math.max(0, Number(card.dataset.groupLane ?? 0));
    geometries.push({
      card,
      ...timelinePackedCardGeometry(
        stableWidth,
        lane,
        groupIndex,
        groupLane,
        lanePitch,
        expanded.groupWidth,
        normalizedProgress,
      ),
    });
  }

  for (const geometry of geometries) {
    setPixelStyle(geometry.card, 'left', geometry.left + expansion.cardInsetPx);
    setPixelStyle(
      geometry.card,
      'width',
      Math.max(expansion.cardMinWidthPx, geometry.width),
    );
  }

  if (
    normalizedProgress < expansion.settledProgress &&
    trackWidth <= viewportWidth + syncTolerance
  ) {
    if (Math.abs(grid.scrollLeft) > syncTolerance) {
      grid.scrollLeft = 0;
    }
    if (groupScroller && Math.abs(groupScroller.scrollLeft) > syncTolerance) {
      groupScroller.scrollLeft = 0;
    }
  } else if (
    groupScroller &&
    Math.abs(groupScroller.scrollLeft - grid.scrollLeft) > syncTolerance
  ) {
    groupScroller.scrollLeft = grid.scrollLeft;
  }
}
