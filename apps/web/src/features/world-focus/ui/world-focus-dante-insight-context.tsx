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
  createWorldFocusDanteInsightRequest,
  type WorldFocusDanteInsight,
  type WorldFocusDanteInsightReader,
  type WorldFocusDanteInsightRequest,
} from '../application/world-focus-dante-insight';
import { readWorldFocusDanteInsight } from '../application/world-focus-dante-insight-runtime';
import { WorldFocusLatestReadCoordinator } from '../application/world-focus-foundation';
import type { WorldFocusDanteConversationResultClass } from '../application/world-focus-dante-conversation';
import type { WorldFocusId } from '../model/world-focus-identity';
import {
  WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
} from './world-focus-dante-conversation-context';
import { useWorldFocusDanteEntry } from './world-focus-dante-entry';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export const WORLD_FOCUS_DANTE_INSIGHT_KIND = 'dante-insight' as const;
export const WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID = 'dante:insight' as const;

export type WorldFocusDanteInsightSourceMessage = Readonly<{
  id: string;
  resultClass: WorldFocusDanteConversationResultClass;
  text: string;
}>;

export type WorldFocusDanteInsightRequestState =
  | Readonly<{ status: 'idle' }>
  | Readonly<{
      status: 'pending';
      requestId: string;
      sourceMessageId: string;
      workspaceGeneration: number;
    }>
  | Readonly<{
      status: 'unavailable';
      requestId: string;
      sourceMessageId: string;
      retryable: boolean;
    }>
  | Readonly<{
      status: 'error';
      requestId: string;
      sourceMessageId: string;
    }>
  | Readonly<{
      status: 'superseded';
      requestId: string;
      sourceMessageId: string;
    }>;

type WorldFocusDanteInsightContextValue = Readonly<{
  insight: WorldFocusDanteInsight | null;
  requestState: WorldFocusDanteInsightRequestState;
  isOpen: boolean;
  canRequestInsight: boolean;
  requestInsight: (source: WorldFocusDanteInsightSourceMessage) => boolean;
}>;

const WorldFocusDanteInsightContext =
  createContext<WorldFocusDanteInsightContextValue | null>(null);

type WorldFocusDanteInsightProviderProps = Readonly<{
  worldId: WorldFocusId;
  children: ReactNode;
  reader?: WorldFocusDanteInsightReader;
}>;

function restoreLogicalInsightInvoker(sourceMessageId: string): void {
  queueMicrotask(() => {
    queueMicrotask(() => {
      const candidates = document.querySelectorAll<HTMLButtonElement>(
        '[data-world-focus-dante-insight-invoker]',
      );
      const invoker = Array.from(candidates).find(
        (candidate) =>
          candidate.dataset.worldFocusDanteInsightInvoker === sourceMessageId,
      );
      invoker?.focus({ preventScroll: true });
    });
  });
}

/**
 * D5 route-scoped owner for one validated standalone Insight artifact. It
 * stores presentation state only and reuses the existing Workspace surface
 * stack. The exact D4 composer invocation remains the bounded contextual basis;
 * D3 conversation state is not widened or re-owned here.
 */
export function WorldFocusDanteInsightProvider({
  worldId,
  children,
  reader = readWorldFocusDanteInsight,
}: WorldFocusDanteInsightProviderProps) {
  const { i18n } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();
  const danteEntry = useWorldFocusDanteEntry();
  const [insight, setInsight] = useState<WorldFocusDanteInsight | null>(null);
  const [requestState, setRequestState] =
    useState<WorldFocusDanteInsightRequestState>({ status: 'idle' });
  const [readCoordinator] = useState(() => new WorldFocusLatestReadCoordinator());
  const requestSerialRef = useRef(0);
  const generationRef = useRef(workspace.state.generation);
  const insightWasOpenRef = useRef(false);
  const invokerMessageIdRef = useRef<string | null>(null);

  generationRef.current = workspace.state.generation;

  if (workspace.state.worldId !== worldId) {
    throw new Error('World Focus DANTE Insight owner belongs to another World');
  }

  const contextualInvocation = danteEntry.composerInvocation;
  const insightSurface = workspace.state.surfaces.find(
    (surface) => surface.instanceId === WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
  );
  const isOpen = insightSurface !== undefined;
  const canRequestInsight =
    contextualInvocation?.contextReferences !== null &&
    contextualInvocation?.contextReferences !== undefined &&
    contextualInvocation.workspaceGeneration === workspace.state.generation &&
    !isOpen;

  const requestInsight = useCallback(
    (source: WorldFocusDanteInsightSourceMessage): boolean => {
      const invocation = danteEntry.composerInvocation;
      if (
        requestState.status === 'pending' ||
        invocation === null ||
        invocation.contextReferences === null ||
        invocation.workspaceGeneration !== workspace.state.generation ||
        isOpen
      ) {
        return false;
      }

      const conversationSurface = workspace.state.surfaces.find(
        (surface) =>
          surface.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
      );
      if (conversationSurface === undefined) {
        return false;
      }

      const nextSerial = requestSerialRef.current + 1;
      const requestId = `${worldId}:local-insight:${nextSerial}`;
      let request: WorldFocusDanteInsightRequest;
      try {
        request = createWorldFocusDanteInsightRequest({
          requestId,
          worldId,
          workspaceGeneration: invocation.workspaceGeneration,
          sourceMessageId: source.id,
          sourceResultClass: source.resultClass,
          sourceText: source.text,
          locale: i18n.resolvedLanguage ?? i18n.language ?? 'en',
          contextReferences: invocation.contextReferences,
        });
      } catch {
        return false;
      }

      requestSerialRef.current = nextSerial;
      invokerMessageIdRef.current = source.id;
      setRequestState({
        status: 'pending',
        requestId,
        sourceMessageId: source.id,
        workspaceGeneration: request.workspaceGeneration,
      });

      const lease = readCoordinator.begin();
      void reader(request, lease.signal)
        .then((result) => {
          lease.commit(() => {
            if (generationRef.current !== request.workspaceGeneration) {
              setRequestState({
                status: 'superseded',
                requestId,
                sourceMessageId: source.id,
              });
              return;
            }

            if (result.status === 'unavailable') {
              setRequestState({
                status: 'unavailable',
                requestId,
                sourceMessageId: source.id,
                retryable: result.retryable,
              });
              return;
            }

            const routePresentation = conversationSurface.presentation === 'route';
            setInsight(result.insight);
            workspace.openSurface({
              instanceId: WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
              kind: WORLD_FOCUS_DANTE_INSIGHT_KIND,
              depth: 'insight',
              presentation: routePresentation ? 'route' : 'sidecar',
              origin: 'dante',
              contextReference: result.insight.basisReferences.primary,
              dismissible: true,
              blocksWorkspaceInteraction: routePresentation,
              expectedWorkspace: {
                worldId: workspace.state.worldId,
                generation: request.workspaceGeneration,
              },
            });
            setRequestState({ status: 'idle' });
          });
        })
        .catch(() => {
          if (lease.signal.aborted) return;
          lease.commit(() =>
            setRequestState({
              status: 'error',
              requestId,
              sourceMessageId: source.id,
            }),
          );
        })
        .finally(() => lease.release());

      return true;
    },
    [
      danteEntry.composerInvocation,
      i18n.language,
      i18n.resolvedLanguage,
      isOpen,
      readCoordinator,
      reader,
      requestState.status,
      workspace,
      worldId,
    ],
  );

  useEffect(() => {
    if (
      requestState.status !== 'pending' ||
      requestState.workspaceGeneration === workspace.state.generation
    ) {
      return;
    }

    const requestId = requestState.requestId;
    const sourceMessageId = requestState.sourceMessageId;
    readCoordinator.cancelCurrent();
    queueMicrotask(() =>
      setRequestState({ status: 'superseded', requestId, sourceMessageId }),
    );
  }, [readCoordinator, requestState, workspace.state.generation]);

  useEffect(() => {
    if (
      insight === null ||
      insight.workspaceGeneration === workspace.state.generation
    ) {
      return;
    }

    readCoordinator.cancelCurrent();
    workspace.closeSurface(WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID);
    setInsight(null);
  }, [insight, readCoordinator, workspace]);

  useEffect(() => {
    if (isOpen) {
      insightWasOpenRef.current = true;
      return;
    }

    if (!insightWasOpenRef.current) {
      return;
    }

    insightWasOpenRef.current = false;
    const sourceMessageId = invokerMessageIdRef.current;
    setInsight(null);
    setRequestState({ status: 'idle' });
    if (sourceMessageId !== null) {
      restoreLogicalInsightInvoker(sourceMessageId);
    }
  }, [isOpen]);

  useEffect(
    () => () => {
      readCoordinator.cancelCurrent();
    },
    [readCoordinator],
  );

  const value = useMemo<WorldFocusDanteInsightContextValue>(
    () => ({
      insight,
      requestState,
      isOpen,
      canRequestInsight,
      requestInsight,
    }),
    [canRequestInsight, insight, isOpen, requestInsight, requestState],
  );

  return (
    <WorldFocusDanteInsightContext.Provider value={value}>
      {children}
    </WorldFocusDanteInsightContext.Provider>
  );
}

export function useOptionalWorldFocusDanteInsight(): WorldFocusDanteInsightContextValue | null {
  return useContext(WorldFocusDanteInsightContext);
}

export function useWorldFocusDanteInsight(): WorldFocusDanteInsightContextValue {
  const value = useOptionalWorldFocusDanteInsight();
  if (value === null) {
    throw new Error(
      'useWorldFocusDanteInsight must be used inside WorldFocusDanteInsightProvider',
    );
  }
  return value;
}
