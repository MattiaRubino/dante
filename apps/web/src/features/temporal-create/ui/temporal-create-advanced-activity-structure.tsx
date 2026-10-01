import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import './temporal-create-advanced-activity-structure.css';

export function TemporalCreateAdvancedActivityStructure() {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const [open, setOpen] = useState(false);

  return (
    <div
      className="temporal-create-advanced-structure-inline"
      data-create-activity-structure
    >
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
              <button type="button" role="menuitem" disabled>
                {italian ? 'Sotto-attività' : 'Sub-activity'}
              </button>
              <button type="button" role="menuitem" disabled>
                {italian ? 'Sessione' : 'Session'}
              </button>
            </div>
          ) : null}
        </div>
      </div>

      <div
        className="temporal-create-advanced-structure-inline__actions"
        data-create-structure-actions
        aria-label={italian ? 'Azioni attività' : 'Activity actions'}
      />
    </div>
  );
}
