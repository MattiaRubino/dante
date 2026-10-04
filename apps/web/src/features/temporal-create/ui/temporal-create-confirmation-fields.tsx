import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import type { TemporalCreateRealityMode } from '../model/temporal-create-u2-authoring';
import { useTemporalCreateU2Draft } from './temporal-create-u2-draft-context';

type TemporalCreateConfirmationFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  onPatch?: (patch: Partial<TemporalCreateFields>) => void;
  renderError?: (path: string) => React.ReactNode;
}>;

export function TemporalCreateConfirmationFields({
  fields,
}: TemporalCreateConfirmationFieldsProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const [open, setOpen] = useState(false);
  const { draft, patch } = useTemporalCreateU2Draft();

  if (fields.kind !== 'activity') return null;

  const structure = draft.activityStructure;
  const setMode = (realityMode: TemporalCreateRealityMode) =>
    patch({
      activityStructure: Object.freeze({ ...structure, realityMode }),
    });

  return (
    <section
      className="temporal-create-section temporal-create-reality-section"
      aria-labelledby="temporal-create-reality-heading"
    >
      <button
        type="button"
        className="temporal-create-reality-trigger"
        aria-expanded={open}
        aria-controls="temporal-create-reality-options"
        onClick={() => setOpen((current) => !current)}
      >
        <span id="temporal-create-reality-heading">
          {italian ? 'Realtà' : 'Reality'}
        </span>
        <span aria-hidden="true">{open ? '⌃' : '⌄'}</span>
      </button>

      {open ? (
        <div
          className="temporal-create-reality-section__body"
          id="temporal-create-reality-options"
        >
          <h4>{italian ? 'Gestione dell’esito' : 'Outcome handling'}</h4>
          <label className="temporal-create-control">
            <span>{italian ? 'Quando verificare' : 'When to verify'}</span>
            <select
              data-create-path="activity.realityMode"
              aria-label={italian ? 'Gestione realtà' : 'Reality handling'}
              value={structure.realityMode}
              onChange={(event) =>
                setMode(event.currentTarget.value as TemporalCreateRealityMode)
              }
            >
              <option value="manual">
                {italian ? 'Gestione manuale' : 'Manual handling'}
              </option>
              <option value="review_on_end">
                {italian ? 'Chiedimi alla fine' : 'Ask me at the end'}
              </option>
              <option value="auto_confirm_outcome">
                {italian
                  ? 'Conferma l’esito registrato'
                  : 'Confirm the recorded outcome'}
              </option>
            </select>
          </label>
          <p className="temporal-create-reality-note">
            {italian
              ? 'Questa regola non crea automaticamente ciò che è successo: Actual e Outcome restano verità separate.'
              : 'This rule never invents what happened: Actual and Outcome remain separate truth.'}
          </p>
        </div>
      ) : null}
    </section>
  );
}
