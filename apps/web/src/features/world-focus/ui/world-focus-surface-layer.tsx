import { useTranslation } from 'react-i18next';

import { WorldFocusRenderBoundary } from './world-focus-render-boundary';
import {
  WorldFocusSurfaceRegistry,
  type WorldFocusSurfaceRegistration,
} from './world-focus-surface-registry';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

type WorldFocusSurfaceLayerProps = Readonly<{
  registry: WorldFocusSurfaceRegistry<WorldFocusSurfaceRegistration>;
}>;

/**
 * Renders transient/deeper workspace surfaces from finite shipped
 * registrations. Unknown kinds and renderer failures degrade locally and never
 * become a second route/page failure boundary.
 */
export function WorldFocusSurfaceLayer({
  registry,
}: WorldFocusSurfaceLayerProps) {
  const { t } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();

  if (workspace.state.surfaces.length === 0) {
    return null;
  }

  return (
    <div
      className="world-focus-surface-layer"
      data-world-focus-surface-count={workspace.state.surfaces.length}
    >
      {workspace.state.surfaces.map((surface) => {
        const registration = registry.resolve(surface.kind);
        const isCurrentGeneration =
          surface.boundGeneration === workspace.state.generation;
        const requestClose = () => workspace.closeSurface(surface.instanceId);

        if (registration === null) {
          return (
            <section
              key={surface.instanceId}
              className="world-focus-surface world-focus-surface-unsupported"
              data-world-focus-surface-id={surface.instanceId}
              data-world-focus-surface-kind={surface.kind}
              data-world-focus-surface-status="unsupported"
              role="alert"
            >
              <p>{t(($) => $.common.worldFocus.surfaces.unavailable)}</p>
              {surface.dismissible ? (
                <button type="button" onClick={requestClose}>
                  {t(($) => $.common.worldFocus.surfaces.close)}
                </button>
              ) : null}
            </section>
          );
        }

        return (
          <div
            key={surface.instanceId}
            className="world-focus-surface"
            data-world-focus-surface-id={surface.instanceId}
            data-world-focus-surface-kind={surface.kind}
            data-world-focus-surface-depth={surface.depth}
            data-world-focus-surface-presentation={surface.presentation}
            data-world-focus-surface-origin={surface.origin}
            data-world-focus-surface-generation={surface.boundGeneration}
            data-world-focus-surface-current={
              isCurrentGeneration ? 'true' : 'false'
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
      })}
    </div>
  );
}
