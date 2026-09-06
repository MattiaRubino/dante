import { describe, expect, it } from 'vitest';

import { TIMELINE_PROTOTYPE_TODAY } from './model/timeline-fixtures';
import { TIMELINE_POLICY } from './model/timeline-policy';
import { createInitialTimelineState } from './model/timeline-state';
import { addTimelineDays } from './model/timeline-temporal';
import {
  buildTimelineRenderedDays,
  captureTimelineViewportAnchor,
  findTimelineDayAtOffset,
  parseTimelineViewedDate,
  timelineCompactCardWidth,
  timelineExpandedTrackGeometry,
  timelineIntrinsicCardWidth,
  timelineNowViewportOffset,
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

  it('only shrinks a card when the overlap lane is genuinely narrower', () => {
    const isolated = timelineCompactCardWidth(410, 1400, null);
    const constrained = timelineCompactCardWidth(410, 1400, 180);

    expect(constrained).toBe(180);
    expect(constrained).toBeLessThan(isolated);
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
