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

function weekdayLabel(
  weekday: TemporalCreateWeekday,
  t: ReturnType<typeof useTranslation>['t'],
): string {
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
}

export function TemporalCreateRecurrenceFields({
  fields,
  depth,
  onPatch,
  renderError,
}: RecurrenceFieldsProps) {
  const { t } = useTranslation('common');
  const recurrence = fields.recurrence;
  const confirmation = fields.confirmation;
  const patchRecurrence = (
    patch: Partial<TemporalCreateFields['recurrence']>,
  ) => onPatch({ recurrence: { ...recurrence, ...patch } });
  const patchConfirmation = (
    patch: Partial<TemporalCreateFields['confirmation']>,
  ) => onPatch({ confirmation: { ...confirmation, ...patch } });

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
    <section
      className="temporal-create-section"
      aria-labelledby="temporal-create-recurrence-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-recurrence-heading">
            {t(($) => $.common.home.timeline.create.recurrence.title)}
          </h3>
          <p>
            {t(($) => $.common.home.timeline.create.recurrence.description)}
          </p>
        </div>
      </div>

      <div className="temporal-create-grid two">
        <label className="temporal-create-control">
          <span>
            {t(($) => $.common.home.timeline.create.recurrence.frequency)}
          </span>
          <select
            value={recurrence.frequency}
            onChange={(event) =>
              patchRecurrence({
                frequency: event.currentTarget
                  .value as TemporalCreateFields['recurrence']['frequency'],
              })
            }
          >
            <option value="none">
              {t(($) => $.common.home.timeline.create.recurrence.none)}
            </option>
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

        {recurrence.frequency !== 'none' ? (
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.recurrence.interval)}
            </span>
            <input
              data-create-path="recurrence.interval"
              type="number"
              min="1"
              max="365"
              value={recurrence.interval}
              onChange={(event) =>
                patchRecurrence({ interval: Number(event.currentTarget.value) })
              }
            />
            {renderError('recurrence.interval')}
          </label>
        ) : null}
      </div>

      {recurrence.frequency === 'weekly' ? (
        <div
          className="temporal-create-weekdays"
          data-create-path="recurrence.weekdays"
          role="group"
          aria-label={t(
            ($) => $.common.home.timeline.create.recurrence.weekdays,
          )}
        >
          {temporalCreateWeekdays().map((weekday) => (
            <button
              key={weekday}
              type="button"
              className={recurrence.weekdays.includes(weekday) ? 'is-active' : ''}
              aria-pressed={recurrence.weekdays.includes(weekday)}
              onClick={() => toggleWeekday(weekday)}
            >
              {weekdayLabel(weekday, t)}
            </button>
          ))}
          {renderError('recurrence.weekdays')}
        </div>
      ) : null}

      {recurrence.frequency !== 'none' ? (
        <div className="temporal-create-grid two">
          <label className="temporal-create-control">
            <span>{t(($) => $.common.home.timeline.create.recurrence.ends)}</span>
            <select
              value={recurrence.endMode}
              onChange={(event) =>
                patchRecurrence({
                  endMode: event.currentTarget
                    .value as TemporalCreateFields['recurrence']['endMode'],
                })
              }
            >
              <option value="never">
                {t(($) => $.common.home.timeline.create.recurrence.never)}
              </option>
              <option value="date">
                {t(($) => $.common.home.timeline.create.recurrence.until)}
              </option>
              <option value="count">
                {t(($) => $.common.home.timeline.create.recurrence.afterCount)}
              </option>
            </select>
          </label>
          {recurrence.endMode === 'date' ? (
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.recurrence.untilDate)}
              </span>
              <input
                data-create-path="recurrence.untilDate"
                type="date"
                value={recurrence.untilDate}
                onChange={(event) =>
                  patchRecurrence({ untilDate: event.currentTarget.value })
                }
              />
              {renderError('recurrence.untilDate')}
            </label>
          ) : recurrence.endMode === 'count' ? (
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.recurrence.count)}
              </span>
              <input
                data-create-path="recurrence.count"
                type="number"
                min="1"
                max="999"
                value={recurrence.count}
                onChange={(event) =>
                  patchRecurrence({ count: Number(event.currentTarget.value) })
                }
              />
              {renderError('recurrence.count')}
            </label>
          ) : null}
        </div>
      ) : null}

      <div className="temporal-create-divider" />

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
              {t(
                ($) => $.common.home.timeline.create.confirmation.askImmediately,
              )}
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
              {t(
                ($) =>
                  $.common.home.timeline.create.confirmation.autoNotCompleted,
              )}
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
                    ? t(
                        ($) =>
                          $.common.home.timeline.create.confirmation.noReminder,
                      )
                    : minutes === 0
                      ? t(
                          ($) =>
                            $.common.home.timeline.create.confirmation.atStart,
                        )
                      : t(
                          ($) =>
                            $.common.home.timeline.create.confirmation.before,
                          { value: temporalCreateDurationLabel(minutes) },
                        )}
                </option>
              ))}
            </select>
            {renderError('confirmation.reminderLeadMinutes')}
          </label>
        ) : null}
      </div>

      {depth !== 'quick' ? (
        <p className="temporal-create-truth-note">
          {t(
            ($) => $.common.home.timeline.create.confirmation.deliveryNote,
          )}
        </p>
      ) : null}
    </section>
  );
}
