import { describe, expect, it } from 'vitest';

import {
  resolveWorldFocusCompositionPlan,
  type WorldFocusCompositionCandidate,
} from '../model/world-focus-composition-plan';
import { WORLD_FOCUS_GENERAL_3_WAY_VECTORS } from '../model/world-focus-substrate-combinatorial-vectors';
import {
  createWorldFocusOracleReferenceSet,
  decodeWorldFocusGeneralOracleVector,
  resolveWorldFocusSubstrateOracle,
} from '../model/world-focus-substrate-oracle';
import { WORLD_FOCUS_WORK_PRIMITIVE_KINDS } from '../model/world-focus-work-primitives';
import {
  createWorldFocusWorkspaceState,
  reduceWorldFocusWorkspaceState,
} from '../model/world-focus-workspace';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { WorldFocusModuleRegistry } from './world-focus-module-registry';

function createCompositionCandidates(
  stability: 'stable' | 'adaptive',
): readonly WorldFocusCompositionCandidate[] {
  return WORLD_FOCUS_WORK_PRIMITIVE_KINDS.map((kind, index) => ({
    instanceId: `primitive:${kind}`,
    kind,
    ownership: {
      stability,
      origin: stability === 'stable' ? 'user' : 'application-derived',
    },
    prominence: index === 0 ? 'primary' : 'supporting',
    footprint: kind === 'trajectory' ? 'wide' : 'standard',
    order: index,
  }));
}

describe('World Focus WS7 substrate integration harness', () => {
  it('keeps the finite WS6 primitive catalog registered without a generic escape hatch', () => {
    const registry = new WorldFocusModuleRegistry(
      WORLD_FOCUS_WORK_PRIMITIVE_KINDS.map((kind) => ({ kind })),
    );

    expect(registry.kinds).toEqual(WORLD_FOCUS_WORK_PRIMITIVE_KINDS);
    expect(registry.resolve('continuity')).toEqual({ kind: 'continuity' });
    expect(registry.resolve('world-item')).toBeNull();
    expect(registry.resolve('thing')).toBeNull();
  });

  it('runs every fixed 3-way scenario through oracle, planner, cursor and allocation', () => {
    const registry = new WorldFocusModuleRegistry(
      WORLD_FOCUS_WORK_PRIMITIVE_KINDS.map((kind) => ({ kind })),
    );

    for (const vector of WORLD_FOCUS_GENERAL_3_WAY_VECTORS) {
      const scenario = decodeWorldFocusGeneralOracleVector(vector);
      const oracle = resolveWorldFocusSubstrateOracle(scenario);
      const stability =
        scenario.config === 'transient' ? 'adaptive' : ('stable' as const);
      const composition = resolveWorldFocusCompositionPlan(
        createCompositionCandidates(stability),
        {
          maxAdaptiveEntries: 4,
          maxEphemeralEntries: 0,
        },
      );

      expect(composition.entries.length).toBeGreaterThan(0);
      expect(
        composition.entries.every((entry) => registry.has(entry.kind)),
      ).toBe(true);

      let workspace = createWorldFocusWorkspaceState('oracle-world');
      let staleGeneration: number | null = null;

      if (scenario.interaction === 'primary-supporting') {
        const refs = createWorldFocusOracleReferenceSet({
          primary: { kind: 'projection', key: `primary:${vector}` },
          supporting: [
            { kind: 'projection', key: `supporting-a:${vector}` },
            { kind: 'projection', key: `supporting-b:${vector}` },
          ],
          maxSupportingReferences: 2,
        });

        expect(refs.supporting).toHaveLength(2);
        workspace = reduceWorldFocusWorkspaceState(workspace, {
          type: 'select-context',
          reference: refs.primary,
        });
      } else if (scenario.interaction === 'world-switch-late') {
        workspace = reduceWorldFocusWorkspaceState(workspace, {
          type: 'select-context',
          reference: { kind: 'projection', key: `old:${vector}` },
        });
        staleGeneration = workspace.generation;
        workspace = reduceWorldFocusWorkspaceState(workspace, {
          type: 'select-context',
          reference: { kind: 'projection', key: `new:${vector}` },
        });
      }

      if (scenario.dante !== 'unavailable-quiet') {
        const expectedGeneration = staleGeneration ?? workspace.generation;
        const before = workspace;
        const attempted = reduceWorldFocusWorkspaceState(workspace, {
          type: 'open-surface',
          surface: {
            instanceId: `dante:${vector}`,
            kind: 'dante-proof',
            depth: 'insight',
            presentation: 'sidecar',
            origin: 'dante',
            expectedGeneration,
          },
        });

        if (scenario.interaction === 'world-switch-late') {
          expect(attempted).toBe(before);
          expect(oracle.danteDisposition).toBe('reject-late-result');
        } else if (oracle.canAttachDerivedResult) {
          workspace = attempted;
          expect(workspace.surfaces).toHaveLength(1);
        } else {
          workspace = before;
          expect(oracle.danteDisposition).toBe('rebuild-or-reject-context');
        }
      }

      const width =
        scenario.presentation === 'constrained-a11y'
          ? 640
          : scenario.presentation === 'specialist-missing'
            ? 920
            : 1200;
      const allocation = resolveWorldFocusWorkspaceAllocation(workspace, width);

      expect(allocation.workspaceInlineSize).toBe(width);
      expect(allocation.mainInlineSize).toBeGreaterThanOrEqual(0);

      if (
        workspace.surfaces.length > 0 &&
        scenario.presentation === 'constrained-a11y'
      ) {
        expect(allocation.mainAllocation).toBe('full');
        expect(allocation.topLayer).toBe('overlay');
      }

      if (scenario.presentation === 'specialist-missing') {
        expect(registry.resolve('unknown-specialist')).toBeNull();
        expect(oracle.presentationDisposition).toBe(
          'safe-fallback-or-local-failure',
        );
      }
    }
  });

  it('preserves stable relative ordering when configuration is persistent', () => {
    const plan = resolveWorldFocusCompositionPlan(
      createCompositionCandidates('stable'),
      {
        maxAdaptiveEntries: 0,
        maxEphemeralEntries: 0,
      },
    );

    expect(plan.entries.map(({ kind }) => kind)).toEqual([
      'continuity',
      'attention',
      'comparison',
      'trajectory',
    ]);
  });
});
