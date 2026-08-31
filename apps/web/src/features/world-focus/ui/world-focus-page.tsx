import { useCallback, useEffect, useMemo, useRef, useState, type CSSProperties } from 'react';
import { useTranslation } from 'react-i18next';

import {
  clearWorldFocusEntry,
  readWorldFocusEntry,
  type WorldFocusEntrySource,
} from '../model/world-focus-transition';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import { WorldFocusEntryEffect } from './world-focus-entry-effect';
import './world-focus.css';
import './world-focus-states.css';

export type WorldFocusCloseRequest = Readonly<{
  preferHistory: boolean;
}>;

export type WorldFocusShellStatus =
  | 'loading'
  | 'ready'
  | 'error'
  | 'unavailable';

type WorldFocusPageProps = Readonly<{
  world: WorldFocusWorld;
  source: WorldFocusEntrySource;
  status?: WorldFocusShellStatus;
  onClose: (request: WorldFocusCloseRequest) => void;
}>;

type EntryPhase = 'entering' | 'settled';

function prefersReducedMotion() {
  return (
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches
  );
}

export function WorldFocusPage({
  world,
  source,
  status = 'ready',
  onClose,
}: WorldFocusPageProps) {
  const { t } = useTranslation('common');
  const mainRef = useRef<HTMLElement | null>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  const [entry] = useState(() => readWorldFocusEntry(world.id, source));
  const [entryPhase, setEntryPhase] = useState<EntryPhase>(() =>
    entry !== null && !prefersReducedMotion() ? 'entering' : 'settled',
  );

  const label = t(($) => $.common.worldFocus.worlds[world.id].label);
  const description = t(
    ($) => $.common.worldFocus.worlds[world.id].description,
  );
  const statusMessage =
    status === 'loading'
      ? t(($) => $.common.worldFocus.states.loading, { world: label })
      : status === 'error'
        ? t(($) => $.common.worldFocus.states.error, { world: label })
        : status === 'unavailable'
          ? t(($) => $.common.worldFocus.states.unavailable, { world: label })
          : null;
  const closeRequest = useMemo<WorldFocusCloseRequest>(
    () => ({ preferHistory: entry !== null }),
    [entry],
  );
  const settleEntry = useCallback(() => setEntryPhase('settled'), []);

  const style = {
    '--world-focus-accent': world.accent,
    '--world-focus-ambient-intensity': String(world.theme.ambientIntensity),
    '--world-focus-particle-density': String(world.theme.particleDensity),
  } as CSSProperties;

  useEffect(() => {
    if (entry !== null) {
      clearWorldFocusEntry(entry.token);
    }
  }, [entry]);

  useEffect(() => {
    previousFocusRef.current =
      document.activeElement instanceof HTMLElement
        ? document.activeElement
        : null;

    const root = document.documentElement;
    const previousOverflow = root.style.overflow;
    root.style.overflow = 'hidden';
    mainRef.current?.focus({ preventScroll: true });

    return () => {
      root.style.overflow = previousOverflow;
      const previousFocus = previousFocusRef.current;
      queueMicrotask(() => {
        if (previousFocus?.isConnected === true) {
          previousFocus.focus({ preventScroll: true });
        }
      });
    };
  }, []);

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') {
        return;
      }

      event.preventDefault();
      onClose(closeRequest);
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [closeRequest, onClose]);

  return (
    <main
      ref={mainRef}
      className="world-focus-shell"
      data-world-focus-id={world.id}
      data-world-focus-source={source}
      data-world-focus-status={status}
      data-entry-origin={entry === null ? 'fallback' : 'live'}
      data-entry-phase={entryPhase}
      data-motion={world.theme.motionCharacter}
      data-texture={world.theme.texture}
      aria-label={t(($) => $.common.worldFocus.mainLabel, { world: label })}
      style={style}
      tabIndex={-1}
    >
      <div className="world-focus-ambient" aria-hidden="true">
        <span className="world-focus-ambient-field" />
        <span className="world-focus-ambient-stars" />
      </div>

      {entry !== null && entryPhase === 'entering' ? (
        <WorldFocusEntryEffect
          entry={entry}
          world={world}
          onComplete={settleEntry}
        />
      ) : null}

      <button
        className="world-focus-back"
        type="button"
        onClick={() => onClose(closeRequest)}
        aria-label={t(($) => $.common.worldFocus.back)}
      >
        <span aria-hidden="true">←</span>
        <span>{t(($) => $.common.worldFocus.back)}</span>
      </button>

      <header className="world-focus-identity">
        <span className="world-focus-kicker">
          {t(($) => $.common.worldFocus.kicker)}
        </span>
        <h1>{label}</h1>
        <p>{description}</p>
      </header>

      <section
        className="world-focus-canvas"
        aria-label={t(($) => $.common.worldFocus.canvasLabel, {
          world: label,
        })}
        aria-busy={status === 'loading' ? true : undefined}
      >
        <div className="world-focus-canvas-boundary" aria-hidden="true" />
        {statusMessage === null ? null : (
          <p
            className="world-focus-state"
            role={status === 'loading' ? 'status' : 'alert'}
          >
            {statusMessage}
          </p>
        )}
      </section>
    </main>
  );
}
