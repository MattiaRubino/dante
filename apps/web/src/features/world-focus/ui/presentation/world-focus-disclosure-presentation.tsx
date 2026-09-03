import { useTranslation } from 'react-i18next';

import type { WorldFocusDisclosureOutcome } from '../../model/world-focus-disclosure';
import {
  WorldFocusQualifier,
  WorldFocusQualifierGroup,
} from './world-focus-qualifiers';

type WorldFocusDisclosurePresentationProps = Readonly<{
  disclosure: WorldFocusDisclosureOutcome;
}>;

export function WorldFocusDisclosurePresentation({
  disclosure,
}: WorldFocusDisclosurePresentationProps) {
  const { t } = useTranslation('common');

  if (disclosure.status === 'available') return null;

  const label =
    disclosure.status === 'restricted'
      ? t(($) => $.common.worldFocus.presentation.disclosure.states.restricted)
      : t(($) => $.common.worldFocus.presentation.disclosure.states.unavailable);

  return (
    <WorldFocusQualifierGroup
      aria-label={t(($) => $.common.worldFocus.presentation.qualifiers.disclosure)}
      data-world-focus-disclosure-presentation="true"
    >
      <WorldFocusQualifier axis="disclosure" state={disclosure.status}>
        {label}
      </WorldFocusQualifier>
    </WorldFocusQualifierGroup>
  );
}
