import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import {
  startWorldFocusPerformanceSpan,
  WORLD_FOCUS_PERFORMANCE_MEASURES,
  type WorldFocusPerformanceSpan,
} from '../application/world-focus-foundation';
import type { WorldFocusWorld } from '../model/world-focus-fixtures';
import { WORLD_FOCUS_GEOMETRY } from '../model/world-focus-geometry';
import type { WorldFocusIdentityDescriptor } from '../model/world-focus-identity';
import type {
  WorldFocusFeatureAvailability,
  WorldFocusShellStatus,
} from '../model/world-focus-platform';
import {
  WORLD_FOCUS_REGION,
  WORLD_FOCUS_STRUCTURE_VERSION,
} from '../model/world-focus-structure';
import {
  clearWorldFocusEntry,
  readWorldFocusEntry,
  type WorldFocusEntrySource,
} from '../model/world-focus-transition';
import { WORLD_FOCUS_VISUAL_VERSION } from '../model/world-focus-visual';
import { WorldFocusAdaptiveComposition } from './world-focus-adaptive-composition';
import {
  WorldFocusCompositionCustomizationProvider,
  WorldFocusCompositionCustomizeInvoke,
} from './world-focus-composition-customization-context';
import { WorldFocusContext } from './world-focus-context';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import {
  WorldFocusDanteConversationPresentationController,
} from './world-focus-dante-conversation';
import {
  WorldFocusDanteConversationProvider,
} from './world-focus-dante-conversation-context';
import {
  WorldFocusDanteEntryProvider,
  WorldFocusDanteInvoke,
  useWorldFocusDanteEntry,
} from './world-focus-dante-entry';
import { WorldFocusDanteInsightProvider } from './world-focus-dante-insight-context';
import { WorldFocusRouteSurfaceLayer } from './world-focus-route-surface-layer';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusVisualFrame } from './world-focus-visual-frame';
import { WorldFocusWorkspace } from './world-focus-workspace';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';
import './world-focus.css';
import './world-focus-composition-customization.css';
import './world-focus-dante-conversation.css';
import './world-focus-dante-entry.css';
import './world-focus-dante-insight.css';
import './world-focus-visual-frame-v4.css';
import './world-focus-states.css';

export type WorldFocusCloseRequest = Readonly<{
  preferHistory: boolean;
}>;

export type { WorldFocusShellStatus } from '../model/world-focus-platform';

const PRE_BACKEND_DANTE_ENTRY_AVAILABILITY: WorldFocusFeatureAvailability =
  Object.freeze({ status: 'available' });

type WorldFocusPageProps = Readonly<{
  world: WorldFocusWorld;
  identity: WorldFocusIdentityDescriptor;
  source: WorldFocusEntrySource;
  status?: WorldFocusShellStatus;
  onClose: (request: WorldFocusCloseRequest) => void;
}>;

type WorldFocusWorkspaceExperienceProps = Readonly<{
  identity: WorldFocusIdentityDescriptor;
  status: WorldFocusShellStatus;
  routeSurfaceHost: HTMLElement | null;
  onRequestWorldClose: () => void;
}>;

type WorldFocusDanteConversationOwnerProps = Readonly<{
  worldId: WorldFocusIdentityDescriptor['id'];
  children: ReactNode;
}>;

function WorldFocusDanteConversationOwner({
  worldId,
  children,
}: WorldFocusDanteConversationOwnerProps) {
  const { restoreInvokerFocus } = useWorldFocusDanteEntry();

  return (
    <WorldFocusDanteConversationProvider
      worldId={worldId}
      restoreInvokerFocus={restoreInvokerFocus}
    >
      {children}
    </WorldFocusDanteConversationProvider>
  );
}

function WorldFocusWorkspaceExperience({
  identity,
  status,
  routeSurfaceHost,
  onRequestWorldClose,
}: WorldFocusWorkspaceExperienceProps) {
  const { requestEscape } = useWorldFocusWorkspace();
  const registry = getCoreWorldFocusSurfaceRegistry();

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key !== 'Escape' || event.defaultPrevented) {
        return;
      }

      const disposition = requestEscape();
      event.preventDefault();

      if (disposition === 'no-surface') {
        onRequestWorldClose();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [onRequestWorldClose, requestEscape]);

  return (
    <WorldFocusCompositionCustomizationProvider
      worldId={identity.id}
      worldLabel={identity.label}
    >
      <WorldFocusDanteEntryProvider
        worldId={identity.id}
        worldLabel={identity.label}
        availability={PRE_BACKEND_DANTE_ENTRY_AVAILABILITY}
      >
        <WorldFocusDanteConversationOwner worldId={identity.id}>
          <WorldFocusDanteInsightProvider worldId={identity.id}>
            <WorldFocusWorkspace
              worldLabel={identity.label}
              status={status}
              context={<WorldFocusContext identity={identity} />}
              surfaces={
                <>
                  <WorldFocusCompositionCustomizeInvoke />
                  <WorldFocusDanteInvoke />
                  <WorldFocusDanteConversationPresentationController>
                    <WorldFocusSurfaceLayer registry={registry} />
                    <WorldFocusRouteSurfaceLayer
                      registry={registry}
                      host={routeSurfaceHost}
                    />
                  </WorldFocusDanteConversationPresentationController>
                </>
              }
            >
              <WorldFocusAdaptiveComposition worldId={identity.id} />
            </WorldFocusWorkspace>
          </WorldFocusDanteInsightProvider>
        </WorldFocusDanteConversationOwner>
      </WorldFocusDanteEntryProvider>
    </WorldFocusCompositionCustomizationProvider>
  );
}

export function WorldFocusPage({
  world,
  identity,
  source,
  status = 'ready',
  onClose,
}: WorldFocusPageProps) {
  const { t } = useTranslation('common');
  const mainRef = useRef<HTMLElement | null>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  const performanceSpanRef = useRef<WorldFocusPerformanceSpan | null>(null);
  const [routeSurfaceHost, setRouteSurfaceHost] =
    useState<HTMLDivElement | null>(null);
  const entry = useMemo(
    () => readWorldFocusEntry(identity.id, source),
    [identity.id, source],
  );

  const closeRequest = useMemo<WorldFocusCloseRequest>(
    () => ({ preferHistory: entry !== null }),
    [entry],
  );
  const requestWorldClose = useCallback(
    () => onClose(closeRequest),
    [closeRequest, onClose],
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
    const span = startWorldFocusPerformanceSpan(
      WORLD_FOCUS_PERFORMANCE_MEASURES.openToUsable,
    );
    performanceSpanRef.current = span;

    return () => {
      if (performanceSpanRef.current === span) {
        span.cancel();
        performanceSpanRef.current = null;
      }
    };
  }, [identity.id]);

  useEffect(() => {
    if (status !== 'ready') {
      return;
    }

    performanceSpanRef.current?.finish();
    performanceSpanRef.current = null;
  }, [identity.id, status]);

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

  return (
    <main
      ref={mainRef}
      className="world-focus-shell"
      data-world-focus-region={WORLD_FOCUS_REGION.shell}
      data-world-focus-id={identity.id}
      data-world-focus-source={source}
      data-world-focus-status={status}
      data-world-focus-structure-version={WORLD_FOCUS_STRUCTURE_VERSION}
      data-world-focus-geometry-version={WORLD_FOCUS_GEOMETRY.version}
      data-world-focus-visual-version={WORLD_FOCUS_VISUAL_VERSION}
      data-entry-origin={entry === null ? 'fallback' : 'live'}
      aria-label={t(($) => $.common.worldFocus.mainLabel, {
        world: identity.label,
      })}
      style={geometryStyle}
      tabIndex={-1}
    >
      <WorldFocusVisualFrame world={world} />

      <div
        className="world-focus-shell-controls"
        data-world-focus-region={WORLD_FOCUS_REGION.shellControls}
        aria-hidden="true"
      />

      <div
        ref={setRouteSurfaceHost}
        className="world-focus-route-surface-host"
        data-world-focus-route-surface-host="true"
      />

      <WorldFocusWorkspaceHost key={identity.id} worldId={identity.id}>
        <WorldFocusWorkspaceExperience
          identity={identity}
          status={status}
          routeSurfaceHost={routeSurfaceHost}
          onRequestWorldClose={requestWorldClose}
        />
      </WorldFocusWorkspaceHost>
    </main>
  );
}
