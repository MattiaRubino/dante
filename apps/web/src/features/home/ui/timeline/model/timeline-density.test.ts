import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createTimelineTimeMapper,
  timelineEventReadableHeight,
  timelineRulerLabels,
} from './timeline-density';
import { TIMELINE_PROTOTYPE_EVENTS } from './timeline-fixtures';
import { computeTimelineEventLayouts } from './timeline-layout';
import type { TimelineEvent } from './timeline-types';

const denseEvents = TIMELINE_PROTOTYPE_EVENTS['2026-08-04'] ?? [];

describe('timeline density engine', () => {
  it('stretches overlapping cards locally while empty hours keep their spacing', () => {
    const cards: TimelineEvent[] = [
      {
        id: 'first',
        title: 'Primo',
        groupId: 'health',
        startMinute: 675,
        endMinute: 705,
      },
      {
        id: 'second',
        title: 'Secondo',
        groupId: 'health',
        startMinute: 690,
        endMinute: 720,
      },
      {
        id: 'third',
        title: 'Terzo',
        groupId: 'health',
        startMinute: 690,
        endMinute: 720,
      },
    ];
    const empty = createTimelineTimeMapper([], 1);
    const withCards = createTimelineTimeMapper(cards, 1);
    const quietHour = empty.map(14 * 60) - empty.map(13 * 60);

    expect(withCards.map(3 * 60) - withCards.map(2 * 60)).toBeCloseTo(
      quietHour,
      5,
    );
    expect(withCards.map(14 * 60) - withCards.map(13 * 60)).toBeCloseTo(
      quietHour,
      5,
    );
    expect(withCards.map(12 * 60) - withCards.map(11 * 60)).toBeGreaterThan(
      quietHour,
    );
    const labels = timelineRulerLabels(withCards);
    expect(labels.some(({ minute, minor }) => minute === 690 && minor)).toBe(
      true,
    );
    expect(labels.some(({ minute, minor }) => minute === 810 && minor)).toBe(
      false,
    );
    for (const zoom of [0.75, 2]) {
      const emptyZoomed = createTimelineTimeMapper([], zoom);
      const populatedZoomed = createTimelineTimeMapper(cards, zoom);
      expect(populatedZoomed.map(840) - populatedZoomed.map(780)).toBeCloseTo(
        emptyZoomed.map(840) - emptyZoomed.map(780),
        5,
      );
    }
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

  it('keeps empty Activity and Event cards compact without hiding richer rows', () => {
    const plain: TimelineEvent = {
      id: 'plain',
      title: 'Poco',
      groupId: 'health',
      startMinute: 600,
      endMinute: 630,
    };
    const activity: TimelineEvent = {
      ...plain,
      canonicalBasis: {
        kind: 'scheduled-activity',
        activityRef: 'activity',
        scheduleRef: 'schedule',
        placementMaterialStateRef: 'state',
        placement: {
          kind: 'absolute',
          startsAt: Temporal.Instant.from('2026-10-10T10:00:00Z'),
          endsAt: Temporal.Instant.from('2026-10-10T10:30:00Z'),
        },
      },
    };
    expect(timelineEventReadableHeight(plain)).toBeLessThan(90);
    expect(timelineEventReadableHeight(activity)).toBeLessThan(130);
    expect(timelineEventReadableHeight(activity)).toBeGreaterThanOrEqual(110);
    expect(
      timelineEventReadableHeight({ ...activity, title: 'X'.repeat(80) }),
    ).toBeGreaterThan(timelineEventReadableHeight(activity));
  });

  it('keeps a 30-minute card compact around a readable overlapping one-minute card', () => {
    const long: TimelineEvent = {
      id: 'long',
      title: 'Intervallo lungo',
      groupId: 'health',
      startMinute: 20 * 60,
      endMinute: 20 * 60 + 30,
      canonicalBasis: {
        kind: 'scheduled-activity',
        activityRef: 'long-activity',
        scheduleRef: 'long-schedule',
        placementMaterialStateRef: 'long-state',
        placement: {
          kind: 'absolute',
          startsAt: Temporal.Instant.from('2026-10-16T18:00:00Z'),
          endsAt: Temporal.Instant.from('2026-10-16T18:30:00Z'),
        },
      },
    };
    const short: TimelineEvent = {
      id: 'short',
      title: 'Un minuto',
      groupId: 'health',
      startMinute: 20 * 60 + 15,
      endMinute: 20 * 60 + 16,
      canonicalBasis: {
        kind: 'scheduled-activity',
        activityRef: 'short-activity',
        scheduleRef: 'short-schedule',
        placementMaterialStateRef: 'short-state',
        placement: {
          kind: 'absolute',
          startsAt: Temporal.Instant.from('2026-10-16T18:15:00Z'),
          endsAt: Temporal.Instant.from('2026-10-16T18:16:00Z'),
        },
      },
    };
    const alone = createTimelineTimeMapper([long], 1);
    const together = createTimelineTimeMapper([long, short], 1);
    const [longLayout, shortLayout] = computeTimelineEventLayouts(
      [long, short],
      [{ id: 'health', label: 'Salute', tone: 'health' }],
      together,
    );
    const longHeight =
      together.map(long.endMinute) - together.map(long.startMinute);

    expect(shortLayout?.height).toBeGreaterThanOrEqual(
      timelineEventReadableHeight(short),
    );
    expect(longLayout?.height).toBeCloseTo(longHeight, 5);
    expect(longHeight).toBeGreaterThan(
      alone.map(long.endMinute) - alone.map(long.startMinute),
    );
    expect(longHeight).toBeLessThan(280);
    expect(together.inv(together.map(short.endMinute))).toBeCloseTo(
      short.endMinute,
      3,
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

  it('retains hourly labels far from activity while showing local elastic and explicit zoom detail', () => {
    const event: TimelineEvent = {
      id: 'late',
      title: 'Attività',
      groupId: 'health',
      startMinute: 12 * 60,
      endMinute: 12 * 60 + 30,
    };
    const mapper = createTimelineTimeMapper([event], 1);
    const labels = timelineRulerLabels(mapper);
    expect(
      labels.filter((label) => label.minute > 5 * 60 && label.minute < 6 * 60),
    ).toEqual([]);
    expect(labels.some((label) => label.minute === 12 * 60 + 15)).toBe(true);
    const zoomed = timelineRulerLabels(createTimelineTimeMapper([], 2), 2);
    expect(zoomed.some((label) => label.minute === 5 * 60 + 30)).toBe(true);
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
