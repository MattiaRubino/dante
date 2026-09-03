import { describe, expect, it, vi } from 'vitest';

import {
  createWorldFocusCoverageFacet,
  createWorldFocusFreshnessFacet,
  createWorldFocusMaterialPayloadFacet,
  createWorldFocusValidityFacet,
} from '../model/world-focus-basis';
import {
  resolveWorldFocusCompositionPlan,
  type WorldFocusCompositionCandidate,
} from '../model/world-focus-composition-plan';
import { createWorldFocusDisclosureOutcome } from '../model/world-focus-disclosure';
import {
  createWorldFocusEvidenceHistoryProjection,
  createWorldFocusNextProjection,
  createWorldFocusSituationProjection,
} from '../model/world-focus-direct-projections';
import { createWorldFocusEffectPresentation } from '../model/world-focus-effect';
import { createWorldFocusEvidenceReferenceFacet } from '../model/world-focus-evidence';
import { createWorldFocusReferenceResolution } from '../model/world-focus-reference-resolution';
import { createWorldFocusSyncPresentation } from '../model/world-focus-sync';
import {
  createWorldFocusAttentionPrimitive,
  createWorldFocusComparisonPrimitive,
  createWorldFocusContinuityPrimitive,
  createWorldFocusTrajectoryPrimitive,
} from '../model/world-focus-work-primitives';
import {
  createWorldFocusWorkspaceState,
  getWorldFocusInteractionCursor,
  reduceWorldFocusWorkspaceState,
} from '../model/world-focus-workspace';
import {
  createWorldFocusScopedReader,
  type WorldFocusScopedReadAdapter,
} from './world-focus-foundation';

describe('World Focus post-M1 safety falsification', () => {
  it('keeps 729 high-risk reference/basis/coverage/disclosure/sync/effect combinations orthogonal', () => {
    const referenceStatuses = ['usable', 'unresolved', 'retired'] as const;
    const basisCases = [
      {
        freshness: createWorldFocusFreshnessFacet({
          status: 'current',
          asOf: '2026-09-03T08:00:00Z',
        }),
        validity: createWorldFocusValidityFacet({ status: 'current' }),
        expectedFreshness: 'current',
        expectedValidity: 'current',
      },
      {
        freshness: createWorldFocusFreshnessFacet({
          status: 'stale',
          asOf: '2026-09-01T08:00:00Z',
        }),
        validity: createWorldFocusValidityFacet({ status: 'current' }),
        expectedFreshness: 'stale',
        expectedValidity: 'current',
      },
      {
        freshness: createWorldFocusFreshnessFacet({
          status: 'current',
          asOf: '2026-09-03T08:00:00Z',
        }),
        validity: createWorldFocusValidityFacet({
          status: 'retracted',
          reasonCode: 'authoritative-retraction',
        }),
        expectedFreshness: 'current',
        expectedValidity: 'retracted',
      },
    ] as const;
    const coverageCases = [
      createWorldFocusCoverageFacet({ status: 'complete' }),
      createWorldFocusCoverageFacet({
        status: 'incomplete',
        reasonCode: 'source-gap',
      }),
      createWorldFocusCoverageFacet({
        status: 'conflicted',
        reasonCode: 'sources-disagree',
      }),
    ] as const;
    const disclosureStatuses = ['available', 'restricted', 'unavailable'] as const;
    const syncCases = [
      createWorldFocusSyncPresentation({
        connectivity: 'online',
        replay: 'idle',
        providerDelivery: 'nominal',
        requestTiming: 'within-window',
      }),
      createWorldFocusSyncPresentation({
        connectivity: 'offline',
        replay: 'pending',
        providerDelivery: 'unknown',
        requestTiming: 'unknown',
      }),
      createWorldFocusSyncPresentation({
        connectivity: 'online',
        replay: 'idle',
        providerDelivery: 'lagging',
        requestTiming: 'timed-out',
      }),
    ] as const;
    const effectCases = [
      createWorldFocusEffectPresentation({
        state: 'pending',
        executionRevalidation: 'not-required',
      }),
      createWorldFocusEffectPresentation({
        state: 'ambiguous',
        executionRevalidation: 'required-before-execution',
      }),
      createWorldFocusEffectPresentation({
        state: 'partial-real',
        executionRevalidation: 'required-before-execution',
      }),
    ] as const;

    let combinations = 0;

    for (const referenceStatus of referenceStatuses) {
      const resolution =
        referenceStatus === 'usable'
          ? createWorldFocusReferenceResolution({
              status: 'usable',
              reference: { kind: 'material-state', key: 'state:42' },
            })
          : createWorldFocusReferenceResolution({
              status: referenceStatus,
              reference: { kind: 'material-state', key: 'state:42' },
              reasonCode:
                referenceStatus === 'retired'
                  ? 'retired-or-redacted'
                  : 'authoritative-resolution-required',
            });

      for (const basis of basisCases) {
        for (const coverage of coverageCases) {
          for (const disclosureStatus of disclosureStatuses) {
            const disclosure = createWorldFocusDisclosureOutcome({
              status: disclosureStatus,
              authorization: 'must-not-cross-presentation-boundary',
            });

            for (const sync of syncCases) {
              for (const effect of effectCases) {
                expect(resolution.status).toBe(referenceStatus);
                expect(basis.freshness.status).toBe(basis.expectedFreshness);
                expect(basis.validity.status).toBe(basis.expectedValidity);
                expect(coverage.status).not.toBeUndefined();
                expect(disclosure.status).toBe(disclosureStatus);
                expect('authorization' in disclosure).toBe(false);
                expect(sync.connectivity).not.toBeUndefined();
                expect(sync.requestTiming).not.toBeUndefined();
                expect(effect.state).not.toBeUndefined();
                expect(effect.executionRevalidation).not.toBeUndefined();
                combinations += 1;
              }
            }
          }
        }
      }
    }

    expect(combinations).toBe(729);
  });

  it('keeps retirement as reference/history continuity without restoring protected payload', () => {
    const retiredReference = createWorldFocusReferenceResolution({
      status: 'retired',
      reference: { kind: 'material-state', key: 'state:retired:7' },
      reasonCode: 'redacted',
    });
    const payload = createWorldFocusMaterialPayloadFacet({
      status: 'retired',
      materialStateReference: retiredReference.reference,
      reasonCode: 'redacted',
      retiredAt: '2026-09-02T12:00:00Z',
    });

    expect(retiredReference.reference).toEqual({
      kind: 'material-state',
      key: 'state:retired:7',
    });
    expect(payload.status).toBe('retired');
    expect(payload.materialStateReference).toEqual(retiredReference.reference);
    expect(Object.keys(payload).sort()).toEqual([
      'materialStateReference',
      'reasonCode',
      'retiredAt',
      'status',
    ]);
  });

  it('keeps primary/supporting ownership bounded, no-op stable and primary-only for surface inheritance', () => {
    const initial = createWorldFocusWorkspaceState('future-apiary');
    const selected = reduceWorldFocusWorkspaceState(initial, {
      type: 'set-context',
      references: {
        primary: { kind: 'artifact', key: 'hive:inspection:42' },
        supporting: [
          { kind: 'source', key: 'sensor:temperature:42' },
          { kind: 'source', key: 'note:queen-state:42' },
        ],
      },
    });
    const repeated = reduceWorldFocusWorkspaceState(selected, {
      type: 'set-context',
      references: {
        primary: { kind: 'artifact', key: 'hive:inspection:42' },
        supporting: [
          { kind: 'source', key: 'sensor:temperature:42' },
          { kind: 'source', key: 'note:queen-state:42' },
        ],
      },
    });
    const opened = reduceWorldFocusWorkspaceState(selected, {
      type: 'open-surface',
      surface: {
        instanceId: 'explore:hive:42',
        kind: 'artifact-explore',
        depth: 'explore',
        presentation: 'sidecar',
        origin: 'user',
        expectedWorkspace: {
          worldId: selected.worldId,
          generation: selected.generation,
        },
      },
    });

    expect(selected.generation).toBe(1);
    expect(repeated).toBe(selected);
    expect(opened.surfaces).toHaveLength(1);
    expect(opened.surfaces[0]?.contextReference).toEqual(
      selected.contextReferences?.primary,
    );
    expect(opened.surfaces[0]?.contextReference).not.toEqual(
      selected.contextReferences?.supporting[0],
    );

    const cursor = getWorldFocusInteractionCursor(opened);
    expect(Object.keys(cursor)).toContain('contextReferences');
    expect(cursor.selection).toEqual(cursor.contextReferences?.primary);
    expect(Object.isFrozen(cursor.contextReferences)).toBe(true);
  });

  it('rejects wrong-World and stale-generation surface attachment independently', () => {
    const apiary = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('future-apiary'),
      {
        type: 'select-context',
        reference: { kind: 'hive', key: '42' },
      },
    );
    const orchard = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('future-orchard'),
      {
        type: 'select-context',
        reference: { kind: 'tree', key: '7' },
      },
    );

    expect(apiary.generation).toBe(orchard.generation);

    const wrongWorld = reduceWorldFocusWorkspaceState(orchard, {
      type: 'open-surface',
      surface: {
        instanceId: 'late:apiary',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'application',
        expectedWorkspace: {
          worldId: apiary.worldId,
          generation: apiary.generation,
        },
      },
    });
    expect(wrongWorld).toBe(orchard);

    const advanced = reduceWorldFocusWorkspaceState(apiary, {
      type: 'select-context',
      reference: { kind: 'hive', key: '43' },
    });
    const staleGeneration = reduceWorldFocusWorkspaceState(advanced, {
      type: 'open-surface',
      surface: {
        instanceId: 'late:generation',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'application',
        expectedWorkspace: {
          worldId: apiary.worldId,
          generation: apiary.generation,
        },
      },
    });
    expect(staleGeneration).toBe(advanced);
  });

  it('keeps an unknown future World useful through O2/O5/O8 and WP01-WP04 without DANTE', () => {
    const evidence = createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences: [{ kind: 'observation', key: 'hive:weight:42' }],
        provenanceReferences: [{ kind: 'source', key: 'scale:alpha' }],
        integrityAttestationReferences: [
          { kind: 'attestation', key: 'scale:alpha:calibration' },
        ],
      },
      {
        maxEvidenceReferences: 4,
        maxProvenanceReferences: 4,
        maxIntegrityAttestationReferences: 4,
      },
    );
    const situation = createWorldFocusSituationProjection({
      worldId: 'future-apiary',
      orderedSituationReferences: [
        { kind: 'projection', key: 'hive:42:current-state' },
      ],
    });
    const next = createWorldFocusNextProjection({
      worldId: 'future-apiary',
      orderedNextReferences: [
        { kind: 'schedule', key: 'inspection:next' },
        { kind: 'request', key: 'lab:sample:follow-up' },
      ],
    });
    const history = createWorldFocusEvidenceHistoryProjection({
      worldId: 'future-apiary',
      evidence,
      orderedHistoryReferences: [
        { kind: 'history', key: 'inspection:previous' },
      ],
    });
    const continuity = createWorldFocusContinuityPrimitive({
      instanceId: 'continuity:hive:42',
      threadReference: { kind: 'thread', key: 'hive:42' },
      checkpointReference: { kind: 'checkpoint', key: 'inspection:last' },
      continuationReference: { kind: 'action', key: 'inspection:resume' },
      state: 'active',
    });
    const attention = createWorldFocusAttentionPrimitive({
      instanceId: 'attention:hive:42',
      matterReference: { kind: 'matter', key: 'queen-state:uncertain' },
      reasonCode: 'material-uncertainty',
      resolutionReference: { kind: 'request', key: 'inspect:queen-state' },
      state: 'unresolved',
    });
    const comparison = createWorldFocusComparisonPrimitive(
      {
        instanceId: 'comparison:hive:weight',
        mode: 'change',
        subjectReferences: [
          { kind: 'observation', key: 'weight:previous' },
          { kind: 'observation', key: 'weight:current' },
        ],
        basisReference: { kind: 'basis', key: 'scale:alpha' },
      },
      { maxSubjectReferences: 6 },
    );
    const trajectory = createWorldFocusTrajectoryPrimitive(
      {
        instanceId: 'trajectory:hive:weight',
        subjectReference: { kind: 'subject', key: 'hive:42:weight' },
        axis: 'sequence',
        orderedPointReferences: [
          { kind: 'observation', key: 'weight:1' },
          { kind: 'observation', key: 'weight:3' },
        ],
        missingPositionReferences: [
          { kind: 'missing-position', key: 'weight:2' },
        ],
        orderingBasisReference: { kind: 'basis', key: 'inspection-sequence' },
        aggregationBasisReference: null,
      },
      { maxOrderedPointReferences: 12, maxMissingPositionReferences: 12 },
    );

    expect(situation.worldId).toBe('future-apiary');
    expect(next.worldId).toBe('future-apiary');
    expect(history.worldId).toBe('future-apiary');
    expect(evidence.evidenceReferences).not.toEqual(evidence.provenanceReferences);
    expect(evidence.provenanceReferences).not.toEqual(
      evidence.integrityAttestationReferences,
    );
    expect(continuity.kind).toBe('continuity');
    expect(attention.kind).toBe('attention');
    expect(comparison.kind).toBe('comparison');
    expect(trajectory.kind).toBe('trajectory');
    expect(trajectory.missingPositionReferences).toEqual([
      { kind: 'missing-position', key: 'weight:2' },
    ]);
  });

  it('keeps a 5,000-candidate hostile composition bounded without reordering stable entries', () => {
    const candidates: WorldFocusCompositionCandidate[] = [];

    for (let index = 0; index < 5_000; index += 1) {
      const stability =
        index < 5 ? 'stable' : index % 2 === 0 ? 'adaptive' : 'ephemeral';
      const origin =
        stability === 'stable'
          ? 'user'
          : stability === 'adaptive'
            ? 'application-derived'
            : 'dante-proposed';
      candidates.push({
        instanceId: `candidate:${index}`,
        kind: 'projection',
        ownership: { stability, origin },
        prominence: index % 17 === 0 ? 'lead' : 'supporting',
        footprint: 'compact',
        order: index,
      });
    }

    const plan = resolveWorldFocusCompositionPlan(candidates, {
      maxAdaptiveEntries: 7,
      maxEphemeralEntries: 5,
    });

    expect(plan.entries).toHaveLength(17);
    expect(plan.omitted).toHaveLength(4_983);
    const stableEntries = plan.entries.filter(
      (entry) => entry.ownership.stability === 'stable',
    );
    expect(stableEntries.map((entry) => entry.instanceId)).toEqual([
      'candidate:0',
      'candidate:1',
      'candidate:2',
      'candidate:3',
      'candidate:4',
    ]);
  });

  it('does not accept a late adapter result after upstream cancellation even if the adapter ignores AbortSignal', async () => {
    let resolveLate: ((value: unknown) => void) | null = null;
    const adapter: WorldFocusScopedReadAdapter = () =>
      new Promise((resolve) => {
        resolveLate = resolve;
      });
    const validator = vi.fn(() => ({ ok: true as const, value: 'late-result' }));
    const reader = createWorldFocusScopedReader(adapter, validator);
    const upstream = new AbortController();

    const pending = reader('future-apiary', upstream.signal);
    await Promise.resolve();
    upstream.abort();
    expect(resolveLate).not.toBeNull();
    if (resolveLate === null) {
      throw new Error('late adapter resolver was not installed');
    }
    resolveLate({ worldId: 'future-apiary', value: 'late-result' });

    let resolved = false;
    let rejection: unknown;
    try {
      await pending;
      resolved = true;
    } catch (error) {
      rejection = error;
    }

    expect(resolved).toBe(false);
    expect(rejection).toBeDefined();
    expect(validator).not.toHaveBeenCalled();
  });

  it('does not let a mutable caller alias mutate an already-created O8 evidence projection', () => {
    const mutableEvidence = {
      evidenceReferences: [{ kind: 'observation', key: 'weight:1' }],
      provenanceReferences: [{ kind: 'source', key: 'scale:alpha' }],
      integrityAttestationReferences: [] as Array<{
        kind: string;
        key: string;
      }>,
    };
    const projection = createWorldFocusEvidenceHistoryProjection({
      worldId: 'future-apiary',
      evidence: mutableEvidence,
      orderedHistoryReferences: [],
    });

    mutableEvidence.evidenceReferences.push({
      kind: 'observation',
      key: 'weight:late-mutation',
    });

    expect(projection.evidence.evidenceReferences).toEqual([
      { kind: 'observation', key: 'weight:1' },
    ]);
    expect(Object.isFrozen(projection.evidence)).toBe(true);
    expect(Object.isFrozen(projection.evidence.evidenceReferences)).toBe(true);
  });

  it('rejects malformed empty World scope instead of treating an opaque blank id as a usable World', () => {
    expect(() => createWorldFocusWorkspaceState('   ')).toThrow();
    expect(() =>
      createWorldFocusSituationProjection({
        worldId: '   ',
        orderedSituationReferences: [{ kind: 'projection', key: 'state:1' }],
      }),
    ).toThrow();
  });
});
