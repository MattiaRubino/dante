import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type FormEvent,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import type {
  WorldFocusSurfaceDescriptor,
  WorldFocusWorkspaceState,
} from '../model/world-focus-workspace';
import type { WorldFocusSurfaceRendererProps } from './world-focus-surface-registry';
import {
  WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  WORLD_FOCUS_DANTE_CONVERSATION_KIND,
  useOptionalWorldFocusDanteConversation,
} from './world-focus-dante-conversation-context';
import { useWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation-context';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export {
  WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  WORLD_FOCUS_DANTE_CONVERSATION_KIND,
} from './world-focus-dante-conversation-context';

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
 * D2 remains the geometry owner. When D3's route-scoped conversation provider
 * is present this surface renders its mounted transcript/request state; without
 * D3 it remains the original empty structural D2 shell used by D2 tests.
 */
export function WorldFocusDanteConversation({
  surface,
  onRequestClose,
}: WorldFocusSurfaceRendererProps) {
  const { t } = useTranslation('common');
  const presentation = useWorldFocusDanteConversationPresentation();
  const conversation = useOptionalWorldFocusDanteConversation();
  const maximizeRef = useRef<HTMLButtonElement | null>(null);
  const restoreRef = useRef<HTMLButtonElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  const inputRef = useRef<HTMLTextAreaElement | null>(null);
  const [draft, setDraft] = useState('');

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

  useEffect(() => {
    if (
      conversation === null ||
      conversation.messages.length === 0 ||
      surface.presentation === 'route' ||
      conversation.requestState.status === 'pending'
    ) {
      return;
    }

    queueMicrotask(() => inputRef.current?.focus({ preventScroll: true }));
  }, [
    conversation,
    conversation?.messages.length,
    conversation?.requestState.status,
    surface.presentation,
  ]);

  const canRestore =
    surface.presentation === 'route' && presentation.preference === 'focus';
  const pending = conversation?.requestState.status === 'pending';

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (conversation === null) return;
    const request = draft.trim();
    if (request.length === 0) return;

    if (conversation.submitTurn(request)) {
      setDraft('');
    }
  };

  return (
    <section
      id="world-focus-dante-conversation"
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
        data-world-focus-dante-conversation-body={
          conversation === null ? 'empty' : 'active'
        }
      >
        {conversation === null ? null : (
          <>
            <ol
              className="world-focus-dante-conversation-messages"
              aria-label={t(($) => $.common.worldFocus.dante.messages)}
              aria-live="polite"
            >
              {conversation.messages.map((message) => (
                <li
                  key={message.id}
                  className="world-focus-dante-conversation-message"
                  data-world-focus-dante-message-role={message.role}
                  {...(message.role === 'assistant'
                    ? {
                        'data-world-focus-dante-response': 'true',
                        'data-world-focus-dante-result-class':
                          message.resultClass,
                      }
                    : {})}
                >
                  <span className="world-focus-dante-conversation-message-speaker">
                    {message.role === 'user'
                      ? t(($) => $.common.worldFocus.dante.you)
                      : 'DANTE'}
                  </span>
                  <p>{message.text}</p>
                </li>
              ))}
            </ol>

            {conversation.requestState.status === 'pending' ? (
              <p className="world-focus-dante-conversation-status" role="status">
                {t(($) => $.common.worldFocus.dante.localPending)}
              </p>
            ) : conversation.requestState.status === 'unavailable' ? (
              <p className="world-focus-dante-conversation-status" role="status">
                {t(($) => $.common.worldFocus.dante.localUnavailable)}
              </p>
            ) : conversation.requestState.status === 'error' ? (
              <p className="world-focus-dante-conversation-status" role="alert">
                {t(($) => $.common.worldFocus.dante.localError)}
              </p>
            ) : conversation.requestState.status === 'cancelled' ? (
              <p className="world-focus-dante-conversation-status" role="status">
                {t(($) => $.common.worldFocus.dante.localCancelled)}
              </p>
            ) : conversation.requestState.status === 'superseded' ? (
              <p className="world-focus-dante-conversation-status" role="status">
                {t(($) => $.common.worldFocus.dante.localSuperseded)}
              </p>
            ) : null}

            <form
              className="world-focus-dante-conversation-composer"
              onSubmit={handleSubmit}
            >
              <label
                className="world-focus-dante-conversation-composer-label"
                htmlFor="world-focus-dante-conversation-draft"
              >
                {t(($) => $.common.worldFocus.dante.followUpLabel)}
              </label>
              <textarea
                ref={inputRef}
                id="world-focus-dante-conversation-draft"
                className="world-focus-dante-conversation-input"
                rows={2}
                value={draft}
                placeholder={t(($) => $.common.worldFocus.dante.followUpPlaceholder)}
                disabled={pending}
                onChange={(event) => setDraft(event.currentTarget.value)}
              />
              <div className="world-focus-dante-conversation-composer-actions">
                {pending ? (
                  <button
                    className="world-focus-dante-conversation-cancel-request"
                    type="button"
                    onClick={conversation.cancelPending}
                  >
                    {t(($) => $.common.worldFocus.dante.cancelRequest)}
                  </button>
                ) : null}
                <button
                  className="world-focus-dante-conversation-send"
                  type="submit"
                  disabled={pending || draft.trim().length === 0}
                >
                  {t(($) => $.common.worldFocus.dante.send)}
                </button>
              </div>
            </form>
          </>
        )}
      </div>
    </section>
  );
}
