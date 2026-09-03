import { useTranslation } from 'react-i18next';

import type {
  WorldFocusCoverageFacet,
  WorldFocusFreshnessFacet,
  WorldFocusMaterialPayloadFacet,
  WorldFocusValidityFacet,
} from '../../model/world-focus-basis';
import {
  WorldFocusQualifier,
  WorldFocusQualifierGroup,
} from './world-focus-qualifiers';

type QualifierDescriptor = Readonly<{
  axis: 'freshness' | 'validity' | 'coverage' | 'material-payload';
  state: string;
  label: string;
}>;

type WorldFocusBasisPresentationProps = Readonly<{
  freshness?: WorldFocusFreshnessFacet | null;
  validity?: WorldFocusValidityFacet | null;
  coverage?: WorldFocusCoverageFacet | null;
  materialPayload?: WorldFocusMaterialPayloadFacet | null;
}>;

export function WorldFocusBasisPresentation({
  freshness = null,
  validity = null,
  coverage = null,
  materialPayload = null,
}: WorldFocusBasisPresentationProps) {
  const { t } = useTranslation('common');
  const qualifiers: QualifierDescriptor[] = [];

  if (freshness?.status === 'stale') {
    qualifiers.push({
      axis: 'freshness',
      state: 'stale',
      label: t(($) => $.common.worldFocus.presentation.basis.freshness.stale),
    });
  } else if (freshness?.status === 'unknown') {
    qualifiers.push({
      axis: 'freshness',
      state: 'unknown',
      label: t(($) => $.common.worldFocus.presentation.basis.freshness.unknown),
    });
  }

  if (validity !== null && validity.status !== 'current') {
    qualifiers.push({
      axis: 'validity',
      state: validity.status,
      label: t(($) => $.common.worldFocus.presentation.basis.validity[validity.status]),
    });
  }

  if (coverage !== null && coverage.status !== 'complete') {
    qualifiers.push({
      axis: 'coverage',
      state: coverage.status,
      label: t(($) => $.common.worldFocus.presentation.basis.coverage[coverage.status]),
    });
  }

  if (materialPayload?.status === 'retired') {
    qualifiers.push({
      axis: 'material-payload',
      state: 'retired',
      label: t(($) => $.common.worldFocus.presentation.basis.material.retired),
    });
  }

  if (qualifiers.length === 0) return null;

  return (
    <WorldFocusQualifierGroup
      aria-label={t(($) => $.common.worldFocus.presentation.qualifiers.basis)}
      data-world-focus-basis-presentation="true"
    >
      {qualifiers.map((qualifier) => (
        <WorldFocusQualifier
          axis={qualifier.axis}
          state={qualifier.state}
          key={`${qualifier.axis}:${qualifier.state}`}
        >
          {qualifier.label}
        </WorldFocusQualifier>
      ))}
    </WorldFocusQualifierGroup>
  );
}
