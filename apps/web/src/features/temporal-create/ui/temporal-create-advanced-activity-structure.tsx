import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Temporal } from '@dante/time';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type {
  TemporalCreateActivityChildDraft,
  TemporalCreatePlannedSliceDraft,
} from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

import './temporal-create-advanced-activity-structure.css';

type TemporalCreateAdvancedActivityStructureProps = Readonly<{
  fields: TemporalCreateFields;
}>;

let nextStructureRowId = 0;
const newRowId = () => `structure-${++nextStructureRowId}`;

function rootInterval(fields: TemporalCreateFields): Readonly<{
  startDate: string;
  startTime: string;
  endDate: string;
  endTime: string;
}> {
  try {
    const start = Temporal.PlainDateTime.from(
      `${fields.date}T${fields.startTime}`,
    );
    const end = start.add({ minutes: fields.durationMinutes });
    return Object.freeze({
      startDate: start.toPlainDate().toString(),
      startTime: start.toPlainTime().toString({ smallestUnit: 'minute' }),
      endDate: end.toPlainDate().toString(),
      endTime: end.toPlainTime().toString({ smallestUnit: 'minute' }),
    });
  } catch {
    return Object.freeze({
      startDate: fields.date,
      startTime: fields.startTime,
      endDate: fields.date,
      endTime: fields.startTime,
    });
  }
}

function plannedSlice(
  fields: TemporalCreateFields,
  owner?: TemporalCreateActivityChildDraft,
): TemporalCreatePlannedSliceDraft {
  const root = rootInterval(fields);
  const useChild = owner?.scheduleEnabled === true;
  return Object.freeze({
    id: newRowId(),
    title: '',
    date: useChild ? owner.startDate : root.startDate,
    startTime: useChild ? owner.startTime : root.startTime,
    endTime: useChild ? owner.endTime : root.endTime,
  });
}

/**
 * Session capability is execution truth, not planning truth.
 * Enabling it means that the Activity can start a live B08 Session after
 * creation. Planned Session rows below remain Schedule-only intent.
 */
export function TemporalCreateAdvancedActivityHeaderActions() {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const structure = draft.activityStructure;
  const enabled = structure.captureMode !== 'disabled';

  return (
    <label
      className="temporal-create-structure-session-toggle"
      data-create-structure-actions
      data-session-capability="activity"
    >
      <input
        type="checkbox"
        checked={enabled}
        onChange={(event) =>
          patch({
            activityStructure: Object.freeze({
              ...structure,
              captureMode: event.currentTarget.checked ? 'live' : 'disabled',
            }),
          })
        }
      />
      {italian ? 'Sessione' : 'Session'}
    </label>
  );
}

export function TemporalCreateAdvancedActivityStructure({
  fields,
}: TemporalCreateAdvancedActivityStructureProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const structure = draft.activityStructure;
  const [openTimes, setOpenTimes] = useState<readonly string[]>([]);

  const patchStructure = (changes: Partial<typeof structure>) =>
    patch({ activityStructure: Object.freeze({ ...structure, ...changes }) });

  const toggleTime = (id: string) =>
    setOpenTimes((current) =>
      current.includes(id)
        ? current.filter((entry) => entry !== id)
        : [...current, id],
    );

  const addRootSession = () => {
    patchStructure({
      plannedSlices: [...structure.plannedSlices, plannedSlice(fields)],
    });
  };

  const addChild = () => {
    const interval = rootInterval(fields);
    patchStructure({
      children: [
        ...structure.children,
        Object.freeze({
          id: newRowId(),
          title: '',
          requirementCode: 'required' as const,
          captureMode: 'disabled' as const,
          scheduleEnabled: false,
          startDate: interval.startDate,
          startTime: interval.startTime,
          endDate: interval.endDate,
          endTime: interval.endTime,
          plannedSlices: Object.freeze([]),
        }),
      ],
    });
  };

  const updateChild = (
    id: string,
    changes: Partial<TemporalCreateActivityChildDraft>,
  ) =>
    patchStructure({
      children: structure.children.map((child) =>
        child.id === id ? Object.freeze({ ...child, ...changes }) : child,
      ),
    });

  const updateSlice = (
    owner: string | null,
    id: string,
    changes: Partial<TemporalCreatePlannedSliceDraft>,
  ) => {
    if (owner === null) {
      patchStructure({
        plannedSlices: structure.plannedSlices.map((slice) =>
          slice.id === id ? Object.freeze({ ...slice, ...changes }) : slice,
        ),
      });
      return;
    }
    const child = structure.children.find((entry) => entry.id === owner);
    if (child) {
      updateChild(owner, {
        plannedSlices: child.plannedSlices.map((slice) =>
          slice.id === id ? Object.freeze({ ...slice, ...changes }) : slice,
        ),
      });
    }
  };

  const removeSlice = (owner: string | null, id: string) => {
    if (owner === null) {
      patchStructure({
        plannedSlices: structure.plannedSlices.filter(
          (slice) => slice.id !== id,
        ),
      });
      return;
    }
    const child = structure.children.find((entry) => entry.id === owner);
    if (child) {
      updateChild(owner, {
        plannedSlices: child.plannedSlices.filter((slice) => slice.id !== id),
      });
    }
  };

  const renderPlannedSlice = (
    slice: TemporalCreatePlannedSliceDraft,
    owner: string | null,
    level: 'root' | 'child',
  ) => {
    const timeId = `session:${slice.id}`;
    const timeOpen = openTimes.includes(timeId);
    return (
      <div
        className={`temporal-create-tree-item is-session is-${level}`}
        key={slice.id}
        data-create-planned-session
        data-create-owner={owner ?? 'root'}
      >
        <div className="temporal-create-tree-row">
          <span className="temporal-create-tree-row__icon" aria-hidden="true">
            ▶
          </span>
          <span className="temporal-create-tree-row__divider" aria-hidden="true" />
          <input
            className="temporal-create-tree-row__title"
            type="text"
            value={slice.title}
            maxLength={300}
            placeholder={italian ? 'Nome Sessione' : 'Session name'}
            aria-label={italian ? 'Nome Sessione' : 'Session name'}
            onChange={(event) =>
              updateSlice(owner, slice.id, { title: event.currentTarget.value })
            }
          />
          <div className="temporal-create-tree-row__actions">
            <button
              type="button"
              className={timeOpen ? 'is-active' : undefined}
              aria-expanded={timeOpen}
              aria-controls={`${timeId}:editor`}
              onClick={() => toggleTime(timeId)}
            >
              {italian ? 'Orario' : 'Time'}
            </button>
            <button
              type="button"
              className="is-remove"
              onClick={() => removeSlice(owner, slice.id)}
              aria-label={italian ? 'Rimuovi Sessione' : 'Remove Session'}
            >
              ×
            </button>
          </div>
        </div>
        {timeOpen ? (
          <div
            id={`${timeId}:editor`}
            className="temporal-create-tree-time-editor"
          >
            <label>
              <span>{italian ? 'Data' : 'Date'}</span>
              <input
                type="date"
                value={slice.date}
                onChange={(event) =>
                  updateSlice(owner, slice.id, {
                    date: event.currentTarget.value,
                  })
                }
              />
            </label>
            <label>
              <span>{italian ? 'Inizio' : 'Start'}</span>
              <input
                type="time"
                value={slice.startTime}
                onChange={(event) =>
                  updateSlice(owner, slice.id, {
                    startTime: event.currentTarget.value,
                  })
                }
              />
            </label>
            <label>
              <span>{italian ? 'Fine' : 'End'}</span>
              <input
                type="time"
                value={slice.endTime}
                onChange={(event) =>
                  updateSlice(owner, slice.id, {
                    endTime: event.currentTarget.value,
                  })
                }
              />
            </label>
          </div>
        ) : null}
      </div>
    );
  };

  return (
    <section
      className="temporal-create-activity-tree"
      data-create-activity-structure
      aria-label={italian ? 'Struttura attività' : 'Activity structure'}
    >
      <div className="temporal-create-activity-tree__spine" aria-hidden="true" />

      {structure.plannedSlices.length > 0 ? (
        <div className="temporal-create-activity-tree__root-sessions">
          <div className="temporal-create-activity-tree__group-label">
            {italian ? 'Sessioni attività' : 'Activity sessions'}
          </div>
          {structure.plannedSlices.map((slice) =>
            renderPlannedSlice(slice, null, 'root'),
          )}
        </div>
      ) : null}

      <div className="temporal-create-activity-tree__children">
        {structure.children.map((child, index) => {
          const childTimeId = `child:${child.id}`;
          const childTimeOpen = openTimes.includes(childTimeId);
          return (
            <div
              className="temporal-create-tree-item is-child"
              key={child.id}
              data-create-subactivity
            >
              <div className="temporal-create-tree-row is-child-row">
                <span
                  className="temporal-create-tree-row__icon is-child"
                  aria-hidden="true"
                >
                  ◇
                </span>
                <span
                  className="temporal-create-tree-row__divider"
                  aria-hidden="true"
                />
                <input
                  className="temporal-create-tree-row__title"
                  type="text"
                  value={child.title}
                  required
                  maxLength={300}
                  placeholder={
                    italian ? 'Titolo sotto-attività' : 'Sub-activity title'
                  }
                  aria-label={
                    italian ? 'Titolo sotto-attività' : 'Sub-activity title'
                  }
                  onChange={(event) =>
                    updateChild(child.id, { title: event.currentTarget.value })
                  }
                />
                <div className="temporal-create-tree-row__actions">
                  <label
                    className="temporal-create-tree-session-toggle"
                    data-session-capability="sub-activity"
                  >
                    <input
                      type="checkbox"
                      checked={child.captureMode !== 'disabled'}
                      onChange={(event) =>
                        updateChild(child.id, {
                          captureMode: event.currentTarget.checked
                            ? 'live'
                            : 'disabled',
                        })
                      }
                    />
                    {italian ? 'Sessione' : 'Session'}
                  </label>
                  <button
                    type="button"
                    className={child.scheduleEnabled ? 'is-active' : undefined}
                    aria-expanded={childTimeOpen}
                    onClick={() => {
                      if (!child.scheduleEnabled) {
                        updateChild(child.id, { scheduleEnabled: true });
                      }
                      toggleTime(childTimeId);
                    }}
                  >
                    {italian ? 'Orario' : 'Time'}
                  </button>
                  <select
                    value={child.requirementCode}
                    aria-label={
                      italian
                        ? 'Requisito sotto-attività'
                        : 'Sub-activity requirement'
                    }
                    onChange={(event) =>
                      updateChild(child.id, {
                        requirementCode: event.currentTarget.value as
                          | 'required'
                          | 'optional',
                      })
                    }
                  >
                    <option value="required">
                      {italian ? 'Richiesta' : 'Required'}
                    </option>
                    <option value="optional">
                      {italian ? 'Facoltativa' : 'Optional'}
                    </option>
                  </select>
                  <button
                    type="button"
                    disabled={index === 0}
                    aria-label={italian ? 'Sposta su' : 'Move up'}
                    onClick={() => {
                      const list = [...structure.children];
                      [list[index - 1], list[index]] = [
                        list[index]!,
                        list[index - 1]!,
                      ];
                      patchStructure({ children: list });
                    }}
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    disabled={index === structure.children.length - 1}
                    aria-label={italian ? 'Sposta giù' : 'Move down'}
                    onClick={() => {
                      const list = [...structure.children];
                      [list[index], list[index + 1]] = [
                        list[index + 1]!,
                        list[index]!,
                      ];
                      patchStructure({ children: list });
                    }}
                  >
                    ↓
                  </button>
                  <button
                    type="button"
                    className="is-remove"
                    aria-label={
                      italian ? 'Rimuovi sotto-attività' : 'Remove sub-activity'
                    }
                    onClick={() =>
                      patchStructure({
                        children: structure.children.filter(
                          (entry) => entry.id !== child.id,
                        ),
                      })
                    }
                  >
                    ×
                  </button>
                </div>
              </div>

              {childTimeOpen && child.scheduleEnabled ? (
                <div
                  className="temporal-create-tree-time-editor is-child-time"
                  data-create-subactivity-time
                >
                  <label>
                    <span>{italian ? 'Dal' : 'From'}</span>
                    <input
                      type="date"
                      value={child.startDate}
                      onChange={(event) =>
                        updateChild(child.id, {
                          startDate: event.currentTarget.value,
                        })
                      }
                    />
                  </label>
                  <label>
                    <span>{italian ? 'Inizio' : 'Start'}</span>
                    <input
                      type="time"
                      value={child.startTime}
                      onChange={(event) =>
                        updateChild(child.id, {
                          startTime: event.currentTarget.value,
                        })
                      }
                    />
                  </label>
                  <label>
                    <span>{italian ? 'Al' : 'To'}</span>
                    <input
                      type="date"
                      value={child.endDate}
                      onChange={(event) =>
                        updateChild(child.id, {
                          endDate: event.currentTarget.value,
                        })
                      }
                    />
                  </label>
                  <label>
                    <span>{italian ? 'Fine' : 'End'}</span>
                    <input
                      type="time"
                      value={child.endTime}
                      onChange={(event) =>
                        updateChild(child.id, {
                          endTime: event.currentTarget.value,
                        })
                      }
                    />
                  </label>
                  <button
                    type="button"
                    className="temporal-create-tree-time-editor__clear"
                    onClick={() => {
                      updateChild(child.id, { scheduleEnabled: false });
                      setOpenTimes((current) =>
                        current.filter((entry) => entry !== childTimeId),
                      );
                    }}
                  >
                    {italian ? 'Rimuovi orario' : 'Remove time'}
                  </button>
                </div>
              ) : null}

              <div className="temporal-create-activity-tree__child-body">
                {child.plannedSlices.map((slice) =>
                  renderPlannedSlice(slice, child.id, 'child'),
                )}
                <button
                  className="temporal-create-tree-add is-child-add"
                  type="button"
                  onClick={() =>
                    updateChild(child.id, {
                      plannedSlices: [
                        ...child.plannedSlices,
                        plannedSlice(fields, child),
                      ],
                    })
                  }
                >
                  <span aria-hidden="true">＋</span>
                  {italian ? 'Sessione' : 'Session'}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      <div
        className="temporal-create-activity-tree__root-actions"
        aria-label={italian ? 'Aggiungi alla struttura' : 'Add to structure'}
      >
        <button
          className="temporal-create-tree-add"
          type="button"
          onClick={addRootSession}
        >
          <span aria-hidden="true">＋</span>
          {italian ? 'Sessione' : 'Session'}
        </button>
        <button
          className="temporal-create-tree-add"
          type="button"
          onClick={addChild}
        >
          <span aria-hidden="true">＋</span>
          {italian ? 'Sotto-attività' : 'Sub-activity'}
        </button>
      </div>
    </section>
  );
}
