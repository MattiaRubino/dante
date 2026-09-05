import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type FormEvent,
  type MouseEvent,
  type ReactNode,
  type RefObject,
} from 'react';
import { useTranslation } from 'react-i18next';

import { WORLD_FOCUS_DANTE_CONVERSATION_MAX_INPUT_LENGTH } from '../application/world-focus-dante-conversation';
import {
  createWorldFocusContextReferenceSet,
  type WorldFocusContextReferenceSet,
} from '../model/world-focus-context-reference';
import {
  isWorldFocusFeatureAvailable,
  type WorldFocusFeatureAvailability,
} from '../model/world-focus-platform';
import { getWorldFocusBlockingSurface } from '../model/world-focus-workspace';
import {
  WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  useOptionalWorldFocusDanteConversation,
} from './world-focus-dante-conversation-context';
import { useWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation-context';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export const WORLD_FOCUS_DANTE_COMPOSER_KIND = 'dante-composer' as const;
export const WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID =
  'dante:composer' as const;

export type WorldFocusDanteComposerInvocation = Readonly<{
  prompt: string;
  contextReferences: WorldFocusContextReferenceSet | null;
  worldId: string;
  workspaceGeneration: number;
}>;

type WorldFocusDanteComposerRequest = Readonly<{
  invoker: HTMLButtonElement;
  prompt: string;
  contextReferences: WorldFocusContextReferenceSet | null;
}>;

export type WorldFocusDanteEntryContextValue = Readonly<{
  worldId: string;
  worldLabel: string;
  availability: WorldFocusFeatureAvailability;
  invokerRef: RefObject<HTMLButtonElement | null>;
  composerInvocation: WorldFocusDanteComposerInvocation | null;
  canRequestComposer: boolean;
  requestComposer: (request: WorldFocusDanteComposerRequest) => boolean;
  restoreInvokerFocus: () => void;
}>;

const WorldFocusDanteEntryContext =
  createContext<WorldFocusDanteEntryContextValue | null>(null);

type WorldFocusDanteEntryProviderProps = Readonly<{
  worldId: string;
  worldLabel: string;
  availability: WorldFocusFeatureAvailability;
  children: ReactNode;
}>;

/**
 * DANTE-specific focus/invocation context. DOM focus ownership deliberately
 * stays outside the generic workspace cursor so no DOM node can become DANTE
 * context, authorization input or durable Run state.
 */
export function WorldFocusDanteEntryProvider({
  worldId,
  worldLabel,
  availability,
  children,
}: WorldFocusDanteEntryProviderProps) {
  const workspace = useWorldFocusWorkspace();
  const invokerRef = useRef<HTMLButtonElement | null>(null);
  const activeInvokerRef = useRef<HTMLButtonElement | null>(null);
  const [composerInvocation, setComposerInvocation] =
    useState<WorldFocusDanteComposerInvocation | null>(null);
  const danteInteractionIsOpen = workspace.state.surfaces.some(
    (surface) =>
      surface.instanceId === WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID ||
      surface.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  );
  const canRequestComposer =
    !danteInteractionIsOpen && getWorldFocusBlockingSurface(workspace.state) === null;

  const restoreInvokerFocus = useCallback(() => {
    const preferredInvoker = activeInvokerRef.current;
    const fallbackInvoker = invokerRef.current;
    activeInvokerRef.current = null;
    queueMicrotask(() => {
      const target =
        preferredInvoker?.isConnected === true && !preferredInvoker.disabled
          ? preferredInvoker
          : fallbackInvoker?.isConnected === true && !fallbackInvoker.disabled
            ? fallbackInvoker
            : null;
      target?.focus({ preventScroll: true });
    });
  }, []);

  const requestComposer = useCallback(
    (request: WorldFocusDanteComposerRequest): boolean => {
      if (
        workspace.state.surfaces.some(
          (surface) =>
            surface.instanceId === WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID ||
            surface.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
        ) ||
        getWorldFocusBlockingSurface(workspace.state) !== null
      ) {
        return false;
      }

      const prompt = request.prompt.trim();
      if (prompt.length > WORLD_FOCUS_DANTE_CONVERSATION_MAX_INPUT_LENGTH) {
        return false;
      }

      let contextReferences: WorldFocusContextReferenceSet | null = null;
      try {
        contextReferences =
          request.contextReferences === null
            ? null
            : createWorldFocusContextReferenceSet({
                primary: request.contextReferences.primary,
                supporting: request.contextReferences.supporting,
              });
      } catch {
        return false;
      }
      if (contextReferences !== null && prompt.length === 0) {
        return false;
      }

      const invocation = Object.freeze({
        prompt,
        contextReferences,
        worldId: workspace.state.worldId,
        workspaceGeneration: workspace.state.generation,
      });
      activeInvokerRef.current = request.invoker;
      setComposerInvocation(invocation);
      workspace.openSurface({
        instanceId: WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID,
        kind: WORLD_FOCUS_DANTE_COMPOSER_KIND,
        depth: 'peek',
        presentation: 'popover',
        origin: 'user',
        contextReference: contextReferences?.primary ?? null,
        expectedWorkspace: {
          worldId: workspace.state.worldId,
          generation: workspace.state.generation,
        },
      });
      return true;
    },
    [workspace],
  );

  const value = useMemo<WorldFocusDanteEntryContextValue>(
    () => ({
      worldId,
      worldLabel,
      availability,
      invokerRef,
      composerInvocation,
      canRequestComposer,
      requestComposer,
      restoreInvokerFocus,
    }),
    [
      availability,
      canRequestComposer,
      composerInvocation,
      requestComposer,
      restoreInvokerFocus,
      worldId,
      worldLabel,
    ],
  );

  return (
    <WorldFocusDanteEntryContext.Provider value={value}>
      {children}
    </WorldFocusDanteEntryContext.Provider>
  );
}

export function useOptionalWorldFocusDanteEntry(): WorldFocusDanteEntryContextValue | null {
  return useContext(WorldFocusDanteEntryContext);
}

export function useWorldFocusDanteEntry(): WorldFocusDanteEntryContextValue {
  const value = useOptionalWorldFocusDanteEntry();
  if (value === null) {
    throw new Error(
      'useWorldFocusDanteEntry must be used inside WorldFocusDanteEntryProvider',
    );
  }
  return value;
}

/**
 * P0 quiet presence. This is only an invoke affordance: it never renders model
 * output, reserves a chat column or infers authorization from the active World.
 */
export function WorldFocusDanteInvoke() {
  const { t } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();
  const allocation = useWorldFocusWorkspaceAllocation();
  const { worldLabel, availability, invokerRef, requestComposer } =
    useWorldFocusDanteEntry();
  const composerIsOpen = workspace.state.surfaces.some(
    (surface) => surface.instanceId === WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID,
  );
  const conversationIsOpen = workspace.state.surfaces.some(
    (surface) =>
      surface.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  );
  const danteInteractionIsOpen = composerIsOpen || conversationIsOpen;
  const backgroundIsInert = allocation.mainInteraction === 'inert';

  const requestOpen = useCallback(
    (event: MouseEvent<HTMLButtonElement>) => {
      requestComposer({
        invoker: event.currentTarget,
        prompt: '',
        contextReferences: null,
      });
    },
    [requestComposer],
  );

  return (
    <div
      className="world-focus-dante-entry"
      data-world-focus-dante-availability={availability.status}
      data-world-focus-dante-open={danteInteractionIsOpen ? 'true' : 'false'}
      inert={backgroundIsInert ? true : undefined}
    >
      <button
        ref={invokerRef}
        className="world-focus-dante-invoke"
        type="button"
        aria-controls={composerIsOpen ? 'world-focus-dante-composer' : undefined}
        aria-expanded={danteInteractionIsOpen}
        aria-label={t(($) => $.common.worldFocus.dante.invokeForWorld, {
          world: worldLabel,
        })}
        disabled={danteInteractionIsOpen}
        onClick={requestOpen}
      >
        <span className="world-focus-dante-invoke-mark" aria-hidden="true">
          D
        </span>
        <span className="world-focus-dante-invoke-label">DANTE</span>
        {availability.status === 'unavailable' ? (
          <span
            className="world-focus-dante-invoke-unavailable"
            aria-hidden="true"
          >
            —
          </span>
        ) : null}
      </button>
    </div>
  );
}

type WorldFocusDanteComposerProps = Readonly<{
  onRequestClose: () => void;
}>;

/**
 * P1 composer shell. Without the D3 route-scoped conversation owner it keeps
 * the original truthful pre-backend unavailable fallback; with D3 mounted, a
 * successful submit atomically hands this surface to the one conversation.
 */
export function WorldFocusDanteComposer({
  onRequestClose,
}: WorldFocusDanteComposerProps) {
  const { t } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();
  const {
    worldId,
    worldLabel,
    availability,
    composerInvocation,
    restoreInvokerFocus,
  } = useWorldFocusDanteEntry();
  const conversation = useOptionalWorldFocusDanteConversation();
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  const handoffRef = useRef(false);
  const [draft, setDraft] = useState(() => composerInvocation?.prompt ?? '');
  const [submissionUnavailable, setSubmissionUnavailable] = useState(false);
  const [contextStale, setContextStale] = useState(false);
  const entryIsAvailable = isWorldFocusFeatureAvailable(availability);

  useEffect(() => {
    if (entryIsAvailable) {
      textareaRef.current?.focus({ preventScroll: true });
    } else {
      closeRef.current?.focus({ preventScroll: true });
    }

    return () => {
      if (!handoffRef.current) {
        restoreInvokerFocus();
      }
    };
  }, [entryIsAvailable, restoreInvokerFocus]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const request = draft.trim();
    if (request.length === 0) {
      return;
    }

    const contextualReferences = composerInvocation?.contextReferences ?? null;
    if (
      contextualReferences !== null &&
      (composerInvocation?.worldId !== workspace.state.worldId ||
        composerInvocation.workspaceGeneration !== workspace.state.generation)
    ) {
      setContextStale(true);
      setSubmissionUnavailable(false);
      textareaRef.current?.focus({ preventScroll: true });
      return;
    }

    const contextSeed =
      contextualReferences === null || composerInvocation === null
        ? null
        : Object.freeze({
            references: contextualReferences,
            workspaceGeneration: composerInvocation.workspaceGeneration,
          });

    if (
      conversation?.beginFromComposer(
        WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID,
        request,
        contextSeed,
      ) === true
    ) {
      handoffRef.current = true;
      setSubmissionUnavailable(false);
      setContextStale(false);
      return;
    }

    setSubmissionUnavailable(true);
    setContextStale(false);
    textareaRef.current?.focus({ preventScroll: true });
  };

  const statusId =
    submissionUnavailable || contextStale
      ? 'world-focus-dante-submit-status'
      : undefined;

  return (
    <section
      id="world-focus-dante-composer"
      className="world-focus-dante-composer"
      data-world-focus-dante-surface="composer"
      data-world-focus-dante-world-id={worldId}
      data-world-focus-dante-status={availability.status}
      data-world-focus-dante-contextual={
        composerInvocation?.contextReferences == null ? 'false' : 'true'
      }
      role="dialog"
      aria-modal="false"
      aria-labelledby="world-focus-dante-composer-title"
    >
      <header className="world-focus-dante-composer-header">
        <div className="world-focus-dante-composer-heading">
          <p
            id="world-focus-dante-composer-title"
            className="world-focus-dante-composer-title"
          >
            DANTE
          </p>
          <p className="world-focus-dante-composer-context">
            {t(($) => $.common.worldFocus.dante.worldContext, {
              world: worldLabel,
            })}
          </p>
        </div>
        <button
          ref={closeRef}
          className="world-focus-dante-composer-close"
          type="button"
          aria-label={t(($) => $.common.worldFocus.dante.close)}
          onClick={onRequestClose}
        >
          <span aria-hidden="true">×</span>
        </button>
      </header>

      {entryIsAvailable ? (
        <form
          className="world-focus-dante-composer-form"
          onSubmit={handleSubmit}
        >
          <label
            className="world-focus-dante-composer-label"
            htmlFor="world-focus-dante-draft"
          >
            {t(($) => $.common.worldFocus.dante.inputLabel)}
          </label>
          <div className="world-focus-dante-composer-field">
            <textarea
              ref={textareaRef}
              id="world-focus-dante-draft"
              className="world-focus-dante-composer-input"
              value={draft}
              rows={3}
              placeholder={t(($) => $.common.worldFocus.dante.placeholder)}
              aria-describedby={statusId}
              onChange={(event) => {
                setDraft(event.currentTarget.value);
                if (submissionUnavailable) {
                  setSubmissionUnavailable(false);
                }
                if (contextStale) {
                  setContextStale(false);
                }
              }}
            />
            <button
              className="world-focus-dante-composer-submit"
              type="submit"
              disabled={draft.trim().length === 0}
              aria-label={t(($) => $.common.worldFocus.dante.send)}
            >
              <span aria-hidden="true">↑</span>
            </button>
          </div>
          {contextStale ? (
            <p
              id="world-focus-dante-submit-status"
              className="world-focus-dante-composer-status"
              role="alert"
            >
              {t(($) => $.common.worldFocus.dante.contextChangedBeforeSubmit)}
            </p>
          ) : submissionUnavailable ? (
            <p
              id="world-focus-dante-submit-status"
              className="world-focus-dante-composer-status"
              role="alert"
            >
              {t(($) => $.common.worldFocus.dante.submissionUnavailable)}
            </p>
          ) : null}
        </form>
      ) : (
        <p className="world-focus-dante-composer-status" role="status">
          {t(($) => $.common.worldFocus.dante.unavailable)}
        </p>
      )}
    </section>
  );
}
