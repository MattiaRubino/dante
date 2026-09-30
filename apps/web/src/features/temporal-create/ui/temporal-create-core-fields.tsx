import { Temporal } from '@dante/time';
import {
  useEffect,
  useRef,
  useState,
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
  | 'none'
  | 'daily'
  | 'weekly'
  | 'monthly'
  | 'yearly'
  | 'custom';

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

const TIME_PRESETS = Object.freeze([
  Object.freeze({ key: 'morning', value: '08:00' }),
  Object.freeze({ key: 'afternoon', value: '14:00' }),
  Object.freeze({ key: 'evening', value: '19:00' }),
  Object.freeze({ key: 'night', value: '23:00' }),
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
  const { i18n } = useTranslation('common');
  const [pickerOpen, setPickerOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const listRef = useRef<HTMLDivElement | null>(null);
  const italian = i18n.language.toLowerCase().startsWith('it');
  const presetLabels: Readonly<Record<string, string>> = italian
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
      const selected = nearestQuarter(value);
      const option = Array.from(
        listRef.current?.querySelectorAll<HTMLElement>('[data-time-value]') ?? [],
      ).find((candidate) => candidate.dataset.timeValue === selected);
      option?.scrollIntoView({ block: 'center' });
    });
    return () => cancelAnimationFrame(frame);
  }, [pickerOpen, value]);

  const adjust = (delta: number) => onChange(shiftTime(value, delta));

  return (
    <div ref={rootRef} className="temporal-create-time-control">
      <span className="temporal-create-time-control__label">{label}</span>
      <div className="temporal-create-time-control__field">
        <input
          data-create-path={dataPath}
          type="text"
          inputMode="numeric"
          value={value}
          onChange={(event) => onChange(event.currentTarget.value)}
          onBlur={(event) => {
            const parsed = timeToMinute(event.currentTarget.value);
            if (parsed !== null) {
              onChange(minuteToTime(parsed));
            }
          }}
          aria-label={label}
          autoComplete="off"
          spellCheck="false"
        />
        <div className="temporal-create-time-stepper" aria-label={`${label} stepper`}>
          <div>
            <button
              type="button"
              aria-label={`${label}: aumenta ora`}
              onClick={() => adjust(60)}
            >
              ▲
            </button>
            <button
              type="button"
              aria-label={`${label}: diminuisci ora`}
              onClick={() => adjust(-60)}
            >
              ▼
            </button>
          </div>
          <div>
            <button
              type="button"
              aria-label={`${label}: aumenta 15 minuti`}
              onClick={() => adjust(15)}
            >
              ▲
            </button>
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
        <div className="temporal-create-time-picker" role="dialog" aria-label={label}>
          <div className="temporal-create-time-presets">
            {TIME_PRESETS.map((preset) => (
              <button
                key={preset.key}
                type="button"
                onClick={() => {
                  onChange(preset.value);
                  setPickerOpen(false);
                }}
              >
                <span>{presetLabels[preset.key]}</span>
                <small>{preset.value}</small>
              </button>
            ))}
          </div>
          <div ref={listRef} className="temporal-create-time-list">
            {TIME_OPTIONS.map((option) => (
              <button
                key={option}
                type="button"
                data-time-value={option}
                className={nearestQuarter(value) === option ? 'is-selected' : ''}
                onClick={() => {
                  onChange(option);
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
  const timeZoneRootRef = useRef<HTMLDivElement | null>(null);
  const italian = i18n.language.toLowerCase().startsWith('it');
  const recurrenceOwner: Exclude<TemporalCreateRecurrenceOwner, null> =
    fields.kind === 'event' ? 'event' : 'routine';
  const patchEvent = (patch: Partial<TemporalCreateFields['event']>) =>
    onPatch({ event: { ...fields.event, ...patch } });

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

  return (
    <>
      <fieldset className="temporal-create-type-fieldset">
        <legend className="temporal-create-visually-hidden">{copy.typeLabel}</legend>
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
          <button type="button" className="is-deferred" disabled aria-disabled="true">
            <strong>Timer</strong>
            <small>{italian ? 'Prossimamente' : 'Coming soon'}</small>
          </button>
          <button type="button" className="is-deferred" disabled aria-disabled="true">
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
          <div className="temporal-create-date-timezone-row">
            <label className="temporal-create-control temporal-create-date-control">
              <span>{t(($) => $.common.home.timeline.create.date)}</span>
              <input
                data-create-path="date"
                type="date"
                value={fields.date}
                onChange={(event) =>
                  onPatch({ date: event.currentTarget.value })
                }
              />
              {renderError('date')}
            </label>
            <div ref={timeZoneRootRef} className="temporal-create-timezone-control">
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
                      className={fields.timeMode === 'floating' ? 'is-selected' : ''}
                      onClick={() => onPatch({ timeMode: 'floating' })}
                    >
                      {italian ? 'Ora locale' : 'Local time'}
                    </button>
                    {TIME_ZONES.map((zoneId) => (
                      <button
                        key={zoneId}
                        type="button"
                        className={
                          fields.timeMode === 'zoned' && fields.timeZoneId === zoneId
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
          </div>

          <div className="temporal-create-time-range">
            <TemporalCreateTimeControl
              label={t(($) => $.common.home.timeline.create.start)}
              value={fields.startTime}
              dataPath="startTime"
              onChange={(startTime) => onPatch({ startTime })}
              helper={renderError('startTime')}
            />
            <span className="temporal-create-time-range__arrow" aria-hidden="true">
              →
            </span>
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
            <span>{t(($) => $.common.home.timeline.create.date)}</span>
            <input
              data-create-path="date"
              type="date"
              value={fields.date}
              onChange={(event) => onPatch({ date: event.currentTarget.value })}
            />
            {renderError('date')}
          </label>
        </div>
      ) : null}

      {fields.kind === 'event' && fields.timeSemantics === 'all-day' ? (
        <div className="temporal-create-grid two">
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.eventDetails.startDate)}
            </span>
            <input
              data-create-path="date"
              type="date"
              value={fields.date}
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
            <span>
              {t(($) => $.common.home.timeline.create.eventDetails.endDate)}
            </span>
            <input
              data-create-path="event.allDayEndDate"
              type="date"
              value={fields.event.allDayEndDate}
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
          <span>{copy.event.repeat}</span>
          <select
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
