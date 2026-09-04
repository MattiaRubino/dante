import { describe, expect, it } from 'vitest';

import {
  createWorldFocusCompositionConfig,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
} from '../model/world-focus-composition-config';
import {
  createWorldFocusAdaptiveCompositionReader,
  readWorldFocusAdaptiveCompositionSnapshot,
  resolveWorldFocusAdaptiveComposition,
} from './world-focus-adaptive-composition';
import {
  createWorldFocusCompositionOpportunity,
  createWorldFocusCompositionOpportunitySet,
} from './world-focus-composition-opportunities';

function config(
  worldId: string,
  entries: readonly Readonly<{
    instanceId: string;
    kind: string;
    visibility: 'visible' | 'hidden';
    pinned: boolean;
    prominenceOverride: 'lead' | null;
  }>[],
) {
  return createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision: 0,
    worldId,
    entries,
  });
}

function abortError() {
  const error = new Error('aborted');
  error.name = 'AbortError';
  return error;
}

describe('World Focus M3-4 adaptive composition application integration', () => {
  it('reads every owned M1 seam exactly once and keeps a truly sparse World sparse', async () => {
    const calls = new Map<string, number>();
    const emptyReader = (name: string) => async (worldId: string, signal?: AbortSignal) => {
      calls.set(name, (calls.get(name) ?? 0) + 1);
      if (signal?.aborted === true) throw abortError();
      return Object.freeze({ status: 'empty' as const, worldId });
    };
    const reader = createWorldFocusAdaptiveCompositionReader({
      readSituation: emptyReader('situation'),
      readContinuity: emptyReader('continuity'),
      readAttention: emptyReader('attention'),
      readNext: emptyReader('next'),
      readComparison: emptyReader('comparison'),
      readTrajectory: emptyReader('trajectory'),
      readEvidenceHistory: emptyReader('evidence-history'),
    });

    const snapshot = await reader('finance');
    expect(Object.fromEntries(calls)).toEqual({
      situation: 1,
      continuity: 1,
      attention: 1,
      next: 1,
      comparison: 1,
      trajectory: 1,
      'evidence-history': 1,
    });
    expect(snapshot.opportunitySet.opportunities).toHaveLength(0);
    expect(
      resolveWorldFocusAdaptiveComposition(snapshot, config('finance', [])).plan.entries,
    ).toHaveLength(0);
  });

  it('propagates cancellation to all seven M1 reads instead of converting abort into empty meaning', async () => {
    let aborted = 0;
    const blockedReader = (worldId: string, signal?: AbortSignal) =>
      new Promise<Readonly<{ status: 'empty'; worldId: string }>>((resolve, reject) => {
        if (signal === undefined) {
          reject(new Error('missing signal'));
          return;
        }
        if (signal.aborted) {
          aborted += 1;
          reject(abortError());
          return;
        }
        signal.addEventListener(
          'abort',
          () => {
            aborted += 1;
            reject(abortError());
          },
          { once: true },
        );
        void resolve;
      });
    const reader = createWorldFocusAdaptiveCompositionReader({
      readSituation: blockedReader,
      readContinuity: blockedReader,
      readAttention: blockedReader,
      readNext: blockedReader,
      readComparison: blockedReader,
      readTrajectory: blockedReader,
      readEvidenceHistory: blockedReader,
    });
    const controller = new AbortController();
    const pending = reader('music', controller.signal);

    controller.abort();

    await expect(pending).rejects.toMatchObject({ name: 'AbortError' });
    expect(aborted).toBe(7);
  });

  it('keeps hidden content hidden, pinned meaningful content outside adaptive budget, and unresolved pins non-fabricated', async () => {
    const snapshot = await readWorldFocusAdaptiveCompositionSnapshot('music');
    const hidden = resolveWorldFocusAdaptiveComposition(
      snapshot,
      config('music', [
        {
          instanceId: 'situation',
          kind: 'situation',
          visibility: 'hidden',
          pinned: false,
          prominenceOverride: null,
        },
      ]),
    );
    expect(hidden.plan.entries.some((entry) => entry.instanceId === 'situation')).toBe(
      false,
    );
    expect(hidden.candidateResolution.omitted).toContainEqual({
      instanceId: 'situation',
      kind: 'situation',
      reason: 'hidden-by-user',
    });

    const allPinned = resolveWorldFocusAdaptiveComposition(
      snapshot,
      config(
        'music',
        snapshot.opportunitySet.opportunities.map((opportunity) => ({
          instanceId: opportunity.instanceId,
          kind: opportunity.kind,
          visibility: 'visible' as const,
          pinned: true,
          prominenceOverride: null,
        })),
      ),
    );
    expect(allPinned.plan.entries).toHaveLength(
      snapshot.opportunitySet.opportunities.length,
    );

    const unresolved = resolveWorldFocusAdaptiveComposition(
      snapshot,
      config('music', [
        {
          instanceId: 'future:missing',
          kind: 'future-module',
          visibility: 'visible',
          pinned: true,
          prominenceOverride: null,
        },
      ]),
    );
    expect(
      unresolved.plan.entries.some((entry) => entry.instanceId === 'future:missing'),
    ).toBe(false);
    expect(unresolved.candidateResolution.unresolvedPinned).toEqual([
      {
        instanceId: 'future:missing',
        kind: 'future-module',
        reason: 'meaningful-projection-unavailable',
      },
    ]);
  });

  it('preserves configured relative order ahead of adaptive prominence ranking', async () => {
    const source = await readWorldFocusAdaptiveCompositionSnapshot('music');
    const opportunitySet = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: [
        createWorldFocusCompositionOpportunity({
          instanceId: 'comparison:music-master-change',
          kind: 'comparison',
          defaultProminence: 'supporting',
          footprint: 'standard',
        }),
        createWorldFocusCompositionOpportunity({
          instanceId: 'situation',
          kind: 'situation',
          defaultProminence: 'primary',
          footprint: 'standard',
        }),
      ],
    });
    const snapshot = Object.freeze({ ...source, opportunitySet });
    const resolved = resolveWorldFocusAdaptiveComposition(
      snapshot,
      config('music', [
        {
          instanceId: 'comparison:music-master-change',
          kind: 'comparison',
          visibility: 'visible',
          pinned: false,
          prominenceOverride: null,
        },
        {
          instanceId: 'situation',
          kind: 'situation',
          visibility: 'visible',
          pinned: false,
          prominenceOverride: null,
        },
      ]),
    );

    expect(resolved.plan.entries.map((entry) => entry.instanceId)).toEqual([
      'comparison:music-master-change',
      'situation',
    ]);
    expect(resolved.plan.entries[0]?.prominence).toBe('supporting');
  });
});
