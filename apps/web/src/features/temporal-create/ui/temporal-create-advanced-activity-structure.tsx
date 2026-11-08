import { useTranslation } from 'react-i18next';
import { Temporal } from '@dante/time';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreatePlannedSliceDraft } from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';
import { TemporalCreatePlacementLockButton } from './temporal-create-placement-lock-button';

import './temporal-create-advanced-activity-structure.css';
import './temporal-create-outcome-dropdown.css';
import './temporal-create-product-freeze.css';
import './temporal-create-session-time-polish.css';

type TemporalCreateAdvancedActivityStructureProps = Readonly<{
  fields: TemporalCreateFields;
  validationTarget?: string | null;
  validationMessage?: string;
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

export function plannedSlice(
  fields: TemporalCreateFields,
): TemporalCreatePlannedSliceDraft {
  const root = rootInterval(fields);
  return Object.freeze({
    id: newRowId(),
    title: '',
    timeEnabled: false,
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

  return (
    <>
      <TemporalCreatePlacementLockButton
        kind="activity"
        italian={italian}
        locked={structure.placementProtected}
        onToggle={() =>
          patchStructure({ placementProtected: !structure.placementProtected })
        }
      />
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
  validationTarget = null,
  validationMessage = '',
}: TemporalCreateAdvancedActivityStructureProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const structure = draft.activityStructure;

  const patchStructure = (changes: Partial<typeof structure>) =>
    patch({ activityStructure: Object.freeze({ ...structure, ...changes }) });

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
      data-create-path="activityStructure"
      aria-label={italian ? 'Sessioni attività' : 'Activity sessions'}
    >
      <div
        className="temporal-create-activity-tree__spine"
        aria-hidden="true"
      />

      {structure.plannedSlices.length > 0 ? (
        <div
          className="temporal-create-activity-tree__root-sessions"
          data-create-path="plannedSessions"
        >
          <div className="temporal-create-activity-tree__group-label temporal-editor-section-heading">
            {italian ? 'Sessioni attività' : 'Activity sessions'}
          </div>
          {structure.plannedSlices.map((slice) => {
            const invalid = validationTarget === `plannedSession:${slice.id}`;
            return (
              <div
                className="temporal-create-tree-item is-session is-root"
                key={slice.id}
                data-create-planned-session
                data-create-path={`plannedSession:${slice.id}`}
                data-create-owner="root"
              >
                <div
                  className="temporal-create-tree-row"
                  data-create-invalid={invalid ? 'true' : undefined}
                >
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
                    aria-invalid={invalid || undefined}
                    aria-describedby={
                      invalid ? `planned-session-error-${slice.id}` : undefined
                    }
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
                {invalid && validationMessage ? (
                  <span
                    id={`planned-session-error-${slice.id}`}
                    className="temporal-create-field-error temporal-create-tree-error"
                    role="alert"
                  >
                    {validationMessage}
                  </span>
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
