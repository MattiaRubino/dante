import {
  resolveWorldFocusCompositionPlan,
  type WorldFocusCompositionCandidate,
  type WorldFocusCompositionPolicy,
} from '../model/world-focus-composition-plan';
import type { WorldFocusId } from '../model/world-focus-fixtures';
import { type WorldFocusCompositionRegistration } from './world-focus-composition-host';
import { WorldFocusContinuity } from './world-focus-continuity';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';

const CORE_WORLD_FOCUS_COMPOSITION_POLICY: WorldFocusCompositionPolicy =
  Object.freeze({
    maxAdaptiveEntries: 4,
    maxEphemeralEntries: 2,
  });

const CORE_WORLD_FOCUS_COMPOSITION_CANDIDATES: readonly WorldFocusCompositionCandidate[] =
  Object.freeze([
    Object.freeze({
      instanceId: 'continuity',
      kind: 'continuity',
      ownership: Object.freeze({
        stability: 'adaptive',
        origin: 'application-derived',
      }),
      prominence: 'primary',
      footprint: 'standard',
      order: 0,
    }),
  ]);

const CORE_WORLD_FOCUS_COMPOSITION_PLAN = resolveWorldFocusCompositionPlan(
  CORE_WORLD_FOCUS_COMPOSITION_CANDIDATES,
  CORE_WORLD_FOCUS_COMPOSITION_POLICY,
);

const CORE_WORLD_FOCUS_MODULE_REGISTRY = new WorldFocusModuleRegistry<
  WorldFocusCompositionRegistration<string, WorldFocusId>
>([
  {
    kind: 'continuity',
    render: ({ worldId }) => <WorldFocusContinuity worldId={worldId} />,
  },
]);

/**
 * Current pre-backend composition input. The candidate list is intentionally
 * tiny, but it now travels through the same planner that future World output
 * candidates use instead of being placed directly by WorldFocusPage.
 */
export function getCoreWorldFocusComposition() {
  return CORE_WORLD_FOCUS_COMPOSITION_PLAN;
}

export function getCoreWorldFocusModuleRegistry() {
  return CORE_WORLD_FOCUS_MODULE_REGISTRY;
}
