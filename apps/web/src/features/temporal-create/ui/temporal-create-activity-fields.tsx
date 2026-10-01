import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';

type ActivityFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export function TemporalCreateActivityFields({
  fields,
  onPatch,
  renderError,
}: ActivityFieldsProps) {
  const { t, i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const scheduling = fields.scheduling;
  const unplaced = fields.timeSemantics === 'unscheduled';

  const patchScheduling = (
    patch: Partial<TemporalCreateFields['scheduling']>,
  ) => onPatch({ scheduling: { ...scheduling, ...patch } });

  return (
    <section
      className="temporal-create-section is-wide"
      aria-labelledby="temporal-create-activity-planning-heading"
    >
      <div className="temporal-create-section__heading">
        <h3 id="temporal-create-activity-planning-heading">
          {italian ? 'Pianificazione' : 'Planning'}
        </h3>
      </div>

      {!unplaced ? (
        <div
          className="temporal-create-planning-mode"
          role="group"
          aria-label={italian ? 'Modalità di pianificazione' : 'Planning mode'}
        >
          <button type="button" className="is-active" aria-pressed="true">
            {italian ? 'Unica' : 'Single'}
          </button>
          <button
            type="button"
            disabled
            aria-pressed="false"
            title={
              italian
                ? 'La pianificazione suddivisa sarà collegata al percorso canonico multi-placement nel prossimo slice.'
                : 'Split planning will be connected to the canonical multi-placement path in the next slice.'
            }
          >
            {italian ? 'Suddivisa' : 'Split'}
          </button>
        </div>
      ) : null}

      {unplaced ? (
        <label className="temporal-create-control">
          <span>{italian ? 'Vincolo temporale' : 'Time constraint'}</span>
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
              {t(($) => $.common.home.timeline.create.planning.constraintDeadline)}
            </option>
            <option value="preferred-window">
              {t(($) => $.common.home.timeline.create.planning.constraintPreferred)}
            </option>
          </select>
        </label>
      ) : (
        <div className="temporal-create-candidate-control" aria-disabled="true">
          <div>
            <strong>{italian ? 'Proteggi collocazione' : 'Protect placement'}</strong>
            <small>
              {italian
                ? 'utente + automazioni Dante'
                : 'user + Dante automations'}
            </small>
          </div>
          <button
            type="button"
            disabled
            aria-label={
              italian
                ? 'Proteggi collocazione, da collegare'
                : 'Protect placement, not wired yet'
            }
          >
            {italian ? 'Da collegare' : 'Not wired'}
          </button>
        </div>
      )}

      {unplaced && scheduling.constraintKind === 'bounded-window' ? (
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

      {unplaced && scheduling.constraintKind === 'deadline' ? (
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

      {unplaced && scheduling.constraintKind === 'preferred-window' ? (
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
    </section>
  );
}
