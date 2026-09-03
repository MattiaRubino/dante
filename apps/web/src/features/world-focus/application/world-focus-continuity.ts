import {
  createWorldFocusScopedReader,
  type WorldFocusScopedReader,
  type WorldFocusValidationIssue,
  type WorldFocusValidationResult,
} from './world-focus-foundation';
import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from '../model/world-focus-identity';
import {
  isWorldFocusContinuityPresentationState,
  WORLD_FOCUS_CONTINUITY_FIRST_OPEN_LIMIT,
  type WorldFocusContinuityItem,
  type WorldFocusContinuityProjection,
  type WorldFocusContinuityReadResult,
} from '../model/world-focus-continuity';
import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from '../model/world-focus-context-reference';
import { createWorldFocusContinuityPrimitive } from '../model/world-focus-work-primitives';

export type WorldFocusContinuityReadAdapter = Readonly<{
  read: (request: Readonly<{ worldId: WorldFocusId; signal: AbortSignal }>) => Promise<unknown>;
}>;

export type WorldFocusContinuityReader = WorldFocusScopedReader<WorldFocusContinuityReadResult>;

function issue(
  code: string,
  path: readonly (string | number)[] = [],
): WorldFocusValidationIssue {
  return Object.freeze({ code, path });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function readNonEmptyString(value: unknown): string | null {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  return trimmed.length === 0 ? null : trimmed;
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

function validateContinuityItem(
  input: unknown,
  index: number,
): WorldFocusValidationResult<WorldFocusContinuityItem> {
  if (!isRecord(input)) {
    return { ok: false, issues: [issue('item.record', ['orderedItems', index])] };
  }

  const key = readNonEmptyString(input.key);
  const title = readNonEmptyString(input.title);
  const context = readNonEmptyString(input.context);
  const checkpoint = readNonEmptyString(input.checkpoint);
  const threadReference = readReference(input.threadReference);
  const checkpointReference = readReference(input.checkpointReference);
  const continuationReference =
    input.continuationReference === null
      ? null
      : readReference(input.continuationReference);
  const presentationState = input.presentationState;
  const issues: WorldFocusValidationIssue[] = [];

  if (key === null) issues.push(issue('item.key', ['orderedItems', index, 'key']));
  if (title === null) issues.push(issue('item.title', ['orderedItems', index, 'title']));
  if (context === null) issues.push(issue('item.context', ['orderedItems', index, 'context']));
  if (checkpoint === null) issues.push(issue('item.checkpoint', ['orderedItems', index, 'checkpoint']));
  if (threadReference === null) issues.push(issue('item.threadReference', ['orderedItems', index, 'threadReference']));
  if (checkpointReference === null) issues.push(issue('item.checkpointReference', ['orderedItems', index, 'checkpointReference']));
  if (input.continuationReference !== null && continuationReference === null) {
    issues.push(issue('item.continuationReference', ['orderedItems', index, 'continuationReference']));
  }
  if (!isWorldFocusContinuityPresentationState(presentationState)) {
    issues.push(issue('item.presentationState', ['orderedItems', index, 'presentationState']));
  }

  if (
    issues.length > 0 ||
    key === null ||
    title === null ||
    context === null ||
    checkpoint === null ||
    threadReference === null ||
    checkpointReference === null ||
    !isWorldFocusContinuityPresentationState(presentationState)
  ) {
    return { ok: false, issues };
  }

  const primitive = createWorldFocusContinuityPrimitive({
    instanceId: key,
    threadReference,
    checkpointReference,
    continuationReference,
    state: presentationState,
  });

  return {
    ok: true,
    value: Object.freeze({
      key,
      title,
      context,
      checkpoint,
      threadReference: primitive.threadReference,
      checkpointReference: primitive.checkpointReference,
      continuationReference: primitive.continuationReference,
      presentationState: primitive.state,
    }),
  };
}

function validateProjection(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusContinuityProjection> {
  if (!isRecord(input)) {
    return { ok: false, issues: [issue('projection.record', ['projection'])] };
  }

  const worldId = normalizeWorldFocusId(input.worldId);
  const orderedItems = input.orderedItems;
  const issues: WorldFocusValidationIssue[] = [];

  if (input.schemaVersion !== 1) issues.push(issue('projection.schemaVersion', ['projection', 'schemaVersion']));
  if (worldId !== expectedWorldId) issues.push(issue('projection.worldId', ['projection', 'worldId']));
  if (!Array.isArray(orderedItems)) {
    issues.push(issue('projection.orderedItems', ['projection', 'orderedItems']));
  } else if (
    orderedItems.length === 0 ||
    orderedItems.length > WORLD_FOCUS_CONTINUITY_FIRST_OPEN_LIMIT
  ) {
    issues.push(issue('projection.orderedItems.bounds', ['projection', 'orderedItems']));
  }

  if (issues.length > 0 || worldId === undefined || !Array.isArray(orderedItems)) {
    return { ok: false, issues };
  }

  const validatedItems: WorldFocusContinuityItem[] = [];
  const itemIssues: WorldFocusValidationIssue[] = [];
  const keys = new Set<string>();

  for (const [index, item] of orderedItems.entries()) {
    const result = validateContinuityItem(item, index);
    if (!result.ok) {
      itemIssues.push(...result.issues);
      continue;
    }
    if (keys.has(result.value.key)) {
      itemIssues.push(issue('item.key.duplicate', ['orderedItems', index, 'key']));
      continue;
    }
    keys.add(result.value.key);
    validatedItems.push(result.value);
  }

  if (itemIssues.length > 0 || validatedItems.length !== orderedItems.length) {
    return { ok: false, issues: itemIssues };
  }

  return {
    ok: true,
    value: Object.freeze({
      schemaVersion: 1 as const,
      worldId,
      orderedItems: Object.freeze(validatedItems.slice()),
    }),
  };
}

export function validateWorldFocusContinuityReadResult(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusContinuityReadResult> {
  if (!isRecord(input)) return { ok: false, issues: [issue('result.record')] };
  const status = input.status;

  if (status === 'empty') {
    const worldId = normalizeWorldFocusId(input.worldId);
    return worldId === expectedWorldId
      ? { ok: true, value: Object.freeze({ status, worldId }) }
      : { ok: false, issues: [issue('result.worldId', ['worldId'])] };
  }

  if (status === 'unavailable') {
    const worldId = normalizeWorldFocusId(input.worldId);
    const reasonCode = readNonEmptyString(input.reasonCode);
    if (worldId !== expectedWorldId || reasonCode === null || typeof input.retryable !== 'boolean') {
      return { ok: false, issues: [issue('result.unavailable')] };
    }
    return {
      ok: true,
      value: Object.freeze({ status, worldId, reasonCode, retryable: input.retryable }),
    };
  }

  if (status !== 'ready' && status !== 'partial' && status !== 'stale') {
    return { ok: false, issues: [issue('result.status', ['status'])] };
  }

  const projectionResult = validateProjection(input.projection, expectedWorldId);
  if (!projectionResult.ok) return projectionResult;

  if (status === 'ready') {
    return { ok: true, value: Object.freeze({ status, projection: projectionResult.value }) };
  }

  if (status === 'partial') {
    const reasonCode = readNonEmptyString(input.reasonCode);
    return reasonCode === null
      ? { ok: false, issues: [issue('result.reasonCode', ['reasonCode'])] }
      : {
          ok: true,
          value: Object.freeze({ status, projection: projectionResult.value, reasonCode }),
        };
  }

  const asOf = readNonEmptyString(input.asOf);
  if (asOf === null || Number.isNaN(Date.parse(asOf))) {
    return { ok: false, issues: [issue('result.asOf', ['asOf'])] };
  }
  return {
    ok: true,
    value: Object.freeze({ status, projection: projectionResult.value, asOf }),
  };
}

export function createWorldFocusContinuityReader(
  adapter: WorldFocusContinuityReadAdapter,
): WorldFocusContinuityReader {
  return createWorldFocusScopedReader(
    adapter.read,
    validateWorldFocusContinuityReadResult,
  );
}
