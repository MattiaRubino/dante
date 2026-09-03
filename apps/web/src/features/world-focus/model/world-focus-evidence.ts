import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from './world-focus-context-reference';

export type WorldFocusEvidenceReferencePolicy = Readonly<{
  maxEvidenceReferences: number;
  maxProvenanceReferences: number;
  maxIntegrityAttestationReferences: number;
}>;

export type WorldFocusEvidenceReferenceFacet = Readonly<{
  evidenceReferences: readonly WorldFocusContextReference[];
  provenanceReferences: readonly WorldFocusContextReference[];
  integrityAttestationReferences: readonly WorldFocusContextReference[];
}>;

function assertReferenceMaximum(value: number, label: string): number {
  if (!Number.isInteger(value) || value < 0) {
    throw new Error(`${label} must be a non-negative integer`);
  }
  return value;
}

function referenceIdentity(reference: WorldFocusContextReference): string {
  return `${reference.kind}\u0000${reference.key}`;
}

function normalizeDistinctReferences(
  references: readonly WorldFocusContextReference[],
  maximum: number,
  label: string,
): readonly WorldFocusContextReference[] {
  const boundedMaximum = assertReferenceMaximum(maximum, `${label} maximum`);
  if (references.length > boundedMaximum) {
    throw new Error(`${label} exceed configured maximum ${boundedMaximum}`);
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

/**
 * L2 evidence metadata is deliberately reference-only and role-preserving.
 * Evidence, provenance and integrity/attestation can coexist but one role never
 * substitutes for another, and this facet carries no confidence/winner policy.
 */
export function createWorldFocusEvidenceReferenceFacet(
  input: WorldFocusEvidenceReferenceFacet,
  policy: WorldFocusEvidenceReferencePolicy,
): WorldFocusEvidenceReferenceFacet {
  const evidenceReferences = normalizeDistinctReferences(
    input.evidenceReferences,
    policy.maxEvidenceReferences,
    'World Focus evidence references',
  );
  const provenanceReferences = normalizeDistinctReferences(
    input.provenanceReferences,
    policy.maxProvenanceReferences,
    'World Focus provenance references',
  );
  const integrityAttestationReferences = normalizeDistinctReferences(
    input.integrityAttestationReferences,
    policy.maxIntegrityAttestationReferences,
    'World Focus integrity/attestation references',
  );

  if (
    evidenceReferences.length === 0 &&
    provenanceReferences.length === 0 &&
    integrityAttestationReferences.length === 0
  ) {
    throw new Error('World Focus evidence facet must contain at least one reference');
  }

  return Object.freeze({
    evidenceReferences,
    provenanceReferences,
    integrityAttestationReferences,
  });
}
