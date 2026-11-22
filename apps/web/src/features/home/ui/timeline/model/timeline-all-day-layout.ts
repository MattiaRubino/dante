import type {
  TimelineAllDayItem,
  TimelineGroupId,
  TimelineTimeMapper,
} from './timeline-types';
import {
  addTimelineDays,
  parseTimelineDate,
  timelineDateKey,
} from './timeline-temporal';

export const TIMELINE_ALL_DAY_LANE_HEADER_HEIGHT_PX = 34;
export const TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX = 42;
export const TIMELINE_ALL_DAY_VISIBLE_ROWS = 2;
export const TIMELINE_ALL_DAY_OVERFLOW_ROW_HEIGHT_PX = 32;
export const TIMELINE_ALL_DAY_MAX_EXPANDED_ROWS = 6;

export type TimelineAllDayRangePosition = 'single' | 'start' | 'middle' | 'end';

export function timelineAllDayItemsForVisibleDate(
  items: readonly TimelineAllDayItem[],
  filters: ReadonlySet<TimelineGroupId>,
  dateKey: string,
): readonly TimelineAllDayItem[] {
  return items.filter(
    (item) =>
      item.startDateKey <= dateKey &&
      dateKey < item.endDateExclusiveKey &&
      (filters.size === 0 || filters.has(item.groupId)),
  );
}

/**
 * The expanded rows occupy actual calendar geometry, not a floating popover.
 * Both the painted lane and every consumer of the time mapper use this value.
 * After six additional rows the list scrolls inside the SAME date-lane panel.
 */
export function timelineAllDayLaneHeightPx(
  itemCount: number,
  expanded = false,
): number {
  if (itemCount <= 0) {
    return 0;
  }
  return (
    TIMELINE_ALL_DAY_LANE_HEADER_HEIGHT_PX +
    Math.min(itemCount, TIMELINE_ALL_DAY_VISIBLE_ROWS) *
      TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX +
    (itemCount > TIMELINE_ALL_DAY_VISIBLE_ROWS
      ? TIMELINE_ALL_DAY_OVERFLOW_ROW_HEIGHT_PX
      : 0) +
    (expanded
      ? Math.min(
          Math.max(0, itemCount - TIMELINE_ALL_DAY_VISIBLE_ROWS),
          TIMELINE_ALL_DAY_MAX_EXPANDED_ROWS,
        ) * TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX
      : 0)
  );
}

export function timelineAllDayRangePosition(
  item: TimelineAllDayItem,
  dateKey: string,
): TimelineAllDayRangePosition {
  const startsHere = dateKey === item.startDateKey;
  const endsHere =
    timelineDateKey(addTimelineDays(parseTimelineDate(dateKey), 1)) ===
    item.endDateExclusiveKey;

  if (startsHere && endsHere) {
    return 'single';
  }
  if (startsHere) {
    return 'start';
  }
  if (endsHere) {
    return 'end';
  }
  return 'middle';
}

/**
 * Adds a real all-day lane above minute zero without changing minute semantics.
 * Every consumer that maps or inverses time now sees the same geometry, so
 * scroll anchors, drag/drop, Now and contextual Create remain aligned.
 */
export function offsetTimelineTimeMapper(
  mapper: TimelineTimeMapper,
  offsetPx: number,
): TimelineTimeMapper {
  if (offsetPx <= 0) {
    return mapper;
  }
  return Object.freeze({
    height: mapper.height + offsetPx,
    pxPerMinute: mapper.pxPerMinute,
    map: (minute: number) => offsetPx + mapper.map(minute),
    inv: (pixel: number) => mapper.inv(Math.max(0, pixel - offsetPx)),
  });
}
