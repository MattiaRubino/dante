import { describe, expect, it } from 'vitest';

import {
  createTimelinePrototypeEventsForDate,
  createTimelinePrototypeStore,
  timelinePrototypeFixturesEnabled,
  timelinePrototypeGroupsForMode,
} from './timeline-fixtures';
import { parseTimelineDate } from './timeline-temporal';

describe('timeline prototype fixture boundary', () => {
  it('enables accepted prototype data only in the explicit test mode', () => {
    expect(timelinePrototypeFixturesEnabled('test')).toBe(true);
    expect(timelinePrototypeFixturesEnabled('production')).toBe(false);
    expect(timelinePrototypeFixturesEnabled('development')).toBe(false);
  });

  it('cannot manufacture normal-runtime cards or product groups', () => {
    expect(timelinePrototypeGroupsForMode('production')).toEqual([]);
    expect(
      createTimelinePrototypeEventsForDate('2034-02-17', 'production'),
    ).toEqual([]);
    expect(
      createTimelinePrototypeStore(
        parseTimelineDate('2034-02-17'),
        'production',
      ),
    ).toEqual({});
  });

  it('keeps the frozen T1 dataset available to explicit tests', () => {
    expect(timelinePrototypeGroupsForMode('test').length).toBeGreaterThan(0);
    expect(
      createTimelinePrototypeEventsForDate('2026-08-04', 'test').some(
        (event) => event.id === '2',
      ),
    ).toBe(true);
  });
});
