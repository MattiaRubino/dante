import { describe, expect, it } from 'vitest';

import { TIMELINE_PROTOTYPE_TODAY } from './model/timeline-fixtures';
import { TIMELINE_POLICY, timelineStableCardWidth } from './model/timeline-policy';
import { computeTimelineEventLayouts } from './model/timeline-layout';
import type { TimelineEvent, TimelineGroup } from './model/timeline-types';
import { createInitialTimelineState } from './model/timeline-state';
import { addTimelineDays } from './model/timeline-temporal';
import {
  applyTimelineExpansion,
  buildTimelineRenderedDays,
  captureTimelineViewportAnchor,
  findTimelineDayAtOffset,
  parseTimelineViewedDate,
  timelineCompactCardWidth,
  timelineExpandedTrackGeometry,
  buildTimelineRenderedWeek,
  timelineIntrinsicCardWidth,
  timelineNowViewportOffset,
  timelinePackedCardGeometry,
  timelineScrollTopForViewportAnchor,
} from './timeline-viewport-runtime';

function buildReferenceDays() {
  const state = createInitialTimelineState(TIMELINE_PROTOTYPE_TODAY);
  return buildTimelineRenderedDays(
    TIMELINE_PROTOTYPE_TODAY,
    TIMELINE_POLICY.window.pastBufferDays,
    TIMELINE_POLICY.window.futureBufferDays,
    {
      eventsByDate: state.eventsByDate,
      groups: state.groups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    },
  );
}

describe('timeline viewport runtime', () => {
  it('parses external view dates defensively', () => {
    expect(parseTimelineViewedDate('2034-02-17')?.toString()).toBe(
      '2034-02-17',
    );
    expect(parseTimelineViewedDate(undefined)).toBeNull();
    expect(parseTimelineViewedDate('not-a-date')).toBeNull();
  });

  it('builds the bounded rolling day window with cumulative offsets', () => {
    const days = buildReferenceDays();

    expect(days).toHaveLength(
      TIMELINE_POLICY.window.pastBufferDays +
        TIMELINE_POLICY.window.futureBufferDays +
        1,
    );
    expect(days[0]?.date.toString()).toBe('2026-08-03');
    expect(days[1]?.date.toString()).toBe('2026-08-04');

    for (let index = 1; index < days.length; index += 1) {
      const previous = days[index - 1];
      const current = days[index];
      expect(previous).toBeDefined();
      expect(current).toBeDefined();
      if (!previous || !current) {
        continue;
      }
      expect(current.offsetTop).toBeCloseTo(
        previous.offsetTop + previous.height,
        6,
      );
    }
  });

  it('places every weekday on one aligned elastic time axis', () => {
    const state = createInitialTimelineState(TIMELINE_PROTOTYPE_TODAY);
    const days = buildTimelineRenderedWeek(TIMELINE_PROTOTYPE_TODAY, {
      eventsByDate: state.eventsByDate,
      groups: state.groups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    });
    expect(days).toHaveLength(7);
    expect(days[0]?.date.dayOfWeek).toBe(1);
    expect(days[6]?.date.dayOfWeek).toBe(7);
    expect(days.every((day) => day.offsetTop === 0)).toBe(true);
    expect(new Set(days.map((day) => day.mapper.map(630))).size).toBe(1);
  });

  it('resolves the semantic day nearest a viewport offset', () => {
    const days = buildReferenceDays();
    const today = days.find((day) => day.date.equals(TIMELINE_PROTOTYPE_TODAY));

    expect(today).toBeDefined();
    if (!today) {
      return;
    }

    expect(findTimelineDayAtOffset(days, today.offsetTop + 1)?.dateKey).toBe(
      today.dateKey,
    );
    expect(findTimelineDayAtOffset(days, -1)?.dateKey).toBe(days[0]?.dateKey);
    expect(
      findTimelineDayAtOffset(days, Number.MAX_SAFE_INTEGER)?.dateKey,
    ).toBe(days.at(-1)?.dateKey);
  });

  it('restores the same semantic viewport point after the rolling window shifts', () => {
    const state = createInitialTimelineState(TIMELINE_PROTOTYPE_TODAY);
    const inputs = {
      eventsByDate: state.eventsByDate,
      groups: state.groups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    };
    const before = buildTimelineRenderedDays(
      TIMELINE_PROTOTYPE_TODAY,
      TIMELINE_POLICY.window.pastBufferDays,
      TIMELINE_POLICY.window.futureBufferDays,
      inputs,
    );
    const targetDay = before.at(-1);
    expect(targetDay).toBeDefined();
    if (!targetDay) {
      return;
    }

    const viewportOffset = 137;
    const originalScrollTop =
      targetDay.offsetTop + targetDay.mapper.map(18 * 60 + 17) - viewportOffset;
    const viewportAnchor = captureTimelineViewportAnchor(
      before,
      originalScrollTop,
      viewportOffset,
    );
    expect(viewportAnchor).not.toBeNull();
    if (!viewportAnchor) {
      return;
    }

    const after = buildTimelineRenderedDays(
      addTimelineDays(
        TIMELINE_PROTOTYPE_TODAY,
        TIMELINE_POLICY.window.shiftByDays,
      ),
      TIMELINE_POLICY.window.pastBufferDays,
      TIMELINE_POLICY.window.futureBufferDays,
      inputs,
    );
    const restoredScrollTop = timelineScrollTopForViewportAnchor(
      after,
      viewportAnchor,
    );
    expect(restoredScrollTop).not.toBeNull();
    if (restoredScrollTop === null) {
      return;
    }

    const restoredAnchor = captureTimelineViewportAnchor(
      after,
      restoredScrollTop,
      viewportOffset,
    );
    expect(restoredAnchor?.dateKey).toBe(viewportAnchor.dateKey);
    expect(restoredAnchor?.minute).toBeCloseTo(viewportAnchor.minute, 6);
    expect(restoredAnchor?.viewportOffset).toBe(viewportOffset);
  });

  it('keeps the mounted window size constant even for distant anchors', () => {
    const state = createInitialTimelineState(TIMELINE_PROTOTYPE_TODAY);
    const inputs = {
      eventsByDate: state.eventsByDate,
      groups: state.groups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    };
    const expectedCount =
      TIMELINE_POLICY.window.pastBufferDays +
      TIMELINE_POLICY.window.futureBufferDays +
      1;

    for (const offset of [-730, -365, -31, 0, 31, 365, 730]) {
      const days = buildTimelineRenderedDays(
        addTimelineDays(TIMELINE_PROTOTYPE_TODAY, offset),
        TIMELINE_POLICY.window.pastBufferDays,
        TIMELINE_POLICY.window.futureBufferDays,
        inputs,
      );
      expect(days).toHaveLength(expectedCount);
      expect(days.every((day) => Number.isFinite(day.height))).toBe(true);
    }
  });

  it('keeps the Now viewport anchor policy-owned', () => {
    const height = TIMELINE_POLICY.viewport.defaultGridHeightPx;
    expect(timelineNowViewportOffset(height)).toBeCloseTo(
      Math.max(
        TIMELINE_POLICY.viewport.nowOffsetMinPx,
        height * TIMELINE_POLICY.viewport.nowOffsetRatio,
      ),
      6,
    );
  });

  it('sizes arbitrary isolated content inside stable responsive bounds', () => {
    const layout = TIMELINE_POLICY.layout;

    expect(timelineIntrinsicCardWidth(40, 1400)).toBe(
      layout.compactIntrinsicMinWidthPx,
    );
    expect(timelineIntrinsicCardWidth(250, 1400)).toBe(
      250 + layout.compactIntrinsicHorizontalBreathingPx,
    );
    expect(timelineIntrinsicCardWidth(4000, 1400)).toBe(
      layout.compactIntrinsicMaxWidthPx,
    );
  });

  it('never lets intrinsic sizing exceed the compact viewport', () => {
    expect(timelineIntrinsicCardWidth(4000, 240)).toBeLessThanOrEqual(240);
    expect(timelineIntrinsicCardWidth(20, 120)).toBe(120);
  });

  it('does not inflate a short card just because it enters an overlap lane', () => {
    const isolated = timelineCompactCardWidth(110, 1400, null);
    const spaciousOverlapLane = timelineCompactCardWidth(110, 1400, 620);

    expect(spaciousOverlapLane).toBe(isolated);
  });

  it('never shrinks a card when a collision lane would be narrower', () => {
    const isolated = timelineCompactCardWidth(410, 1400, null);
    const constrained = timelineCompactCardWidth(410, 1400, 180);

    // The canvas expands horizontally instead of compressing cards.
    expect(constrained).toBe(isolated);
    expect(constrained).toBeGreaterThan(180);
  });

  it('keeps DOM card width invariant as group tracks expand and collision lanes change', () => {
    const previousWidth = window.innerWidth;
    Object.defineProperty(window, 'innerWidth', {
      configurable: true, value: 1440,
    });
    try {
      const root = document.createElement('div');
      root.dataset.timelineView = 'timeline';
      const grid = document.createElement('div');
      Object.defineProperty(grid, 'clientWidth', { configurable: true, value: 980 });
      const stream = document.createElement('div');
      stream.className = 'timeline-day-stream';
      const day = document.createElement('section');
      day.className = 'timeline-day-section';
      stream.appendChild(day);
      root.appendChild(stream);
      root.appendChild(grid);
      const data = [
        { lane: 0, group: 0, groupLane: 0, width: 352 },
        { lane: 1, group: 1, groupLane: 0, width: 292 },
        { lane: 2, group: 1, groupLane: 1, width: 414 },
      ];
      const cards = data.map((entry) => {
        const card = document.createElement('article');
        card.className = 'timeline-event-card';
        card.dataset.compactLane = String(entry.lane);
        card.dataset.compactLanes = '3';
        card.dataset.groupIndex = String(entry.group);
        card.dataset.groupLane = String(entry.groupLane);
        card.dataset.groupLanes = entry.group === 1 ? '2' : '1';
        card.dataset.stableWidth = String(entry.width);
        day.appendChild(card);
        return card;
      });
      for (const progress of [0, 0.25, 0.5, 0.75, 1]) {
        applyTimelineExpansion(root, grid, null, 3, progress);
        for (const [index, card] of cards.entries()) {
          expect(parseFloat(card.style.width)).toBe(data[index]!.width);
        }
        const positions = cards.map((card) => ({
          left: parseFloat(card.style.left),
          width: parseFloat(card.style.width),
        }));
        expect(positions[0]!.left + positions[0]!.width).toBeLessThan(
          positions[1]!.left,
        );
        expect(positions[1]!.left + positions[1]!.width).toBeLessThan(
          positions[2]!.left,
        );
        expect(parseFloat(day.style.minWidth)).toBeGreaterThanOrEqual(980);
        expect(stream.style.minWidth).toBe(day.style.minWidth);
      }
      // Removing a temporal overlap allows lane reuse, never card resizing.
      cards[2]!.dataset.compactLane = '0';
      cards[2]!.dataset.compactLanes = '2';
      cards[2]!.dataset.groupLane = '0';
      cards[2]!.dataset.groupLanes = '1';
      applyTimelineExpansion(root, grid, null, 3, 1);
      expect(parseFloat(cards[2]!.style.width)).toBe(414);
    } finally {
      Object.defineProperty(window, 'innerWidth', {
        configurable: true, value: previousWidth,
      });
    }
  });

  it('uses one identity width for the same Activity across moves and Session transitions', () => {
    const title = 'Allenamento e programma personale molto articolato';
    const expected = timelineStableCardWidth(title, true);
    expect(expected).toBeGreaterThanOrEqual(
      TIMELINE_POLICY.layout.activityCardMinimumWidthPx,
    );
    expect(expected).toBeLessThanOrEqual(
      TIMELINE_POLICY.layout.cardMaximumWidthPx,
    );
    const pitch = expected + TIMELINE_POLICY.layout.cardLaneGapPx;
    for (const lane of [0, 1, 2, 3]) {
      for (const progress of [0, 0.2, 0.5, 0.8, 1]) {
        const card = timelinePackedCardGeometry(
          expected, lane, 1, lane, pitch, 3 * pitch, progress,
        );
        expect(card.width).toBe(expected);
      }
    }
    expect(timelineStableCardWidth('short', false)).toBe(
      TIMELINE_POLICY.layout.eventCardMinimumWidthPx,
    );
    expect(timelineStableCardWidth('x'.repeat(400), true)).toBe(
      TIMELINE_POLICY.layout.cardMaximumWidthPx,
    );
  });

  it('packs simultaneous and short painted cards without overlap at every expansion fraction', () => {
    const groups: readonly TimelineGroup[] = [
      { id: 'work', label: 'Work', tone: 'focus' },
      { id: 'home', label: 'Home', tone: 'personal' },
      { id: 'other', label: 'Other', tone: 'creative' },
    ];
    const source: readonly TimelineEvent[] = [
      { id: 'a', title: 'A', groupId: 'work', startMinute: 720, endMinute: 750 },
      { id: 'b', title: 'B', groupId: 'home', startMinute: 720, endMinute: 750 },
      { id: 'c', title: 'C', groupId: 'home', startMinute: 721, endMinute: 722 },
      { id: 'd', title: 'D', groupId: 'other', startMinute: 722, endMinute: 752 },
      { id: 'e', title: 'E', groupId: 'work', startMinute: 800, endMinute: 825 },
    ];
    const mapper = {
      height: 2880,
      pxPerMinute: 2,
      map: (minute: number) => minute * 2,
      inv: (pixel: number) => pixel / 2,
    };
    // Each move changes the collision cluster without changing the source
    // identity, title or painted minimum height.
    for (const moveTo of [720, 721, 739, 805]) {
      const events = source.map((event) =>
        event.id === 'e'
          ? { ...event, startMinute: moveTo, endMinute: moveTo + 25 }
          : event,
      );
      const layouts = computeTimelineEventLayouts(events, groups, mapper);
      const widths = layouts.map((layout) => timelineStableCardWidth(
        layout.event.title,
        layout.event.canonicalBasis?.kind === 'scheduled-activity',
      ));
      const pitch = Math.max(
        TIMELINE_POLICY.layout.activityCardMinimumWidthPx, ...widths,
      ) + TIMELINE_POLICY.layout.cardLaneGapPx;
      const groupsLanes = Math.max(...layouts.map((layout) => layout.groupLaneCount));
      const groupedWidth = timelineExpandedTrackGeometry(
        1560, groups.length, pitch * groupsLanes,
      ).groupWidth;
      for (const progress of [0, 0.1, 0.25, 0.5, 0.75, 0.9, 1]) {
        const geometries = layouts.map((layout, index) =>
          timelinePackedCardGeometry(
            widths[index]!,
            layout.compactLane,
            layout.groupIndex,
            layout.groupLane,
            pitch,
            groupedWidth,
            progress,
          ),
        );
        for (let left = 0; left < layouts.length; left += 1) {
          for (let right = left + 1; right < layouts.length; right += 1) {
            const a = layouts[left]!;
            const b = layouts[right]!;
            if (a.top >= b.top + b.height || b.top >= a.top + a.height)
              continue;
            const x = geometries[left]!;
            const y = geometries[right]!;
            expect(
              x.left + x.width + 1 <= y.left ||
              y.left + y.width + 1 <= x.left,
              `Overlap at move=${moveTo}, expansion=${progress}, ${a.event.id}/${b.event.id}`,
            ).toBe(true);
          }
        }
      }
    }
  });

  it('widens a group track instead of shrinking two overlapping cards', () => {
    const width = TIMELINE_POLICY.layout.activityCardMinimumWidthPx;
    const pitch = width + TIMELINE_POLICY.layout.cardLaneGapPx;
    const grouped = timelineExpandedTrackGeometry(1100, 4, pitch * 3);
    expect(grouped.groupWidth).toBeGreaterThanOrEqual(pitch * 3);
    expect(grouped.expandedTrackWidth).toBeGreaterThan(1100);
    const left = timelinePackedCardGeometry(width, 0, 2, 0, pitch, grouped.groupWidth, 1);
    const right = timelinePackedCardGeometry(width, 1, 2, 1, pitch, grouped.groupWidth, 1);
    expect(left.width).toBe(width);
    expect(right.width).toBe(width);
    expect(right.left).toBeGreaterThanOrEqual(left.left + width);
  });

  it('keeps expanded header and event canvas on the same scroll range', () => {
    const layout = TIMELINE_POLICY.layout;
    const viewportWidth = 1440;
    const geometry = timelineExpandedTrackGeometry(viewportWidth, 6);
    const gridScrollableWidth = geometry.expandedTrackWidth - viewportWidth;
    const groupScrollerViewportWidth = viewportWidth - layout.eventsLeftInsetPx;
    const headerScrollableWidth =
      geometry.groupHeaderTrackWidth - groupScrollerViewportWidth;

    expect(geometry.chromeWidth).toBe(
      layout.eventsLeftInsetPx + layout.eventsRightInsetPx,
    );
    expect(geometry.groupWidth).toBeGreaterThanOrEqual(layout.groupMinWidthPx);
    expect(headerScrollableWidth).toBeCloseTo(gridScrollableWidth, 6);
  });

  it('distributes expanded columns evenly on wide viewports without header drift', () => {
    const layout = TIMELINE_POLICY.layout;
    const viewportWidth = 1920;
    const geometry = timelineExpandedTrackGeometry(viewportWidth, 6);

    expect(geometry.expandedTrackWidth).toBe(viewportWidth);
    expect(geometry.groupWidth).toBeCloseTo(
      (viewportWidth - layout.eventsLeftInsetPx - layout.eventsRightInsetPx) /
        6,
      6,
    );
    expect(geometry.groupHeaderTrackWidth).toBe(
      geometry.expandedInnerWidth + layout.eventsRightInsetPx,
    );
  });

  it('sanitizes invalid measurement inputs instead of emitting NaN geometry', () => {
    expect(Number.isFinite(timelineIntrinsicCardWidth(Number.NaN, 900))).toBe(
      true,
    );
    expect(
      Number.isFinite(timelineCompactCardWidth(200, Number.NaN, Number.NaN)),
    ).toBe(true);
    expect(
      Number.isFinite(
        timelineExpandedTrackGeometry(Number.NaN, Number.NaN).groupWidth,
      ),
    ).toBe(true);
  });
});
