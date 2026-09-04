import { describe, expect, it } from 'vitest';

import {
  createWorldFocusCompositionConfig,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
  type WorldFocusCompositionConfig,
} from '../model/world-focus-composition-config';
import { createWorldFocusCompositionOpportunity } from './world-focus-composition-opportunities';
import {
  applyWorldFocusCompositionDraft,
  beginWorldFocusCompositionCustomization,
  cancelWorldFocusCompositionDraft,
  updateWorldFocusCompositionDraft,
  type WorldFocusCompositionCustomizationCommand,
} from './world-focus-composition-customization';

function makeConfig(revision = 4): WorldFocusCompositionConfig {
  return createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision,
    worldId: 'music',
    entries: [
      {
        instanceId: 'continuity',
        kind: 'continuity',
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
      {
        instanceId: 'next',
        kind: 'next',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
      {
        instanceId: 'trajectory',
        kind: 'trajectory',
        visibility: 'visible',
        pinned: false,
        prominenceOverride: null,
      },
    ],
  });
}

function runCommands(
  config: WorldFocusCompositionConfig,
  commands: readonly WorldFocusCompositionCustomizationCommand[],
) {
  return commands.reduce(
    (draft, command) => updateWorldFocusCompositionDraft(draft, command),
    beginWorldFocusCompositionCustomization(config),
  );
}

describe('World Focus composition customization draft', () => {
  it('keeps current config immutable while manual commands mutate only the draft', () => {
    const current = makeConfig();
    const draft = runCommands(current, [
      { source: 'manual', type: 'pin', instanceId: 'next' },
      { source: 'manual', type: 'hide', instanceId: 'trajectory' },
      {
        source: 'manual',
        type: 'move',
        instanceId: 'situation',
        beforeInstanceId: 'continuity',
      },
      { source: 'manual', type: 'promote', instanceId: 'continuity' },
    ]);

    expect(current.entries.map((entry) => entry.instanceId)).toEqual([
      'continuity',
      'situation',
      'next',
      'trajectory',
    ]);
    expect(current.entries.find((entry) => entry.instanceId === 'next')?.pinned).toBe(
      false,
    );

    expect(draft.workingConfig.entries.map((entry) => entry.instanceId)).toEqual([
      'situation',
      'continuity',
      'next',
      'trajectory',
    ]);
    expect(
      draft.workingConfig.entries.find((entry) => entry.instanceId === 'next')?.pinned,
    ).toBe(true);
    expect(
      draft.workingConfig.entries.find((entry) => entry.instanceId === 'trajectory')
        ?.visibility,
    ).toBe('hidden');
    expect(
      draft.workingConfig.entries.find((entry) => entry.instanceId === 'continuity')
        ?.prominenceOverride,
    ).toBe('lead');
  });

  it('cancels without side effects and restores the exact base snapshot', () => {
    const current = makeConfig();
    const draft = runCommands(current, [
      { source: 'manual', type: 'hide', instanceId: 'next' },
      { source: 'manual', type: 'pin', instanceId: 'continuity' },
    ]);

    const cancelled = cancelWorldFocusCompositionDraft(draft);

    expect(cancelled).toEqual(current);
    expect(cancelled.revision).toBe(4);
    expect(current.entries.find((entry) => entry.instanceId === 'next')?.visibility).toBe(
      'visible',
    );
  });

  it('applies once against the matching revision and fails closed on stale revision', () => {
    const current = makeConfig();
    const draft = runCommands(current, [
      { source: 'manual', type: 'pin', instanceId: 'next' },
    ]);

    const applied = applyWorldFocusCompositionDraft(current, draft);
    expect(applied.status).toBe('applied');
    if (applied.status !== 'applied') {
      throw new Error('Expected applied composition draft');
    }
    expect(applied.config.revision).toBe(5);
    expect(applied.config.entries.find((entry) => entry.instanceId === 'next')?.pinned).toBe(
      true,
    );

    const concurrentCurrent = makeConfig(5);
    const conflict = applyWorldFocusCompositionDraft(concurrentCurrent, draft);
    expect(conflict).toEqual({
      status: 'revision-conflict',
      baseRevision: 4,
      currentRevision: 5,
    });
  });

  it('keeps hide distinct from delete and restore returns one entry to its base state and order', () => {
    const current = makeConfig();
    const draft = runCommands(current, [
      { source: 'manual', type: 'hide', instanceId: 'situation' },
      { source: 'manual', type: 'pin', instanceId: 'situation' },
      {
        source: 'manual',
        type: 'move',
        instanceId: 'situation',
        beforeInstanceId: null,
      },
      { source: 'manual', type: 'restore', instanceId: 'situation' },
    ]);

    expect(draft.workingConfig.entries).toHaveLength(4);
    expect(draft.workingConfig.entries.map((entry) => entry.instanceId)).toEqual([
      'continuity',
      'situation',
      'next',
      'trajectory',
    ]);
    expect(
      draft.workingConfig.entries.find((entry) => entry.instanceId === 'situation'),
    ).toMatchObject({ visibility: 'visible', pinned: false, prominenceOverride: null });
  });

  it('adopts only opportunity metadata and restore removes an entry that was absent from the base snapshot', () => {
    const current = makeConfig();
    const comparison = createWorldFocusCompositionOpportunity({
      instanceId: 'comparison:release',
      kind: 'comparison',
      defaultProminence: 'supporting',
      footprint: 'standard',
    });
    const adopted = runCommands(current, [
      { source: 'manual', type: 'adopt', opportunity: comparison },
      { source: 'manual', type: 'pin', instanceId: 'comparison:release' },
    ]);

    expect(adopted.workingConfig.entries.at(-1)).toEqual({
      instanceId: 'comparison:release',
      kind: 'comparison',
      visibility: 'visible',
      pinned: true,
      prominenceOverride: null,
    });

    const restored = updateWorldFocusCompositionDraft(adopted, {
      source: 'manual',
      type: 'restore',
      instanceId: 'comparison:release',
    });
    expect(
      restored.workingConfig.entries.some(
        (entry) => entry.instanceId === 'comparison:release',
      ),
    ).toBe(false);
    expect(restored.workingConfig.entries).toEqual(current.entries);
  });

  it('uses the same command language for DANTE proposals without letting them bypass review/apply', () => {
    const current = makeConfig();
    const comparison = createWorldFocusCompositionOpportunity({
      instanceId: 'comparison:release',
      kind: 'comparison',
      defaultProminence: 'supporting',
      footprint: 'standard',
    });
    const draft = runCommands(current, [
      { source: 'dante-proposed', type: 'adopt', opportunity: comparison },
      { source: 'dante-proposed', type: 'pin', instanceId: 'comparison:release' },
      {
        source: 'dante-proposed',
        type: 'move',
        instanceId: 'comparison:release',
        beforeInstanceId: 'continuity',
      },
    ]);

    expect(current.revision).toBe(4);
    expect(
      current.entries.some((entry) => entry.instanceId === 'comparison:release'),
    ).toBe(false);
    expect(draft.baseRevision).toBe(4);
    expect(draft.operations.map((operation) => operation.source)).toEqual([
      'dante-proposed',
      'dante-proposed',
      'dante-proposed',
    ]);
    expect(draft.workingConfig.entries[0]?.instanceId).toBe('comparison:release');
    expect(
      draft.workingConfig.entries.find(
        (entry) => entry.instanceId === 'comparison:release',
      )?.pinned,
    ).toBe(true);
  });

  it('is deterministic for the same command sequence and rejects commands that target missing instances', () => {
    const current = makeConfig();
    const commands: readonly WorldFocusCompositionCustomizationCommand[] = [
      { source: 'manual', type: 'show', instanceId: 'next' },
      { source: 'manual', type: 'pin', instanceId: 'next' },
      { source: 'manual', type: 'unpin', instanceId: 'next' },
      {
        source: 'manual',
        type: 'move',
        instanceId: 'trajectory',
        beforeInstanceId: 'situation',
      },
    ];

    expect(runCommands(current, commands)).toEqual(runCommands(current, commands));

    expect(() =>
      updateWorldFocusCompositionDraft(beginWorldFocusCompositionCustomization(current), {
        source: 'manual',
        type: 'pin',
        instanceId: 'missing',
      }),
    ).toThrow(/missing/i);

    expect(() =>
      updateWorldFocusCompositionDraft(
        beginWorldFocusCompositionCustomization(current),
        {
          source: 'manual',
          type: 'move',
          instanceId: 'next',
          beforeInstanceId: 'missing',
        },
      ),
    ).toThrow(/missing/i);
  });

  it('rejects unsupported runtime command shapes instead of accepting a generic patch/property bag', () => {
    const current = makeConfig();

    expect(() =>
      updateWorldFocusCompositionDraft(
        beginWorldFocusCompositionCustomization(current),
        {
          source: 'manual',
          type: 'patch-everything',
          instanceId: 'next',
          payload: { canonicalTruth: true },
        } as never,
      ),
    ).toThrow(/unsupported/i);
  });

  it('rejects cross-World apply even when revisions happen to match', () => {
    const current = makeConfig();
    const draft = beginWorldFocusCompositionCustomization(current);
    const otherWorld = createWorldFocusCompositionConfig({
      schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
      revision: 4,
      worldId: 'travel',
      entries: current.entries,
    });

    expect(() => applyWorldFocusCompositionDraft(otherWorld, draft)).toThrow(/world/i);
  });
});
