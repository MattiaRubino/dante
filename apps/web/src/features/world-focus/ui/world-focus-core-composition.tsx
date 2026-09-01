import { defineWorldFocusComposition } from '../model/world-focus-composition';
import { WorldFocusContinuity } from './world-focus-continuity';
import {
  type WorldFocusCompositionRegistration,
} from './world-focus-composition-host';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';

const CORE_WORLD_FOCUS_COMPOSITION = defineWorldFocusComposition([
  {
    instanceId: 'continuity',
    kind: 'continuity',
    ownership: {
      stability: 'adaptive',
      origin: 'application-derived',
    },
  },
] as const);

const CORE_WORLD_FOCUS_MODULE_REGISTRY = new WorldFocusModuleRegistry<
  WorldFocusCompositionRegistration
>([
  {
    kind: 'continuity',
    render: ({ worldId }) => <WorldFocusContinuity worldId={worldId} />,
  },
]);

/**
 * Current pre-backend composition input. It is deliberately tiny: this proves
 * that WorldFocusPage no longer owns concrete module rendering without
 * pretending that a full dynamic ranking resolver already exists.
 */
export function getCoreWorldFocusComposition() {
  return CORE_WORLD_FOCUS_COMPOSITION;
}

export function getCoreWorldFocusModuleRegistry() {
  return CORE_WORLD_FOCUS_MODULE_REGISTRY;
}
