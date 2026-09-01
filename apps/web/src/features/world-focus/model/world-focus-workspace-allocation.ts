import type {
  WorldFocusPresentationSurface,
} from './world-focus-platform';
import type {
  WorldFocusSurfaceDescriptor,
  WorldFocusWorkspaceState,
} from './world-focus-workspace';

export const WORLD_FOCUS_MAIN_ALLOCATIONS = ['full', 'split'] as const;

export type WorldFocusMainAllocation =
  (typeof WORLD_FOCUS_MAIN_ALLOCATIONS)[number];

export const WORLD_FOCUS_TOP_LAYERS = ['none', 'overlay', 'focus'] as const;

export type WorldFocusTopLayer = (typeof WORLD_FOCUS_TOP_LAYERS)[number];

export const WORLD_FOCUS_MAIN_INTERACTIONS = ['interactive', 'inert'] as const;

export type WorldFocusMainInteraction =
  (typeof WORLD_FOCUS_MAIN_INTERACTIONS)[number];

export const WORLD_FOCUS_SURFACE_SLOTS = [
  'sidecar',
  'overlay',
  'focus',
  'dormant',
  'external',
] as const;

export type WorldFocusSurfaceSlot =
  (typeof WORLD_FOCUS_SURFACE_SLOTS)[number];

export type WorldFocusWorkspaceAllocationPolicy = Readonly<{
  minSplitInlineSize: number;
  minMainInlineSize: number;
  minSidecarInlineSize: number;
  maxSidecarInlineSize: number;
  preferredSidecarFraction: number;
  splitGap: number;
}>;

export const DEFAULT_WORLD_FOCUS_WORKSPACE_ALLOCATION_POLICY: WorldFocusWorkspaceAllocationPolicy =
  Object.freeze({
    minSplitInlineSize: 900,
    minMainInlineSize: 520,
    minSidecarInlineSize: 300,
    maxSidecarInlineSize: 420,
    preferredSidecarFraction: 0.36,
    splitGap: 16,
  });

export type WorldFocusSurfacePlacement = Readonly<{
  instanceId: string;
  requestedPresentation: WorldFocusPresentationSurface;
  slot: WorldFocusSurfaceSlot;
  activeInSlot: boolean;
}>;

export type WorldFocusWorkspaceAllocationPlan = Readonly<{
  mainAllocation: WorldFocusMainAllocation;
  topLayer: WorldFocusTopLayer;
  mainInteraction: WorldFocusMainInteraction;
  workspaceInlineSize: number;
  mainInlineSize: number;
  sidecarInlineSize: number | null;
  splitGap: number;
  activeSidecarInstanceId: string | null;
  activeOverlayInstanceId: string | null;
  activeFocusInstanceId: string | null;
  topSurfaceInstanceId: string | null;
  placements: readonly WorldFocusSurfacePlacement[];
}>;

function assertFiniteNonNegative(value: number, label: string): number {
  if (!Number.isFinite(value) || value < 0) {
    throw new Error(`${label} must be a finite non-negative number`);
  }
  return value;
}

function assertPolicy(
  policy: WorldFocusWorkspaceAllocationPolicy,
): WorldFocusWorkspaceAllocationPolicy {
  const minSplitInlineSize = assertFiniteNonNegative(
    policy.minSplitInlineSize,
    'World Focus minimum split inline size',
  );
  const minMainInlineSize = assertFiniteNonNegative(
    policy.minMainInlineSize,
    'World Focus minimum main inline size',
  );
  const minSidecarInlineSize = assertFiniteNonNegative(
    policy.minSidecarInlineSize,
    'World Focus minimum sidecar inline size',
  );
  const maxSidecarInlineSize = assertFiniteNonNegative(
    policy.maxSidecarInlineSize,
    'World Focus maximum sidecar inline size',
  );
  const splitGap = assertFiniteNonNegative(
    policy.splitGap,
    'World Focus split gap',
  );

  if (
    !Number.isFinite(policy.preferredSidecarFraction) ||
    policy.preferredSidecarFraction <= 0 ||
    policy.preferredSidecarFraction >= 1
  ) {
    throw new Error(
      'World Focus preferred sidecar fraction must be greater than 0 and less than 1',
    );
  }
  if (minSidecarInlineSize > maxSidecarInlineSize) {
    throw new Error(
      'World Focus minimum sidecar inline size must not exceed maximum sidecar inline size',
    );
  }
  if (
    minSplitInlineSize <
    minMainInlineSize + minSidecarInlineSize + splitGap
  ) {
    throw new Error(
      'World Focus minimum split inline size cannot satisfy main, sidecar and gap minima',
    );
  }

  return Object.freeze({
    minSplitInlineSize,
    minMainInlineSize,
    minSidecarInlineSize,
    maxSidecarInlineSize,
    preferredSidecarFraction: policy.preferredSidecarFraction,
    splitGap,
  });
}

function clamp(value: number, minimum: number, maximum: number): number {
  return Math.min(Math.max(value, minimum), maximum);
}

function findLatestSurfaceByPresentation(
  surfaces: readonly WorldFocusSurfaceDescriptor[],
  presentation: WorldFocusPresentationSurface,
): WorldFocusSurfaceDescriptor | null {
  for (let index = surfaces.length - 1; index >= 0; index -= 1) {
    const surface = surfaces[index];
    if (surface?.presentation === presentation) {
      return surface;
    }
  }
  return null;
}

function getTopSurface(
  surfaces: readonly WorldFocusSurfaceDescriptor[],
): WorldFocusSurfaceDescriptor | null {
  return surfaces.at(-1) ?? null;
}

function isOverlayPresentation(
  presentation: WorldFocusPresentationSurface,
): boolean {
  return presentation === 'popover' || presentation === 'modal';
}

function isWorkspaceLayerPresentation(
  presentation: WorldFocusPresentationSurface,
): boolean {
  return (
    presentation === 'sidecar' ||
    presentation === 'popover' ||
    presentation === 'modal' ||
    presentation === 'full-screen'
  );
}

function findTopWorkspaceLayerSurface(
  surfaces: readonly WorldFocusSurfaceDescriptor[],
): WorldFocusSurfaceDescriptor | null {
  for (let index = surfaces.length - 1; index >= 0; index -= 1) {
    const surface = surfaces[index];
    if (surface !== undefined && isWorkspaceLayerPresentation(surface.presentation)) {
      return surface;
    }
  }
  return null;
}

/**
 * Resolves how transient/deeper surfaces consume the already-owned rectangular
 * World workspace. It never ranks World content, knows World identity, or owns
 * canonical truth.
 *
 * The plan deliberately separates three independent concerns:
 * - mainAllocation: whether a sidecar consumes real canvas width;
 * - topLayer: whether an overlay/focus surface sits above that canvas;
 * - mainInteraction: whether the main plane remains operable underneath it.
 *
 * This means a wide sidecar can remain allocated while a confirmation modal or
 * focused Explore surface temporarily sits above it. Narrow sidecars degrade to
 * a non-modal overlay without changing their requested presentation contract.
 */
export function resolveWorldFocusWorkspaceAllocation(
  state: WorldFocusWorkspaceState,
  workspaceInlineSize: number,
  policy: WorldFocusWorkspaceAllocationPolicy =
    DEFAULT_WORLD_FOCUS_WORKSPACE_ALLOCATION_POLICY,
): WorldFocusWorkspaceAllocationPlan {
  const inlineSize = assertFiniteNonNegative(
    workspaceInlineSize,
    'World Focus workspace inline size',
  );
  const resolvedPolicy = assertPolicy(policy);
  const activeSidecar = findLatestSurfaceByPresentation(
    state.surfaces,
    'sidecar',
  );
  const topSurface = getTopSurface(state.surfaces);
  const topWorkspaceLayerSurface = findTopWorkspaceLayerSurface(state.surfaces);

  const preferredSidecarInlineSize = clamp(
    inlineSize * resolvedPolicy.preferredSidecarFraction,
    resolvedPolicy.minSidecarInlineSize,
    resolvedPolicy.maxSidecarInlineSize,
  );
  const canSplit =
    activeSidecar !== null &&
    inlineSize >= resolvedPolicy.minSplitInlineSize &&
    inlineSize - resolvedPolicy.splitGap - preferredSidecarInlineSize >=
      resolvedPolicy.minMainInlineSize;

  const sidecarInlineSize = canSplit ? preferredSidecarInlineSize : null;
  const mainInlineSize =
    sidecarInlineSize === null
      ? inlineSize
      : inlineSize - resolvedPolicy.splitGap - sidecarInlineSize;

  const activeLayerSurface =
    topWorkspaceLayerSurface?.presentation === 'sidecar' && canSplit
      ? null
      : topWorkspaceLayerSurface;
  const activeFocusSurface =
    activeLayerSurface?.presentation === 'full-screen'
      ? activeLayerSurface
      : null;
  const activeOverlaySurface =
    activeLayerSurface !== null &&
    (activeLayerSurface.presentation === 'sidecar' ||
      isOverlayPresentation(activeLayerSurface.presentation))
      ? activeLayerSurface
      : null;
  const mainInteraction: WorldFocusMainInteraction =
    activeFocusSurface !== null || activeOverlaySurface?.presentation === 'modal'
      ? 'inert'
      : 'interactive';

  const placements = state.surfaces.map<WorldFocusSurfacePlacement>((surface) => {
    if (surface.presentation === 'route') {
      return Object.freeze({
        instanceId: surface.instanceId,
        requestedPresentation: surface.presentation,
        slot: 'external' as const,
        activeInSlot: surface === topSurface,
      });
    }

    if (surface.presentation === 'sidecar') {
      if (surface !== activeSidecar) {
        return Object.freeze({
          instanceId: surface.instanceId,
          requestedPresentation: surface.presentation,
          slot: 'dormant' as const,
          activeInSlot: false,
        });
      }

      if (canSplit) {
        return Object.freeze({
          instanceId: surface.instanceId,
          requestedPresentation: surface.presentation,
          slot: 'sidecar' as const,
          activeInSlot: true,
        });
      }

      return Object.freeze({
        instanceId: surface.instanceId,
        requestedPresentation: surface.presentation,
        slot:
          surface === activeOverlaySurface
            ? ('overlay' as const)
            : ('dormant' as const),
        activeInSlot: surface === activeOverlaySurface,
      });
    }

    if (surface.presentation === 'full-screen') {
      return Object.freeze({
        instanceId: surface.instanceId,
        requestedPresentation: surface.presentation,
        slot:
          surface === activeFocusSurface
            ? ('focus' as const)
            : ('dormant' as const),
        activeInSlot: surface === activeFocusSurface,
      });
    }

    if (isOverlayPresentation(surface.presentation)) {
      return Object.freeze({
        instanceId: surface.instanceId,
        requestedPresentation: surface.presentation,
        slot:
          surface === activeOverlaySurface
            ? ('overlay' as const)
            : ('dormant' as const),
        activeInSlot: surface === activeOverlaySurface,
      });
    }

    return Object.freeze({
      instanceId: surface.instanceId,
      requestedPresentation: surface.presentation,
      slot: 'dormant' as const,
      activeInSlot: false,
    });
  });

  return Object.freeze({
    mainAllocation: canSplit ? 'split' : 'full',
    topLayer:
      activeFocusSurface !== null
        ? 'focus'
        : activeOverlaySurface !== null
          ? 'overlay'
          : 'none',
    mainInteraction,
    workspaceInlineSize: inlineSize,
    mainInlineSize,
    sidecarInlineSize,
    splitGap: canSplit ? resolvedPolicy.splitGap : 0,
    activeSidecarInstanceId: canSplit ? activeSidecar?.instanceId ?? null : null,
    activeOverlayInstanceId: activeOverlaySurface?.instanceId ?? null,
    activeFocusInstanceId: activeFocusSurface?.instanceId ?? null,
    topSurfaceInstanceId: topSurface?.instanceId ?? null,
    placements: Object.freeze(placements),
  });
}
