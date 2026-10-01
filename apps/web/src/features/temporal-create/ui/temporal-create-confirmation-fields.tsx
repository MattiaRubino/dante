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
  const patchConfirmation = (
    patch: Partial<TemporalCreateFields['confirmation']>,
  ) => onPatch({ confirmation: { ...confirmation, ...patch } });

  return (
    <section
      className="temporal-create-section"
      aria-labelledby="temporal-create-outcome-verification-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-outcome-verification-heading">
            {italian ? 'Verifica esito' : 'Outcome verification'}
          </h3>
          <p>
            {italian
              ? 'Definisce come Dante dovrà gestire la verifica dopo che l’attività dovrebbe essere avvenuta. Non è un promemoria.'
              : 'Defines how Dante should handle verification after the activity was expected to happen. This is not a reminder.'}
          </p>
        </div>
      </div>

      <div className="temporal-create-grid two">
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

        <p className="temporal-create-truth-note">
          {italian
            ? 'Le strategie automatiche di verifica verranno esposte qui solo quando il relativo vertical sarà realmente disponibile. Ricorda resta configurabile nella parte principale di Crea.'
            : 'Automatic verification strategies will appear here only when the corresponding vertical is truly available. Reminder stays configurable in the main Create surface.'}
        </p>
      </div>
    </section>
  );
}
