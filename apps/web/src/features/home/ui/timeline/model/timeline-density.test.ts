import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  computeTimelineBaseScale,
  computeTimelineDensityMetrics,
  createTimelineTimeMapper,
  timelineEventReadableHeight,
  timelineRulerLabels,
} from './timeline-density';
import { TIMELINE_PROTOTYPE_EVENTS } from './timeline-fixtures';
import { computeTimelineEventLayouts } from './timeline-layout';
import type { TimelineEvent } from './timeline-types';

const denseEvents = TIMELINE_PROTOTYPE_EVENTS['2026-08-04'] ?? [];
const sparseEvents = TIMELINE_PROTOTYPE_EVENTS['2026-08-07'] ?? [];

describe('timeline density engine', () => {
  it('detects real overlap and raises the base scale for denser days', () => {
    const metrics = computeTimelineDensityMetrics(denseEvents);

    expect(metrics.count).toBe(13);
    expect(metrics.maxConcurrent).toBeGreaterThanOrEqual(3);
    expect(metrics.overlapRatio).toBeGreaterThan(0);
    expect(computeTimelineBaseScale(denseEvents)).toBeGreaterThan(
      computeTimelineBaseScale(sparseEvents),
    );
  });

  it('reserves the Activity card content height on the same minute ruler', () => {
    const activity: TimelineEvent = {
      id: 'activity',
      title: 'Focus',
      groupId: 'health',
      startMinute: 600,
      endMinute: 630,
      canonicalBasis: {
        kind: 'scheduled-activity',
        activityRef: 'activity-ref',
        scheduleRef: 'schedule-ref',
        placementMaterialStateRef: 'state-ref',
        placement: {
          kind: 'absolute',
          startsAt: Temporal.Instant.from('2026-10-10T10:00:00Z'),
          endsAt: Temporal.Instant.from('2026-10-10T10:30:00Z'),
        },
      },
    };
    const mapper = createTimelineTimeMapper([activity], 1);
    expect(timelineEventReadableHeight(activity)).toBeGreaterThanOrEqual(88);
    expect(mapper.map(630) - mapper.map(600)).toBeGreaterThanOrEqual(69.99);
    const [layout] = computeTimelineEventLayouts(
      [activity],
      [{ id: 'health', label: 'Salute', tone: 'health' }],
      mapper,
    );
    expect((layout?.top ?? 0) + (layout?.height ?? 0)).toBeCloseTo(
      mapper.map(630),
      5,
    );
  });

  it('only labels quarter-hours with enough elastic pixel separation', () => {
    const quiet = timelineRulerLabels(createTimelineTimeMapper([], 1));
    expect(
      quiet.filter((label) => label.minute >= 600 && label.minute <= 660),
    ).toEqual([
      { minute: 600, minor: false },
      { minute: 660, minor: false },
    ]);
    const mapper = createTimelineTimeMapper(
      [
        {
          id: 'brief',
          title: 'Breve',
          groupId: 'health',
          startMinute: 600,
          endMinute: 615,
        },
      ],
      2,
    );
    const stretched = timelineRulerLabels(mapper);
    const inside = stretched.filter(
      (label) => label.minute >= 600 && label.minute <= 660,
    );
    expect(inside.some((label) => label.minor)).toBe(true);
    expect(
      inside.every(
        (label, index) =>
          index === 0 ||
          mapper.map(label.minute) -
            mapper.map(inside[index - 1]?.minute ?? 0) >=
            28,
      ),
    ).toBe(true);
  });

  it('adds 10:45 inside a genuinely stretched 10:30–11:00 interval', () => {
    const map = (minute: number) =>
      minute <= 630
        ? minute
        : minute <= 660
          ? 630 + (minute - 630) * 3
          : 720 + minute - 660;
    const labels = timelineRulerLabels({
      map,
      inv: (pixel) => pixel,
      height: map(1440),
      pxPerMinute: 1,
    });
    expect(labels.find((label) => label.minute === 645)).toEqual({
      minute: 645,
      minor: true,
    });
  });

  it('reserves a second title row for a long Activity before Session Play', () => {
    const activity: TimelineEvent = {
      id: 'long',
      title:
        'Una attività con un titolo molto lungo che richiede due righe leggibili',
      groupId: 'health',
      startMinute: 600,
      endMinute: 630,
      canonicalBasis: {
        kind: 'scheduled-activity',
        activityRef: 'activity-ref',
        scheduleRef: 'schedule-ref',
        placementMaterialStateRef: 'state-ref',
        placement: {
          kind: 'absolute',
          startsAt: Temporal.Instant.from('2026-10-10T10:00:00Z'),
          endsAt: Temporal.Instant.from('2026-10-10T10:30:00Z'),
        },
      },
    };
    expect(timelineEventReadableHeight(activity)).toBeGreaterThanOrEqual(108);
  });

  it('keeps the nonlinear minute-to-pixel map strictly monotonic', () => {
    const mapper = createTimelineTimeMapper(denseEvents, 1);
    let previous = mapper.map(0);

    for (let minute = 1; minute <= 24 * 60; minute += 1) {
      const current = mapper.map(minute);
      expect(current).toBeGreaterThan(previous);
      previous = current;
    }
  });

  it('round-trips semantic time anchors through the inverse mapper', () => {
    const mapper = createTimelineTimeMapper(denseEvents, 1.35);

    for (const minute of [0, 480, 570, 860, 915, 1170, 1440]) {
      expect(mapper.inv(mapper.map(minute))).toBeCloseTo(minute, 3);
    }
  });

  it('reserves readable space for short events and expanded subitems', () => {
    const reminder = denseEvents.find((event) => event.id === '12');
    const focus = denseEvents.find((event) => event.id === '2');

    expect(reminder).toBeDefined();
    expect(focus).toBeDefined();
    if (!reminder || !focus) {
      return;
    }

    expect(timelineEventReadableHeight(reminder)).toBeGreaterThanOrEqual(68);

    const collapsed = createTimelineTimeMapper(denseEvents, 1);
    const expanded = createTimelineTimeMapper(denseEvents, 1, {
      expandedEventIds: new Set([focus.id]),
    });
    expect(expanded.height).toBeGreaterThan(collapsed.height);
  });
});
