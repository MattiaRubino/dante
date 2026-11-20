import { useId, useState, type ReactNode } from 'react';

import type {
  TemporalCreateObjectiveComparator,
  TemporalCreateObjectiveDraft,
  TemporalCreateObjectiveKind,
} from '../model/temporal-create-u2-authoring';
import type { ObjectiveFieldIssue, ObjectiveInvalidField } from '../model/temporal-objective-validation';

import './temporal-create-objectives.css';

/** Shared visual row; the Create/Edit owner keeps its own persistence rules. */
export function TemporalObjectiveEditorRow({
  objective,
  index,
  total,
  variant = 'create',
  italian,
  disabled = false,
  onInspect,
  update,
  changeKind,
  move,
  remove,
  extras,
  issue,
  issues,
}: Readonly<{
  objective: TemporalCreateObjectiveDraft;
  index: number;
  total: number;
  variant?: 'create' | 'edit';
  italian: boolean;
  disabled?: boolean;
  onInspect?: () => void;
  update: (id: string, patch: Partial<TemporalCreateObjectiveDraft>) => void;
  changeKind: (id: string, kind: TemporalCreateObjectiveKind) => void;
  move: (index: number, direction: -1 | 1) => void;
  remove: (id: string) => void;
  extras?: ReactNode;
  issue?: ObjectiveFieldIssue | null | undefined;
  issues?: readonly ObjectiveFieldIssue[] | undefined;
}>) {
  const errorId = useId();
  const [badNumericInput, setBadNumericInput] =
    useState<ReadonlySet<ObjectiveInvalidField>>(new Set());
  const activeIssues = issues ?? (issue ? [issue] : []);
  const fieldIssue = (field: ObjectiveInvalidField) => {
    const current = activeIssues.find((candidate) => candidate.field === field);
    return current && badNumericInput.has(field)
      ? { field, message: italian ? 'Solo numeri.' : 'Numbers only.' }
      : current;
  };
  const invalid = (field: ObjectiveInvalidField) =>
    fieldIssue(field) !== undefined;
  const idFor = (field: ObjectiveInvalidField) => `${errorId}-${field}`;
  const fieldMessage = (field: ObjectiveInvalidField) => {
    const message = fieldIssue(field)?.message;
    return message ? (
      <small
        id={idFor(field)}
        className="temporal-create-field-error"
        role="alert"
      >
        {message}
      </small>
    ) : null;
  };
  const fieldHeading = (field: ObjectiveInvalidField, name: string) => (
    <span className="temporal-create-objective__field-heading">
      <span>{name}</span>
      {fieldMessage(field)}
    </span>
  );
  const changeNumeric = (
    field: 'targetValue' | 'targetMin' | 'targetMax',
    value: string,
    badInput: boolean,
  ) => {
    setBadNumericInput((current) => {
      const next = new Set(current);
      if (badInput) next.add(field);
      else next.delete(field);
      return next;
    });
    update(objective.id, { [field]: value });
  };
  return (
    <div
      className={`temporal-create-objective${variant === 'edit' ? ' is-edit' : ''}`}
      data-create-objective
      data-objective-id={objective.id}
      data-objective-invalid={activeIssues.length ? 'true' : undefined}
      onFocusCapture={onInspect}
    >
      <div
        className="temporal-create-objective__row"
        data-field-invalid={invalid('label') || undefined}
      >
        <span className="temporal-create-objective__index" aria-hidden="true">
          {index + 1}
        </span>
        <span
          className="temporal-create-objective__divider"
          aria-hidden="true"
        />
        <span className="temporal-create-objective__title-cell">
          <input
            className="temporal-create-objective__title"
            disabled={disabled}
            type="text"
            maxLength={300}
            value={objective.label}
            aria-invalid={invalid('label') || undefined}
            aria-describedby={invalid('label') ? idFor('label') : undefined}
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
          {fieldMessage('label')}
        </span>
        <div className="temporal-create-objective__actions">
          <button
            type="button"
            disabled={disabled || index === 0}
            aria-label={italian ? 'Sposta obiettivo su' : 'Move objective up'}
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
              italian
                ? variant === 'edit'
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
      {activeIssues
        .filter((current) => fieldIssue(current.field)?.message === null)
        .map((current) => (
          <span
            key={current.field}
            id={idFor(current.field)}
            className="temporal-create-visually-hidden"
          >
            Campo obbligatorio.
          </span>
        ))}
      <div className="temporal-create-objective__details">
        <div
          className="temporal-create-objective__definition"
          data-result-kind={objective.resultKind}
        >
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
              onChange={(event) => {
                setBadNumericInput(new Set());
                changeKind(
                  objective.id,
                  event.currentTarget.value as TemporalCreateObjectiveKind,
                );
              }}
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
              <option value="range">{italian ? 'Intervallo' : 'Range'}</option>
            </select>
          </label>

          {objective.resultKind === 'quantity' ? (
            <>
              <label data-field-invalid={invalid('comparatorCode') || undefined}>
                {fieldHeading('comparatorCode', italian ? 'Regola' : 'Rule')}
                <select
                  value={objective.comparatorCode ?? 'gte'}
                  aria-invalid={invalid('comparatorCode') || undefined}
                  aria-describedby={invalid('comparatorCode') ? idFor('comparatorCode') : undefined}
                  disabled={disabled}
                  aria-label={
                    italian ? 'Confronto obiettivo' : 'Objective comparator'
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
              <label data-field-invalid={invalid('targetValue') || undefined}>
                {fieldHeading('targetValue', 'Target')}
                <input
                  type="number"
                  step="any"
                  value={objective.targetValue}
                  aria-invalid={invalid('targetValue') || undefined}
                  aria-describedby={invalid('targetValue') ? idFor('targetValue') : undefined}
                  disabled={disabled}
                  aria-label={
                    italian
                      ? variant === 'edit'
                        ? 'Valore obiettivo'
                        : 'Target obiettivo'
                      : 'Objective target'
                  }
                  onChange={(event) =>
                    changeNumeric(
                      'targetValue',
                      event.currentTarget.value,
                      event.currentTarget.validity.badInput,
                    )
                  }
                  onInput={(event) => {
                    if (event.currentTarget.validity.badInput)
                      changeNumeric('targetValue', '', true);
                  }}
                  onInvalid={(event) => event.preventDefault()}
                />
              </label>
              <label data-field-invalid={invalid('unitCode') || undefined}>
                {fieldHeading('unitCode', italian ? 'Unità' : 'Unit')}
                <input
                  type="text"
                  maxLength={40}
                  value={objective.unitCode}
                  aria-invalid={invalid('unitCode') || undefined}
                  aria-describedby={invalid('unitCode') ? idFor('unitCode') : undefined}
                  disabled={disabled}
                  aria-label={
                    italian
                      ? variant === 'edit'
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
              <label data-field-invalid={invalid('targetMin') || undefined}>
                {fieldHeading('targetMin', 'Min')}
                <input
                  type="number"
                  step="any"
                  value={objective.targetMin}
                  aria-invalid={invalid('targetMin') || undefined}
                  aria-describedby={invalid('targetMin') ? idFor('targetMin') : undefined}
                  disabled={disabled}
                  aria-label={
                    italian ? 'Minimo obiettivo' : 'Objective minimum'
                  }
                  onChange={(event) =>
                    changeNumeric(
                      'targetMin',
                      event.currentTarget.value,
                      event.currentTarget.validity.badInput,
                    )
                  }
                  onInput={(event) => {
                    if (event.currentTarget.validity.badInput)
                      changeNumeric('targetMin', '', true);
                  }}
                  onInvalid={(event) => event.preventDefault()}
                />
              </label>
              <label data-field-invalid={invalid('targetMax') || undefined}>
                {fieldHeading('targetMax', 'Max')}
                <input
                  type="number"
                  step="any"
                  value={objective.targetMax}
                  aria-invalid={invalid('targetMax') || undefined}
                  aria-describedby={invalid('targetMax') ? idFor('targetMax') : undefined}
                  disabled={disabled}
                  aria-label={
                    italian ? 'Massimo obiettivo' : 'Objective maximum'
                  }
                  onChange={(event) =>
                    changeNumeric(
                      'targetMax',
                      event.currentTarget.value,
                      event.currentTarget.validity.badInput,
                    )
                  }
                  onInput={(event) => {
                    if (event.currentTarget.validity.badInput)
                      changeNumeric('targetMax', '', true);
                  }}
                  onInvalid={(event) => event.preventDefault()}
                />
              </label>
              <label data-field-invalid={invalid('unitCode') || undefined}>
                {fieldHeading('unitCode', italian ? 'Unità' : 'Unit')}
                <input
                  type="text"
                  maxLength={40}
                  value={objective.unitCode}
                  aria-invalid={invalid('unitCode') || undefined}
                  aria-describedby={invalid('unitCode') ? idFor('unitCode') : undefined}
                  disabled={disabled}
                  aria-label={
                    italian
                      ? variant === 'edit'
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

        </div>
        <label className="temporal-create-objective__verification">
          <span>
            {italian ? 'Verifica dell’obiettivo' : 'Objective verification'}
          </span>
          <select
            value={objective.verificationMode ?? 'none'}
            disabled={disabled}
            aria-label={
              italian
                ? `Verifica obiettivo ${index + 1}`
                : `Verify objective ${index + 1}`
            }
            onChange={(event) =>
              update(objective.id, {
                verificationMode: event.currentTarget.value as
                  'none' | 'review_on_end',
              })
            }
          >
            <option value="none">
              {italian ? 'Nessuna richiesta' : 'No prompt'}
            </option>
            <option value="review_on_end">
              {italian ? 'Chiedi al termine' : 'Ask at end'}
            </option>
            <option value="auto_if_evidence" disabled>
              {italian
                ? 'Valutazione automatica · non disponibile'
                : 'Automatic · unavailable'}
            </option>
          </select>
        </label>
      </div>
      {extras ? (
        <div className="temporal-create-objective__extras">{extras}</div>
      ) : null}
    </div>
  );
}
