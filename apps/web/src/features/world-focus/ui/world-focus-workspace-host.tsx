import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useReducer,
  useRef,
  type ReactNode,
} from 'react';

import {
  createWorldFocusWorkspaceState,
  getWorldFocusEscapeDisposition,
  reduceWorldFocusWorkspaceState,
  type WorldFocusContextReference,
  type WorldFocusEscapeDisposition,
  type WorldFocusSurfaceRequest,
  type WorldFocusWorkspaceState,
} from '../model/world-focus-workspace';
import type {
  WorldFocusInteractionDepth,
  WorldFocusPresentationSurface,
} from '../model/world-focus-platform';

export type WorldFocusWorkspaceApi = Readonly<{
  state: WorldFocusWorkspaceState;
  selectContext: (reference: WorldFocusContextReference) => void;
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
    expectedGeneration?: number,
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

/**
 * Owns only transient workspace interaction state for the current mounted
 * World. Durable truth, authorization and DANTE Run lifetime remain outside
 * this frontend host.
 */
export function WorldFocusWorkspaceHost({
  worldId,
  children,
}: WorldFocusWorkspaceHostProps) {
  const [state, dispatch] = useReducer(
    reduceWorldFocusWorkspaceState,
    worldId,
    createWorldFocusWorkspaceState,
  );
  const stateRef = useRef(state);
  stateRef.current = state;

  const selectContext = useCallback((reference: WorldFocusContextReference) => {
    dispatch({ type: 'select-context', reference });
  }, []);

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
      expectedGeneration?: number,
    ) => {
      dispatch({
        type: 'promote-surface',
        instanceId,
        depth,
        presentation,
        expectedGeneration,
      });
    },
    [],
  );

  const closeSurface = useCallback((instanceId: string) => {
    dispatch({ type: 'close-surface', instanceId });
  }, []);

  const requestEscape = useCallback((): WorldFocusEscapeDisposition => {
    const disposition = getWorldFocusEscapeDisposition(stateRef.current);
    if (disposition === 'surface-dismissible') {
      dispatch({ type: 'close-top-surface' });
    }
    return disposition;
  }, []);

  const value = useMemo<WorldFocusWorkspaceApi>(
    () => ({
      state,
      selectContext,
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
      openSurface,
      promoteSurface,
      replaceSurface,
      requestEscape,
      selectContext,
      state,
    ],
  );

  return (
    <WorldFocusWorkspaceContext.Provider value={value}>
      {children}
    </WorldFocusWorkspaceContext.Provider>
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
