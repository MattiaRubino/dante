import { describe, expect, it } from 'vitest';

import {
  createWorldFocusCoverageFacet,
  createWorldFocusFreshnessFacet,
  createWorldFocusMaterialPayloadFacet,
  createWorldFocusValidityFacet,
} from '../model/world-focus-basis';
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

describe('World Focus M1 final production falsification', () => {
  it('exposes the canonical bounded context set as a normal frozen cursor property', () => {
    const selected = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('future-apiary'),
      {
        type: 'set-context',
        references: {
          primary: { kind: 'artifact', key: 'hive:inspection:42' },
          supporting: [
            { kind: 'source', key: 'sensor:temperature:42' },
            { kind: 'source', key: 'note:queen-state:42' },
          ],
        },
      },
    );
    const opened = reduceWorldFocusWorkspaceState(selected, {
      type: 'open-surface',
      surface: {
        instanceId: 'explore:hive-42',
        kind: 'artifact-explore',
        depth: 'explore',
        presentation: 'sidecar',
        origin: 'user',
      },
    });

    const cursor = getWorldFocusInteractionCursor(opened);
    const descriptor = Object.getOwnPropertyDescriptor(
      cursor,
      'contextReferences',
    );

    expect(Object.keys(cursor)).toContain('contextReferences');
    expect(descriptor?.enumerable).toBe(true);
    expect(cursor.contextReferences).toEqual({
      primary: { kind: 'artifact', key: 'hive:inspection:42' },
      supporting: [
        { kind: 'source', key: 'sensor:temperature:42' },
        { kind: 'source', key: 'note:queen-state:42' },
      ],
    });
    expect(cursor.selection).toEqual(cursor.contextReferences?.primary);
    expect(cursor.activeSurface?.contextReference).toEqual(
      cursor.contextReferences?.primary,
    );
    expect(Object.isFrozen(cursor)).toBe(true);
    expect(Object.isFrozen(cursor.contextReferences)).toBe(true);
  });

  it('keeps reference, basis, disclosure, sync and effect axes independent under hostile composition', () => {
    const retiredReference = createWorldFocusReferenceResolution({
      status: 'retired',
      reference: { kind: 'material-state', key: 'state:legacy:7' },
      reasonCode: 'redacted',
    });
    const freshness = createWorldFocusFreshnessFacet({
      status: 'stale',
      asOf: '2026-09-01T10:00:00Z',
    });
    const validity = createWorldFocusValidityFacet({ status: 'current' });
    const coverage = createWorldFocusCoverageFacet({
      status: 'conflicted',
      reasonCode: 'sources-disagree',
    });
    const material = createWorldFocusMaterialPayloadFacet({
      status: 'retired',
      materialStateReference: retiredReference.reference,
      reasonCode: 'redacted',
      retiredAt: '2026-09-02T12:00:00Z',
    });
    const disclosure = createWorldFocusDisclosureOutcome({
      status: 'restricted',
      authorization: 'must-not-cross-boundary',
    });
    const sync = createWorldFocusSyncPresentation({
      connectivity: 'offline',
      replay: 'pending',
      providerDelivery: 'lagging',
      requestTiming: 'timed-out',
      semanticResult: false,
    });
    const effect = createWorldFocusEffectPresentation({
      state: 'partial-real',
      executionRevalidation: 'required-before-execution',
      providerAck: 'success',
    });

    expect(retiredReference.status).toBe('retired');
    expect(freshness.status).toBe('stale');
    expect(validity.status).toBe('current');
    expect(coverage.status).toBe('conflicted');
    expect(material.status).toBe('retired');
    expect(disclosure).toEqual({ status: 'restricted' });
    expect(sync).toEqual({
      connectivity: 'offline',
      replay: 'pending',
      providerDelivery: 'lagging',
      requestTiming: 'timed-out',
    });
    expect(effect).toEqual({
      state: 'partial-real',
      executionRevalidation: 'required-before-execution',
    });

    expect('authorization' in disclosure).toBe(false);
    expect('semanticResult' in sync).toBe(false);
    expect('providerAck' in effect).toBe(false);
  });

  it('supports an unknown future World through O2/O5/O8 plus finite WP semantics without DANTE', () => {
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
      instanceId: 'continuity:hive-42',
      threadReference: { kind: 'thread', key: 'hive:42' },
      checkpointReference: { kind: 'checkpoint', key: 'inspection:last' },
      continuationReference: { kind: 'action', key: 'inspection:resume' },
      state: 'active',
    });
    const attention = createWorldFocusAttentionPrimitive({
      instanceId: 'attention:hive-42',
      matterReference: { kind: 'matter', key: 'queen-state:uncertain' },
      reasonCode: 'material-uncertainty',
      resolutionReference: { kind: 'request', key: 'inspect:queen-state' },
      state: 'unresolved',
    });
    const comparison = createWorldFocusComparisonPrimitive(
      {
        instanceId: 'comparison:hive-weight',
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
        instanceId: 'trajectory:hive-weight',
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
    expect(evidence.evidenceReferences).not.toEqual(
      evidence.provenanceReferences,
    );
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

  it('rejects a same-generation late surface from the wrong World', () => {
    const source = createWorldFocusWorkspaceState('future-apiary');
    const target = createWorldFocusWorkspaceState('future-orchard');

    expect(source.generation).toBe(target.generation);

    const misrouted = reduceWorldFocusWorkspaceState(target, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:apiary',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'application',
        expectedWorkspace: {
          worldId: source.worldId,
          generation: source.generation,
        },
      },
    });

    expect(misrouted).toBe(target);
    expect(misrouted.surfaces).toEqual([]);
  });
});
