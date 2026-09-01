import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import {
  TEMPORAL_CREATE_DURATION_OPTIONS,
  temporalCreateDurationLabel,
} from './temporal-create-field-shared';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

type TemporalCreateCoreFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  contexts: readonly TemporalCreateContextOption[];
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export function TemporalCreateCoreFields({
  fields,
  contexts,
  onPatch,
  renderError,
}: TemporalCreateCoreFieldsProps) {
  const { t } = useTranslation('common');
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

  return (
    <>
      <div className="temporal-create-quick-properties">
        <label className="temporal-create-compact-control">
          <span>{t(($) => $.common.home.timeline.create.kind.label)}</span>
          <select
            value={fields.kind}
            onChange={(event) =>
              onPatch({
                kind: event.currentTarget.value as TemporalCreateFields['kind'],
              })
            }
          >
            <option value="activity">
              {t(($) => $.common.home.timeline.create.kind.activity)}
            </option>
            <option value="event">
              {t(($) => $.common.home.timeline.create.kind.event)}
            </option>
          </select>
        </label>

        <label className="temporal-create-compact-control">
          <span>{t(($) => $.common.home.timeline.create.context)}</span>
          <select
            data-create-path="contextId"
            value={fields.contextId}
            onChange={(event) => onPatch({ contextId: event.currentTarget.value })}
          >
            {contexts.map((context) => (
              <option key={context.id} value={context.id}>
                {context.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      <fieldset
        className="temporal-create-choice-group"
        data-create-path="timeSemantics"
        role="radiogroup"
      >
        <legend>
          {t(($) => $.common.home.timeline.create.timeSemantics.label)}
        </legend>
        <div className="temporal-create-choice-row">
          {(['timed', 'all-day', 'unscheduled'] as const).map((semantics) => (
            <button
              key={semantics}
              type="button"
              role="radio"
              aria-checked={fields.timeSemantics === semantics}
              disabled={fields.kind === 'event' && semantics === 'unscheduled'}
              className={fields.timeSemantics === semantics ? 'is-active' : ''}
              onClick={() =>
                onPatch({
                  timeSemantics: semantics,
                  scheduling:
                    semantics === 'unscheduled'
                      ? fields.scheduling
                      : { ...fields.scheduling, constraintKind: 'none' },
                })
              }
            >
              {semantics === 'timed'
                ? t(($) => $.common.home.timeline.create.timeSemantics.timed)
                : semantics === 'all-day'
                  ? t(($) => $.common.home.timeline.create.timeSemantics.allDay)
                  : t(
                      ($) =>
                        $.common.home.timeline.create.timeSemantics.unscheduled,
                    )}
            </button>
          ))}
        </div>
      </fieldset>
      {renderError('timeSemantics')}

      {fields.timeSemantics === 'timed' ? (
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
              onChange={(event) =>
                onPatch({ startTime: event.currentTarget.value })
              }
            />
            {renderError('startTime')}
          </label>
          {durationControl}
        </div>
      ) : fields.timeSemantics === 'all-day' ? (
        <div
          className={`temporal-create-grid ${
            fields.kind === 'event' ? 'two' : 'one'
          }`}
        >
          <label className="temporal-create-control">
            <span>
              {fields.kind === 'event'
                ? t(($) => $.common.home.timeline.create.eventDetails.startDate)
                : t(($) => $.common.home.timeline.create.date)}
            </span>
            <input
              data-create-path="date"
              type="date"
              value={fields.date}
              onChange={(event) => onPatch({ date: event.currentTarget.value })}
            />
            {renderError('date')}
          </label>
          {fields.kind === 'event' ? (
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
          ) : null}
        </div>
      ) : (
        <div className="temporal-create-grid one">{durationControl}</div>
      )}
    </>
  );
}
