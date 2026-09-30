import { Temporal } from '@dante/time';
import { useEffect, useMemo, useRef, useState } from 'react';

import './temporal-create-date-picker.css';

type TemporalCreateDatePickerProps = Readonly<{
  label: string;
  value: string;
  locale: string;
  min?: string;
  onChange: (value: string) => void;
}>;

const WEEKDAYS_IT = Object.freeze(['L', 'M', 'M', 'G', 'V', 'S', 'D']);
const WEEKDAYS_EN = Object.freeze(['M', 'T', 'W', 'T', 'F', 'S', 'S']);

function plainDate(value: string): Temporal.PlainDate {
  return Temporal.PlainDate.from(value);
}

function firstDayOfMonth(value: Temporal.PlainDate): Temporal.PlainDate {
  return value.with({ day: 1 });
}

function monthGridStart(month: Temporal.PlainDate): Temporal.PlainDate {
  return month.subtract({ days: month.dayOfWeek - 1 });
}

function compactLabel(value: Temporal.PlainDate, locale: string): string {
  const date = new Date(Date.UTC(value.year, value.month - 1, value.day));
  const parts = new Intl.DateTimeFormat(locale, {
    weekday: 'short',
    day: 'numeric',
    month: 'short',
    ...(value.year === new Date().getUTCFullYear() ? {} : { year: 'numeric' }),
    timeZone: 'UTC',
  }).formatToParts(date);
  const weekday = parts.find((part) => part.type === 'weekday')?.value ?? '';
  const day = parts.find((part) => part.type === 'day')?.value ?? String(value.day);
  const month = parts.find((part) => part.type === 'month')?.value ?? '';
  const year = parts.find((part) => part.type === 'year')?.value;
  return [weekday.replace('.', ''), day, month.replace('.', ''), year]
    .filter(Boolean)
    .join(' ')
    .toLowerCase();
}

function monthLabel(value: Temporal.PlainDate, locale: string): string {
  const date = new Date(Date.UTC(value.year, value.month - 1, 1));
  return new Intl.DateTimeFormat(locale, {
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(date);
}

export function TemporalCreateDatePicker({
  label,
  value,
  locale,
  min,
  onChange,
}: TemporalCreateDatePickerProps) {
  const selected = plainDate(value);
  const minimum = min ? plainDate(min) : null;
  const [open, setOpen] = useState(false);
  const [month, setMonth] = useState(() => firstDayOfMonth(selected));
  const rootRef = useRef<HTMLDivElement | null>(null);
  const italian = locale.toLowerCase().startsWith('it');

  useEffect(() => {
    if (!open) return;
    setMonth(firstDayOfMonth(selected));
  }, [open, value]);

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [open]);

  const days = useMemo(() => {
    const start = monthGridStart(month);
    return Array.from({ length: 42 }, (_, index) => start.add({ days: index }));
  }, [month]);

  return (
    <div ref={rootRef} className="temporal-create-date-picker">
      <button
        className="temporal-create-date-picker__trigger"
        type="button"
        aria-label={`${label}: ${compactLabel(selected, locale)}`}
        aria-expanded={open}
        onClick={() => setOpen((current) => !current)}
      >
        {compactLabel(selected, locale)}
      </button>

      {open ? (
        <div
          className="temporal-create-date-picker__popover"
          role="dialog"
          aria-label={label}
        >
          <header>
            <button
              type="button"
              aria-label={italian ? 'Mese precedente' : 'Previous month'}
              onClick={() => setMonth((current) => current.subtract({ months: 1 }))}
            >
              ‹
            </button>
            <strong>{monthLabel(month, locale)}</strong>
            <button
              type="button"
              aria-label={italian ? 'Mese successivo' : 'Next month'}
              onClick={() => setMonth((current) => current.add({ months: 1 }))}
            >
              ›
            </button>
          </header>
          <div className="temporal-create-date-picker__weekdays" aria-hidden="true">
            {(italian ? WEEKDAYS_IT : WEEKDAYS_EN).map((weekday, index) => (
              <span key={`${weekday}-${index}`}>{weekday}</span>
            ))}
          </div>
          <div className="temporal-create-date-picker__grid">
            {days.map((day) => {
              const disabled =
                minimum !== null && Temporal.PlainDate.compare(day, minimum) < 0;
              const selectedDay = Temporal.PlainDate.compare(day, selected) === 0;
              const outside = day.month !== month.month || day.year !== month.year;
              return (
                <button
                  key={day.toString()}
                  type="button"
                  disabled={disabled}
                  className={`${selectedDay ? 'is-selected ' : ''}${
                    outside ? 'is-outside' : ''
                  }`.trim()}
                  aria-pressed={selectedDay}
                  onClick={() => {
                    onChange(day.toString());
                    setOpen(false);
                  }}
                >
                  {day.day}
                </button>
              );
            })}
          </div>
        </div>
      ) : null}
    </div>
  );
}
