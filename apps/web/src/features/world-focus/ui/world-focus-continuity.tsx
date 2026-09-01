import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

import {
  type WorldFocusContinuityReader,
} from '../application/world-focus-continuity';
import { readWorldFocusContinuity } from '../application/world-focus-continuity-runtime';
import { WorldFocusLatestReadCoordinator } from '../application/world-focus-foundation';
import type {
  WorldFocusContinuityPresentationState,
  WorldFocusContinuityReadResult,
} from '../model/world-focus-continuity';
import type { WorldFocusId } from '../model/world-focus-fixtures';

type WorldFocusContinuityViewState =
  | Readonly<{ status: 'loading' }>
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
  const [state, setState] = useState<WorldFocusContinuityViewState>({
    status: 'loading',
  });

  useEffect(() => {
    const lease = coordinator.begin();
    setState({ status: 'loading' });

    void reader(worldId, lease.signal)
      .then((result) => {
        lease.commit(() => setState(result));
      })
      .catch(() => {
        if (lease.signal.aborted) {
          return;
        }
        lease.commit(() => setState({ status: 'error' }));
      })
      .finally(() => lease.release());

    return () => coordinator.cancelCurrent();
  }, [coordinator, reader, retryGeneration, worldId]);

  if (state.status === 'empty') {
    return null;
  }

  const retry = () => setRetryGeneration((generation) => generation + 1);

  if (state.status === 'loading') {
    return (
      <section
        className="world-focus-continuity world-focus-continuity-loading"
        aria-busy="true"
        aria-labelledby="world-focus-continuity-title"
        data-world-focus-continuity-status="loading"
      >
        <h2
          className="world-focus-continuity-title"
          id="world-focus-continuity-title"
        >
          {t(($) => $.common.worldFocus.continuity.title)}
        </h2>
        <p className="world-focus-continuity-status" role="status">
          {t(($) => $.common.worldFocus.continuity.loading)}
        </p>
      </section>
    );
  }

  if (state.status === 'error' || state.status === 'unavailable') {
    const retryable = state.status === 'error' || state.retryable;
    return (
      <section
        className="world-focus-continuity world-focus-continuity-degraded"
        aria-labelledby="world-focus-continuity-title"
        data-world-focus-continuity-status={state.status}
      >
        <h2
          className="world-focus-continuity-title"
          id="world-focus-continuity-title"
        >
          {t(($) => $.common.worldFocus.continuity.title)}
        </h2>
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
      </section>
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
    <section
      className="world-focus-continuity"
      aria-labelledby="world-focus-continuity-title"
      data-world-focus-continuity-status={state.status}
    >
      <div className="world-focus-continuity-heading">
        <h2
          className="world-focus-continuity-title"
          id="world-focus-continuity-title"
        >
          {t(($) => $.common.worldFocus.continuity.title)}
        </h2>
        {qualification === null ? null : (
          <p className="world-focus-continuity-qualification" role="status">
            {qualification}
          </p>
        )}
      </div>

      <ul className="world-focus-continuity-list">
        {projection.orderedItems.map((item) => (
          <li
            className="world-focus-continuity-item"
            data-world-focus-continuity-state={item.presentationState}
            key={item.key}
          >
            <div className="world-focus-continuity-item-copy">
              <p className="world-focus-continuity-item-title">{item.title}</p>
              <p className="world-focus-continuity-item-meta">
                <span>{item.context}</span>
                <span aria-hidden="true">·</span>
                <span>{item.checkpoint}</span>
              </p>
            </div>
            <span className="world-focus-continuity-item-state">
              {getPresentationStateLabel(item.presentationState, t)}
            </span>
          </li>
        ))}
      </ul>
    </section>
  );
}

function getPresentationStateLabel(
  state: WorldFocusContinuityPresentationState,
  t: ReturnType<typeof useTranslation>['t'],
) {
  switch (state) {
    case 'active':
      return t(($) => $.common.worldFocus.continuity.states.active);
    case 'paused':
      return t(($) => $.common.worldFocus.continuity.states.paused);
    case 'blocked':
      return t(($) => $.common.worldFocus.continuity.states.blocked);
  }
}
