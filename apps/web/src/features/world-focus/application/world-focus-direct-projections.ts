import {
  createWorldFocusEvidenceHistoryProjection,
  createWorldFocusNextProjection,
  createWorldFocusSituationProjection,
  type WorldFocusEvidenceHistoryProjection,
  type WorldFocusNextProjection,
  type WorldFocusSituationProjection,
} from '../model/world-focus-direct-projections';
import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from '../model/world-focus-context-reference';
import {
  createWorldFocusEvidenceReferenceFacet,
  type WorldFocusEvidenceReferenceFacet,
} from '../model/world-focus-evidence';
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

const EVIDENCE_POLICY = Object.freeze({
  maxEvidenceReferences: 8,
  maxProvenanceReferences: 8,
  maxIntegrityAttestationReferences: 8,
});

export type WorldFocusSituationReadResult =
  | Readonly<{ status: 'ready'; projection: WorldFocusSituationProjection }>
  | Readonly<{ status: 'empty'; worldId: WorldFocusId }>;

export type WorldFocusNextReadResult =
  | Readonly<{ status: 'ready'; projection: WorldFocusNextProjection }>
  | Readonly<{ status: 'empty'; worldId: WorldFocusId }>;

export type WorldFocusEvidenceHistoryReadResult =
  | Readonly<{
      status: 'ready';
      projection: WorldFocusEvidenceHistoryProjection;
    }>
  | Readonly<{ status: 'empty'; worldId: WorldFocusId }>;

export type WorldFocusDirectProjectionReadAdapter = Readonly<{
  readSituation: WorldFocusScopedReadAdapter;
  readNext: WorldFocusScopedReadAdapter;
  readEvidenceHistory: WorldFocusScopedReadAdapter;
}>;

export type WorldFocusDirectProjectionReaders = Readonly<{
  readSituation: WorldFocusScopedReader<WorldFocusSituationReadResult>;
  readNext: WorldFocusScopedReader<WorldFocusNextReadResult>;
  readEvidenceHistory: WorldFocusScopedReader<WorldFocusEvidenceHistoryReadResult>;
}>;

function issue(code: string): WorldFocusValidationIssue {
  return Object.freeze({ code, path: Object.freeze([]) });
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
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

function readReferenceArray(value: unknown): readonly WorldFocusContextReference[] | null {
  if (!Array.isArray(value)) {
    return null;
  }
  const references: WorldFocusContextReference[] = [];
  for (const item of value) {
    const reference = readReference(item);
    if (reference === null) {
      return null;
    }
    references.push(reference);
  }
  return Object.freeze(references);
}

function validateEmpty(
  input: Record<string, unknown>,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<Readonly<{ status: 'empty'; worldId: WorldFocusId }>> | null {
  if (input.status !== 'empty') {
    return null;
  }
  const worldId = normalizeWorldFocusId(input.worldId);
  return worldId === expectedWorldId
    ? { ok: true, value: Object.freeze({ status: 'empty' as const, worldId }) }
    : { ok: false, issues: [issue('result.worldId')] };
}

function validateSituationResult(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusSituationReadResult> {
  if (!isRecord(input)) return { ok: false, issues: [issue('result.record')] };
  const empty = validateEmpty(input, expectedWorldId);
  if (empty !== null) return empty;
  if (input.status !== 'ready' || !isRecord(input.projection)) {
    return { ok: false, issues: [issue('result.status')] };
  }
  const projection = input.projection;
  const worldId = normalizeWorldFocusId(projection.worldId);
  const references = readReferenceArray(projection.orderedSituationReferences);
  if (projection.schemaVersion !== 1 || worldId !== expectedWorldId || references === null) {
    return { ok: false, issues: [issue('projection.invalid')] };
  }
  try {
    return {
      ok: true,
      value: Object.freeze({
        status: 'ready' as const,
        projection: createWorldFocusSituationProjection({
          worldId,
          orderedSituationReferences: references,
        }),
      }),
    };
  } catch {
    return { ok: false, issues: [issue('projection.invalid')] };
  }
}

function validateNextResult(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusNextReadResult> {
  if (!isRecord(input)) return { ok: false, issues: [issue('result.record')] };
  const empty = validateEmpty(input, expectedWorldId);
  if (empty !== null) return empty;
  if (input.status !== 'ready' || !isRecord(input.projection)) {
    return { ok: false, issues: [issue('result.status')] };
  }
  const projection = input.projection;
  const worldId = normalizeWorldFocusId(projection.worldId);
  const references = readReferenceArray(projection.orderedNextReferences);
  if (projection.schemaVersion !== 1 || worldId !== expectedWorldId || references === null) {
    return { ok: false, issues: [issue('projection.invalid')] };
  }
  try {
    return {
      ok: true,
      value: Object.freeze({
        status: 'ready' as const,
        projection: createWorldFocusNextProjection({
          worldId,
          orderedNextReferences: references,
        }),
      }),
    };
  } catch {
    return { ok: false, issues: [issue('projection.invalid')] };
  }
}

function readEvidenceFacet(value: unknown): WorldFocusEvidenceReferenceFacet | null {
  if (!isRecord(value)) return null;
  const evidenceReferences = readReferenceArray(value.evidenceReferences);
  const provenanceReferences = readReferenceArray(value.provenanceReferences);
  const integrityAttestationReferences = readReferenceArray(
    value.integrityAttestationReferences,
  );
  if (
    evidenceReferences === null ||
    provenanceReferences === null ||
    integrityAttestationReferences === null
  ) {
    return null;
  }
  try {
    return createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences,
        provenanceReferences,
        integrityAttestationReferences,
      },
      EVIDENCE_POLICY,
    );
  } catch {
    return null;
  }
}

function validateEvidenceHistoryResult(
  input: unknown,
  expectedWorldId: WorldFocusId,
): WorldFocusValidationResult<WorldFocusEvidenceHistoryReadResult> {
  if (!isRecord(input)) return { ok: false, issues: [issue('result.record')] };
  const empty = validateEmpty(input, expectedWorldId);
  if (empty !== null) return empty;
  if (input.status !== 'ready' || !isRecord(input.projection)) {
    return { ok: false, issues: [issue('result.status')] };
  }
  const projection = input.projection;
  const worldId = normalizeWorldFocusId(projection.worldId);
  const evidence = readEvidenceFacet(projection.evidence);
  const historyReferences = readReferenceArray(projection.orderedHistoryReferences);
  if (
    projection.schemaVersion !== 1 ||
    worldId !== expectedWorldId ||
    evidence === null ||
    historyReferences === null
  ) {
    return { ok: false, issues: [issue('projection.invalid')] };
  }
  try {
    return {
      ok: true,
      value: Object.freeze({
        status: 'ready' as const,
        projection: createWorldFocusEvidenceHistoryProjection({
          worldId,
          evidence,
          orderedHistoryReferences: historyReferences,
        }),
      }),
    };
  } catch {
    return { ok: false, issues: [issue('projection.invalid')] };
  }
}

export function createWorldFocusDirectProjectionReaders(
  adapter: WorldFocusDirectProjectionReadAdapter,
): WorldFocusDirectProjectionReaders {
  return Object.freeze({
    readSituation: createWorldFocusScopedReader(
      adapter.readSituation,
      validateSituationResult,
    ),
    readNext: createWorldFocusScopedReader(adapter.readNext, validateNextResult),
    readEvidenceHistory: createWorldFocusScopedReader(
      adapter.readEvidenceHistory,
      validateEvidenceHistoryResult,
    ),
  });
}
