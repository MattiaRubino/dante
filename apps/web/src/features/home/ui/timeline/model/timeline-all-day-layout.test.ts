import { describe, expect, it } from 'vitest';

import {
  TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX,
  TIMELINE_ALL_DAY_LANE_HEADER_HEIGHT_PX,
  offsetTimelineTimeMapper,
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
  timelineAllDayRangePosition,
} from './timeline-all-day-layout';
import type { TimelineAllDayItem, TimelineTimeMapper } from './timeline-types';

const multiDay: TimelineAllDayItem = Object.freeze({
  id: 'all-day:multi',
  startDateKey: '2026-09-03',
  endDateExclusiveKey: '2026-09-06',
  title: 'Fiera',
  groupId: 'work',
});

const singleDay: TimelineAllDayItem = Object.freeze({
  id: 'all-day:single',
  startDateKey: '2026-09-04',
  endDateExclusiveKey: '2026-09-05',
  title: 'Review',
  groupId: 'personal',
});

function baseMapper(): TimelineTimeMapper {
  return Object.freeze({
    height: 2880,
    pxPerMinute: 2,
    map: (minute: number) => minute * 2,
    inv: (pixel: number) => pixel / 2,
  });
}

describe('Timeline all-day layout', () => {
  it('uses half-open civil-date coverage and respects active Context filters', () => {
    const items = [multiDay, singleDay];

    expect(
      timelineAllDayItemsForVisibleDate(items, new Set(), '2026-09-02'),
    ).toEqual([]);
    expect(
      timelineAllDayItemsForVisibleDate(items, new Set(), '2026-09-03'),
    ).toEqual([multiDay]);
    expect(
      timelineAllDayItemsForVisibleDate(items, new Set(), '2026-09-04'),
    ).toEqual([multiDay, singleDay]);
    expect(
      timelineAllDayItemsForVisibleDate(items, new Set(), '2026-09-06'),
    ).toEqual([]);
    expect(
      timelineAllDayItemsForVisibleDate(
        items,
        new Set(['personal']),
        '2026-09-04',
      ),
    ).toEqual([singleDay]);
  });

  it('owns exact lane geometry without adding height when the lane is empty', () => {
    expect(timelineAllDayLaneHeightPx(0)).toBe(0);
    expect(timelineAllDayLaneHeightPx(1)).toBe(
      TIMELINE_ALL_DAY_LANE_HEADER_HEIGHT_PX +
        TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX,
    );
    expect(timelineAllDayLaneHeightPx(3)).toBe(
      TIMELINE_ALL_DAY_LANE_HEADER_HEIGHT_PX +
        3 * TIMELINE_ALL_DAY_ITEM_ROW_HEIGHT_PX,
    );
  });

  it('classifies single/start/middle/end segments from one canonical date span', () => {
    expect(timelineAllDayRangePosition(multiDay, '2026-09-03')).toBe('start');
    expect(timelineAllDayRangePosition(multiDay, '2026-09-04')).toBe('middle');
    expect(timelineAllDayRangePosition(multiDay, '2026-09-05')).toBe('end');
    expect(timelineAllDayRangePosition(singleDay, '2026-09-04')).toBe('single');
  });

  it('moves minute zero below the lane while preserving minute scale and inverse mapping', () => {
    const laneHeight = timelineAllDayLaneHeightPx(2);
    const mapper = offsetTimelineTimeMapper(baseMapper(), laneHeight);

    expect(mapper.height).toBe(2880 + laneHeight);
    expect(mapper.pxPerMinute).toBe(2);
    expect(mapper.map(0)).toBe(laneHeight);
    expect(mapper.map(60)).toBe(laneHeight + 120);
    expect(mapper.inv(laneHeight)).toBe(0);
    expect(mapper.inv(laneHeight + 120)).toBe(60);
    expect(mapper.inv(laneHeight - 10)).toBe(0);
  });

  it('returns the original mapper when no lane offset exists', () => {
    const mapper = baseMapper();
    expect(offsetTimelineTimeMapper(mapper, 0)).toBe(mapper);
  });
});
