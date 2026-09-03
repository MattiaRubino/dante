import { describe, expect, it } from 'vitest';

import { createWorldFocusEvidenceReferenceFacet } from './world-focus-evidence';
import {
  createWorldFocusEvidenceHistoryProjection,
  createWorldFocusNextProjection,
  createWorldFocusSituationProjection,
  WORLD_FOCUS_EVIDENCE_HISTORY_FIRST_OPEN_LIMIT,
  WORLD_FOCUS_NEXT_FIRST_OPEN_LIMIT,
  WORLD_FOCUS_SITUATION_FIRST_OPEN_LIMIT,
} from './world-focus-direct-projections';

const ref = (kind: string, key: string) => ({ kind, key });

describe('World Focus M1-2 direct Output Grammar projections', () => {
  it('accepts an unknown future World id without requiring the fixture catalog', () => {
    const situation = createWorldFocusSituationProjection({
      worldId: 'apiary',
      orderedSituationReferences: [ref('observation', 'hive-7-temperature')],
    });

    expect(situation.worldId).toBe('apiary');
    expect(situation.orderedSituationReferences).toEqual([
      { kind: 'observation', key: 'hive-7-temperature' },
    ]);
  });

  it('keeps O2 Situation and O5 Next as bounded typed references rather than generic payload bags', () => {
    const next = createWorldFocusNextProjection({
      worldId: 'music',
      orderedNextReferences: [
        ref('schedule', 'release-day'),
        ref('dependency', 'artwork-approval'),
      ],
    });

    expect(next).toEqual({
      schemaVersion: 1,
      worldId: 'music',
      orderedNextReferences: [
        { kind: 'schedule', key: 'release-day' },
        { kind: 'dependency', key: 'artwork-approval' },
      ],
    });
    expect('data' in next).toBe(false);
    expect('properties' in next).toBe(false);
    expect('goal' in next).toBe(false);
    expect('priorityScore' in next).toBe(false);
  });

  it('keeps O8 Evidence/History reference-only and evidence-role aware', () => {
    const evidence = createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences: [ref('observation', 'mix-review')],
        provenanceReferences: [ref('provenance', 'studio-import')],
        integrityAttestationReferences: [],
      },
      {
        maxEvidenceReferences: 3,
        maxProvenanceReferences: 3,
        maxIntegrityAttestationReferences: 3,
      },
    );
    const projection = createWorldFocusEvidenceHistoryProjection({
      worldId: 'music',
      evidence,
      orderedHistoryReferences: [ref('material-state', 'master-v2')],
    });

    expect(projection.evidence).toEqual(evidence);
    expect(projection.orderedHistoryReferences).toEqual([
      { kind: 'material-state', key: 'master-v2' },
    ]);
    expect('sourcePayload' in projection).toBe(false);
  });

  it('rejects duplicate and unbounded direct projection references', () => {
    expect(() =>
      createWorldFocusSituationProjection({
        worldId: 'music',
        orderedSituationReferences: [
          ref('observation', 'same'),
          ref('observation', 'same'),
        ],
      }),
    ).toThrow();

    expect(() =>
      createWorldFocusSituationProjection({
        worldId: 'music',
        orderedSituationReferences: Array.from(
          { length: WORLD_FOCUS_SITUATION_FIRST_OPEN_LIMIT + 1 },
          (_, index) => ref('observation', `s-${index}`),
        ),
      }),
    ).toThrow();

    expect(() =>
      createWorldFocusNextProjection({
        worldId: 'music',
        orderedNextReferences: Array.from(
          { length: WORLD_FOCUS_NEXT_FIRST_OPEN_LIMIT + 1 },
          (_, index) => ref('schedule', `n-${index}`),
        ),
      }),
    ).toThrow();

    const evidence = createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences: [ref('observation', 'obs')],
        provenanceReferences: [],
        integrityAttestationReferences: [],
      },
      {
        maxEvidenceReferences: 2,
        maxProvenanceReferences: 2,
        maxIntegrityAttestationReferences: 2,
      },
    );
    expect(() =>
      createWorldFocusEvidenceHistoryProjection({
        worldId: 'music',
        evidence,
        orderedHistoryReferences: Array.from(
          { length: WORLD_FOCUS_EVIDENCE_HISTORY_FIRST_OPEN_LIMIT + 1 },
          (_, index) => ref('material-state', `h-${index}`),
        ),
      }),
    ).toThrow();
  });
});
