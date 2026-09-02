import type {
  WorldFocusInteractionDepth,
  WorldFocusPresentationSurface,
} from './world-focus-platform';

export const WORLD_FOCUS_SURFACE_ORIGINS = [
  'user',
  'dante',
  'application',
] as const;

export type WorldFocusSurfaceOrigin =
  (typeof WORLD_FOCUS_SURFACE_ORIGINS)[number];

export const WORLD_FOCUS_BLOCKING_PRESENTATIONS = [
  'modal',
  'full-screen',
] as const satisfies readonly WorldFocusPresentationSurface[];

export type WorldFocusContextReference = Readonly<{
  kind: string;
  key: string;
}>;

export type WorldFocusWorkspaceExpectation = Readonly<{
  worldId: string;
  generation: number;
}>;

export type WorldFocusSurfaceDescriptor<Kind extends string = string> = Readonly<{
  instanceId: string;
  kind: Kind;
  depth: WorldFocusInteractionDepth;
  presentation: WorldFocusPresentationSurface;
  origin: WorldFocusSurfaceOrigin;
  boundGeneration: number;
  contextReference: WorldFocusContextReference | null;
  dismissible: boolean;
}>;

export type WorldFocusSurfaceRequest<Kind extends string = string> = Readonly<{
  instanceId: string;
  kind: Kind;
  depth: WorldFocusInteractionDepth;
  presentation: WorldFocusPresentationSurface;
  origin: WorldFocusSurfaceOrigin;
  contextReference?: WorldFocusContextReference | null;
  dismissible?: boolean;
  expectedWorkspace?: WorldFocusWorkspaceExpectation;
}>;

export type WorldFocusWorkspaceState<Kind extends string = string> = Readonly<{
  worldId: string;
  generation: number;
  selection: WorldFocusContextReference | null;
  surfaces: readonly WorldFocusSurfaceDescriptor<Kind>[];
}>;

export type WorldFocusInteractionCursor = Readonly<{
  worldId: string;
  generation: number;
  selection: WorldFocusContextReference | null;
  activeSurface: Readonly<{
    instanceId: string;
    kind: string;
    depth: WorldFocusInteractionDepth;
    boundGeneration: number;
    contextReference: WorldFocusContextReference | null;
  }> | null;
}>;

export type WorldFocusWorkspaceIntent<Kind extends string = string> =
  | Readonly<{
      type: 'select-context';
      reference: WorldFocusContextReference;
    }>
  | Readonly<{ type: 'clear-context' }>
  | Readonly<{
      type: 'open-surface';
      surface: WorldFocusSurfaceRequest<Kind>;
    }>
  | Readonly<{
      type: 'replace-surface';
      instanceId: string;
      surface: WorldFocusSurfaceRequest<Kind>;
    }>
  | Readonly<{
      type: 'promote-surface';
      instanceId: string;
      depth: WorldFocusInteractionDepth;
      presentation: WorldFocusPresentationSurface;
      expectedWorkspace?: WorldFocusWorkspaceExpectation;
    }>
  | Readonly<{
      type: 'close-surface';
      instanceId: string;
    }>
  | Readonly<{ type: 'close-top-surface' }>;

export type WorldFocusEscapeDisposition =
  | 'no-surface'
  | 'surface-dismissible'
  | 'surface-blocked';

function assertNonEmptyToken(value: string, label: string): string {
  const token = value.trim();
  if (token.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  return token;
}

function assertNonNegativeInteger(value: number, label: string): number {
  if (!Number.isInteger(value) || value < 0) {
    throw new Error(`${label} must be a non-negative integer`);
  }
  return value;
}

function sameContextReference(
  left: WorldFocusContextReference | null,
  right: WorldFocusContextReference | null,
): boolean {
  return left?.kind === right?.kind && left?.key === right?.key;
}

function canApplyWorkspaceExpectation(
  state: WorldFocusWorkspaceState,
  expectedWorkspace: WorldFocusWorkspaceExpectation | undefined,
): boolean {
  if (expectedWorkspace === undefined) {
    return true;
  }

  const expectedWorldId = assertNonEmptyToken(
    expectedWorkspace.worldId,
    'World Focus expected workspace world id',
  );
  const expectedGeneration = assertNonNegativeInteger(
    expectedWorkspace.generation,
    'World Focus expected workspace generation',
  );

  return (
    expectedWorldId === state.worldId &&
    expectedGeneration === state.generation
  );
}

export function isWorldFocusBlockingPresentation(
  presentation: WorldFocusPresentationSurface,
): boolean {
  return presentation === 'modal' || presentation === 'full-screen';
}

export function getWorldFocusBlockingSurface<Kind extends string = string>(
  state: WorldFocusWorkspaceState<Kind>,
): WorldFocusSurfaceDescriptor<Kind> | null {
  for (let index = state.surfaces.length - 1; index >= 0; index -= 1) {
    const surface = state.surfaces[index];
    if (
      surface !== undefined &&
      isWorldFocusBlockingPresentation(surface.presentation)
    ) {
      return surface;
    }
  }
  return null;
}

function isSurfaceBarrierSafe<Kind extends string>(
  surfaces: readonly WorldFocusSurfaceDescriptor<Kind>[],
): boolean {
  let blockingTailStarted = false;

  for (const surface of surfaces) {
    if (isWorldFocusBlockingPresentation(surface.presentation)) {
      blockingTailStarted = true;
      continue;
    }
    if (blockingTailStarted) {
      return false;
    }
  }

  return true;
}

function canMutateSurfaceWhileBlocked<Kind extends string>(
  state: WorldFocusWorkspaceState<Kind>,
  index: number,
): boolean {
  const blocker = getWorldFocusBlockingSurface(state);
  return blocker === null || index === state.surfaces.length - 1;
}

function buildSurfaceDescriptor<Kind extends string>(
  state: WorldFocusWorkspaceState<Kind>,
  request: WorldFocusSurfaceRequest<Kind>,
): WorldFocusSurfaceDescriptor<Kind> {
  return Object.freeze({
    instanceId: assertNonEmptyToken(
      request.instanceId,
      'World Focus surface instance id',
    ),
    kind: assertNonEmptyToken(request.kind, 'World Focus surface kind') as Kind,
    depth: request.depth,
    presentation: request.presentation,
    origin: request.origin,
    boundGeneration: state.generation,
    contextReference: request.contextReference ?? state.selection,
    dismissible: request.dismissible ?? true,
  });
}

function withSurfaces<Kind extends string>(
  state: WorldFocusWorkspaceState<Kind>,
  surfaces: readonly WorldFocusSurfaceDescriptor<Kind>[],
): WorldFocusWorkspaceState<Kind> {
  return Object.freeze({
    ...state,
    surfaces: Object.freeze(surfaces.slice()),
  });
}

/**
 * Creates transient World workspace state. This is intentionally presentation /
 * interaction state only: it never owns canonical World truth, authorization,
 * provider state or durable DANTE run lifetime.
 */
export function createWorldFocusWorkspaceState<Kind extends string = string>(
  worldId: string,
): WorldFocusWorkspaceState<Kind> {
  return Object.freeze({
    worldId: assertNonEmptyToken(worldId, 'World Focus workspace world id'),
    generation: 0,
    selection: null,
    surfaces: Object.freeze([]),
  });
}

export function getWorldFocusTopSurface<Kind extends string = string>(
  state: WorldFocusWorkspaceState<Kind>,
): WorldFocusSurfaceDescriptor<Kind> | null {
  return state.surfaces.at(-1) ?? null;
}

/**
 * Produces the bounded transient cursor a future contextual DANTE request may
 * reference. It contains identities/hints only and intentionally excludes raw
 * module payloads, canonical truth, authorization decisions and React/DOM
 * state.
 */
export function getWorldFocusInteractionCursor(
  state: WorldFocusWorkspaceState,
): WorldFocusInteractionCursor {
  const activeSurface = getWorldFocusTopSurface(state);

  return Object.freeze({
    worldId: state.worldId,
    generation: state.generation,
    selection: state.selection,
    activeSurface:
      activeSurface === null
        ? null
        : Object.freeze({
            instanceId: activeSurface.instanceId,
            kind: activeSurface.kind,
            depth: activeSurface.depth,
            boundGeneration: activeSurface.boundGeneration,
            contextReference: activeSurface.contextReference,
          }),
  });
}

export function getWorldFocusEscapeDisposition(
  state: WorldFocusWorkspaceState,
): WorldFocusEscapeDisposition {
  const surface = getWorldFocusTopSurface(state);
  if (surface === null) {
    return 'no-surface';
  }
  return surface.dismissible ? 'surface-dismissible' : 'surface-blocked';
}

/**
 * Pure workspace transition function. Async callers may attach an atomic
 * expectedWorkspace identity + generation to presentation intents. A request
 * from another World, or from an older cursor generation in the same World,
 * becomes a deterministic no-op instead of presenting against a newer or
 * different workspace.
 *
 * Modal/full-screen presentations form a blocking tail. Once one is active,
 * weaker presentations cannot be appended above it. Additional blocking
 * surfaces are allowed so deliberate nested modal/focus flows remain possible.
 * Lower surfaces cannot be replaced/promoted while a blocker owns interaction.
 */
export function reduceWorldFocusWorkspaceState<Kind extends string = string>(
  state: WorldFocusWorkspaceState<Kind>,
  intent: WorldFocusWorkspaceIntent<Kind>,
): WorldFocusWorkspaceState<Kind> {
  switch (intent.type) {
    case 'select-context': {
      const reference = Object.freeze({
        kind: assertNonEmptyToken(
          intent.reference.kind,
          'World Focus context reference kind',
        ),
        key: assertNonEmptyToken(
          intent.reference.key,
          'World Focus context reference key',
        ),
      });

      if (sameContextReference(state.selection, reference)) {
        return state;
      }

      return Object.freeze({
        ...state,
        generation: state.generation + 1,
        selection: reference,
      });
    }

    case 'clear-context':
      if (state.selection === null) {
        return state;
      }
      return Object.freeze({
        ...state,
        generation: state.generation + 1,
        selection: null,
      });

    case 'open-surface': {
      if (
        !canApplyWorkspaceExpectation(
          state,
          intent.surface.expectedWorkspace,
        )
      ) {
        return state;
      }
      if (
        state.surfaces.some(
          (surface) => surface.instanceId === intent.surface.instanceId.trim(),
        )
      ) {
        return state;
      }
      if (
        getWorldFocusBlockingSurface(state) !== null &&
        !isWorldFocusBlockingPresentation(intent.surface.presentation)
      ) {
        return state;
      }

      return withSurfaces(state, [
        ...state.surfaces,
        buildSurfaceDescriptor(state, intent.surface),
      ]);
    }

    case 'replace-surface': {
      if (
        !canApplyWorkspaceExpectation(
          state,
          intent.surface.expectedWorkspace,
        )
      ) {
        return state;
      }

      const index = state.surfaces.findIndex(
        (surface) => surface.instanceId === intent.instanceId,
      );
      if (index < 0 || !canMutateSurfaceWhileBlocked(state, index)) {
        return state;
      }

      const replacement = buildSurfaceDescriptor(state, intent.surface);
      const duplicateIndex = state.surfaces.findIndex(
        (surface, candidateIndex) =>
          candidateIndex !== index &&
          surface.instanceId === replacement.instanceId,
      );
      if (duplicateIndex >= 0) {
        return state;
      }

      const surfaces = state.surfaces.slice();
      surfaces[index] = replacement;
      return isSurfaceBarrierSafe(surfaces) ? withSurfaces(state, surfaces) : state;
    }

    case 'promote-surface': {
      if (!canApplyWorkspaceExpectation(state, intent.expectedWorkspace)) {
        return state;
      }

      const index = state.surfaces.findIndex(
        (surface) => surface.instanceId === intent.instanceId,
      );
      if (index < 0 || !canMutateSurfaceWhileBlocked(state, index)) {
        return state;
      }

      const current = state.surfaces[index];
      if (current === undefined) {
        return state;
      }
      if (
        current.depth === intent.depth &&
        current.presentation === intent.presentation
      ) {
        return state;
      }

      const surfaces = state.surfaces.slice();
      surfaces[index] = Object.freeze({
        ...current,
        depth: intent.depth,
        presentation: intent.presentation,
      });
      return isSurfaceBarrierSafe(surfaces) ? withSurfaces(state, surfaces) : state;
    }

    case 'close-surface': {
      const surfaces = state.surfaces.filter(
        (surface) => surface.instanceId !== intent.instanceId,
      );
      return surfaces.length === state.surfaces.length
        ? state
        : withSurfaces(state, surfaces);
    }

    case 'close-top-surface': {
      const top = getWorldFocusTopSurface(state);
      if (top === null || !top.dismissible) {
        return state;
      }
      return withSurfaces(state, state.surfaces.slice(0, -1));
    }
  }
}
