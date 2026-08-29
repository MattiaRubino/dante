const VIEWBOX_HEIGHT = 74;
const BASELINE = 31;
const MIN_SAMPLES = 64;
const SAMPLE_STEP_PX = 8;
const MINUTES_PER_DAY = 24 * 60;

export const DAY_ROUTE_HEIGHT = VIEWBOX_HEIGHT;
export const DAY_ROUTE_ROAD_Y = 66;
export const DAY_ROUTE_SCENE_BOTTOM_Y = 60;

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

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value));
}

function normalizeWidth(width: number): number {
  return Number.isFinite(width) && width > 0 ? width : 900;
}

export function waveConfigForWidth(width: number): DayRouteWaveConfig {
  const safeWidth = normalizeWidth(width);
  const primaryCycles = safeWidth < 760 ? 4.6 : safeWidth < 1180 ? 3.7 : 2.9;

  return {
    primaryCycles,
    primaryAmplitude: safeWidth < 760 ? 13.5 : safeWidth < 1180 ? 15 : 16,
    secondaryCycles: primaryCycles * 2.05,
    secondaryAmplitude: safeWidth < 760 ? 3.2 : safeWidth < 1180 ? 3.8 : 4.2,
    primaryPhase: 0.28,
    secondaryPhase: 1.82,
  };
}

function routeY(progress: number, width: number): number {
  const p = clamp01(progress);
  const config = waveConfigForWidth(width);

  return (
    BASELINE -
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
    return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
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
