import { useTranslation } from 'react-i18next';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import { TemporalCreateObjectives } from './temporal-create-objectives';

import './temporal-create-reality-objectives-section.css';

type Props = Readonly<{ fields: TemporalCreateFields }>;

/**
 * Each Objective owns its verification policy. The legacy occurrence Reality
 * policy stays in draft persistence; this view never silently resets it.
 */
export function TemporalCreateRealityObjectivesSection({ fields }: Props) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');

  return (
    <section
      className="temporal-create-reality-objectives"
      aria-label={
        italian ? 'Configurazione obiettivi' : 'Objective configuration'
      }
      data-create-objective-subject={fields.kind}
    >
      <div
        className="temporal-create-reality-objectives__block is-objectives"
        data-create-path="objectives"
      >
        <div className="temporal-create-reality-objectives__block-copy">
          <strong className="temporal-editor-section-heading">
            {italian ? 'Obiettivi' : 'Objectives'}
          </strong>
        </div>
        <TemporalCreateObjectives />
      </div>
    </section>
  );
}
