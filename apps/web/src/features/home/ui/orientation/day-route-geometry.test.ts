import { describe, expect, it } from 'vitest';

import {
  createDayRouteGeometry,
  DAY_ROUTE_BASELINE_Y,
  DAY_ROUTE_ROAD_Y,
  DAY_ROUTE_SCENE_BOTTOM_Y,
  minuteToProgress,
  pointOnDayRoute,
  waveConfigForWidth,
} from './day-route-geometry';

describe('day route geometry', () => {
  it('matches the accepted Round 30 width interpolation', () => {
    expect(waveConfigForWidth(420)).toEqual({
      primaryCycles: 2.25,
      primaryAmplitude: 13.5,
      secondaryCycles: 4.5,
      secondaryAmplitude: 1.6,
      primaryPhase: 0.28,
      secondaryPhase: 1.82,
    });

    const middle = waveConfigForWidth(870);
    expect(middle.primaryCycles).toBeCloseTo(3.425, 10);
    expect(middle.primaryAmplitude).toBeCloseTo(14.75, 10);
    expect(middle.secondaryCycles).toBeCloseTo(6.85, 10);
    expect(middle.secondaryAmplitude).toBeCloseTo(2.05, 10);

    expect(waveConfigForWidth(1320)).toEqual({
      primaryCycles: 4.6,
      primaryAmplitude: 16,
      secondaryCycles: 9.2,
      secondaryAmplitude: 2.5,
      primaryPhase: 0.28,
      secondaryPhase: 1.82,
    });
  });

  it('uses the accepted 74px scene geometry', () => {
    expect(DAY_ROUTE_BASELINE_Y).toBeCloseTo(31.82, 10);
    expect(DAY_ROUTE_ROAD_Y).toBe(70);
    expect(DAY_ROUTE_SCENE_BOTTOM_Y).toBe(62);
  });

  it('generates a finite real-pixel path and clamps sampled progress', () => {
    const geometry = createDayRouteGeometry(920);
    const before = pointOnDayRoute(-10, 920);
    const after = pointOnDayRoute(10, 920);

    expect(geometry.viewBox).toBe('0 0 920 74');
    expect(geometry.path.startsWith('M0.00,')).toBe(true);
    expect(geometry.path).not.toMatch(/NaN|Infinity/);
    expect(before.x).toBe(0);
    expect(after.x).toBe(920);
    expect(Number.isFinite(before.rotation)).toBe(true);
  });

  it('maps clock labels onto the prototype 1440-minute day', () => {
    expect(minuteToProgress('12:00')).toBe(0.5);
    expect(minuteToProgress('23:59')).toBeCloseTo(1439 / 1440, 8);
    expect(minuteToProgress('24:00')).toBe(0);
    expect(minuteToProgress('oops')).toBe(0);
  });
});
