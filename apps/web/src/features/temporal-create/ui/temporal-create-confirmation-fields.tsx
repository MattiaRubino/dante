import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';

type TemporalCreateConfirmationFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => React.ReactNode;
}>;

export function TemporalCreateConfirmationFields({
  fields,
  onPatch,
  renderError,
}: TemporalCreateConfirmationFieldsProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const confirmation = fields.confirmation;
  const [open, setOpen] = useState(false);
  const patchConfirmation = (
    patch: Partial<TemporalCreateFields['confirmation']>,
  ) => onPatch({ confirmation: { ...confirmation, ...patch } });

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
          <h4>{italian ? 'Verifica esito' : 'Outcome verification'}</h4>
          <label className="temporal-create-control">
            <span>{italian ? 'Regola di verifica' : 'Verification rule'}</span>
            <select
              data-create-path="confirmation.outcomePolicy"
              value={confirmation.outcomePolicy}
              onChange={(event) =>
                patchConfirmation({
                  outcomePolicy: event.currentTarget
                    .value as TemporalCreateFields['confirmation']['outcomePolicy'],
                })
              }
            >
              <option value="inherit">
                {italian ? 'Eredita impostazione' : 'Use inherited setting'}
              </option>
            </select>
            {renderError('confirmation.outcomePolicy')}
          </label>

          <div
            className="temporal-create-reality-flow"
            aria-label={
              italian ? 'Flusso realtà ed esito' : 'Reality and outcome flow'
            }
          >
            <span>Actual</span>
            <span aria-hidden="true">→</span>
            <span>Outcome</span>
            <span aria-hidden="true">→</span>
            <span>Confirmation</span>
            <span aria-hidden="true">→</span>
            <span>Reconciliation</span>
          </div>
        </div>
      ) : null}
    </section>
  );
}
