import { describe, expect, it } from 'vitest';

import {
  createWorldFocusEvidenceHistoryProjection,
  createWorldFocusNextProjection,
  createWorldFocusSituationProjection,
} from '../model/world-focus-direct-projections';
import { createWorldFocusEvidenceReferenceFacet } from '../model/world-focus-evidence';
import type { WorldFocusContinuityProjection } from '../model/world-focus-continuity';
import {
  createWorldFocusAttentionPrimitive,
  createWorldFocusComparisonPrimitive,
  createWorldFocusTrajectoryPrimitive,
} from '../model/world-focus-work-primitives';
import {
  collectWorldFocusCompositionOpportunities,
  createWorldFocusCompositionOpportunity,
  createWorldFocusCompositionOpportunitySet,
  WORLD_FOCUS_COMPOSITION_OPPORTUNITY_LIMIT,
} from './world-focus-composition-opportunities';

const ref = (kind: string, key: string) => ({ kind, key });

const CONTINUITY_PROJECTION: WorldFocusContinuityProjection = Object.freeze({
  schemaVersion: 1,
  worldId: 'music',
  orderedItems: Object.freeze([
    Object.freeze({
      key: 'release-thread',
      title: 'Release thread',
      context: 'Single rollout',
      checkpoint: 'Master approved',
      threadReference: ref('release', 'single-1'),
      checkpointReference: ref('material-state', 'master-v3'),
      continuationReference: ref('activity', 'promo-plan'),
      presentationState: 'active' as const,
    }),
  ]),
});

function emptyProjectionSet(worldId = 'music') {
  return {
    worldId,
    situation: { status: 'empty' as const, worldId },
    continuity: {
      status: 'unavailable' as const,
      worldId,
      reasonCode: 'fixture-unavailable',
      retryable: true,
    },
    attention: { status: 'empty' as const, worldId },
    next: { status: 'empty' as const, worldId },
    comparison: { status: 'empty' as const, worldId },
    trajectory: { status: 'empty' as const, worldId },
    evidenceHistory: { status: 'empty' as const, worldId },
  };
}

describe('World Focus M3-2 composition opportunities', () => {
  it('derives only meaningful projection-backed opportunities without retaining source payload or references', () => {
    const attentionA = createWorldFocusAttentionPrimitive({
      instanceId: 'shared',
      matterReference: ref('dependency', 'release-copy'),
      reasonCode: 'blocked-copy',
      resolutionReference: null,
      state: 'blocked',
    });
    const attentionB = createWorldFocusAttentionPrimitive({
      instanceId: 'second',
      matterReference: ref('request', 'cover-review'),
      reasonCode: 'awaiting-review',
      resolutionReference: null,
      state: 'awaiting-response',
    });
    const comparison = createWorldFocusComparisonPrimitive(
      {
        instanceId: 'shared',
        mode: 'difference',
        subjectReferences: [
          ref('material-state', 'master-v2'),
          ref('material-state', 'master-v3'),
        ],
        basisReference: null,
      },
      { maxSubjectReferences: 6 },
    );
    const trajectory = createWorldFocusTrajectoryPrimitive(
      {
        instanceId: 'shared',
        subjectReference: ref('release', 'single-1'),
        axis: 'time',
        orderedPointReferences: [
          ref('observation', 'day-1'),
          ref('observation', 'day-2'),
        ],
        missingPositionReferences: [],
        orderingBasisReference: null,
        aggregationBasisReference: null,
      },
      {
        maxOrderedPointReferences: 12,
        maxMissingPositionReferences: 12,
      },
    );
    const evidence = createWorldFocusEvidenceReferenceFacet(
      {
        evidenceReferences: [ref('observation', 'release-state')],
        provenanceReferences: [],
        integrityAttestationReferences: [],
      },
      {
        maxEvidenceReferences: 8,
        maxProvenanceReferences: 8,
        maxIntegrityAttestationReferences: 8,
      },
    );

    const opportunities = collectWorldFocusCompositionOpportunities({
      worldId: 'music',
      situation: {
        status: 'ready',
        projection: createWorldFocusSituationProjection({
          worldId: 'music',
          orderedSituationReferences: [ref('observation', 'release-state')],
        }),
      },
      continuity: {
        status: 'partial',
        projection: CONTINUITY_PROJECTION,
        reasonCode: 'partial-fixture',
      },
      attention: {
        status: 'ready',
        projection: Object.freeze({
          schemaVersion: 1 as const,
          worldId: 'music',
          orderedItems: Object.freeze([attentionA, attentionB]),
        }),
      },
      next: {
        status: 'ready',
        projection: createWorldFocusNextProjection({
          worldId: 'music',
          orderedNextReferences: [ref('schedule', 'release-date')],
        }),
      },
      comparison: {
        status: 'ready',
        projection: Object.freeze({
          schemaVersion: 1 as const,
          worldId: 'music',
          orderedItems: Object.freeze([comparison]),
        }),
      },
      trajectory: {
        status: 'ready',
        projection: Object.freeze({
          schemaVersion: 1 as const,
          worldId: 'music',
          orderedItems: Object.freeze([trajectory]),
        }),
      },
      evidenceHistory: {
        status: 'ready',
        projection: createWorldFocusEvidenceHistoryProjection({
          worldId: 'music',
          evidence,
          orderedHistoryReferences: [ref('activity', 'master-approved')],
        }),
      },
    });

    expect(opportunities.worldId).toBe('music');
    expect(opportunities.opportunities.map((item) => item.instanceId)).toEqual([
      'situation',
      'continuity',
      'attention:shared',
      'attention:second',
      'next',
      'comparison:shared',
      'trajectory:shared',
      'evidence-history',
    ]);
    expect(opportunities.opportunities.map((item) => item.kind)).toEqual([
      'situation',
      'continuity',
      'attention',
      'attention',
      'next',
      'comparison',
      'trajectory',
      'evidence-history',
    ]);
    expect(opportunities.opportunities).not.toEqual(
      expect.arrayContaining([
        expect.objectContaining({ projection: expect.anything() }),
      ]),
    );
    expect(JSON.stringify(opportunities)).not.toContain('release-copy');
    expect(JSON.stringify(opportunities)).not.toContain('blocked-copy');
    expect(JSON.stringify(opportunities)).not.toContain('release-state');
  });

  it('keeps sparse or unavailable projections sparse while preserving stale Continuity with real content', () => {
    expect(
      collectWorldFocusCompositionOpportunities(emptyProjectionSet('apiary')),
    ).toEqual({ worldId: 'apiary', opportunities: [] });

    const stale = collectWorldFocusCompositionOpportunities({
      ...emptyProjectionSet('music'),
      continuity: {
        status: 'stale' as const,
        projection: CONTINUITY_PROJECTION,
        asOf: '2026-09-03T20:00:00Z',
      },
    });

    expect(stale.opportunities).toEqual([
      {
        instanceId: 'continuity',
        kind: 'continuity',
        defaultProminence: 'primary',
        footprint: 'standard',
      },
    ]);
  });

  it('fails closed when a supposedly validated result belongs to another World', () => {
    expect(() =>
      collectWorldFocusCompositionOpportunities({
        ...emptyProjectionSet('music'),
        situation: {
          status: 'ready' as const,
          projection: createWorldFocusSituationProjection({
            worldId: 'travel',
            orderedSituationReferences: [ref('observation', 'trip-state')],
          }),
        },
      }),
    ).toThrow(/World/i);
  });

  it('keeps unknown future module kinds representable while stripping arbitrary payload and bounding the opportunity set', () => {
    const future = createWorldFocusCompositionOpportunity({
      instanceId: 'future-specialist',
      kind: 'future-specialist',
      defaultProminence: 'supporting',
      footprint: 'wide',
      canonicalPayload: { mustNotSurvive: true },
      aiRelevance: 0.99,
    } as never);

    expect(future).toEqual({
      instanceId: 'future-specialist',
      kind: 'future-specialist',
      defaultProminence: 'supporting',
      footprint: 'wide',
    });
    expect(future).not.toHaveProperty('canonicalPayload');
    expect(future).not.toHaveProperty('aiRelevance');

    const futureSet = createWorldFocusCompositionOpportunitySet({
      worldId: 'future-world-2040',
      opportunities: [future],
    });
    expect(futureSet.worldId).toBe('future-world-2040');
    expect(Object.isFrozen(futureSet)).toBe(true);
    expect(Object.isFrozen(futureSet.opportunities)).toBe(true);

    expect(() =>
      createWorldFocusCompositionOpportunitySet({
        worldId: 'future-world-2040',
        opportunities: Array.from(
          { length: WORLD_FOCUS_COMPOSITION_OPPORTUNITY_LIMIT + 1 },
          (_, index) =>
            createWorldFocusCompositionOpportunity({
              instanceId: `future:${index}`,
              kind: 'future-specialist',
              defaultProminence: 'supporting',
              footprint: 'standard',
            }),
        ),
      }),
    ).toThrow(/limit/i);
  });
});
