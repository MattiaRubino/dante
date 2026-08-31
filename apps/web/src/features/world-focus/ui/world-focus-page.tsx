import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from 'react';
import { useTranslation } from 'react-i18next';

import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import {
  WORLD_FOCUS_REGION,
  WORLD_FOCUS_STRUCTURE_VERSION,
} from '../model/world-focus-structure';
import { WORLD_FOCUS_VISUAL_VERSION } from '../model/world-focus-visual';
import {
  clearWorldFocusEntry,
  readWorldFocusEntry,
  type WorldFocusEntrySource,
} from '../model/world-focus-transition';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import { WorldFocusVisualFrame } from './world-focus-visual-frame';
import './world-focus.css';
import './world-focus-visual-frame-v4.css';
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

  const geometryStyle = {
    '--world-focus-workspace-inline-inset':
      WORLD_FOCUS_GEOMETRY.layout.workspaceInlineInset,
    '--world-focus-workspace-inline-inset-compact':
      WORLD_FOCUS_GEOMETRY.layout.compactWorkspaceInlineInset,
    '--world-focus-workspace-block-inset':
      WORLD_FOCUS_GEOMETRY.layout.workspaceBlockInset,
    '--world-focus-workspace-block-inset-compact':
      WORLD_FOCUS_GEOMETRY.layout.compactWorkspaceBlockInset,
    '--world-focus-accent': world.accent,
    '--world-focus-violet': '#7b4dff',
    '--world-focus-hot': '#ff8736',
    '--world-focus-ambient-intensity': String(world.theme.ambientIntensity),
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

    mainRef.current?.focus({ preventScroll: true });

    return () => {
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
      data-world-focus-region={WORLD_FOCUS_REGION.shell}
      data-world-focus-id={world.id}
      data-world-focus-source={source}
      data-world-focus-status={status}
      data-world-focus-structure-version={WORLD_FOCUS_STRUCTURE_VERSION}
      data-world-focus-geometry-version={WORLD_FOCUS_GEOMETRY.version}
      data-world-focus-visual-version={WORLD_FOCUS_VISUAL_VERSION}
      data-entry-origin={entry === null ? 'fallback' : 'live'}
      aria-label={t(($) => $.common.worldFocus.mainLabel, { world: label })}
      style={geometryStyle}
      tabIndex={-1}
    >
      <h1 className="world-focus-visually-hidden">{label}</h1>

      <WorldFocusVisualFrame world={world} />

      <div
        className="world-focus-shell-controls"
        data-world-focus-region={WORLD_FOCUS_REGION.shellControls}
        aria-hidden="true"
      />

      <section
        className="world-focus-workspace"
        data-world-focus-region={WORLD_FOCUS_REGION.workspace}
        aria-label={t(($) => $.common.worldFocus.canvasLabel, { world: label })}
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
    </main>
  );
}
