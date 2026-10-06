import { Temporal } from '@dante/time';
import {
  useEffect,
  useRef,
  useState,
  type KeyboardEvent,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateEventCalendarFrequency,
  TemporalCreateFields,
  TemporalCreateKind,
  TemporalCreateRecurrenceOwner,
  TemporalCreateTimeSemantics,
  TemporalCreateWeekday,
} from '../model/temporal-create-session';
import { normalizeTemporalCreateU2EndDate } from '../model/temporal-create-u2-authoring';
import {
  temporalCreateDurationFromEndDateTime,
  temporalCreateDurationLabel,
  temporalCreateEndDateTime,
} from './temporal-create-field-shared';
import { TemporalCreateDatePicker } from './temporal-create-date-picker';
import { TemporalCreateLifeAreaField } from './temporal-create-life-area-field';
import { temporalCreateProductCopy } from './temporal-create-product-copy';
import { TemporalCreateQuickReminder } from './temporal-create-quick-reminder';
import { temporalCreateTypeRegistry } from './temporal-create-type-registry';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

import './temporal-create-core-u2.css';

type Props = Readonly<{
  fields: TemporalCreateFields;
  contexts: readonly TemporalCreateContextOption[];
  showCompactTimezone?: boolean;
  repeatDetails?: ReactNode;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  onRequestAdvanced: (target?: 'recurrence') => void;
  renderError: (path: string) => ReactNode;
}>;

type QuickRecurrence =
  'none' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';

type TimeBand = Readonly<{
  key: 'morning' | 'afternoon' | 'evening' | 'night';
  start: string;
  end: string;
}>;

type TimeControlProps = Readonly<{
  label: string;
  value: string;
  dataPath: string;
  onChange: (value: string) => void;
  helper?: ReactNode;
}>;

const WEEKDAYS: readonly TemporalCreateWeekday[] = Object.freeze([
  'MO',
  'TU',
  'WE',
  'TH',
  'FR',
  'SA',
  'SU',
]);

const TIME_OPTIONS = Object.freeze(
  Array.from({ length: 96 }, (_, index) => {
    const minute = index * 15;
    return `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(
      minute % 60,
    ).padStart(2, '0')}`;
  }),
);

const TIME_BANDS: readonly TimeBand[] = Object.freeze([
  Object.freeze({ key: 'morning', start: '06:00', end: '12:00' }),
  Object.freeze({ key: 'afternoon', start: '12:00', end: '18:00' }),
  Object.freeze({ key: 'evening', start: '18:00', end: '23:00' }),
  Object.freeze({ key: 'night', start: '23:00', end: '06:00' }),
]);

const FALLBACK_TIME_ZONES = Object.freeze([
  'Europe/Rome',
  'Europe/London',
  'Europe/Paris',
  'Europe/Berlin',
  'Europe/Madrid',
  'Europe/Athens',
  'America/New_York',
  'America/Chicago',
  'America/Denver',
  'America/Los_Angeles',
  'America/Sao_Paulo',
  'Asia/Dubai',
  'Asia/Kolkata',
  'Asia/Singapore',
  'Asia/Tokyo',
  'Australia/Sydney',
  'Pacific/Auckland',
  'UTC',
]);

function supportedTimeZones(): readonly string[] {
  const intl = Intl as typeof Intl & {
    supportedValuesOf?: (key: string) => string[];
  };
  try {
    const values = intl.supportedValuesOf?.('timeZone') ?? [];
    if (values.length > 0) {
      return Object.freeze(
        Array.from(new Set(['UTC', ...values])).sort((left, right) =>
          left.localeCompare(right),
        ),
      );
    }
  } catch {
    // Stable fallback for runtimes without Intl.supportedValuesOf.
  }
  return FALLBACK_TIME_ZONES;
}

const TIME_ZONES = supportedTimeZones();

function timeToMinute(value: string): number | null {
  const match = /^(\d{1,2}):(\d{2})$/.exec(value.trim());
  if (!match) return null;
  const hour = Number(match[1]);
  const minute = Number(match[2]);
  return hour >= 0 && hour <= 23 && minute >= 0 && minute <= 59
    ? hour * 60 + minute
    : null;
}

function minuteToTime(value: number): string {
  const minute = ((value % 1440) + 1440) % 1440;
  return `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(
    minute % 60,
  ).padStart(2, '0')}`;
}

function shiftTime(value: string, deltaMinutes: number): string {
  return minuteToTime((timeToMinute(value) ?? 0) + deltaMinutes);
}

function nearestQuarter(value: string): string {
  return minuteToTime(Math.round((timeToMinute(value) ?? 0) / 15) * 15);
}

function weekdayForDate(date: string): TemporalCreateWeekday {
  try {
    return WEEKDAYS[Temporal.PlainDate.from(date).dayOfWeek - 1] ?? 'MO';
  } catch {
    return 'MO';
  }
}

function quickRecurrence(fields: TemporalCreateFields): QuickRecurrence {
  const recurrence = fields.eventRecurrence;
  if (recurrence.patternKind === 'none') return 'none';
  if (
    recurrence.patternKind !== 'calendar-wall-clock' ||
    recurrence.calendarInterval !== 1 ||
    recurrence.calendarFrequency === 'monthly-ordinal'
  ) {
    return 'custom';
  }
  return recurrence.calendarFrequency;
}

function safeAllDayEndDate(startDate: string, currentEndDate: string): string {
  try {
    return Temporal.PlainDate.compare(currentEndDate, startDate) < 0
      ? startDate
      : currentEndDate;
  } catch {
    return startDate;
  }
}

function ClockIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="8" />
      <path d="M12 7v5l3 2" />
    </svg>
  );
}

function GlobeIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="8" />
      <path d="M4 12h16M12 4c2.2 2.1 3.3 4.8 3.3 8S14.2 17.9 12 20M12 4c-2.2 2.1-3.3 4.8-3.3 8S9.8 17.9 12 20" />
    </svg>
  );
}

export function TimeControl({
  label,
  value,
  dataPath,
  onChange,
  helper,
}: TimeControlProps) {
  const parsedValue = timeToMinute(value);
  const normalizedValue =
    parsedValue === null ? '00:00' : minuteToTime(parsedValue);
  const [hourDraft, setHourDraft] = useState(normalizedValue.slice(0, 2));
  const [minuteDraft, setMinuteDraft] = useState(normalizedValue.slice(3, 5));
  const [pickerOpen, setPickerOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const listRef = useRef<HTMLDivElement | null>(null);
  const minuteRef = useRef<HTMLInputElement | null>(null);
  const lastValidRef = useRef(normalizedValue);

  useEffect(() => {
    const parsed = timeToMinute(value);
    if (parsed === null) return;
    const next = minuteToTime(parsed);
    lastValidRef.current = next;
    setHourDraft(next.slice(0, 2));
    setMinuteDraft(next.slice(3, 5));
  }, [value]);

  useEffect(() => {
    if (!pickerOpen) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setPickerOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [pickerOpen]);

  useEffect(() => {
    if (!pickerOpen) return;
    const frame = requestAnimationFrame(() => {
      const selected = nearestQuarter(lastValidRef.current);
      Array.from(
        listRef.current?.querySelectorAll<HTMLElement>('[data-time-value]') ??
          [],
      )
        .find((candidate) => candidate.dataset.timeValue === selected)
        ?.scrollIntoView({ block: 'center' });
    });
    return () => cancelAnimationFrame(frame);
  }, [pickerOpen]);

  const syncDraft = (next: string) => {
    lastValidRef.current = next;
    setHourDraft(next.slice(0, 2));
    setMinuteDraft(next.slice(3, 5));
    onChange(next);
  };

  const restore = () => {
    setHourDraft(lastValidRef.current.slice(0, 2));
    setMinuteDraft(lastValidRef.current.slice(3, 5));
  };

  const commitParts = (hourValue: string, minuteValue: string) => {
    if (!/^\d{1,2}$/.test(hourValue) || !/^\d{1,2}$/.test(minuteValue)) {
      restore();
      return false;
    }
    const hour = Number(hourValue);
    const minute = Number(minuteValue);
    if (hour > 23 || minute > 59) {
      restore();
      return false;
    }
    syncDraft(
      `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`,
    );
    return true;
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      event.preventDefault();
      commitParts(hourDraft, minuteDraft);
      event.currentTarget.blur();
    } else if (event.key === 'Escape') {
      event.preventDefault();
      restore();
      event.currentTarget.blur();
    }
  };

  return (
    <div
      ref={rootRef}
      className="temporal-create-time-control"
      role="group"
      aria-label={label}
    >
      <input
        className="temporal-create-time-raw-input"
        data-create-path={dataPath}
        type="text"
        tabIndex={-1}
        aria-hidden="true"
        value={lastValidRef.current}
        onChange={(event) => {
          const parsed = timeToMinute(event.currentTarget.value);
          if (parsed !== null) syncDraft(minuteToTime(parsed));
        }}
      />
      <div className="temporal-create-time-control__field">
        <div className="temporal-create-inline-time-editor">
          <div className="temporal-create-time-segment">
            <button
              type="button"
              aria-label={`${label}: aumenta ora`}
              onClick={() => syncDraft(shiftTime(lastValidRef.current, 60))}
            >
              ▲
            </button>
            <input
              type="text"
              inputMode="numeric"
              maxLength={2}
              aria-label={`${label}: ore`}
              value={hourDraft}
              onFocus={(event) => {
                setPickerOpen(false);
                event.currentTarget.select();
              }}
              onChange={(event) => {
                const next = event.currentTarget.value;
                if (!/^\d{0,2}$/.test(next)) return;
                setHourDraft(next);
                if (next.length === 2 && Number(next) <= 23) {
                  commitParts(next, minuteDraft);
                  queueMicrotask(() => {
                    minuteRef.current?.focus();
                    minuteRef.current?.select();
                  });
                }
              }}
              onBlur={() => commitParts(hourDraft, minuteDraft)}
              onKeyDown={handleKeyDown}
              autoComplete="off"
              spellCheck="false"
            />
            <button
              type="button"
              aria-label={`${label}: diminuisci ora`}
              onClick={() => syncDraft(shiftTime(lastValidRef.current, -60))}
            >
              ▼
            </button>
          </div>
          <span
            className="temporal-create-inline-time-editor__separator"
            aria-hidden="true"
          >
            :
          </span>
          <div className="temporal-create-time-segment">
            <button
              type="button"
              aria-label={`${label}: aumenta 15 minuti`}
              onClick={() => syncDraft(shiftTime(lastValidRef.current, 15))}
            >
              ▲
            </button>
            <input
              ref={minuteRef}
              type="text"
              inputMode="numeric"
              maxLength={2}
              aria-label={`${label}: minuti`}
              value={minuteDraft}
              onFocus={(event) => {
                setPickerOpen(false);
                event.currentTarget.select();
              }}
              onChange={(event) => {
                const next = event.currentTarget.value;
                if (!/^\d{0,2}$/.test(next)) return;
                setMinuteDraft(next);
                if (next.length === 2 && Number(next) <= 59) {
                  commitParts(hourDraft, next);
                }
              }}
              onBlur={() => commitParts(hourDraft, minuteDraft)}
              onKeyDown={handleKeyDown}
              autoComplete="off"
              spellCheck="false"
            />
            <button
              type="button"
              aria-label={`${label}: diminuisci 15 minuti`}
              onClick={() => syncDraft(shiftTime(lastValidRef.current, -15))}
            >
              ▼
            </button>
          </div>
        </div>
        <button
          className="temporal-create-clock-trigger"
          type="button"
          aria-label={`${label}: scegli orario`}
          aria-expanded={pickerOpen}
          onClick={() => setPickerOpen((current) => !current)}
        >
          <ClockIcon />
        </button>
      </div>
      {helper ? <small>{helper}</small> : null}
      {pickerOpen ? (
        <div
          className="temporal-create-time-picker"
          role="dialog"
          aria-label={label}
        >
          <div ref={listRef} className="temporal-create-time-list">
            {TIME_OPTIONS.map((option) => (
              <button
                key={option}
                type="button"
                data-time-value={option}
                className={
                  nearestQuarter(lastValidRef.current) === option
                    ? 'is-selected'
                    : ''
                }
                onClick={() => {
                  syncDraft(option);
                  setPickerOpen(false);
                }}
              >
                {option}
              </button>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}

export function TemporalCreateCoreFieldsU2({
  fields,
  contexts,
  showCompactTimezone = true,
  repeatDetails,
  onPatch,
  onRequestAdvanced,
  renderError,
}: Props) {
  const { t, i18n } = useTranslation('common');
  const { draft: authoringDraft, patch: patchAuthoring } =
    useTemporalCreateU2Draft();
  const copy = temporalCreateProductCopy(
    i18n.resolvedLanguage ?? i18n.language,
  );
  const locale = i18n.resolvedLanguage ?? i18n.language ?? 'it';
  const italian = locale.toLowerCase().startsWith('it');
  const typeRegistry = temporalCreateTypeRegistry();
  const [timeZoneOpen, setTimeZoneOpen] = useState(false);
  const [timeBandOpen, setTimeBandOpen] = useState(false);
  const timeZoneRootRef = useRef<HTMLDivElement | null>(null);
  const timeBandRootRef = useRef<HTMLDivElement | null>(null);
  const recurrenceOwner: Exclude<TemporalCreateRecurrenceOwner, null> =
    fields.kind === 'event' ? 'event' : 'routine';

  const patchEvent = (patch: Partial<TemporalCreateFields['event']>) =>
    onPatch({ event: { ...fields.event, ...patch } });

  const patchActivityIntervals = (
    intervals: typeof authoringDraft.activityStructure.activityIntervals,
  ) =>
    patchAuthoring({
      activityStructure: Object.freeze({
        ...authoringDraft.activityStructure,
        activityIntervals: intervals,
      }),
    });

  const addActivityInterval = () => {
    const last = authoringDraft.activityStructure.activityIntervals.at(-1);
    const after = last
      ? Temporal.PlainDateTime.from(`${last.endDate}T${last.endTime}`).add({
          minutes: 30,
        })
      : Temporal.PlainDateTime.from(`${fields.date}T${fields.startTime}`).add({
          minutes: fields.durationMinutes + 30,
        });
    const end = after.add({ hours: 1 });
    patchActivityIntervals([
      ...authoringDraft.activityStructure.activityIntervals,
      Object.freeze({
        id: globalThis.crypto.randomUUID(),
        date: after.toPlainDate().toString(),
        startTime: after.toPlainTime().toString({ smallestUnit: 'minute' }),
        endDate: end.toPlainDate().toString(),
        endTime: end.toPlainTime().toString({ smallestUnit: 'minute' }),
      }),
    ]);
  };

  const updateActivityInterval = (
    id: string,
    changes: Partial<
      (typeof authoringDraft.activityStructure.activityIntervals)[number]
    >,
  ) =>
    patchActivityIntervals(
      authoringDraft.activityStructure.activityIntervals.map((interval) =>
        interval.id === id
          ? Object.freeze({ ...interval, ...changes })
          : interval,
      ),
    );

  useEffect(() => {
    if (!timeZoneOpen) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !timeZoneRootRef.current?.contains(event.target)
      ) {
        setTimeZoneOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [timeZoneOpen]);

  useEffect(() => {
    if (!timeBandOpen) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !timeBandRootRef.current?.contains(event.target)
      ) {
        setTimeBandOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [timeBandOpen]);

  const changeKind = (kind: TemporalCreateKind) => {
    if (kind === fields.kind) return;
    if (
      kind !== 'activity' &&
      authoringDraft.activityStructure.activityIntervals.length > 0
    )
      return;
    const targetOwner = kind === 'event' ? 'event' : 'routine';
    const eventRecurrence = {
      ...fields.eventRecurrence,
      owner: fields.eventRecurrence.patternKind === 'none' ? null : targetOwner,
    } as const;
    if (kind === 'event') {
      onPatch({
        kind,
        timeSemantics:
          fields.timeSemantics === 'coarse' ? 'timed' : fields.timeSemantics,
        scheduling: {
          ...fields.scheduling,
          constraintKind: 'none',
          fallbackPolicy: 'inherit',
        },
        eventRecurrence,
      });
      return;
    }
    onPatch({ kind, eventRecurrence });
  };

  const changeTimeSemantics = (semantics: TemporalCreateTimeSemantics) => {
    if (
      semantics === 'all-day' &&
      fields.kind === 'activity' &&
      authoringDraft.activityStructure.activityIntervals.length > 0
    ) {
      patchActivityIntervals([]);
    }

    onPatch({
      timeSemantics: semantics,
      scheduling:
        semantics === 'unscheduled'
          ? { ...fields.scheduling, constraintKind: 'none' }
          : {
              ...fields.scheduling,
              constraintKind: 'none',
              fallbackPolicy: 'inherit',
            },
      ...(semantics === 'unscheduled'
        ? {
            eventRecurrence: {
              ...fields.eventRecurrence,
              owner: null,
              patternKind: 'none' as const,
            },
          }
        : {}),
    });
  };

  const calculatedEnd = temporalCreateEndDateTime(
    fields.date,
    fields.startTime,
    fields.durationMinutes,
    fields.timeMode,
    fields.timeZoneId,
  );
  const visibleEndDate = normalizeTemporalCreateU2EndDate(
    fields.date,
    authoringDraft.endDate,
  );
  const visibleAllDayEndDate =
    fields.kind === 'event'
      ? safeAllDayEndDate(fields.date, fields.event.allDayEndDate)
      : safeAllDayEndDate(fields.date, authoringDraft.endDate);

  const patchEnd = (endDate: string, endTime: string) => {
    const normalizedEndDate = normalizeTemporalCreateU2EndDate(
      fields.date,
      endDate,
    );
    const duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      fields.startTime,
      normalizedEndDate,
      endTime,
      fields.timeMode,
      fields.timeZoneId,
    );
    patchAuthoring({ endDate: normalizedEndDate });
    if (duration !== null) onPatch({ durationMinutes: duration });
  };

  const patchStartDate = (date: string) => {
    const endDate = normalizeTemporalCreateU2EndDate(date, visibleEndDate);
    const duration = temporalCreateDurationFromEndDateTime(
      date,
      fields.startTime,
      endDate,
      calculatedEnd.time,
      fields.timeMode,
      fields.timeZoneId,
    );
    patchAuthoring({ endDate });
    onPatch({
      date,
      ...(duration === null ? {} : { durationMinutes: duration }),
    });
  };

  const patchAllDayStartDate = (date: string) => {
    const endDate = safeAllDayEndDate(date, visibleAllDayEndDate);
    if (fields.kind === 'event') {
      onPatch({
        date,
        event: { ...fields.event, allDayEndDate: endDate },
      });
      return;
    }
    patchAuthoring({ endDate });
    onPatch({ date });
  };

  const patchAllDayEndDate = (date: string) => {
    const endDate = safeAllDayEndDate(fields.date, date);
    if (fields.kind === 'event') {
      patchEvent({ allDayEndDate: endDate });
      return;
    }
    patchAuthoring({ endDate });
  };

  const patchStartTime = (startTime: string) => {
    let endDate = visibleEndDate;
    let duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      startTime,
      endDate,
      calculatedEnd.time,
      fields.timeMode,
      fields.timeZoneId,
    );
    if (duration === null) {
      try {
        endDate = Temporal.PlainDate.from(endDate).add({ days: 1 }).toString();
        duration = temporalCreateDurationFromEndDateTime(
          fields.date,
          startTime,
          endDate,
          calculatedEnd.time,
          fields.timeMode,
          fields.timeZoneId,
        );
      } catch {
        duration = null;
      }
    }
    patchAuthoring({ endDate });
    onPatch({
      startTime,
      ...(duration === null ? {} : { durationMinutes: duration }),
    });
  };

  const bandLabels: Readonly<Record<TimeBand['key'], string>> = italian
    ? {
        morning: 'Mattina',
        afternoon: 'Pomeriggio',
        evening: 'Sera',
        night: 'Notte',
      }
    : {
        morning: 'Morning',
        afternoon: 'Afternoon',
        evening: 'Evening',
        night: 'Night',
      };

  const applyTimeBand = (band: TimeBand) => {
    const startMinute = timeToMinute(band.start) ?? 0;
    const endMinute = timeToMinute(band.end) ?? 0;
    const endDate =
      endMinute <= startMinute
        ? Temporal.PlainDate.from(fields.date).add({ days: 1 }).toString()
        : fields.date;
    const duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      band.start,
      endDate,
      band.end,
      fields.timeMode,
      fields.timeZoneId,
    );
    patchAuthoring({ endDate });
    if (duration !== null)
      onPatch({ startTime: band.start, durationMinutes: duration });
    setTimeBandOpen(false);
  };

  const changeQuickRecurrence = (value: QuickRecurrence) => {
    if (value === 'custom') {
      onPatch({
        eventRecurrence:
          fields.eventRecurrence.patternKind === 'none'
            ? {
                ...fields.eventRecurrence,
                owner: recurrenceOwner,
                patternKind: 'calendar-wall-clock',
                calendarFrequency: 'weekly',
                calendarInterval: 1,
                weekdays: Object.freeze([weekdayForDate(fields.date)]),
              }
            : { ...fields.eventRecurrence, owner: recurrenceOwner },
      });
      onRequestAdvanced('recurrence');
      return;
    }
    if (value === 'none') {
      onPatch({
        eventRecurrence: {
          ...fields.eventRecurrence,
          owner: null,
          patternKind: 'none',
        },
      });
      return;
    }
    const frequency = value satisfies TemporalCreateEventCalendarFrequency;
    onPatch({
      eventRecurrence: {
        ...fields.eventRecurrence,
        owner: recurrenceOwner,
        patternKind: 'calendar-wall-clock',
        calendarFrequency: frequency,
        calendarInterval: 1,
        weekdays:
          frequency === 'weekly'
            ? Object.freeze([weekdayForDate(fields.date)])
            : fields.eventRecurrence.weekdays,
      },
    });
  };

  const timeZoneLabel =
    fields.timeMode === 'floating'
      ? italian
        ? 'Ora locale'
        : 'Local time'
      : fields.timeZoneId;

  return (
    <>
      <fieldset className="temporal-create-type-fieldset">
        <legend className="temporal-create-visually-hidden">
          {copy.typeLabel}
        </legend>
        <div className="temporal-create-type-grid is-four">
          {typeRegistry.map((descriptor) => (
            <button
              key={descriptor.kind}
              type="button"
              role="radio"
              aria-checked={fields.kind === descriptor.kind}
              disabled={
                descriptor.kind !== 'activity' &&
                authoringDraft.activityStructure.activityIntervals.length > 0
              }
              title={
                descriptor.kind !== 'activity' &&
                authoringDraft.activityStructure.activityIntervals.length > 0
                  ? italian
                    ? 'Rimuovi prima gli intervalli aggiuntivi'
                    : 'Remove the additional intervals first'
                  : undefined
              }
              className={fields.kind === descriptor.kind ? 'is-active' : ''}
              onClick={() => changeKind(descriptor.kind)}
            >
              <strong>
                {descriptor.kind === 'activity' ? 'Attività' : 'Evento'}
              </strong>
            </button>
          ))}
          <button type="button" className="is-deferred" disabled>
            <strong>Timer</strong>
            <small>Prossimamente</small>
          </button>
          <button type="button" className="is-deferred" disabled>
            <strong>Sveglia</strong>
            <small>Prossimamente</small>
          </button>
        </div>
      </fieldset>

      <fieldset
        className="temporal-create-choice-group"
        data-create-path="timeSemantics"
      >
        <legend className="temporal-create-visually-hidden">
          Collocazione
        </legend>
        <div className="temporal-create-choice-row">
          <button
            type="button"
            role="radio"
            aria-checked={fields.timeSemantics === 'timed'}
            className={fields.timeSemantics === 'timed' ? 'is-active' : ''}
            onClick={() => changeTimeSemantics('timed')}
          >
            Orario
          </button>
          <button
            type="button"
            role="radio"
            aria-checked={fields.timeSemantics === 'all-day'}
            className={fields.timeSemantics === 'all-day' ? 'is-active' : ''}
            onClick={() => changeTimeSemantics('all-day')}
          >
            Tutto il giorno
          </button>
          <button
            type="button"
            role="radio"
            aria-checked={fields.timeSemantics === 'unscheduled'}
            className={
              fields.timeSemantics === 'unscheduled' ? 'is-active' : ''
            }
            disabled={
              fields.kind === 'activity' &&
              authoringDraft.activityStructure.activityIntervals.length > 0
            }
            title={
              fields.kind === 'activity' &&
              authoringDraft.activityStructure.activityIntervals.length > 0
                ? 'Rimuovi prima gli intervalli aggiuntivi'
                : undefined
            }
            onClick={() => changeTimeSemantics('unscheduled')}
          >
            Da collocare
          </button>
        </div>
      </fieldset>
      {renderError('timeSemantics')}

      {fields.timeSemantics === 'timed' ? (
        <div className="temporal-create-u2-when">
          <div
            ref={timeZoneRootRef}
            className="temporal-create-timezone-control"
          >
            <button
              className={`temporal-create-timezone-trigger${timeZoneOpen ? ' is-open' : ''}`}
              type="button"
              aria-label={`Fuso orario: ${timeZoneLabel}`}
              aria-expanded={timeZoneOpen}
              title={timeZoneLabel}
              onClick={() => setTimeZoneOpen((current) => !current)}
            >
              <GlobeIcon />
              <span className="temporal-create-timezone-divider" aria-hidden="true" />
              <span className="temporal-create-timezone-label">
                {italian ? 'Fuso orario' : 'Time zone'} · {timeZoneLabel}
              </span>
              <span className="temporal-create-timezone-chevron" aria-hidden="true">
                {timeZoneOpen ? '⌃' : '⌄'}
              </span>
            </button>
            {timeZoneOpen ? (
              <div className="temporal-create-timezone-panel">
                <div className="temporal-create-timezone-current">
                  <GlobeIcon />
                  <span>{timeZoneLabel}</span>
                </div>
                <div className="temporal-create-timezone-list">
                  <button
                    type="button"
                    className={
                      fields.timeMode === 'floating' ? 'is-selected' : ''
                    }
                    onClick={() => {
                      onPatch({ timeMode: 'floating' });
                      setTimeZoneOpen(false);
                    }}
                  >
                    Ora locale
                  </button>
                  {TIME_ZONES.map((zoneId) => (
                    <button
                      key={zoneId}
                      type="button"
                      className={
                        fields.timeMode === 'zoned' &&
                        fields.timeZoneId === zoneId
                          ? 'is-selected'
                          : ''
                      }
                      onClick={() => {
                        onPatch({ timeMode: 'zoned', timeZoneId: zoneId });
                        setTimeZoneOpen(false);
                      }}
                    >
                      {zoneId.replaceAll('_', ' ')}
                    </button>
                  ))}
                </div>
              </div>
            ) : null}
          </div>

          <input
            className="temporal-create-u2-date-bridge"
            data-create-path="date"
            aria-hidden="true"
            tabIndex={-1}
            value={fields.date}
            onChange={(event) => patchStartDate(event.currentTarget.value)}
          />

          <TemporalCreateDatePicker
            label={italian ? 'Data inizio' : 'Start date'}
            value={fields.date}
            locale={locale}
            onChange={patchStartDate}
          />

          <TimeControl
            label={italian ? 'Inizio' : 'Start'}
            value={fields.startTime}
            dataPath="startTime"
            onChange={patchStartTime}
            helper={renderError('startTime')}
          />

          <div
            ref={timeBandRootRef}
            className="temporal-create-time-band-control"
          >
            <button
              type="button"
              className="temporal-create-time-band-trigger"
              aria-label="Fasce orarie"
              aria-expanded={timeBandOpen}
              onClick={() => setTimeBandOpen((current) => !current)}
            >
              <span aria-hidden="true">→</span>
              <small aria-hidden="true">⌄</small>
            </button>
            {timeBandOpen ? (
              <div
                className="temporal-create-time-band-panel"
                role="dialog"
                aria-label="Fasce orarie"
              >
                {TIME_BANDS.map((band) => (
                  <button
                    key={band.key}
                    type="button"
                    onClick={() => applyTimeBand(band)}
                  >
                    <strong>{bandLabels[band.key]}</strong>
                    <small>{`${band.start}–${band.end}`}</small>
                  </button>
                ))}
              </div>
            ) : null}
          </div>

          <TimeControl
            label={italian ? 'Fine' : 'End'}
            value={calculatedEnd.time}
            dataPath="endTime"
            onChange={(endTime) => patchEnd(visibleEndDate, endTime)}
            helper={
              <>
                {temporalCreateDurationLabel(fields.durationMinutes)}
                {renderError('durationMinutes')}
              </>
            }
          />

          <TemporalCreateDatePicker
            label={italian ? 'Data fine' : 'End date'}
            value={visibleEndDate}
            min={fields.date}
            locale={locale}
            onChange={(date) => patchEnd(date, calculatedEnd.time)}
          />

          {fields.kind === 'activity' &&
          (!showCompactTimezone ||
            authoringDraft.activityStructure.activityIntervals.length > 0) ? (
            <div
              className="temporal-create-activity-intervals"
              data-create-activity-intervals
            >
              {authoringDraft.activityStructure.activityIntervals.map(
                (interval, index) => (
                  <div
                    className="temporal-create-activity-interval"
                    key={interval.id}
                  >
                    <span className="temporal-create-activity-interval__label">
                      {italian
                        ? `Intervallo ${index + 2}`
                        : `Interval ${index + 2}`}
                    </span>
                    <div className="temporal-create-activity-interval__fields">
                      <TemporalCreateDatePicker
                        label={italian ? 'Data inizio' : 'Start date'}
                        value={interval.date}
                        locale={locale}
                        onChange={(date) =>
                          updateActivityInterval(interval.id, { date })
                        }
                      />
                      <TimeControl
                        label={italian ? 'Inizio' : 'Start'}
                        value={interval.startTime}
                        dataPath={`activityIntervals.${interval.id}.startTime`}
                        onChange={(startTime) =>
                          updateActivityInterval(interval.id, { startTime })
                        }
                      />
                      <span
                        className="temporal-create-activity-interval__arrow"
                        aria-hidden="true"
                      >
                        →
                      </span>
                      <TimeControl
                        label={italian ? 'Fine' : 'End'}
                        value={interval.endTime}
                        dataPath={`activityIntervals.${interval.id}.endTime`}
                        onChange={(endTime) =>
                          updateActivityInterval(interval.id, { endTime })
                        }
                      />
                      <TemporalCreateDatePicker
                        label={italian ? 'Data fine' : 'End date'}
                        value={interval.endDate}
                        locale={locale}
                        onChange={(endDate) =>
                          updateActivityInterval(interval.id, { endDate })
                        }
                      />
                      <button
                        type="button"
                        className="temporal-create-activity-interval__remove"
                        aria-label={
                          italian
                            ? `Rimuovi intervallo ${index + 2}`
                            : `Remove interval ${index + 2}`
                        }
                        onClick={() =>
                          patchActivityIntervals(
                            authoringDraft.activityStructure.activityIntervals.filter(
                              (item) => item.id !== interval.id,
                            ),
                          )
                        }
                      >
                        ×
                      </button>
                    </div>
                  </div>
                ),
              )}
              {authoringDraft.activityStructure.activityIntervals.length <
              99 ? (
                <button
                  type="button"
                  className="temporal-create-activity-intervals__add"
                  onClick={addActivityInterval}
                >
                  <span aria-hidden="true">＋</span>{' '}
                  {italian ? 'Aggiungi intervallo' : 'Add interval'}
                </button>
              ) : null}
            </div>
          ) : null}
        </div>
      ) : null}

      {fields.timeSemantics === 'all-day' ? (
        <div className="temporal-create-u2-all-day">
          <TemporalCreateDatePicker
            label="Data inizio"
            value={fields.date}
            locale={locale}
            onChange={patchAllDayStartDate}
          />
          <TemporalCreateDatePicker
            label="Data fine"
            value={visibleAllDayEndDate}
            min={fields.date}
            locale={locale}
            onChange={patchAllDayEndDate}
          />
        </div>
      ) : null}

      {fields.timeSemantics !== 'unscheduled' ? (
        <>
          <div className="temporal-create-u2-repeat">
            <select
              aria-label={copy.event.repeat}
              value={quickRecurrence(fields)}
              onChange={(event) =>
                changeQuickRecurrence(
                  event.currentTarget.value as QuickRecurrence,
                )
              }
            >
              <option value="none">{copy.event.repeatNever}</option>
              <option value="daily">{copy.event.repeatDaily}</option>
              <option value="weekly">{copy.event.repeatWeekly}</option>
              <option value="monthly">{copy.event.repeatMonthly}</option>
              <option value="yearly">{copy.event.repeatYearly}</option>
              <option value="custom">{copy.event.repeatCustom}</option>
            </select>
          </div>
          {repeatDetails}
        </>
      ) : null}

      <TemporalCreateLifeAreaField
        contexts={contexts}
        draft={authoringDraft}
        onLifeAreaChange={(lifeArea) => patchAuthoring({ lifeArea })}
        onItemColorChange={(itemColorCode) => patchAuthoring({ itemColorCode })}
        onLegacyContextChange={(contextId) => onPatch({ contextId })}
      />
      {renderError('contextId')}

      <input
        className="temporal-create-u2-location"
        type="text"
        value={fields.event.location}
        aria-label="Località"
        placeholder="Località"
        autoComplete="off"
        onChange={(event) =>
          patchEvent({ location: event.currentTarget.value })
        }
      />

      {fields.timeSemantics !== 'unscheduled' ? (
        <TemporalCreateQuickReminder fields={fields} onPatch={onPatch} />
      ) : null}

      <textarea
        className="temporal-create-u2-description"
        value={fields.notes}
        aria-label="Descrizione"
        placeholder="Descrizione"
        rows={3}
        onChange={(event) => onPatch({ notes: event.currentTarget.value })}
      />
    </>
  );
}
