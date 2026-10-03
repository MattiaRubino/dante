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

function beginsLater(fields: TemporalCreateFields): boolean {
  try {
    const now = Temporal.Now.zonedDateTimeISO(fields.timeZoneId);
    if (fields.timeSemantics === 'timed') {
      const start = Temporal.PlainDateTime.from(
        `${fields.date}T${fields.startTime}`,
      );
      return Temporal.PlainDateTime.compare(start, now.toPlainDateTime()) > 0;
    }
    return (
      Temporal.PlainDate.compare(
        Temporal.PlainDate.from(fields.date),
        now.toPlainDate(),
      ) > 0
    );
  } catch {
    return fields.date > Temporal.Now.plainDateISO().toString();
  }
}

function plannedSlice(
  fields: TemporalCreateFields,
): TemporalCreatePlannedSliceDraft {
  return Object.freeze({
    id: newRowId(),
    title: '',
    date: fields.date,
    startTime: fields.startTime,
    endTime: '',
  });
}

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
    >
      <input
        type="checkbox"
        checked={enabled}
        onChange={(event) =>
          patch({
            activityStructure: Object.freeze({
              ...structure,
              captureMode: event.currentTarget.checked
                ? 'record_and_live'
                : 'disabled',
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
  const [open, setOpen] = useState(false);
  const { draft, patch } = useTemporalCreateU2Draft();
  const structure = draft.activityStructure;
  const startsLater = beginsLater(fields);

  const addSessionConfiguration = () => {
    if (startsLater) {
      patchStructure({
        captureMode:
          structure.captureMode === 'disabled'
            ? 'record_and_live'
            : structure.captureMode,
        plannedSlices: [...structure.plannedSlices, plannedSlice(fields)],
      });
    } else {
      patchStructure({ captureMode: 'record_and_live' });
    }
    setOpen(false);
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
        <input
          type="text"
          value={slice.title}
          maxLength={300}
          placeholder={italian ? 'Nome Sessione' : 'Session name'}
          aria-label={italian ? 'Nome Sessione' : 'Session name'}
          onChange={(event) =>
            updateSlice(owner, slice.id, { title: event.currentTarget.value })
          }
        />
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
                  onClick={addSessionConfiguration}
                >
                  {italian ? 'Sessione' : 'Session'}
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
                <label className="temporal-create-structure-session-toggle">
                  <input
                    type="checkbox"
                    checked={child.captureMode !== 'disabled'}
                    onChange={(event) =>
                      updateChild(child.id, {
                        captureMode: event.currentTarget.checked
                          ? 'record_and_live'
                          : 'disabled',
                      })
                    }
                  />
                  {italian ? 'Sessione' : 'Session'}
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
            {startsLater ? (
              <button
                className="temporal-create-structure-add-slice"
                type="button"
                onClick={() =>
                  updateChild(child.id, {
                    captureMode:
                      child.captureMode === 'disabled'
                        ? 'record_and_live'
                        : child.captureMode,
                    plannedSlices: [
                      ...child.plannedSlices,
                      plannedSlice(fields),
                    ],
                  })
                }
              >
                + {italian ? 'Sessione' : 'Session'}
              </button>
            ) : null}
            {child.plannedSlices.map((slice) =>
              renderPlannedSlice(slice, child.id),
            )}
          </div>
        ))}

        {structure.plannedSlices.map((slice) =>
          renderPlannedSlice(slice, null),
        )}
      </div>
    </div>
  );
}
