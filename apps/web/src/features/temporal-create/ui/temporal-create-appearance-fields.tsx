import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateAppearanceTone,
  TemporalCreateFields,
} from '../model/temporal-create-session';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

import './temporal-create-appearance-fields.css';

const APPEARANCE_TONES: readonly TemporalCreateAppearanceTone[] = Object.freeze([
  'focus',
  'meeting',
  'health',
  'creative',
  'personal',
  'urgent',
]);

type TemporalCreateAppearanceFieldsProps = Readonly<{
  fields: TemporalCreateFields;
  contexts: readonly TemporalCreateContextOption[];
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
}>;

export function TemporalCreateAppearanceFields({
  fields,
  contexts,
  onPatch,
}: TemporalCreateAppearanceFieldsProps) {
  const { t } = useTranslation('common');
  const inheritedContext =
    contexts.find((context) => context.id === fields.contextId) ?? null;
  const inheritedTone = inheritedContext?.tone ?? 'personal';
  const colorLabel = (tone: TemporalCreateAppearanceTone): string => {
    switch (tone) {
      case 'focus':
        return t(($) => $.common.home.timeline.create.appearance.colors.purple);
      case 'meeting':
        return t(($) => $.common.home.timeline.create.appearance.colors.cyan);
      case 'health':
        return t(($) => $.common.home.timeline.create.appearance.colors.green);
      case 'creative':
        return t(($) => $.common.home.timeline.create.appearance.colors.amber);
      case 'personal':
        return t(($) => $.common.home.timeline.create.appearance.colors.rose);
      case 'urgent':
        return t(($) => $.common.home.timeline.create.appearance.colors.red);
    }
  };

  return (
    <section
      className="temporal-create-section is-compact temporal-create-appearance"
      aria-labelledby="temporal-create-appearance-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-appearance-heading">
            {t(($) => $.common.home.timeline.create.appearance.title)}
          </h3>
          <p>
            {t(($) => $.common.home.timeline.create.appearance.description)}
          </p>
        </div>
      </div>

      <fieldset className="temporal-create-appearance__fieldset">
        <legend>
          {t(($) => $.common.home.timeline.create.appearance.choice)}
        </legend>

        <label
          className="temporal-create-appearance__inherit"
          data-appearance-tone={inheritedTone}
        >
          <input
            type="radio"
            name="temporal-create-appearance-tone"
            checked={fields.appearanceTone === null}
            onChange={() => onPatch({ appearanceTone: null })}
          />
          <span className="temporal-create-appearance__swatch" aria-hidden="true" />
          <span>
            <strong>
              {t(($) => $.common.home.timeline.create.appearance.inherit)}
            </strong>
            <small>
              {inheritedContext?.label ??
                t(($) => $.common.home.timeline.create.context)}
            </small>
          </span>
          <i aria-hidden="true">✓</i>
        </label>

        <div className="temporal-create-appearance__tones">
          {APPEARANCE_TONES.map((tone) => {
            const label = colorLabel(tone);
            return (
              <label
                key={tone}
                className="temporal-create-appearance__tone"
                data-appearance-tone={tone}
                title={label}
              >
                <input
                  type="radio"
                  name="temporal-create-appearance-tone"
                  checked={fields.appearanceTone === tone}
                  onChange={() => onPatch({ appearanceTone: tone })}
                  aria-label={`${t(($) => $.common.home.timeline.create.appearance.override)} · ${label}`}
                />
                <span
                  className="temporal-create-appearance__swatch"
                  aria-hidden="true"
                />
                <small>{label}</small>
              </label>
            );
          })}
        </div>
      </fieldset>
    </section>
  );
}
