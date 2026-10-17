import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateObjectiveComparator,
  TemporalCreateObjectiveDraft,
  TemporalCreateObjectiveKind,
} from '../model/temporal-create-u2-authoring';

import './temporal-create-objectives.css';

/** Shared visual row; the Create/Edit owner keeps its own persistence rules. */
export function TemporalObjectiveEditorRow({
  objective,
  index,
  total,
  variant = 'create',
  disabled = false,
  onInspect,
  update,
  changeKind,
  move,
  remove,
  extras,
}: Readonly<{
  objective: TemporalCreateObjectiveDraft;
  index: number;
  total: number;
  variant?: 'create' | 'edit';
  disabled?: boolean;
  onInspect?: () => void;
  update: (id: string, patch: Partial<TemporalCreateObjectiveDraft>) => void;
  changeKind: (id: string, kind: TemporalCreateObjectiveKind) => void;
  move: (index: number, direction: -1 | 1) => void;
  remove: (id: string) => void;
  extras?: ReactNode;
}>) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  return (
    <div
      className="temporal-create-objective"
      data-create-objective
      data-objective-id={objective.id}
      onFocusCapture={onInspect}
    >
      <div className="temporal-create-objective__row">
        <span
          className="temporal-create-objective__index"
          aria-hidden="true"
        >
          {index + 1}
        </span>
        <span
          className="temporal-create-objective__divider"
          aria-hidden="true"
        />
        <input
          className="temporal-create-objective__title"
          disabled={disabled}
          type="text"
          maxLength={300}
          value={objective.label}
          aria-label={
            italian
              ? variant === 'edit'
                ? 'Nome obiettivo'
                : `Obiettivo ${index + 1}`
              : `Objective ${index + 1}`
          }
          placeholder={
            italian
              ? 'Cosa vuoi ottenere o verificare?'
              : 'What do you want to achieve or verify?'
          }
          onChange={(event) =>
            update(objective.id, { label: event.currentTarget.value })
          }
        />
        <div className="temporal-create-objective__actions">
          <button
            type="button"
            disabled={disabled || index === 0}
            aria-label={
              italian ? 'Sposta obiettivo su' : 'Move objective up'
            }
            onClick={() => move(index, -1)}
          >
            ↑
          </button>
          <button
            type="button"
            disabled={disabled || index === total - 1}
            aria-label={
              italian ? 'Sposta obiettivo giù' : 'Move objective down'
            }
            onClick={() => move(index, 1)}
          >
            ↓
          </button>
          <button
            type="button"
            className="is-remove"
            aria-label={
              italian ? variant === 'edit'
                  ? `Rimuovi obiettivo ${objective.label.trim() || 'Nuovo obiettivo'}`
                  : 'Rimuovi obiettivo'
                : 'Remove objective'
            }
            onClick={() => remove(objective.id)}
            disabled={disabled}
          >
            ×
          </button>
        </div>
      </div>

      <div className="temporal-create-objective__definition">
        <label>
          <span>{italian ? 'Risultato' : 'Result'}</span>
          <select
            value={objective.resultKind}
            disabled={disabled}
            aria-label={
              italian
                ? variant === 'edit'
                      ? 'Tipo obiettivo'
                      : `Tipo risultato obiettivo ${index + 1}`
                : `Objective ${index + 1} result type`
            }
            onChange={(event) =>
              changeKind(
                objective.id,
                event.currentTarget
                  .value as TemporalCreateObjectiveKind,
              )
            }
          >
            <option value="boolean">
              {italian ? 'Sì / No' : 'Yes / No'}
            </option>
            <option value="quantity">
              {italian ? 'Quantità' : 'Quantity'}
            </option>
            <option value="qualitative">
              {italian ? 'Valutazione' : 'Assessment'}
            </option>
            <option value="range">
              {italian ? 'Intervallo' : 'Range'}
            </option>
          </select>
        </label>

        {objective.resultKind === 'quantity' ? (
          <>
            <label>
              <span>{italian ? 'Regola' : 'Rule'}</span>
              <select
                value={objective.comparatorCode ?? 'gte'}
                disabled={disabled}
                aria-label={
                  italian
                    ? 'Confronto obiettivo'
                    : 'Objective comparator'
                }
                onChange={(event) =>
                  update(objective.id, {
                    comparatorCode: event.currentTarget
                      .value as TemporalCreateObjectiveComparator,
                  })
                }
              >
                <option value="gte">≥</option>
                <option value="lte">≤</option>
                <option value="eq">=</option>
              </select>
            </label>
            <label>
              <span>{italian ? 'Target' : 'Target'}</span>
              <input
                type="number"
                step="any"
                value={objective.targetValue}
                disabled={disabled}
                aria-label={
                  italian ? variant === 'edit'
                              ? 'Valore obiettivo'
                              : 'Target obiettivo'
                            : 'Objective target'
                }
                onChange={(event) =>
                  update(objective.id, {
                    targetValue: event.currentTarget.value,
                  })
                }
              />
            </label>
            <label>
              <span>{italian ? 'Unità' : 'Unit'}</span>
              <input
                type="text"
                maxLength={40}
                value={objective.unitCode}
                disabled={disabled}
                aria-label={
                  italian ? variant === 'edit'
                              ? 'Unità di misura'
                              : 'Unità obiettivo'
                            : 'Objective unit'
                }
                placeholder="km, kg, €, mele…"
                onChange={(event) =>
                  update(objective.id, {
                    unitCode: event.currentTarget.value,
                  })
                }
              />
            </label>
          </>
        ) : null}

        {objective.resultKind === 'range' ? (
          <>
            <label>
              <span>{italian ? 'Min' : 'Min'}</span>
              <input
                type="number"
                step="any"
                value={objective.targetMin}
                disabled={disabled}
                aria-label={
                  italian ? 'Minimo obiettivo' : 'Objective minimum'
                }
                onChange={(event) =>
                  update(objective.id, {
                    targetMin: event.currentTarget.value,
                  })
                }
              />
            </label>
            <label>
              <span>{italian ? 'Max' : 'Max'}</span>
              <input
                type="number"
                step="any"
                value={objective.targetMax}
                disabled={disabled}
                aria-label={
                  italian ? 'Massimo obiettivo' : 'Objective maximum'
                }
                onChange={(event) =>
                  update(objective.id, {
                    targetMax: event.currentTarget.value,
                  })
                }
              />
            </label>
            <label>
              <span>{italian ? 'Unità' : 'Unit'}</span>
              <input
                type="text"
                maxLength={40}
                value={objective.unitCode}
                disabled={disabled}
                aria-label={
                  italian ? variant === 'edit'
                              ? 'Unità di misura'
                              : 'Unità obiettivo'
                            : 'Objective unit'
                }
                placeholder="kg, bpm, €…"
                onChange={(event) =>
                  update(objective.id, {
                    unitCode: event.currentTarget.value,
                  })
                }
              />
            </label>
          </>
        ) : null}

        {objective.resultKind === 'boolean' ? (
          <span className="temporal-create-objective__hint">
            {italian
              ? 'Alla verifica registrerai Sì oppure No.'
              : 'At review you will record Yes or No.'}
          </span>
        ) : null}

        {objective.resultKind === 'qualitative' ? (
          <span className="temporal-create-objective__hint">
            {italian
              ? 'Alla verifica: raggiunto, parziale, non raggiunto o non valutabile.'
              : 'At review: reached, partial, not reached or indeterminate.'}
          </span>
        ) : null}
      </div>
      {extras ? (
    <div className="temporal-create-objective__extras">{extras}</div>
  ) : null}
    </div>
  );
}
