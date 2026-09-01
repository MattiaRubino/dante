import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

import type { WorldFocusCompositionEntry } from '../model/world-focus-composition';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';
import { WorldFocusRenderBoundary } from './world-focus-render-boundary';

export type WorldFocusCompositionRendererProps<Kind extends string = string> =
  Readonly<{
    worldId: string;
    entry: WorldFocusCompositionEntry<Kind>;
  }>;

export type WorldFocusCompositionRegistration<Kind extends string = string> =
  Readonly<{
    kind: Kind;
    render: (props: WorldFocusCompositionRendererProps<Kind>) => ReactNode;
  }>;

type WorldFocusCompositionHostProps = Readonly<{
  worldId: string;
  entries: readonly WorldFocusCompositionEntry[];
  registry: WorldFocusModuleRegistry<WorldFocusCompositionRegistration>;
}>;

/**
 * Owns outer placement and isolation for already-resolved World composition.
 * It deliberately does not decide ranking, canonical meaning or authorization.
 */
export function WorldFocusCompositionHost({
  worldId,
  entries,
  registry,
}: WorldFocusCompositionHostProps) {
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
