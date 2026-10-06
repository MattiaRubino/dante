import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateObjectiveComparator,
  TemporalCreateObjectiveDraft,
  TemporalCreateObjectiveKind,
} from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

import './temporal-create-objectives.css';

function newObjective(): TemporalCreateObjectiveDraft {
  return Object.freeze({
    id: crypto.randomUUID(),
    label: '',
    resultKind: 'boolean' as const,
    comparatorCode: null,
    targetValue: '',
    targetMin: '',
    targetMax: '',
    unitCode: '',
  });
}

export function TemporalCreateObjectives() {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();

  const publish = (objectives: readonly TemporalCreateObjectiveDraft[]) =>
    patch({ objectives: Object.freeze([...objectives]) });

  const update = (
    id: string,
    next: Partial<TemporalCreateObjectiveDraft>,
  ) => {
    publish(
      draft.objectives.map((objective) =>
        objective.id === id
          ? Object.freeze({ ...objective, ...next })
          : objective,
      ),
    );
  };

  const changeKind = (id: string, resultKind: TemporalCreateObjectiveKind) => {
    update(id, {
      resultKind,
      comparatorCode:
        resultKind === 'quantity'
          ? 'gte'
          : resultKind === 'range'
            ? 'between'
            : null,
      targetValue: '',
      targetMin: '',
      targetMax: '',
      unitCode: '',
    });
  };

  const move = (index: number, direction: -1 | 1) => {
    const target = index + direction;
    if (target < 0 || target >= draft.objectives.length) return;
    const next = [...draft.objectives];
    [next[index], next[target]] = [next[target]!, next[index]!];
    publish(next);
  };

  const remove = (id: string) =>
    publish(draft.objectives.filter((objective) => objective.id !== id));

  return (
    <section
      className="temporal-create-objectives"
      data-create-objectives
      aria-label={italian ? 'Obiettivi' : 'Objectives'}
    >
      {draft.objectives.length > 0 ? (
        <div className="temporal-create-objectives__list">
          {draft.objectives.map((objective, index) => (
            <div
              className="temporal-create-objective"
              data-create-objective
              key={objective.id}
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
                  type="text"
                  maxLength={300}
                  value={objective.label}
                  aria-label={
                    italian
                      ? `Obiettivo ${index + 1}`
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
                    disabled={index === 0}
                    aria-label={italian ? 'Sposta obiettivo su' : 'Move objective up'}
                    onClick={() => move(index, -1)}
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    disabled={index === draft.objectives.length - 1}
                    aria-label={italian ? 'Sposta obiettivo giù' : 'Move objective down'}
                    onClick={() => move(index, 1)}
                  >
                    ↓
                  </button>
                  <button
                    type="button"
                    className="is-remove"
                    aria-label={italian ? 'Rimuovi obiettivo' : 'Remove objective'}
                    onClick={() => remove(objective.id)}
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
                    aria-label={
                      italian
                        ? `Tipo risultato obiettivo ${index + 1}`
                        : `Objective ${index + 1} result type`
                    }
                    onChange={(event) =>
                      changeKind(
                        objective.id,
                        event.currentTarget.value as TemporalCreateObjectiveKind,
                      )
                    }
                  >
                    <option value="boolean">{italian ? 'Sì / No' : 'Yes / No'}</option>
                    <option value="quantity">{italian ? 'Quantità' : 'Quantity'}</option>
                    <option value="qualitative">
                      {italian ? 'Valutazione' : 'Assessment'}
                    </option>
                    <option value="range">{italian ? 'Intervallo' : 'Range'}</option>
                  </select>
                </label>

                {objective.resultKind === 'quantity' ? (
                  <>
                    <label>
                      <span>{italian ? 'Regola' : 'Rule'}</span>
                      <select
                        value={objective.comparatorCode ?? 'gte'}
                        aria-label={italian ? 'Confronto obiettivo' : 'Objective comparator'}
                        onChange={(event) =>
                          update(objective.id, {
                            comparatorCode:
                              event.currentTarget
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
                        aria-label={italian ? 'Target obiettivo' : 'Objective target'}
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
                        aria-label={italian ? 'Unità obiettivo' : 'Objective unit'}
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
                        aria-label={italian ? 'Minimo obiettivo' : 'Objective minimum'}
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
                        aria-label={italian ? 'Massimo obiettivo' : 'Objective maximum'}
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
                        aria-label={italian ? 'Unità obiettivo' : 'Objective unit'}
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
            </div>
          ))}
        </div>
      ) : null}

      <div className="temporal-create-objectives__root-actions">
        <button
          className="temporal-create-objectives__add"
          type="button"
          aria-label={italian ? 'Aggiungi obiettivo' : 'Add objective'}
          onClick={() => publish([...draft.objectives, newObjective()])}
        >
          <span aria-hidden="true">＋</span>
          {italian ? 'Aggiungi obiettivo' : 'Add objective'}
        </button>
      </div>
    </section>
  );
}
