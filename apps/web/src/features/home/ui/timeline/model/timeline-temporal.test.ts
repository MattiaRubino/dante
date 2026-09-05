import { describe, expect, it } from 'vitest';

import {
  addTimelineDays,
  buildIsoWeek,
  formatTimelineMinute,
  parseTimelineDate,
  startOfIsoWeek,
  timelineDateKey,
} from './timeline-temporal';

describe('timeline temporal model', () => {
  it('keeps calendar-day arithmetic timezone-free across month and year boundaries', () => {
    const date = parseTimelineDate('2026-12-31');

    expect(timelineDateKey(addTimelineDays(date, 1))).toBe('2027-01-01');
    expect(timelineDateKey(addTimelineDays(date, -31))).toBe('2026-11-30');
  });

  it('builds a real ISO Monday-to-Sunday week', () => {
    const date = parseTimelineDate('2026-08-04');
    const week = buildIsoWeek(date).map(timelineDateKey);

    expect(timelineDateKey(startOfIsoWeek(date))).toBe('2026-08-03');
    expect(week).toEqual([
      '2026-08-03',
      '2026-08-04',
      '2026-08-05',
      '2026-08-06',
      '2026-08-07',
      '2026-08-08',
      '2026-08-09',
    ]);
  });

  it('formats minute positions without leaking Date semantics', () => {
    expect(formatTimelineMinute(0)).toBe('00:00');
    expect(formatTimelineMinute(14 * 60 + 20)).toBe('14:20');
    expect(formatTimelineMinute(24 * 60)).toBe('24:00');
    expect(formatTimelineMinute(-50)).toBe('00:00');
  });
});
