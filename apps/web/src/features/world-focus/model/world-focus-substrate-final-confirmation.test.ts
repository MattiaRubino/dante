import { describe, expect, it } from 'vitest';

import {
  WORLD_FOCUS_GENERAL_3_WAY_VECTORS,
  WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS,
} from './world-focus-substrate-combinatorial-vectors';
import {
  auditWorldFocusSubstrateOracle,
  decodeWorldFocusGeneralOracleVector,
  decodeWorldFocusHighRiskOracleVector,
  resolveWorldFocusSubstrateOracle,
  type WorldFocusOracleOutcome,
  type WorldFocusOracleScenario,
} from './world-focus-substrate-oracle';
import {
  createWorldFocusWorkspaceState,
  reduceWorldFocusWorkspaceState,
} from './world-focus-workspace';

const semanticTruth = (outcome: WorldFocusOracleOutcome) => ({
  basisDisposition: outcome.basisDisposition,
  disclosureDisposition: outcome.disclosureDisposition,
  referenceDisposition: outcome.referenceDisposition,
  configDisposition: outcome.configDisposition,
  canAttachDerivedResult: outcome.canAttachDerivedResult,
  canReuseSavedDerivedResult: outcome.canReuseSavedDerivedResult,
  timeDisposition: outcome.timeDisposition,
});

function withoutDante(
  scenario: WorldFocusOracleScenario,
): WorldFocusOracleScenario {
  return Object.freeze({ ...scenario, dante: 'unavailable-quiet' as const });
}

function constrainedPresentation(
  scenario: WorldFocusOracleScenario,
): WorldFocusOracleScenario {
  return Object.freeze({ ...scenario, presentation: 'constrained-a11y' as const });
}

describe('World Focus WS8 final falsification — post-hardening confirmation', () => {
  it('reconfirms every fixed general vector after the final CG-40 audit hardening', () => {
    for (const vector of WORLD_FOCUS_GENERAL_3_WAY_VECTORS) {
      const scenario = decodeWorldFocusGeneralOracleVector(vector);
      const outcome = resolveWorldFocusSubstrateOracle(scenario);

      expect(auditWorldFocusSubstrateOracle(scenario, outcome)).toEqual([]);

      if (outcome.canReuseSavedDerivedResult) {
        expect(scenario.basis).toBe('current');
        expect(scenario.disclosure).toBe('allowed');
        expect(scenario.identity).toBe('stable');
        expect(scenario.config).not.toBe('concurrent-shared');
      }
    }
  });

  it('reconfirms every high-risk vector after the final CG-40 audit hardening', () => {
    for (const vector of WORLD_FOCUS_HIGH_RISK_4_WAY_VECTORS) {
      const scenario = decodeWorldFocusHighRiskOracleVector(vector);
      const outcome = resolveWorldFocusSubstrateOracle(scenario);

      expect(auditWorldFocusSubstrateOracle(scenario, outcome)).toEqual([]);

      if (outcome.canReuseSavedDerivedResult) {
        expect(scenario.basis).toBe('current');
        expect(scenario.disclosure).toBe('allowed');
        expect(scenario.identity).toBe('stable');
      }
    }
  });

  it('keeps the no-DANTE path independent from truth, disclosure and reference semantics', () => {
    for (const vector of WORLD_FOCUS_GENERAL_3_WAY_VECTORS) {
      const scenario = decodeWorldFocusGeneralOracleVector(vector);
      const withCurrentDanteState = resolveWorldFocusSubstrateOracle(scenario);
      const quietScenario = withoutDante(scenario);
      const quiet = resolveWorldFocusSubstrateOracle(quietScenario);

      expect(quiet.danteDisposition).toBe('quiet');
      expect(semanticTruth(quiet)).toEqual(semanticTruth(withCurrentDanteState));
      expect(auditWorldFocusSubstrateOracle(quietScenario, quiet)).toEqual([]);
    }
  });

  it('keeps constrained/a11y presentation from rewriting substrate semantics', () => {
    for (const vector of WORLD_FOCUS_GENERAL_3_WAY_VECTORS) {
      const scenario = decodeWorldFocusGeneralOracleVector(vector);
      const baseline = resolveWorldFocusSubstrateOracle(scenario);
      const constrainedScenario = constrainedPresentation(scenario);
      const constrained = resolveWorldFocusSubstrateOracle(constrainedScenario);

      expect(constrained.presentationDisposition).toBe('semantic-invariant');
      expect({
        ...constrained,
        presentationDisposition: baseline.presentationDisposition,
      }).toEqual(baseline);
    }
  });

  it('keeps unknown future Worlds on the same reducer contract and rejects wrong-World attachment', () => {
    const futureWorldIds = [
      'future-apiary-field-coop',
      'future-archive-restoration-lab',
      'future-community-kitchen',
    ] as const;

    for (const worldId of futureWorldIds) {
      let workspace = createWorldFocusWorkspaceState(worldId);
      workspace = reduceWorldFocusWorkspaceState(workspace, {
        type: 'select-context',
        reference: { kind: 'projection', key: 'current-work' },
      });

      const accepted = reduceWorldFocusWorkspaceState(workspace, {
        type: 'open-surface',
        surface: {
          instanceId: `${worldId}:insight`,
          kind: 'future-specialist-proof',
          depth: 'insight',
          presentation: 'sidecar',
          origin: 'application',
          expectedWorkspace: {
            worldId,
            generation: workspace.generation,
          },
        },
      });
      expect(accepted.surfaces).toHaveLength(1);

      const wrongWorld = reduceWorldFocusWorkspaceState(workspace, {
        type: 'open-surface',
        surface: {
          instanceId: `${worldId}:wrong`,
          kind: 'future-specialist-proof',
          depth: 'insight',
          presentation: 'sidecar',
          origin: 'application',
          expectedWorkspace: {
            worldId: `${worldId}:other`,
            generation: workspace.generation,
          },
        },
      });
      expect(wrongWorld).toBe(workspace);
    }
  });

  it('keeps saved-result non-interference invariant under each invalidating axis independently', () => {
    const baseline = decodeWorldFocusGeneralOracleVector('00000010000');
    const invalidations: readonly Partial<WorldFocusOracleScenario>[] = [
      { basis: 'superseded-retracted' },
      { basis: 'conflicted-incomplete' },
      { disclosure: 'revoked' },
      { disclosure: 'purpose-recipient-mismatch' },
      { identity: 'ambiguous-candidate' },
      { identity: 'retired-merge-split' },
      { config: 'concurrent-shared' },
    ];

    const valid = resolveWorldFocusSubstrateOracle(baseline);
    expect(valid.canReuseSavedDerivedResult).toBe(true);

    for (const change of invalidations) {
      const candidate = Object.freeze({ ...baseline, ...change });
      const outcome = resolveWorldFocusSubstrateOracle(candidate);
      expect(outcome.canReuseSavedDerivedResult).toBe(false);
      expect(auditWorldFocusSubstrateOracle(candidate, outcome)).toEqual([]);
    }
  });
});
