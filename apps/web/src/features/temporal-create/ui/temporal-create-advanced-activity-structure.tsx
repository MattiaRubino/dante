import { useState, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type {
  TemporalCreateActivityChildDraft,
  TemporalCreatePlannedSliceDraft,
} from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

import './temporal-create-advanced-activity-structure.css';

type TemporalCreateAdvancedActivityStructureProps = Readonly<{
  fields: TemporalCreateFields;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

let nextStructureRowId = 0;
const newRowId = () => `structure-${++nextStructureRowId}`;

function plannedSlice(
  fields: TemporalCreateFields,
): TemporalCreatePlannedSliceDraft {
  return Object.freeze({
    id: newRowId(),
    date: fields.date,
    startTime: fields.startTime,
    endTime: '',
  });
}

export function TemporalCreateAdvancedActivityStructure({
  fields,
  onPatch,
  renderError,
}: TemporalCreateAdvancedActivityStructureProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const [open, setOpen] = useState(false);
  const { draft, patch } = useTemporalCreateU2Draft();
  const structure = draft.activityStructure;
  const execution = fields.execution;
  const sessionConfigured = execution.sessionMode === 'splittable';

  const patchExecution = (patch: Partial<TemporalCreateFields['execution']>) =>
    onPatch({ execution: { ...execution, ...patch } });

  const addSessionConfiguration = () => {
    patchExecution({ sessionMode: 'splittable' });
    setOpen(false);
  };

  const removeSessionConfiguration = () => {
    patchExecution({ sessionMode: 'indivisible' });
  };

  const patchStructure = (changes: Partial<typeof structure>) =>
    patch({ activityStructure: Object.freeze({ ...structure, ...changes }) });

  const addChild = () => {
    patchStructure({
      children: [
        ...structure.children,
        Object.freeze({
          id: newRowId(),
          title: '',
          requirementCode: 'required' as const,
          captureMode: 'disabled' as const,
          plannedSlices: Object.freeze([]),
        }),
      ],
    });
    setOpen(false);
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
    if (child)
      updateChild(owner, {
        plannedSlices: child.plannedSlices.map((slice) =>
          slice.id === id ? Object.freeze({ ...slice, ...changes }) : slice,
        ),
      });
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
    if (child)
      updateChild(owner, {
        plannedSlices: child.plannedSlices.filter((slice) => slice.id !== id),
      });
  };

  const renderPlannedSlice = (
    slice: TemporalCreatePlannedSliceDraft,
    owner: string | null,
  ) => (
    <div
      className="temporal-create-structure-node is-planned"
      key={slice.id}
      data-create-planned-session
      data-create-owner={owner ?? 'root'}
    >
      <div className="temporal-create-structure-node__identity">
        <span
          className="temporal-create-structure-node__elbow"
          aria-hidden="true"
        />
        <strong>{italian ? 'Sessione pianificata' : 'Planned session'}</strong>
      </div>
      <div className="temporal-create-structure-node__actions is-planned-controls">
        <label>
          {italian ? 'Data' : 'Date'}
          <input
            type="date"
            value={slice.date}
            onChange={(event) =>
              updateSlice(owner, slice.id, { date: event.currentTarget.value })
            }
          />
        </label>
        <label>
          {italian ? 'Inizio' : 'Start'}
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
          {italian ? 'Fine' : 'End'}
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
        <button
          type="button"
          className="is-remove"
          onClick={() => removeSlice(owner, slice.id)}
          aria-label={
            italian ? 'Rimuovi Sessione pianificata' : 'Remove planned session'
          }
        >
          ×
        </button>
      </div>
    </div>
  );

  return (
    <div
      className="temporal-create-advanced-structure-inline"
      data-create-activity-structure
    >
      <div className="temporal-create-advanced-structure-inline__tree">
        <div className="temporal-create-advanced-structure-inline__branch">
          <span
            className="temporal-create-advanced-structure-inline__connector"
            aria-hidden="true"
          />
          <div className="temporal-create-advanced-structure-inline__add">
            <button
              type="button"
              aria-label={
                italian ? 'Aggiungi alla struttura' : 'Add to structure'
              }
              aria-expanded={open}
              onClick={() => setOpen((current) => !current)}
            >
              <span aria-hidden="true">+</span>
              {italian ? 'Aggiungi' : 'Add'}
            </button>

            {open ? (
              <div
                className="temporal-create-structure-menu"
                role="menu"
                aria-label={
                  italian ? 'Aggiungi alla struttura' : 'Add to structure'
                }
              >
                <button type="button" role="menuitem" onClick={addChild}>
                  {italian ? 'Sotto-attività' : 'Sub-activity'}
                </button>
                <button
                  type="button"
                  role="menuitem"
                  disabled={sessionConfigured}
                  onClick={addSessionConfiguration}
                >
                  {italian ? 'Sessione' : 'Session'}
                </button>
                <button
                  type="button"
                  role="menuitem"
                  onClick={() => {
                    patchStructure({
                      plannedSlices: [
                        ...structure.plannedSlices,
                        plannedSlice(fields),
                      ],
                    });
                    setOpen(false);
                  }}
                >
                  {italian ? 'Sessione pianificata' : 'Planned session'}
                </button>
              </div>
            ) : null}
          </div>
        </div>

        {structure.children.map((child, index) => (
          <div key={child.id} data-create-subactivity>
            <div className="temporal-create-structure-node is-child">
              <div className="temporal-create-structure-node__identity">
                <span
                  className="temporal-create-structure-node__elbow"
                  aria-hidden="true"
                />
                <input
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
              </div>
              <div className="temporal-create-structure-node__actions">
                <label>
                  {italian ? 'Requisito' : 'Requirement'}
                  <select
                    value={child.requirementCode}
                    onChange={(event) =>
                      updateChild(child.id, {
                        requirementCode: event.currentTarget.value as
                          'required' | 'optional',
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
                </label>
                <label>
                  {italian ? 'Sessioni' : 'Sessions'}
                  <select
                    value={child.captureMode}
                    onChange={(event) =>
                      updateChild(child.id, {
                        captureMode: event.currentTarget
                          .value as TemporalCreateActivityChildDraft['captureMode'],
                      })
                    }
                  >
                    <option value="disabled">
                      {italian ? 'Disabilitate' : 'Disabled'}
                    </option>
                    <option value="record">
                      {italian ? 'Registra' : 'Record'}
                    </option>
                    <option value="live">Live</option>
                    <option value="record_and_live">
                      {italian ? 'Registra e live' : 'Record and live'}
                    </option>
                  </select>
                </label>
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
            <button
              className="temporal-create-structure-add-slice"
              type="button"
              onClick={() =>
                updateChild(child.id, {
                  plannedSlices: [...child.plannedSlices, plannedSlice(fields)],
                })
              }
            >
              + {italian ? 'Sessione pianificata' : 'Planned session'}
            </button>
            {child.plannedSlices.map((slice) =>
              renderPlannedSlice(slice, child.id),
            )}
          </div>
        ))}

        {structure.plannedSlices.map((slice) =>
          renderPlannedSlice(slice, null),
        )}

        {sessionConfigured ? (
          <div
            className="temporal-create-structure-node is-session"
            data-create-structure-session
          >
            <div className="temporal-create-structure-node__identity">
              <span
                className="temporal-create-structure-node__elbow"
                aria-hidden="true"
              />
              <div>
                <strong>{italian ? 'Sessione' : 'Session'}</strong>
                <small>
                  {italian
                    ? 'Configura come potrà essere eseguita l’Activity.'
                    : 'Configure how the Activity may be executed.'}
                </small>
              </div>
            </div>

            <div
              className="temporal-create-structure-node__actions"
              data-create-structure-session-options
              aria-label={
                italian ? 'Impostazioni Sessione' : 'Session settings'
              }
            >
              <label className="temporal-create-structure-node__minimum">
                <span>{italian ? 'Minimo' : 'Minimum'}</span>
                <input
                  data-create-path="execution.minSessionMinutes"
                  type="number"
                  min="1"
                  step="1"
                  value={execution.minSessionMinutes}
                  onChange={(event) =>
                    patchExecution({
                      minSessionMinutes: Number(event.currentTarget.value),
                    })
                  }
                />
                <span>min</span>
              </label>
              {renderError('execution.minSessionMinutes')}
              <button
                className="is-remove"
                type="button"
                aria-label={
                  italian
                    ? 'Disabilita configurazione Sessione'
                    : 'Disable Session configuration'
                }
                title={
                  italian
                    ? 'Rimuovi la configurazione Sessione da questa Activity.'
                    : 'Remove Session configuration from this Activity.'
                }
                onClick={removeSessionConfiguration}
              >
                ×
              </button>
            </div>
          </div>
        ) : null}
      </div>

      <div
        className="temporal-create-advanced-structure-inline__actions"
        data-create-structure-actions
        aria-label={italian ? 'Impostazioni attività' : 'Activity settings'}
      >
        <label>
          {italian ? 'Sessioni' : 'Sessions'}
          <select
            value={structure.captureMode}
            onChange={(event) =>
              patchStructure({
                captureMode: event.currentTarget
                  .value as typeof structure.captureMode,
              })
            }
          >
            <option value="disabled">
              {italian ? 'Disabilitate' : 'Disabled'}
            </option>
            <option value="record">{italian ? 'Registra' : 'Record'}</option>
            <option value="live">Live</option>
            <option value="record_and_live">
              {italian ? 'Registra e live' : 'Record and live'}
            </option>
          </select>
        </label>
        <label>
          {italian ? 'Figli richiesti' : 'Required children'}
          <select
            value={structure.childGuardMode}
            onChange={(event) =>
              patchStructure({
                childGuardMode: event.currentTarget
                  .value as typeof structure.childGuardMode,
              })
            }
          >
            <option value="none">
              {italian ? 'Nessun vincolo' : 'No guard'}
            </option>
            <option value="confirm">{italian ? 'Conferma' : 'Confirm'}</option>
            <option value="block">{italian ? 'Blocca' : 'Block'}</option>
          </select>
        </label>
      </div>
    </div>
  );
}
