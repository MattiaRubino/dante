import type {
  WorldFocusSurfaceDescriptor,
  WorldFocusWorkspaceState,
} from './world-focus-workspace';

export const WORLD_FOCUS_WORKSPACE_ALLOCATION_MODES = [
  'content',
  'split',
  'overlay',
  'focus',
] as const;

export type WorldFocusWorkspaceAllocationMode =
  (typeof WORLD_FOCUS_WORKSPACE_ALLOCATION_MODES)[number];

export const WORLD_FOCUS_SURFACE_SLOTS = [
  'sidecar',
  'overlay',
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
  requestedPresentation: WorldFocusSurfaceDescriptor['presentation'];
  slot: WorldFocusSurfaceSlot;
  activeInSlot: boolean;
}>;

export type WorldFocusWorkspaceAllocationPlan = Readonly<{
  mode: WorldFocusWorkspaceAllocationMode;
  workspaceInlineSize: number;
  mainInlineSize: number;
  sidecarInlineSize: number | null;
  activeSidecarInstanceId: string | null;
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

function findActiveSidecar(
  surfaces: readonly WorldFocusSurfaceDescriptor[],
): WorldFocusSurfaceDescriptor | null {
  for (let index = surfaces.length - 1; index >= 0; index -= 1) {
    const surface = surfaces[index];
    if (surface?.presentation === 'sidecar') {
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
  presentation: WorldFocusSurfaceDescriptor['presentation'],
): boolean {
  return (
    presentation === 'popover' ||
    presentation === 'modal' ||
    presentation === 'full-screen'
  );
}

/**
 * Resolves how transient/deeper surfaces consume the already-owned rectangular
 * World workspace. It never ranks World content and never knows World identity.
 *
 * - one most-recent sidecar may consume layout space when the allocated
 *   workspace is genuinely wide enough;
 * - older sidecars remain dormant in the interaction stack so close/back can
 *   restore them without rendering competing columns;
 * - popover/modal/full-screen are overlay presentations and never shrink the
 *   composition beneath them;
 * - a requested sidecar degrades to overlay when preserving a useful main
 *   canvas would otherwise fail;
 * - route presentation is external to workspace allocation.
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
  const activeSidecar = findActiveSidecar(state.surfaces);
  const topSurface = getTopSurface(state.surfaces);

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

      return Object.freeze({
        instanceId: surface.instanceId,
        requestedPresentation: surface.presentation,
        slot: canSplit ? ('sidecar' as const) : ('overlay' as const),
        activeInSlot: true,
      });
    }

    if (isOverlayPresentation(surface.presentation)) {
      return Object.freeze({
        instanceId: surface.instanceId,
        requestedPresentation: surface.presentation,
        slot: 'overlay' as const,
        activeInSlot: surface === topSurface,
      });
    }

    return Object.freeze({
      instanceId: surface.instanceId,
      requestedPresentation: surface.presentation,
      slot: 'dormant' as const,
      activeInSlot: false,
    });
  });

  let mode: WorldFocusWorkspaceAllocationMode = 'content';
  if (topSurface?.presentation === 'full-screen') {
    mode = 'focus';
  } else if (canSplit) {
    mode = 'split';
  } else if (
    topSurface !== null &&
    (isOverlayPresentation(topSurface.presentation) ||
      topSurface.presentation === 'sidecar')
  ) {
    mode = 'overlay';
  }

  return Object.freeze({
    mode,
    workspaceInlineSize: inlineSize,
    mainInlineSize,
    sidecarInlineSize,
    activeSidecarInstanceId: activeSidecar?.instanceId ?? null,
    topSurfaceInstanceId: topSurface?.instanceId ?? null,
    placements: Object.freeze(placements),
  });
}
