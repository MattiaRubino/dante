import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import type {
  WorldFocusSurfaceDescriptor,
  WorldFocusWorkspaceState,
} from '../model/world-focus-workspace';
import type { WorldFocusSurfaceRendererProps } from './world-focus-surface-registry';
import { useWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation-context';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export const WORLD_FOCUS_DANTE_CONVERSATION_KIND = 'dante-conversation' as const;
export const WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID =
  'dante:conversation' as const;

export const WORLD_FOCUS_DANTE_CONVERSATION_PREFERENCES = [
  'adaptive',
  'focus',
] as const;

export type WorldFocusDanteConversationPreference =
  (typeof WORLD_FOCUS_DANTE_CONVERSATION_PREFERENCES)[number];

type WorldFocusDanteConversationFocusTransition = Readonly<{
  serial: number;
  action: 'maximize' | 'restore' | null;
}>;

type WorldFocusDanteConversationPresentationContextValue = Readonly<{
  preference: WorldFocusDanteConversationPreference;
  focusTransition: WorldFocusDanteConversationFocusTransition;
  requestMaximize: () => void;
  requestRestore: () => void;
}>;

const WorldFocusDanteConversationPresentationContext =
  createContext<WorldFocusDanteConversationPresentationContextValue | null>(
    null,
  );

type WorldFocusDanteConversationPresentationControllerProps = Readonly<{
  children: ReactNode;
}>;

type WorldFocusDanteConversationPresentationSessionProps = Readonly<{
  conversation: WorldFocusSurfaceDescriptor | null;
  children: ReactNode;
}>;

function withConversationPresentedAsSidecar(
  state: WorldFocusWorkspaceState,
): WorldFocusWorkspaceState {
  return Object.freeze({
    ...state,
    surfaces: Object.freeze(
      state.surfaces.map((surface) =>
        surface.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID
          ? Object.freeze({
              ...surface,
              presentation: 'sidecar' as const,
              blocksWorkspaceInteraction: false,
            })
          : surface,
      ),
    ),
  });
}

function WorldFocusDanteConversationPresentationSession({
  conversation,
  children,
}: WorldFocusDanteConversationPresentationSessionProps) {
  const { state, promoteSurface } = useWorldFocusWorkspace();
  const allocation = useWorldFocusWorkspaceAllocation();
  const [preference, setPreference] =
    useState<WorldFocusDanteConversationPreference>('adaptive');
  const [focusTransition, setFocusTransition] =
    useState<WorldFocusDanteConversationFocusTransition>(() =>
      Object.freeze({ serial: 0, action: null }),
    );

  const requestMaximize = useCallback(() => {
    setPreference('focus');
    setFocusTransition((current) =>
      Object.freeze({ serial: current.serial + 1, action: 'maximize' }),
    );
  }, []);

  const requestRestore = useCallback(() => {
    setPreference('adaptive');
    setFocusTransition((current) =>
      Object.freeze({ serial: current.serial + 1, action: 'restore' }),
    );
  }, []);

  useEffect(() => {
    if (conversation === null) {
      return;
    }

    const desiredPresentation = (() => {
      if (preference === 'focus') {
        return 'route' as const;
      }

      const sidecarPlan = resolveWorldFocusWorkspaceAllocation(
        withConversationPresentedAsSidecar(state),
        allocation.workspaceInlineSize,
      );
      const sidecarPlacement = sidecarPlan.placements.find(
        (placement) =>
          placement.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
      );

      return sidecarPlacement?.slot === 'sidecar'
        ? ('sidecar' as const)
        : ('route' as const);
    })();
    const desiredBlocksWorkspaceInteraction =
      desiredPresentation === 'route';

    if (
      conversation.presentation === desiredPresentation &&
      (conversation.blocksWorkspaceInteraction ?? false) ===
        desiredBlocksWorkspaceInteraction
    ) {
      return;
    }

    promoteSurface(
      conversation.instanceId,
      conversation.depth,
      desiredPresentation,
      {
        worldId: state.worldId,
        generation: state.generation,
      },
      desiredBlocksWorkspaceInteraction,
    );
  }, [
    allocation.workspaceInlineSize,
    conversation,
    preference,
    promoteSurface,
    state,
  ]);

  const value = useMemo<WorldFocusDanteConversationPresentationContextValue>(
    () => ({
      preference,
      focusTransition,
      requestMaximize,
      requestRestore,
    }),
    [focusTransition, preference, requestMaximize, requestRestore],
  );

  return (
    <WorldFocusDanteConversationPresentationContext.Provider value={value}>
      {children}
    </WorldFocusDanteConversationPresentationContext.Provider>
  );
}

/**
 * Owns only D2 presentation preference for the one contextual conversation
 * surface. It does not own messages, a conversation transcript, model output,
 * provider state, authorization, or durable DANTE Run lifetime.
 *
 * Adaptive mode asks the existing Workspace allocation resolver whether this
 * exact surface can consume a real sidecar slot. If not, the same surface is
 * promoted to the already-defined external `route` presentation. Route focus
 * explicitly blocks the rectangular World workspace; generic route surfaces do
 * not inherit that behavior. No viewport breakpoint or second responsive
 * policy is introduced here.
 *
 * The keyed session deliberately remounts across idle -> active -> idle. That
 * gives every newly opened conversation surface a fresh `adaptive` preference
 * without an effect-driven state reset, while sidecar/route changes within the
 * same open surface preserve the user's explicit maximize/restore preference.
 */
export function WorldFocusDanteConversationPresentationController({
  children,
}: WorldFocusDanteConversationPresentationControllerProps) {
  const { state } = useWorldFocusWorkspace();
  const topSurface = state.surfaces.at(-1) ?? null;
  const conversation =
    topSurface?.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID
      ? topSurface
      : null;

  return (
    <WorldFocusDanteConversationPresentationSession
      key={conversation === null ? 'idle' : 'active'}
      conversation={conversation}
    >
      {children}
    </WorldFocusDanteConversationPresentationSession>
  );
}

export function useWorldFocusDanteConversationPresentation(): WorldFocusDanteConversationPresentationContextValue {
  const value = useContext(WorldFocusDanteConversationPresentationContext);
  if (value === null) {
    throw new Error(
      'useWorldFocusDanteConversationPresentation must be used inside WorldFocusDanteConversationPresentationController',
    );
  }
  return value;
}

/**
 * D2-only structural conversation shell. It deliberately renders no messages,
 * generated answer, transcript, composer submission result, or backend state.
 * D3 will own the deterministic conversation adapter and feed real typed state
 * into this already-proven presentation surface.
 */
export function WorldFocusDanteConversation({
  surface,
  onRequestClose,
}: WorldFocusSurfaceRendererProps) {
  const { t } = useTranslation('common');
  const presentation = useWorldFocusDanteConversationPresentation();
  const maximizeRef = useRef<HTMLButtonElement | null>(null);
  const restoreRef = useRef<HTMLButtonElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    const transition = presentation.focusTransition;
    if (transition.serial === 0 && surface.presentation !== 'route') {
      return;
    }

    queueMicrotask(() => {
      if (surface.presentation === 'route') {
        if (transition.action === 'maximize') {
          restoreRef.current?.focus({ preventScroll: true });
        } else {
          closeRef.current?.focus({ preventScroll: true });
        }
        return;
      }

      if (transition.action === 'restore') {
        maximizeRef.current?.focus({ preventScroll: true });
      }
    });
  }, [presentation.focusTransition, surface.presentation]);

  const canRestore =
    surface.presentation === 'route' && presentation.preference === 'focus';

  return (
    <section
      className="world-focus-dante-conversation"
      data-world-focus-dante-surface="conversation"
      data-world-focus-dante-conversation-presentation={surface.presentation}
      role="dialog"
      aria-modal="false"
      aria-labelledby="world-focus-dante-conversation-title"
    >
      <header className="world-focus-dante-conversation-header">
        <h2
          id="world-focus-dante-conversation-title"
          className="world-focus-dante-conversation-title"
        >
          {t(($) => $.common.worldFocus.dante.conversationTitle)}
        </h2>
        <div className="world-focus-dante-conversation-actions">
          {surface.presentation === 'sidecar' ? (
            <button
              ref={maximizeRef}
              className="world-focus-dante-conversation-action"
              type="button"
              onClick={presentation.requestMaximize}
            >
              {t(($) => $.common.worldFocus.dante.maximizeConversation)}
            </button>
          ) : canRestore ? (
            <button
              ref={restoreRef}
              className="world-focus-dante-conversation-action"
              type="button"
              onClick={presentation.requestRestore}
            >
              {t(($) => $.common.worldFocus.dante.restoreConversation)}
            </button>
          ) : null}
          <button
            ref={closeRef}
            className="world-focus-dante-conversation-close"
            type="button"
            aria-label={t(($) => $.common.worldFocus.dante.closeConversation)}
            onClick={onRequestClose}
          >
            <span aria-hidden="true">×</span>
          </button>
        </div>
      </header>
      <div
        className="world-focus-dante-conversation-body"
        data-world-focus-dante-conversation-body="empty"
      />
    </section>
  );
}
