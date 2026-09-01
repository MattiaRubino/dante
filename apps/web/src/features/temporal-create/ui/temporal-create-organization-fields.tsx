import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateFields,
  TemporalCreateSurface,
} from '../model/temporal-create-session';

type OrganizationFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  depth: TemporalCreateSurface;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
}>;

export function TemporalCreateOrganizationFields({
  fields,
  depth,
  onPatch,
}: OrganizationFieldsProps) {
  const { t } = useTranslation('common');

  return (
    <section
      className="temporal-create-section"
      aria-labelledby="temporal-create-organization-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-organization-heading">
            {t(($) => $.common.home.timeline.create.organization.title)}
          </h3>
          <p>
            {t(($) => $.common.home.timeline.create.organization.description)}
          </p>
        </div>
      </div>

      <label className="temporal-create-control">
        <span>{t(($) => $.common.home.timeline.create.notes)}</span>
        <textarea
          value={fields.notes}
          rows={depth === 'full' ? 5 : 3}
          onChange={(event) => onPatch({ notes: event.currentTarget.value })}
          placeholder={t(
            ($) => $.common.home.timeline.create.notesPlaceholder,
          )}
        />
      </label>
    </section>
  );
}
