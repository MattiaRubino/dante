import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import { TemporalCreateEventAgenda } from './temporal-create-event-agenda';
import {
  TEMPORAL_CREATE_BUFFER_OPTIONS,
  temporalCreateDurationLabel,
} from './temporal-create-field-shared';

type EventFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export function TemporalCreateEventFields({
  fields,
  depth,
  onPatch,
  renderError,
}: EventFieldsProps) {
  const { t } = useTranslation('common');
  const event = fields.event;
  const patchEvent = (patch: Partial<TemporalCreateFields['event']>) =>
    onPatch({ event: { ...event, ...patch } });

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
          <div className="temporal-create-section__heading">
            <div>
              <h4>
                {t(
                  ($) => $.common.home.timeline.create.eventDetails.intentTitle,
                )}
              </h4>
              <p>
                {t(
                  ($) =>
                    $.common.home.timeline.create.eventDetails
                      .intentDescription,
                )}
              </p>
            </div>
          </div>
          <div className="temporal-create-grid two">
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.eventDetails.purpose)}
              </span>
              <textarea
                rows={3}
                value={event.purpose}
                onChange={(inputEvent) =>
                  patchEvent({ purpose: inputEvent.currentTarget.value })
                }
                placeholder={t(
                  ($) =>
                    $.common.home.timeline.create.eventDetails
                      .purposePlaceholder,
                )}
              />
            </label>
            <label className="temporal-create-control">
              <span>
                {t(
                  ($) =>
                    $.common.home.timeline.create.eventDetails.expectedOutcome,
                )}
              </span>
              <textarea
                rows={3}
                value={event.expectedOutcome}
                onChange={(inputEvent) =>
                  patchEvent({
                    expectedOutcome: inputEvent.currentTarget.value,
                  })
                }
                placeholder={t(
                  ($) =>
                    $.common.home.timeline.create.eventDetails
                      .expectedOutcomePlaceholder,
                )}
              />
            </label>
          </div>
          <TemporalCreateEventAgenda
            parts={event.agendaParts}
            onChange={(agendaParts) => patchEvent({ agendaParts })}
          />
          <div className="temporal-create-check-grid">
            <label>
              <input
                type="checkbox"
                checked={event.decisionRequired}
                onChange={(inputEvent) =>
                  patchEvent({
                    decisionRequired: inputEvent.currentTarget.checked,
                  })
                }
              />
              <span>
                {t(
                  ($) =>
                    $.common.home.timeline.create.eventDetails.decisionRequired,
                )}
              </span>
            </label>
          </div>

          <div className="temporal-create-divider" />
          <div className="temporal-create-grid two">
            <label className="temporal-create-control">
              <span>
                {t(
                  ($) =>
                    $.common.home.timeline.create.integrations
                      .requiredParticipants,
                )}
              </span>
              <textarea
                rows={3}
                value={event.requiredParticipants}
                onChange={(inputEvent) =>
                  patchEvent({
                    requiredParticipants: inputEvent.currentTarget.value,
                  })
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
                {t(
                  ($) =>
                    $.common.home.timeline.create.integrations
                      .optionalParticipants,
                )}
              </span>
              <textarea
                rows={3}
                value={event.optionalParticipants}
                onChange={(inputEvent) =>
                  patchEvent({
                    optionalParticipants: inputEvent.currentTarget.value,
                  })
                }
                placeholder={t(
                  ($) =>
                    $.common.home.timeline.create.integrations
                      .participantsPlaceholder,
                )}
              />
            </label>
          </div>
          <div className="temporal-create-grid two">
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
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.integrations.preRead)}
              </span>
              <textarea
                rows={3}
                value={event.preRead}
                onChange={(inputEvent) =>
                  patchEvent({ preRead: inputEvent.currentTarget.value })
                }
                placeholder={t(
                  ($) =>
                    $.common.home.timeline.create.integrations
                      .preReadPlaceholder,
                )}
              />
            </label>
          </div>

          <div
            className="temporal-create-grid two"
            data-create-path="event.buffers"
          >
            <label className="temporal-create-control">
              <span>
                {t(
                  ($) => $.common.home.timeline.create.eventDetails.preparation,
                )}
              </span>
              <select
                value={event.preparationMinutes}
                onChange={(inputEvent) =>
                  patchEvent({
                    preparationMinutes: Number(inputEvent.currentTarget.value),
                  })
                }
              >
                {TEMPORAL_CREATE_BUFFER_OPTIONS.map((value) => (
                  <option key={value} value={value}>
                    {temporalCreateDurationLabel(value)}
                  </option>
                ))}
              </select>
            </label>
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.eventDetails.recovery)}
              </span>
              <select
                value={event.recoveryMinutes}
                onChange={(inputEvent) =>
                  patchEvent({
                    recoveryMinutes: Number(inputEvent.currentTarget.value),
                  })
                }
              >
                {TEMPORAL_CREATE_BUFFER_OPTIONS.map((value) => (
                  <option key={value} value={value}>
                    {temporalCreateDurationLabel(value)}
                  </option>
                ))}
              </select>
            </label>
            {renderError('event.buffers')}
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
              ($) =>
                $.common.home.timeline.create.integrations.providerRequired,
            )}
          </p>
        </>
      ) : null}
    </section>
  );
}
