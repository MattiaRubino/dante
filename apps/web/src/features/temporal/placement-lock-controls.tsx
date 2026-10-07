import { useEffect, useState } from 'react';

import {
  createRemotePlacementLockDataSource,
  type PlacementLockState,
} from './remote-placement-lock-data-source';
import { invalidateTemporalTimelineRead } from './timeline-invalidation';

const source = createRemotePlacementLockDataSource();

export function PlacementLockControls({
  scheduleRef,
  variant = 'text',
}: Readonly<{ scheduleRef: string; variant?: 'text' | 'icon' }>) {
  const [state, setState] = useState<PlacementLockState | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setState(null);
    setError(null);
    void source.get(scheduleRef).then(
      (value) => {
        if (active) setState(value);
      },
      () => {
        if (active) setError('Impossibile leggere il blocco spostamenti.');
      },
    );
    return () => {
      active = false;
    };
  }, [scheduleRef]);

  const toggle = async () => {
    if (state === null || pending) return;
    setPending(true);
    setError(null);
    try {
      const next = await source.set(
        scheduleRef,
        !state.locked,
        state.revision || null,
      );
      setState(next);
      invalidateTemporalTimelineRead();
    } catch {
      setError('Non è stato possibile cambiare il blocco. Riprova.');
    } finally {
      setPending(false);
    }
  };

  return (
    <div className="timeline-placement-lock-controls">
      <button
        type="button"
        disabled={pending || state === null}
        onClick={() => void toggle()}
        aria-pressed={state?.locked ?? false}
        aria-label={
          state?.locked ? 'Sblocca spostamenti' : 'Blocca spostamenti'
        }
        title={state?.locked ? 'Sblocca spostamenti' : 'Blocca spostamenti'}
      >
        {variant === 'icon' ? (
          <span aria-hidden="true">{state?.locked ? '▣' : '▢'}</span>
        ) : state?.locked ? (
          'Sblocca spostamenti'
        ) : (
          'Blocca spostamenti'
        )}
      </button>
      {error ? <span role="alert">{error}</span> : null}
    </div>
  );
}
