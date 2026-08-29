import { describe, expect, it } from 'vitest';

import {
  createDayRouteGeometry,
  minuteToProgress,
  pointOnDayRoute,
  waveConfigForWidth,
} from './day-route-geometry';

describe('day route geometry', () => {
  it('adapts wave amplitude to available width', () => {
    expect(waveConfigForWidth(320).primaryAmplitude).toBeLessThan(
      waveConfigForWidth(1200).primaryAmplitude,
    );
  });

  it('generates a finite path and clamps sampled progress', () => {
    const geometry = createDayRouteGeometry(920);
    const before = pointOnDayRoute(-10, 920);
    const after = pointOnDayRoute(10, 920);

    expect(geometry.path.startsWith('M 0.00')).toBe(true);
    expect(geometry.path).not.toMatch(/NaN|Infinity/);
    expect(before.x).toBe(0);
    expect(after.x).toBe(1000);
    expect(Number.isFinite(before.rotation)).toBe(true);
  });

  it('maps valid clock labels and rejects malformed values', () => {
    expect(minuteToProgress('12:00')).toBeCloseTo(720 / 1439, 8);
    expect(minuteToProgress('23:59')).toBe(1);
    expect(minuteToProgress('24:00')).toBe(0);
    expect(minuteToProgress('oops')).toBe(0);
  });
});
