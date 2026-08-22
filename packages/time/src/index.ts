import { Temporal } from 'temporal-polyfill';

export { Temporal };

export type Instant = Temporal.Instant;
export type PlainDate = Temporal.PlainDate;
export type PlainTime = Temporal.PlainTime;
export type PlainDateTime = Temporal.PlainDateTime;
export type ZonedDateTime = Temporal.ZonedDateTime;
export type Duration = Temporal.Duration;

export function parseInstant(value: string): Instant {
  return Temporal.Instant.from(value);
}

export function parsePlainDate(value: string): PlainDate {
  return Temporal.PlainDate.from(value);
}

export function parsePlainTime(value: string): PlainTime {
  return Temporal.PlainTime.from(value);
}

export function parsePlainDateTime(value: string): PlainDateTime {
  return Temporal.PlainDateTime.from(value);
}

export function parseZonedDateTime(value: string): ZonedDateTime {
  return Temporal.ZonedDateTime.from(value);
}

export function parseDuration(value: string): Duration {
  return Temporal.Duration.from(value);
}

export function instantToZonedDateTime(
  instant: Instant,
  timeZone: string,
): ZonedDateTime {
  return instant.toZonedDateTimeISO(timeZone);
}

export function zonedDateTimeToInstant(zonedDateTime: ZonedDateTime): Instant {
  return zonedDateTime.toInstant();
}
