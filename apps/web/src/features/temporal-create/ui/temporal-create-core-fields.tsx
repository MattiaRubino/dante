import { Temporal } from '@dante/time';
import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateEventCalendarFrequency,
  TemporalCreateFields,
  TemporalCreateKind,
  TemporalCreateTimeSemantics,
  TemporalCreateWeekday,
} from '../model/temporal-create-session';
import { useTemporalCreateContextCreator } from './temporal-create-context-catalog';
import { TemporalCreateContextPicker } from './temporal-create-context-picker';
import {
  TEMPORAL_CREATE_DURATION_OPTIONS,
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
  onRequestAdvanced: () => void;
  renderError: (path: string) => ReactNode;
}>;

type QuickRecurrence =
  | 'none'
  | 'daily'
  | 'weekly'
  | 'monthly'
  | 'yearly'
  | 'custom';

const WEEKDAYS: readonly TemporalCreateWeekday[] = Object.freeze([
  'MO',
  'TU',
  'WE',
  'TH',
  'FR',
  'SA',
  'SU',
]);

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

export function TemporalCreateCoreFields({
  fields,
  contexts,
  onPatch,
  onRequestAdvanced,
  renderError,
}: TemporalCreateCoreFieldsProps) {
  const { t, i18n } = useTranslation('common');
  const copy = temporalCreateProductCopy(i18n.resolvedLanguage ?? i18n.language);
  const onCreateContext = useTemporalCreateContextCreator();
  const typeRegistry = temporalCreateTypeRegistry();
  const patchEvent = (patch: Partial<TemporalCreateFields['event']>) =>
    onPatch({ event: { ...fields.event, ...patch } });
  const durationOptions = TEMPORAL_CREATE_DURATION_OPTIONS.includes(
    fields.durationMinutes,
  )
    ? TEMPORAL_CREATE_DURATION_OPTIONS
    : Object.freeze(
        [...TEMPORAL_CREATE_DURATION_OPTIONS, fields.durationMinutes].sort(
          (left, right) => left - right,
        ),
      );

  const durationControl = (
    <label className="temporal-create-control">
      <span>{t(($) => $.common.home.timeline.create.duration)}</span>
      <select
        data-create-path="durationMinutes"
        value={fields.durationMinutes}
        onChange={(event) =>
          onPatch({ durationMinutes: Number(event.currentTarget.value) })
        }
      >
        {durationOptions.map((minutes) => (
          <option key={minutes} value={minutes}>
            {temporalCreateDurationLabel(minutes)}
          </option>
        ))}
      </select>
      {renderError('durationMinutes')}
    </label>
  );

  const changeKind = (kind: TemporalCreateKind) => {
    if (kind === fields.kind) {
      return;
    }
    if (kind === 'event') {
      onPatch({
        kind,
        timeSemantics:
          fields.timeSemantics === 'unscheduled' ? 'timed' : fields.timeSemantics,
        scheduling: {
          ...fields.scheduling,
          constraintKind: 'none',
          fallbackPolicy: 'inherit',
        },
      });
      return;
    }
    onPatch({ kind });
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

  const patchEventEnd = (endDate: string, endTime: string) => {
    const duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      fields.startTime,
      endDate,
      endTime,
      fields.timeMode,
      fields.timeZoneId,
    );
    if (duration !== null) {
      onPatch({ durationMinutes: duration });
    }
  };

  const changeQuickRecurrence = (value: QuickRecurrence) => {
    if (value === 'custom') {
      if (
        fields.kind === 'activity' &&
        fields.eventRecurrence.patternKind === 'none'
      ) {
        onPatch({
          eventRecurrence: {
            ...fields.eventRecurrence,
            patternKind: 'calendar-wall-clock',
            calendarFrequency: 'weekly',
            calendarInterval: 1,
            weekdays: Object.freeze([weekdayForDate(fields.date)]),
          },
        });
      }
      onRequestAdvanced();
      return;
    }
    if (value === 'none') {
      onPatch({
        eventRecurrence: { ...fields.eventRecurrence, patternKind: 'none' },
      });
      return;
    }
    const frequency = value satisfies TemporalCreateEventCalendarFrequency;
    onPatch({
      eventRecurrence: {
        ...fields.eventRecurrence,
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

  return (
    <>
      <fieldset className="temporal-create-type-fieldset">
        <legend>{copy.typeLabel}</legend>
        <div className="temporal-create-type-grid">
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
        </div>
      </fieldset>

      <fieldset
        className="temporal-create-choice-group"
        data-create-path="timeSemantics"
      >
        <legend>
          {fields.kind === 'activity' ? copy.activity.placement : copy.event.when}
        </legend>
        <div className="temporal-create-choice-row">
          <button
            type="button"
            role="radio"
            aria-checked={fields.timeSemantics === 'timed'}
            className={fields.timeSemantics === 'timed' ? 'is-active' : ''}
            onClick={() => changeTimeSemantics('timed')}
          >
            {fields.kind === 'activity' ? copy.activity.timed : copy.event.timed}
          </button>
          <button
            type="button"
            role="radio"
            aria-checked={fields.timeSemantics === 'all-day'}
            className={fields.timeSemantics === 'all-day' ? 'is-active' : ''}
            onClick={() => changeTimeSemantics('all-day')}
          >
            {fields.kind === 'activity' ? copy.activity.allDay : copy.event.allDay}
          </button>
          {fields.kind === 'activity' ? (
            <button
              type="button"
              role="radio"
              aria-checked={fields.timeSemantics === 'unscheduled'}
              className={fields.timeSemantics === 'unscheduled' ? 'is-active' : ''}
              onClick={() => changeTimeSemantics('unscheduled')}
            >
              {copy.activity.toPlace}
            </button>
          ) : null}
        </div>
      </fieldset>
      {renderError('timeSemantics')}

      {fields.kind === 'activity' && fields.timeSemantics === 'timed' ? (
        <div className="temporal-create-temporal-row">
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
          <label className="temporal-create-control">
            <span>{t(($) => $.common.home.timeline.create.start)}</span>
            <input
              data-create-path="startTime"
              type="time"
              step="300"
              value={fields.startTime}
              onChange={(event) => onPatch({ startTime: event.currentTarget.value })}
            />
            {renderError('startTime')}
          </label>
          {durationControl}
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

      {fields.kind === 'activity' && fields.timeSemantics === 'unscheduled' ? (
        <div className="temporal-create-grid one">{durationControl}</div>
      ) : null}

      {fields.kind === 'event' && fields.timeSemantics === 'timed' ? (
        <div className="temporal-create-event-time-grid">
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
          <label className="temporal-create-control">
            <span>{t(($) => $.common.home.timeline.create.start)}</span>
            <input
              data-create-path="startTime"
              type="time"
              step="300"
              value={fields.startTime}
              onChange={(event) => onPatch({ startTime: event.currentTarget.value })}
            />
            {renderError('startTime')}
          </label>
          <label className="temporal-create-control">
            <span>{copy.event.end}</span>
            <input
              type="time"
              step="300"
              value={end.time}
              onChange={(event) => patchEventEnd(end.date, event.currentTarget.value)}
            />
            {end.dayOffset > 0 ? <small>+{end.dayOffset}d</small> : null}
          </label>
        </div>
      ) : null}

      {fields.kind === 'event' && fields.timeSemantics === 'all-day' ? (
        <div className="temporal-create-grid two">
          <label className="temporal-create-control">
            <span>{t(($) => $.common.home.timeline.create.eventDetails.startDate)}</span>
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
            <span>{t(($) => $.common.home.timeline.create.eventDetails.endDate)}</span>
            <input
              data-create-path="event.allDayEndDate"
              type="date"
              value={fields.event.allDayEndDate}
              onChange={(event) => patchEvent({ allDayEndDate: event.currentTarget.value })}
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
              changeQuickRecurrence(event.currentTarget.value as QuickRecurrence)
            }
          >
            <option value="none">{copy.event.repeatNever}</option>
            <option value="daily">{copy.event.repeatDaily}</option>
            <option value="weekly">{copy.event.repeatWeekly}</option>
            <option value="monthly">{copy.event.repeatMonthly}</option>
            <option value="yearly">{copy.event.repeatYearly}</option>
            {quickRecurrence(fields) === 'custom' ? (
              <option value="custom">{copy.event.repeatCustom}</option>
            ) : null}
          </select>
        </label>
        <button
          className="temporal-create-inline-action"
          type="button"
          onClick={() => changeQuickRecurrence('custom')}
        >
          {copy.event.repeatCustom}
        </button>
      </div>

      <div className="temporal-create-context-row">
        <TemporalCreateContextPicker
          value={fields.contextId}
          contexts={contexts}
          onChange={(contextId) => onPatch({ contextId })}
          onCreateContext={onCreateContext}
        />
      </div>

      {fields.kind === 'event' ? (
        <label className="temporal-create-control temporal-create-location-control">
          <span>{t(($) => $.common.home.timeline.create.eventDetails.location)}</span>
          <input
            type="text"
            value={fields.event.location}
            onChange={(event) => patchEvent({ location: event.currentTarget.value })}
            placeholder={t(
              ($) => $.common.home.timeline.create.eventDetails.locationPlaceholder,
            )}
          />
        </label>
      ) : null}
    </>
  );
}
