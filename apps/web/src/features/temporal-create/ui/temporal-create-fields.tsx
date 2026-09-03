import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import { TemporalCreateActivityFields } from './temporal-create-activity-fields';
import { TemporalCreateAppearanceFields } from './temporal-create-appearance-fields';
import { TemporalCreateCoreFields } from './temporal-create-core-fields';
import { TemporalCreateEventFields } from './temporal-create-event-fields';
import { TemporalCreateOrganizationFields } from './temporal-create-organization-fields';
import { TemporalCreateRecurrenceFields } from './temporal-create-recurrence-fields';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

type TemporalCreateAdvancedFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  contexts: readonly TemporalCreateContextOption[];
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
  renderError: (path: string) => ReactNode;
}>;

export { TemporalCreateCoreFields };

export function TemporalCreateAdvancedFields({
  fields,
  contexts,
  depth,
  onPatch,
  renderError,
}: TemporalCreateAdvancedFieldsProps) {
  const { t } = useTranslation('common');

  if (depth === 'quick') {
    return null;
  }

  return (
    <div className="temporal-create-advanced" data-create-advanced={fields.kind}>
      {fields.timeSemantics === 'timed' ? (
        <section
          className="temporal-create-section is-compact"
          aria-labelledby="temporal-create-time-heading"
        >
          <div className="temporal-create-section__heading">
            <div>
              <h3 id="temporal-create-time-heading">
                {t(($) => $.common.home.timeline.create.timeDetails.title)}
              </h3>
              <p>
                {t(
                  ($) => $.common.home.timeline.create.timeDetails.description,
                )}
              </p>
            </div>
          </div>
          <div className="temporal-create-grid two">
            <label className="temporal-create-control">
              <span>{t(($) => $.common.home.timeline.create.timeMode.label)}</span>
              <select
                value={fields.timeMode}
                onChange={(event) =>
                  onPatch({
                    timeMode: event.currentTarget
                      .value as TemporalCreateFields['timeMode'],
                  })
                }
              >
                <option value="floating">
                  {t(($) => $.common.home.timeline.create.timeMode.floating)}
                </option>
                <option value="zoned">
                  {t(($) => $.common.home.timeline.create.timeMode.zoned)}
                </option>
              </select>
            </label>
            {fields.timeMode === 'zoned' ? (
              <label className="temporal-create-control">
                <span>{t(($) => $.common.home.timeline.create.timeZone)}</span>
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
        <>
          <TemporalCreateEventFields
            fields={fields}
            depth="full"
            onPatch={onPatch}
            renderError={renderError}
          />
          <TemporalCreateRecurrenceFields
            fields={fields}
            depth="full"
            onPatch={onPatch}
            renderError={renderError}
          />
        </>
      )}

      <TemporalCreateOrganizationFields
        fields={fields}
        depth="full"
        onPatch={onPatch}
      />

      <TemporalCreateAppearanceFields
        fields={fields}
        contexts={contexts}
        onPatch={onPatch}
      />
    </div>
  );
}
