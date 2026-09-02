import { createHash } from 'node:crypto';

import { describe, expect, it } from 'vitest';

import {
  countWorldFocusCoveredInteractions,
  serializeWorldFocusVectors,
  WORLD_FOCUS_GENERAL_3_WAY_VECTORS,
  WORLD_FOCUS_GENERAL_EXPECTED_INTERACTIONS,
  WORLD_FOCUS_GENERAL_VECTOR_AXIS_COUNT,
  WORLD_FOCUS_GENERAL_VECTOR_SHA256,
  WORLD_FOCUS_GENERAL_VECTOR_STRENGTH,
  WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS,
  WORLD_FOCUS_HIGH_RISK_EXPECTED_INTERACTIONS,
  WORLD_FOCUS_HIGH_RISK_VECTOR_AXIS_COUNT,
  WORLD_FOCUS_HIGH_RISK_VECTOR_SHA256,
  WORLD_FOCUS_HIGH_RISK_VECTOR_STRENGTH,
} from './world-focus-substrate-combinatorial-vectors';
import {
  auditWorldFocusSubstrateOracle,
  createWorldFocusOracleReferenceSet,
  resolveWorldFocusSubstrateOracle,
  WORLD_FOCUS_ORACLE_BASIS_LEVELS,
  WORLD_FOCUS_ORACLE_CONFIG_LEVELS,
  WORLD_FOCUS_ORACLE_DANTE_LEVELS,
  WORLD_FOCUS_ORACLE_DISCLOSURE_LEVELS,
  WORLD_FOCUS_ORACLE_EFFECT_LEVELS,
  WORLD_FOCUS_ORACLE_GOVERNANCE_LEVELS,
  WORLD_FOCUS_ORACLE_IDENTITY_LEVELS,
  WORLD_FOCUS_ORACLE_INTERACTION_LEVELS,
  WORLD_FOCUS_ORACLE_PRESENTATION_LEVELS,
  WORLD_FOCUS_ORACLE_SYNC_LEVELS,
  WORLD_FOCUS_ORACLE_TIME_LEVELS,
  type WorldFocusOracleScenario,
} from './world-focus-substrate-oracle';

function sha256(value: string): string {
  return createHash('sha256').update(value).digest('hex');
}

function decodeGeneralVector(vector: string): WorldFocusOracleScenario {
  const digit = (index: number) => Number(vector[index]) as 0 | 1 | 2;

  return Object.freeze({
    basis: WORLD_FOCUS_ORACLE_BASIS_LEVELS[digit(0)],
    disclosure: WORLD_FOCUS_ORACLE_DISCLOSURE_LEVELS[digit(1)],
    identity: WORLD_FOCUS_ORACLE_IDENTITY_LEVELS[digit(2)],
    governance: WORLD_FOCUS_ORACLE_GOVERNANCE_LEVELS[digit(3)],
    effect: WORLD_FOCUS_ORACLE_EFFECT_LEVELS[digit(4)],
    sync: WORLD_FOCUS_ORACLE_SYNC_LEVELS[digit(5)],
    config: WORLD_FOCUS_ORACLE_CONFIG_LEVELS[digit(6)],
    interaction: WORLD_FOCUS_ORACLE_INTERACTION_LEVELS[digit(7)],
    presentation: WORLD_FOCUS_ORACLE_PRESENTATION_LEVELS[digit(8)],
    dante: WORLD_FOCUS_ORACLE_DANTE_LEVELS[digit(9)],
    time: WORLD_FOCUS_ORACLE_TIME_LEVELS[digit(10)],
  });
}

function decodeHighRiskVector(vector: string): WorldFocusOracleScenario {
  const digit = (index: number) => Number(vector[index]) as 0 | 1 | 2;

  return Object.freeze({
    basis: WORLD_FOCUS_ORACLE_BASIS_LEVELS[digit(0)],
    disclosure: WORLD_FOCUS_ORACLE_DISCLOSURE_LEVELS[digit(1)],
    identity: WORLD_FOCUS_ORACLE_IDENTITY_LEVELS[digit(2)],
    governance: WORLD_FOCUS_ORACLE_GOVERNANCE_LEVELS[digit(3)],
    effect: WORLD_FOCUS_ORACLE_EFFECT_LEVELS[digit(4)],
    sync: WORLD_FOCUS_ORACLE_SYNC_LEVELS[digit(5)],
    config: 'transient',
    interaction: 'none',
    presentation: 'normal',
    dante: WORLD_FOCUS_ORACLE_DANTE_LEVELS[digit(6)],
    time: 'simple',
  });
}

describe('World Focus WS7 substrate oracle', () => {
  it('preserves the exact fixed analytical vector payloads and hashes', () => {
    expect(WORLD_FOCUS_GENERAL_3_WAY_VECTORS).toHaveLength(67);
    expect(WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS).toHaveLength(157);

    expect(
      sha256(
        serializeWorldFocusVectors(
          WORLD_FOCUS_GENERAL_3_WAY_VECTORS,
          WORLD_FOCUS_GENERAL_VECTOR_AXIS_COUNT,
        ),
      ),
    ).toBe(WORLD_FOCUS_GENERAL_VECTOR_SHA256);

    expect(
      sha256(
        serializeWorldFocusVectors(
          WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS,
          WORLD_FOCUS_HIGH_RISK_VECTOR_AXIS_COUNT,
        ),
      ),
    ).toBe(WORLD_FOCUS_HIGH_RISK_VECTOR_SHA256);
  });

  it('proves complete 3-way and high-risk 4-way tuple coverage', () => {
    expect(
      countWorldFocusCoveredInteractions(
        WORLD_FOCUS_GENERAL_3_WAY_VECTORS,
        WORLD_FOCUS_GENERAL_VECTOR_AXIS_COUNT,
        WORLD_FOCUS_GENERAL_VECTOR_STRENGTH,
      ),
    ).toBe(WORLD_FOCUS_GENERAL_EXPECTED_INTERACTIONS);

    expect(
      countWorldFocusCoveredInteractions(
        WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS,
        WORLD_FOCUS_HIGH_RISK_VECTOR_AXIS_COUNT,
        WORLD_FOCUS_HIGH_RISK_VECTOR_STRENGTH,
      ),
    ).toBe(WORLD_FOCUS_HIGH_RISK_EXPECTED_INTERACTIONS);
  });

  it('keeps every fixed 3-way vector owned by the hardened oracle', () => {
    for (const vector of WORLD_FOCUS_GENERAL_3_WAY_VECTORS) {
      const scenario = decodeGeneralVector(vector);
      const outcome = resolveWorldFocusSubstrateOracle(scenario);
      expect(auditWorldFocusSubstrateOracle(scenario, outcome)).toEqual([]);
    }
  });

  it('keeps every fixed high-risk 4-way vector owned by the hardened oracle', () => {
    for (const vector of WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS) {
      const scenario = decodeHighRiskVector(vector);
      const outcome = resolveWorldFocusSubstrateOracle(scenario);
      expect(auditWorldFocusSubstrateOracle(scenario, outcome)).toEqual([]);
    }
  });

  it('blocks disclosure invalidation and retired identities from derived attachment', () => {
    const revoked = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      disclosure: 'revoked',
    });
    expect(revoked.disclosureDisposition).toBe('reject');
    expect(revoked.canAttachDerivedResult).toBe(false);

    const retired = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      identity: 'retired-merge-split',
    });
    expect(retired.referenceDisposition).toBe('retired');
    expect(retired.canAttachDerivedResult).toBe(false);
  });

  it('keeps ambiguous identity unresolved and forbids derived attachment until authoritative resolution', () => {
    const outcome = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      identity: 'ambiguous-candidate',
      dante: 'contextual-analysis',
    });

    expect(outcome.referenceDisposition).toBe('unresolved');
    expect(outcome.canAttachDerivedResult).toBe(false);
    expect(outcome.danteDisposition).toBe('rebuild-or-reject-context');
  });

  it('keeps conflicted basis unresolved rather than treating missing certainty as false', () => {
    const outcome = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      basis: 'conflicted-incomplete',
    });

    expect(outcome.basisDisposition).toBe('unresolved');
  });

  it('requires consequential revalidation after offline replay or material governance pressure', () => {
    const offline = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      effect: 'pending-ambiguous',
      sync: 'offline-replay',
    });
    expect(offline.requiresExecutionRevalidation).toBe(true);
    expect(offline.effectDisposition).toBe('revalidate-before-execution');

    const revisionBound = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      effect: 'pending-ambiguous',
      governance: 'revision-bound-binding',
    });
    expect(revisionBound.requiresExecutionRevalidation).toBe(true);
  });

  it('keeps a DANTE consequential proposal execution-bound even before any effect exists', () => {
    const outcome = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      effect: 'read-only',
      dante: 'proposal-action-late',
    });

    expect(outcome.effectDisposition).toBe('not-applicable');
    expect(outcome.requiresExecutionRevalidation).toBe(true);
    expect(outcome.danteDisposition).toBe('revalidate-consequential-action');
  });

  it('distinguishes partial real effects from cancellation-before-effect', () => {
    const outcome = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      effect: 'partial-real-compensating',
    });

    expect(outcome.effectDisposition).toBe('compensate-or-reconcile');
  });

  it('rejects late DANTE attachment after a World/cursor switch', () => {
    const outcome = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      interaction: 'world-switch-late',
      dante: 'contextual-analysis',
    });

    expect(outcome.danteDisposition).toBe('reject-late-result');
    expect(outcome.canAttachDerivedResult).toBe(false);
  });

  it('does not let pinned/saved output bypass basis, disclosure or identity validity', () => {
    const outcome = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      config: 'pinned-saved',
      basis: 'superseded-retracted',
    });

    expect(outcome.configDisposition).toBe('revalidate-saved');
    expect(outcome.canReuseSavedDerivedResult).toBe(false);
  });

  it('keeps responsive/a11y pressure semantically invariant', () => {
    const outcome = resolveWorldFocusSubstrateOracle({
      ...decodeGeneralVector('00000000000'),
      presentation: 'constrained-a11y',
    });

    expect(outcome.presentationDisposition).toBe('semantic-invariant');
  });

  it('builds explicit bounded primary + ordered supporting context refs', () => {
    const refs = createWorldFocusOracleReferenceSet({
      primary: { kind: 'projection', key: 'current' },
      supporting: [
        { kind: 'checkpoint', key: 'previous-1' },
        { kind: 'checkpoint', key: 'previous-2' },
      ],
      maxSupportingReferences: 2,
    });

    expect(refs).toEqual({
      primary: { kind: 'projection', key: 'current' },
      supporting: [
        { kind: 'checkpoint', key: 'previous-1' },
        { kind: 'checkpoint', key: 'previous-2' },
      ],
    });

    expect(() =>
      createWorldFocusOracleReferenceSet({
        primary: { kind: 'projection', key: 'current' },
        supporting: [
          { kind: 'checkpoint', key: 'previous-1' },
          { kind: 'checkpoint', key: 'previous-2' },
        ],
        maxSupportingReferences: 1,
      }),
    ).toThrow(/exceed policy/);

    expect(() =>
      createWorldFocusOracleReferenceSet({
        primary: { kind: 'projection', key: 'current' },
        supporting: [{ kind: 'projection', key: 'current' }],
        maxSupportingReferences: 2,
      }),
    ).toThrow(/must not contain duplicates/);
  });
});
