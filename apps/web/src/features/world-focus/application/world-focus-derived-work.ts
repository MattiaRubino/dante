import {
  createWorldFocusAttentionPrimitive,
  createWorldFocusComparisonPrimitive,
  createWorldFocusTrajectoryPrimitive,
  WORLD_FOCUS_ATTENTION_STATES,
  WORLD_FOCUS_COMPARISON_MODES,
  WORLD_FOCUS_TRAJECTORY_AXES,
  type WorldFocusAttentionPrimitive,
  type WorldFocusAttentionState,
  type WorldFocusComparisonMode,
  type WorldFocusComparisonPrimitive,
  type WorldFocusTrajectoryAxis,
  type WorldFocusTrajectoryPrimitive,
} from '../model/world-focus-work-primitives';
import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from '../model/world-focus-context-reference';
import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from '../model/world-focus-identity';
import {
  createWorldFocusScopedReader,
  type WorldFocusScopedReadAdapter,
  type WorldFocusScopedReader,
  type WorldFocusValidationIssue,
  type WorldFocusValidationResult,
} from './world-focus-foundation';

export const WORLD_FOCUS_DERIVED_WORK_FIRST_OPEN_LIMIT = 4;
const COMPARISON_POLICY = Object.freeze({ maxSubjectReferences: 6 });
const TRAJECTORY_POLICY = Object.freeze({
  maxOrderedPointReferences: 12,
  maxMissingPositionReferences: 12,
});

export type WorldFocusAttentionProjection = Readonly<{
  schemaVersion: 1;
  worldId: WorldFocusId;
  orderedItems: readonly WorldFocusAttentionPrimitive[];
}>;
export type WorldFocusComparisonProjection = Readonly<{
  schemaVersion: 1;
  worldId: WorldFocusId;
  orderedItems: readonly WorldFocusComparisonPrimitive[];
}>;
export type WorldFocusTrajectoryProjection = Readonly<{
  schemaVersion: 1;
  worldId: WorldFocusId;
  orderedItems: readonly WorldFocusTrajectoryPrimitive[];
}>;

export type WorldFocusAttentionReadResult =
  | Readonly<{ status: 'ready'; projection: WorldFocusAttentionProjection }>
  | Readonly<{ status: 'empty'; worldId: WorldFocusId }>;
export type WorldFocusComparisonReadResult =
  | Readonly<{ status: 'ready'; projection: WorldFocusComparisonProjection }>
  | Readonly<{ status: 'empty'; worldId: WorldFocusId }>;
export type WorldFocusTrajectoryReadResult =
  | Readonly<{ status: 'ready'; projection: WorldFocusTrajectoryProjection }>
  | Readonly<{ status: 'empty'; worldId: WorldFocusId }>;

export type WorldFocusDerivedWorkReadAdapter = Readonly<{
  readAttention: WorldFocusScopedReadAdapter;
  readComparison: WorldFocusScopedReadAdapter;
  readTrajectory: WorldFocusScopedReadAdapter;
}>;

export type WorldFocusDerivedWorkReaders = Readonly<{
  readAttention: WorldFocusScopedReader<WorldFocusAttentionReadResult>;
  readComparison: WorldFocusScopedReader<WorldFocusComparisonReadResult>;
  readTrajectory: WorldFocusScopedReader<WorldFocusTrajectoryReadResult>;
}>;

function issue(code: string): WorldFocusValidationIssue {
  return Object.freeze({ code, path: Object.freeze([]) });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function readToken(value: unknown): string | null {
  if (typeof value !== 'string') return null;
  const token = value.trim();
  return token.length === 0 ? null : token;
}

function readReference(value: unknown): WorldFocusContextReference | null {
  if (!isRecord(value) || typeof value.kind !== 'string' || typeof value.key !== 'string') {
    return null;
  }
  try {
    return normalizeWorldFocusContextReference({ kind: value.kind, key: value.key });
  } catch {
    return null;
  }
}

function readOptionalReference(value: unknown): WorldFocusContextReference | null | undefined {
  if (value === null || value === undefined) return null;
  return readReference(value) ?? undefined;
}

function readReferenceArray(value: unknown): readonly WorldFocusContextReference[] | null {
  if (!Array.isArray(value)) return null;
  const references: WorldFocusContextReference[] = [];
  for (const item of value) {
    const reference = readReference(item);
    if (reference === null) return null;
    references.push(reference);
  }
  return Object.freeze(references);
}

function validateProjectionShell(
  input: unknown,
  expectedWorldId: WorldFocusId,
): Record<string, unknown> | null {
  if (!isRecord(input) || input.schemaVersion !== 1) return null;
  const worldId = normalizeWorldFocusId(input.worldId);
  if (worldId !== expectedWorldId || !Array.isArray(input.orderedItems)) return null;
  if (
    input.orderedItems.length === 0 ||
    input.orderedItems.length > WORLD_FOCUS_DERIVED_WORK_FIRST_OPEN_LIMIT
  ) {
    return null;
  }
  return input;
}

function validateEmpty(
  input: Record<string, unknown>,
  expectedWorldId: WorldFocusId,
): Readonly<{ status: 'empty'; worldId: WorldFocusId }> | null | undefined {
  if (input.status !== 'empty') return undefined;
  const worldId = normalizeWorldFocusId(input.worldId);
  return worldId === expectedWorldId
    ? Object.freeze({ status: 'empty' as const, worldId })
    : null;
}

function readAttentionPrimitive(input: unknown): WorldFocusAttentionPrimitive | null {
  if (!isRecord(input) || input.kind !== 'attention') return null;
  const instanceId = readToken(input.instanceId);
  const matterReference = readReference(input.matterReference);
  const reasonCode = readToken(input.reasonCode);
  const resolutionReference = readOptionalReference(input.resolutionReference);
  const state = input.state;
  if (
    instanceId === null ||
    matterReference === null ||
    reasonCode === null ||
    resolutionReference === undefined ||
    typeof state !== 'string' ||
    !WORLD_FOCUS_ATTENTION_STATES.includes(state as WorldFocusAttentionState)
  ) {
    return null;
  }
  try {
    return createWorldFocusAttentionPrimitive({
      instanceId,
      matterReference,
      reasonCode,
      resolutionReference,
      state: state as WorldFocusAttentionState,
    });
  } catch {
    return null;
  }
}

function readComparisonPrimitive(input: unknown): WorldFocusComparisonPrimitive | null {
  if (!isRecord(input) || input.kind !== 'comparison') return null;
  const instanceId = readToken(input.instanceId);
  const subjectReferences = readReferenceArray(input.subjectReferences);
  const basisReference = readOptionalReference(input.basisReference);
  const mode = input.mode;
  if (
    instanceId === null ||
    subjectReferences === null ||
    subjectReferences.length < 2 ||
    basisReference === undefined ||
    typeof mode !== 'string' ||
    !WORLD_FOCUS_COMPARISON_MODES.includes(mode as WorldFocusComparisonMode)
  ) {
    return null;
  }
  try {
    return createWorldFocusComparisonPrimitive(
      {
        instanceId,
        mode: mode as WorldFocusComparisonMode,
        subjectReferences: subjectReferences as WorldFocusComparisonPrimitive['subjectReferences'],
        basisReference,
      },
      COMPARISON_POLICY,
    );
  } catch {
    return null;
  }
}

function readTrajectoryPrimitive(input: unknown): WorldFocusTrajectoryPrimitive | null {
  if (!isRecord(input) || input.kind !== 'trajectory') return null;
  const instanceId = readToken(input.instanceId);
  const subjectReference = readReference(input.subjectReference);
  const orderedPointReferences = readReferenceArray(input.orderedPointReferences);
  const missingPositionReferences = readReferenceArray(input.missingPositionReferences);
  const orderingBasisReference = readOptionalReference(input.orderingBasisReference);
  const aggregationBasisReference = readOptionalReference(input.aggregationBasisReference);
  const axis = input.axis;
  if (
    instanceId === null ||
    subjectReference === null ||
    orderedPointReferences === null ||
    orderedPointReferences.length < 2 ||
    missingPositionReferences === null ||
    orderingBasisReference === undefined ||
    aggregationBasisReference === undefined ||
    typeof axis !== 'string' ||
    !WORLD_FOCUS_TRAJECTORY_AXES.includes(axis as WorldFocusTrajectoryAxis)
  ) {
    return null;
  }
  try {
    return createWorldFocusTrajectoryPrimitive(
      {
        instanceId,
        subjectReference,
        axis: axis as WorldFocusTrajectoryAxis,
        orderedPointReferences: orderedPointReferences as WorldFocusTrajectoryPrimitive['orderedPointReferences'],
        missingPositionReferences,
        orderingBasisReference,
        aggregationBasisReference,
      },
      TRAJECTORY_POLICY,
    );
  } catch {
    return null;
  }
}

function validateReadyItems<Item>(
  input: Record<string, unknown>,
  expectedWorldId: WorldFocusId,
  readItem: (value: unknown) => Item | null,
): readonly Item[] | null {
  if (input.status !== 'ready') return null;
  const projection = validateProjectionShell(input.projection, expectedWorldId);
  if (projection === null || !Array.isArray(projection.orderedItems)) return null;
  const items: Item[] = [];
  const instanceIds = new Set<string>();
  for (const rawItem of projection.orderedItems) {
    const item = readItem(rawItem);
    if (item === null || !isRecord(item)) return null;
    const instanceId = readToken(item.instanceId);
    if (instanceId === null || instanceIds.has(instanceId)) return null;
    instanceIds.add(instanceId);
    items.push(item);
  }
  return Object.freeze(items);
}

function validateAttentionResult(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusAttentionReadResult> {
  if (!isRecord(input)) return { ok: false, issues: [issue('result.record')] };
  const empty = validateEmpty(input, expectedWorldId);
  if (empty !== undefined) {
    return empty === null
      ? { ok: false, issues: [issue('result.worldId')] }
      : { ok: true, value: empty };
  }
  const items = validateReadyItems(input, expectedWorldId, readAttentionPrimitive);
  return items === null
    ? { ok: false, issues: [issue('attention.invalid')] }
    : {
        ok: true,
        value: Object.freeze({
          status: 'ready' as const,
          projection: Object.freeze({
            schemaVersion: 1 as const,
            worldId: expectedWorldId,
            orderedItems: items,
          }),
        }),
      };
}

function validateComparisonResult(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusComparisonReadResult> {
  if (!isRecord(input)) return { ok: false, issues: [issue('result.record')] };
  const empty = validateEmpty(input, expectedWorldId);
  if (empty !== undefined) {
    return empty === null
      ? { ok: false, issues: [issue('result.worldId')] }
      : { ok: true, value: empty };
  }
  const items = validateReadyItems(input, expectedWorldId, readComparisonPrimitive);
  return items === null
    ? { ok: false, issues: [issue('comparison.invalid')] }
    : {
        ok: true,
        value: Object.freeze({
          status: 'ready' as const,
          projection: Object.freeze({
            schemaVersion: 1 as const,
            worldId: expectedWorldId,
            orderedItems: items,
          }),
        }),
      };
}

function validateTrajectoryResult(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusTrajectoryReadResult> {
  if (!isRecord(input)) return { ok: false, issues: [issue('result.record')] };
  const empty = validateEmpty(input, expectedWorldId);
  if (empty !== undefined) {
    return empty === null
      ? { ok: false, issues: [issue('result.worldId')] }
      : { ok: true, value: empty };
  }
  const items = validateReadyItems(input, expectedWorldId, readTrajectoryPrimitive);
  return items === null
    ? { ok: false, issues: [issue('trajectory.invalid')] }
    : {
        ok: true,
        value: Object.freeze({
          status: 'ready' as const,
          projection: Object.freeze({
            schemaVersion: 1 as const,
            worldId: expectedWorldId,
            orderedItems: items,
          }),
        }),
      };
}

export function createWorldFocusDerivedWorkReaders(
  adapter: WorldFocusDerivedWorkReadAdapter,
): WorldFocusDerivedWorkReaders {
  return Object.freeze({
    readAttention: createWorldFocusScopedReader(
      adapter.readAttention,
      validateAttentionResult,
    ),
    readComparison: createWorldFocusScopedReader(
      adapter.readComparison,
      validateComparisonResult,
    ),
    readTrajectory: createWorldFocusScopedReader(
      adapter.readTrajectory,
      validateTrajectoryResult,
    ),
  });
}
