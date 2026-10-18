import { Temporal, type PlainDate } from '@dante/time';

import { TIMELINE_MINUTES_PER_DAY } from './timeline-policy';

export function parseTimelineDate(value: string): PlainDate {
  return Temporal.PlainDate.from(value);
}

export function timelineDateKey(date: PlainDate): string {
  return date.toString();
}

export function addTimelineDays(date: PlainDate, days: number): PlainDate {
  return date.add({ days });
}

export function compareTimelineDates(
  left: PlainDate,
  right: PlainDate,
): number {
  return Temporal.PlainDate.compare(left, right);
}

export function startOfIsoWeek(date: PlainDate): PlainDate {
  return date.subtract({ days: date.dayOfWeek - 1 });
}

export function buildIsoWeek(date: PlainDate): readonly PlainDate[] {
  const monday = startOfIsoWeek(date);
  return Array.from({ length: 7 }, (_, index) => monday.add({ days: index }));
}

export function clampTimelineMinute(minute: number): number {
  if (!Number.isFinite(minute)) {
    return 0;
  }

  return Math.max(0, Math.min(TIMELINE_MINUTES_PER_DAY, minute));
}

/** Keep the now ruler on the same sub-minute axis as real Session timestamps. */
export function timelineMinuteOfClock(
  clock: Readonly<{
    hour: number;
    minute: number;
    second: number;
    millisecond: number;
  }>,
): number {
  return (
    clock.hour * 60 +
    clock.minute +
    clock.second / 60 +
    clock.millisecond / 60_000
  );
}

export function formatTimelineMinute(minute: number): string {
  const clamped = Math.round(clampTimelineMinute(minute));
  if (clamped === TIMELINE_MINUTES_PER_DAY) {
    return '24:00';
  }

  const hours = Math.floor(clamped / 60);
  const minutes = clamped % 60;
  return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}`;
}

export function isSameTimelineDate(left: PlainDate, right: PlainDate): boolean {
  return left.equals(right);
}
