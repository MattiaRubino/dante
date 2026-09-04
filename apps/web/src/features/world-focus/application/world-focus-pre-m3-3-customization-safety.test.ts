import { describe, expect, it } from 'vitest';

import {
  createWorldFocusCompositionConfig,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
} from '../model/world-focus-composition-config';
import {
  createWorldFocusCompositionOpportunity,
  createWorldFocusCompositionOpportunitySet,
} from './world-focus-composition-opportunities';
import {
  applyWorldFocusCompositionDraft,
  beginWorldFocusCompositionCustomization,
  updateWorldFocusCompositionDraft,
} from './world-focus-composition-customization';
import { resolveWorldFocusCompositionCandidates } from './world-focus-composition-resolver';

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
  revision = 7,
) {
  return createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision,
    worldId: 'music',
    entries: entries.map((entry) => ({
      instanceId: entry.instanceId,
      kind: entry.kind,
      visibility: entry.visibility ?? 'visible',
      pinned: entry.pinned ?? false,
      prominenceOverride: entry.prominenceOverride ?? null,
    })),
  });
}

function opportunity(
  instanceId: string,
  kind: string,
  defaultProminence: 'lead' | 'primary' | 'supporting' = 'supporting',
) {
  return createWorldFocusCompositionOpportunity({
    instanceId,
    kind,
    defaultProminence,
    footprint: 'standard',
  });
}

describe('World Focus PRE-M3-3 customization reachability safety', () => {
  it('lets a meaningful unconfigured opportunity enter the same finite draft path before pin/hide/move/promote', () => {
    const current = config([{ instanceId: 'continuity', kind: 'continuity' }]);
    const comparison = opportunity('comparison:release', 'comparison', 'supporting');

    const adopted = updateWorldFocusCompositionDraft(
      beginWorldFocusCompositionCustomization(current),
      {
        source: 'manual',
        type: 'adopt',
        opportunity: comparison,
      } as never,
    );

    expect(adopted.workingConfig.entries).toEqual([
      {
        instanceId: 'continuity',
        kind: 'continuity',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
      {
        instanceId: 'comparison:release',
        kind: 'comparison',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
    ]);

    const configured = updateWorldFocusCompositionDraft(adopted, {
      source: 'manual',
      type: 'pin',
      instanceId: 'comparison:release',
    });
    expect(
      configured.workingConfig.entries.find(
        (entry) => entry.instanceId === 'comparison:release',
      )?.pinned,
    ).toBe(true);
  });

  it('preserves opportunity default prominence when configuration exists without explicit promote', () => {
    const comparison = opportunity('comparison:release', 'comparison', 'supporting');
    const resolution = resolveWorldFocusCompositionCandidates({
      opportunitySet: createWorldFocusCompositionOpportunitySet({
        worldId: 'music',
        opportunities: [comparison],
      }),
      config: config([
        {
          instanceId: 'comparison:release',
          kind: 'comparison',
          prominenceOverride: null,
        },
      ]),
      valueSignals: [],
    });

    expect(resolution.candidates).toHaveLength(1);
    expect(resolution.candidates[0]).toMatchObject({
      instanceId: 'comparison:release',
      ownership: { stability: 'adaptive', origin: 'user' },
      prominence: 'supporting',
    });
  });

  it('fails closed when revision matches but draft base snapshot is not the current snapshot', () => {
    const current = config([
      { instanceId: 'continuity', kind: 'continuity', pinned: false },
    ]);
    const differentSameRevision = config([
      { instanceId: 'continuity', kind: 'continuity', pinned: true },
    ]);
    const draft = beginWorldFocusCompositionCustomization(differentSameRevision);

    expect(() => applyWorldFocusCompositionDraft(current, draft)).toThrow(
      /base|snapshot|invalid/i,
    );
  });

  it('normalizes adopt through opportunity metadata and never retains arbitrary payload', () => {
    const current = config([]);
    const adopted = updateWorldFocusCompositionDraft(
      beginWorldFocusCompositionCustomization(current),
      {
        source: 'dante-proposed',
        type: 'adopt',
        opportunity: {
          instanceId: 'trajectory:release',
          kind: 'trajectory',
          defaultProminence: 'supporting',
          footprint: 'standard',
          canonicalPayload: { secret: true },
          disclosure: 'available',
          aiRelevance: 0.99,
        },
      } as never,
    );

    expect(adopted.operations).toEqual([
      {
        source: 'dante-proposed',
        type: 'adopt',
        instanceId: 'trajectory:release',
        kind: 'trajectory',
      },
    ]);
    expect(JSON.stringify(adopted)).not.toContain('canonicalPayload');
    expect(JSON.stringify(adopted)).not.toContain('secret');
    expect(JSON.stringify(adopted)).not.toContain('aiRelevance');
    expect(JSON.stringify(adopted)).not.toContain('disclosure');
  });

  it('rejects duplicate, blank and malformed adopt targets instead of creating arbitrary config entries', () => {
    const comparison = opportunity('comparison:release', 'comparison');
    const adopted = updateWorldFocusCompositionDraft(
      beginWorldFocusCompositionCustomization(config([])),
      {
        source: 'manual',
        type: 'adopt',
        opportunity: comparison,
      } as never,
    );

    expect(() =>
      updateWorldFocusCompositionDraft(adopted, {
        source: 'manual',
        type: 'adopt',
        opportunity: comparison,
      } as never),
    ).toThrow(/duplicate/i);

    expect(() =>
      updateWorldFocusCompositionDraft(
        beginWorldFocusCompositionCustomization(config([])),
        {
          source: 'manual',
          type: 'adopt',
          opportunity: {
            instanceId: '   ',
            kind: 'comparison',
            defaultProminence: 'supporting',
            footprint: 'standard',
          },
        } as never,
      ),
    ).toThrow(/empty/i);

    expect(() =>
      updateWorldFocusCompositionDraft(
        beginWorldFocusCompositionCustomization(config([])),
        {
          source: 'manual',
          type: 'adopt',
          opportunity: {
            instanceId: 'comparison:release',
            kind: 'comparison',
            defaultProminence: 'magic',
            footprint: 'standard',
          },
        } as never,
      ),
    ).toThrow(/prominence|unsupported/i);
  });
});
