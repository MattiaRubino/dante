import { createPortal } from 'react-dom';

import {
  WorldFocusAllocatedSurface,
  type WorldFocusSurfaceLayerRegistry,
} from './world-focus-surface-layer';
import { useWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation-context';

type WorldFocusRouteSurfaceLayerProps = Readonly<{
  registry: WorldFocusSurfaceLayerRegistry;
  host: HTMLElement | null;
}>;

/**
 * Presents only allocation slot `external` into a route-owned DOM host. The
 * component remains inside the Workspace/World React ownership tree so it
 * consumes the same reducer, allocation plan, registry and render boundary,
 * while its DOM is no longer trapped inside the rectangular World workspace.
 */
export function WorldFocusRouteSurfaceLayer({
  registry,
  host,
}: WorldFocusRouteSurfaceLayerProps) {
  const allocation = useWorldFocusWorkspaceAllocation();
  const activeExternalPlacements = allocation.placements.filter(
    (placement) => placement.activeInSlot && placement.slot === 'external',
  );

  if (host === null || activeExternalPlacements.length === 0) {
    return null;
  }

  return createPortal(
    <div
      className="world-focus-route-surface-layer"
      data-world-focus-route-surface-count={activeExternalPlacements.length}
    >
      {activeExternalPlacements.map((placement) => (
        <WorldFocusAllocatedSurface
          key={placement.instanceId}
          registry={registry}
          placement={placement}
        />
      ))}
    </div>,
    host,
  );
}
