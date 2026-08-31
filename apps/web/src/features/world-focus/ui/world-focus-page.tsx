import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from 'react';
import { useTranslation } from 'react-i18next';

import {
  clearWorldFocusEntry,
  readWorldFocusEntry,
  type WorldFocusEntrySource,
} from '../model/world-focus-transition';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import './world-focus.css';

export type WorldFocusCloseRequest = Readonly<{
  preferHistory: boolean;
}>;

type WorldFocusPageProps = Readonly<{
  world: WorldFocusWorld;
  source: WorldFocusEntrySource;
  onClose: (request: WorldFocusCloseRequest) => void;
}>;

type WorldFocusGeometry = Readonly<{
  originX: number;
  originY: number;
  originScale: number;
  portalSize: number;
}>;

function clamp(value: number, minimum: number, maximum: number) {
  return Math.max(minimum, Math.min(maximum, value));
}

function resolveGeometry(
  origin:
    | Readonly<{ left: number; top: number; width: number; height: number }>
    | undefined,
): WorldFocusGeometry {
  const viewportWidth =
    typeof window === 'undefined' ? 1440 : Math.max(320, window.innerWidth);
  const viewportHeight =
    typeof window === 'undefined' ? 900 : Math.max(480, window.innerHeight);
  const portalSize = clamp(viewportWidth * 0.13, 156, 210);

  if (origin === undefined) {
    return {
      originX: 0,
      originY: 12,
      originScale: 0.58,
      portalSize,
    };
  }

  const originCenterX = origin.left + origin.width / 2;
  const originCenterY = origin.top + origin.height / 2;
  const targetCenterX = viewportWidth / 2;
  const targetCenterY = viewportHeight * 0.43;

  return {
    originX: originCenterX - targetCenterX,
    originY: originCenterY - targetCenterY,
    originScale: clamp(
      Math.max(origin.width, origin.height) / portalSize,
      0.14,
      1.1,
    ),
    portalSize,
  };
}

export function WorldFocusPage({
  world,
  source,
  onClose,
}: WorldFocusPageProps) {
  const { t } = useTranslation('common');
  const mainRef = useRef<HTMLElement | null>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  const [entry] = useState(() => readWorldFocusEntry(world.id, source));
  const geometry = useMemo(
    () => resolveGeometry(entry?.origin),
    [entry?.origin],
  );

  const label = t(($) => $.common.worldFocus.worlds[world.id].label);
  const description = t(
    ($) => $.common.worldFocus.worlds[world.id].description,
  );
  const closeRequest = useMemo<WorldFocusCloseRequest>(
    () => ({ preferHistory: entry !== null }),
    [entry],
  );

  const style = {
    '--world-focus-accent': world.accent,
    '--world-focus-ambient-intensity': String(world.theme.ambientIntensity),
    '--world-focus-particle-density': String(world.theme.particleDensity),
    '--world-focus-origin-x': `${geometry.originX}px`,
    '--world-focus-origin-y': `${geometry.originY}px`,
    '--world-focus-origin-scale': String(geometry.originScale),
    '--world-focus-portal-size': `${geometry.portalSize}px`,
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
      if (previousFocus?.isConnected === true) {
        previousFocus.focus({ preventScroll: true });
      }
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
      data-entry-origin={entry === null ? 'fallback' : 'live'}
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

      <div className="world-focus-portal" aria-hidden="true">
        <span className="world-focus-portal-halo" />
        {Array.from({ length: world.theme.orbitalDensity }, (_, index) => (
          <span
            key={index}
            className="world-focus-orbit"
            style={{ '--world-focus-orbit-index': index } as CSSProperties}
          />
        ))}
        <span className="world-focus-portal-core">
          <span />
        </span>
      </div>

      <section
        className="world-focus-canvas"
        aria-label={t(($) => $.common.worldFocus.canvasLabel, {
          world: label,
        })}
      >
        <div className="world-focus-canvas-boundary" aria-hidden="true" />
      </section>
    </main>
  );
}
