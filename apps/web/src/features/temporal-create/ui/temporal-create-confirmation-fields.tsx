import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreateRealityMode } from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

type Props = Readonly<{ fields: TemporalCreateFields }>;

export function TemporalCreateConfirmationToggle({ fields }: Props) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  if (fields.kind !== 'activity') return null;

  const structure = draft.activityStructure;
  const enabled = structure.realityMode !== 'manual';
  return (
    <label className="temporal-create-outcome-toggle" data-outcome-confirmation="activity">
      <input
        type="checkbox"
        checked={enabled}
        onChange={(event) => {
          const realityMode = event.currentTarget.checked ? 'review_on_end' : 'manual';
          const hasRequiredChild = structure.children.some(
            (child) => child.requirementCode === 'required',
          );
          patch({
            activityStructure: Object.freeze({
              ...structure,
              realityMode,
              childGuardMode: realityMode !== 'manual' && hasRequiredChild ? 'confirm' : 'none',
            }),
          });
        }}
      />
      {italian ? 'Verifica esito' : 'Review outcome'}
    </label>
  );
}

export function TemporalCreateConfirmationFields({ fields }: Props) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const { draft, patch } = useTemporalCreateU2Draft();
  if (fields.kind !== 'activity' || draft.activityStructure.realityMode === 'manual') {
    return null;
  }

  const structure = draft.activityStructure;
  const options: readonly [TemporalCreateRealityMode, string][] = italian
    ? [
        ['review_on_end', 'Chiedi conferma alla fine'],
        ['auto_confirm_outcome', 'Conferma automaticamente'],
      ]
    : [
        ['review_on_end', 'Ask for confirmation at the end'],
        ['auto_confirm_outcome', 'Confirm automatically'],
      ];

  return (
    <fieldset
      className="temporal-create-outcome-field"
      aria-label={italian ? 'Modalità verifica esito' : 'Outcome review mode'}
    >
      <legend className="temporal-create-visually-hidden">
        {italian ? 'Modalità verifica esito' : 'Outcome review mode'}
      </legend>
      {options.map(([realityMode, label]) => (
        <label key={realityMode} className="temporal-create-outcome-field__option">
          <input
            type="radio"
            name="temporal-create-outcome-mode"
            checked={structure.realityMode === realityMode}
            onChange={() => patch({
              activityStructure: Object.freeze({ ...structure, realityMode }),
            })}
          />
          {label}
        </label>
      ))}
    </fieldset>
  );
}
