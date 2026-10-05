import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';

import './temporal-create-activity-polish.css';

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

  /* Timed Activity planning is authored by the interval surface above. Keep
     this section only for B04 constraints that still belong to an unplaced
     Activity; do not render a second, empty "Pianificazione" surface. */
  if (!unplaced) return null;

  const patchScheduling = (
    patch: Partial<TemporalCreateFields['scheduling']>,
  ) => onPatch({ scheduling: { ...scheduling, ...patch } });

  return (
    <section
      className="temporal-create-section is-wide"
      aria-labelledby="temporal-create-activity-constraints-heading"
    >
      <div className="temporal-create-section__heading">
        <h3 id="temporal-create-activity-constraints-heading">
          {italian ? 'Vincoli temporali' : 'Time constraints'}
        </h3>
      </div>

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
                patchScheduling({
                  earliestStartDate: event.currentTarget.value,
                })
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
                patchScheduling({
                  earliestStartTime: event.currentTarget.value,
                })
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
                patchScheduling({
                  preferredStartTime: event.currentTarget.value,
                })
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
