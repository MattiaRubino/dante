import { describe, expect, it } from 'vitest';

import {
  TIMELINE_PROTOTYPE_TODAY,
} from './model/timeline-fixtures';
import { TIMELINE_POLICY } from './model/timeline-policy';
import { createInitialTimelineState } from './model/timeline-state';
import {
  buildTimelineRenderedDays,
  findTimelineDayAtOffset,
  parseTimelineViewedDate,
  timelineNowViewportOffset,
} from './timeline-viewport-runtime';

function buildReferenceDays() {
  const state = createInitialTimelineState(TIMELINE_PROTOTYPE_TODAY);
  return buildTimelineRenderedDays(
    TIMELINE_PROTOTYPE_TODAY,
    TIMELINE_POLICY.window.initialPastDays,
    TIMELINE_POLICY.window.initialFutureDays,
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
    expect(parseTimelineViewedDate('2034-02-17')?.toString()).toBe('2034-02-17');
    expect(parseTimelineViewedDate(undefined)).toBeNull();
    expect(parseTimelineViewedDate('not-a-date')).toBeNull();
  });

  it('builds the bounded Phase 1 day window with cumulative offsets', () => {
    const days = buildReferenceDays();

    expect(days).toHaveLength(
      TIMELINE_POLICY.window.initialPastDays +
        TIMELINE_POLICY.window.initialFutureDays +
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
    expect(findTimelineDayAtOffset(days, Number.MAX_SAFE_INTEGER)?.dateKey).toBe(
      days.at(-1)?.dateKey,
    );
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
});
