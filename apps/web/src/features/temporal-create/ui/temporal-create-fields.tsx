import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import { TemporalCreateActivityFields } from './temporal-create-activity-fields';
import { TemporalCreateConfirmationFields } from './temporal-create-confirmation-fields';
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

  const recurrenceAdvanced =
    fields.kind === 'event' ||
    (fields.kind === 'activity' && fields.eventRecurrence.patternKind !== 'none');

  return (
    <div
      className="temporal-create-advanced"
      data-create-advanced={fields.kind}
    >
      {fields.timeSemantics === 'timed' ? (
        <section
          className="temporal-create-section is-compact is-wide"
          aria-labelledby="temporal-create-time-heading"
        >
          <div className="temporal-create-section__heading">
            <h3 id="temporal-create-time-heading">
              {italian ? 'Riferimento orario' : 'Time reference'}
            </h3>
          </div>
          <div className="temporal-create-grid two">
            <label className="temporal-create-control">
              <span>{italian ? 'Modalità' : 'Mode'}</span>
              <select
                data-create-path="timeMode"
                value={fields.timeMode}
                onChange={(event) =>
                  onPatch({
                    timeMode: event.currentTarget
                      .value as TemporalCreateFields['timeMode'],
                  })
                }
              >
                <option value="floating">
                  {italian ? 'Ora locale' : 'Local time'}
                </option>
                <option value="zoned">
                  {italian ? 'Fuso specifico' : 'Named time zone'}
                </option>
              </select>
            </label>
            {fields.timeMode === 'zoned' ? (
              <label className="temporal-create-control">
                <span>{italian ? 'Fuso orario' : 'Time zone'}</span>
                <input
                  data-create-path="timeZoneId"
                  type="text"
                  value={fields.timeZoneId}
                  onChange={(event) =>
                    onPatch({ timeZoneId: event.currentTarget.value })
                  }
                  autoComplete="off"
                />
                {renderError('timeZoneId')}
              </label>
            ) : null}
          </div>
        </section>
      ) : null}

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

      {recurrenceAdvanced ? (
        <TemporalCreateRecurrenceFields
          fields={fields}
          depth="full"
          onPatch={onPatch}
          renderError={renderError}
        />
      ) : null}

      <TemporalCreateConfirmationFields
        fields={fields}
        onPatch={onPatch}
        renderError={renderError}
      />

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