import { Temporal, type PlainDate } from '@dante/time';

export type TimelineCalendarLevel = 'days' | 'months' | 'years';

export type TimelineCalendarCursor = Readonly<{
  year: number;
  month: number;
}>;

export function calendarCursorFromDate(date: PlainDate): TimelineCalendarCursor {
  return { year: date.year, month: date.month };
}

export function calendarCursorDate(cursor: TimelineCalendarCursor): PlainDate {
  return Temporal.PlainDate.from({
    year: cursor.year,
    month: cursor.month,
    day: 1,
  });
}

export function shiftCalendarCursorMonth(
  cursor: TimelineCalendarCursor,
  delta: number,
): TimelineCalendarCursor {
  return calendarCursorFromDate(calendarCursorDate(cursor).add({ months: delta }));
}

export function shiftCalendarCursorYear(
  cursor: TimelineCalendarCursor,
  delta: number,
): TimelineCalendarCursor {
  return calendarCursorFromDate(calendarCursorDate(cursor).add({ years: delta }));
}

export function calendarYearPageBase(year: number): number {
  return Math.floor(year / 12) * 12;
}

export function buildCalendarYearPage(year: number): readonly number[] {
  const base = calendarYearPageBase(year);
  return Array.from({ length: 12 }, (_, index) => base + index);
}

export function buildCalendarMonthGrid(
  cursor: TimelineCalendarCursor,
): readonly PlainDate[] {
  const monthStart = calendarCursorDate(cursor);
  const gridStart = monthStart.subtract({ days: monthStart.dayOfWeek - 1 });
  return Array.from({ length: 42 }, (_, index) =>
    gridStart.add({ days: index }),
  );
}

export function moveCalendarDay(date: PlainDate, delta: number): PlainDate {
  return date.add({ days: delta });
}

export function compareCalendarDate(
  left: PlainDate,
  right: PlainDate,
): number {
  return Temporal.PlainDate.compare(left, right);
}
