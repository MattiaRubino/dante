import { useState, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';

import './temporal-create-advanced-activity-structure.css';

type TemporalCreateAdvancedActivityStructureProps = Readonly<{
  fields: TemporalCreateFields;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export function TemporalCreateAdvancedActivityStructure({
  fields,
  onPatch,
  renderError,
}: TemporalCreateAdvancedActivityStructureProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const [open, setOpen] = useState(false);
  const execution = fields.execution;
  const sessionConfigured = execution.sessionMode === 'splittable';

  const patchExecution = (patch: Partial<TemporalCreateFields['execution']>) =>
    onPatch({ execution: { ...execution, ...patch } });

  const addSessionConfiguration = () => {
    patchExecution({ sessionMode: 'splittable' });
    setOpen(false);
  };

  const removeSessionConfiguration = () => {
    patchExecution({ sessionMode: 'indivisible' });
  };

  return (
    <div
      className="temporal-create-advanced-structure-inline"
      data-create-activity-structure
    >
      <div className="temporal-create-advanced-structure-inline__tree">
        <div className="temporal-create-advanced-structure-inline__branch">
          <span
            className="temporal-create-advanced-structure-inline__connector"
            aria-hidden="true"
          />
          <div className="temporal-create-advanced-structure-inline__add">
            <button
              type="button"
              aria-label={italian ? 'Aggiungi alla struttura' : 'Add to structure'}
              aria-expanded={open}
              onClick={() => setOpen((current) => !current)}
            >
              <span aria-hidden="true">+</span>
              {italian ? 'Aggiungi' : 'Add'}
            </button>

            {open ? (
              <div
                className="temporal-create-structure-menu"
                role="menu"
                aria-label={italian ? 'Aggiungi alla struttura' : 'Add to structure'}
              >
                <button
                  type="button"
                  role="menuitem"
                  disabled
                  title={
                    italian
                      ? 'La gerarchia Activity → sotto-attività non ha ancora un contratto canonico: non viene simulata con Step.'
                      : 'Activity → sub-activity hierarchy has no canonical contract yet; it is not simulated with Step.'
                  }
                >
                  {italian ? 'Sotto-attività' : 'Sub-activity'}
                </button>
                <button
                  type="button"
                  role="menuitem"
                  disabled={sessionConfigured}
                  onClick={addSessionConfiguration}
                >
                  {italian ? 'Sessione' : 'Session'}
                </button>
              </div>
            ) : null}
          </div>
        </div>

        {sessionConfigured ? (
          <div className="temporal-create-structure-node is-session" data-create-structure-session>
            <div className="temporal-create-structure-node__identity">
              <span className="temporal-create-structure-node__elbow" aria-hidden="true" />
              <div>
                <strong>{italian ? 'Sessione' : 'Session'}</strong>
                <label className="temporal-create-structure-node__minimum">
                  <span>{italian ? 'Minimo' : 'Minimum'}</span>
                  <input
                    data-create-path="execution.minSessionMinutes"
                    type="number"
                    min="1"
                    step="1"
                    value={execution.minSessionMinutes}
                    onChange={(event) =>
                      patchExecution({
                        minSessionMinutes: Number(event.currentTarget.value),
                      })
                    }
                  />
                  <span>min</span>
                </label>
                {renderError('execution.minSessionMinutes')}
              </div>
            </div>

            <div
              className="temporal-create-structure-node__actions"
              aria-label={italian ? 'Controlli Sessione' : 'Session controls'}
            >
              <button
                type="button"
                disabled
                aria-label={italian ? 'Avvia Sessione dopo la creazione' : 'Start Session after creation'}
                title={italian ? 'Disponibile quando l’Activity esiste.' : 'Available once the Activity exists.'}
              >
                ▶
              </button>
              <button
                type="button"
                disabled
                aria-label={italian ? 'Pausa Sessione dopo la creazione' : 'Pause Session after creation'}
                title={italian ? 'Disponibile quando una Sessione è attiva.' : 'Available while a Session is active.'}
              >
                ⏸
              </button>
              <button
                type="button"
                disabled
                aria-label={italian ? 'Riprendi Sessione dopo la creazione' : 'Resume Session after creation'}
                title={italian ? 'Disponibile quando una Sessione è in pausa.' : 'Available while a Session is paused.'}
              >
                ▶
              </button>
              <button
                type="button"
                disabled
                aria-label={italian ? 'Termina Sessione dopo la creazione' : 'End Session after creation'}
                title={italian ? 'Disponibile quando una Sessione è attiva.' : 'Available while a Session is active.'}
              >
                ■
              </button>
              <button
                className="is-remove"
                type="button"
                aria-label={italian ? 'Rimuovi configurazione Sessione' : 'Remove Session configuration'}
                onClick={removeSessionConfiguration}
              >
                ×
              </button>
            </div>
          </div>
        ) : null}
      </div>

      <div
        className="temporal-create-advanced-structure-inline__actions"
        data-create-structure-actions
        aria-label={italian ? 'Azioni attività' : 'Activity actions'}
      />
    </div>
  );
}
