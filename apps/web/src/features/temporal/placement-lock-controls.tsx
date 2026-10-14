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
}: Readonly<{
  scheduleRef: string;
  variant?: 'text' | 'icon';
  onLockChanged?: (locked: boolean) => void;
}>) {
  const [loaded, setLoaded] = useState<Readonly<{
    scheduleRef: string;
    value: PlacementLockState | null;
  }> | null>(null);
  const [pending, setPending] = useState(false);
  const [readError, setReadError] = useState<Readonly<{
    scheduleRef: string;
    message: string;
  }> | null>(null);
  const [mutationError, setMutationError] = useState<Readonly<{
    scheduleRef: string;
    message: string;
  }> | null>(null);
  const state = loaded?.scheduleRef === scheduleRef ? loaded.value : null;
  const error =
    (mutationError?.scheduleRef === scheduleRef
      ? mutationError.message
      : null) ??
    (readError?.scheduleRef === scheduleRef ? readError.message : null);
  const onLockChangedRef = useRef(onLockChanged);

  useEffect(() => {
    onLockChangedRef.current = onLockChanged;
  }, [onLockChanged]);

  useEffect(() => {
    let active = true;
    void source.get(scheduleRef).then(
      (value) => {
        if (active) {
          setLoaded({ scheduleRef, value });
          setReadError(null);
          onLockChangedRef.current?.(value.locked);
        }
      },
      () => {
        if (active)
          setReadError({
            scheduleRef,
            message: 'Impossibile leggere il blocco spostamenti.',
          });
      },
    );
    return () => {
      active = false;
    };
  }, [scheduleRef]);

  const toggle = async () => {
    if (state === null || pending) return;
    setPending(true);
    setMutationError(null);
    try {
      const next = await source.set(
        scheduleRef,
        !state.locked,
        state.revision || null,
      );
      setLoaded({ scheduleRef, value: next });
      onLockChanged?.(next.locked);
      invalidateTemporalTimelineRead();
    } catch {
      setMutationError({
        scheduleRef,
        message: 'Non è stato possibile cambiare il blocco. Riprova.',
      });
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
          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <rect x="5" y="10" width="14" height="11" rx="2" />
            <path
              d={
                state?.locked
                  ? 'M8 10V7a4 4 0 0 1 8 0v3'
                  : 'M8 10V7a4 4 0 0 1 7.5-1.9'
              }
            />
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
