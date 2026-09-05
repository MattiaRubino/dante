import {
  createWorldFocusContextReferenceSet,
  sameWorldFocusContextReferenceSet,
  type WorldFocusContextReferenceSet,
} from '../model/world-focus-context-reference';
import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from '../model/world-focus-identity';
import type { WorldFocusDanteInsightKind } from './world-focus-dante-insight';
import {
  validateWorldFocusBoundary,
  type WorldFocusValidationIssue,
  type WorldFocusValidationResult,
} from './world-focus-foundation';

export const WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION = 1 as const;
export const WORLD_FOCUS_DANTE_PROPOSAL_MAX_TITLE_LENGTH = 120;
export const WORLD_FOCUS_DANTE_PROPOSAL_MAX_TARGET_LENGTH = 120;
export const WORLD_FOCUS_DANTE_PROPOSAL_MAX_CHANGE_LENGTH = 2_000;
export const WORLD_FOCUS_DANTE_PROPOSAL_MAX_SOURCE_LENGTH = 2_000;

export type WorldFocusDanteProposalRequest = Readonly<{
  schemaVersion: typeof WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION;
  requestId: string;
  worldId: WorldFocusId;
  workspaceGeneration: number;
  sourceInsightId: string;
  sourceInsightKind: WorldFocusDanteInsightKind;
  sourceTitle: string;
  sourceSummary: string;
  locale: string;
  contextReferences: WorldFocusContextReferenceSet;
}>;

export type WorldFocusDanteProposalRequestInput = Omit<
  WorldFocusDanteProposalRequest,
  'schemaVersion'
>;

export type WorldFocusDanteProposal = Readonly<{
  schemaVersion: typeof WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION;
  proposalId: string;
  worldId: WorldFocusId;
  workspaceGeneration: number;
  sourceInsightId: string;
  title: string;
  targetLabel: string;
  changeSummary: string;
  decisionRequirement: 'explicit-confirmation';
  basisReferences: WorldFocusContextReferenceSet;
}>;

export type WorldFocusDanteProposalReadResult =
  | Readonly<{
      schemaVersion: typeof WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION;
      status: 'ready';
      requestId: string;
      worldId: WorldFocusId;
      workspaceGeneration: number;
      proposal: WorldFocusDanteProposal;
    }>
  | Readonly<{
      schemaVersion: typeof WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION;
      status: 'unavailable';
      requestId: string;
      worldId: WorldFocusId;
      workspaceGeneration: number;
      reasonCode: string;
      retryable: boolean;
    }>;

export type WorldFocusDanteProposalReadAdapter = Readonly<{
  read: (input: Readonly<{
    request: WorldFocusDanteProposalRequest;
    signal: AbortSignal;
  }>) => Promise<unknown>;
}>;

export type WorldFocusDanteProposalReader = (
  request: WorldFocusDanteProposalRequest,
  signal?: AbortSignal,
) => Promise<WorldFocusDanteProposalReadResult>;

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

export function createWorldFocusDanteProposalRequest(
  input: WorldFocusDanteProposalRequestInput,
): WorldFocusDanteProposalRequest {
  const worldId = normalizeWorldFocusId(input.worldId);
  const requestId = readBoundedString(input.requestId, 128);
  const sourceInsightId = readBoundedString(input.sourceInsightId, 160);
  const sourceTitle = readBoundedString(
    input.sourceTitle,
    WORLD_FOCUS_DANTE_PROPOSAL_MAX_TITLE_LENGTH,
  );
  const sourceSummary = readBoundedString(
    input.sourceSummary,
    WORLD_FOCUS_DANTE_PROPOSAL_MAX_SOURCE_LENGTH,
  );
  const locale = readBoundedString(input.locale, 32);

  if (
    worldId === undefined ||
    requestId === null ||
    sourceInsightId === null ||
    sourceTitle === null ||
    sourceSummary === null ||
    locale === null ||
    !isNonNegativeInteger(input.workspaceGeneration) ||
    !['observation', 'pattern', 'change'].includes(input.sourceInsightKind)
  ) {
    throw new Error('World Focus DANTE Proposal request is invalid');
  }

  const contextReferences = createWorldFocusContextReferenceSet({
    primary: input.contextReferences.primary,
    supporting: input.contextReferences.supporting,
  });

  return Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
    requestId,
    worldId,
    workspaceGeneration: input.workspaceGeneration,
    sourceInsightId,
    sourceInsightKind: input.sourceInsightKind,
    sourceTitle,
    sourceSummary,
    locale,
    contextReferences,
  });
}

function validateReadyResult(
  input: Record<string, unknown>,
  expectedRequest: WorldFocusDanteProposalRequest,
): WorldFocusValidationResult<WorldFocusDanteProposalReadResult> {
  if (
    !hasExactKeys(input, [
      'schemaVersion',
      'status',
      'requestId',
      'worldId',
      'workspaceGeneration',
      'proposalId',
      'title',
      'targetLabel',
      'changeSummary',
    ])
  ) {
    return { ok: false, issues: [issue('proposal.ready.shape')] };
  }

  const proposalId = readBoundedString(input.proposalId, 160);
  const title = readBoundedString(
    input.title,
    WORLD_FOCUS_DANTE_PROPOSAL_MAX_TITLE_LENGTH,
  );
  const targetLabel = readBoundedString(
    input.targetLabel,
    WORLD_FOCUS_DANTE_PROPOSAL_MAX_TARGET_LENGTH,
  );
  const changeSummary = readBoundedString(
    input.changeSummary,
    WORLD_FOCUS_DANTE_PROPOSAL_MAX_CHANGE_LENGTH,
  );
  if (
    proposalId === null ||
    title === null ||
    targetLabel === null ||
    changeSummary === null
  ) {
    return { ok: false, issues: [issue('proposal.ready.value')] };
  }

  const proposal = Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
    proposalId,
    worldId: expectedRequest.worldId,
    workspaceGeneration: expectedRequest.workspaceGeneration,
    sourceInsightId: expectedRequest.sourceInsightId,
    title,
    targetLabel,
    changeSummary,
    decisionRequirement: 'explicit-confirmation' as const,
    basisReferences: createWorldFocusContextReferenceSet({
      primary: expectedRequest.contextReferences.primary,
      supporting: expectedRequest.contextReferences.supporting,
    }),
  });

  if (
    !sameWorldFocusContextReferenceSet(
      proposal.basisReferences,
      expectedRequest.contextReferences,
    )
  ) {
    return { ok: false, issues: [issue('proposal.ready.basis')] };
  }

  return {
    ok: true,
    value: Object.freeze({
      schemaVersion: WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
      status: 'ready' as const,
      requestId: expectedRequest.requestId,
      worldId: expectedRequest.worldId,
      workspaceGeneration: expectedRequest.workspaceGeneration,
      proposal,
    }),
  };
}

function validateReadResult(
  input: unknown,
  expectedRequest: WorldFocusDanteProposalRequest,
): WorldFocusValidationResult<WorldFocusDanteProposalReadResult> {
  if (!isRecord(input)) {
    return { ok: false, issues: [issue('proposal.result.record')] };
  }

  const worldId = normalizeWorldFocusId(input.worldId);
  if (
    input.schemaVersion !== WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION ||
    input.requestId !== expectedRequest.requestId ||
    worldId !== expectedRequest.worldId ||
    input.workspaceGeneration !== expectedRequest.workspaceGeneration
  ) {
    return { ok: false, issues: [issue('proposal.result.correlation')] };
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
      return { ok: false, issues: [issue('proposal.unavailable.shape')] };
    }
    const reasonCode = readBoundedString(input.reasonCode, 128);
    if (reasonCode === null || typeof input.retryable !== 'boolean') {
      return { ok: false, issues: [issue('proposal.unavailable.value')] };
    }
    return {
      ok: true,
      value: Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
        status: 'unavailable' as const,
        requestId: expectedRequest.requestId,
        worldId: expectedRequest.worldId,
        workspaceGeneration: expectedRequest.workspaceGeneration,
        reasonCode,
        retryable: input.retryable,
      }),
    };
  }

  return { ok: false, issues: [issue('proposal.result.status')] };
}

function assertActive(signal: AbortSignal): void {
  if (!signal.aborted) return;
  const error = new Error('World Focus DANTE Proposal read aborted');
  error.name = 'AbortError';
  throw error;
}

/**
 * D6 provider-neutral pre-backend Proposal boundary. A validated D5 Insight may
 * explicitly seed a proposal request, but only this separately validated result
 * becomes a Proposal. The adapter cannot widen basis references or manufacture
 * Decision/effect/provider-completion semantics.
 */
export function createWorldFocusDanteProposalReader(
  adapter: WorldFocusDanteProposalReadAdapter,
): WorldFocusDanteProposalReader {
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
