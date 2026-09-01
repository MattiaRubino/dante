import {
  WorldFocusDanteComposer,
  WORLD_FOCUS_DANTE_COMPOSER_KIND,
} from './world-focus-dante-entry';
import {
  WorldFocusSurfaceRegistry,
  type WorldFocusSurfaceRegistration,
} from './world-focus-surface-registry';

const CORE_WORLD_FOCUS_SURFACE_REGISTRY = new WorldFocusSurfaceRegistry<
  WorldFocusSurfaceRegistration
>([
  {
    kind: WORLD_FOCUS_DANTE_COMPOSER_KIND,
    render: ({ onRequestClose }) => (
      <WorldFocusDanteComposer onRequestClose={onRequestClose} />
    ),
  },
]);

/**
 * Finite shipped World surface registry. Concrete kinds are added only by real
 * product verticals; remote/model-generated executable UI never enters here.
 */
export function getCoreWorldFocusSurfaceRegistry() {
  return CORE_WORLD_FOCUS_SURFACE_REGISTRY;
}
