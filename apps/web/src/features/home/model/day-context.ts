import { Temporal } from '@dante/time';

const ISO_DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;
const MINUTES_PER_DAY = 24 * 60;

export type DayRelation = 'past' | 'today' | 'future';

export type DayContextSnapshot = Readonly<{
  viewedDate: Temporal.PlainDate;
  today: Temporal.PlainDate;
  relation: DayRelation;
  zonedNow: Temporal.ZonedDateTime;
  minuteOfDay: number | null;
  progress: number | null;
}>;

export type WeatherCondition =
  | 'clear'
  | 'partly-cloudy'
  | 'cloudy'
  | 'rain'
  | 'storm';

export type DailyWeatherForecast = Readonly<{
  date: Temporal.PlainDate;
  condition: WeatherCondition;
  conditionLabel: string;
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
    condition: 'partly-cloudy',
    conditionLabel: 'Parzialmente nuvoloso',
    highCelsius: 14,
    lowCelsius: 7,
    precipitationPercent: 18,
    sunrise: '07:18',
    sunset: '17:42',
  },
  {
    condition: 'clear',
    conditionLabel: 'Sereno',
    highCelsius: 15,
    lowCelsius: 6,
    precipitationPercent: 8,
    sunrise: '07:17',
    sunset: '17:43',
  },
  {
    condition: 'cloudy',
    conditionLabel: 'Nuvoloso',
    highCelsius: 13,
    lowCelsius: 7,
    precipitationPercent: 26,
    sunrise: '07:16',
    sunset: '17:44',
  },
  {
    condition: 'rain',
    conditionLabel: 'Pioggia',
    highCelsius: 12,
    lowCelsius: 8,
    precipitationPercent: 64,
    sunrise: '07:15',
    sunset: '17:46',
  },
  {
    condition: 'partly-cloudy',
    conditionLabel: 'Variabile',
    highCelsius: 14,
    lowCelsius: 8,
    precipitationPercent: 31,
    sunrise: '07:14',
    sunset: '17:47',
  },
  {
    condition: 'clear',
    conditionLabel: 'Sereno',
    highCelsius: 16,
    lowCelsius: 7,
    precipitationPercent: 9,
    sunrise: '07:13',
    sunset: '17:48',
  },
  {
    condition: 'storm',
    conditionLabel: 'Temporali',
    highCelsius: 13,
    lowCelsius: 7,
    precipitationPercent: 71,
    sunrise: '07:12',
    sunset: '17:49',
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
