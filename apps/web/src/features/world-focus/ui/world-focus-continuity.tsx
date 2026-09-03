import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusContinuityReader } from '../application/world-focus-continuity';
import { readWorldFocusContinuity } from '../application/world-focus-continuity-runtime';
import { WorldFocusLatestReadCoordinator } from '../application/world-focus-foundation';
import type {
  WorldFocusContinuityPresentationState,
  WorldFocusContinuityReadResult,
} from '../model/world-focus-continuity';
import type { WorldFocusId } from '../model/world-focus-identity';
import {
  WorldFocusPresentationSection,
  WorldFocusPresentationState,
} from './presentation/world-focus-presentation-primitives';

type WorldFocusContinuitySettledState =
  | Readonly<{ status: 'error' }>
  | WorldFocusContinuityReadResult;

type WorldFocusContinuityProps = Readonly<{
  worldId: WorldFocusId;
  reader?: WorldFocusContinuityReader;
}>;

export function WorldFocusContinuity({
  worldId,
  reader = readWorldFocusContinuity,
}: WorldFocusContinuityProps) {
  const { t } = useTranslation('common');
  const [coordinator] = useState(() => new WorldFocusLatestReadCoordinator());
  const [retryGeneration, setRetryGeneration] = useState(0);
  const [settled, setSettled] = useState<Readonly<{
    requestKey: string;
    state: WorldFocusContinuitySettledState;
  }> | null>(null);
  const requestKey = `${worldId}:${retryGeneration}`;
  const state =
    settled?.requestKey === requestKey
      ? settled.state
      : ({ status: 'loading' } as const);
  const stateLabels: Readonly<
    Record<WorldFocusContinuityPresentationState, string>
  > = {
    active: t(($) => $.common.worldFocus.continuity.states.active),
    paused: t(($) => $.common.worldFocus.continuity.states.paused),
    blocked: t(($) => $.common.worldFocus.continuity.states.blocked),
  };

  useEffect(() => {
    const lease = coordinator.begin();

    void reader(worldId, lease.signal)
      .then((result) => {
        lease.commit(() => setSettled({ requestKey, state: result }));
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

  if (state.status === 'empty') return null;
  const retry = () => setRetryGeneration((generation) => generation + 1);
  const title = t(($) => $.common.worldFocus.continuity.title);

  if (state.status === 'loading') {
    return (
      <WorldFocusPresentationSection
        className="world-focus-continuity world-focus-continuity-loading"
        title={title}
        aria-busy="true"
        data-world-focus-continuity-status="loading"
      >
        <p className="world-focus-continuity-status" role="status">
          {t(($) => $.common.worldFocus.continuity.loading)}
        </p>
      </WorldFocusPresentationSection>
    );
  }

  if (state.status === 'error' || state.status === 'unavailable') {
    const retryable = state.status === 'error' || state.retryable;
    return (
      <WorldFocusPresentationSection
        className="world-focus-continuity world-focus-continuity-degraded"
        title={title}
        data-world-focus-continuity-status={state.status}
      >
        <div className="world-focus-continuity-degraded-row">
          <p className="world-focus-continuity-status" role="alert">
            {state.status === 'error'
              ? t(($) => $.common.worldFocus.continuity.error)
              : t(($) => $.common.worldFocus.continuity.unavailable)}
          </p>
          {retryable ? (
            <button
              className="world-focus-continuity-retry"
              type="button"
              onClick={retry}
            >
              {t(($) => $.common.worldFocus.continuity.retry)}
            </button>
          ) : null}
        </div>
      </WorldFocusPresentationSection>
    );
  }

  const projection = state.projection;
  const qualification =
    state.status === 'partial'
      ? t(($) => $.common.worldFocus.continuity.partial)
      : state.status === 'stale'
        ? t(($) => $.common.worldFocus.continuity.stale)
        : null;

  return (
    <WorldFocusPresentationSection
      className="world-focus-continuity"
      title={title}
      qualification={qualification}
      data-world-focus-continuity-status={state.status}
    >
      <ul className="world-focus-continuity-list">
        {projection.orderedItems.map((item) => (
          <li
            className="world-focus-continuity-item world-focus-presentation-row"
            data-world-focus-continuity-state={item.presentationState}
            key={item.key}
          >
            <div className="world-focus-continuity-item-copy world-focus-presentation-row-copy">
              <p className="world-focus-continuity-item-title world-focus-presentation-row-title">
                {item.title}
              </p>
              <p className="world-focus-continuity-item-meta world-focus-presentation-row-meta">
                <span>{item.context}</span>
                <span aria-hidden="true">·</span>
                <span>{item.checkpoint}</span>
              </p>
            </div>
            <WorldFocusPresentationState state={item.presentationState}>
              {stateLabels[item.presentationState]}
            </WorldFocusPresentationState>
          </li>
        ))}
      </ul>
    </WorldFocusPresentationSection>
  );
}
