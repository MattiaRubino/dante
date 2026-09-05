import {
  createWorldFocusContextReferenceSet,
  type WorldFocusContextReference,
  type WorldFocusContextReferenceSet,
} from '../model/world-focus-context-reference';
import type { WorldFocusContinuityItem } from '../model/world-focus-continuity';
import type {
  WorldFocusAttentionPrimitive,
  WorldFocusComparisonPrimitive,
} from '../model/world-focus-work-primitives';

export const WORLD_FOCUS_DANTE_CONTEXTUAL_INTENTS = [
  'why',
  'compare',
  'continue',
  'open-source',
] as const;

export type WorldFocusDanteContextualIntent =
  (typeof WORLD_FOCUS_DANTE_CONTEXTUAL_INTENTS)[number];

function tryCreateReferenceSet(
  primary: WorldFocusContextReference,
  supporting: readonly WorldFocusContextReference[],
): WorldFocusContextReferenceSet | null {
  try {
    return createWorldFocusContextReferenceSet({ primary, supporting });
  } catch {
    return null;
  }
}

/**
 * Converts already-materialized Attention semantics into bounded contextual
 * coordinates only. Display copy, payloads, authorization and disclosure state
 * deliberately do not cross this boundary.
 */
export function createWorldFocusDanteAttentionContext(
  primitive: WorldFocusAttentionPrimitive,
): WorldFocusContextReferenceSet | null {
  return tryCreateReferenceSet(
    primitive.matterReference,
    primitive.resolutionReference === null
      ? []
      : [primitive.resolutionReference],
  );
}

/**
 * Comparison preserves every required subject plus its optional basis. If the
 * existing bounded reference-set policy cannot represent the complete meaning,
 * D4 fails closed rather than silently truncating context.
 */
export function createWorldFocusDanteComparisonContext(
  primitive: WorldFocusComparisonPrimitive,
): WorldFocusContextReferenceSet | null {
  const primary = primitive.subjectReferences[0];
  const supporting = [
    ...primitive.subjectReferences.slice(1),
    ...(primitive.basisReference === null ? [] : [primitive.basisReference]),
  ];
  return tryCreateReferenceSet(primary, supporting);
}

/**
 * Continuity binds the visible thread to the exact checkpoint and optional
 * continuation coordinate that already back the projection item.
 */
export function createWorldFocusDanteContinuityContext(
  item: WorldFocusContinuityItem,
): WorldFocusContextReferenceSet | null {
  return tryCreateReferenceSet(item.threadReference, [
    item.checkpointReference,
    ...(item.continuationReference === null ? [] : [item.continuationReference]),
  ]);
}

/**
 * Only an actual Evidence reference receives the D4 source-opening deictic
 * coordinate. Provenance, integrity and history remain separate semantic roles.
 */
export function createWorldFocusDanteEvidenceContext(
  reference: WorldFocusContextReference,
): WorldFocusContextReferenceSet | null {
  return tryCreateReferenceSet(reference, []);
}
