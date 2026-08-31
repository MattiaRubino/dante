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
import { TIMELINE_POLICY } from './timeline-policy';
import type { TimelineEvent, TimelineGroup } from './timeline-types';

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

  it('keeps overlapping compact lanes in the same left-to-right order as reordered groups', () => {
    const overlapping: readonly TimelineEvent[] = [
      {
        id: 'focus-card',
        startMinute: 14 * 60,
        endMinute: 15 * 60 + 10,
        title: 'Focus',
        groupId: 'focus',
      },
      {
        id: 'creative-card',
        startMinute: 14 * 60 + 5,
        endMinute: 15 * 60 + 15,
        title: 'Creative',
        groupId: 'creativita',
      },
      {
        id: 'personal-card',
        startMinute: 14 * 60 + 10,
        endMinute: 15 * 60 + 20,
        title: 'Personal',
        groupId: 'personale',
      },
    ];
    const groups: readonly TimelineGroup[] = [
      { id: 'focus', label: 'Focus', tone: 'focus' },
      { id: 'personale', label: 'Personale', tone: 'personal' },
      { id: 'creativita', label: 'Creatività', tone: 'creative' },
    ];

    const first = computeTimelineOverlapLayout(overlapping, groups);
    expect(first.get('focus-card')?.lane).toBeLessThan(
      first.get('personal-card')?.lane ?? -1,
    );
    expect(first.get('personal-card')?.lane).toBeLessThan(
      first.get('creative-card')?.lane ?? -1,
    );

    const reordered = computeTimelineOverlapLayout(overlapping, [
      groups[2]!,
      groups[1]!,
      groups[0]!,
    ]);
    expect(reordered.get('creative-card')?.lane).toBeLessThan(
      reordered.get('personal-card')?.lane ?? -1,
    );
    expect(reordered.get('personal-card')?.lane).toBeLessThan(
      reordered.get('focus-card')?.lane ?? -1,
    );
  });

  it('leaves isolated width to the rendered-content runtime and keeps one compact axis', () => {
    const mapper = createTimelineTimeMapper(events, 1);
    const layouts = computeTimelineEventLayouts(
      events,
      TIMELINE_GROUPS,
      mapper,
    );
    const isolated = layouts.filter((layout) => layout.compactLaneCount === 1);

    expect(isolated.length).toBeGreaterThan(2);
    expect(new Set(isolated.map((layout) => layout.compactLeftPercent)).size).toBe(
      1,
    );
    expect(
      isolated.every((layout) => layout.compactWidthPercent === 0),
    ).toBe(true);
  });

  it('packs small overlap clusters instead of spreading them across the whole timeline', () => {
    const mapper = createTimelineTimeMapper(events, 1);
    const layouts = computeTimelineEventLayouts(
      events,
      TIMELINE_GROUPS,
      mapper,
    );
    const cluster = layouts
      .filter((layout) => ['7', '8', '12'].includes(layout.event.id))
      .sort((left, right) => left.compactLane - right.compactLane);
    const first = cluster[0];
    const last = cluster.at(-1);

    expect(cluster).toHaveLength(3);
    expect(first).toBeDefined();
    expect(last).toBeDefined();
    if (!first || !last) {
      return;
    }

    const spread = last.compactLeftPercent - first.compactLeftPercent;
    expect(spread).toBeCloseTo(
      TIMELINE_POLICY.layout.compactTargetLaneWidthPercent * 2,
      6,
    );
    expect(spread).toBeLessThan(
      TIMELINE_POLICY.layout.compactLaneRegionPercent / 2,
    );
  });

  it('keeps overlap lane widths explicit because collisions constrain geometry', () => {
    const mapper = createTimelineTimeMapper(events, 1);
    const layouts = computeTimelineEventLayouts(
      events,
      TIMELINE_GROUPS,
      mapper,
    );
    const overlapping = layouts.filter((layout) => layout.compactLaneCount > 1);

    expect(overlapping.length).toBeGreaterThan(0);
    expect(
      overlapping.every((layout) => layout.compactWidthPercent > 0),
    ).toBe(true);
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
      expect(layout.compactWidthPercent).toBeGreaterThanOrEqual(0);
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
