import { describe, expect, it } from 'vitest';

import type { WorldFocusContinuityProjection } from '../model/world-focus-continuity';
import {
  createWorldFocusCompositionConfig,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
} from '../model/world-focus-composition-config';
import { resolveWorldFocusCompositionPlan } from '../model/world-focus-composition-plan';
import {
  WORLD_FOCUS_ADAPTIVE_COMPOSITION_POLICY,
} from './world-focus-adaptive-composition';
import {
  applyWorldFocusCompositionDraft,
  beginWorldFocusCompositionCustomization,
  updateWorldFocusCompositionDraft,
} from './world-focus-composition-customization';
import {
  collectWorldFocusCompositionOpportunities,
  createWorldFocusCompositionOpportunity,
  createWorldFocusCompositionOpportunitySet,
} from './world-focus-composition-opportunities';
import { resolveWorldFocusCompositionCandidates } from './world-focus-composition-resolver';

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

function config(
  entries: ReadonlyArray<
    Readonly<{
      instanceId: string;
      kind: string;
      visibility: 'visible' | 'hidden';
      pinned: boolean;
      prominenceOverride: 'lead' | null;
    }>
  >,
  revision = 0,
) {
  return createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision,
    worldId: 'music',
    entries,
  });
}

function opportunity(index: number) {
  return createWorldFocusCompositionOpportunity({
    instanceId: `hostile:${index}`,
    kind: `hostile-kind-${index}`,
    defaultProminence: index % 3 === 0 ? 'primary' : 'supporting',
    footprint: index % 2 === 0 ? 'compact' : 'standard',
  });
}

function createRandom(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(state, 1_664_525) + 1_013_904_223) >>> 0;
    return state / 0x1_0000_0000;
  };
}

function shuffle<T>(values: readonly T[], random: () => number): T[] {
  const result = [...values];
  for (let index = result.length - 1; index > 0; index -= 1) {
    const target = Math.floor(random() * (index + 1));
    const current = result[index];
    const replacement = result[target];
    if (current === undefined || replacement === undefined) {
      throw new Error('Hostile shuffle received an invalid index');
    }
    result[index] = replacement;
    result[target] = current;
  }
  return result;
}

function resolve(
  opportunitySet: ReturnType<typeof createWorldFocusCompositionOpportunitySet>,
  currentConfig: ReturnType<typeof config>,
) {
  const candidateResolution = resolveWorldFocusCompositionCandidates({
    opportunitySet,
    config: currentConfig,
    valueSignals: [],
  });
  const plan = resolveWorldFocusCompositionPlan(
    candidateResolution.candidates,
    WORLD_FOCUS_ADAPTIVE_COMPOSITION_POLICY,
  );
  return { candidateResolution, plan };
}

describe('World Focus M3 final hostile closure', () => {
  it('keeps partial/stale-capable content meaningful while empty and unavailable inputs stay sparse through the full planning path', () => {
    const mixed = collectWorldFocusCompositionOpportunities({
      worldId: 'music',
      situation: { status: 'empty' as const, worldId: 'music' },
      continuity: {
        status: 'partial' as const,
        projection: CONTINUITY_PROJECTION,
        reasonCode: 'hostile-partial',
      },
      attention: {
        status: 'unavailable' as const,
        worldId: 'music',
        reasonCode: 'hostile-unavailable',
        retryable: true,
      },
      next: { status: 'empty' as const, worldId: 'music' },
      comparison: {
        status: 'unavailable' as const,
        worldId: 'music',
        reasonCode: 'hostile-unavailable',
        retryable: false,
      },
      trajectory: { status: 'empty' as const, worldId: 'music' },
      evidenceHistory: { status: 'empty' as const, worldId: 'music' },
    });

    expect(mixed.opportunities.map((item) => item.instanceId)).toEqual([
      'continuity',
    ]);
    expect(resolve(mixed, config([])).plan.entries.map((entry) => entry.instanceId)).toEqual([
      'continuity',
    ]);

    const sparse = collectWorldFocusCompositionOpportunities({
      worldId: 'music',
      situation: { status: 'empty' as const, worldId: 'music' },
      continuity: {
        status: 'unavailable' as const,
        worldId: 'music',
        reasonCode: 'hostile-unavailable',
        retryable: true,
      },
      attention: { status: 'empty' as const, worldId: 'music' },
      next: { status: 'empty' as const, worldId: 'music' },
      comparison: { status: 'empty' as const, worldId: 'music' },
      trajectory: { status: 'empty' as const, worldId: 'music' },
      evidenceHistory: { status: 'empty' as const, worldId: 'music' },
    });

    expect(sparse.opportunities).toEqual([]);
    expect(resolve(sparse, config([])).plan.entries).toEqual([]);
  });

  it('keeps adopt/hide/pin/promote/move inside one guarded transaction and preserves their distinct semantics in the resulting plan', () => {
    const opportunities = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: [opportunity(0), opportunity(1), opportunity(2)],
    });
    const base = config([
      {
        instanceId: 'hostile:0',
        kind: 'hostile-kind-0',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
      {
        instanceId: 'hostile:1',
        kind: 'hostile-kind-1',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
    ], 7);
    const adopted = createWorldFocusCompositionOpportunity({
      ...opportunity(2),
      canonicalPayload: { mustNotSurvive: true },
      disclosure: 'must-not-survive',
      aiRelevance: 1,
    } as never);

    let draft = beginWorldFocusCompositionCustomization(base);
    draft = updateWorldFocusCompositionDraft(draft, {
      source: 'manual',
      type: 'hide',
      instanceId: 'hostile:0',
    });
    draft = updateWorldFocusCompositionDraft(draft, {
      source: 'manual',
      type: 'promote',
      instanceId: 'hostile:1',
    });
    draft = updateWorldFocusCompositionDraft(draft, {
      source: 'manual',
      type: 'adopt',
      opportunity: adopted,
    });
    draft = updateWorldFocusCompositionDraft(draft, {
      source: 'manual',
      type: 'pin',
      instanceId: 'hostile:2',
    });
    draft = updateWorldFocusCompositionDraft(draft, {
      source: 'manual',
      type: 'move',
      instanceId: 'hostile:2',
      beforeInstanceId: 'hostile:1',
    });

    expect(base.revision).toBe(7);
    expect(base.entries).toHaveLength(2);

    const applied = applyWorldFocusCompositionDraft(base, draft);
    expect(applied.status).toBe('applied');
    if (applied.status !== 'applied') {
      throw new Error('Expected hostile customization draft to apply');
    }

    expect(applied.config.revision).toBe(8);
    expect(JSON.stringify(applied.config)).not.toContain('mustNotSurvive');
    expect(JSON.stringify(applied.config)).not.toContain('aiRelevance');

    const resolved = resolve(opportunities, applied.config);
    expect(resolved.candidateResolution.omitted).toContainEqual({
      instanceId: 'hostile:0',
      kind: 'hostile-kind-0',
      reason: 'hidden-by-user',
    });
    expect(resolved.plan.entries.map((entry) => entry.instanceId)).toEqual([
      'hostile:2',
      'hostile:1',
    ]);
    expect(resolved.plan.entries[0]).toMatchObject({
      ownership: { stability: 'stable', origin: 'user' },
    });
    expect(resolved.plan.entries[1]?.prominence).toBe('lead');
  });

  it('fails closed on stale or same-revision structurally different accepted config instead of merging a hostile draft', () => {
    const base = config([
      {
        instanceId: 'hostile:0',
        kind: 'hostile-kind-0',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
      {
        instanceId: 'hostile:1',
        kind: 'hostile-kind-1',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
    ], 3);
    const draft = updateWorldFocusCompositionDraft(
      beginWorldFocusCompositionCustomization(base),
      { source: 'manual', type: 'pin', instanceId: 'hostile:1' },
    );

    const stale = config(base.entries, 4);
    expect(applyWorldFocusCompositionDraft(stale, draft)).toEqual({
      status: 'revision-conflict',
      baseRevision: 3,
      currentRevision: 4,
    });

    const sameRevisionDifferentSnapshot = config([...base.entries].reverse(), 3);
    expect(() =>
      applyWorldFocusCompositionDraft(sameRevisionDifferentSnapshot, draft),
    ).toThrow(/base snapshot/i);
  });

  it('survives 200 deterministic hostile config/order/budget combinations without losing pinned intent, exposing hidden entries, or becoming nondeterministic', () => {
    const opportunities = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: Array.from({ length: 10 }, (_, index) => opportunity(index)),
    });

    for (let seed = 1; seed <= 200; seed += 1) {
      const random = createRandom(seed);
      const ordered = shuffle(opportunities.opportunities, random);
      const current = config(
        ordered.map((item) => ({
          instanceId: item.instanceId,
          kind: item.kind,
          visibility: random() < 0.25 ? 'hidden' as const : 'visible' as const,
          pinned: random() < 0.35,
          prominenceOverride: random() < 0.2 ? 'lead' as const : null,
        })),
        seed,
      );

      const first = resolve(opportunities, current);
      const repeated = resolve(opportunities, current);
      expect(repeated).toEqual(first);

      const hiddenIds = new Set(
        current.entries
          .filter((entry) => entry.visibility === 'hidden')
          .map((entry) => entry.instanceId),
      );
      expect(
        first.plan.entries.some((entry) => hiddenIds.has(entry.instanceId)),
        `seed ${seed}: hidden entry leaked into plan`,
      ).toBe(false);

      const plannedIds = new Set(first.plan.entries.map((entry) => entry.instanceId));
      for (const entry of current.entries) {
        if (entry.visibility === 'visible' && entry.pinned) {
          expect(plannedIds.has(entry.instanceId), `seed ${seed}: pinned intent lost`).toBe(
            true,
          );
        }
      }

      const configuredVisibleOrder = current.entries
        .filter((entry) => entry.visibility === 'visible')
        .map((entry) => entry.instanceId);
      const plannedUserOrder = first.plan.entries
        .filter((entry) => entry.ownership.origin === 'user')
        .map((entry) => entry.instanceId);
      let previousIndex = -1;
      for (const instanceId of plannedUserOrder) {
        const index = configuredVisibleOrder.indexOf(instanceId);
        expect(index, `seed ${seed}: planned user entry must come from config`).toBeGreaterThan(
          previousIndex,
        );
        previousIndex = index;
      }

      expect(
        first.plan.entries.filter(
          (entry) => entry.ownership.stability === 'adaptive',
        ).length,
      ).toBeLessThanOrEqual(WORLD_FOCUS_ADAPTIVE_COMPOSITION_POLICY.maxAdaptiveEntries);
      expect(new Set(first.plan.entries.map((entry) => entry.instanceId)).size).toBe(
        first.plan.entries.length,
      );
    }
  });
});
