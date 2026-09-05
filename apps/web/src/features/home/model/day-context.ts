import { Temporal } from '@dante/time';

const ISO_DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;
const MINUTES_PER_DAY = 24 * 60;

export type DayRelation = 'past' | 'today' | 'future';
export type DayGreetingPeriod = 'morning' | 'afternoon' | 'evening' | 'night';

export type DayContextSnapshot = Readonly<{
  viewedDate: Temporal.PlainDate;
  today: Temporal.PlainDate;
  relation: DayRelation;
  zonedNow: Temporal.ZonedDateTime;
  minuteOfDay: number | null;
  progress: number | null;
}>;

export type WeatherCondition =
  'clear' | 'partly-cloudy' | 'cloudy' | 'rain' | 'storm';

export type DailyWeatherForecast = Readonly<{
  date: Temporal.PlainDate;
  condition: WeatherCondition;
  highCelsius: number;
  lowCelsius: number;
  precipitationPercent: number;
  sunrise: string;
  sunset: string;
}>;

export type WeeklyWeatherForecast = Readonly<{
  source: 'prototype-fixture';
  days: readonly DailyWeatherForecast[];
}>;

const PROTOTYPE_WEATHER: readonly Omit<DailyWeatherForecast, 'date'>[] = [
  {
    condition: 'clear',
    highCelsius: 29,
    lowCelsius: 20,
    precipitationPercent: 8,
    sunrise: '06:17',
    sunset: '19:34',
  },
  {
    condition: 'clear',
    highCelsius: 30,
    lowCelsius: 20,
    precipitationPercent: 6,
    sunrise: '06:18',
    sunset: '19:32',
  },
  {
    condition: 'partly-cloudy',
    highCelsius: 31,
    lowCelsius: 21,
    precipitationPercent: 16,
    sunrise: '06:19',
    sunset: '19:31',
  },
  {
    condition: 'partly-cloudy',
    highCelsius: 28,
    lowCelsius: 20,
    precipitationPercent: 28,
    sunrise: '06:20',
    sunset: '19:29',
  },
  {
    condition: 'rain',
    highCelsius: 27,
    lowCelsius: 19,
    precipitationPercent: 56,
    sunrise: '06:21',
    sunset: '19:28',
  },
  {
    condition: 'clear',
    highCelsius: 29,
    lowCelsius: 19,
    precipitationPercent: 9,
    sunrise: '06:22',
    sunset: '19:26',
  },
  {
    condition: 'storm',
    highCelsius: 26,
    lowCelsius: 18,
    precipitationPercent: 68,
    sunrise: '06:23',
    sunset: '19:25',
  },
];

export function parseHomeDate(value: unknown): Temporal.PlainDate | null {
  if (typeof value !== 'string' || !ISO_DATE_PATTERN.test(value)) {
    return null;
  }

  try {
    return Temporal.PlainDate.from(value);
  } catch {
    return null;
  }
}

export function normalizeHomeDateSearch(value: unknown): string | undefined {
  return parseHomeDate(value)?.toString();
}

export function normalizePreferredName(value: unknown): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }

  const normalized = value.trim().replace(/\s+/g, ' ');
  return normalized.length === 0 ? undefined : normalized;
}

export function getDayGreetingPeriod(hour: number): DayGreetingPeriod {
  if (hour >= 5 && hour < 12) {
    return 'morning';
  }
  if (hour >= 12 && hour < 18) {
    return 'afternoon';
  }
  if (hour >= 18 && hour < 23) {
    return 'evening';
  }
  return 'night';
}

export function resolveTimeZone(candidate?: string): string {
  if (candidate) {
    try {
      Temporal.Now.zonedDateTimeISO(candidate);
      return candidate;
    } catch {
      // Fall through to UTC. Browser-provided IANA names are normally valid.
    }
  }

  return 'UTC';
}

export function getBrowserTimeZone(): string {
  return resolveTimeZone(Intl.DateTimeFormat().resolvedOptions().timeZone);
}

export function createDayContextSnapshot(
  viewedDateIso: string | undefined,
  zonedNow: Temporal.ZonedDateTime,
): DayContextSnapshot {
  const today = zonedNow.toPlainDate();
  const viewedDate = parseHomeDate(viewedDateIso) ?? today;
  const comparison = Temporal.PlainDate.compare(viewedDate, today);
  const relation: DayRelation =
    comparison === 0 ? 'today' : comparison < 0 ? 'past' : 'future';
  const minuteOfDay =
    relation === 'today' ? zonedNow.hour * 60 + zonedNow.minute : null;

  return {
    viewedDate,
    today,
    relation,
    zonedNow,
    minuteOfDay,
    progress:
      minuteOfDay === null
        ? null
        : Math.max(0, Math.min(1, minuteOfDay / MINUTES_PER_DAY)),
  };
}

export function createPrototypeWeeklyForecast(
  anchorDate: Temporal.PlainDate,
): WeeklyWeatherForecast {
  return {
    source: 'prototype-fixture',
    days: PROTOTYPE_WEATHER.map((forecast, index) => ({
      ...forecast,
      date: anchorDate.add({ days: index }),
    })),
  };
}

export function shiftIsoDate(
  isoDate: string | undefined,
  days: number,
  today: Temporal.PlainDate,
): string {
  const base = parseHomeDate(isoDate) ?? today;
  return base.add({ days }).toString();
}
