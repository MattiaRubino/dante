import { useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  readWorldFocusAdaptiveCompositionSnapshot,
  resolveWorldFocusAdaptiveComposition,
  type WorldFocusAdaptiveCompositionReader,
  type WorldFocusAdaptiveCompositionSnapshot,
} from '../application/world-focus-adaptive-composition';
import { WorldFocusLatestReadCoordinator } from '../application/world-focus-foundation';
import type { WorldFocusId } from '../model/world-focus-identity';
import { WorldFocusCompositionHost } from './world-focus-composition-host';
import { useWorldFocusCompositionCustomization } from './world-focus-composition-customization-context';
import { createCoreWorldFocusModuleRegistry } from './world-focus-core-composition';

type WorldFocusAdaptiveCompositionState =
  | Readonly<{ status: 'loading' }>
  | Readonly<{ status: 'error' }>
  | Readonly<{ status: 'ready'; snapshot: WorldFocusAdaptiveCompositionSnapshot }>;

type WorldFocusAdaptiveCompositionProps = Readonly<{
  worldId: WorldFocusId;
  reader?: WorldFocusAdaptiveCompositionReader;
}>;

export function WorldFocusAdaptiveComposition({
  worldId,
  reader = readWorldFocusAdaptiveCompositionSnapshot,
}: WorldFocusAdaptiveCompositionProps) {
  const { t } = useTranslation('common');
  const customization = useWorldFocusCompositionCustomization();
  const [coordinator] = useState(() => new WorldFocusLatestReadCoordinator());
  const [retryGeneration, setRetryGeneration] = useState(0);
  const [settled, setSettled] = useState<Readonly<{
    requestKey: string;
    state: WorldFocusAdaptiveCompositionState;
  }> | null>(null);
  const requestKey = `${worldId}:${retryGeneration}`;
  const state = useMemo<WorldFocusAdaptiveCompositionState>(
    () =>
      settled?.requestKey === requestKey
        ? settled.state
        : ({ status: 'loading' } as const),
    [requestKey, settled],
  );

  useEffect(() => {
    const lease = coordinator.begin();

    void reader(worldId, lease.signal)
      .then((snapshot) => {
        lease.commit(() =>
          setSettled({ requestKey, state: { status: 'ready', snapshot } }),
        );
      })
      .catch(() => {
        if (lease.signal.aborted) return;
        lease.commit(() =>
          setSettled({ requestKey, state: { status: 'error' } }),
        );
      })
      .finally(() => lease.release());

    return () => coordinator.cancelCurrent();
  }, [coordinator, reader, requestKey, worldId]);

  const resolution = useMemo(
    () =>
      state.status === 'ready'
        ? resolveWorldFocusAdaptiveComposition(
            state.snapshot,
            customization.acceptedConfig,
          )
        : null,
    [customization.acceptedConfig, state],
  );
  const registry = useMemo(
    () =>
      state.status === 'ready'
        ? createCoreWorldFocusModuleRegistry(state.snapshot)
        : null,
    [state],
  );

  if (state.status === 'loading') {
    return (
      <div
        className="world-focus-composition"
        data-world-focus-composition-count="0"
        data-world-focus-composition-status="loading"
        aria-busy="true"
      />
    );
  }

  if (state.status === 'error') {
    return (
      <section
        className="world-focus-composition world-focus-composition-runtime-state"
        data-world-focus-composition-count="0"
        data-world-focus-composition-status="error"
        role="alert"
      >
        <p>{t(($) => $.common.worldFocus.surfaces.error)}</p>
        <button
          type="button"
          onClick={() => setRetryGeneration((generation) => generation + 1)}
        >
          {t(($) => $.common.worldFocus.states.retry)}
        </button>
      </section>
    );
  }

  if (resolution === null || registry === null) {
    throw new Error('World Focus adaptive composition ready state is incomplete');
  }

  return (
    <WorldFocusCompositionHost
      worldId={worldId}
      entries={resolution.plan.entries}
      registry={registry}
    />
  );
}
