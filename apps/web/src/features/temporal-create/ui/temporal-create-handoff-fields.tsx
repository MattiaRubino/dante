import { useTranslation } from 'react-i18next';

import {
  temporalCreateHandoffRegistry,
  type TemporalCreateHandoffTarget,
} from '../application/temporal-create-handoff';

export function TemporalCreateHandoffFields() {
  const { t } = useTranslation('common');
  const handoffs = temporalCreateHandoffRegistry();

  const label = (handoff: TemporalCreateHandoffTarget): string => {
    switch (handoff) {
      case 'project':
        return t(($) => $.common.home.timeline.create.handoffs.project);
      case 'goal':
        return t(($) => $.common.home.timeline.create.handoffs.goal);
      case 'routine':
        return t(($) => $.common.home.timeline.create.handoffs.routine);
      case 'program':
        return t(($) => $.common.home.timeline.create.handoffs.program);
      case 'world':
        return t(($) => $.common.home.timeline.create.handoffs.world);
      case 'template':
        return t(($) => $.common.home.timeline.create.handoffs.template);
      case 'reminder':
        return t(($) => $.common.home.timeline.create.handoffs.reminder);
      case 'block':
        return t(($) => $.common.home.timeline.create.handoffs.block);
      case 'asset':
        return t(($) => $.common.home.timeline.create.handoffs.asset);
    }
  };

  return (
    <section
      className="temporal-create-section"
      aria-labelledby="temporal-create-handoff-heading"
    >
      <div className="temporal-create-section__heading">
        <div>
          <h3 id="temporal-create-handoff-heading">
            {t(($) => $.common.home.timeline.create.handoffs.otherTitle)}
          </h3>
          <p>{t(($) => $.common.home.timeline.create.handoffs.otherDescription)}</p>
        </div>
      </div>

      <div className="temporal-create-handoff-grid">
        {handoffs.map((handoff) => (
          <button
            key={handoff.target}
            type="button"
            disabled
            data-temporal-create-handoff-target={handoff.target}
            data-temporal-create-handoff-availability={handoff.availability}
          >
            <strong>{label(handoff.target)}</strong>
            <small>{t(($) => $.common.home.timeline.create.handoffs.ownerRequired)}</small>
          </button>
        ))}
      </div>
      <p className="temporal-create-truth-note">
        {t(($) => $.common.home.timeline.create.handoffs.separateVertical)}
      </p>
    </section>
  );
}
