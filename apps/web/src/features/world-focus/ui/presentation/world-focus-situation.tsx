import { useTranslation } from 'react-i18next';

import type { WorldFocusSituationProjection } from '../../model/world-focus-direct-projections';
import {
  requireWorldFocusDisplayBinding,
  type WorldFocusDisplayBinding,
  type WorldFocusDisplayBindingSet,
} from './world-focus-display-bindings';
import { WorldFocusPresentationSection } from './world-focus-presentation-primitives';

function bindingKey(binding: WorldFocusDisplayBinding): string {
  return `${binding.reference.kind}\u0000${binding.reference.key}`;
}

type WorldFocusSituationProps = Readonly<{
  projection: WorldFocusSituationProjection;
  bindings: WorldFocusDisplayBindingSet;
}>;

export function WorldFocusSituation({
  projection,
  bindings,
}: WorldFocusSituationProps) {
  const { t } = useTranslation('common');
  const orderedBindings = projection.orderedSituationReferences.map((reference) =>
    requireWorldFocusDisplayBinding(bindings, reference),
  );

  return (
    <WorldFocusPresentationSection
      className="world-focus-direct-output"
      title={t(($) => $.common.worldFocus.presentation.situation.title)}
      data-world-focus-direct-output="situation"
    >
      <ul className="world-focus-direct-list">
        {orderedBindings.map((binding) => (
          <li className="world-focus-direct-row" key={bindingKey(binding)}>
            <p className="world-focus-presentation-row-title">{binding.label}</p>
            {binding.supportingText === undefined ? null : (
              <p className="world-focus-presentation-row-supporting">
                {binding.supportingText}
              </p>
            )}
          </li>
        ))}
      </ul>
    </WorldFocusPresentationSection>
  );
}
