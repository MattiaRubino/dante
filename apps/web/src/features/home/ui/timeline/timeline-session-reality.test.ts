import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import { timelineEventReadableHeight } from './model/timeline-density';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import type { TimelineEvent, TimelineGroup, TimelineTimeMapper } from './model/timeline-types';
import { applyTimelineSessionReality } from './timeline-session-reality';
import type { TimelineRenderedDay } from './timeline-day-stream';

const groups: readonly TimelineGroup[] = [
  { id: 'area', label: 'Salute', tone: 'health' },
];
const mapper: TimelineTimeMapper = {
  height: 1440, pxPerMinute: 1, map: (value) => value,
  inv: (value) => value,
};
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
  return {
    date: Temporal.PlainDate.from('2026-10-10'),
    dateKey: '2026-10-10',
    events, mapper,
    layouts: computeTimelineEventLayouts(events, groups, mapper),
    height: 1440, offsetTop: 0,
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
  it('remodulates one Activity card without changing canonical schedule or identity', () => {
    const planned = activity('interval1', 1080, 1140);
    const current = day(planned);
    const [projected] = applyTimelineSessionReality(
      [current], [ended], 'UTC', '2026-10-10T18:30:00Z',
      Date.parse('2026-10-10T18:30:00Z'), groups,
    );
    const layout = projected?.layouts[0];
    expect(projected?.events).toBe(current.events);
    expect(layout?.event).toBe(planned);
    expect(layout?.top).toBe(1065);
    expect(layout?.height).toBe(Math.max(45, timelineEventReadableHeight(planned)));
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
      Date.parse('2026-10-10T18:30:00Z'), groups,
    );
    expect(projected?.layouts[0]?.top).toBe(840);
    expect(projected?.layouts[1]?.top).toBe(1020);
    expect(projected?.layouts[0]?.height).toBe(current.layouts[0]?.height);
    expect(projected?.layouts[1]?.height).toBe(current.layouts[1]?.height);
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
      Date.parse('2026-10-10T18:30:00Z'), groups,
    );
    expect(projected?.layouts[0]?.height).toBe(Math.max(45, timelineEventReadableHeight(planned)));
  });
});
