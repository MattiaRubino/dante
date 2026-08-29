import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDayContextSnapshot,
  createPrototypeWeeklyForecast,
  normalizeHomeDateSearch,
  shiftIsoDate,
} from './day-context';

describe('day context model', () => {
  const now = Temporal.ZonedDateTime.from(
    '2026-08-29T12:34:00+02:00[Europe/Rome]',
  );

  it('accepts only real canonical ISO calendar dates', () => {
    expect(normalizeHomeDateSearch('2026-08-29')).toBe('2026-08-29');
    expect(normalizeHomeDateSearch('2026-02-30')).toBeUndefined();
    expect(normalizeHomeDateSearch('29-08-2026')).toBeUndefined();
    expect(normalizeHomeDateSearch(20260829)).toBeUndefined();
  });

  it('exposes current-minute progress only for the local today', () => {
    const today = createDayContextSnapshot(undefined, now);
    const past = createDayContextSnapshot('2026-08-28', now);
    const future = createDayContextSnapshot('2026-08-30', now);

    expect(today.relation).toBe('today');
    expect(today.minuteOfDay).toBe(12 * 60 + 34);
    expect(today.progress).toBeCloseTo((12 * 60 + 34) / 1440, 8);
    expect(past.relation).toBe('past');
    expect(past.minuteOfDay).toBeNull();
    expect(past.progress).toBeNull();
    expect(future.relation).toBe('future');
    expect(future.minuteOfDay).toBeNull();
  });

  it('keeps date arithmetic in Temporal calendar space', () => {
    expect(shiftIsoDate('2026-02-28', 1, now.toPlainDate())).toBe('2026-03-01');
    expect(shiftIsoDate(undefined, -1, now.toPlainDate())).toBe('2026-08-28');
    expect(shiftIsoDate('2028-02-28', 1, now.toPlainDate())).toBe('2028-02-29');
    expect(shiftIsoDate('2028-02-29', 1, now.toPlainDate())).toBe('2028-03-01');
    expect(shiftIsoDate('2026-12-31', 1, now.toPlainDate())).toBe('2027-01-01');
  });

  it('creates exactly seven deterministic frontend forecast rows', () => {
    const forecast = createPrototypeWeeklyForecast(
      Temporal.PlainDate.from('2026-08-29'),
    );

    expect(forecast.source).toBe('prototype-fixture');
    expect(forecast.days).toHaveLength(7);
    expect(forecast.days[0]?.date.toString()).toBe('2026-08-29');
    expect(forecast.days[6]?.date.toString()).toBe('2026-09-04');
  });
});
