import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import { timelineAllDayLaneHeightPx } from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineEventLayout,
  TimelineTimeMapper,
} from './model/timeline-types';
import { applyTimelineAllDayGeometry } from './timeline-all-day-runtime';
import type { TimelineRenderedDay } from './timeline-viewport-runtime';

function mapper(): TimelineTimeMapper {
  return Object.freeze({
    height: 1440,
    pxPerMinute: 1,
    map: (minute: number) => minute,
    inv: (pixel: number) => pixel,
  });
}

function layout(top = 120): TimelineEventLayout {
  return Object.freeze({
    event: Object.freeze({
      id: 'timed:1',
      startMinute: 120,
      endMinute: 180,
      title: 'Timed',
      groupId: 'work',
    }),
    top,
    height: 60,
    compactLane: 0,
    compactLaneCount: 1,
    compactLeftPercent: 0,
    compactWidthPercent: 50,
    groupIndex: 0,
    groupLane: 0,
    groupLaneCount: 1,
  });
}

function day(dateKey: string, offsetTop: number): TimelineRenderedDay {
  return Object.freeze({
    date: Temporal.PlainDate.from(dateKey),
    dateKey,
    events: Object.freeze([]),
    mapper: mapper(),
    layouts: Object.freeze([layout()]),
    offsetTop,
    height: 1440,
  });
}

const spanningItem: TimelineAllDayItem = Object.freeze({
  id: 'all-day:1',
  startDateKey: '2026-09-03',
  endDateExclusiveKey: '2026-09-05',
  title: 'Fiera',
  groupId: 'work',
});

describe('Timeline all-day runtime geometry', () => {
  it('adds lane height to every covered day and recomputes cumulative offsets', () => {
    const laneHeight = timelineAllDayLaneHeightPx(1);
    const result = applyTimelineAllDayGeometry(
      [day('2026-09-03', 0), day('2026-09-04', 1440)],
      [spanningItem],
      new Set(),
    );

    expect(result).toHaveLength(2);
    expect(result[0]?.offsetTop).toBe(0);
    expect(result[0]?.height).toBe(1440 + laneHeight);
    expect(result[0]?.mapper.map(0)).toBe(laneHeight);
    expect(result[0]?.layouts[0]?.top).toBe(120 + laneHeight);

    expect(result[1]?.offsetTop).toBe(1440 + laneHeight);
    expect(result[1]?.height).toBe(1440 + laneHeight);
    expect(result[1]?.mapper.map(0)).toBe(laneHeight);
    expect(result[1]?.layouts[0]?.top).toBe(120 + laneHeight);
  });

  it('only changes the day that actually owns visible all-day rows', () => {
    const item: TimelineAllDayItem = Object.freeze({
      ...spanningItem,
      endDateExclusiveKey: '2026-09-04',
    });
    const laneHeight = timelineAllDayLaneHeightPx(1);
    const result = applyTimelineAllDayGeometry(
      [day('2026-09-03', 0), day('2026-09-04', 1440)],
      [item],
      new Set(),
    );

    expect(result[0]?.height).toBe(1440 + laneHeight);
    expect(result[1]?.offsetTop).toBe(1440 + laneHeight);
    expect(result[1]?.height).toBe(1440);
    expect(result[1]?.mapper.map(0)).toBe(0);
    expect(result[1]?.layouts[0]?.top).toBe(120);
  });

  it('removes all-day geometry when Context filters hide every all-day item', () => {
    const originalDays = [day('2026-09-03', 0), day('2026-09-04', 1440)];
    const result = applyTimelineAllDayGeometry(
      originalDays,
      [spanningItem],
      new Set(['personal']),
    );

    expect(result[0]?.height).toBe(1440);
    expect(result[0]?.mapper.map(0)).toBe(0);
    expect(result[0]?.layouts[0]?.top).toBe(120);
    expect(result[1]?.offsetTop).toBe(1440);
  });

  it('stacks multiple rows without changing the minute scale', () => {
    const secondItem: TimelineAllDayItem = Object.freeze({
      ...spanningItem,
      id: 'all-day:2',
      title: 'Workshop',
    });
    const laneHeight = timelineAllDayLaneHeightPx(2);
    const result = applyTimelineAllDayGeometry(
      [day('2026-09-03', 0)],
      [spanningItem, secondItem],
      new Set(),
    );

    expect(result[0]?.mapper.map(0)).toBe(laneHeight);
    expect(result[0]?.mapper.map(60)).toBe(laneHeight + 60);
    expect(result[0]?.mapper.inv(laneHeight + 60)).toBe(60);
  });
});
