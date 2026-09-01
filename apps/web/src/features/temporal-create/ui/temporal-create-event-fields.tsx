import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import {
  temporalCreateDurationFromEndDateTime,
  temporalCreateEndDateTime,
} from './temporal-create-field-shared';

type EventFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
}>;

export function TemporalCreateEventFields({
  fields,
  depth,
  onPatch,
}: EventFieldsProps) {
  const { t } = useTranslation('common');
  const event = fields.event;
  const patchEvent = (patch: Partial<TemporalCreateFields['event']>) =>
    onPatch({ event: { ...event, ...patch } });
  const end = temporalCreateEndDateTime(
    fields.date,
    fields.startTime,
    fields.durationMinutes,
  );

  const patchEnd = (endDate: string, endTime: string) => {
    const duration = temporalCreateDurationFromEndDateTime(
      fields.date,
      fields.startTime,
      endDate,
      endTime,
    );
    if (duration !== null) {
      onPatch({ durationMinutes: duration });
    }
  };

  return (
    <section
      className="temporal-create-section"
      aria-labelledby="temporal-create-event-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-event-heading">
            {t(($) => $.common.home.timeline.create.eventDetails.title)}
          </h3>
          <p>
            {t(($) => $.common.home.timeline.create.eventDetails.description)}
          </p>
        </div>
      </div>

      {fields.timeSemantics === 'timed' ? (
        <div className="temporal-create-grid three">
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.eventDetails.endDate)}
            </span>
            <input
              type="date"
              value={end.date}
              onChange={(inputEvent) =>
                patchEnd(inputEvent.currentTarget.value, end.time)
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.eventDetails.endTime)}
            </span>
            <input
              type="time"
              value={end.time}
              onChange={(inputEvent) =>
                patchEnd(end.date, inputEvent.currentTarget.value)
              }
            />
            {end.dayOffset > 0 ? (
              <small className="temporal-create-field-note">
                {t(
                  ($) => $.common.home.timeline.create.eventDetails.nextDay,
                  { count: end.dayOffset },
                )}
              </small>
            ) : null}
          </label>
          <div className="temporal-create-field-readout">
            <span>{t(($) => $.common.home.timeline.create.duration)}</span>
            <strong>{fields.durationMinutes} min</strong>
          </div>
        </div>
      ) : null}

      <label className="temporal-create-control">
        <span>{t(($) => $.common.home.timeline.create.eventDetails.location)}</span>
        <input
          type="text"
          value={event.location}
          onChange={(inputEvent) =>
            patchEvent({ location: inputEvent.currentTarget.value })
          }
          placeholder={t(
            ($) => $.common.home.timeline.create.eventDetails.locationPlaceholder,
          )}
        />
      </label>

      <div className="temporal-create-grid two">
        <label className="temporal-create-control">
          <span>
            {t(($) => $.common.home.timeline.create.eventDetails.availability)}
          </span>
          <select
            value={event.availability}
            onChange={(inputEvent) =>
              patchEvent({
                availability: inputEvent.currentTarget
                  .value as TemporalCreateFields['event']['availability'],
              })
            }
          >
            <option value="busy">
              {t(($) => $.common.home.timeline.create.eventDetails.busy)}
            </option>
            <option value="free">
              {t(($) => $.common.home.timeline.create.eventDetails.free)}
            </option>
          </select>
        </label>
        <label className="temporal-create-control">
          <span>
            {t(($) => $.common.home.timeline.create.eventDetails.visibility)}
          </span>
          <select
            value={event.visibility}
            onChange={(inputEvent) =>
              patchEvent({
                visibility: inputEvent.currentTarget
                  .value as TemporalCreateFields['event']['visibility'],
              })
            }
          >
            <option value="default">
              {t(
                ($) =>
                  $.common.home.timeline.create.eventDetails.visibilityDefault,
              )}
            </option>
            <option value="private">
              {t(
                ($) =>
                  $.common.home.timeline.create.eventDetails.visibilityPrivate,
              )}
            </option>
            <option value="public">
              {t(
                ($) =>
                  $.common.home.timeline.create.eventDetails.visibilityPublic,
              )}
            </option>
          </select>
        </label>
      </div>

      {depth === 'full' ? (
        <>
          <div className="temporal-create-divider" />
          <div className="temporal-create-grid two">
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.integrations.participants)}
              </span>
              <textarea
                rows={3}
                value={event.participants}
                onChange={(inputEvent) =>
                  patchEvent({ participants: inputEvent.currentTarget.value })
                }
                placeholder={t(
                  ($) =>
                    $.common.home.timeline.create.integrations
                      .participantsPlaceholder,
                )}
              />
            </label>
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.integrations.resources)}
              </span>
              <textarea
                rows={3}
                value={event.resources}
                onChange={(inputEvent) =>
                  patchEvent({ resources: inputEvent.currentTarget.value })
                }
                placeholder={t(
                  ($) =>
                    $.common.home.timeline.create.integrations
                      .resourcesPlaceholder,
                )}
              />
            </label>
          </div>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.integrations.conference)}
            </span>
            <select
              value={event.conferenceMode}
              onChange={(inputEvent) =>
                patchEvent({
                  conferenceMode: inputEvent.currentTarget
                    .value as TemporalCreateFields['event']['conferenceMode'],
                })
              }
            >
              <option value="none">
                {t(($) => $.common.home.timeline.create.integrations.none)}
              </option>
              <option value="provider-default">
                {t(
                  ($) =>
                    $.common.home.timeline.create.integrations.providerDefault,
                )}
              </option>
            </select>
          </label>
          <p className="temporal-create-truth-note">
            {t(
              ($) => $.common.home.timeline.create.integrations.providerRequired,
            )}
          </p>
        </>
      ) : null}
    </section>
  );
}
