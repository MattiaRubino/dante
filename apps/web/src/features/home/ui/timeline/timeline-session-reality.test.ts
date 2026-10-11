import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import { createTimelineTimeMapper, timelineEventReadableHeight } from './model/timeline-density';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import type { TimelineEvent, TimelineGroup, TimelineTimeMapper } from './model/timeline-types';
import { applyTimelineSessionReality } from './timeline-session-reality';
import type { TimelineRenderedDay } from './timeline-day-stream';

const groups: readonly TimelineGroup[] = [
  { id: 'area', label: 'Salute', tone: 'health' },
];
const zoom = 1;
const expanded = new Set<string>();
function activity(
  id: string, startMinute: number, endMinute: number,
): TimelineEvent {
  return {
    id, title: 'Allenamento', groupId: 'area', startMinute, endMinute,
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
    events, mapper,
    layouts: computeTimelineEventLayouts(events, groups, mapper),
    height: mapper.height, offsetTop: 0,
  };
}
const ended = {
  activity_ref: 'activity-one', session_ref: 's1',
  planned_schedule_ref: null, started_at: '2026-10-10T17:45:00Z',
  ended_at: '2026-10-10T18:30:00Z',
  pause_ranges: [{
    started_at: '2026-10-10T18:00:00Z',
    ended_at: '2026-10-10T18:05:00Z',
  }],
} as const;

describe('one-card Activity actual Session projection', () => {
  it('allocates separate lanes for an early stopped card and a nearby planned card', () => {
    const planned = activity('early-execution', 600, 630);
    const neighbor: TimelineEvent = {
      id: 'other', title: 'Vicino', groupId: 'area',
      startMinute: 600, endMinute: 630,
    };
    const early = {
      ...ended, started_at: '2026-10-10T09:49:00Z',
      ended_at: '2026-10-10T09:51:00Z', pause_ranges: [],
    };
    const [projected] = applyTimelineSessionReality(
      [day(planned, neighbor)], [early], 'UTC', '2026-10-10T10:00:00Z',
      Date.parse('2026-10-10T10:00:00Z'), groups, zoom, expanded,
    );
    const [actual, adjacent] = projected?.layouts ?? [];
    expect(actual?.top).toBe(projected?.mapper.map(589));
    expect(actual?.height).toBeGreaterThanOrEqual(50);
    expect(projected?.height).toBe(projected?.mapper.height);
    expect(actual?.event).toBe(planned);
    expect(
      (actual?.top ?? 0) + (actual?.height ?? 0) <= (adjacent?.top ?? 0) ||
      actual?.compactLane !== adjacent?.compactLane,
    ).toBe(true);
  });
  it('remodulates one Activity card without changing canonical schedule or identity', () => {
    const planned = activity('interval1', 1080, 1140);
    const current = day(planned);
    const [projected] = applyTimelineSessionReality(
      [current], [ended], 'UTC', '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'), groups, zoom, expanded,
    );
    const layout = projected?.layouts[0];
    expect(projected?.events).toBe(current.events);
    expect(layout?.event).toBe(planned);
    expect(layout?.top).toBe(projected?.mapper.map(1065));
    expect(layout?.height).toBeGreaterThanOrEqual(timelineEventReadableHeight({
      ...planned, startMinute: 1065, endMinute: 1110,
    }));
    expect(layout?.event.startMinute).toBe(1080); // Schedule not rewritten
    expect(layout?.sessionReality?.state).toBe('ended');
    expect(layout?.sessionReality?.fill).toContain('rgba(147, 163, 184');
    expect(layout?.sessionReality?.fill).toContain('rgba(234, 92, 18');
  });

  it('does not convert the gap between multiple Activity intervals into occupied time', () => {
    const earlier = activity('interval1', 840, 900);
    const later = activity('interval2', 1020, 1080);
    const current = day(earlier, later);
    const [projected] = applyTimelineSessionReality(
      [current], [ended], 'UTC', '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'), groups, zoom, expanded,
    );
    expect(projected?.layouts[0]?.top).toBe(projected?.mapper.map(840));
    expect(projected?.layouts[1]?.top).toBe(projected?.mapper.map(1065));
    expect(projected?.layouts[0]?.sessionReality).toBeUndefined();
    expect(projected?.layouts[1]?.sessionReality?.state).toBe('ended');
  });

  it('uses main timing over simultaneous internal execution without adding time twice', () => {
    const planned = activity('interval1', 1080, 1140);
    const child = {
      ...ended, session_ref: 's2', planned_schedule_ref: 'child-plan',
      started_at: '2026-10-10T18:00:00Z',
      ended_at: '2026-10-10T18:20:00Z',
      pause_ranges: [],
    };
    const [projected] = applyTimelineSessionReality(
      [day(planned)], [ended, child], 'UTC', '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'), groups, zoom, expanded,
    );
    expect(projected?.layouts[0]?.height).toBeGreaterThanOrEqual(timelineEventReadableHeight({
      ...planned, startMinute: 1065, endMinute: 1110,
    }));
  });

  it('stretches a one-minute reality and shifts later day offsets without changing the plan', () => {
    const short = activity('short', 600, 630);
    const later: TimelineEvent = { id: 'later', title: 'Dopo', groupId: 'area',
      startMinute: 631, endMinute: 660 };
    const first = day(short, later);
    const second = { ...day(activity('tomorrow', 800, 860)), dateKey: '2026-10-11',
      date: Temporal.PlainDate.from('2026-10-11'), offsetTop: first.height };
    const [projected, next] = applyTimelineSessionReality(
      [first, second], [{ ...ended, started_at: '2026-10-10T10:00:00Z',
        ended_at: '2026-10-10T10:01:00Z', pause_ranges: [] }],
      'UTC', '2026-10-10T10:02:00Z', Date.parse('2026-10-10T10:02:00Z'),
      groups, zoom, expanded,
    );
    expect(projected?.layouts[0]?.height).toBeGreaterThanOrEqual(94);
    expect(projected?.layouts[0]?.event.startMinute).toBe(600);
    expect(projected?.layouts[0]?.sessionReality?.actualLabel).toBe('10:00–10:01');
    expect(projected?.layouts[1]?.top).toBeGreaterThanOrEqual(
      (projected?.layouts[0]?.top ?? 0) + (projected?.layouts[0]?.height ?? 0),
    );
    expect(next?.offsetTop).toBe(projected?.height);
  });
});
