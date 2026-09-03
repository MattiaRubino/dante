import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from './world-focus-context-reference';
import type { WorldFocusEvidenceReferenceFacet } from './world-focus-evidence';
import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from './world-focus-identity';

export const WORLD_FOCUS_SITUATION_FIRST_OPEN_LIMIT = 6;
export const WORLD_FOCUS_NEXT_FIRST_OPEN_LIMIT = 6;
export const WORLD_FOCUS_EVIDENCE_HISTORY_FIRST_OPEN_LIMIT = 8;

export type WorldFocusSituationProjection = Readonly<{
  schemaVersion: 1;
  worldId: WorldFocusId;
  orderedSituationReferences: readonly WorldFocusContextReference[];
}>;

export type WorldFocusNextProjection = Readonly<{
  schemaVersion: 1;
  worldId: WorldFocusId;
  orderedNextReferences: readonly WorldFocusContextReference[];
}>;

export type WorldFocusEvidenceHistoryProjection = Readonly<{
  schemaVersion: 1;
  worldId: WorldFocusId;
  evidence: WorldFocusEvidenceReferenceFacet;
  orderedHistoryReferences: readonly WorldFocusContextReference[];
}>;

function normalizeWorldId(worldId: WorldFocusId): WorldFocusId {
  const normalized = normalizeWorldFocusId(worldId);
  if (normalized === undefined) {
    throw new Error('World Focus direct projection World id must not be empty');
  }
  return normalized;
}

function referenceIdentity(reference: WorldFocusContextReference): string {
  return `${reference.kind}\u0000${reference.key}`;
}

function normalizeDistinctReferences(
  references: readonly WorldFocusContextReference[],
  maximum: number,
  label: string,
  minimum = 1,
): readonly WorldFocusContextReference[] {
  if (references.length < minimum) {
    throw new Error(`${label} must contain at least ${minimum} reference${minimum === 1 ? '' : 's'}`);
  }
  if (references.length > maximum) {
    throw new Error(`${label} exceed first-open limit ${maximum}`);
  }

  const seen = new Set<string>();
  return Object.freeze(
    references.map((reference, index) => {
      const normalized = normalizeWorldFocusContextReference(
        reference,
        `${label}[${index}]`,
      );
      const identity = referenceIdentity(normalized);
      if (seen.has(identity)) {
        throw new Error(`${label} must not contain duplicate references`);
      }
      seen.add(identity);
      return normalized;
    }),
  );
}

/** O2 — direct typed/application Situation references only. */
export function createWorldFocusSituationProjection(input: Readonly<{
  worldId: WorldFocusId;
  orderedSituationReferences: readonly WorldFocusContextReference[];
}>): WorldFocusSituationProjection {
  return Object.freeze({
    schemaVersion: 1 as const,
    worldId: normalizeWorldId(input.worldId),
    orderedSituationReferences: normalizeDistinctReferences(
      input.orderedSituationReferences,
      WORLD_FOCUS_SITUATION_FIRST_OPEN_LIMIT,
      'World Focus Situation references',
    ),
  });
}

/** O5 — direct Plan/Schedule/Dependency/Request/etc. references only. */
export function createWorldFocusNextProjection(input: Readonly<{
  worldId: WorldFocusId;
  orderedNextReferences: readonly WorldFocusContextReference[];
}>): WorldFocusNextProjection {
  return Object.freeze({
    schemaVersion: 1 as const,
    worldId: normalizeWorldId(input.worldId),
    orderedNextReferences: normalizeDistinctReferences(
      input.orderedNextReferences,
      WORLD_FOCUS_NEXT_FIRST_OPEN_LIMIT,
      'World Focus Next references',
    ),
  });
}

/** O8 — reference-only Evidence/History seam; source payload stays upstream. */
export function createWorldFocusEvidenceHistoryProjection(input: Readonly<{
  worldId: WorldFocusId;
  evidence: WorldFocusEvidenceReferenceFacet;
  orderedHistoryReferences: readonly WorldFocusContextReference[];
}>): WorldFocusEvidenceHistoryProjection {
  return Object.freeze({
    schemaVersion: 1 as const,
    worldId: normalizeWorldId(input.worldId),
    evidence: input.evidence,
    orderedHistoryReferences: normalizeDistinctReferences(
      input.orderedHistoryReferences,
      WORLD_FOCUS_EVIDENCE_HISTORY_FIRST_OPEN_LIMIT,
      'World Focus Evidence/History references',
      0,
    ),
  });
}
