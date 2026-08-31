import type { PlainDate } from '@dante/time';

import { createTimelineTimeMapper } from './model/timeline-density';
import { createTimelinePrototypeEventsForDate } from './model/timeline-fixtures';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import {
  TIMELINE_POLICY,
  timelineSupportsExpandedLayout,
} from './model/timeline-policy';
import type { TimelineState } from './model/timeline-state';
import {
  addTimelineDays,
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
  const safeAvailableWidth = Math.max(1, availableWidth);
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
    Math.max(0, renderedContentWidth) +
      layout.compactIntrinsicHorizontalBreathingPx,
    minimum,
    maximum,
  );
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

function measureTimelineCardContentWidth(card: HTMLElement): number {
  const selectors = [
    '.timeline-event-card__title',
    '.timeline-event-card__time',
    '.timeline-event-card__meta',
  ];
  let maximum = 0;

  for (const selector of selectors) {
    const element = card.querySelector<HTMLElement>(selector);
    if (element) {
      maximum = Math.max(maximum, element.scrollWidth);
    }
  }

  return maximum;
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
  const expandedTrack = Math.max(
    viewportWidth,
    expansion.trackChromeWidthPx + groupCount * layout.groupMinWidthPx,
  );
  const trackWidth =
    viewportWidth + (expandedTrack - viewportWidth) * normalizedProgress;
  const compactInner = Math.max(
    1,
    viewportWidth - expansion.trackChromeWidthPx,
  );
  const expandedInner = Math.max(
    1,
    expandedTrack - expansion.trackChromeWidthPx,
  );
  const safeGroupCount = Math.max(1, groupCount);
  const groupWidth = expandedInner / safeGroupCount;

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

  const stream = root.querySelector<HTMLElement>('.timeline-day-stream');
  if (stream) {
    stream.style.minWidth = `${trackWidth}px`;
  }
  root
    .querySelectorAll<HTMLElement>('.timeline-day-section')
    .forEach((section) => {
      section.style.minWidth = `${trackWidth}px`;
    });

  root.querySelectorAll<HTMLElement>('.timeline-event-card').forEach((card) => {
    const compactLeft = Number(
      card.dataset.compactLeft ?? layout.compactLeftInsetPercent,
    );
    const compactWidthPercent = Number(card.dataset.compactWidth ?? 0);
    const groupIndex = Math.max(0, Number(card.dataset.groupIndex ?? 0));
    const groupLane = Math.max(0, Number(card.dataset.groupLane ?? 0));
    const groupLanes = Math.max(1, Number(card.dataset.groupLanes ?? 1));

    const leftA = (compactLeft / 100) * compactInner;
    const widthA =
      compactWidthPercent > 0
        ? (compactWidthPercent / 100) * compactInner
        : timelineIntrinsicCardWidth(
            measureTimelineCardContentWidth(card),
            compactInner - leftA - expansion.cardInsetPx,
          );
    const leftB =
      groupIndex * groupWidth + (groupLane / groupLanes) * groupWidth;
    const widthB = Math.max(
      expansion.cardMinWidthPx,
      groupWidth / groupLanes - expansion.cardLaneGapPx,
    );
    const left = leftA + (leftB - leftA) * normalizedProgress;
    const width = widthA + (widthB - widthA) * normalizedProgress;

    card.style.left = `${left + expansion.cardInsetPx}px`;
    card.style.width = `${Math.max(expansion.cardMinWidthPx, width)}px`;
  });

  if (normalizedProgress < expansion.settledProgress) {
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
