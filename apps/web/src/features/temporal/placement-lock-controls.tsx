import { useEffect, useRef, useState } from 'react';

import {
  createRemotePlacementLockDataSource,
  type PlacementLockState,
} from './remote-placement-lock-data-source';
import { invalidateTemporalTimelineRead } from './timeline-invalidation';

const source = createRemotePlacementLockDataSource();

export function PlacementLockControls({
  scheduleRef,
  variant = 'text',
  onLockChanged,
}: Readonly<{ scheduleRef: string; variant?: 'text' | 'icon'; onLockChanged?: (locked: boolean) => void }>) {
  const [state, setState] = useState<PlacementLockState | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const onLockChangedRef = useRef(onLockChanged);
  onLockChangedRef.current = onLockChanged;

  useEffect(() => {
    let active = true;
    setState(null);
    setError(null);
    void source.get(scheduleRef).then(
      (value) => {
        if (active) {
          setState(value);
          onLockChangedRef.current?.(value.locked);
        }
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
      onLockChanged?.(next.locked);
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
          <svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor"
            strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
            <rect x="5" y="10" width="14" height="11" rx="2" />
            <path d={state?.locked ? 'M8 10V7a4 4 0 0 1 8 0v3' : 'M8 10V7a4 4 0 0 1 7.5-1.9'} />
          </svg>
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
