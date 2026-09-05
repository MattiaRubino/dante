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

import {
  createWorldFocusDanteConversationRequest,
  WORLD_FOCUS_DANTE_CONVERSATION_MAX_HISTORY,
  type WorldFocusDanteConversationReader,
  type WorldFocusDanteConversationRequest,
  type WorldFocusDanteConversationResultClass,
} from '../application/world-focus-dante-conversation';
import { readWorldFocusDanteConversation } from '../application/world-focus-dante-conversation-runtime';
import { WorldFocusLatestReadCoordinator } from '../application/world-focus-foundation';
import type { WorldFocusContextReferenceSet } from '../model/world-focus-context-reference';
import type { WorldFocusId } from '../model/world-focus-identity';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export const WORLD_FOCUS_DANTE_CONVERSATION_KIND = 'dante-conversation' as const;
export const WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID =
  'dante:conversation' as const;

export type WorldFocusDanteConversationMessage =
  | Readonly<{
      id: string;
      role: 'user';
      text: string;
    }>
  | Readonly<{
      id: string;
      role: 'assistant';
      resultClass: WorldFocusDanteConversationResultClass;
      text: string;
    }>;

export type WorldFocusDanteConversationRequestState =
  | Readonly<{ status: 'idle' }>
  | Readonly<{
      status: 'pending';
      requestId: string;
      workspaceGeneration: number;
    }>
  | Readonly<{
      status: 'unavailable';
      requestId: string;
      retryable: boolean;
    }>
  | Readonly<{ status: 'error'; requestId: string }>
  | Readonly<{ status: 'cancelled'; requestId: string }>
  | Readonly<{ status: 'superseded'; requestId: string }>;

export type WorldFocusDanteConversationContextSeed = Readonly<{
  references: WorldFocusContextReferenceSet;
  workspaceGeneration: number;
}>;

type WorldFocusDanteConversationContextValue = Readonly<{
  messages: readonly WorldFocusDanteConversationMessage[];
  requestState: WorldFocusDanteConversationRequestState;
  isOpen: boolean;
  beginFromComposer: (
    composerInstanceId: string,
    input: string,
    contextSeed?: WorldFocusDanteConversationContextSeed | null,
  ) => boolean;
  submitTurn: (input: string) => boolean;
  cancelPending: () => void;
}>;

const WorldFocusDanteConversationContext =
  createContext<WorldFocusDanteConversationContextValue | null>(null);

type WorldFocusDanteConversationProviderProps = Readonly<{
  worldId: WorldFocusId;
  restoreInvokerFocus: () => void;
  children: ReactNode;
  reader?: WorldFocusDanteConversationReader;
}>;

type WorldFocusDanteConversationContextSession = Readonly<{
  references: WorldFocusContextReferenceSet;
  workspaceGeneration: number;
}>;

function toHistory(
  messages: readonly WorldFocusDanteConversationMessage[],
): WorldFocusDanteConversationRequest['history'] {
  return Object.freeze(
    messages
      .slice(-WORLD_FOCUS_DANTE_CONVERSATION_MAX_HISTORY)
      .map((message) =>
        message.role === 'user'
          ? Object.freeze({ role: 'user' as const, text: message.text })
          : Object.freeze({
              role: 'assistant' as const,
              resultClass: message.resultClass,
              text: message.text,
            }),
      ),
  );
}

function resultMatchesRequest(
  result: Awaited<ReturnType<WorldFocusDanteConversationReader>>,
  request: WorldFocusDanteConversationRequest,
): boolean {
  return (
    result.requestId === request.requestId &&
    result.worldId === request.worldId &&
    result.workspaceGeneration === request.workspaceGeneration
  );
}

export function WorldFocusDanteConversationProvider({
  worldId,
  restoreInvokerFocus,
  children,
  reader = readWorldFocusDanteConversation,
}: WorldFocusDanteConversationProviderProps) {
  const { i18n } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();
  const [messages, setMessages] = useState<
    readonly WorldFocusDanteConversationMessage[]
  >(() => Object.freeze([]));
  const [requestState, setRequestState] =
    useState<WorldFocusDanteConversationRequestState>({ status: 'idle' });
  const [contextSession, setContextSession] =
    useState<WorldFocusDanteConversationContextSession | null>(null);
  const [readCoordinator] = useState(() => new WorldFocusLatestReadCoordinator());
  const requestSerialRef = useRef(0);
  const conversationWasOpenRef = useRef(false);

  if (workspace.state.worldId !== worldId) {
    throw new Error('World Focus DANTE conversation owner belongs to another World');
  }

  const isOpen = workspace.state.surfaces.some(
    (surface) =>
      surface.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  );

  const runRequest = useCallback(
    (
      input: string,
      replaceInstanceId: string | null,
      requestedContextSession: WorldFocusDanteConversationContextSession | null,
    ): boolean => {
      if (requestState.status === 'pending') {
        return false;
      }

      if (
        replaceInstanceId !== null &&
        !workspace.state.surfaces.some(
          (surface) => surface.instanceId === replaceInstanceId,
        )
      ) {
        return false;
      }

      if (replaceInstanceId === null && !isOpen) {
        return false;
      }

      const effectiveContextSession =
        replaceInstanceId === null ? contextSession : requestedContextSession;
      if (
        effectiveContextSession !== null &&
        effectiveContextSession.workspaceGeneration !== workspace.state.generation
      ) {
        return false;
      }

      const nextSerial = requestSerialRef.current + 1;
      const requestId = `${worldId}:local-dante:${nextSerial}`;
      let request: WorldFocusDanteConversationRequest;
      try {
        request = createWorldFocusDanteConversationRequest({
          requestId,
          worldId,
          workspaceGeneration:
            effectiveContextSession?.workspaceGeneration ?? workspace.state.generation,
          input,
          history: toHistory(messages),
          locale: i18n.resolvedLanguage ?? i18n.language ?? 'en',
          contextReferences: effectiveContextSession?.references ?? null,
        });
      } catch {
        return false;
      }

      requestSerialRef.current = nextSerial;
      const userMessage = Object.freeze({
        id: `${requestId}:user`,
        role: 'user' as const,
        text: request.input,
      });

      if (replaceInstanceId !== null) {
        workspace.replaceSurface(replaceInstanceId, {
          instanceId: WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
          kind: WORLD_FOCUS_DANTE_CONVERSATION_KIND,
          depth: 'explore',
          presentation: 'sidecar',
          origin: 'user',
          contextReference: request.contextReferences?.primary ?? null,
          dismissible: true,
          expectedWorkspace: {
            worldId: workspace.state.worldId,
            generation: workspace.state.generation,
          },
        });
        setContextSession(
          request.contextReferences === null
            ? null
            : Object.freeze({
                references: request.contextReferences,
                workspaceGeneration: request.workspaceGeneration,
              }),
        );
      }

      setMessages((current) => Object.freeze([...current, userMessage]));
      setRequestState({
        status: 'pending',
        requestId,
        workspaceGeneration: request.workspaceGeneration,
      });

      const lease = readCoordinator.begin();
      void reader(request, lease.signal)
        .then((result) => {
          lease.commit(() => {
            if (!resultMatchesRequest(result, request)) {
              setRequestState({ status: 'error', requestId });
              return;
            }

            if (result.status === 'unavailable') {
              setRequestState({
                status: 'unavailable',
                requestId,
                retryable: result.retryable,
              });
              return;
            }

            const assistantMessage = Object.freeze({
              id: `${requestId}:assistant`,
              role: 'assistant' as const,
              resultClass: result.resultClass,
              text: result.output,
            });
            setMessages((current) =>
              Object.freeze([...current, assistantMessage]),
            );
            setRequestState({ status: 'idle' });
          });
        })
        .catch(() => {
          if (lease.signal.aborted) return;
          lease.commit(() => setRequestState({ status: 'error', requestId }));
        })
        .finally(() => lease.release());

      return true;
    },
    [
      contextSession,
      i18n.language,
      i18n.resolvedLanguage,
      isOpen,
      messages,
      readCoordinator,
      reader,
      requestState.status,
      workspace,
      worldId,
    ],
  );

  const beginFromComposer = useCallback(
    (
      composerInstanceId: string,
      input: string,
      contextSeed: WorldFocusDanteConversationContextSeed | null = null,
    ) => runRequest(input, composerInstanceId, contextSeed),
    [runRequest],
  );

  const submitTurn = useCallback(
    (input: string) => runRequest(input, null, contextSession),
    [contextSession, runRequest],
  );

  const cancelPending = useCallback(() => {
    if (requestState.status !== 'pending') return;
    const requestId = requestState.requestId;
    readCoordinator.cancelCurrent();
    setRequestState({ status: 'cancelled', requestId });
  }, [readCoordinator, requestState]);

  useEffect(() => {
    if (
      requestState.status !== 'pending' ||
      requestState.workspaceGeneration === workspace.state.generation
    ) {
      return;
    }

    const requestId = requestState.requestId;
    const requestGeneration = requestState.workspaceGeneration;
    readCoordinator.cancelCurrent();
    queueMicrotask(() => {
      setRequestState((current) =>
        current.status === 'pending' &&
        current.requestId === requestId &&
        current.workspaceGeneration === requestGeneration
          ? { status: 'superseded', requestId }
          : current,
      );
    });
  }, [readCoordinator, requestState, workspace.state.generation]);

  useEffect(() => {
    if (
      contextSession === null ||
      contextSession.workspaceGeneration === workspace.state.generation ||
      requestState.status === 'superseded' ||
      requestState.status === 'cancelled'
    ) {
      return;
    }

    readCoordinator.cancelCurrent();
    const requestId =
      requestState.status === 'pending'
        ? requestState.requestId
        : `${worldId}:context-session:${contextSession.workspaceGeneration}`;
    queueMicrotask(() => {
      setRequestState((current) =>
        current.status === 'superseded' || current.status === 'cancelled'
          ? current
          : { status: 'superseded', requestId },
      );
    });
  }, [
    contextSession,
    readCoordinator,
    requestState,
    workspace.state.generation,
    worldId,
  ]);

  useEffect(() => {
    if (isOpen) {
      conversationWasOpenRef.current = true;
      return;
    }

    if (!conversationWasOpenRef.current) {
      return;
    }

    conversationWasOpenRef.current = false;
    readCoordinator.cancelCurrent();
    queueMicrotask(() => {
      setMessages(Object.freeze([]));
      setContextSession(null);
      setRequestState({ status: 'idle' });
      restoreInvokerFocus();
    });
  }, [isOpen, readCoordinator, restoreInvokerFocus]);

  useEffect(
    () => () => {
      readCoordinator.cancelCurrent();
    },
    [readCoordinator],
  );

  const value = useMemo<WorldFocusDanteConversationContextValue>(
    () => ({
      messages,
      requestState,
      isOpen,
      beginFromComposer,
      submitTurn,
      cancelPending,
    }),
    [
      beginFromComposer,
      cancelPending,
      isOpen,
      messages,
      requestState,
      submitTurn,
    ],
  );

  return (
    <WorldFocusDanteConversationContext.Provider value={value}>
      {children}
    </WorldFocusDanteConversationContext.Provider>
  );
}

export function useOptionalWorldFocusDanteConversation(): WorldFocusDanteConversationContextValue | null {
  return useContext(WorldFocusDanteConversationContext);
}

export function useWorldFocusDanteConversation(): WorldFocusDanteConversationContextValue {
  const value = useOptionalWorldFocusDanteConversation();
  if (value === null) {
    throw new Error(
      'useWorldFocusDanteConversation must be used inside WorldFocusDanteConversationProvider',
    );
  }
  return value;
}
