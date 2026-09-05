import {
  createWorldFocusContextReferenceSet,
  sameWorldFocusContextReferenceSet,
  type WorldFocusContextReferenceSet,
} from '../model/world-focus-context-reference';
import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from '../model/world-focus-identity';
import {
  isWorldFocusDanteConversationResultClass,
  type WorldFocusDanteConversationResultClass,
} from './world-focus-dante-conversation';
import {
  validateWorldFocusBoundary,
  type WorldFocusValidationIssue,
  type WorldFocusValidationResult,
} from './world-focus-foundation';

export const WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION = 1 as const;
export const WORLD_FOCUS_DANTE_INSIGHT_MAX_TITLE_LENGTH = 120;
export const WORLD_FOCUS_DANTE_INSIGHT_MAX_SUMMARY_LENGTH = 2_000;
export const WORLD_FOCUS_DANTE_INSIGHT_MAX_SOURCE_LENGTH = 8_000;

export const WORLD_FOCUS_DANTE_INSIGHT_KINDS = [
  'observation',
  'pattern',
  'change',
] as const;

export type WorldFocusDanteInsightKind =
  (typeof WORLD_FOCUS_DANTE_INSIGHT_KINDS)[number];

export type WorldFocusDanteInsightRequest = Readonly<{
  schemaVersion: typeof WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION;
  requestId: string;
  worldId: WorldFocusId;
  workspaceGeneration: number;
  sourceMessageId: string;
  sourceResultClass: WorldFocusDanteConversationResultClass;
  sourceText: string;
  locale: string;
  contextReferences: WorldFocusContextReferenceSet;
}>;

export type WorldFocusDanteInsightRequestInput = Omit<
  WorldFocusDanteInsightRequest,
  'schemaVersion'
>;

export type WorldFocusDanteInsight = Readonly<{
  schemaVersion: typeof WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION;
  insightId: string;
  worldId: WorldFocusId;
  workspaceGeneration: number;
  kind: WorldFocusDanteInsightKind;
  title: string;
  summary: string;
  basisReferences: WorldFocusContextReferenceSet;
}>;

export type WorldFocusDanteInsightReadResult =
  | Readonly<{
      schemaVersion: typeof WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION;
      status: 'ready';
      requestId: string;
      worldId: WorldFocusId;
      workspaceGeneration: number;
      insight: WorldFocusDanteInsight;
    }>
  | Readonly<{
      schemaVersion: typeof WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION;
      status: 'unavailable';
      requestId: string;
      worldId: WorldFocusId;
      workspaceGeneration: number;
      reasonCode: string;
      retryable: boolean;
    }>;

export type WorldFocusDanteInsightReadAdapter = Readonly<{
  read: (request: Readonly<{
    request: WorldFocusDanteInsightRequest;
    signal: AbortSignal;
  }>) => Promise<unknown>;
}>;

export type WorldFocusDanteInsightReader = (
  request: WorldFocusDanteInsightRequest,
  signal?: AbortSignal,
) => Promise<WorldFocusDanteInsightReadResult>;

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
  return keys.length === expected.length && keys.every((key) => expected.includes(key));
}

function readBoundedString(value: unknown, maxLength: number): string | null {
  if (typeof value !== 'string') return null;
  const trimmed = value.trim();
  return trimmed.length > 0 && trimmed.length <= maxLength ? trimmed : null;
}

function isNonNegativeInteger(value: unknown): value is number {
  return typeof value === 'number' && Number.isInteger(value) && value >= 0;
}

export function isWorldFocusDanteInsightKind(
  value: unknown,
): value is WorldFocusDanteInsightKind {
  return (
    typeof value === 'string' &&
    WORLD_FOCUS_DANTE_INSIGHT_KINDS.some((kind) => kind === value)
  );
}

export function createWorldFocusDanteInsightRequest(
  input: WorldFocusDanteInsightRequestInput,
): WorldFocusDanteInsightRequest {
  const worldId = normalizeWorldFocusId(input.worldId);
  const requestId = readBoundedString(input.requestId, 128);
  const sourceMessageId = readBoundedString(input.sourceMessageId, 160);
  const sourceText = readBoundedString(
    input.sourceText,
    WORLD_FOCUS_DANTE_INSIGHT_MAX_SOURCE_LENGTH,
  );
  const locale = readBoundedString(input.locale, 32);

  if (
    worldId === undefined ||
    requestId === null ||
    sourceMessageId === null ||
    sourceText === null ||
    locale === null ||
    !isNonNegativeInteger(input.workspaceGeneration) ||
    !isWorldFocusDanteConversationResultClass(input.sourceResultClass)
  ) {
    throw new Error('World Focus DANTE Insight request is invalid');
  }

  const contextReferences = createWorldFocusContextReferenceSet({
    primary: input.contextReferences.primary,
    supporting: input.contextReferences.supporting,
  });

  return Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
    requestId,
    worldId,
    workspaceGeneration: input.workspaceGeneration,
    sourceMessageId,
    sourceResultClass: input.sourceResultClass,
    sourceText,
    locale,
    contextReferences,
  });
}

function validateReadyResult(
  input: Record<string, unknown>,
  expectedRequest: WorldFocusDanteInsightRequest,
): WorldFocusValidationResult<WorldFocusDanteInsightReadResult> {
  if (
    !hasExactKeys(input, [
      'schemaVersion',
      'status',
      'requestId',
      'worldId',
      'workspaceGeneration',
      'insightId',
      'kind',
      'title',
      'summary',
    ]) ||
    !isWorldFocusDanteInsightKind(input.kind)
  ) {
    return { ok: false, issues: [issue('insight.ready.shape')] };
  }

  const insightId = readBoundedString(input.insightId, 160);
  const title = readBoundedString(
    input.title,
    WORLD_FOCUS_DANTE_INSIGHT_MAX_TITLE_LENGTH,
  );
  const summary = readBoundedString(
    input.summary,
    WORLD_FOCUS_DANTE_INSIGHT_MAX_SUMMARY_LENGTH,
  );
  if (insightId === null || title === null || summary === null) {
    return { ok: false, issues: [issue('insight.ready.value')] };
  }

  const insight = Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
    insightId,
    worldId: expectedRequest.worldId,
    workspaceGeneration: expectedRequest.workspaceGeneration,
    kind: input.kind,
    title,
    summary,
    basisReferences: createWorldFocusContextReferenceSet({
      primary: expectedRequest.contextReferences.primary,
      supporting: expectedRequest.contextReferences.supporting,
    }),
  });

  if (!sameWorldFocusContextReferenceSet(insight.basisReferences, expectedRequest.contextReferences)) {
    return { ok: false, issues: [issue('insight.ready.basis')] };
  }

  return {
    ok: true,
    value: Object.freeze({
      schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
      status: 'ready' as const,
      requestId: expectedRequest.requestId,
      worldId: expectedRequest.worldId,
      workspaceGeneration: expectedRequest.workspaceGeneration,
      insight,
    }),
  };
}

function validateReadResult(
  input: unknown,
  expectedRequest: WorldFocusDanteInsightRequest,
): WorldFocusValidationResult<WorldFocusDanteInsightReadResult> {
  if (!isRecord(input)) {
    return { ok: false, issues: [issue('insight.result.record')] };
  }

  const worldId = normalizeWorldFocusId(input.worldId);
  if (
    input.schemaVersion !== WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION ||
    input.requestId !== expectedRequest.requestId ||
    worldId !== expectedRequest.worldId ||
    input.workspaceGeneration !== expectedRequest.workspaceGeneration
  ) {
    return { ok: false, issues: [issue('insight.result.correlation')] };
  }

  if (input.status === 'ready') {
    return validateReadyResult(input, expectedRequest);
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
      return { ok: false, issues: [issue('insight.unavailable.shape')] };
    }
    const reasonCode = readBoundedString(input.reasonCode, 128);
    if (reasonCode === null || typeof input.retryable !== 'boolean') {
      return { ok: false, issues: [issue('insight.unavailable.value')] };
    }
    return {
      ok: true,
      value: Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
        status: 'unavailable' as const,
        requestId: expectedRequest.requestId,
        worldId: expectedRequest.worldId,
        workspaceGeneration: expectedRequest.workspaceGeneration,
        reasonCode,
        retryable: input.retryable,
      }),
    };
  }

  return { ok: false, issues: [issue('insight.result.status')] };
}

function assertActive(signal: AbortSignal): void {
  if (!signal.aborted) return;
  const error = new Error('World Focus DANTE Insight read aborted');
  error.name = 'AbortError';
  throw error;
}

/**
 * D5 provider-neutral pre-backend Insight boundary. A conversation message may
 * be the explicit source of a request, but only a separately validated result
 * becomes an Insight artifact. The basis is reconstructed from the bounded
 * request context; the adapter cannot widen it. Canonical truth, authorization,
 * Proposal/Decision/effect semantics and provider transport remain outside.
 */
export function createWorldFocusDanteInsightReader(
  adapter: WorldFocusDanteInsightReadAdapter,
): WorldFocusDanteInsightReader {
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
