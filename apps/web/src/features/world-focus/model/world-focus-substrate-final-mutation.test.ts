import { describe, expect, it } from 'vitest';

import {
  auditWorldFocusSubstrateOracle,
  resolveWorldFocusSubstrateOracle,
  type WorldFocusOracleOutcome,
  type WorldFocusOracleScenario,
} from './world-focus-substrate-oracle';
import {
  createWorldFocusWorkspaceState,
  reduceWorldFocusWorkspaceState,
} from './world-focus-workspace';

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

function mutateOutcome(
  source: WorldFocusOracleOutcome,
  changes: Partial<WorldFocusOracleOutcome>,
): WorldFocusOracleOutcome {
  return Object.freeze({ ...source, ...changes });
}

describe('World Focus WS8 final falsification — mutation kill and transition sequences', () => {
  it('kills deliberately wrong oracle outcomes instead of only validating its own resolver', () => {
    const cases: readonly Readonly<{
      scenario: WorldFocusOracleScenario;
      mutation: Partial<WorldFocusOracleOutcome>;
      expectedViolation: RegExp;
    }>[] = [
      {
        scenario: scenario({ disclosure: 'revoked' }),
        mutation: { disclosureDisposition: 'allowed' },
        expectedViolation: /disclosure.*reject/i,
      },
      {
        scenario: scenario({ disclosure: 'purpose-recipient-mismatch' }),
        mutation: { canAttachDerivedResult: true },
        expectedViolation: /cannot attach.*disclosure/i,
      },
      {
        scenario: scenario({ disclosure: 'revoked' }),
        mutation: { canReuseSavedDerivedResult: true },
        expectedViolation: /saved|reuse|disclosure/i,
      },
      {
        scenario: scenario({ identity: 'ambiguous-candidate' }),
        mutation: { referenceDisposition: 'usable' },
        expectedViolation: /ambiguous identity/i,
      },
      {
        scenario: scenario({ identity: 'ambiguous-candidate' }),
        mutation: { canReuseSavedDerivedResult: true },
        expectedViolation: /saved|reuse|identity/i,
      },
      {
        scenario: scenario({ config: 'concurrent-shared' }),
        mutation: { configDisposition: 'transient' },
        expectedViolation: /concurrent shared config/i,
      },
      {
        scenario: scenario({ config: 'concurrent-shared' }),
        mutation: { canReuseSavedDerivedResult: true },
        expectedViolation: /saved|reuse|config/i,
      },
      {
        scenario: scenario({ effect: 'partial-real-compensating' }),
        mutation: { effectDisposition: 'blocked' },
        expectedViolation: /partial real effect/i,
      },
      {
        scenario: scenario({ dante: 'proposal-action-late' }),
        mutation: { requiresExecutionRevalidation: false },
        expectedViolation: /proposal.*revalidate/i,
      },
      {
        scenario: scenario({ presentation: 'constrained-a11y' }),
        mutation: { presentationDisposition: 'normal' },
        expectedViolation: /responsive|a11y/i,
      },
    ];

    for (const candidate of cases) {
      const correct = resolveWorldFocusSubstrateOracle(candidate.scenario);
      const mutant = mutateOutcome(correct, candidate.mutation);
      const violations = auditWorldFocusSubstrateOracle(
        candidate.scenario,
        mutant,
      );
      expect(violations.join('; ')).toMatch(candidate.expectedViolation);
    }
  });

  it('rejects wrong-World and stale-generation open, replace and promote sequences atomically', () => {
    let state = createWorldFocusWorkspaceState('music');
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:1',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: { worldId: 'music', generation: 0 },
      },
    });
    expect(state.surfaces).toHaveLength(1);

    const wrongWorldOpen = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:wrong-world',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: { worldId: 'travel', generation: 0 },
      },
    });
    expect(wrongWorldOpen).toBe(state);

    state = reduceWorldFocusWorkspaceState(state, {
      type: 'select-context',
      reference: { kind: 'projection', key: 'next' },
    });
    expect(state.generation).toBe(1);

    const staleReplace = reduceWorldFocusWorkspaceState(state, {
      type: 'replace-surface',
      instanceId: 'insight:1',
      surface: {
        instanceId: 'insight:replacement',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: { worldId: 'music', generation: 0 },
      },
    });
    expect(staleReplace).toBe(state);

    const stalePromote = reduceWorldFocusWorkspaceState(state, {
      type: 'promote-surface',
      instanceId: 'insight:1',
      depth: 'explore',
      presentation: 'full-screen',
      expectedWorkspace: { worldId: 'music', generation: 0 },
    });
    expect(stalePromote).toBe(state);

    const wrongWorldPromote = reduceWorldFocusWorkspaceState(state, {
      type: 'promote-surface',
      instanceId: 'insight:1',
      depth: 'explore',
      presentation: 'full-screen',
      expectedWorkspace: { worldId: 'finance', generation: 1 },
    });
    expect(wrongWorldPromote).toBe(state);
  });

  it('keeps generation tied to meaningful cursor changes rather than surface churn', () => {
    let state = createWorldFocusWorkspaceState('study');
    const initial = state;

    state = reduceWorldFocusWorkspaceState(state, {
      type: 'select-context',
      reference: { kind: 'projection', key: 'chapter-3' },
    });
    expect(state.generation).toBe(1);

    const sameSelection = reduceWorldFocusWorkspaceState(state, {
      type: 'select-context',
      reference: { kind: 'projection', key: 'chapter-3' },
    });
    expect(sameSelection).toBe(state);

    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'detail:1',
        kind: 'detail',
        depth: 'peek',
        presentation: 'popover',
        origin: 'user',
      },
    });
    expect(state.generation).toBe(1);

    state = reduceWorldFocusWorkspaceState(state, { type: 'close-top-surface' });
    expect(state.generation).toBe(1);

    state = reduceWorldFocusWorkspaceState(state, { type: 'clear-context' });
    expect(state.generation).toBe(2);
    expect(state.selection).toBeNull();
    expect(initial.generation).toBe(0);
  });

  it('preserves the blocking-tail invariant under current and stale async pressure', () => {
    let state = createWorldFocusWorkspaceState('finance');
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'confirm:1',
        kind: 'confirm',
        depth: 'explore',
        presentation: 'modal',
        origin: 'user',
      },
    });

    const weakerAboveBlocker = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'sidecar:late',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: { worldId: 'finance', generation: 0 },
      },
    });
    expect(weakerAboveBlocker).toBe(state);

    const nestedBlocker = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'focus:2',
        kind: 'focus',
        depth: 'explore',
        presentation: 'full-screen',
        origin: 'user',
        expectedWorkspace: { worldId: 'finance', generation: 0 },
      },
    });
    expect(nestedBlocker.surfaces.map(({ instanceId }) => instanceId)).toEqual([
      'confirm:1',
      'focus:2',
    ]);

    const staleAfterContextChange = reduceWorldFocusWorkspaceState(
      reduceWorldFocusWorkspaceState(nestedBlocker, {
        type: 'select-context',
        reference: { kind: 'projection', key: 'changed' },
      }),
      {
        type: 'open-surface',
        surface: {
          instanceId: 'modal:stale',
          kind: 'confirm',
          depth: 'explore',
          presentation: 'modal',
          origin: 'dante',
          expectedWorkspace: { worldId: 'finance', generation: 0 },
        },
      },
    );
    expect(staleAfterContextChange.generation).toBe(1);
    expect(staleAfterContextChange.surfaces).toHaveLength(2);
  });

  it('keeps the no-DANTE path semantically usable under hostile substrate pressure', () => {
    const outcome = resolveWorldFocusSubstrateOracle(
      scenario({
        basis: 'conflicted-incomplete',
        identity: 'ambiguous-candidate',
        sync: 'offline-replay',
        presentation: 'specialist-missing',
        dante: 'unavailable-quiet',
      }),
    );

    expect(outcome.danteDisposition).toBe('quiet');
    expect(outcome.basisDisposition).toBe('unresolved');
    expect(outcome.referenceDisposition).toBe('unresolved');
    expect(outcome.presentationDisposition).toBe(
      'safe-fallback-or-local-failure',
    );
  });
});
