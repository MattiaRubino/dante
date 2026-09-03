import { useTranslation } from 'react-i18next';

import type { WorldFocusSyncPresentation } from '../../model/world-focus-sync';
import {
  WorldFocusQualifier,
  WorldFocusQualifierGroup,
} from './world-focus-qualifiers';

type QualifierDescriptor = Readonly<{
  axis: 'connectivity' | 'replay' | 'provider-delivery' | 'request-timing';
  state: string;
  label: string;
}>;

type WorldFocusSyncStatusProps = Readonly<{
  sync: WorldFocusSyncPresentation;
}>;

export function WorldFocusSyncStatus({ sync }: WorldFocusSyncStatusProps) {
  const { t } = useTranslation('common');
  const qualifiers: QualifierDescriptor[] = [];

  if (sync.connectivity === 'offline') {
    qualifiers.push({
      axis: 'connectivity',
      state: 'offline',
      label: t(($) => $.common.worldFocus.presentation.sync.offline),
    });
  }

  if (sync.replay === 'pending') {
    qualifiers.push({
      axis: 'replay',
      state: 'pending',
      label: t(($) => $.common.worldFocus.presentation.sync.replayPending),
    });
  }

  if (sync.providerDelivery !== 'nominal') {
    qualifiers.push({
      axis: 'provider-delivery',
      state: sync.providerDelivery,
      label:
        sync.providerDelivery === 'lagging'
          ? t(($) => $.common.worldFocus.presentation.sync.providerLagging)
          : t(($) => $.common.worldFocus.presentation.sync.providerUnknown),
    });
  }

  if (sync.requestTiming !== 'within-window') {
    qualifiers.push({
      axis: 'request-timing',
      state: sync.requestTiming,
      label:
        sync.requestTiming === 'timed-out'
          ? t(($) => $.common.worldFocus.presentation.sync.timedOut)
          : t(($) => $.common.worldFocus.presentation.sync.timingUnknown),
    });
  }

  if (qualifiers.length === 0) return null;

  return (
    <WorldFocusQualifierGroup
      aria-label={t(($) => $.common.worldFocus.presentation.qualifiers.sync)}
      data-world-focus-sync-presentation="true"
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
