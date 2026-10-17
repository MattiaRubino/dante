import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import { createTimelineTimeMapper } from './model/timeline-density';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import type {
  TimelineEvent,
  TimelineGroup,
  TimelineTimeMapper,
} from './model/timeline-types';
import { applyTimelineSessionReality } from './timeline-session-reality';
import type { TimelineRenderedDay } from './timeline-day-stream';
import { buildTimelineRenderedWeek } from './timeline-viewport-runtime';

const groups: readonly TimelineGroup[] = [
  { id: 'area', label: 'Salute', tone: 'health' },
];
const zoom = 1;
const expanded = new Set<string>();
function activity(
  id: string,
  startMinute: number,
  endMinute: number,
): TimelineEvent {
  return {
    id,
    title: 'Allenamento',
    groupId: 'area',
    startMinute,
    endMinute,
    canonicalBasis: {
      kind: 'scheduled-activity',
      activityRef: 'activity-one',
      scheduleRef: id,
      placementMaterialStateRef: `state-${id}`,
      placement: {
        kind: 'absolute',
        startsAt: Temporal.Instant.from('2026-10-10T18:00:00Z'),
        endsAt: Temporal.Instant.from('2026-10-10T19:00:00Z'),
      },
    },
  };
}
function day(...events: TimelineEvent[]): TimelineRenderedDay {
  const mapper: TimelineTimeMapper = createTimelineTimeMapper(events, zoom);
  return {
    date: Temporal.PlainDate.from('2026-10-10'),
    dateKey: '2026-10-10',
    events,
    mapper,
    layouts: computeTimelineEventLayouts(events, groups, mapper),
    height: mapper.height,
    offsetTop: 0,
  };
}
const ended = {
  activity_ref: 'activity-one',
  session_ref: 's1',
  planned_schedule_ref: null,
  started_at: '2026-10-10T17:45:00Z',
  ended_at: '2026-10-10T18:30:00Z',
  pause_ranges: [
    {
      started_at: '2026-10-10T18:00:00Z',
      ended_at: '2026-10-10T18:05:00Z',
    },
  ],
} as const;

describe('one-card Activity actual Session projection', () => {
  it('keeps a Session stopped after a few seconds above the exact now marker', () => {
    const planned = activity('short-session', 20 * 60 + 2, 20 * 60 + 32);
    const [projected] = applyTimelineSessionReality(
      [day(planned)],
      [{
        ...ended,
        started_at: '2026-10-10T19:31:20Z',
        ended_at: '2026-10-10T19:31:25Z',
        pause_ranges: [],
      }],
      'UTC',
      '2026-10-10T19:31:30Z',
      Date.parse('2026-10-10T19:31:30Z'),
      groups,
      zoom,
      expanded,
    );
    const card = projected?.layouts[0];
    expect(card?.sessionReality?.state).toBe('ended');
    // Main Stop after five seconds must keep the title, planned/actual
    // timestamps and both Session/Objective badges readable on one card.
    expect(card?.height).toBeGreaterThanOrEqual(168);
    expect(card?.top).toBeCloseTo(
      projected?.mapper.map(19 * 60 + 31 + 20 / 60) ?? 0,
      3,
    );
    expect((card?.top ?? 0) + (card?.height ?? 0)).toBeLessThanOrEqual(
      (projected?.mapper.map(19 * 60 + 31 + 30 / 60) ?? 0) + 0.001,
    );
    // Five seconds must be mapped continuously between their actual second
    // coordinates. Stretching the entire minute would create a huge day,
    // while a discontinuity at Stop would misrepresent the midpoint.
    const start = 19 * 60 + 31 + 20 / 60;
    const stop = 19 * 60 + 31 + 25 / 60;
    const middle = (start + stop) / 2;
    const mapper = projected?.mapper;
    expect(mapper).toBeDefined();
    if (!mapper) return;
    expect(mapper.map(middle)).toBeCloseTo(
      (mapper.map(start) + mapper.map(stop)) / 2,
      3,
    );
    expect(mapper.inv(mapper.map(middle))).toBeCloseTo(middle, 3);
    expect(
      mapper.map(19 * 60 + 32) - mapper.map(19 * 60 + 31),
    ).toBeLessThan(220);
  });

  it('moves immediately on Play without resizing during Play or Pause', () => {
    const planned = activity('minute-aligned', 600, 630);
    const current = day(planned);
    const visual = {
      ...ended,
      started_at: '2026-10-10T09:08:50Z',
      ended_at: null,
      pause_ranges: [],
    };
    const [projected] = applyTimelineSessionReality(
      [current],
      [visual],
      'UTC',
      '2026-10-10T09:09:10Z',
      Date.parse('2026-10-10T09:09:10Z'),
      groups,
      zoom,
      expanded,
    );
    expect(projected?.layouts[0]?.top).toBeCloseTo(
      current.mapper.map(548 + 50 / 60),
      3,
    );
    expect(projected?.layouts[0]?.height).toBe(current.layouts[0]?.height);
    expect(projected?.layouts[0]?.sessionReality?.actualLabel).toBe(
      '09:08–ora',
    );
  });
  it('reassigns lanes from real painted positions and fits stopped time on the ruler', () => {
    const planned = activity('early-execution', 600, 630);
    const neighbor: TimelineEvent = {
      id: 'other',
      title: 'Vicino',
      groupId: 'area',
      startMinute: 600,
      endMinute: 630,
    };
    const early = {
      ...ended,
      started_at: '2026-10-10T09:49:00Z',
      ended_at: '2026-10-10T09:51:00Z',
      pause_ranges: [],
    };
    const current = day(planned, neighbor);
    const [projected] = applyTimelineSessionReality(
      [current],
      [early],
      'UTC',
      '2026-10-10T10:00:00Z',
      Date.parse('2026-10-10T10:00:00Z'),
      groups,
      zoom,
      expanded,
    );
    const [actual, adjacent] = projected?.layouts ?? [];
    expect(actual?.top).toBeCloseTo(projected?.mapper.map(589) ?? 0, 3);
    expect(actual?.height).toBeGreaterThanOrEqual(70);
    expect((actual?.top ?? 0) + (actual?.height ?? 0)).toBeLessThanOrEqual(
      (projected?.mapper.map(591) ?? 0) + 0.001,
    );
    expect(actual?.event).toBe(planned);
    expect(adjacent?.top).toBeCloseTo(projected?.mapper.map(600) ?? 0, 3);
  });
  it('keeps live Session visual height collision-free after a real-time move', () => {
    const planned = activity('moving', 600, 610);
    const neighbor: TimelineEvent = {
      id: 'neighbor',
      title: 'Appuntamento vicino',
      groupId: 'area',
      startMinute: 635,
      endMinute: 645,
    };
    // Under a denser planned scale the visible Activity was taller than
    // the default short-event minimum. Play moves its top, not its height.
    const basis = day(planned, neighbor);
    const original = basis.layouts.find((layout) => layout.event.id === planned.id)!;
    const crowded: TimelineRenderedDay = {
      ...basis,
      layouts: basis.layouts.map((layout) =>
        layout.event.id === planned.id ? { ...layout, height: 240 } : layout,
      ),
    };
    const [projected] = applyTimelineSessionReality(
      [crowded],
      [
        {
          ...ended,
          started_at: '2026-10-10T09:30:00Z',
          ended_at: null,
          pause_ranges: [],
        },
      ],
      'UTC',
      '2026-10-10T09:32:00Z',
      Date.parse('2026-10-10T09:32:00Z'),
      groups,
      zoom,
      expanded,
    );
    const moving = projected?.layouts.find((layout) => layout.event.id === planned.id);
    const adjacent = projected?.layouts.find((layout) => layout.event.id === neighbor.id);
    expect(original.height).toBeLessThan(240);
    expect(moving?.height).toBe(240);
    expect((moving?.top ?? 0) + (moving?.height ?? 0)).toBeGreaterThan(
      adjacent?.top ?? Infinity,
    );
    expect(moving?.compactLane).not.toBe(adjacent?.compactLane);
    expect(moving?.groupLane).not.toBe(adjacent?.groupLane);
    expect(projected?.mapper).toBe(basis.mapper);
  });

  it('remodulates one Activity card without changing canonical schedule or identity', () => {
    const planned = activity('interval1', 1080, 1140);
    const current = day(planned);
    const [projected] = applyTimelineSessionReality(
      [current],
      [ended],
      'UTC',
      '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'),
      groups,
      zoom,
      expanded,
    );
    const layout = projected?.layouts[0];
    expect(projected?.events).toEqual(current.events);
    expect(layout?.event).toBe(planned);
    expect(layout?.top).toBeCloseTo(projected?.mapper.map(1065) ?? 0, 3);
    // The ended 45-minute execution is shorter than the 60-minute plan,
    // but both intervals hit the new 116px content floor. No longer demand
    // a strict height decrease that would make the card unreadable.
    expect(layout?.height).toBeGreaterThanOrEqual(116);
    expect(layout?.height).toBeLessThanOrEqual(
      (current.layouts[0]?.height ?? Infinity) + 0.001,
    );
    expect(
      (layout?.top ?? 0) + (layout?.height ?? 0),
    ).toBeLessThanOrEqual((projected?.mapper.map(1110) ?? 0) + 0.001);
    expect(layout?.event.startMinute).toBe(1080); // Schedule not rewritten
    expect(layout?.sessionReality?.state).toBe('ended');
    expect(layout?.sessionReality?.fill).toContain('rgba(234, 92, 18, .12)');
    expect(layout?.sessionReality?.fill).toContain('rgba(234, 92, 18');
  });

  it('does not convert the gap between multiple Activity intervals into occupied time', () => {
    const earlier = activity('interval1', 840, 900);
    const later = activity('interval2', 1020, 1080);
    const current = day(earlier, later);
    const [projected] = applyTimelineSessionReality(
      [current],
      [ended],
      'UTC',
      '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'),
      groups,
      zoom,
      expanded,
    );
    expect(projected?.layouts[0]?.top).toBeCloseTo(
      projected?.mapper.map(840) ?? 0,
      3,
    );
    expect(projected?.layouts[1]?.top).toBeCloseTo(
      projected?.mapper.map(1065) ?? 0,
      3,
    );
    expect(projected?.layouts[0]?.sessionReality).toBeUndefined();
    expect(projected?.layouts[1]?.sessionReality?.state).toBe('ended');
  });

  it('does not paint a named Session as the Activity main Session', () => {
    const planned = activity('interval1', 1080, 1140);
    const current = day(planned);
    const child = {
      ...ended,
      session_ref: 'child-session',
      planned_schedule_ref: 'named-plan',
    };
    const [projected] = applyTimelineSessionReality(
      [current],
      [child],
      'UTC',
      '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'),
      groups,
      zoom,
      expanded,
    );
    expect(projected?.layouts[0]?.sessionReality).toBeUndefined();
    expect(projected?.mapper).toBe(current.mapper);
    expect(projected?.height).toBe(current.height);
  });

  it('projects an early main execution into its real day without moving the Schedule', () => {
    const plan = activity('tomorrow-plan', 600, 630);
    const yesterday = {
      ...day(),
      dateKey: '2026-10-09',
      date: Temporal.PlainDate.from('2026-10-09'),
    };
    const tomorrow = {
      ...day(plan),
      offsetTop: yesterday.height,
    };
    const [actualDay, plannedDay] = applyTimelineSessionReality(
      [yesterday, tomorrow],
      [
        {
          ...ended,
          started_at: '2026-10-09T09:00:00Z',
          ended_at: '2026-10-09T09:20:00Z',
          pause_ranges: [],
        },
      ],
      'UTC',
      '2026-10-10T12:00:00Z',
      Date.parse('2026-10-10T12:00:00Z'),
      groups,
      zoom,
      expanded,
    );
    expect(actualDay?.layouts).toHaveLength(1);
    expect(actualDay?.layouts[0]?.top).toBeCloseTo(
      actualDay?.mapper.map(540) ?? 0,
      3,
    );
    expect(actualDay?.layouts[0]?.plannedDateKey).toBe('2026-10-10');
    expect(actualDay?.layouts[0]?.event).toBe(plan);
    expect(plannedDay?.layouts).toHaveLength(0);
    expect(plan.startMinute).toBe(600);
  });

  it('aligns every week column after a short cross-day Stop', () => {
    const plan = activity('week-plan', 600, 630);
    const week = buildTimelineRenderedWeek(
      Temporal.PlainDate.from('2026-10-10'),
      {
        eventsByDate: { '2026-10-10': [plan] },
        groups,
        zoom,
        expandedEventIds: expanded,
      },
    );
    const projected = applyTimelineSessionReality(
      week,
      [
        {
          ...ended,
          started_at: '2026-10-09T09:00:00Z',
          ended_at: '2026-10-09T09:01:00Z',
          pause_ranges: [],
        },
      ],
      'UTC',
      '2026-10-10T12:00:00Z',
      Date.parse('2026-10-10T12:00:00Z'),
      groups,
      zoom,
      expanded,
    );
    const actual = projected.find((day) => day.dateKey === '2026-10-09');
    const planned = projected.find((day) => day.dateKey === '2026-10-10');
    const relocated = actual?.layouts.find(
      (layout) => layout.event.id === plan.id,
    );
    expect(relocated?.plannedDateKey).toBe('2026-10-10');
    expect(planned?.layouts).toHaveLength(0);
    expect(projected.every((day) => day.mapper === actual?.mapper)).toBe(true);
    expect(projected.every((day) => day.offsetTop === 0)).toBe(true);
    expect(
      (relocated?.top ?? 0) + (relocated?.height ?? 0),
    ).toBeLessThanOrEqual((actual?.mapper.map(541) ?? 0) + 0.001);
  });

  it('uses main timing over simultaneous internal execution without adding time twice', () => {
    const planned = activity('interval1', 1080, 1140);
    const child = {
      ...ended,
      session_ref: 's2',
      planned_schedule_ref: 'child-plan',
      started_at: '2026-10-10T18:00:00Z',
      ended_at: '2026-10-10T18:20:00Z',
      pause_ranges: [],
    };
    const current = day(planned);
    const [projected] = applyTimelineSessionReality(
      [current],
      [ended, child],
      'UTC',
      '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'),
      groups,
      zoom,
      expanded,
    );
    const [mainOnly] = applyTimelineSessionReality(
      [current],
      [ended],
      'UTC',
      '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'),
      groups,
      zoom,
      expanded,
    );
    // A named internal Session never increases the outer card duration,
    // changes its true start/end or double-counts the execution.
    expect(projected?.layouts[0]?.top).toBeCloseTo(
      mainOnly?.layouts[0]?.top ?? 0,
      3,
    );
    expect(projected?.layouts[0]?.height).toBeCloseTo(
      mainOnly?.layouts[0]?.height ?? 0,
      3,
    );
    expect(projected?.layouts[0]?.sessionReality?.actualLabel).toBe(
      mainOnly?.layouts[0]?.sessionReality?.actualLabel,
    );
    expect(projected?.layouts[0]?.height).toBeGreaterThanOrEqual(116);
  });

  it('does not stretch a one-minute reality or shift later day offsets', () => {
    const short = activity('short', 600, 630);
    const later: TimelineEvent = {
      id: 'later',
      title: 'Dopo',
      groupId: 'area',
      startMinute: 631,
      endMinute: 660,
    };
    const first = day(short, later);
    const second = {
      ...day(activity('tomorrow', 800, 860)),
      dateKey: '2026-10-11',
      date: Temporal.PlainDate.from('2026-10-11'),
      offsetTop: first.height,
    };
    const [projected, next] = applyTimelineSessionReality(
      [first, second],
      [
        {
          ...ended,
          started_at: '2026-10-10T10:00:00Z',
          ended_at: '2026-10-10T10:01:00Z',
          pause_ranges: [],
        },
      ],
      'UTC',
      '2026-10-10T10:02:00Z',
      Date.parse('2026-10-10T10:02:00Z'),
      groups,
      zoom,
      expanded,
    );
    expect(projected?.layouts[0]?.height).toBeGreaterThanOrEqual(70);
    expect(projected?.layouts[0]?.event.startMinute).toBe(600);
    expect(projected?.layouts[0]?.sessionReality?.actualLabel).toBe(
      '10:00–10:01',
    );
    expect(
      (projected?.layouts[0]?.top ?? 0) + (projected?.layouts[0]?.height ?? 0),
    ).toBeLessThanOrEqual((projected?.mapper.map(601) ?? 0) + 0.001);
    expect(projected?.layouts[1]?.top).toBeCloseTo(
      projected?.mapper.map(631) ?? 0,
      3,
    );
    expect(next?.offsetTop).toBe(projected?.height);
  });
});
