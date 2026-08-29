import { describe, expect, it } from 'vitest';

import {
  createDayRouteGeometry,
  minuteToProgress,
  pointOnDayRoute,
  waveConfigForWidth,
} from './day-route-geometry';

describe('day route geometry', () => {
  it('uses the prototype responsive wave bands', () => {
    expect(waveConfigForWidth(759)).toMatchObject({
      primaryCycles: 4.6,
      primaryAmplitude: 13.5,
      secondaryAmplitude: 3.2,
    });
    expect(waveConfigForWidth(760)).toMatchObject({
      primaryCycles: 3.7,
      primaryAmplitude: 15,
      secondaryAmplitude: 3.8,
    });
    expect(waveConfigForWidth(1179).primaryCycles).toBe(3.7);
    expect(waveConfigForWidth(1180)).toMatchObject({
      primaryCycles: 2.9,
      primaryAmplitude: 16,
      secondaryAmplitude: 4.2,
    });
  });

  it('generates a finite width-aware path and clamps sampled progress', () => {
    const geometry = createDayRouteGeometry(920);
    const before = pointOnDayRoute(-10, 920);
    const after = pointOnDayRoute(10, 920);

    expect(geometry.viewBox).toBe('0 0 920 74');
    expect(geometry.path.startsWith('M 0.00')).toBe(true);
    expect(geometry.path).not.toMatch(/NaN|Infinity/);
    expect(before.x).toBe(0);
    expect(after.x).toBe(920);
    expect(Number.isFinite(before.rotation)).toBe(true);
  });

  it('maps clock labels onto the 1440-minute day used by the prototype', () => {
    expect(minuteToProgress('12:00')).toBe(0.5);
    expect(minuteToProgress('23:59')).toBeCloseTo(1439 / 1440, 8);
    expect(minuteToProgress('24:00')).toBe(0);
    expect(minuteToProgress('oops')).toBe(0);
  });
});
