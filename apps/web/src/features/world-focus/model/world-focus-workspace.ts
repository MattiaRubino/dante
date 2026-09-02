import {
  createWorldFocusContextReferenceSet,
  normalizeWorldFocusContextReference,
  sameWorldFocusContextReferenceSet,
  type WorldFocusContextReference,
  type WorldFocusContextReferenceSet,
} from './world-focus-context-reference';
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
  /** Compatibility projection of contextReferences.primary for existing callers. */
  selection: WorldFocusContextReference | null;
  contextReferences: WorldFocusContextReferenceSet | null;
  surfaces: readonly WorldFocusSurfaceDescriptor<Kind>[];
}>;

export type WorldFocusInteractionCursor = Readonly<{
  worldId: string;
  generation: number;
  /** Compatibility projection of contextReferences.primary. */
  selection: WorldFocusContextReference | null;
  contextReferences: WorldFocusContextReferenceSet | null;
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
  | Readonly<{
      type: 'set-context';
      references: WorldFocusContextReferenceSet;
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
    contextReference:
      request.contextReference === undefined
        ? state.contextReferences?.primary ?? null
        : request.contextReference === null
          ? null
          : normalizeWorldFocusContextReference(
              request.contextReference,
              'World Focus surface context reference',
            ),
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

function withContextReferences<Kind extends string>(
  state: WorldFocusWorkspaceState<Kind>,
  contextReferences: WorldFocusContextReferenceSet | null,
): WorldFocusWorkspaceState<Kind> {
  if (sameWorldFocusContextReferenceSet(state.contextReferences, contextReferences)) {
    return state;
  }

  return Object.freeze({
    ...state,
    generation: state.generation + 1,
    selection: contextReferences?.primary ?? null,
    contextReferences,
  });
}

export function createWorldFocusWorkspaceState<Kind extends string = string>(
  worldId: string,
): WorldFocusWorkspaceState<Kind> {
  return Object.freeze({
    worldId: assertNonEmptyToken(worldId, 'World Focus workspace world id'),
    generation: 0,
    selection: null,
    contextReferences: null,
    surfaces: Object.freeze([]),
  });
}

export function getWorldFocusTopSurface<Kind extends string = string>(
  state: WorldFocusWorkspaceState<Kind>,
): WorldFocusSurfaceDescriptor<Kind> | null {
  return state.surfaces.at(-1) ?? null;
}

export function getWorldFocusInteractionCursor(
  state: WorldFocusWorkspaceState,
): WorldFocusInteractionCursor {
  const activeSurface = getWorldFocusTopSurface(state);
  const cursor = {
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
  } as Omit<WorldFocusInteractionCursor, 'contextReferences'> &
    Partial<Pick<WorldFocusInteractionCursor, 'contextReferences'>>;

  Object.defineProperty(cursor, 'contextReferences', {
    value: state.contextReferences,
    enumerable: false,
    configurable: false,
    writable: false,
  });

  return Object.freeze(cursor) as WorldFocusInteractionCursor;
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

export function reduceWorldFocusWorkspaceState<Kind extends string = string>(
  state: WorldFocusWorkspaceState<Kind>,
  intent: WorldFocusWorkspaceIntent<Kind>,
): WorldFocusWorkspaceState<Kind> {
  switch (intent.type) {
    case 'select-context': {
      const primary = normalizeWorldFocusContextReference(
        intent.reference,
        'World Focus context reference',
      );
      return withContextReferences(
        state,
        createWorldFocusContextReferenceSet({ primary }),
      );
    }

    case 'set-context':
      return withContextReferences(
        state,
        createWorldFocusContextReferenceSet({
          primary: intent.references.primary,
          supporting: intent.references.supporting,
        }),
      );

    case 'clear-context':
      return withContextReferences(state, null);

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
