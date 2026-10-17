import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateObjectiveComparator,
  TemporalCreateObjectiveDraft,
  TemporalCreateObjectiveKind,
} from '../model/temporal-create-u2-authoring';
import { TemporalObjectiveEditorRow } from './temporal-objective-editor-row';
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

  const update = (id: string, next: Partial<TemporalCreateObjectiveDraft>) => {
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
            <TemporalObjectiveEditorRow
              key={objective.id}
              objective={objective}
              index={index}
              total={draft.objectives.length}
              update={update}
              changeKind={changeKind}
              move={move}
              remove={remove}
            />
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
