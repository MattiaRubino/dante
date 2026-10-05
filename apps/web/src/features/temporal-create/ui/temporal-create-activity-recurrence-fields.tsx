import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import {
  temporalCreateWeekdays,
  type TemporalCreateFields,
  type TemporalCreateWeekday,
} from '../model/temporal-create-session';
import { TemporalCreateDatePicker } from './temporal-create-date-picker';

import './temporal-create-activity-recurrence-fields.css';

type TemporalCreateActivityRecurrenceFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

type CalendarFrequency = Exclude<
  TemporalCreateFields['eventRecurrence']['calendarFrequency'],
  'monthly-ordinal'
>;

type EndMode = TemporalCreateFields['eventRecurrence']['endMode'];

const ORDINALS = Object.freeze([1, 2, 3, 4, 5, -1]);

export function TemporalCreateActivityRecurrenceFields({
  fields,
  onPatch,
  renderError,
}: TemporalCreateActivityRecurrenceFieldsProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const locale = i18n.resolvedLanguage ?? i18n.language;
  const recurrence = fields.eventRecurrence;

  if (recurrence.patternKind !== 'calendar-wall-clock') return null;

  const patchRecurrence = (
    changes: Partial<TemporalCreateFields['eventRecurrence']>,
  ) => {
    onPatch({
      eventRecurrence: {
        ...recurrence,
        ...changes,
        owner: 'routine',
        patternKind: 'calendar-wall-clock',
      },
    });
  };

  const weekdayShortLabel = (weekday: TemporalCreateWeekday): string => {
    const labels: Record<TemporalCreateWeekday, string> = italian
      ? { MO: 'L', TU: 'M', WE: 'M', TH: 'G', FR: 'V', SA: 'S', SU: 'D' }
      : { MO: 'M', TU: 'T', WE: 'W', TH: 'T', FR: 'F', SA: 'S', SU: 'S' };
    return labels[weekday];
  };

  const weekdayLongLabel = (weekday: TemporalCreateWeekday): string => {
    const labels: Record<TemporalCreateWeekday, string> = italian
      ? {
          MO: 'Lunedì',
          TU: 'Martedì',
          WE: 'Mercoledì',
          TH: 'Giovedì',
          FR: 'Venerdì',
          SA: 'Sabato',
          SU: 'Domenica',
        }
      : {
          MO: 'Monday',
          TU: 'Tuesday',
          WE: 'Wednesday',
          TH: 'Thursday',
          FR: 'Friday',
          SA: 'Saturday',
          SU: 'Sunday',
        };
    return labels[weekday];
  };

  const toggleWeekday = (weekday: TemporalCreateWeekday) => {
    const selected = recurrence.weekdays.includes(weekday);
    if (selected && recurrence.weekdays.length <= 1) return;
    const canonical = temporalCreateWeekdays();
    const next = selected
      ? recurrence.weekdays.filter((candidate) => candidate !== weekday)
      : [...recurrence.weekdays, weekday].sort(
          (left, right) => canonical.indexOf(left) - canonical.indexOf(right),
        );
    patchRecurrence({ weekdays: Object.freeze(next) });
  };

  const frequency: CalendarFrequency =
    recurrence.calendarFrequency === 'monthly-ordinal'
      ? 'monthly'
      : recurrence.calendarFrequency;

  const setEndMode = (endMode: EndMode) => {
    patchRecurrence({
      endMode,
      ...(endMode === 'until-date' && !recurrence.untilDate
        ? { untilDate: fields.date }
        : {}),
    });
  };

  const ordinalLabel = (ordinal: number): string => {
    if (!italian) {
      if (ordinal === -1) return 'Last';
      if (ordinal === 1) return 'First';
      if (ordinal === 2) return 'Second';
      if (ordinal === 3) return 'Third';
      if (ordinal === 4) return 'Fourth';
      return 'Fifth';
    }
    if (ordinal === -1) return 'Ultimo';
    if (ordinal === 1) return 'Primo';
    if (ordinal === 2) return 'Secondo';
    if (ordinal === 3) return 'Terzo';
    if (ordinal === 4) return 'Quarto';
    return 'Quinto';
  };

  const unitLabel = (() => {
    const plural = recurrence.calendarInterval !== 1;
    if (italian) {
      if (frequency === 'daily') return plural ? 'giorni' : 'giorno';
      if (frequency === 'weekly') return plural ? 'settimane' : 'settimana';
      if (frequency === 'monthly') return plural ? 'mesi' : 'mese';
      return plural ? 'anni' : 'anno';
    }
    if (frequency === 'daily') return plural ? 'days' : 'day';
    if (frequency === 'weekly') return plural ? 'weeks' : 'week';
    if (frequency === 'monthly') return plural ? 'months' : 'month';
    return plural ? 'years' : 'year';
  })();

  const anchorDate = new Date(`${fields.date}T00:00:00Z`);
  const anchorDay = new Intl.DateTimeFormat(locale, {
    day: 'numeric',
    timeZone: 'UTC',
  }).format(anchorDate);
  const anchorDayMonth = new Intl.DateTimeFormat(locale, {
    day: 'numeric',
    month: 'long',
    timeZone: 'UTC',
  }).format(anchorDate);

  const endChoice = (mode: EndMode, label: string) => (
    <button
      type="button"
      role="radio"
      aria-checked={recurrence.endMode === mode}
      className={`temporal-create-activity-repeat__end-choice${
        recurrence.endMode === mode ? ' is-active' : ''
      }`}
      onClick={() => setEndMode(mode)}
    >
      <span className="temporal-create-activity-repeat__radio-dot" aria-hidden="true" />
      <span>{label}</span>
    </button>
  );

  return (
    <section
      className="temporal-create-section is-wide temporal-create-activity-repeat"
      aria-labelledby="temporal-create-activity-repeat-heading"
      data-create-recurrence-owner="routine"
    >
      <div className="temporal-create-section__heading temporal-create-activity-repeat__heading">
        <h3 id="temporal-create-activity-repeat-heading">
          {italian ? 'Ripetizione' : 'Repeat'}
        </h3>
      </div>

      <div className="temporal-create-activity-repeat__row">
        <span className="temporal-create-activity-repeat__row-label">
          {italian ? 'Ripeti ogni' : 'Repeat every'}
        </span>
        <input
          className="temporal-create-activity-repeat__interval"
          data-create-path="eventRecurrence.calendarInterval"
          type="number"
          min="1"
          max="365"
          aria-label={italian ? 'Intervallo di ripetizione' : 'Repeat interval'}
          value={recurrence.calendarInterval}
          onChange={(event) =>
            patchRecurrence({
              calendarInterval: Math.max(1, Number(event.currentTarget.value) || 1),
            })
          }
        />
        <span className="temporal-create-activity-repeat__unit-label">{unitLabel}</span>
        {renderError('eventRecurrence.calendarInterval')}
      </div>

      {frequency === 'weekly' ? (
        <div className="temporal-create-activity-repeat__detail-row">
          <span className="temporal-create-activity-repeat__row-label">
            {italian ? 'Giorni' : 'Days'}
          </span>
          <div
            className="temporal-create-activity-repeat__weekdays"
            data-create-path="eventRecurrence.weekdays"
            role="group"
            aria-label={italian ? 'Giorni della settimana' : 'Weekdays'}
          >
            {temporalCreateWeekdays().map((weekday) => {
              const active = recurrence.weekdays.includes(weekday);
              return (
                <button
                  key={weekday}
                  type="button"
                  className={active ? 'is-active' : ''}
                  aria-label={weekdayLongLabel(weekday)}
                  aria-pressed={active}
                  onClick={() => toggleWeekday(weekday)}
                >
                  {weekdayShortLabel(weekday)}
                </button>
              );
            })}
          </div>
          {renderError('eventRecurrence.weekdays')}
        </div>
      ) : null}

      {frequency === 'monthly' ? (
        <div className="temporal-create-activity-repeat__monthly">
          <span className="temporal-create-activity-repeat__row-label">
            {italian ? 'Nel mese' : 'In the month'}
          </span>
          <div className="temporal-create-activity-repeat__segmented">
            <button
              type="button"
              className={recurrence.calendarFrequency === 'monthly' ? 'is-active' : ''}
              aria-pressed={recurrence.calendarFrequency === 'monthly'}
              onClick={() => patchRecurrence({ calendarFrequency: 'monthly' })}
            >
              {italian ? `Il giorno ${anchorDay}` : `On day ${anchorDay}`}
            </button>
            <button
              type="button"
              className={
                recurrence.calendarFrequency === 'monthly-ordinal' ? 'is-active' : ''
              }
              aria-pressed={recurrence.calendarFrequency === 'monthly-ordinal'}
              onClick={() => patchRecurrence({ calendarFrequency: 'monthly-ordinal' })}
            >
              {italian ? 'Per posizione' : 'By position'}
            </button>
          </div>

          {recurrence.calendarFrequency === 'monthly-ordinal' ? (
            <div className="temporal-create-activity-repeat__ordinal">
              <select
                aria-label={italian ? 'Posizione nel mese' : 'Position in month'}
                value={recurrence.calendarOrdinal}
                onChange={(event) =>
                  patchRecurrence({ calendarOrdinal: Number(event.currentTarget.value) })
                }
              >
                {ORDINALS.map((ordinal) => (
                  <option key={ordinal} value={ordinal}>{ordinalLabel(ordinal)}</option>
                ))}
              </select>
              <select
                aria-label={italian ? 'Giorno della settimana' : 'Weekday'}
                value={recurrence.calendarOrdinalWeekday}
                onChange={(event) =>
                  patchRecurrence({
                    calendarOrdinalWeekday: event.currentTarget.value as TemporalCreateWeekday,
                  })
                }
              >
                {temporalCreateWeekdays().map((weekday) => (
                  <option key={weekday} value={weekday}>{weekdayLongLabel(weekday)}</option>
                ))}
              </select>
              {renderError('eventRecurrence.calendarOrdinal')}
            </div>
          ) : null}
        </div>
      ) : null}

      {frequency === 'yearly' ? (
        <p className="temporal-create-activity-repeat__anchor-note">
          {italian ? `Si ripete il ${anchorDayMonth}.` : `Repeats on ${anchorDayMonth}.`}
        </p>
      ) : null}

      <div className="temporal-create-activity-repeat__end-row">
        <span className="temporal-create-activity-repeat__row-label">
          {italian ? 'Termina' : 'Ends'}
        </span>
        <div
          className="temporal-create-activity-repeat__end-choices"
          role="radiogroup"
          aria-label={italian ? 'Fine ripetizione' : 'Repeat ending'}
        >
          <div className="temporal-create-activity-repeat__end-option">
            {endChoice('none', italian ? 'Mai' : 'Never')}
          </div>

          <div
            className={`temporal-create-activity-repeat__end-option${
              recurrence.endMode === 'until-date' ? ' is-active' : ''
            }`}
            onPointerDown={() => setEndMode('until-date')}
          >
            {endChoice('until-date', italian ? 'Data' : 'Date')}
            <div className="temporal-create-activity-repeat__end-date">
              <TemporalCreateDatePicker
                label={italian ? 'Data di fine ripetizione' : 'Repeat end date'}
                value={recurrence.untilDate || fields.date}
                min={fields.date}
                locale={locale}
                onChange={(untilDate) => patchRecurrence({ untilDate, endMode: 'until-date' })}
              />
              {renderError('eventRecurrence.untilDate')}
            </div>
          </div>

          <div
            className={`temporal-create-activity-repeat__end-option${
              recurrence.endMode === 'count' ? ' is-active' : ''
            }`}
          >
            {endChoice('count', italian ? 'Dopo' : 'After')}
            <label className="temporal-create-activity-repeat__count">
              <input
                data-create-path="eventRecurrence.count"
                type="number"
                min="1"
                max="999"
                aria-label={italian ? 'Numero di occorrenze' : 'Number of occurrences'}
                value={recurrence.count}
                onFocus={() => setEndMode('count')}
                onChange={(event) =>
                  patchRecurrence({
                    endMode: 'count',
                    count: Math.max(1, Number(event.currentTarget.value) || 1),
                  })
                }
              />
              <span>{italian ? 'occorrenze' : 'occurrences'}</span>
              {renderError('eventRecurrence.count')}
            </label>
          </div>
        </div>
      </div>
    </section>
  );
}
