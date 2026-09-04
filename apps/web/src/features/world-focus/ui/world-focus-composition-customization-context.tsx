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
  readWorldFocusCompositionCustomizationOpportunities,
  type WorldFocusCompositionCustomizationReader,
} from '../application/world-focus-composition-customization-read';
import type { WorldFocusCompositionOpportunitySet } from '../application/world-focus-composition-opportunities';
import {
  applyWorldFocusCompositionDraft,
  beginWorldFocusCompositionCustomization,
  updateWorldFocusCompositionDraft,
  type WorldFocusCompositionCustomizationCommand,
  type WorldFocusCompositionCustomizationDraft,
} from '../application/world-focus-composition-customization';
import { WorldFocusLatestReadCoordinator } from '../application/world-focus-foundation';
import {
  createWorldFocusCompositionConfig,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
  type WorldFocusCompositionConfig,
} from '../model/world-focus-composition-config';
import type { WorldFocusId } from '../model/world-focus-identity';
import { getWorldFocusBlockingSurface } from '../model/world-focus-workspace';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export const WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_KIND =
  'composition-customize';
export const WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_ID =
  'composition:customize';

type WorldFocusCompositionCustomizationIssue =
  | Readonly<{
      status: 'revision-conflict';
      baseRevision: number;
      currentRevision: number;
    }>
  | Readonly<{ status: 'invalid-state' }>;

type WorldFocusCompositionCustomizationOpportunitiesState =
  | Readonly<{ status: 'idle' }>
  | Readonly<{ status: 'loading' }>
  | Readonly<{ status: 'ready'; set: WorldFocusCompositionOpportunitySet }>
  | Readonly<{ status: 'error' }>;

type ApplyDraft = typeof applyWorldFocusCompositionDraft;

type WorldFocusCompositionCustomizationContextValue = Readonly<{
  worldLabel: string;
  acceptedConfig: WorldFocusCompositionConfig;
  draft: WorldFocusCompositionCustomizationDraft | null;
  opportunities: WorldFocusCompositionCustomizationOpportunitiesState;
  issue: WorldFocusCompositionCustomizationIssue | null;
  isDirty: boolean;
  isOpen: boolean;
  begin: (invoker: HTMLElement) => void;
  retryOpportunities: () => void;
  execute: (command: WorldFocusCompositionCustomizationCommand) => boolean;
  apply: () => void;
  cancel: () => void;
}>;

const WorldFocusCompositionCustomizationContext =
  createContext<WorldFocusCompositionCustomizationContextValue | null>(null);

function createInitialConfig(worldId: WorldFocusId): WorldFocusCompositionConfig {
  return createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision: 0,
    worldId,
    entries: [],
  });
}

function sameConfig(
  left: WorldFocusCompositionConfig,
  right: WorldFocusCompositionConfig,
): boolean {
  if (
    left.schemaVersion !== right.schemaVersion ||
    left.revision !== right.revision ||
    left.worldId !== right.worldId ||
    left.entries.length !== right.entries.length
  ) {
    return false;
  }

  return left.entries.every((entry, index) => {
    const other = right.entries[index];
    return (
      other !== undefined &&
      entry.instanceId === other.instanceId &&
      entry.kind === other.kind &&
      entry.visibility === other.visibility &&
      entry.pinned === other.pinned &&
      entry.prominenceOverride === other.prominenceOverride
    );
  });
}

type WorldFocusCompositionCustomizationProviderProps = Readonly<{
  worldId: WorldFocusId;
  worldLabel: string;
  children: ReactNode;
  reader?: WorldFocusCompositionCustomizationReader;
  applyDraft?: ApplyDraft;
}>;

export function WorldFocusCompositionCustomizationProvider({
  worldId,
  worldLabel,
  children,
  reader = readWorldFocusCompositionCustomizationOpportunities,
  applyDraft = applyWorldFocusCompositionDraft,
}: WorldFocusCompositionCustomizationProviderProps) {
  const workspace = useWorldFocusWorkspace();
  const [acceptedConfig, setAcceptedConfig] = useState(() =>
    createInitialConfig(worldId),
  );
  const [draft, setDraft] =
    useState<WorldFocusCompositionCustomizationDraft | null>(null);
  const [opportunities, setOpportunities] =
    useState<WorldFocusCompositionCustomizationOpportunitiesState>({
      status: 'idle',
    });
  const [issue, setIssue] =
    useState<WorldFocusCompositionCustomizationIssue | null>(null);
  const [readCoordinator] = useState(() => new WorldFocusLatestReadCoordinator());
  const invokerRef = useRef<HTMLElement | null>(null);
  const surfaceWasOpenRef = useRef(false);
  const applyingRef = useRef(false);

  if (workspace.state.worldId !== worldId) {
    throw new Error('World Focus customization owner belongs to another World');
  }

  const isOpen = workspace.state.surfaces.some(
    (surface) =>
      surface.instanceId === WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_ID,
  );

  const restoreFocus = useCallback(() => {
    const invoker = invokerRef.current;
    queueMicrotask(() => {
      if (invoker?.isConnected === true) {
        invoker.focus({ preventScroll: true });
      }
    });
  }, []);

  const resetDraftState = useCallback(() => {
    readCoordinator.cancelCurrent();
    setDraft(null);
    setOpportunities({ status: 'idle' });
    setIssue(null);
  }, [readCoordinator]);

  const readOpportunities = useCallback(() => {
    const lease = readCoordinator.begin();
    setOpportunities({ status: 'loading' });

    void reader(worldId, lease.signal)
      .then((set) => {
        lease.commit(() => setOpportunities({ status: 'ready', set }));
      })
      .catch(() => {
        if (lease.signal.aborted) return;
        lease.commit(() => setOpportunities({ status: 'error' }));
      })
      .finally(() => lease.release());
  }, [readCoordinator, reader, worldId]);

  const begin = useCallback(
    (invoker: HTMLElement) => {
      if (
        draft !== null ||
        isOpen ||
        getWorldFocusBlockingSurface(workspace.state) !== null
      ) {
        return;
      }

      invokerRef.current = invoker;
      setIssue(null);
      setDraft(beginWorldFocusCompositionCustomization(acceptedConfig));
      readOpportunities();
      workspace.openSurface({
        instanceId: WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_ID,
        kind: WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_KIND,
        // `explore` is the existing deep-interaction metadata token. It does
        // not turn composition customization into Output Grammar O9 Explore.
        depth: 'explore',
        presentation: 'sidecar',
        origin: 'user',
        contextReference: null,
        dismissible: true,
        expectedWorkspace: {
          worldId: workspace.state.worldId,
          generation: workspace.state.generation,
        },
      });
    }, [acceptedConfig, draft, isOpen, readOpportunities, workspace]);

  const execute = useCallback(
    (command: WorldFocusCompositionCustomizationCommand): boolean => {
      if (draft === null) return false;
      try {
        const next = updateWorldFocusCompositionDraft(draft, command);
        setDraft(next);
        setIssue(null);
        return true;
      } catch {
        setIssue({ status: 'invalid-state' });
        return false;
      }
    },
    [draft],
  );

  const cancel = useCallback(() => {
    if (draft === null) return;
    resetDraftState();
    workspace.closeSurface(WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_ID);
    restoreFocus();
  }, [draft, resetDraftState, restoreFocus, workspace]);

  const apply = useCallback(() => {
    if (draft === null || applyingRef.current) return;
    applyingRef.current = true;
    try {
      const result = applyDraft(acceptedConfig, draft);
      if (result.status === 'revision-conflict') {
        setIssue(result);
        return;
      }

      setAcceptedConfig(result.config);
      resetDraftState();
      workspace.closeSurface(WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_ID);
      restoreFocus();
    } catch {
      setIssue({ status: 'invalid-state' });
    } finally {
      applyingRef.current = false;
    }
  }, [acceptedConfig, applyDraft, draft, resetDraftState, restoreFocus, workspace]);

  useEffect(() => {
    if (isOpen) {
      surfaceWasOpenRef.current = true;
      return;
    }

    if (surfaceWasOpenRef.current && draft !== null) {
      surfaceWasOpenRef.current = false;
      resetDraftState();
      restoreFocus();
    }
  }, [draft, isOpen, resetDraftState, restoreFocus]);

  useEffect(
    () => () => {
      readCoordinator.cancelCurrent();
    },
    [readCoordinator],
  );

  const value = useMemo<WorldFocusCompositionCustomizationContextValue>(
    () => ({
      worldLabel,
      acceptedConfig,
      draft,
      opportunities,
      issue,
      isDirty: draft === null ? false : !sameConfig(draft.baseConfig, draft.workingConfig),
      isOpen,
      begin,
      retryOpportunities: readOpportunities,
      execute,
      apply,
      cancel,
    }),
    [
      acceptedConfig,
      apply,
      begin,
      cancel,
      draft,
      execute,
      isOpen,
      issue,
      opportunities,
      readOpportunities,
      worldLabel,
    ],
  );

  return (
    <WorldFocusCompositionCustomizationContext.Provider value={value}>
      {children}
    </WorldFocusCompositionCustomizationContext.Provider>
  );
}

export function useWorldFocusCompositionCustomization(): WorldFocusCompositionCustomizationContextValue {
  const value = useContext(WorldFocusCompositionCustomizationContext);
  if (value === null) {
    throw new Error(
      'useWorldFocusCompositionCustomization must be used inside WorldFocusCompositionCustomizationProvider',
    );
  }
  return value;
}

export function WorldFocusCompositionCustomizeInvoke() {
  const { t } = useTranslation('common');
  const customization = useWorldFocusCompositionCustomization();

  return (
    <button
      className="world-focus-composition-customize-invoke"
      type="button"
      aria-expanded={customization.isOpen}
      onClick={(event) => customization.begin(event.currentTarget)}
    >
      {t(($) => $.common.worldFocus.customization.invoke)}
    </button>
  );
}
