import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useReducer,
  type ReactNode,
} from 'react';

import type {
  WorldFocusContextReference,
  WorldFocusContextReferenceSet,
} from '../model/world-focus-context-reference';
import type {
  WorldFocusInteractionDepth,
  WorldFocusPresentationSurface,
} from '../model/world-focus-platform';
import {
  createWorldFocusWorkspaceState,
  getWorldFocusEscapeDisposition,
  getWorldFocusInteractionCursor,
  reduceWorldFocusWorkspaceState,
  type WorldFocusEscapeDisposition,
  type WorldFocusInteractionCursor,
  type WorldFocusSurfaceRequest,
  type WorldFocusWorkspaceExpectation,
  type WorldFocusWorkspaceIntent,
  type WorldFocusWorkspaceState,
} from '../model/world-focus-workspace';

export type WorldFocusWorkspaceApi = Readonly<{
  state: WorldFocusWorkspaceState;
  cursor: WorldFocusInteractionCursor;
  selectContext: (reference: WorldFocusContextReference) => void;
  setContextReferences: (references: WorldFocusContextReferenceSet) => void;
  clearContext: () => void;
  openSurface: (surface: WorldFocusSurfaceRequest) => void;
  replaceSurface: (
    instanceId: string,
    surface: WorldFocusSurfaceRequest,
  ) => void;
  promoteSurface: (
    instanceId: string,
    depth: WorldFocusInteractionDepth,
    presentation: WorldFocusPresentationSurface,
    expectedWorkspace?: WorldFocusWorkspaceExpectation,
    blocksWorkspaceInteraction?: boolean,
  ) => void;
  closeSurface: (instanceId: string) => void;
  requestEscape: () => WorldFocusEscapeDisposition;
}>;

const WorldFocusWorkspaceContext = createContext<WorldFocusWorkspaceApi | null>(
  null,
);

type WorldFocusWorkspaceHostProps = Readonly<{
  worldId: string;
  children: ReactNode;
}>;

function workspaceReducer(
  state: WorldFocusWorkspaceState,
  intent: WorldFocusWorkspaceIntent,
): WorldFocusWorkspaceState {
  return reduceWorldFocusWorkspaceState(state, intent);
}

function WorldFocusWorkspaceHostInstance({
  worldId,
  children,
}: WorldFocusWorkspaceHostProps) {
  const [state, dispatch] = useReducer(
    workspaceReducer,
    worldId,
    createWorldFocusWorkspaceState,
  );

  const selectContext = useCallback((reference: WorldFocusContextReference) => {
    dispatch({ type: 'select-context', reference });
  }, []);

  const setContextReferences = useCallback(
    (references: WorldFocusContextReferenceSet) => {
      dispatch({ type: 'set-context', references });
    },
    [],
  );

  const clearContext = useCallback(() => {
    dispatch({ type: 'clear-context' });
  }, []);

  const openSurface = useCallback((surface: WorldFocusSurfaceRequest) => {
    dispatch({ type: 'open-surface', surface });
  }, []);

  const replaceSurface = useCallback(
    (instanceId: string, surface: WorldFocusSurfaceRequest) => {
      dispatch({ type: 'replace-surface', instanceId, surface });
    },
    [],
  );

  const promoteSurface = useCallback(
    (
      instanceId: string,
      depth: WorldFocusInteractionDepth,
      presentation: WorldFocusPresentationSurface,
      expectedWorkspace?: WorldFocusWorkspaceExpectation,
      blocksWorkspaceInteraction?: boolean,
    ) => {
      const baseIntent = {
        type: 'promote-surface' as const,
        instanceId,
        depth,
        presentation,
      };

      if (
        expectedWorkspace === undefined &&
        blocksWorkspaceInteraction === undefined
      ) {
        dispatch(baseIntent);
        return;
      }
      if (expectedWorkspace === undefined) {
        dispatch({ ...baseIntent, blocksWorkspaceInteraction });
        return;
      }
      if (blocksWorkspaceInteraction === undefined) {
        dispatch({ ...baseIntent, expectedWorkspace });
        return;
      }
      dispatch({
        ...baseIntent,
        expectedWorkspace,
        blocksWorkspaceInteraction,
      });
    },
    [],
  );

  const closeSurface = useCallback((instanceId: string) => {
    dispatch({ type: 'close-surface', instanceId });
  }, []);

  const requestEscape = useCallback((): WorldFocusEscapeDisposition => {
    const disposition = getWorldFocusEscapeDisposition(state);
    if (disposition === 'surface-dismissible') {
      dispatch({ type: 'close-top-surface' });
    }
    return disposition;
  }, [state]);

  const cursor = useMemo(() => getWorldFocusInteractionCursor(state), [state]);

  const value = useMemo<WorldFocusWorkspaceApi>(
    () => ({
      state,
      cursor,
      selectContext,
      setContextReferences,
      clearContext,
      openSurface,
      replaceSurface,
      promoteSurface,
      closeSurface,
      requestEscape,
    }),
    [
      clearContext,
      closeSurface,
      cursor,
      openSurface,
      promoteSurface,
      replaceSurface,
      requestEscape,
      selectContext,
      setContextReferences,
      state,
    ],
  );

  return (
    <WorldFocusWorkspaceContext.Provider value={value}>
      {children}
    </WorldFocusWorkspaceContext.Provider>
  );
}

/**
 * Owns only transient workspace interaction state for the current mounted
 * World. The keyed inner owner guarantees that changing worldId cannot retain
 * another World's context/surface state even when a caller forgets to key the
 * host itself. Durable truth, authorization and DANTE Run lifetime remain
 * outside this frontend host.
 */
export function WorldFocusWorkspaceHost({
  worldId,
  children,
}: WorldFocusWorkspaceHostProps) {
  return (
    <WorldFocusWorkspaceHostInstance key={worldId} worldId={worldId}>
      {children}
    </WorldFocusWorkspaceHostInstance>
  );
}

export function useWorldFocusWorkspace(): WorldFocusWorkspaceApi {
  const value = useContext(WorldFocusWorkspaceContext);
  if (value === null) {
    throw new Error(
      'useWorldFocusWorkspace must be used inside WorldFocusWorkspaceHost',
    );
  }
  return value;
}
