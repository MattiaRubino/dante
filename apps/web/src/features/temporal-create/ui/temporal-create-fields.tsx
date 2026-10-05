import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import { TemporalCreateActivityFields } from './temporal-create-activity-fields';
import { TemporalCreateCoreFieldsU2 } from './temporal-create-core-u2';
import { TemporalCreateEventFields } from './temporal-create-event-fields';
import { TemporalCreateRecurrenceFields } from './temporal-create-recurrence-fields';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

import './temporal-create-advanced-shell.css';

type TemporalCreateAdvancedFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  contexts: readonly TemporalCreateContextOption[];
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export { TemporalCreateCoreFieldsU2 as TemporalCreateCoreFields };

export function TemporalCreateAdvancedFields({
  fields,
  depth,
  onPatch,
  renderError,
}: TemporalCreateAdvancedFieldsProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');

  if (depth === 'quick') {
    return null;
  }

  return (
    <div
      className="temporal-create-advanced"
      data-create-advanced={fields.kind}
    >
      {fields.kind === 'activity' ? (
        <TemporalCreateActivityFields
          fields={fields}
          depth="full"
          onPatch={onPatch}
          renderError={renderError}
        />
      ) : (
        <TemporalCreateEventFields
          fields={fields}
          depth="full"
          onPatch={onPatch}
          renderError={renderError}
        />
      )}

      {fields.kind === 'event' ? (
        <TemporalCreateRecurrenceFields
          fields={fields}
          depth="full"
          onPatch={onPatch}
          renderError={renderError}
        />
      ) : null}

      <section
        className="temporal-create-section is-wide temporal-create-description-section"
        aria-labelledby="temporal-create-description-heading"
      >
        <div className="temporal-create-section__heading">
          <h3 id="temporal-create-description-heading">
            {italian ? 'Descrizione' : 'Description'}
          </h3>
        </div>
        <textarea
          className="temporal-create-u2-description temporal-create-advanced-description"
          value={fields.notes}
          aria-label={italian ? 'Descrizione avanzata' : 'Advanced description'}
          placeholder={italian ? 'Descrizione' : 'Description'}
          rows={5}
          onChange={(event) => onPatch({ notes: event.currentTarget.value })}
        />
      </section>
    </div>
  );
}
