import { describe, expect, it } from 'vitest';

import {
  resolveWorldFocusCompositionPlan,
  type WorldFocusCompositionCandidate,
} from './world-focus-composition-plan';
import {
  resolveWorldFocusSubstrateOracle,
  type WorldFocusOracleScenario,
} from './world-focus-substrate-oracle';
import {
  createWorldFocusWorkspaceState,
  reduceWorldFocusWorkspaceState,
} from './world-focus-workspace';
import { resolveWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation';

const BASE_SCENARIO: WorldFocusOracleScenario = Object.freeze({
  basis: 'current',
  disclosure: 'allowed',
  identity: 'stable',
  governance: 'none',
  effect: 'read-only',
  sync: 'online',
  config: 'transient',
  interaction: 'none',
  presentation: 'normal',
  dante: 'unavailable-quiet',
  time: 'simple',
});

function scenario(
  changes: Partial<WorldFocusOracleScenario>,
): WorldFocusOracleScenario {
  return Object.freeze({ ...BASE_SCENARIO, ...changes });
}

describe('World Focus WS8 final falsification — stateful and metamorphic pressure', () => {
  it('rejects an async result from another World even when both workspaces share generation zero', () => {
    const source = createWorldFocusWorkspaceState('music');
    const target = createWorldFocusWorkspaceState('future-apiary');

    expect(source.generation).toBe(0);
    expect(target.generation).toBe(0);

    const result = reduceWorldFocusWorkspaceState(target, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:wrong-world',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: {
          worldId: source.worldId,
          generation: source.generation,
        },
      },
    });

    expect(result).toBe(target);
    expect(result.surfaces).toEqual([]);
  });

  it('supports an unknown future World without page-specific substrate semantics', () => {
    let state = createWorldFocusWorkspaceState('future-apiary-field-coop');
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'select-context',
      reference: { kind: 'projection', key: 'hive:inspection-needed' },
    });

    expect(state.worldId).toBe('future-apiary-field-coop');
    expect(state.generation).toBe(1);
    expect(state.selection).toEqual({
      kind: 'projection',
      key: 'hive:inspection-needed',
    });
  });

  it('does not allow a previously attachable derived result to survive revocation or identity ambiguity', () => {
    const initial = resolveWorldFocusSubstrateOracle(
      scenario({ dante: 'contextual-analysis' }),
    );
    expect(initial.canAttachDerivedResult).toBe(true);

    const revoked = resolveWorldFocusSubstrateOracle(
      scenario({ disclosure: 'revoked', dante: 'contextual-analysis' }),
    );
    expect(revoked.canAttachDerivedResult).toBe(false);
    expect(revoked.danteDisposition).toBe('rebuild-or-reject-context');

    const ambiguous = resolveWorldFocusSubstrateOracle(
      scenario({ identity: 'ambiguous-candidate', dante: 'contextual-analysis' }),
    );
    expect(ambiguous.canAttachDerivedResult).toBe(false);
    expect(ambiguous.referenceDisposition).toBe('unresolved');

    const retired = resolveWorldFocusSubstrateOracle(
      scenario({ identity: 'retired-merge-split', dante: 'contextual-analysis' }),
    );
    expect(retired.canAttachDerivedResult).toBe(false);
    expect(retired.referenceDisposition).toBe('retired');
  });

  it('preserves a real partial-effect obligation after later revocation, retraction and identity retirement', () => {
    const mutations: readonly Partial<WorldFocusOracleScenario>[] = [
      { disclosure: 'revoked' },
      { basis: 'superseded-retracted' },
      { identity: 'retired-merge-split' },
      {
        disclosure: 'purpose-recipient-mismatch',
        basis: 'superseded-retracted',
        identity: 'retired-merge-split',
      },
    ];

    for (const mutation of mutations) {
      const outcome = resolveWorldFocusSubstrateOracle(
        scenario({ effect: 'partial-real-compensating', ...mutation }),
      );

      expect(outcome.effectDisposition).toBe('compensate-or-reconcile');
      if (
        mutation.disclosure !== undefined ||
        mutation.basis === 'superseded-retracted' ||
        mutation.identity !== undefined
      ) {
        expect(outcome.canAttachDerivedResult).toBe(false);
      }
    }
  });

  it('keeps saved output provisional and rejects silent reuse once shared configuration conflicts', () => {
    const saved = resolveWorldFocusSubstrateOracle(
      scenario({ config: 'pinned-saved' }),
    );
    expect(saved.configDisposition).toBe('revalidate-saved');
    expect(saved.canReuseSavedDerivedResult).toBe(true);

    const conflicted = resolveWorldFocusSubstrateOracle(
      scenario({ config: 'concurrent-shared' }),
    );
    expect(conflicted.configDisposition).toBe('conflict');
    expect(conflicted.canReuseSavedDerivedResult).toBe(false);

    const staleSaved = resolveWorldFocusSubstrateOracle(
      scenario({ config: 'pinned-saved', basis: 'superseded-retracted' }),
    );
    expect(staleSaved.canReuseSavedDerivedResult).toBe(false);
  });

  it('keeps consequential DANTE proposals execution-bound across offline replay and time uncertainty', () => {
    for (const mutation of [
      { sync: 'offline-replay' as const },
      { sync: 'provider-lag-timeout' as const },
      { time: 'recurrence-exception-dst' as const },
      { time: 'ordering-effective-unclear' as const },
    ]) {
      const outcome = resolveWorldFocusSubstrateOracle(
        scenario({ dante: 'proposal-action-late', ...mutation }),
      );

      expect(outcome.requiresExecutionRevalidation).toBe(true);
      expect(outcome.danteDisposition).toBe('revalidate-consequential-action');
    }
  });

  it('bounds extreme dynamic composition pressure through existing planner budgets', () => {
    const candidates: readonly WorldFocusCompositionCandidate[] = Array.from(
      { length: 5_000 },
      (_, index) => ({
        instanceId: `adaptive:${index}`,
        kind: index % 2 === 0 ? 'attention' : 'comparison',
        ownership: {
          stability: 'adaptive' as const,
          origin: 'application-derived' as const,
        },
        prominence: index < 2 ? ('primary' as const) : ('supporting' as const),
        footprint: 'compact' as const,
        order: index,
      }),
    );

    const plan = resolveWorldFocusCompositionPlan(candidates, {
      maxAdaptiveEntries: 8,
      maxEphemeralEntries: 0,
    });

    expect(plan.entries).toHaveLength(8);
    expect(plan.omitted).toHaveLength(4_992);
    expect(plan.entries.every((entry) => entry.kind !== 'world-item')).toBe(true);
  });

  it('changes workspace allocation under narrow pressure without changing the underlying surface semantic identity', () => {
    const initial = createWorldFocusWorkspaceState('travel');
    const state = reduceWorldFocusWorkspaceState(initial, {
      type: 'open-surface',
      surface: {
        instanceId: 'explore:comparison',
        kind: 'comparison-explore',
        depth: 'explore',
        presentation: 'sidecar',
        origin: 'user',
      },
    });

    const wide = resolveWorldFocusWorkspaceAllocation(state, 1_200);
    const narrow = resolveWorldFocusWorkspaceAllocation(state, 640);

    expect(wide.mainAllocation).toBe('split');
    expect(wide.activeSidecarInstanceId).toBe('explore:comparison');
    expect(narrow.mainAllocation).toBe('full');
    expect(narrow.topLayer).toBe('overlay');
    expect(state.surfaces[0]?.instanceId).toBe('explore:comparison');
    expect(state.surfaces[0]?.presentation).toBe('sidecar');
  });

  it('treats conflicted evidence, retraction and simple freshness as distinct state transitions', () => {
    const current = resolveWorldFocusSubstrateOracle(scenario({}));
    const conflicted = resolveWorldFocusSubstrateOracle(
      scenario({ basis: 'conflicted-incomplete' }),
    );
    const retracted = resolveWorldFocusSubstrateOracle(
      scenario({ basis: 'superseded-retracted' }),
    );

    expect(current.basisDisposition).toBe('usable');
    expect(conflicted.basisDisposition).toBe('unresolved');
    expect(retracted.basisDisposition).toBe('invalid');
  });
});
