import { createContext, useContext, type ReactNode } from 'react';

import type { WorldFocusWorkspaceAllocationPlan } from '../model/world-focus-workspace-allocation';

const WorldFocusWorkspaceAllocationContext =
  createContext<WorldFocusWorkspaceAllocationPlan | null>(null);

type WorldFocusWorkspaceAllocationProviderProps = Readonly<{
  plan: WorldFocusWorkspaceAllocationPlan;
  children: ReactNode;
}>;

export function WorldFocusWorkspaceAllocationProvider({
  plan,
  children,
}: WorldFocusWorkspaceAllocationProviderProps) {
  return (
    <WorldFocusWorkspaceAllocationContext.Provider value={plan}>
      {children}
    </WorldFocusWorkspaceAllocationContext.Provider>
  );
}

export function useWorldFocusWorkspaceAllocation(): WorldFocusWorkspaceAllocationPlan {
  const plan = useContext(WorldFocusWorkspaceAllocationContext);
  if (plan === null) {
    throw new Error(
      'useWorldFocusWorkspaceAllocation must be used inside WorldFocusWorkspaceAllocationProvider',
    );
  }
  return plan;
}
