import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreateRealityMode } from '../model/temporal-create-u2-authoring';
import { TemporalCreateObjectives } from './temporal-create-objectives';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

import './temporal-create-reality-objectives-section.css';

type Props = Readonly<{ fields: TemporalCreateFields }>;

export function TemporalCreateRealityObjectivesSection({ fields }: Props) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  const structure = draft.activityStructure;

  const applyMode = (realityMode: TemporalCreateRealityMode) => {
    const hasRequiredChild = structure.children.some(
      (child) => child.requirementCode === 'required',
    );

    patch({
      realityMode,
      activityStructure: Object.freeze({
        ...structure,
        realityMode,
        childGuardMode:
          fields.kind === 'activity' &&
          realityMode !== 'manual' &&
          hasRequiredChild
            ? 'confirm'
            : 'none',
      }),
    });
  };

  const subjectLabel =
    fields.kind === 'event'
      ? italian
        ? 'Svolgimento dell’evento'
        : 'Event occurrence'
      : italian
        ? 'Svolgimento dell’attività'
        : 'Activity completion';

  const modes: readonly Readonly<{
    value: TemporalCreateRealityMode;
    label: string;
  }>[] = Object.freeze([
    Object.freeze({
      value: 'manual',
      label: italian ? 'Nessuna verifica' : 'No review',
    }),
    Object.freeze({
      value: 'review_on_end',
      label: italian ? 'Chiedi al termine' : 'Ask at the end',
    }),
    Object.freeze({
      value: 'auto_confirm_outcome',
      label: italian ? 'Conferma automatica' : 'Confirm automatically',
    }),
  ]);

  return (
    <section
      className="temporal-create-reality-objectives"
      aria-label={italian ? 'Svolgimento e obiettivi' : 'Occurrence and objectives'}
    >
      <div className="temporal-create-reality-objectives__heading">
        <div>
          <h3>{italian ? 'Svolgimento e obiettivi' : 'Occurrence and objectives'}</h3>
          <p>
            {italian
              ? 'Decidi se verificare lo svolgimento e quali risultati vuoi misurare.'
              : 'Choose whether to review occurrence and which results you want to measure.'}
          </p>
        </div>
      </div>

      <div
        className="temporal-create-reality-objectives__block is-reality"
        data-reality-policy={fields.kind}
      >
        <div className="temporal-create-reality-objectives__block-copy">
          <strong>{subjectLabel}</strong>
          <span>
            {italian
              ? 'Come vuoi gestire la conferma dello svolgimento?'
              : 'How should occurrence confirmation be handled?'}
          </span>
        </div>

        <div
          className="temporal-create-reality-mode"
          role="radiogroup"
          aria-label={
            italian
              ? 'Modalità ' + subjectLabel.toLowerCase()
              : subjectLabel + ' mode'
          }
        >
          {modes.map((mode) => (
            <button
              key={mode.value}
              type="button"
              role="radio"
              aria-checked={draft.realityMode === mode.value}
              className={draft.realityMode === mode.value ? 'is-active' : ''}
              onClick={() => applyMode(mode.value)}
            >
              {mode.label}
            </button>
          ))}
        </div>
      </div>

      <div className="temporal-create-reality-objectives__divider" />

      <div
        className="temporal-create-reality-objectives__block is-objectives"
        data-create-path="objectives"
      >
        <div className="temporal-create-reality-objectives__block-copy">
          <strong>{italian ? 'Obiettivi' : 'Objectives'}</strong>
          <span>
            {italian
              ? 'Aggiungi solo ciò che vuoi verificare o misurare separatamente.'
              : 'Add only the results you want to review or measure separately.'}
          </span>
        </div>
        <TemporalCreateObjectives />
      </div>
    </section>
  );
}
