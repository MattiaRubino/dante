import { Temporal } from '@dante/time';

import type { TemporalCreateTimeMode } from '../model/temporal-create-session';

export const TEMPORAL_CREATE_DURATION_OPTIONS = Object.freeze([
  15, 30, 45, 60, 90, 120, 180, 240, 360, 480,
]);

export const TEMPORAL_CREATE_BUFFER_OPTIONS = Object.freeze([
  0, 5, 10, 15, 20, 30, 45, 60,
]);

export const TEMPORAL_CREATE_REMINDER_OPTIONS: readonly (number | null)[] =
  Object.freeze([null, 0, 5, 10, 15, 30, 60, 120, 1440]);

const NANOSECONDS_PER_MINUTE = 60_000_000_000n;

export function temporalCreateDurationLabel(minutes: number): string {
  if (minutes < 60) {
    return `${minutes} min`;
  }
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return rest === 0 ? `${hours} h` : `${hours} h ${rest} min`;
}

function parseMinute(value: string): number | null {
  const match = /^(\d{2}):(\d{2})$/.exec(value);
  if (!match) {
    return null;
  }
  const hour = Number(match[1]);
  const minute = Number(match[2]);
  if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
    return null;
  }
  return hour * 60 + minute;
}

function plainDateTime(dateValue: string, timeValue: string) {
  const minute = parseMinute(timeValue);
  if (minute === null) {
    return null;
  }
  try {
    const date = Temporal.PlainDate.from(dateValue);
    return date.toPlainDateTime({
      hour: Math.floor(minute / 60),
      minute: minute % 60,
    });
  } catch {
    return null;
  }
}

function formatPlainDateTime(
  startDate: string,
  start: ReturnType<typeof Temporal.PlainDateTime.from>,
  end: ReturnType<typeof Temporal.PlainDateTime.from>,
): Readonly<{ date: string; time: string; dayOffset: number }> {
  const startDay = Temporal.PlainDate.from(startDate);
  return Object.freeze({
    date: end.toPlainDate().toString(),
    time: `${String(end.hour).padStart(2, '0')}:${String(end.minute).padStart(
      2,
      '0',
    )}`,
    dayOffset: startDay.until(end.toPlainDate()).days,
  });
}

export function temporalCreateEndDateTime(
  startDate: string,
  startTime: string,
  durationMinutes: number,
  timeMode: TemporalCreateTimeMode = 'floating',
  timeZoneId = 'UTC',
): Readonly<{ date: string; time: string; dayOffset: number }> {
  const start = plainDateTime(startDate, startTime);
  if (!start) {
    return Object.freeze({ date: startDate, time: '00:00', dayOffset: 0 });
  }

  try {
    if (timeMode === 'zoned') {
      const zonedStart = start.toZonedDateTime(timeZoneId);
      const zonedEnd = zonedStart.add({
        minutes: Math.max(0, durationMinutes),
      });
      return formatPlainDateTime(
        startDate,
        zonedStart.toPlainDateTime(),
        zonedEnd.toPlainDateTime(),
      );
    }

    const end = start.add({ minutes: Math.max(0, durationMinutes) });
    return formatPlainDateTime(startDate, start, end);
  } catch {
    return Object.freeze({ date: startDate, time: '00:00', dayOffset: 0 });
  }
}

export function temporalCreateDurationFromEndDateTime(
  startDate: string,
  startTime: string,
  endDate: string,
  endTime: string,
  timeMode: TemporalCreateTimeMode = 'floating',
  timeZoneId = 'UTC',
): number | null {
  const start = plainDateTime(startDate, startTime);
  const end = plainDateTime(endDate, endTime);
  if (!start || !end) {
    return null;
  }

  if (timeMode === 'zoned') {
    try {
      const startInstant = start.toZonedDateTime(timeZoneId).toInstant();
      const endInstant = end.toZonedDateTime(timeZoneId).toInstant();
      const elapsedNanoseconds =
        endInstant.epochNanoseconds - startInstant.epochNanoseconds;
      if (elapsedNanoseconds <= 0n) {
        return null;
      }
      return Math.max(5, Number(elapsedNanoseconds / NANOSECONDS_PER_MINUTE));
    } catch {
      return null;
    }
  }

  if (Temporal.PlainDateTime.compare(end, start) <= 0) {
    return null;
  }
  const difference = start.until(end, { largestUnit: 'days' });
  const minutes =
    difference.days * 1440 +
    difference.hours * 60 +
    difference.minutes +
    Math.ceil(difference.seconds / 60);
  return Math.max(5, minutes);
}

export function temporalCreateEndTime(
  startTime: string,
  durationMinutes: number,
): Readonly<{ time: string; dayOffset: number }> {
  const start = parseMinute(startTime) ?? 0;
  const total = start + Math.max(0, durationMinutes);
  const minute = total % 1440;
  return Object.freeze({
    time: `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(
      minute % 60,
    ).padStart(2, '0')}`,
    dayOffset: Math.floor(total / 1440),
  });
}

export function temporalCreateDurationFromEndTime(
  startTime: string,
  endTime: string,
): number | null {
  const start = parseMinute(startTime);
  const end = parseMinute(endTime);
  if (start === null || end === null) {
    return null;
  }
  const delta = end > start ? end - start : end + 1440 - start;
  return Math.max(5, delta);
}
