import { describe, expect, it } from 'vitest';

import {
  createWorldFocusEvidenceReferenceFacet,
  type WorldFocusEvidenceReferencePolicy,
} from './world-focus-evidence';

const POLICY: WorldFocusEvidenceReferencePolicy = {
  maxEvidenceReferences: 2,
  maxProvenanceReferences: 2,
  maxIntegrityAttestationReferences: 2,
};

const ref = (kind: string, key: string) => ({ kind, key });

describe('World Focus M1-2 evidence/reference facet', () => {
  it('keeps evidence, provenance and integrity-attestation as separate reference roles', () => {
    const facet = createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences: [ref('observation', 'obs-1')],
        provenanceReferences: [ref('provenance', 'prov-1')],
        integrityAttestationReferences: [ref('attestation', 'att-1')],
      },
      POLICY,
    );

    expect(facet).toEqual({
      evidenceReferences: [{ kind: 'observation', key: 'obs-1' }],
      provenanceReferences: [{ kind: 'provenance', key: 'prov-1' }],
      integrityAttestationReferences: [{ kind: 'attestation', key: 'att-1' }],
    });
    expect('confidence' in facet).toBe(false);
    expect('winner' in facet).toBe(false);
    expect('trusted' in facet).toBe(false);
  });

  it('rejects an empty facet instead of inventing evidence', () => {
    expect(() =>
      createWorldFocusEvidenceReferenceFacet(
        {
          evidenceReferences: [],
          provenanceReferences: [],
          integrityAttestationReferences: [],
        },
        POLICY,
      ),
    ).toThrow();
  });

  it('rejects duplicate, blank and unbounded references within each role', () => {
    expect(() =>
      createWorldFocusEvidenceReferenceFacet(
        {
          evidenceReferences: [ref('observation', 'obs-1'), ref('observation', 'obs-1')],
          provenanceReferences: [],
          integrityAttestationReferences: [],
        },
        POLICY,
      ),
    ).toThrow();

    expect(() =>
      createWorldFocusEvidenceReferenceFacet(
        {
          evidenceReferences: [ref(' ', 'obs-1')],
          provenanceReferences: [],
          integrityAttestationReferences: [],
        },
        POLICY,
      ),
    ).toThrow();

    expect(() =>
      createWorldFocusEvidenceReferenceFacet(
        {
          evidenceReferences: [
            ref('observation', 'obs-1'),
            ref('observation', 'obs-2'),
            ref('observation', 'obs-3'),
          ],
          provenanceReferences: [],
          integrityAttestationReferences: [],
        },
        POLICY,
      ),
    ).toThrow();
  });
});
