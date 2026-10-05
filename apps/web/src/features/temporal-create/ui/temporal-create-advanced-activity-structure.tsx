import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Temporal } from '@dante/time';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreatePlannedSliceDraft } from '../model/temporal-create-u2-authoring';
import { TemporalCreateDatePicker } from './temporal-create-date-picker';
import { TimeControl } from './temporal-create-core-u2';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

import './temporal-create-advanced-activity-structure.css';
import './temporal-create-product-freeze.css';

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

export function plannedSlice(fields: TemporalCreateFields): TemporalCreatePlannedSliceDraft {
  const root = rootInterval(fields);
  return Object.freeze({
    id: newRowId(),
    title: '',
    date: root.startDate,
    startTime: root.startTime,
    endTime: root.endTime,
  });
}

/**
 * Root Activity product capabilities. Session enables truthful B08 live
 * execution after creation. Placement protection maps to the canonical B04
 * Movement Policy (`blocked + direct`) and never constrains real execution.
 */
export function TemporalCreateAdvancedActivityHeaderActions() {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const structure = draft.activityStructure;
  const enabled = structure.captureMode !== 'disabled';

  const patchStructure = (changes: Partial<typeof structure>) =>
    patch({ activityStructure: Object.freeze({ ...structure, ...changes }) });

  const placementActionLabel = italian
    ? structure.placementProtected
      ? 'Sblocca spostamenti'
      : 'Blocca spostamenti'
    : structure.placementProtected
      ? 'Unlock placement'
      : 'Lock placement';

  const placementActionTitle = italian
    ? structure.placementProtected
      ? 'Consenti di nuovo gli spostamenti manuali e automatici della collocazione'
      : 'Blocca gli spostamenti manuali e automatici della collocazione'
    : structure.placementProtected
      ? 'Allow manual and automatic placement changes again'
      : 'Block manual and automatic placement changes';

  return (
    <>
      <label
        className="temporal-create-structure-session-toggle"
        data-create-structure-actions
        data-session-capability="activity"
      >
        <input
          type="checkbox"
          checked={enabled}
          onChange={(event) =>
            patchStructure({
              captureMode: event.currentTarget.checked ? 'live' : 'disabled',
            })
          }
        />
        {italian ? 'Sessione' : 'Session'}
      </label>
      <button
        type="button"
        className="temporal-create-placement-lock"
        data-placement-protection="activity"
        aria-pressed={structure.placementProtected}
        aria-label={placementActionLabel}
        title={placementActionTitle}
        onClick={() =>
          patchStructure({ placementProtected: !structure.placementProtected })
        }
      >
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <rect x="5" y="10" width="14" height="11" rx="2" />
          {structure.placementProtected ? (
            <path d="M8 10V7a4 4 0 0 1 8 0v3" />
          ) : (
            <path d="M8 10V7a4 4 0 0 1 7.5-1.9" />
          )}
        </svg>
        <span>{placementActionLabel}</span>
      </button>
    </>
  );
}

/**
 * Product v1 intentionally exposes one Activity with zero or more planned
 * execution slices. Activity decomposition remains a canonical kernel
 * capability, but Sub-Activities are not authored from Create while the
 * product model is being consolidated.
 */
export function TemporalCreateAdvancedActivityStructure({
  fields,
}: TemporalCreateAdvancedActivityStructureProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const locale = i18n.resolvedLanguage ?? i18n.language ?? 'it';
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

  const updateSlice = (
    id: string,
    changes: Partial<TemporalCreatePlannedSliceDraft>,
  ) =>
    patchStructure({
      plannedSlices: structure.plannedSlices.map((slice) =>
        slice.id === id ? Object.freeze({ ...slice, ...changes }) : slice,
      ),
    });

  const removeSlice = (id: string) => {
    patchStructure({
      plannedSlices: structure.plannedSlices.filter((slice) => slice.id !== id),
    });
  };

  return (
    <section
      className="temporal-create-activity-tree"
      data-create-activity-structure
      aria-label={italian ? 'Sessioni pianificate' : 'Planned Sessions'}
    >
      <div className="temporal-create-activity-tree__spine" aria-hidden="true" />

      {structure.plannedSlices.length > 0 ? (
        <div className="temporal-create-activity-tree__root-sessions">
          <div className="temporal-create-activity-tree__group-label">
            {italian ? 'Sessioni attività' : 'Activity sessions'}
          </div>
          {structure.plannedSlices.map((slice) => {
            const timeId = `session:${slice.id}`;
            const timeOpen = openTimes.includes(timeId);
            return (
              <div
                className="temporal-create-tree-item is-session is-root"
                key={slice.id}
                data-create-planned-session
                data-create-owner="root"
              >
                <div className="temporal-create-tree-row">
                  <span
                    className="temporal-create-tree-row__icon"
                    aria-hidden="true"
                  >
                    ▶
                  </span>
                  <span
                    className="temporal-create-tree-row__divider"
                    aria-hidden="true"
                  />
                  <input
                    className="temporal-create-tree-row__title"
                    type="text"
                    value={slice.title}
                    maxLength={300}
                    placeholder={italian ? 'Nome Sessione' : 'Session name'}
                    aria-label={italian ? 'Nome Sessione' : 'Session name'}
                    onChange={(event) =>
                      updateSlice(slice.id, {
                        title: event.currentTarget.value,
                      })
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
                      onClick={() => removeSlice(slice.id)}
                      aria-label={
                        italian ? 'Rimuovi Sessione' : 'Remove Session'
                      }
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
                    <TemporalCreateDatePicker
                      label={italian ? 'Data Sessione' : 'Session date'}
                      value={slice.date}
                      locale={locale}
                      onChange={(date) => updateSlice(slice.id, { date })}
                    />
                    <TimeControl
                      label={italian ? 'Inizio Sessione' : 'Session start'}
                      value={slice.startTime}
                      dataPath={`plannedSlices.${slice.id}.startTime`}
                      onChange={(startTime) => updateSlice(slice.id, { startTime })}
                    />
                    <TimeControl
                      label={italian ? 'Fine Sessione' : 'Session end'}
                      value={slice.endTime}
                      dataPath={`plannedSlices.${slice.id}.endTime`}
                      onChange={(endTime) => updateSlice(slice.id, { endTime })}
                    />
                  </div>
                ) : null}
              </div>
            );
          })}
        </div>
      ) : null}

      <div
        className="temporal-create-activity-tree__root-actions"
        aria-label={
          italian ? 'Aggiungi Sessione pianificata' : 'Add planned Session'
        }
      >
        <button
          className="temporal-create-tree-add"
          type="button"
          onClick={addRootSession}
        >
          <span aria-hidden="true">＋</span>
          {italian ? 'Sessione' : 'Session'}
        </button>
      </div>
    </section>
  );
}
