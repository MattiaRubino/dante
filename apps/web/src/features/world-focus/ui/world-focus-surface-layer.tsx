import { useTranslation } from 'react-i18next';

import type { WorldFocusSurfacePlacement } from '../model/world-focus-workspace-allocation';
import { WorldFocusRenderBoundary } from './world-focus-render-boundary';
import {
  WorldFocusSurfaceRegistry,
  type WorldFocusSurfaceRegistration,
} from './world-focus-surface-registry';
import { useWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation-context';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export type WorldFocusSurfaceLayerRegistry = WorldFocusSurfaceRegistry<
  WorldFocusSurfaceRegistration
>;

type WorldFocusSurfaceLayerProps = Readonly<{
  registry: WorldFocusSurfaceLayerRegistry;
}>;

type WorldFocusAllocatedSurfaceProps = Readonly<{
  registry: WorldFocusSurfaceLayerRegistry;
  placement: WorldFocusSurfacePlacement;
}>;

/**
 * Shared renderer for an allocation placement that has already been selected
 * by Workspace ownership. Workspace-local and route-owned presenters both use
 * this path so registry lookup, unsupported-kind fallback and renderer error
 * isolation cannot drift between presentation surfaces.
 */
export function WorldFocusAllocatedSurface({
  registry,
  placement,
}: WorldFocusAllocatedSurfaceProps) {
  const { t } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();
  const surface = workspace.state.surfaces.find(
    (candidate) => candidate.instanceId === placement.instanceId,
  );

  if (surface === undefined) {
    return null;
  }

  const registration = registry.resolve(surface.kind);
  const isCurrentGeneration =
    surface.boundGeneration === workspace.state.generation;
  const requestClose = () => workspace.closeSurface(surface.instanceId);
  const surfaceIsInert = placement.interaction === 'inert';
  const wrapperIsPointerTransparent = surface.presentation === 'popover';

  if (registration === null) {
    return (
      <section
        className="world-focus-surface world-focus-surface-unsupported"
        data-world-focus-surface-id={surface.instanceId}
        data-world-focus-surface-kind={surface.kind}
        data-world-focus-surface-presentation={surface.presentation}
        data-world-focus-surface-slot={placement.slot}
        data-world-focus-surface-interaction={placement.interaction}
        data-world-focus-surface-status="unsupported"
        inert={surfaceIsInert ? true : undefined}
        role="alert"
        style={
          wrapperIsPointerTransparent ? { pointerEvents: 'none' } : undefined
        }
      >
        <p>{t(($) => $.common.worldFocus.surfaces.unavailable)}</p>
        {surface.dismissible ? (
          <button
            type="button"
            onClick={requestClose}
            style={
              wrapperIsPointerTransparent ? { pointerEvents: 'auto' } : undefined
            }
          >
            {t(($) => $.common.worldFocus.surfaces.close)}
          </button>
        ) : null}
      </section>
    );
  }

  return (
    <div
      className="world-focus-surface"
      data-world-focus-surface-id={surface.instanceId}
      data-world-focus-surface-kind={surface.kind}
      data-world-focus-surface-depth={surface.depth}
      data-world-focus-surface-presentation={surface.presentation}
      data-world-focus-surface-slot={placement.slot}
      data-world-focus-surface-interaction={placement.interaction}
      data-world-focus-surface-origin={surface.origin}
      data-world-focus-surface-generation={surface.boundGeneration}
      data-world-focus-surface-current={
        isCurrentGeneration ? 'true' : 'false'
      }
      inert={surfaceIsInert ? true : undefined}
      style={
        wrapperIsPointerTransparent ? { pointerEvents: 'none' } : undefined
      }
    >
      <WorldFocusRenderBoundary
        resetKey={`${surface.instanceId}:${surface.kind}:${surface.boundGeneration}`}
        fallback={({ reset }) => (
          <section
            className="world-focus-surface world-focus-surface-degraded"
            data-world-focus-surface-status="error"
            role="alert"
          >
            <p>{t(($) => $.common.worldFocus.surfaces.error)}</p>
            <button type="button" onClick={reset}>
              {t(($) => $.common.worldFocus.states.retry)}
            </button>
            {surface.dismissible ? (
              <button type="button" onClick={requestClose}>
                {t(($) => $.common.worldFocus.surfaces.close)}
              </button>
            ) : null}
          </section>
        )}
      >
        {registration.render({
          surface,
          isCurrentGeneration,
          onRequestClose: requestClose,
        })}
      </WorldFocusRenderBoundary>
    </div>
  );
}

/**
 * Renders only Workspace-local surfaces that the allocation plan has made
 * active. External route presentations are rendered by the route-owned layer
 * through the same WorldFocusAllocatedSurface implementation above.
 */
export function WorldFocusSurfaceLayer({
  registry,
}: WorldFocusSurfaceLayerProps) {
  const allocation = useWorldFocusWorkspaceAllocation();
  const activePlacements = allocation.placements.filter(
    (placement) =>
      placement.activeInSlot &&
      placement.slot !== 'dormant' &&
      placement.slot !== 'external',
  );

  if (activePlacements.length === 0) {
    return null;
  }

  return (
    <div
      className="world-focus-surface-layer"
      data-world-focus-surface-count={activePlacements.length}
      data-world-focus-top-layer={allocation.topLayer}
    >
      {activePlacements.map((placement) => (
        <WorldFocusAllocatedSurface
          key={placement.instanceId}
          registry={registry}
          placement={placement}
        />
      ))}
    </div>
  );
}
