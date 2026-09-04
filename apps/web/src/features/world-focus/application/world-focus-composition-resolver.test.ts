import { describe, expect, it } from 'vitest';

import {
  createWorldFocusCompositionConfig,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
} from '../model/world-focus-composition-config';
import { resolveWorldFocusCompositionPlan } from '../model/world-focus-composition-plan';
import {
  createWorldFocusCompositionOpportunity,
  createWorldFocusCompositionOpportunitySet,
} from './world-focus-composition-opportunities';
import {
  createWorldFocusCompositionValueSignalAssignment,
  resolveWorldFocusCompositionCandidates,
} from './world-focus-composition-resolver';

function opportunity(
  instanceId: string,
  kind = instanceId,
  defaultProminence: 'lead' | 'primary' | 'supporting' = 'supporting',
) {
  return createWorldFocusCompositionOpportunity({
    instanceId,
    kind,
    defaultProminence,
    footprint: 'standard',
  });
}

function config(
  entries: ReadonlyArray<
    Readonly<{
      instanceId: string;
      kind: string;
      visibility?: 'visible' | 'hidden';
      pinned?: boolean;
      prominenceOverride?: 'lead' | null;
    }>
  >,
  worldId = 'music',
) {
  return createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision: 4,
    worldId,
    entries: entries.map((entry) => ({
      instanceId: entry.instanceId,
      kind: entry.kind,
      visibility: entry.visibility ?? 'visible',
      pinned: entry.pinned ?? false,
      prominenceOverride: entry.prominenceOverride ?? null,
    })),
  });
}

function signals(
  instanceId: string,
  kind: string,
  values: readonly (
    | 'material-consequence'
    | 'immediacy'
    | 'resumability'
    | 'meaningful-change'
    | 'current-intent'
  )[],
  worldId = 'music',
) {
  return createWorldFocusCompositionValueSignalAssignment({
    worldId,
    instanceId,
    kind,
    signals: values,
  });
}

describe('World Focus M3-2 adaptive candidate resolver', () => {
  it('lets explicit hide win over ranking signals and keeps hide distinct from deletion', () => {
    const opportunitySet = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: [opportunity('attention:blocked', 'attention', 'primary')],
    });

    const resolution = resolveWorldFocusCompositionCandidates({
      opportunitySet,
      config: config([
        {
          instanceId: 'attention:blocked',
          kind: 'attention',
          visibility: 'hidden',
        },
      ]),
      valueSignals: [
        signals('attention:blocked', 'attention', [
          'material-consequence',
          'immediacy',
          'current-intent',
        ]),
      ],
    });

    expect(resolution.candidates).toEqual([]);
    expect(resolution.omitted).toEqual([
      {
        instanceId: 'attention:blocked',
        kind: 'attention',
        reason: 'hidden-by-user',
      },
    ]);
    expect(resolution.unresolvedPinned).toEqual([]);
  });

  it('turns a meaningful pinned entry into stable user-owned composition that survives adaptive budget zero', () => {
    const opportunitySet = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: [
        opportunity('continuity', 'continuity', 'primary'),
        opportunity('next', 'next', 'primary'),
      ],
    });

    const resolution = resolveWorldFocusCompositionCandidates({
      opportunitySet,
      config: config([
        {
          instanceId: 'continuity',
          kind: 'continuity',
          pinned: true,
        },
      ]),
      valueSignals: [signals('next', 'next', ['current-intent'])],
    });

    const continuity = resolution.candidates.find(
      (candidate) => candidate.instanceId === 'continuity',
    );
    expect(continuity).toMatchObject({
      ownership: { stability: 'stable', origin: 'user' },
      prominence: 'primary',
      order: 0,
    });

    const plan = resolveWorldFocusCompositionPlan(resolution.candidates, {
      maxAdaptiveEntries: 0,
      maxEphemeralEntries: 0,
    });
    expect(plan.entries.map((entry) => entry.instanceId)).toEqual(['continuity']);
  });

  it('preserves pinned intent without fabricating a candidate when meaningful projection is unavailable', () => {
    const resolution = resolveWorldFocusCompositionCandidates({
      opportunitySet: createWorldFocusCompositionOpportunitySet({
        worldId: 'music',
        opportunities: [opportunity('situation', 'situation', 'primary')],
      }),
      config: config([
        {
          instanceId: 'comparison:release',
          kind: 'comparison',
          pinned: true,
        },
      ]),
      valueSignals: [],
    });

    expect(
      resolution.candidates.map((candidate) => candidate.instanceId),
    ).toEqual(['situation']);
    expect(resolution.unresolvedPinned).toEqual([
      {
        instanceId: 'comparison:release',
        kind: 'comparison',
        reason: 'meaningful-projection-unavailable',
      },
    ]);
  });

  it('preserves configured relative order and opportunity prominence, ignores adaptive signals for configured entries, and honors explicit promote', () => {
    const opportunitySet = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: [
        opportunity('situation', 'situation', 'supporting'),
        opportunity('continuity', 'continuity', 'supporting'),
        opportunity('attention:new', 'attention', 'supporting'),
      ],
    });

    const resolution = resolveWorldFocusCompositionCandidates({
      opportunitySet,
      config: config([
        { instanceId: 'continuity', kind: 'continuity' },
        {
          instanceId: 'situation',
          kind: 'situation',
          prominenceOverride: 'lead',
        },
      ]),
      valueSignals: [
        signals('continuity', 'continuity', ['current-intent', 'immediacy']),
        signals('attention:new', 'attention', ['resumability']),
      ],
    });

    const byId = new Map(
      resolution.candidates.map((candidate) => [candidate.instanceId, candidate]),
    );
    expect(byId.get('continuity')).toMatchObject({
      ownership: { stability: 'adaptive', origin: 'user' },
      prominence: 'supporting',
      order: 0,
    });
    expect(byId.get('situation')).toMatchObject({
      ownership: { stability: 'adaptive', origin: 'user' },
      prominence: 'lead',
      order: 1,
    });
    expect(byId.get('attention:new')).toMatchObject({
      ownership: { stability: 'adaptive', origin: 'application-derived' },
      prominence: 'primary',
    });
  });

  it('ranks only unconfigured opportunities through finite foreground/active/ordinary bands with no magic score', () => {
    const opportunitySet = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: [
        opportunity('ordinary', 'situation'),
        opportunity('active', 'continuity'),
        opportunity('foreground', 'attention'),
      ],
    });
    const valueSignals = [
      signals('active', 'continuity', ['meaningful-change']),
      signals('foreground', 'attention', ['immediacy']),
    ];

    const resolution = resolveWorldFocusCompositionCandidates({
      opportunitySet,
      config: config([]),
      valueSignals,
    });
    const repeated = resolveWorldFocusCompositionCandidates({
      opportunitySet,
      config: config([]),
      valueSignals,
    });

    expect(repeated).toEqual(resolution);
    expect(
      resolution.candidates.map((candidate) => [
        candidate.instanceId,
        candidate.prominence,
      ]),
    ).toEqual([
      ['foreground', 'lead'],
      ['active', 'primary'],
      ['ordinary', 'supporting'],
    ]);
    expect(JSON.stringify(resolution)).not.toContain('confidence');
    expect(JSON.stringify(resolution)).not.toContain('aiRelevance');
    expect(JSON.stringify(resolution)).not.toContain('score');
  });

  it('rejects stale World/kind/signal assignments instead of silently attaching value to the wrong candidate', () => {
    const opportunitySet = createWorldFocusCompositionOpportunitySet({
      worldId: 'music',
      opportunities: [opportunity('situation', 'situation', 'primary')],
    });

    expect(() =>
      resolveWorldFocusCompositionCandidates({
        opportunitySet,
        config: config([], 'travel'),
        valueSignals: [],
      }),
    ).toThrow(/World/i);

    expect(() =>
      resolveWorldFocusCompositionCandidates({
        opportunitySet,
        config: config([{ instanceId: 'situation', kind: 'next' }]),
        valueSignals: [],
      }),
    ).toThrow(/kind/i);

    expect(() =>
      resolveWorldFocusCompositionCandidates({
        opportunitySet,
        config: config([]),
        valueSignals: [signals('missing', 'situation', ['current-intent'])],
      }),
    ).toThrow(/signal/i);

    expect(() =>
      resolveWorldFocusCompositionCandidates({
        opportunitySet,
        config: config([]),
        valueSignals: [signals('situation', 'next', ['current-intent'])],
      }),
    ).toThrow(/kind/i);

    expect(() =>
      resolveWorldFocusCompositionCandidates({
        opportunitySet,
        config: config([]),
        valueSignals: [
          signals('situation', 'situation', ['current-intent'], 'travel'),
        ],
      }),
    ).toThrow(/World/i);
  });

  it('normalizes finite signal assignments and strips AI/confidence payload rather than creating hidden ranking authority', () => {
    const assignment = createWorldFocusCompositionValueSignalAssignment({
      worldId: 'future-world-2040',
      instanceId: 'future-specialist',
      kind: 'future-specialist',
      signals: ['current-intent', 'resumability'],
      aiRelevance: 0.99,
      confidence: 0.99,
      score: 99,
    } as never);

    expect(assignment).toEqual({
      worldId: 'future-world-2040',
      instanceId: 'future-specialist',
      kind: 'future-specialist',
      signals: ['current-intent', 'resumability'],
    });
    expect(assignment).not.toHaveProperty('aiRelevance');
    expect(assignment).not.toHaveProperty('confidence');
    expect(assignment).not.toHaveProperty('score');

    expect(() =>
      createWorldFocusCompositionValueSignalAssignment({
        worldId: 'music',
        instanceId: 'situation',
        kind: 'situation',
        signals: ['current-intent', 'current-intent'],
      }),
    ).toThrow(/duplicate/i);
  });

  it('supports an unknown future World and future renderer kind without requiring catalog expansion', () => {
    const opportunitySet = createWorldFocusCompositionOpportunitySet({
      worldId: 'apiary-2040',
      opportunities: [
        opportunity('specialist:apiary', 'specialist-apiary', 'supporting'),
      ],
    });

    const resolution = resolveWorldFocusCompositionCandidates({
      opportunitySet,
      config: config([], 'apiary-2040'),
      valueSignals: [
        signals(
          'specialist:apiary',
          'specialist-apiary',
          ['current-intent'],
          'apiary-2040',
        ),
      ],
    });

    expect(resolution.candidates).toEqual([
      {
        instanceId: 'specialist:apiary',
        kind: 'specialist-apiary',
        ownership: {
          stability: 'adaptive',
          origin: 'application-derived',
        },
        prominence: 'lead',
        footprint: 'standard',
        order: 0,
      },
    ]);
    expect(resolution.omitted).toEqual([]);
    expect(resolution.unresolvedPinned).toEqual([]);
  });
});
