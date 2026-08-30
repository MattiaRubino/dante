import { describe, expect, it } from 'vitest';

import { createTimelineTimeMapper } from './timeline-density';
import {
  TIMELINE_GROUPS,
  TIMELINE_PROTOTYPE_EVENTS,
} from './timeline-fixtures';
import {
  computeTimelineEventLayouts,
  computeTimelineGaps,
  computeTimelineOverlapLayout,
} from './timeline-layout';

const events = TIMELINE_PROTOTYPE_EVENTS['2026-08-04'] ?? [];

describe('timeline layout engine', () => {
  it('assigns separate lanes to overlapping events and reuses lanes afterwards', () => {
    const overlap = computeTimelineOverlapLayout(events, TIMELINE_GROUPS);
    const study = overlap.get('7');
    const concept = overlap.get('8');
    const reminder = overlap.get('12');

    expect(study?.laneCount).toBeGreaterThanOrEqual(3);
    expect(concept?.laneCount).toBe(study?.laneCount);
    expect(reminder?.laneCount).toBe(study?.laneCount);
    expect(new Set([study?.lane, concept?.lane, reminder?.lane]).size).toBe(3);
  });

  it('creates deterministic compact and grouped geometry from the semantic model', () => {
    const mapper = createTimelineTimeMapper(events, 1);
    const first = computeTimelineEventLayouts(events, TIMELINE_GROUPS, mapper);
    const second = computeTimelineEventLayouts(events, TIMELINE_GROUPS, mapper);

    expect(first).toEqual(second);
    expect(first).toHaveLength(events.length);

    for (const layout of first) {
      expect(layout.top).toBeGreaterThanOrEqual(0);
      expect(layout.height).toBeGreaterThan(0);
      expect(layout.compactLeftPercent).toBeGreaterThanOrEqual(0);
      expect(layout.compactWidthPercent).toBeGreaterThan(0);
      expect(layout.groupIndex).toBeGreaterThanOrEqual(0);
      expect(layout.groupIndex).toBeLessThan(TIMELINE_GROUPS.length);
    }
  });

  it('reports free-time gaps between overlapping clusters rather than between cards', () => {
    const gaps = computeTimelineGaps(events);

    expect(gaps.length).toBeGreaterThan(0);
    expect(gaps.every((gap) => gap.durationMinutes >= 0)).toBe(true);
    expect(
      gaps.some(
        (gap) => gap.fromMinute === 11 * 60 && gap.toMinute === 11 * 60 + 45,
      ),
    ).toBe(true);
  });
});
