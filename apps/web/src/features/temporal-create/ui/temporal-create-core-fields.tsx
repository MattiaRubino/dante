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
import { useTemporalCreateContextCreator } from './temporal-create-context-catalog';
import { TemporalCreateContextPicker } from './temporal-create-context-picker';
import {
  temporalCreateDurationFromEndDateTime,
  temporalCreateDurationLabel,
  temporalCreateEndDateTime,
} from './temporal-create-field-shared';
import { temporalCreateProductCopy } from './temporal-create-product-copy';
import { temporalCreateTypeRegistry } from './temporal-create-type-registry';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

type TemporalCreateCoreFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  contexts: readonly TemporalCreateContextOption[];
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  onRequestAdvanced: (target?: 'recurrence') => void;
  renderError: (path: string) => ReactNode;
}>;

type QuickRecurrence =
  'none' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'custom';

type TimeControlProps = Readonly<{
  label: string;
  value: string;
  dataPath: string;
  onChange: (value: string) => void;
  helper?: ReactNode;
}>;

type TimeBand = Readonly<{
  key: 'morning' | 'afternoon' | 'evening' | 'night';
  start: string;
  end: string;
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
    // Fall back to a stable representative list on older runtimes.
  }
  return FALLBACK_TIME_ZONES;
}

const TIME_ZONES = supportedTimeZones();

function weekdayForDate(date: string): TemporalCreateWeekday {
  try {
    const dayOfWeek = Temporal.PlainDate.from(date).dayOfWeek;
    return WEEKDAYS[dayOfWeek - 1] ?? 'MO';
  } catch {
    return 'MO';
  }
}

function quickRecurrence(fields: TemporalCreateFields): QuickRecurrence {
  const recurrence = fields.eventRecurrence;
  if (recurrence.patternKind === 'none') {
    return 'none';
  }
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

function timeToMinute(value: string): number | null {
  const match = /^(\d{1,2}):(\d{2})$/.exec(value.trim());
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
  const minute = timeToMinute(value) ?? 0;
  return minuteToTime(Math.round(minute / 15) * 15);
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

function TemporalCreateTimeControl({
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
  const lastValidRef = useRef(normalizedValue);

  useEffect(() => {
    const parsed = timeToMinute(value);
    if (parsed === null) {
      return;
    }
    const next = minuteToTime(parsed);
    lastValidRef.current = next;
    setHourDraft(next.slice(0, 2));
    setMinuteDraft(next.slice(3, 5));
  }, [value]);

  useEffect(() => {
    if (!pickerOpen) {
      return;
    }
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
    if (!pickerOpen) {
      return;
    }
    const frame = requestAnimationFrame(() => {
      const selected = nearestQuarter(lastValidRef.current);
      const option = Array.from(
        listRef.current?.querySelectorAll<HTMLElement>('[data-time-value]') ??
          [],
      ).find((candidate) => candidate.dataset.timeValue === selected);
      option?.scrollIntoView({ block: 'center' });
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
      return;
    }
    const hour = Number(hourValue);
    const minute = Number(minuteValue);
    if (hour > 23 || minute > 59) {
      restore();
      return;
    }
    syncDraft(
      `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`,
    );
  };

  const adjust = (delta: number) => {
    syncDraft(shiftTime(lastValidRef.current, delta));
  };

  const handleSegmentKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
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
          const next = event.currentTarget.value;
          const parsed = timeToMinute(next);
          if (parsed !== null) {
            syncDraft(minuteToTime(parsed));
          }
        }}
      />

      <div className="temporal-create-time-control__field">
        <div className="temporal-create-inline-time-editor">
          <div className="temporal-create-time-segment">
            <button
              type="button"
              aria-label={`${label}: aumenta ora`}
              onClick={() => adjust(60)}
            >
              ▲
            </button>
            <input
              type="text"
              inputMode="numeric"
              maxLength={2}
              aria-label={`${label}: ore`}
              value={hourDraft}
              onChange={(event) => {
                const next = event.currentTarget.value;
                if (/^\d{0,2}$/.test(next)) {
                  setHourDraft(next);
                  if (next.length === 2 && Number(next) <= 23) {
                    commitParts(next, minuteDraft);
                  }
                }
              }}
              onBlur={() => commitParts(hourDraft, minuteDraft)}
              onKeyDown={handleSegmentKeyDown}
              autoComplete="off"
              spellCheck="false"
            />
            <button
              type="button"
              aria-label={`${label}: diminuisci ora`}
              onClick={() => adjust(-60)}
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
              onClick={() => adjust(15)}
            >
              ▲
            </button>
            <input
              type="text"
              inputMode="numeric"
              maxLength={2}
              aria-label={`${label}: minuti`}
              value={minuteDraft}
              onChange={(event) => {
                const next = event.currentTarget.value;
                if (/^\d{0,2}$/.test(next)) {
                  setMinuteDraft(next);
                  if (next.length === 2 && Number(next) <= 59) {
                    commitParts(hourDraft, next);
                  }
                }
              }}
              onBlur={() => commitParts(hourDraft, minuteDraft)}
              onKeyDown={handleSegmentKeyDown}
              autoComplete="off"
              spellCheck="false"
            />
            <button
              type="button"
              aria-label={`${label}: diminuisci 15 minuti`}
              onClick={() => adjust(-15)}
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

export function TemporalCreateCoreFields({
  fields,
  contexts,
  onPatch,
  onRequestAdvanced,
  renderError,
}: TemporalCreateCoreFieldsProps) {
  const { t, i18n } = useTranslation('common');
  const copy = temporalCreateProductCopy(
    i18n.resolvedLanguage ?? i18n.language,
  );
  const onCreateContext = useTemporalCreateContextCreator();
  const typeRegistry = temporalCreateTypeRegistry();
  const [timeZoneOpen, setTimeZoneOpen] = useState(false);
  const [timeBandOpen, setTimeBandOpen] = useState(false);
  const timeZoneRootRef = useRef<HTMLDivElement | null>(null);
  const timeBandRootRef = useRef<HTMLDivElement | null>(null);
  const italian = i18n.language.toLowerCase().startsWith('it');
  const recurrenceOwner: Exclude<TemporalCreateRecurrenceOwner, null> =
    fields.kind === 'event' ? 'event' : 'routine';
  const patchEvent = (patch: Partial<TemporalCreateFields['event']>) =>
    onPatch({ event: { ...fields.event, ...patch } });

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

  useEffect(() => {
    if (!timeZoneOpen) {
      return;
    }
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
    if (!timeBandOpen) {
      return;
    }
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
    if (kind === fields.kind) {
      return;
    }
    const targetOwner = kind === 'event' ? 'event' : 'routine';
    const eventRecurrence = {
      ...fields.eventRecurrence,
      owner: fields.eventRecurrence.patternKind === 'none' ? null : targetOwner,
    } as const;
    if (kind === 'event') {
      onPatch({
        kind,
        timeSemantics:
          fields.timeSemantics === 'unscheduled' ||
          fields.timeSemantics === 'coarse'
            ? 'timed'
            : fields.timeSemantics,
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
    });
  };

  const end = temporalCreateEndDateTime(
    fields.date,
    fields.startTime,
    fields.durationMinutes,
    fields.timeMode,
    fields.timeZoneId,
  );

  const patchEnd = (endDate: string, endTime: string) => {
    let duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      fields.startTime,
      endDate,
      endTime,
      fields.timeMode,
      fields.timeZoneId,
    );
    if (duration === null && endDate === fields.date) {
      try {
        const nextDate = Temporal.PlainDate.from(fields.date)
          .add({ days: 1 })
          .toString();
        duration = temporalCreateDurationFromEndDateTime(
          fields.date,
          fields.startTime,
          nextDate,
          endTime,
          fields.timeMode,
          fields.timeZoneId,
        );
      } catch {
        duration = null;
      }
    }
    if (duration !== null) {
      onPatch({ durationMinutes: duration });
    }
  };

  const patchStartTime = (startTime: string) => {
    let duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      startTime,
      end.date,
      end.time,
      fields.timeMode,
      fields.timeZoneId,
    );
    if (duration === null && end.date === fields.date) {
      const nextDate = Temporal.PlainDate.from(fields.date)
        .add({ days: 1 })
        .toString();
      duration = temporalCreateDurationFromEndDateTime(
        fields.date,
        startTime,
        nextDate,
        end.time,
        fields.timeMode,
        fields.timeZoneId,
      );
    }
    onPatch({
      startTime,
      ...(duration === null ? {} : { durationMinutes: duration }),
    });
  };

  const applyTimeBand = (band: TimeBand) => {
    let endDate = fields.date;
    const startMinute = timeToMinute(band.start);
    const endMinute = timeToMinute(band.end);
    if (
      startMinute !== null &&
      endMinute !== null &&
      endMinute <= startMinute
    ) {
      try {
        endDate = Temporal.PlainDate.from(fields.date)
          .add({ days: 1 })
          .toString();
      } catch {
        endDate = fields.date;
      }
    }

    const duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      band.start,
      endDate,
      band.end,
      fields.timeMode,
      fields.timeZoneId,
    );

    if (duration !== null) {
      onPatch({ startTime: band.start, durationMinutes: duration });
    }
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
            : {
                ...fields.eventRecurrence,
                owner: recurrenceOwner,
              },
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

  const startLabel = italian ? 'Inizio' : 'Start';

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
              className={fields.kind === descriptor.kind ? 'is-active' : ''}
              onClick={() => changeKind(descriptor.kind)}
            >
              <strong>
                {descriptor.kind === 'activity'
                  ? t(($) => $.common.home.timeline.create.kind.activity)
                  : t(($) => $.common.home.timeline.create.kind.event)}
              </strong>
            </button>
          ))}
          <button
            type="button"
            className="is-deferred"
            disabled
            aria-disabled="true"
          >
            <strong>Timer</strong>
            <small>{italian ? 'Prossimamente' : 'Coming soon'}</small>
          </button>
          <button
            type="button"
            className="is-deferred"
            disabled
            aria-disabled="true"
          >
            <strong>{italian ? 'Sveglia' : 'Alarm'}</strong>
            <small>{italian ? 'Prossimamente' : 'Coming soon'}</small>
          </button>
        </div>
      </fieldset>

      <fieldset
        className="temporal-create-choice-group"
        data-create-path="timeSemantics"
      >
        <legend className="temporal-create-visually-hidden">
          {fields.kind === 'activity'
            ? copy.activity.placement
            : copy.event.when}
        </legend>
        <div className="temporal-create-choice-row">
          <button
            type="button"
            role="radio"
            aria-checked={fields.timeSemantics === 'timed'}
            className={fields.timeSemantics === 'timed' ? 'is-active' : ''}
            onClick={() => changeTimeSemantics('timed')}
          >
            {fields.kind === 'activity'
              ? copy.activity.timed
              : copy.event.timed}
          </button>
          <button
            type="button"
            role="radio"
            aria-checked={fields.timeSemantics === 'all-day'}
            className={fields.timeSemantics === 'all-day' ? 'is-active' : ''}
            onClick={() => changeTimeSemantics('all-day')}
          >
            {fields.kind === 'activity'
              ? copy.activity.allDay
              : copy.event.allDay}
          </button>
          {fields.kind === 'activity' ? (
            <button
              type="button"
              role="radio"
              aria-checked={fields.timeSemantics === 'unscheduled'}
              className={
                fields.timeSemantics === 'unscheduled' ? 'is-active' : ''
              }
              onClick={() => changeTimeSemantics('unscheduled')}
            >
              {copy.activity.toPlace}
            </button>
          ) : null}
        </div>
      </fieldset>
      {renderError('timeSemantics')}

      {fields.timeSemantics === 'timed' ? (
        <div className="temporal-create-when-block">
          <div className="temporal-create-date-time-row">
            <div
              ref={timeZoneRootRef}
              className="temporal-create-timezone-control"
            >
              <button
                className={`temporal-create-timezone-trigger${timeZoneOpen ? ' is-open' : ''}`}
                type="button"
                aria-label={`${italian ? 'Fuso orario' : 'Time zone'}: ${timeZoneLabel}`}
                aria-expanded={timeZoneOpen}
                title={timeZoneLabel}
                onClick={() => setTimeZoneOpen((current) => !current)}
              >
                <GlobeIcon />
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
                      onClick={() => onPatch({ timeMode: 'floating' })}
                    >
                      {italian ? 'Ora locale' : 'Local time'}
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
                        onClick={() =>
                          onPatch({ timeMode: 'zoned', timeZoneId: zoneId })
                        }
                      >
                        {zoneId.replaceAll('_', ' ')}
                      </button>
                    ))}
                  </div>
                  {renderError('timeZoneId')}
                </div>
              ) : null}
            </div>

            <label className="temporal-create-control temporal-create-date-control">
              <span className="temporal-create-visually-hidden">
                {t(($) => $.common.home.timeline.create.date)}
              </span>
              <input
                data-create-path="date"
                type="date"
                value={fields.date}
                onChange={(event) =>
                  onPatch({ date: event.currentTarget.value })
                }
                aria-label={t(($) => $.common.home.timeline.create.date)}
              />
              {renderError('date')}
            </label>

            <TemporalCreateTimeControl
              label={startLabel}
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
                aria-label={italian ? 'Fasce orarie' : 'Time bands'}
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
                  aria-label={italian ? 'Fasce orarie' : 'Time bands'}
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

            <TemporalCreateTimeControl
              label={copy.event.end}
              value={end.time}
              dataPath="endTime"
              onChange={(endTime) => patchEnd(end.date, endTime)}
              helper={
                <>
                  {end.dayOffset > 0 ? `+${end.dayOffset}d · ` : ''}
                  {temporalCreateDurationLabel(fields.durationMinutes)}
                  {renderError('durationMinutes')}
                </>
              }
            />
          </div>
        </div>
      ) : null}

      {fields.kind === 'activity' && fields.timeSemantics === 'all-day' ? (
        <div className="temporal-create-grid one">
          <label className="temporal-create-control">
            <span className="temporal-create-visually-hidden">
              {t(($) => $.common.home.timeline.create.date)}
            </span>
            <input
              data-create-path="date"
              type="date"
              value={fields.date}
              onChange={(event) => onPatch({ date: event.currentTarget.value })}
              aria-label={t(($) => $.common.home.timeline.create.date)}
            />
            {renderError('date')}
          </label>
        </div>
      ) : null}

      {fields.kind === 'event' && fields.timeSemantics === 'all-day' ? (
        <div className="temporal-create-grid two">
          <label className="temporal-create-control">
            <span className="temporal-create-visually-hidden">
              {t(($) => $.common.home.timeline.create.eventDetails.startDate)}
            </span>
            <input
              data-create-path="date"
              type="date"
              value={fields.date}
              aria-label={t(
                ($) => $.common.home.timeline.create.eventDetails.startDate,
              )}
              onChange={(event) => {
                const date = event.currentTarget.value;
                onPatch({
                  date,
                  event: {
                    ...fields.event,
                    allDayEndDate: safeAllDayEndDate(
                      date,
                      fields.event.allDayEndDate,
                    ),
                  },
                });
              }}
            />
            {renderError('date')}
          </label>
          <label className="temporal-create-control">
            <span className="temporal-create-visually-hidden">
              {t(($) => $.common.home.timeline.create.eventDetails.endDate)}
            </span>
            <input
              data-create-path="event.allDayEndDate"
              type="date"
              value={fields.event.allDayEndDate}
              aria-label={t(
                ($) => $.common.home.timeline.create.eventDetails.endDate,
              )}
              onChange={(event) =>
                patchEvent({ allDayEndDate: event.currentTarget.value })
              }
            />
            {renderError('event.allDayEndDate')}
          </label>
        </div>
      ) : null}

      <div className="temporal-create-event-quick-row">
        <label className="temporal-create-control">
          <span className="temporal-create-visually-hidden">
            {copy.event.repeat}
          </span>
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
        </label>
      </div>

      <div className="temporal-create-context-row">
        <TemporalCreateContextPicker
          value={fields.contextId}
          contexts={contexts}
          onChange={(contextId) => onPatch({ contextId })}
          onCreateContext={onCreateContext}
        />
        {renderError('contextId')}
      </div>

      {fields.kind === 'event' ? (
        <label className="temporal-create-control temporal-create-location-control">
          <span>
            {t(($) => $.common.home.timeline.create.eventDetails.location)}
          </span>
          <input
            type="text"
            value={fields.event.location}
            onChange={(event) =>
              patchEvent({ location: event.currentTarget.value })
            }
            placeholder={t(
              ($) =>
                $.common.home.timeline.create.eventDetails.locationPlaceholder,
            )}
          />
        </label>
      ) : null}
    </>
  );
}
