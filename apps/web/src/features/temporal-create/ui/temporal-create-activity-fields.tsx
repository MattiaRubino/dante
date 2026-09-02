import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import {
  TEMPORAL_CREATE_BUFFER_OPTIONS,
  temporalCreateDurationLabel,
} from './temporal-create-field-shared';

type ActivityFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export function TemporalCreateActivityFields({
  fields,
  depth,
  onPatch,
  renderError,
}: ActivityFieldsProps) {
  const { t } = useTranslation('common');
  const scheduling = fields.scheduling;
  const execution = fields.execution;
  const patchScheduling = (
    patch: Partial<TemporalCreateFields['scheduling']>,
  ) => onPatch({ scheduling: { ...scheduling, ...patch } });
  const patchExecution = (
    patch: Partial<TemporalCreateFields['execution']>,
  ) => onPatch({ execution: { ...execution, ...patch } });

  return (
    <section
      className="temporal-create-section"
      aria-labelledby="temporal-create-planning-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-planning-heading">
            {t(($) => $.common.home.timeline.create.planning.title)}
          </h3>
          <p>{t(($) => $.common.home.timeline.create.planning.description)}</p>
        </div>
      </div>

      <div className="temporal-create-grid three">
        <label className="temporal-create-control">
          <span>{`${t(($) => $.common.home.timeline.create.duration)} (min)`}</span>
          <input
            data-create-path="durationMinutes"
            type="number"
            min="5"
            max="10080"
            step="5"
            inputMode="numeric"
            value={fields.durationMinutes}
            onChange={(event) =>
              onPatch({ durationMinutes: Number(event.currentTarget.value) })
            }
          />
          {renderError('durationMinutes')}
        </label>

        <label className="temporal-create-control">
          <span>{t(($) => $.common.home.timeline.create.planning.constraint)}</span>
          <select
            value={scheduling.constraintKind}
            onChange={(event) =>
              patchScheduling({
                constraintKind: event.currentTarget
                  .value as TemporalCreateFields['scheduling']['constraintKind'],
              })
            }
          >
            <option value="none">
              {t(($) => $.common.home.timeline.create.planning.constraintNone)}
            </option>
            <option value="open">
              {t(($) => $.common.home.timeline.create.planning.constraintOpen)}
            </option>
            <option value="bounded-window">
              {t(($) => $.common.home.timeline.create.planning.constraintWindow)}
            </option>
            <option value="deadline">
              {t(
                ($) => $.common.home.timeline.create.planning.constraintDeadline,
              )}
            </option>
            <option value="preferred-window">
              {t(
                ($) =>
                  $.common.home.timeline.create.planning.constraintPreferred,
              )}
            </option>
          </select>
        </label>

        <label className="temporal-create-control">
          <span>{t(($) => $.common.home.timeline.create.planning.movement)}</span>
          <select
            value={scheduling.movementPolicy}
            onChange={(event) =>
              patchScheduling({
                movementPolicy: event.currentTarget
                  .value as TemporalCreateFields['scheduling']['movementPolicy'],
              })
            }
          >
            <option value="locked">
              {t(($) => $.common.home.timeline.create.planning.movementLocked)}
            </option>
            <option value="window">
              {t(($) => $.common.home.timeline.create.planning.movementWindow)}
            </option>
            <option value="confirm">
              {t(($) => $.common.home.timeline.create.planning.movementConfirm)}
            </option>
            <option value="free">
              {t(($) => $.common.home.timeline.create.planning.movementFree)}
            </option>
          </select>
        </label>
      </div>

      {scheduling.constraintKind === 'bounded-window' ? (
        <div
          className="temporal-create-grid four"
          data-create-path="scheduling.window"
        >
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.windowStartDate)}
            </span>
            <input
              type="date"
              value={scheduling.windowStartDate}
              onChange={(event) =>
                patchScheduling({ windowStartDate: event.currentTarget.value })
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.windowStartTime)}
            </span>
            <input
              type="time"
              value={scheduling.windowStartTime}
              onChange={(event) =>
                patchScheduling({ windowStartTime: event.currentTarget.value })
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.windowEndDate)}
            </span>
            <input
              type="date"
              value={scheduling.windowEndDate}
              onChange={(event) =>
                patchScheduling({ windowEndDate: event.currentTarget.value })
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.windowEndTime)}
            </span>
            <input
              type="time"
              value={scheduling.windowEndTime}
              onChange={(event) =>
                patchScheduling({ windowEndTime: event.currentTarget.value })
              }
            />
          </label>
          {renderError('scheduling.window')}
        </div>
      ) : null}

      {scheduling.constraintKind === 'deadline' ? (
        <div
          className="temporal-create-grid four"
          data-create-path="scheduling.deadline"
        >
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.earliestDate)}
            </span>
            <input
              type="date"
              value={scheduling.earliestStartDate}
              onChange={(event) =>
                patchScheduling({ earliestStartDate: event.currentTarget.value })
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.earliestTime)}
            </span>
            <input
              type="time"
              value={scheduling.earliestStartTime}
              onChange={(event) =>
                patchScheduling({ earliestStartTime: event.currentTarget.value })
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.deadlineDate)}
            </span>
            <input
              type="date"
              value={scheduling.deadlineDate}
              onChange={(event) =>
                patchScheduling({ deadlineDate: event.currentTarget.value })
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.deadlineTime)}
            </span>
            <input
              type="time"
              value={scheduling.deadlineTime}
              onChange={(event) =>
                patchScheduling({ deadlineTime: event.currentTarget.value })
              }
            />
          </label>
          {renderError('scheduling.deadline')}
        </div>
      ) : null}

      {scheduling.constraintKind === 'preferred-window' ? (
        <div
          className="temporal-create-grid two"
          data-create-path="scheduling.preferredWindow"
        >
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.preferredStart)}
            </span>
            <input
              type="time"
              value={scheduling.preferredStartTime}
              onChange={(event) =>
                patchScheduling({ preferredStartTime: event.currentTarget.value })
              }
            />
          </label>
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.planning.preferredEnd)}
            </span>
            <input
              type="time"
              value={scheduling.preferredEndTime}
              onChange={(event) =>
                patchScheduling({ preferredEndTime: event.currentTarget.value })
              }
            />
          </label>
          {renderError('scheduling.preferredWindow')}
        </div>
      ) : null}

      {depth === 'full' ? (
        <label className="temporal-create-control">
          <span>{t(($) => $.common.home.timeline.create.planning.fallback)}</span>
          <select
            value={scheduling.fallbackPolicy}
            onChange={(event) =>
              patchScheduling({
                fallbackPolicy: event.currentTarget
                  .value as TemporalCreateFields['scheduling']['fallbackPolicy'],
              })
            }
          >
            <option value="inherit">
              {t(($) => $.common.home.timeline.create.planning.fallbackInherit)}
            </option>
            <option value="skip">
              {t(($) => $.common.home.timeline.create.planning.fallbackSkip)}
            </option>
            <option value="same-window">
              {t(($) => $.common.home.timeline.create.planning.fallbackWindow)}
            </option>
            <option value="next-valid-date">
              {t(($) => $.common.home.timeline.create.planning.fallbackNext)}
            </option>
            <option value="shorten-or-split">
              {t(($) => $.common.home.timeline.create.planning.fallbackSplit)}
            </option>
            <option value="replan-dependencies">
              {t(($) => $.common.home.timeline.create.planning.fallbackReplan)}
            </option>
          </select>
        </label>
      ) : null}

      <div className="temporal-create-divider" />

      <div className="temporal-create-grid two">
        <label className="temporal-create-control">
          <span>{t(($) => $.common.home.timeline.create.execution.structure)}</span>
          <select
            value={execution.sessionMode}
            onChange={(event) =>
              patchExecution({
                sessionMode: event.currentTarget
                  .value as TemporalCreateFields['execution']['sessionMode'],
              })
            }
          >
            <option value="indivisible">
              {t(($) => $.common.home.timeline.create.execution.indivisible)}
            </option>
            <option value="splittable">
              {t(($) => $.common.home.timeline.create.execution.splittable)}
            </option>
          </select>
        </label>
        {execution.sessionMode === 'splittable' ? (
          <label className="temporal-create-control">
            <span>
              {t(($) => $.common.home.timeline.create.execution.minimumSession)}
            </span>
            <input
              data-create-path="execution.minSessionMinutes"
              type="number"
              min="5"
              step="5"
              value={execution.minSessionMinutes}
              onChange={(event) =>
                patchExecution({
                  minSessionMinutes: Number(event.currentTarget.value),
                })
              }
            />
            {renderError('execution.minSessionMinutes')}
          </label>
        ) : null}
      </div>

      {depth === 'full' && execution.sessionMode === 'splittable' ? (
        <label className="temporal-create-control">
          <span>
            {t(($) => $.common.home.timeline.create.execution.maximumSessions)}
          </span>
          <input
            data-create-path="execution.maxSessions"
            type="number"
            min="2"
            max="99"
            value={execution.maxSessions ?? ''}
            placeholder={t(
              ($) => $.common.home.timeline.create.execution.noMaximum,
            )}
            onChange={(event) =>
              patchExecution({
                maxSessions:
                  event.currentTarget.value === ''
                    ? null
                    : Number(event.currentTarget.value),
              })
            }
          />
          {renderError('execution.maxSessions')}
        </label>
      ) : null}

      {depth === 'full' ? (
        <>
          <div className="temporal-create-grid three">
            <label className="temporal-create-control">
              <span>
                {t(($) => $.common.home.timeline.create.execution.preparation)}
              </span>
              <select
                value={execution.preparationMinutes}
                onChange={(event) =>
                  patchExecution({
                    preparationMinutes: Number(event.currentTarget.value),
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
                {t(($) => $.common.home.timeline.create.execution.recovery)}
              </span>
              <select
                value={execution.recoveryMinutes}
                onChange={(event) =>
                  patchExecution({
                    recoveryMinutes: Number(event.currentTarget.value),
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
                {t(($) => $.common.home.timeline.create.execution.spacing)}
              </span>
              <select
                value={execution.spacingMinutes}
                onChange={(event) =>
                  patchExecution({
                    spacingMinutes: Number(event.currentTarget.value),
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
          </div>
          {renderError('execution.buffers')}
          <div className="temporal-create-check-grid">
            <label>
              <input
                type="checkbox"
                checked={execution.partialAllowed}
                onChange={(event) =>
                  patchExecution({ partialAllowed: event.currentTarget.checked })
                }
              />
              <span>
                {t(($) => $.common.home.timeline.create.execution.partial)}
              </span>
            </label>
            <label>
              <input
                type="checkbox"
                checked={execution.finishEarlyAllowed}
                onChange={(event) =>
                  patchExecution({
                    finishEarlyAllowed: event.currentTarget.checked,
                  })
                }
              />
              <span>
                {t(($) => $.common.home.timeline.create.execution.finishEarly)}
              </span>
            </label>
            <label>
              <input
                type="checkbox"
                checked={execution.mergeCompatible}
                onChange={(event) =>
                  patchExecution({
                    mergeCompatible: event.currentTarget.checked,
                  })
                }
              />
              <span>
                {t(
                  ($) =>
                    $.common.home.timeline.create.execution.mergeCompatible,
                )}
              </span>
            </label>
          </div>
        </>
      ) : null}
    </section>
  );
}
