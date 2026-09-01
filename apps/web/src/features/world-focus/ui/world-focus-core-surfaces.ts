import {
  WorldFocusSurfaceRegistry,
  type WorldFocusSurfaceRegistration,
} from './world-focus-surface-registry';

const CORE_WORLD_FOCUS_SURFACE_REGISTRY = new WorldFocusSurfaceRegistry<
  WorldFocusSurfaceRegistration
>([]);

/**
 * Starts intentionally empty. Concrete DANTE/Insight/Explore/specialist
 * surfaces are registered only when their real vertical is implemented.
 */
export function getCoreWorldFocusSurfaceRegistry() {
  return CORE_WORLD_FOCUS_SURFACE_REGISTRY;
}
