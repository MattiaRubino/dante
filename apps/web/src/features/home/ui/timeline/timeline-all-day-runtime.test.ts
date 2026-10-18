import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import type { TemporalSessionView } from '../../../temporal/remote-session-data-source';
import { timelineAllDayLaneHeightPx } from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineEventLayout,
  TimelineTimeMapper,
} from './model/timeline-types';
import {
  applyTimelineAllDayGeometry,
  projectTimelineDateLaneSessions,
} from './timeline-all-day-runtime';
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

const activityRef = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const activityItem: TimelineAllDayItem = Object.freeze({
  ...spanningItem,
  startDateKey: '2026-10-18',
  endDateExclusiveKey: '2026-10-29',
  canonicalBasis: {
    kind: 'scheduled-activity' as const,
    activityRef,
    scheduleRef: '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d',
    placementMaterialStateRef: '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d',
    placement: {
      kind: 'date-span' as const,
      startDate: Temporal.PlainDate.from('2026-10-18'),
      endDateExclusive: Temporal.PlainDate.from('2026-10-29'),
    },
  },
});

function mainSession(endedAt: string | null): TemporalSessionView {
  return {
    sessionRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
    plannedScheduleRef: null,
    subjectNativeRef: activityRef,
    timingMaterialStateRef: '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d',
    startedAt: '2026-10-19T09:00:00Z',
    endedAt,
    open: endedAt === null,
    paused: false,
    replayed: false,
    evaluatedAt: endedAt ?? '2026-10-19T09:20:00Z',
    elapsedSeconds: 1200,
    activeSeconds: 1200,
    pausedSeconds: 0,
    durationEvaluations: [],
  };
}

describe('Timeline all-day runtime geometry', () => {
  it('keeps the whole planned range during Play and clips future bars on main Stop only', () => {
    const pending = projectTimelineDateLaneSessions(
      [activityItem],
      new Map(),
      'Europe/Rome',
    );
    const active = projectTimelineDateLaneSessions(
      [activityItem],
      new Map([[activityRef, [mainSession(null)]]]),
      'Europe/Rome',
    );
    const stopped = projectTimelineDateLaneSessions(
      [activityItem],
      new Map([[activityRef, [mainSession('2026-10-20T13:03:00Z')]]]),
      'Europe/Rome',
    );

    expect(pending[0]?.endDateExclusiveKey).toBe('2026-10-29');
    expect(active[0]?.endDateExclusiveKey).toBe('2026-10-29');
    expect(active[0]?.mainSession?.state).toBe('running');
    expect(stopped[0]?.endDateExclusiveKey).toBe('2026-10-21');
    expect(stopped[0]?.plannedEndDateExclusiveKey).toBe('2026-10-29');
    expect(stopped[0]?.canonicalBasis).toBe(activityItem.canonicalBasis);
    expect(
      projectTimelineDateLaneSessions(
        [spanningItem],
        new Map([[activityRef, [mainSession('2026-10-20T13:03:00Z')]]]),
        'Europe/Rome',
      )[0],
    ).toBe(spanningItem);
  });

  it('does not retire future bars when only a named internal Session ends', () => {
    const child = {
      ...mainSession('2026-10-20T13:03:00Z'),
      plannedScheduleRef: '0199a8c0-5e76-7bc0-8ad0-a2f403f5617d',
    };
    const [visible] = projectTimelineDateLaneSessions(
      [activityItem],
      new Map([[activityRef, [child]]]),
      'Europe/Rome',
    );
    expect(visible?.endDateExclusiveKey).toBe('2026-10-29');
    expect(visible?.mainSession).toBeUndefined();
  });
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

  it('aligns a week ruler across columns with different numbers of date bars', () => {
    const extra = {
      ...spanningItem,
      id: 'all-day:extra',
      endDateExclusiveKey: '2026-09-04',
    };
    const result = applyTimelineAllDayGeometry(
      [day('2026-09-03', 0), day('2026-09-04', 0)],
      [spanningItem, extra],
      new Set(),
      true,
    );
    expect(result[0]?.mapper.map(0)).toBe(timelineAllDayLaneHeightPx(2));
    expect(result[1]?.mapper.map(0)).toBe(timelineAllDayLaneHeightPx(2));
    expect(result[1]?.layouts[0]?.top).toBe(
      120 + timelineAllDayLaneHeightPx(2),
    );
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
