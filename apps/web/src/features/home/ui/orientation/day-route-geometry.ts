const VIEWBOX_HEIGHT = 74;
const BASELINE_RATIO = 0.43;
const SAMPLE_STEP_PX = 5;
const MIN_SAMPLES = 120;
const MINUTES_PER_DAY = 24 * 60;
const ROAD_BOTTOM = 4;
const IMAGE_GAP = 8;

export const DAY_ROUTE_HEIGHT = VIEWBOX_HEIGHT;
export const DAY_ROUTE_BASELINE_Y = VIEWBOX_HEIGHT * BASELINE_RATIO;
export const DAY_ROUTE_ROAD_Y = VIEWBOX_HEIGHT - ROAD_BOTTOM;
export const DAY_ROUTE_SCENE_BOTTOM_Y = DAY_ROUTE_ROAD_Y - IMAGE_GAP;

export type DayRouteGeometry = Readonly<{
  width: number;
  height: number;
  path: string;
  viewBox: string;
}>;

export type DayRoutePoint = Readonly<{
  x: number;
  y: number;
  rotation: number;
}>;

export type DayRouteWaveConfig = Readonly<{
  primaryCycles: number;
  primaryAmplitude: number;
  secondaryCycles: number;
  secondaryAmplitude: number;
  primaryPhase: number;
  secondaryPhase: number;
}>;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function clamp01(value: number): number {
  return clamp(value, 0, 1);
}

function normalizeWidth(width: number): number {
  return Number.isFinite(width) && width > 0 ? width : 900;
}

export function waveConfigForWidth(width: number): DayRouteWaveConfig {
  const safeWidth = normalizeWidth(width);
  const t = clamp((safeWidth - 420) / 900, 0, 1);
  const primaryCycles = 2.25 + t * 2.35;

  return {
    primaryCycles,
    primaryAmplitude: 13.5 + t * 2.5,
    secondaryCycles: primaryCycles * 2,
    secondaryAmplitude: 1.6 + t * 0.9,
    primaryPhase: 0.28,
    secondaryPhase: 1.82,
  };
}

function routeY(progress: number, width: number): number {
  const p = clamp01(progress);
  const config = waveConfigForWidth(width);

  return (
    DAY_ROUTE_BASELINE_Y -
    config.primaryAmplitude *
      Math.sin(Math.PI * 2 * p * config.primaryCycles + config.primaryPhase) -
    config.secondaryAmplitude *
      Math.sin(Math.PI * 2 * p * config.secondaryCycles + config.secondaryPhase)
  );
}

export function createDayRouteGeometry(width: number): DayRouteGeometry {
  const safeWidth = normalizeWidth(width);
  const sampleCount = Math.max(
    MIN_SAMPLES,
    Math.round(safeWidth / SAMPLE_STEP_PX),
  );
  const points = Array.from({ length: sampleCount + 1 }, (_, index) => {
    const progress = index / sampleCount;
    const x = progress * safeWidth;
    const y = routeY(progress, safeWidth);
    return `${index === 0 ? 'M' : 'L'}${x.toFixed(2)},${y.toFixed(2)}`;
  });

  return {
    width: safeWidth,
    height: VIEWBOX_HEIGHT,
    path: points.join(' '),
    viewBox: `0 0 ${safeWidth} ${VIEWBOX_HEIGHT}`,
  };
}

export function pointOnDayRoute(
  progress: number,
  width: number,
): DayRoutePoint {
  const safeWidth = normalizeWidth(width);
  const p = clamp01(progress);
  const epsilon = 0.001;
  const before = Math.max(0, p - epsilon);
  const after = Math.min(1, p + epsilon);
  const x = p * safeWidth;
  const y = routeY(p, safeWidth);
  const dx = Math.max(Number.EPSILON, (after - before) * safeWidth);
  const dy = routeY(after, safeWidth) - routeY(before, safeWidth);

  return {
    x,
    y,
    rotation: (Math.atan2(dy, dx) * 180) / Math.PI,
  };
}

export function minuteToProgress(time: string): number {
  const match = /^(\d{2}):(\d{2})$/.exec(time);
  if (!match) {
    return 0;
  }

  const hours = Number(match[1]);
  const minutes = Number(match[2]);
  if (
    !Number.isInteger(hours) ||
    !Number.isInteger(minutes) ||
    hours < 0 ||
    hours > 23 ||
    minutes < 0 ||
    minutes > 59
  ) {
    return 0;
  }

  return (hours * 60 + minutes) / MINUTES_PER_DAY;
}
