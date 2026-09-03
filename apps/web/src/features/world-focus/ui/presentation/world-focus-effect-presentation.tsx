import { useTranslation } from 'react-i18next';

import type { WorldFocusEffectPresentation } from '../../model/world-focus-effect';
import {
  WorldFocusQualifier,
  WorldFocusQualifierGroup,
} from './world-focus-qualifiers';

type WorldFocusEffectStatusProps = Readonly<{
  effect: WorldFocusEffectPresentation;
}>;

export function WorldFocusEffectStatus({ effect }: WorldFocusEffectStatusProps) {
  const { t } = useTranslation('common');

  return (
    <WorldFocusQualifierGroup
      aria-label={t(($) => $.common.worldFocus.presentation.qualifiers.effect)}
      data-world-focus-effect-presentation="true"
    >
      <WorldFocusQualifier axis="effect-state" state={effect.state}>
        {t(($) => $.common.worldFocus.presentation.effect.states[effect.state])}
      </WorldFocusQualifier>
      {effect.executionRevalidation === 'required-before-execution' ? (
        <WorldFocusQualifier
          axis="execution-revalidation"
          state={effect.executionRevalidation}
        >
          {t(($) => $.common.worldFocus.presentation.effect.revalidationRequired)}
        </WorldFocusQualifier>
      ) : null}
    </WorldFocusQualifierGroup>
  );
}
