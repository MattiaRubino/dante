const VIEWBOX_WIDTH = 1000;
const VIEWBOX_HEIGHT = 74;
const BASELINE = 43;
const PRIMARY_CYCLES = 2.25;
const PRIMARY_PHASE = -0.16;
const SECONDARY_PHASE = 0.19;
const SAMPLE_COUNT = 96;

export type DayRouteGeometry = Readonly<{
  path: string;
  viewBox: string;
}>;

export type DayRoutePoint = Readonly<{
  x: number;
  y: number;
  rotation: number;
}>;

type WaveConfig = Readonly<{
  primaryAmplitude: number;
  secondaryAmplitude: number;
}>;

function clamp01(value: number): number {
  return Math.max(0, Math.min(1, value));
}

export function waveConfigForWidth(width: number): WaveConfig {
  if (width <= 460) {
    return { primaryAmplitude: 7.4, secondaryAmplitude: 1.7 };
  }

  if (width <= 760) {
    return { primaryAmplitude: 9.3, secondaryAmplitude: 2.1 };
  }

  return { primaryAmplitude: 11.2, secondaryAmplitude: 2.55 };
}

function routeY(progress: number, width: number): number {
  const p = clamp01(progress);
  const config = waveConfigForWidth(width);
  const primary =
    Math.sin(Math.PI * 2 * (PRIMARY_CYCLES * p + PRIMARY_PHASE)) *
    config.primaryAmplitude;
  const secondary =
    Math.sin(
      Math.PI * 2 * (PRIMARY_CYCLES * 2 * p + SECONDARY_PHASE),
    ) * config.secondaryAmplitude;

  return BASELINE + primary + secondary;
}

export function createDayRouteGeometry(width: number): DayRouteGeometry {
  const safeWidth = Number.isFinite(width) && width > 0 ? width : 900;
  const points = Array.from({ length: SAMPLE_COUNT + 1 }, (_, index) => {
    const progress = index / SAMPLE_COUNT;
    const x = progress * VIEWBOX_WIDTH;
    const y = routeY(progress, safeWidth);
    return `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`;
  });

  return {
    path: points.join(' '),
    viewBox: `0 0 ${VIEWBOX_WIDTH} ${VIEWBOX_HEIGHT}`,
  };
}

export function pointOnDayRoute(
  progress: number,
  width: number,
): DayRoutePoint {
  const p = clamp01(progress);
  const epsilon = 0.001;
  const before = Math.max(0, p - epsilon);
  const after = Math.min(1, p + epsilon);
  const x = p * VIEWBOX_WIDTH;
  const y = routeY(p, width);
  const dx = Math.max(Number.EPSILON, (after - before) * VIEWBOX_WIDTH);
  const dy = routeY(after, width) - routeY(before, width);

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

  return (hours * 60 + minutes) / (24 * 60 - 1);
}
