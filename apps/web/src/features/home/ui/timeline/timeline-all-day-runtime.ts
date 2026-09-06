import {
  offsetTimelineTimeMapper,
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
} from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineGroupId,
} from './model/timeline-types';
import type { TimelineRenderedDay } from './timeline-viewport-runtime';

export function applyTimelineAllDayGeometry(
  days: readonly TimelineRenderedDay[],
  items: readonly TimelineAllDayItem[],
  filters: ReadonlySet<TimelineGroupId>,
): readonly TimelineRenderedDay[] {
  let offsetTop = 0;

  return days.map((day) => {
    const visibleItems = timelineAllDayItemsForVisibleDate(
      items,
      filters,
      day.dateKey,
    );
    const laneHeight = timelineAllDayLaneHeightPx(visibleItems.length);
    const mapper = offsetTimelineTimeMapper(day.mapper, laneHeight);
    const layouts =
      laneHeight === 0
        ? day.layouts
        : day.layouts.map((layout) =>
            Object.freeze({
              ...layout,
              top: layout.top + laneHeight,
            }),
          );
    const result = Object.freeze({
      ...day,
      mapper,
      layouts,
      offsetTop,
      height: mapper.height,
    });
    offsetTop += result.height;
    return result;
  });
}
