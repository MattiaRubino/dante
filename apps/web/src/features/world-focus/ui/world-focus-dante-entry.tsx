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
  type RefObject,
} from 'react';
import { useTranslation } from 'react-i18next';

import {
  isWorldFocusFeatureAvailable,
  type WorldFocusFeatureAvailability,
} from '../model/world-focus-platform';
import { useWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation-context';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export const WORLD_FOCUS_DANTE_COMPOSER_KIND = 'dante-composer' as const;
export const WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID =
  'dante:composer' as const;

export type WorldFocusDanteEntryContextValue = Readonly<{
  worldId: string;
  worldLabel: string;
  availability: WorldFocusFeatureAvailability;
  invokerRef: RefObject<HTMLButtonElement | null>;
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
 * DANTE-specific focus/presentation context. DOM focus ownership deliberately
 * stays outside the generic workspace cursor so no DOM node can become DANTE
 * context, authorization input or durable Run state.
 */
export function WorldFocusDanteEntryProvider({
  worldId,
  worldLabel,
  availability,
  children,
}: WorldFocusDanteEntryProviderProps) {
  const invokerRef = useRef<HTMLButtonElement | null>(null);
  const restoreInvokerFocus = useCallback(() => {
    const invoker = invokerRef.current;
    queueMicrotask(() => {
      if (invoker?.isConnected === true && !invoker.disabled) {
        invoker.focus({ preventScroll: true });
      }
    });
  }, []);

  const value = useMemo<WorldFocusDanteEntryContextValue>(
    () => ({
      worldId,
      worldLabel,
      availability,
      invokerRef,
      restoreInvokerFocus,
    }),
    [availability, restoreInvokerFocus, worldId, worldLabel],
  );

  return (
    <WorldFocusDanteEntryContext.Provider value={value}>
      {children}
    </WorldFocusDanteEntryContext.Provider>
  );
}

export function useWorldFocusDanteEntry(): WorldFocusDanteEntryContextValue {
  const value = useContext(WorldFocusDanteEntryContext);
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
  const { worldLabel, availability, invokerRef } = useWorldFocusDanteEntry();
  const composerIsOpen = workspace.state.surfaces.some(
    (surface) => surface.instanceId === WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID,
  );
  const backgroundIsInert = allocation.mainInteraction === 'inert';

  const requestOpen = useCallback(() => {
    workspace.openSurface({
      instanceId: WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID,
      kind: WORLD_FOCUS_DANTE_COMPOSER_KIND,
      depth: 'peek',
      presentation: 'popover',
      origin: 'user',
      contextReference: null,
      expectedGeneration: workspace.state.generation,
    });
  }, [workspace]);

  return (
    <div
      className="world-focus-dante-entry"
      data-world-focus-dante-availability={availability.status}
      data-world-focus-dante-open={composerIsOpen ? 'true' : 'false'}
      inert={backgroundIsInert ? true : undefined}
    >
      <button
        ref={invokerRef}
        className="world-focus-dante-invoke"
        type="button"
        aria-controls="world-focus-dante-composer"
        aria-expanded={composerIsOpen}
        aria-label={t(($) => $.common.worldFocus.dante.invokeForWorld, {
          world: worldLabel,
        })}
        disabled={composerIsOpen}
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
 * P1 pre-backend composer shell. A submit attempt intentionally yields only a
 * truthful local unavailable state. D1 does not invent a conversation, Run or
 * assistant response before the dedicated deterministic conversation vertical.
 */
export function WorldFocusDanteComposer({
  onRequestClose,
}: WorldFocusDanteComposerProps) {
  const { t } = useTranslation('common');
  const { worldId, worldLabel, availability, restoreInvokerFocus } =
    useWorldFocusDanteEntry();
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  const [draft, setDraft] = useState('');
  const [submissionUnavailable, setSubmissionUnavailable] = useState(false);
  const entryIsAvailable = isWorldFocusFeatureAvailable(availability);

  useEffect(() => {
    if (entryIsAvailable) {
      textareaRef.current?.focus({ preventScroll: true });
    } else {
      closeRef.current?.focus({ preventScroll: true });
    }

    return restoreInvokerFocus;
  }, [entryIsAvailable, restoreInvokerFocus]);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (draft.trim().length === 0) {
      return;
    }

    setSubmissionUnavailable(true);
    textareaRef.current?.focus({ preventScroll: true });
  };

  return (
    <section
      id="world-focus-dante-composer"
      className="world-focus-dante-composer"
      data-world-focus-dante-surface="composer"
      data-world-focus-dante-world-id={worldId}
      data-world-focus-dante-status={availability.status}
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
              aria-describedby={
                submissionUnavailable
                  ? 'world-focus-dante-submit-status'
                  : undefined
              }
              onChange={(event) => {
                setDraft(event.currentTarget.value);
                if (submissionUnavailable) {
                  setSubmissionUnavailable(false);
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
          {submissionUnavailable ? (
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
