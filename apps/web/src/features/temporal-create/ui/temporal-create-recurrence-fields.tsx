import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import {
  temporalCreateWeekdays,
  type TemporalCreateFields,
  type TemporalCreateSurface,
  type TemporalCreateWeekday,
} from '../model/temporal-create-session';
import {
  TEMPORAL_CREATE_REMINDER_OPTIONS,
  temporalCreateDurationLabel,
} from './temporal-create-field-shared';

type RecurrenceFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export function TemporalCreateRecurrenceFields({
  fields,
  depth,
  onPatch,
  renderError,
}: RecurrenceFieldsProps) {
  const { t } = useTranslation('common');
  const recurrence = fields.eventRecurrence;
  const confirmation = fields.confirmation;
  const patchRecurrence = (
    patch: Partial<TemporalCreateFields['eventRecurrence']>,
  ) => onPatch({ eventRecurrence: { ...recurrence, ...patch } });
  const patchConfirmation = (
    patch: Partial<TemporalCreateFields['confirmation']>,
  ) => onPatch({ confirmation: { ...confirmation, ...patch } });

  const weekdayLabel = (weekday: TemporalCreateWeekday): string => {
    switch (weekday) {
      case 'MO':
        return t(($) => $.common.home.timeline.create.recurrence.day.MO);
      case 'TU':
        return t(($) => $.common.home.timeline.create.recurrence.day.TU);
      case 'WE':
        return t(($) => $.common.home.timeline.create.recurrence.day.WE);
      case 'TH':
        return t(($) => $.common.home.timeline.create.recurrence.day.TH);
      case 'FR':
        return t(($) => $.common.home.timeline.create.recurrence.day.FR);
      case 'SA':
        return t(($) => $.common.home.timeline.create.recurrence.day.SA);
      case 'SU':
        return t(($) => $.common.home.timeline.create.recurrence.day.SU);
    }
  };

  const toggleWeekday = (weekday: TemporalCreateWeekday) => {
    const selected = recurrence.weekdays.includes(weekday);
    const canonical = temporalCreateWeekdays();
    const next = selected
      ? recurrence.weekdays.filter((value) => value !== weekday)
      : [...recurrence.weekdays, weekday].sort(
          (left, right) =>
            canonical.indexOf(left) - canonical.indexOf(right),
        );
    patchRecurrence({ weekdays: Object.freeze(next) });
  };

  return (
    <>
      <section
        className="temporal-create-section"
        aria-labelledby="temporal-create-recurrence-heading"
      >
        <div className="temporal-create-section__heading">
          <div>
            <h3 id="temporal-create-recurrence-heading">
              {fields.kind === 'event'
                ? t(($) => $.common.home.timeline.create.recurrence.title)
                : t(($) => $.common.home.timeline.create.recurrence.activityTitle)}
            </h3>
            <p>
              {fields.kind === 'event'
                ? t(($) => $.common.home.timeline.create.recurrence.description)
                : t(
                    ($) =>
                      $.common.home.timeline.create.recurrence.activityDescription,
                  )}
            </p>
          </div>
        </div>

        {fields.kind === 'activity' ? (
          <>
            <div className="temporal-create-field-readout">
              <span>
                {t(($) => $.common.home.timeline.create.handoffs.routine)}
              </span>
              <strong>
                {t(($) => $.common.home.timeline.create.handoffs.ownerRequired)}
              </strong>
            </div>
            <p className="temporal-create-truth-note">
              {t(($) => $.common.home.timeline.create.recurrence.activityHandoff)}
            </p>
          </>
        ) : (
          <>
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.recurrence.patternKind)}
              </span>
              <select
                value={recurrence.patternKind}
                onChange={(event) =>
                  patchRecurrence({
                    patternKind: event.currentTarget
                      .value as TemporalCreateFields['eventRecurrence']['patternKind'],
                  })
                }
              >
                <option value="none">
                  {t(($) => $.common.home.timeline.create.recurrence.none)}
                </option>
                <option value="calendar-wall-clock">
                  {t(($) => $.common.home.timeline.create.recurrence.calendarWallClock)}
                </option>
                <option value="elapsed-interval">
                  {t(($) => $.common.home.timeline.create.recurrence.elapsedInterval)}
                </option>
                <option value="quota-per-period">
                  {t(($) => $.common.home.timeline.create.recurrence.quotaPerPeriod)}
                </option>
                <option value="cyclic-positional">
                  {t(($) => $.common.home.timeline.create.recurrence.cyclicPositional)}
                </option>
              </select>
            </label>

            {recurrence.patternKind === 'calendar-wall-clock' ? (
              <>
                <div className="temporal-create-grid two">
                  <label className="temporal-create-control">
                    <span>
                      {t(($) => $.common.home.timeline.create.recurrence.frequency)}
                    </span>
                    <select
                      value={recurrence.calendarFrequency}
                      onChange={(event) =>
                        patchRecurrence({
                          calendarFrequency: event.currentTarget
                            .value as TemporalCreateFields['eventRecurrence']['calendarFrequency'],
                        })
                      }
                    >
                      <option value="daily">
                        {t(($) => $.common.home.timeline.create.recurrence.daily)}
                      </option>
                      <option value="weekly">
                        {t(($) => $.common.home.timeline.create.recurrence.weekly)}
                      </option>
                      <option value="monthly">
                        {t(($) => $.common.home.timeline.create.recurrence.monthly)}
                      </option>
                    </select>
                  </label>
                  <label className="temporal-create-control">
                    <span>
                      {t(($) => $.common.home.timeline.create.recurrence.interval)}
                    </span>
                    <input
                      data-create-path="eventRecurrence.calendarInterval"
                      type="number"
                      min="1"
                      max="365"
                      value={recurrence.calendarInterval}
                      onChange={(event) =>
                        patchRecurrence({
                          calendarInterval: Number(event.currentTarget.value),
                        })
                      }
                    />
                    {renderError('eventRecurrence.calendarInterval')}
                  </label>
                </div>
                {recurrence.calendarFrequency === 'weekly' ? (
                  <div
                    className="temporal-create-weekdays"
                    data-create-path="eventRecurrence.weekdays"
                    role="group"
                    aria-label={t(
                      ($) => $.common.home.timeline.create.recurrence.weekdays,
                    )}
                  >
                    {temporalCreateWeekdays().map((weekday) => (
                      <button
                        key={weekday}
                        type="button"
                        className={
                          recurrence.weekdays.includes(weekday) ? 'is-active' : ''
                        }
                        aria-pressed={recurrence.weekdays.includes(weekday)}
                        onClick={() => toggleWeekday(weekday)}
                      >
                        {weekdayLabel(weekday)}
                      </button>
                    ))}
                    {renderError('eventRecurrence.weekdays')}
                  </div>
                ) : null}
              </>
            ) : null}

            {recurrence.patternKind === 'elapsed-interval' ? (
              <label className="temporal-create-control">
                <span>
                  {t(($) => $.common.home.timeline.create.recurrence.elapsedMinutes)}
                </span>
                <input
                  data-create-path="eventRecurrence.elapsedIntervalMinutes"
                  type="number"
                  min="1"
                  max="525600"
                  value={recurrence.elapsedIntervalMinutes}
                  onChange={(event) =>
                    patchRecurrence({
                      elapsedIntervalMinutes: Number(event.currentTarget.value),
                    })
                  }
                />
                {renderError('eventRecurrence.elapsedIntervalMinutes')}
              </label>
            ) : null}

            {recurrence.patternKind === 'quota-per-period' ? (
              <div
                className="temporal-create-grid three"
                data-create-path="eventRecurrence.quota"
              >
                <label className="temporal-create-control">
                  <span>
                    {t(($) => $.common.home.timeline.create.recurrence.quotaCount)}
                  </span>
                  <input
                    type="number"
                    min="1"
                    max="999"
                    value={recurrence.quotaCount}
                    onChange={(event) =>
                      patchRecurrence({ quotaCount: Number(event.currentTarget.value) })
                    }
                  />
                </label>
                <label className="temporal-create-control">
                  <span>
                    {t(($) => $.common.home.timeline.create.recurrence.quotaPeriod)}
                  </span>
                  <select
                    value={recurrence.quotaPeriodKind}
                    onChange={(event) =>
                      patchRecurrence({
                        quotaPeriodKind: event.currentTarget
                          .value as TemporalCreateFields['eventRecurrence']['quotaPeriodKind'],
                      })
                    }
                  >
                    <option value="day">
                      {t(($) => $.common.home.timeline.create.recurrence.periodDay)}
                    </option>
                    <option value="week">
                      {t(($) => $.common.home.timeline.create.recurrence.periodWeek)}
                    </option>
                    <option value="month">
                      {t(($) => $.common.home.timeline.create.recurrence.periodMonth)}
                    </option>
                  </select>
                </label>
                <label className="temporal-create-control">
                  <span>
                    {t(($) => $.common.home.timeline.create.recurrence.periodInterval)}
                  </span>
                  <input
                    type="number"
                    min="1"
                    max="365"
                    value={recurrence.quotaPeriodInterval}
                    onChange={(event) =>
                      patchRecurrence({
                        quotaPeriodInterval: Number(event.currentTarget.value),
                      })
                    }
                  />
                </label>
                {renderError('eventRecurrence.quota')}
              </div>
            ) : null}

            {recurrence.patternKind === 'cyclic-positional' ? (
              <div
                className="temporal-create-grid three"
                data-create-path="eventRecurrence.cycle"
              >
                <label className="temporal-create-control">
                  <span>
                    {t(($) => $.common.home.timeline.create.recurrence.cycleLength)}
                  </span>
                  <input
                    type="number"
                    min="1"
                    max="10000"
                    value={recurrence.cycleLength}
                    onChange={(event) =>
                      patchRecurrence({ cycleLength: Number(event.currentTarget.value) })
                    }
                  />
                </label>
                <label className="temporal-create-control">
                  <span>
                    {t(($) => $.common.home.timeline.create.recurrence.cycleOffset)}
                  </span>
                  <input
                    type="number"
                    min="0"
                    max={Math.max(0, recurrence.cycleLength - 1)}
                    value={recurrence.cycleOffset}
                    onChange={(event) =>
                      patchRecurrence({ cycleOffset: Number(event.currentTarget.value) })
                    }
                  />
                </label>
                <label className="temporal-create-control">
                  <span>
                    {t(($) => $.common.home.timeline.create.recurrence.cycleUnit)}
                  </span>
                  <select
                    value={recurrence.cycleUnit}
                    onChange={(event) =>
                      patchRecurrence({
                        cycleUnit: event.currentTarget
                          .value as TemporalCreateFields['eventRecurrence']['cycleUnit'],
                      })
                    }
                  >
                    <option value="day">
                      {t(($) => $.common.home.timeline.create.recurrence.periodDay)}
                    </option>
                    <option value="week">
                      {t(($) => $.common.home.timeline.create.recurrence.periodWeek)}
                    </option>
                    <option value="month">
                      {t(($) => $.common.home.timeline.create.recurrence.periodMonth)}
                    </option>
                  </select>
                </label>
                {renderError('eventRecurrence.cycle')}
              </div>
            ) : null}

            {recurrence.patternKind !== 'none' ? (
              <div className="temporal-create-grid two">
                <label className="temporal-create-control">
                  <span>{t(($) => $.common.home.timeline.create.recurrence.ends)}</span>
                  <select
                    value={recurrence.endMode}
                    onChange={(event) =>
                      patchRecurrence({
                        endMode: event.currentTarget
                          .value as TemporalCreateFields['eventRecurrence']['endMode'],
                      })
                    }
                  >
                    <option value="none">
                      {t(($) => $.common.home.timeline.create.recurrence.never)}
                    </option>
                    <option value="until-date">
                      {t(($) => $.common.home.timeline.create.recurrence.until)}
                    </option>
                    <option value="count">
                      {t(($) => $.common.home.timeline.create.recurrence.afterCount)}
                    </option>
                  </select>
                </label>
                {recurrence.endMode === 'until-date' ? (
                  <label className="temporal-create-control">
                    <span>
                      {t(($) => $.common.home.timeline.create.recurrence.untilDate)}
                    </span>
                    <input
                      data-create-path="eventRecurrence.untilDate"
                      type="date"
                      value={recurrence.untilDate}
                      onChange={(event) =>
                        patchRecurrence({ untilDate: event.currentTarget.value })
                      }
                    />
                    {renderError('eventRecurrence.untilDate')}
                  </label>
                ) : recurrence.endMode === 'count' ? (
                  <label className="temporal-create-control">
                    <span>
                      {t(($) => $.common.home.timeline.create.recurrence.count)}
                    </span>
                    <input
                      data-create-path="eventRecurrence.count"
                      type="number"
                      min="1"
                      max="999"
                      value={recurrence.count}
                      onChange={(event) =>
                        patchRecurrence({ count: Number(event.currentTarget.value) })
                      }
                    />
                    {renderError('eventRecurrence.count')}
                  </label>
                ) : null}
              </div>
            ) : null}

            {recurrence.patternKind !== 'none' ? (
              <p className="temporal-create-truth-note">
                {t(($) => $.common.home.timeline.create.recurrence.backendNote)}
              </p>
            ) : null}
          </>
        )}
      </section>

      <section
        className="temporal-create-section"
        aria-labelledby="temporal-create-confirmation-heading"
      >
        <div className="temporal-create-section__heading">
          <div>
            <h3 id="temporal-create-confirmation-heading">
              {t(($) => $.common.home.timeline.create.confirmation.title)}
            </h3>
            <p>{t(($) => $.common.home.timeline.create.confirmation.description)}</p>
          </div>
        </div>
        <div className="temporal-create-grid two">
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.confirmation.outcome)}
            </span>
            <select
              value={confirmation.outcomePolicy}
              onChange={(event) =>
                patchConfirmation({
                  outcomePolicy: event.currentTarget
                    .value as TemporalCreateFields['confirmation']['outcomePolicy'],
                })
              }
            >
              <option value="inherit">
                {t(($) => $.common.home.timeline.create.confirmation.inherit)}
              </option>
              <option value="ask-immediately">
                {t(($) => $.common.home.timeline.create.confirmation.askImmediately)}
              </option>
              <option value="ask-later">
                {t(($) => $.common.home.timeline.create.confirmation.askLater)}
              </option>
              <option value="daily-review">
                {t(($) => $.common.home.timeline.create.confirmation.dailyReview)}
              </option>
              <option value="weekly-review">
                {t(($) => $.common.home.timeline.create.confirmation.weeklyReview)}
              </option>
              <option value="silent">
                {t(($) => $.common.home.timeline.create.confirmation.silent)}
              </option>
              <option value="auto-complete">
                {t(($) => $.common.home.timeline.create.confirmation.autoComplete)}
              </option>
              <option value="auto-not-completed">
                {t(($) => $.common.home.timeline.create.confirmation.autoNotCompleted)}
              </option>
              <option value="infer-provisional">
                {t(($) => $.common.home.timeline.create.confirmation.inferProvisional)}
              </option>
            </select>
          </label>

          {depth === 'full' ? (
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.confirmation.reminder)}
              </span>
              <select
                data-create-path="confirmation.reminderLeadMinutes"
                value={
                  confirmation.reminderLeadMinutes === null
                    ? 'none'
                    : String(confirmation.reminderLeadMinutes)
                }
                onChange={(event) =>
                  patchConfirmation({
                    reminderLeadMinutes:
                      event.currentTarget.value === 'none'
                        ? null
                        : Number(event.currentTarget.value),
                  })
                }
              >
                {TEMPORAL_CREATE_REMINDER_OPTIONS.map((minutes) => (
                  <option
                    key={minutes === null ? 'none' : minutes}
                    value={minutes === null ? 'none' : minutes}
                  >
                    {minutes === null
                      ? t(($) => $.common.home.timeline.create.confirmation.noReminder)
                      : minutes === 0
                        ? t(($) => $.common.home.timeline.create.confirmation.atStart)
                        : t(
                            ($) => $.common.home.timeline.create.confirmation.before,
                            { value: temporalCreateDurationLabel(minutes) },
                          )}
                  </option>
                ))}
              </select>
              {renderError('confirmation.reminderLeadMinutes')}
            </label>
          ) : null}
        </div>

        {confirmation.outcomePolicy === 'infer-provisional' ? (
          <p className="temporal-create-truth-note">
            {t(($) => $.common.home.timeline.create.confirmation.inferNote)}
          </p>
        ) : null}
        <p className="temporal-create-truth-note">
          {t(($) => $.common.home.timeline.create.confirmation.deliveryNote)}
        </p>
      </section>
    </>
  );
}
