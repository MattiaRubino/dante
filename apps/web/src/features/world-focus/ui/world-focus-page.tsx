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

type PortalParticle = Readonly<{
  x: number;
  y: number;
  size: number;
  alpha: number;
  hot?: boolean;
}>;

const PORTAL_PARTICLES: readonly PortalParticle[] = [
  { x: 15, y: 36, size: 3, alpha: 0.86 },
  { x: 18, y: 28, size: 2, alpha: 0.58 },
  { x: 21, y: 20, size: 4, alpha: 0.84 },
  { x: 27, y: 14, size: 2, alpha: 0.68 },
  { x: 35, y: 10, size: 3, alpha: 0.72 },
  { x: 44, y: 7, size: 2, alpha: 0.52 },
  { x: 55, y: 8, size: 3, alpha: 0.76, hot: true },
  { x: 64, y: 11, size: 2, alpha: 0.6, hot: true },
  { x: 73, y: 16, size: 4, alpha: 0.88, hot: true },
  { x: 81, y: 23, size: 2, alpha: 0.64, hot: true },
  { x: 85, y: 32, size: 3, alpha: 0.82, hot: true },
  { x: 89, y: 42, size: 2, alpha: 0.58, hot: true },
  { x: 90, y: 52, size: 4, alpha: 0.88, hot: true },
  { x: 87, y: 63, size: 2, alpha: 0.56, hot: true },
  { x: 82, y: 72, size: 3, alpha: 0.82, hot: true },
  { x: 75, y: 81, size: 2, alpha: 0.62, hot: true },
  { x: 66, y: 87, size: 4, alpha: 0.86, hot: true },
  { x: 56, y: 91, size: 2, alpha: 0.58 },
  { x: 45, y: 91, size: 3, alpha: 0.78 },
  { x: 35, y: 88, size: 2, alpha: 0.54 },
  { x: 26, y: 82, size: 4, alpha: 0.84 },
  { x: 19, y: 74, size: 2, alpha: 0.62 },
  { x: 14, y: 64, size: 3, alpha: 0.8 },
  { x: 11, y: 53, size: 2, alpha: 0.54 },
  { x: 12, y: 44, size: 4, alpha: 0.86 },
  { x: 24, y: 31, size: 2, alpha: 0.4 },
  { x: 31, y: 22, size: 2, alpha: 0.46 },
  { x: 69, y: 24, size: 2, alpha: 0.48, hot: true },
  { x: 78, y: 35, size: 3, alpha: 0.52, hot: true },
  { x: 78, y: 66, size: 2, alpha: 0.48, hot: true },
  { x: 68, y: 78, size: 3, alpha: 0.52, hot: true },
  { x: 31, y: 77, size: 2, alpha: 0.46 },
  { x: 22, y: 65, size: 3, alpha: 0.52 },
];

const PORTAL_RINGS = [0, 1, 2, 3, 4, 5] as const;
const PORTAL_NODES = ['north', 'east', 'south', 'west'] as const;

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

  const label = t(($) => $.common.worldFocus.worlds[world.id].label);
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
      data-entry-phase="end"
      data-entry-presentation="instant"
      aria-label={t(($) => $.common.worldFocus.mainLabel, { world: label })}
      style={style}
      tabIndex={-1}
    >
      <div className="world-focus-surface">
        <h1 className="world-focus-visually-hidden">{label}</h1>

        <div className="world-focus-cosmic-field" aria-hidden="true">
          <span className="world-focus-nebula world-focus-nebula--violet" />
          <span className="world-focus-nebula world-focus-nebula--ember" />
          <span className="world-focus-star-field" />
        </div>

        <div className="world-focus-surface-corners" aria-hidden="true">
          <span data-corner="north-west" />
          <span data-corner="north-east" />
          <span data-corner="south-east" />
          <span data-corner="south-west" />
        </div>

        <div className="world-focus-portal" aria-hidden="true">
          <span className="world-focus-portal-aura" />
          <span className="world-focus-portal-plasma world-focus-portal-plasma--mist" />
          <span className="world-focus-portal-plasma world-focus-portal-plasma--outer" />
          <span className="world-focus-portal-plasma world-focus-portal-plasma--inner" />

          {PORTAL_RINGS.map((ring) => (
            <span
              key={ring}
              className="world-focus-portal-ring"
              data-ring={ring}
            />
          ))}

          <svg
            className="world-focus-portal-geometry"
            viewBox="0 0 1000 1000"
            focusable="false"
          >
            <circle className="geometry-ring geometry-ring--outer" cx="500" cy="500" r="432" />
            <circle className="geometry-ring geometry-ring--mid" cx="500" cy="500" r="402" />
            <circle className="geometry-ring geometry-ring--inner" cx="500" cy="500" r="360" />
            <g className="geometry-spokes">
              <path d="M500 48V138M500 862v90M48 500h90M862 500h90" />
              <path d="M181 181l66 66M753 753l66 66M819 181l-66 66M247 753l-66 66" />
            </g>
            <g className="geometry-diamonds">
              <path d="M500 92l18 18-18 18-18-18z" />
              <path d="M908 500l-18 18-18-18 18-18z" />
              <path d="M500 908l18-18-18-18-18 18z" />
              <path d="M92 500l18 18 18-18-18-18z" />
              <path d="M211 211l12 22-22-12-12-22z" />
              <path d="M789 211l-12 22 22-12 12-22z" />
              <path d="M789 789l-12-22 22 12 12 22z" />
              <path d="M211 789l12-22-22 12-12 22z" />
            </g>
          </svg>

          <div className="world-focus-portal-nodes">
            {PORTAL_NODES.map((node) => (
              <span key={node} className="world-focus-portal-node" data-node={node}>
                <i />
              </span>
            ))}
          </div>

          <div className="world-focus-portal-particles">
            {PORTAL_PARTICLES.map((particle, index) => (
              <span
                key={index}
                className="world-focus-portal-particle"
                data-hot={particle.hot ? 'true' : 'false'}
                style={
                  {
                    '--particle-x': `${particle.x}%`,
                    '--particle-y': `${particle.y}%`,
                    '--particle-size': `${particle.size}px`,
                    '--particle-alpha': String(particle.alpha),
                  } as CSSProperties
                }
              />
            ))}
          </div>

          <span className="world-focus-portal-void" />
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

        <section
          className="world-focus-workspace"
          aria-label={t(($) => $.common.worldFocus.canvasLabel, {
            world: label,
          })}
          aria-busy={status === 'loading' ? true : undefined}
        >
          {statusMessage === null ? null : (
            <p
              className="world-focus-state"
              role={status === 'loading' ? 'status' : 'alert'}
            >
              {statusMessage}
            </p>
          )}
        </section>
      </div>
    </main>
  );
}
