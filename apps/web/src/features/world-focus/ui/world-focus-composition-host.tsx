import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusCompositionPlanEntry } from '../model/world-focus-composition-plan';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';
import { WorldFocusRenderBoundary } from './world-focus-render-boundary';

export type WorldFocusCompositionRendererProps<
  Kind extends string = string,
  WorldId extends string = string,
> = Readonly<{
  worldId: WorldId;
  entry: WorldFocusCompositionPlanEntry<Kind>;
}>;

export type WorldFocusCompositionRegistration<
  Kind extends string = string,
  WorldId extends string = string,
> = Readonly<{
  kind: Kind;
  render: (
    props: WorldFocusCompositionRendererProps<Kind, WorldId>,
  ) => ReactNode;
}>;

type WorldFocusCompositionHostProps<WorldId extends string = string> = Readonly<{
  worldId: WorldId;
  entries: readonly WorldFocusCompositionPlanEntry[];
  registry: WorldFocusModuleRegistry<
    WorldFocusCompositionRegistration<string, WorldId>
  >;
}>;

/**
 * Owns placement/isolation for an already-resolved World composition plan.
 * Ranking, canonical meaning and authorization remain outside this renderer.
 */
export function WorldFocusCompositionHost<WorldId extends string = string>({
  worldId,
  entries,
  registry,
}: WorldFocusCompositionHostProps<WorldId>) {
  const { t } = useTranslation('common');

  return (
    <div
      className="world-focus-composition"
      data-world-focus-composition-count={entries.length}
    >
      {entries.map((entry) => {
        const registration = registry.resolve(entry.kind);

        if (registration === null) {
          return (
            <section
              key={entry.instanceId}
              className="world-focus-composition-item world-focus-composition-item-unsupported"
              data-world-focus-composition-id={entry.instanceId}
              data-world-focus-module-kind={entry.kind}
              data-world-focus-module-status="unsupported"
              data-world-focus-stability={entry.ownership.stability}
              data-world-focus-origin={entry.ownership.origin}
              data-world-focus-prominence={entry.prominence}
              data-world-focus-footprint={entry.footprint}
              data-world-focus-grid-span={entry.gridSpan}
              data-world-focus-grid-row={entry.row}
              role="alert"
            >
              <p>{t(($) => $.common.worldFocus.surfaces.unavailable)}</p>
            </section>
          );
        }

        return (
          <div
            key={entry.instanceId}
            className="world-focus-composition-item"
            data-world-focus-composition-id={entry.instanceId}
            data-world-focus-module-kind={entry.kind}
            data-world-focus-stability={entry.ownership.stability}
            data-world-focus-origin={entry.ownership.origin}
            data-world-focus-prominence={entry.prominence}
            data-world-focus-footprint={entry.footprint}
            data-world-focus-grid-span={entry.gridSpan}
            data-world-focus-grid-row={entry.row}
          >
            <WorldFocusRenderBoundary
              resetKey={`${worldId}:${entry.instanceId}:${entry.kind}`}
              fallback={({ reset }) => (
                <section
                  className="world-focus-composition-item world-focus-composition-item-degraded"
                  data-world-focus-module-status="error"
                  role="alert"
                >
                  <p>{t(($) => $.common.worldFocus.surfaces.error)}</p>
                  <button type="button" onClick={reset}>
                    {t(($) => $.common.worldFocus.states.retry)}
                  </button>
                </section>
              )}
            >
              {registration.render({ worldId, entry })}
            </WorldFocusRenderBoundary>
          </div>
        );
      })}
    </div>
  );
}
