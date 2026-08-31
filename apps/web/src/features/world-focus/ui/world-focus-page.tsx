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

const GUIDE_LINE_ROLES = ['outer', 'origin', 'inner'] as const;

type GuideLineRole = (typeof GUIDE_LINE_ROLES)[number];

function WorldFocusEllipseGuides() {
  return (
    <svg
      className="world-focus-ellipse-guides"
      aria-hidden="true"
      focusable="false"
    >
      {GUIDE_LINE_ROLES.map((role: GuideLineRole) => {
        const geometry = WORLD_FOCUS_GEOMETRY.guideEllipses[role];

        return (
          <ellipse
            key={role}
            data-guide-line={role}
            cx="50%"
            cy="50%"
            rx={geometry.rx}
            ry={geometry.ry}
          />
        );
      })}
    </svg>
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
      data-world-focus-id={world.id}
      data-world-focus-source={source}
      data-world-focus-status={status}
      data-world-focus-geometry-version={WORLD_FOCUS_GEOMETRY.version}
      data-entry-origin={entry === null ? 'fallback' : 'live'}
      aria-label={t(($) => $.common.worldFocus.mainLabel, { world: label })}
      style={geometryStyle}
      tabIndex={-1}
    >
      <h1 className="world-focus-visually-hidden">{label}</h1>

      <WorldFocusEllipseGuides />

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
        data-world-focus-region="workspace"
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
