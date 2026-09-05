import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from '../model/world-focus-identity';
import {
  validateWorldFocusBoundary,
  type WorldFocusValidationIssue,
  type WorldFocusValidationResult,
} from './world-focus-foundation';

export const WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION = 1 as const;
export const WORLD_FOCUS_DANTE_CONVERSATION_MAX_HISTORY = 12;
export const WORLD_FOCUS_DANTE_CONVERSATION_MAX_INPUT_LENGTH = 4_000;
export const WORLD_FOCUS_DANTE_CONVERSATION_MAX_OUTPUT_LENGTH = 8_000;

export const WORLD_FOCUS_DANTE_CONVERSATION_RESULT_CLASSES = [
  'answer',
  'explanation',
] as const;

export type WorldFocusDanteConversationResultClass =
  (typeof WORLD_FOCUS_DANTE_CONVERSATION_RESULT_CLASSES)[number];

export type WorldFocusDanteConversationHistoryEntry =
  | Readonly<{
      role: 'user';
      text: string;
    }>
  | Readonly<{
      role: 'assistant';
      resultClass: WorldFocusDanteConversationResultClass;
      text: string;
    }>;

export type WorldFocusDanteConversationRequest = Readonly<{
  schemaVersion: typeof WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION;
  requestId: string;
  worldId: WorldFocusId;
  workspaceGeneration: number;
  input: string;
  history: readonly WorldFocusDanteConversationHistoryEntry[];
  locale: string;
}>;

export type WorldFocusDanteConversationReadResult =
  | Readonly<{
      schemaVersion: typeof WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION;
      status: 'ready';
      requestId: string;
      worldId: WorldFocusId;
      workspaceGeneration: number;
      resultClass: WorldFocusDanteConversationResultClass;
      output: string;
    }>
  | Readonly<{
      schemaVersion: typeof WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION;
      status: 'unavailable';
      requestId: string;
      worldId: WorldFocusId;
      workspaceGeneration: number;
      reasonCode: string;
      retryable: boolean;
    }>;

export type WorldFocusDanteConversationReadAdapter = Readonly<{
  read: (request: Readonly<{
    request: WorldFocusDanteConversationRequest;
    signal: AbortSignal;
  }>) => Promise<unknown>;
}>;

export type WorldFocusDanteConversationReader = (
  request: WorldFocusDanteConversationRequest,
  signal?: AbortSignal,
) => Promise<WorldFocusDanteConversationReadResult>;

function issue(code: string): WorldFocusValidationIssue {
  return Object.freeze({ code, path: Object.freeze([]) });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function hasExactKeys(
  value: Record<string, unknown>,
  expected: readonly string[],
): boolean {
  const keys = Object.keys(value);
  return (
    keys.length === expected.length &&
    keys.every((key) => expected.includes(key))
  );
}

function readBoundedString(
  value: unknown,
  maxLength: number,
): string | null {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  return trimmed.length > 0 && trimmed.length <= maxLength ? trimmed : null;
}

function isNonNegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}

export function isWorldFocusDanteConversationResultClass(
  value: unknown,
): value is WorldFocusDanteConversationResultClass {
  return (
    typeof value === 'string' &&
    WORLD_FOCUS_DANTE_CONVERSATION_RESULT_CLASSES.some(
      (resultClass) => resultClass === value,
    )
  );
}

function normalizeHistoryEntry(
  entry: WorldFocusDanteConversationHistoryEntry,
): WorldFocusDanteConversationHistoryEntry {
  const text = readBoundedString(
    entry.text,
    entry.role === 'user'
      ? WORLD_FOCUS_DANTE_CONVERSATION_MAX_INPUT_LENGTH
      : WORLD_FOCUS_DANTE_CONVERSATION_MAX_OUTPUT_LENGTH,
  );
  if (text === null) {
    throw new Error('World Focus DANTE conversation history text is invalid');
  }

  if (entry.role === 'user') {
    return Object.freeze({ role: 'user' as const, text });
  }

  if (!isWorldFocusDanteConversationResultClass(entry.resultClass)) {
    throw new Error('World Focus DANTE conversation history result class is invalid');
  }

  return Object.freeze({
    role: 'assistant' as const,
    resultClass: entry.resultClass,
    text,
  });
}

export function createWorldFocusDanteConversationRequest(
  input: Omit<WorldFocusDanteConversationRequest, 'schemaVersion'>,
): WorldFocusDanteConversationRequest {
  const worldId = normalizeWorldFocusId(input.worldId);
  const requestId = readBoundedString(input.requestId, 128);
  const requestText = readBoundedString(
    input.input,
    WORLD_FOCUS_DANTE_CONVERSATION_MAX_INPUT_LENGTH,
  );
  const locale = readBoundedString(input.locale, 32);

  if (
    worldId === undefined ||
    requestId === null ||
    requestText === null ||
    locale === null ||
    !isNonNegativeInteger(input.workspaceGeneration) ||
    input.history.length > WORLD_FOCUS_DANTE_CONVERSATION_MAX_HISTORY
  ) {
    throw new Error('World Focus DANTE conversation request is invalid');
  }

  return Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
    requestId,
    worldId,
    workspaceGeneration: input.workspaceGeneration,
    input: requestText,
    history: Object.freeze(input.history.map(normalizeHistoryEntry)),
    locale,
  });
}

function validateReadResult(
  input: unknown,
  expectedRequest: WorldFocusDanteConversationRequest,
): WorldFocusValidationResult<WorldFocusDanteConversationReadResult> {
  if (!isRecord(input)) {
    return { ok: false, issues: [issue('result.record')] };
  }

  const worldId = normalizeWorldFocusId(input.worldId);
  const correlationMatches =
    input.schemaVersion === WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION &&
    input.requestId === expectedRequest.requestId &&
    worldId === expectedRequest.worldId &&
    input.workspaceGeneration === expectedRequest.workspaceGeneration;

  if (!correlationMatches || worldId === undefined) {
    return { ok: false, issues: [issue('result.correlation')] };
  }

  if (input.status === 'ready') {
    if (
      !hasExactKeys(input, [
        'schemaVersion',
        'status',
        'requestId',
        'worldId',
        'workspaceGeneration',
        'resultClass',
        'output',
      ]) ||
      !isWorldFocusDanteConversationResultClass(input.resultClass)
    ) {
      return { ok: false, issues: [issue('result.ready.shape')] };
    }

    const output = readBoundedString(
      input.output,
      WORLD_FOCUS_DANTE_CONVERSATION_MAX_OUTPUT_LENGTH,
    );
    if (output === null) {
      return { ok: false, issues: [issue('result.ready.output')] };
    }

    return {
      ok: true,
      value: Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
        status: 'ready' as const,
        requestId: expectedRequest.requestId,
        worldId,
        workspaceGeneration: expectedRequest.workspaceGeneration,
        resultClass: input.resultClass,
        output,
      }),
    };
  }

  if (input.status === 'unavailable') {
    if (
      !hasExactKeys(input, [
        'schemaVersion',
        'status',
        'requestId',
        'worldId',
        'workspaceGeneration',
        'reasonCode',
        'retryable',
      ])
    ) {
      return { ok: false, issues: [issue('result.unavailable.shape')] };
    }

    const reasonCode = readBoundedString(input.reasonCode, 128);
    if (reasonCode === null || typeof input.retryable !== 'boolean') {
      return { ok: false, issues: [issue('result.unavailable.value')] };
    }

    return {
      ok: true,
      value: Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
        status: 'unavailable' as const,
        requestId: expectedRequest.requestId,
        worldId,
        workspaceGeneration: expectedRequest.workspaceGeneration,
        reasonCode,
        retryable: input.retryable,
      }),
    };
  }

  return { ok: false, issues: [issue('result.status')] };
}

function assertActive(signal: AbortSignal): void {
  if (!signal.aborted) return;
  const error = new Error('World Focus DANTE conversation read aborted');
  error.name = 'AbortError';
  throw error;
}

/**
 * Provider-neutral pre-backend conversation boundary. It validates only local
 * conversational correlation and the bounded answer/explanation result class.
 * Context references, authorization, Insight, Proposal, tool/effect state and
 * provider/model transport deliberately do not exist in this contract.
 */
export function createWorldFocusDanteConversationReader(
  adapter: WorldFocusDanteConversationReadAdapter,
): WorldFocusDanteConversationReader {
  return async (request, upstreamSignal) => {
    const controller = new AbortController();
    const abort = () => controller.abort();

    if (upstreamSignal?.aborted === true) {
      controller.abort();
    } else {
      upstreamSignal?.addEventListener('abort', abort, { once: true });
    }

    try {
      assertActive(controller.signal);
      const input = await adapter.read({ request, signal: controller.signal });
      assertActive(controller.signal);
      return validateWorldFocusBoundary(input, (value) =>
        validateReadResult(value, request),
      );
    } finally {
      upstreamSignal?.removeEventListener('abort', abort);
    }
  };
}
