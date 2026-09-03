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
export const TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX = 30;

export type TimelineAllDayRangePosition =
  | 'single'
  | 'start'
  | 'middle'
  | 'end';

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

export function timelineAllDayLaneHeightPx(itemCount: number): number {
  if (itemCount <= 0) {
    return 0;
  }
  return (
    TIMELINE_ALL_DAY_LANE_HEADER_HEIGHT_PX +
    itemCount * TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX
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
