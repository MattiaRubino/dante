import { describe, expect, it } from 'vitest';

import type {
  WorldFocusCompositionFootprint,
  WorldFocusCompositionProminence,
} from './world-focus-composition-plan';
import {
  resolveWorldFocusCompositionPlan,
  type WorldFocusCompositionCandidate,
  type WorldFocusCompositionPolicy,
} from './world-focus-composition-plan';
import type { WorldFocusCompositionStability } from './world-focus-platform';

const DEFAULT_POLICY: WorldFocusCompositionPolicy = Object.freeze({
  maxAdaptiveEntries: 4,
  maxEphemeralEntries: 2,
});

function makeCandidate(
  instanceId: string,
  options: Readonly<{
    stability?: WorldFocusCompositionStability;
    prominence?: WorldFocusCompositionProminence;
    footprint?: WorldFocusCompositionFootprint;
    order?: number;
  }> = {},
): WorldFocusCompositionCandidate {
  return Object.freeze({
    instanceId,
    kind: `kind:${instanceId}`,
    ownership: Object.freeze({
      stability: options.stability ?? 'adaptive',
      origin: 'application-derived' as const,
    }),
    prominence: options.prominence ?? 'primary',
    footprint: options.footprint ?? 'standard',
    order: options.order ?? 0,
  });
}

function createRandom(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(state, 1_664_525) + 1_013_904_223) >>> 0;
    return state / 0x1_0000_0000;
  };
}

function pick<T>(random: () => number, values: readonly T[]): T {
  const value = values[Math.floor(random() * values.length)];
  if (value === undefined) {
    throw new Error('Random scenario source must not be empty');
  }
  return value;
}

const STABILITIES = ['stable', 'adaptive', 'ephemeral'] as const;
const PROMINENCES = ['lead', 'primary', 'supporting'] as const;
const FOOTPRINTS = ['wide', 'standard', 'compact'] as const;
const KINDS = [
  'situation',
  'continuity',
  'attention',
  'next',
  'change',
  'trajectory',
  'evidence',
  'artifact',
  'people',
  'specialist-future',
] as const;

describe('World Focus dynamic composition planner', () => {
  it('keeps all stable entries while bounding adaptive and ephemeral composition', () => {
    const candidates = [
      makeCandidate('stable-a', { stability: 'stable', order: 2 }),
      makeCandidate('adaptive-a', { stability: 'adaptive', order: 0 }),
      makeCandidate('stable-b', { stability: 'stable', order: 1 }),
      makeCandidate('adaptive-b', { stability: 'adaptive', order: 1 }),
      makeCandidate('adaptive-c', { stability: 'adaptive', order: 2 }),
      makeCandidate('ephemeral-a', { stability: 'ephemeral', order: 0 }),
      makeCandidate('ephemeral-b', { stability: 'ephemeral', order: 1 }),
    ];

    const plan = resolveWorldFocusCompositionPlan(candidates, {
      maxAdaptiveEntries: 2,
      maxEphemeralEntries: 1,
    });

    expect(plan.entries.map((entry) => entry.instanceId)).toEqual([
      'stable-b',
      'stable-a',
      'adaptive-a',
      'adaptive-b',
      'ephemeral-a',
    ]);
    expect(plan.omitted).toEqual([
      { instanceId: 'adaptive-c', reason: 'adaptive-budget' },
      { instanceId: 'ephemeral-b', reason: 'ephemeral-budget' },
    ]);
  });

  it('allows explicitly leading dynamic content to surface before stable content without reordering stable entries', () => {
    const plan = resolveWorldFocusCompositionPlan(
      [
        makeCandidate('stable-second', { stability: 'stable', order: 2 }),
        makeCandidate('adaptive-lead', {
          stability: 'adaptive',
          prominence: 'lead',
          order: 9,
        }),
        makeCandidate('stable-first', { stability: 'stable', order: 1 }),
      ],
      DEFAULT_POLICY,
    );

    expect(plan.entries.map((entry) => entry.instanceId)).toEqual([
      'adaptive-lead',
      'stable-first',
      'stable-second',
    ]);
    expect(plan.entries[0]).toMatchObject({ gridSpan: 12, row: 0 });
  });

  it('fills ordinary rows using finite footprint spans instead of free coordinates', () => {
    const standardOnly = resolveWorldFocusCompositionPlan(
      [makeCandidate('standard')],
      DEFAULT_POLICY,
    );
    expect(standardOnly.entries[0]).toMatchObject({ gridSpan: 12, row: 0 });

    const twoCompact = resolveWorldFocusCompositionPlan(
      [
        makeCandidate('compact-a', { footprint: 'compact', order: 0 }),
        makeCandidate('compact-b', { footprint: 'compact', order: 1 }),
      ],
      DEFAULT_POLICY,
    );
    expect(twoCompact.entries.map((entry) => entry.gridSpan)).toEqual([6, 6]);

    const mixed = resolveWorldFocusCompositionPlan(
      [
        makeCandidate('standard-a', { footprint: 'standard', order: 0 }),
        makeCandidate('compact-a', { footprint: 'compact', order: 1 }),
      ],
      DEFAULT_POLICY,
    );
    expect(mixed.entries.map((entry) => entry.gridSpan)).toEqual([6, 6]);

    const threeCompact = resolveWorldFocusCompositionPlan(
      [
        makeCandidate('compact-a', { footprint: 'compact', order: 0 }),
        makeCandidate('compact-b', { footprint: 'compact', order: 1 }),
        makeCandidate('compact-c', { footprint: 'compact', order: 2 }),
      ],
      DEFAULT_POLICY,
    );
    expect(threeCompact.entries.map((entry) => entry.gridSpan)).toEqual([4, 4, 4]);
  });

  it('uses the same composition grammar across realistic contrasting Worlds', () => {
    const scenarios: ReadonlyArray<
      Readonly<{
        name: string;
        candidates: readonly WorldFocusCompositionCandidate[];
      }>
    > = [
      {
        name: 'music-dense',
        candidates: [
          makeCandidate('release-pipeline', {
            stability: 'stable',
            footprint: 'wide',
            order: 0,
          }),
          makeCandidate('active-tracks', {
            stability: 'stable',
            footprint: 'standard',
            order: 1,
          }),
          makeCandidate('attention-release-risk', {
            prominence: 'lead',
            footprint: 'wide',
            order: 0,
          }),
          makeCandidate('next-milestone', {
            footprint: 'compact',
            order: 1,
          }),
          makeCandidate('meaningful-change', {
            footprint: 'compact',
            order: 2,
          }),
          makeCandidate('recent-artifact', {
            stability: 'ephemeral',
            footprint: 'standard',
            order: 0,
          }),
        ],
      },
      {
        name: 'travel-specialist',
        candidates: [
          makeCandidate('itinerary', {
            stability: 'stable',
            footprint: 'wide',
            order: 0,
          }),
          makeCandidate('next-segment', {
            footprint: 'standard',
            order: 0,
          }),
          makeCandidate('booking-evidence', {
            footprint: 'standard',
            order: 1,
          }),
        ],
      },
      {
        name: 'finance-sparse',
        candidates: [
          makeCandidate('situation', {
            footprint: 'standard',
            order: 0,
          }),
        ],
      },
      {
        name: 'relationships-qualitative',
        candidates: [
          makeCandidate('shared-context', {
            stability: 'stable',
            footprint: 'wide',
            order: 0,
          }),
          makeCandidate('evidence-history', {
            footprint: 'standard',
            order: 0,
          }),
        ],
      },
      {
        name: 'unknown-future-empty',
        candidates: [],
      },
      {
        name: 'unknown-future-specialist',
        candidates: [
          makeCandidate('specialist-future', {
            stability: 'stable',
            footprint: 'wide',
            order: 0,
          }),
          makeCandidate('supporting-future', {
            footprint: 'compact',
            order: 0,
          }),
        ],
      },
    ];

    for (const scenario of scenarios) {
      const plan = resolveWorldFocusCompositionPlan(
        scenario.candidates,
        DEFAULT_POLICY,
      );

      expect(
        plan.entries.every((entry) => [4, 6, 12].includes(entry.gridSpan)),
        scenario.name,
      ).toBe(true);
      expect(
        plan.entries.filter((entry) => entry.ownership.stability === 'stable')
          .length,
        scenario.name,
      ).toBe(
        scenario.candidates.filter(
          (candidate) => candidate.ownership.stability === 'stable',
        ).length,
      );

      const rowTotals = new Map<number, number>();
      for (const entry of plan.entries) {
        rowTotals.set(entry.row, (rowTotals.get(entry.row) ?? 0) + entry.gridSpan);
      }
      expect(
        [...rowTotals.values()].every((total) => total <= 12),
        scenario.name,
      ).toBe(true);
    }
  });

  it('rejects invalid policy and duplicate instances before a broken layout can be rendered', () => {
    expect(() =>
      resolveWorldFocusCompositionPlan([], {
        maxAdaptiveEntries: -1,
        maxEphemeralEntries: 2,
      }),
    ).toThrowError('World Focus max adaptive entries must be a non-negative integer');

    expect(() =>
      resolveWorldFocusCompositionPlan(
        [makeCandidate('duplicate'), makeCandidate('duplicate')],
        DEFAULT_POLICY,
      ),
    ).toThrowError('Duplicate World Focus composition instance: duplicate');
  });

  it('survives 500 deterministic random-user/world compositions from empty to 20 candidate answers', () => {
    for (let seed = 1; seed <= 500; seed += 1) {
      const random = createRandom(seed);
      const candidateCount = Math.floor(random() * 21);
      const candidates: WorldFocusCompositionCandidate[] = [];

      for (let index = 0; index < candidateCount; index += 1) {
        candidates.push(
          Object.freeze({
            instanceId: `seed:${seed}:entry:${index}`,
            kind: pick(random, KINDS),
            ownership: Object.freeze({
              stability: pick(random, STABILITIES),
              origin: pick(random, [
                'system-default',
                'user',
                'dante-proposed',
                'application-derived',
              ] as const),
            }),
            prominence: pick(random, PROMINENCES),
            footprint: pick(random, FOOTPRINTS),
            order: index,
          }),
        );
      }

      const plan = resolveWorldFocusCompositionPlan(candidates, DEFAULT_POLICY);
      const repeated = resolveWorldFocusCompositionPlan(candidates, DEFAULT_POLICY);

      expect(repeated).toEqual(plan);
      expect(plan.entries.length + plan.omitted.length).toBe(candidates.length);
      expect(new Set(plan.entries.map((entry) => entry.instanceId)).size).toBe(
        plan.entries.length,
      );

      const stableIds = candidates
        .filter((candidate) => candidate.ownership.stability === 'stable')
        .map((candidate) => candidate.instanceId);
      const plannedStableIds = plan.entries
        .filter((entry) => entry.ownership.stability === 'stable')
        .map((entry) => entry.instanceId);
      expect(plannedStableIds).toEqual(stableIds);

      expect(
        plan.entries.filter(
          (entry) => entry.ownership.stability === 'adaptive',
        ).length,
      ).toBeLessThanOrEqual(DEFAULT_POLICY.maxAdaptiveEntries);
      expect(
        plan.entries.filter(
          (entry) => entry.ownership.stability === 'ephemeral',
        ).length,
      ).toBeLessThanOrEqual(DEFAULT_POLICY.maxEphemeralEntries);

      const rowTotals = new Map<number, number>();
      for (const entry of plan.entries) {
        expect([4, 6, 12]).toContain(entry.gridSpan);
        if (entry.prominence === 'lead') {
          expect(entry.gridSpan).toBe(12);
        }
        rowTotals.set(entry.row, (rowTotals.get(entry.row) ?? 0) + entry.gridSpan);
      }

      for (const total of rowTotals.values()) {
        expect(total).toBeLessThanOrEqual(12);
      }
      expect(plan.rowCount).toBe(rowTotals.size);
    }
  });
});
