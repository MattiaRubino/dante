import { Temporal } from '@dante/time';

export const TEMPORAL_CREATE_DURATION_OPTIONS = Object.freeze([
  15, 30, 45, 60, 90, 120, 180, 240, 360, 480,
]);

export const TEMPORAL_CREATE_BUFFER_OPTIONS = Object.freeze([
  0, 5, 10, 15, 20, 30, 45, 60,
]);

export const TEMPORAL_CREATE_REMINDER_OPTIONS: readonly (number | null)[] =
  Object.freeze([null, 0, 5, 10, 15, 30, 60, 120, 1440]);

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

export function temporalCreateEndDateTime(
  startDate: string,
  startTime: string,
  durationMinutes: number,
): Readonly<{ date: string; time: string; dayOffset: number }> {
  const start = plainDateTime(startDate, startTime);
  if (!start) {
    return Object.freeze({ date: startDate, time: '00:00', dayOffset: 0 });
  }
  const end = start.add({ minutes: Math.max(0, durationMinutes) });
  const dayOffset = start.toPlainDate().until(end.toPlainDate()).days;
  return Object.freeze({
    date: end.toPlainDate().toString(),
    time: `${String(end.hour).padStart(2, '0')}:${String(end.minute).padStart(
      2,
      '0',
    )}`,
    dayOffset,
  });
}

export function temporalCreateDurationFromEndDateTime(
  startDate: string,
  startTime: string,
  endDate: string,
  endTime: string,
): number | null {
  const start = plainDateTime(startDate, startTime);
  const end = plainDateTime(endDate, endTime);
  if (!start || !end || Temporal.PlainDateTime.compare(end, start) <= 0) {
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
