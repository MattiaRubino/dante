import { describe, expect, it } from 'vitest';

import {
  createWorldFocusWorkspaceState,
  getWorldFocusBlockingSurface,
  getWorldFocusEscapeDisposition,
  getWorldFocusInteractionCursor,
  isWorldFocusBlockingPresentation,
  reduceWorldFocusWorkspaceState,
} from './world-focus-workspace';

describe('World Focus workspace orchestration model', () => {
  it('keeps selection as bounded transient references and advances generation only when context changes', () => {
    const initial = createWorldFocusWorkspaceState('music');

    const selected = reduceWorldFocusWorkspaceState(initial, {
      type: 'select-context',
      reference: { kind: 'projection', key: 'continuity:track-a' },
    });

    expect(selected.worldId).toBe('music');
    expect(selected.generation).toBe(1);
    expect(selected.selection).toEqual({
      kind: 'projection',
      key: 'continuity:track-a',
    });

    const repeated = reduceWorldFocusWorkspaceState(selected, {
      type: 'select-context',
      reference: { kind: 'projection', key: 'continuity:track-a' },
    });

    expect(repeated).toBe(selected);

    const cleared = reduceWorldFocusWorkspaceState(selected, {
      type: 'clear-context',
    });

    expect(cleared.generation).toBe(2);
    expect(cleared.selection).toBeNull();
  });

  it('exposes a bounded cursor made only of World, generation and presentation references', () => {
    const selected = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('music'),
      {
        type: 'select-context',
        reference: { kind: 'projection', key: 'continuity:track-a' },
      },
    );
    const opened = reduceWorldFocusWorkspaceState(selected, {
      type: 'open-surface',
      surface: {
        instanceId: 'explore:versions',
        kind: 'artifact-explore',
        depth: 'explore',
        presentation: 'sidecar',
        origin: 'user',
      },
    });

    expect(getWorldFocusInteractionCursor(opened)).toEqual({
      worldId: 'music',
      generation: 1,
      selection: { kind: 'projection', key: 'continuity:track-a' },
      activeSurface: {
        instanceId: 'explore:versions',
        kind: 'artifact-explore',
        depth: 'explore',
        boundGeneration: 1,
        contextReference: {
          kind: 'projection',
          key: 'continuity:track-a',
        },
      },
    });
  });

  it('binds async presentation to both World identity and generation', () => {
    const selected = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('travel'),
      {
        type: 'select-context',
        reference: { kind: 'source', key: 'flight:AZ123' },
      },
    );

    const opened = reduceWorldFocusWorkspaceState(selected, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:flight-delay',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: {
          worldId: selected.worldId,
          generation: selected.generation,
        },
      },
    });

    expect(opened.surfaces).toHaveLength(1);
    expect(opened.surfaces[0]).toMatchObject({
      boundGeneration: 1,
      contextReference: { kind: 'source', key: 'flight:AZ123' },
    });

    const newerSelection = reduceWorldFocusWorkspaceState(opened, {
      type: 'select-context',
      reference: { kind: 'source', key: 'hotel:rome' },
    });

    const staleIntent = reduceWorldFocusWorkspaceState(newerSelection, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:stale-flight',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: {
          worldId: selected.worldId,
          generation: selected.generation,
        },
      },
    });

    expect(staleIntent).toBe(newerSelection);
    expect(staleIntent.surfaces.map((surface) => surface.instanceId)).toEqual([
      'insight:flight-delay',
    ]);
  });

  it('rejects a same-generation async result routed to a different World', () => {
    const sourceWorld = createWorldFocusWorkspaceState('music');
    const targetWorld = createWorldFocusWorkspaceState('travel');

    expect(sourceWorld.generation).toBe(targetWorld.generation);

    const misrouted = reduceWorldFocusWorkspaceState(targetWorld, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:from-music',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
        expectedWorkspace: {
          worldId: sourceWorld.worldId,
          generation: sourceWorld.generation,
        },
      },
    });

    expect(misrouted).toBe(targetWorld);
    expect(misrouted.surfaces).toEqual([]);
  });

  it('rejects malformed async workspace expectations instead of silently weakening the guard', () => {
    const state = createWorldFocusWorkspaceState('music');

    expect(() =>
      reduceWorldFocusWorkspaceState(state, {
        type: 'open-surface',
        surface: {
          instanceId: 'insight:bad-world',
          kind: 'insight',
          depth: 'insight',
          presentation: 'sidecar',
          origin: 'dante',
          expectedWorkspace: { worldId: '   ', generation: 0 },
        },
      }),
    ).toThrow(/expected workspace world id must not be empty/);

    expect(() =>
      reduceWorldFocusWorkspaceState(state, {
        type: 'open-surface',
        surface: {
          instanceId: 'insight:bad-generation',
          kind: 'insight',
          depth: 'insight',
          presentation: 'sidecar',
          origin: 'dante',
          expectedWorkspace: { worldId: 'music', generation: -1 },
        },
      }),
    ).toThrow(/expected workspace generation must be a non-negative integer/);
  });

  it('opens, replaces, promotes and closes finite presentation surfaces without rebinding existing surface context', () => {
    let state = createWorldFocusWorkspaceState<'insight' | 'explore'>('finance');
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'surface:a',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'user',
      },
    });

    expect(getWorldFocusEscapeDisposition(state)).toBe('surface-dismissible');

    state = reduceWorldFocusWorkspaceState(state, {
      type: 'promote-surface',
      instanceId: 'surface:a',
      depth: 'explore',
      presentation: 'full-screen',
    });

    expect(state.surfaces[0]).toMatchObject({
      depth: 'explore',
      presentation: 'full-screen',
      boundGeneration: 0,
    });

    state = reduceWorldFocusWorkspaceState(state, {
      type: 'replace-surface',
      instanceId: 'surface:a',
      surface: {
        instanceId: 'surface:b',
        kind: 'explore',
        depth: 'explore',
        presentation: 'modal',
        origin: 'application',
      },
    });

    expect(state.surfaces.map((surface) => surface.instanceId)).toEqual([
      'surface:b',
    ]);

    state = reduceWorldFocusWorkspaceState(state, {
      type: 'close-top-surface',
    });

    expect(state.surfaces).toEqual([]);
    expect(getWorldFocusEscapeDisposition(state)).toBe('no-surface');
  });

  it('treats modal and full-screen as admission barriers while still allowing deliberate nested blockers', () => {
    expect(isWorldFocusBlockingPresentation('modal')).toBe(true);
    expect(isWorldFocusBlockingPresentation('full-screen')).toBe(true);
    expect(isWorldFocusBlockingPresentation('sidecar')).toBe(false);

    let state = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('projects'),
      {
        type: 'open-surface',
        surface: {
          instanceId: 'confirmation:publish',
          kind: 'confirmation',
          depth: 'insight',
          presentation: 'modal',
          origin: 'application',
        },
      },
    );

    const blockedSidecar = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'dante:late',
        kind: 'assistant',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
      },
    });
    const blockedPopover = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'hint:late',
        kind: 'hint',
        depth: 'insight',
        presentation: 'popover',
        origin: 'application',
      },
    });
    const blockedRoute = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'route:late',
        kind: 'route',
        depth: 'explore',
        presentation: 'route',
        origin: 'user',
      },
    });

    expect(blockedSidecar).toBe(state);
    expect(blockedPopover).toBe(state);
    expect(blockedRoute).toBe(state);
    expect(getWorldFocusBlockingSurface(state)?.instanceId).toBe(
      'confirmation:publish',
    );

    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'confirmation:nested',
        kind: 'nested-confirmation',
        depth: 'insight',
        presentation: 'modal',
        origin: 'application',
      },
    });

    expect(state.surfaces.map((surface) => surface.instanceId)).toEqual([
      'confirmation:publish',
      'confirmation:nested',
    ]);
    expect(getWorldFocusBlockingSurface(state)?.instanceId).toBe(
      'confirmation:nested',
    );

    state = reduceWorldFocusWorkspaceState(state, { type: 'close-top-surface' });
    expect(getWorldFocusBlockingSurface(state)?.instanceId).toBe(
      'confirmation:publish',
    );

    state = reduceWorldFocusWorkspaceState(state, { type: 'close-top-surface' });
    const afterBarrier = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'dante:after',
        kind: 'assistant',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
      },
    });

    expect(afterBarrier.surfaces.map((surface) => surface.instanceId)).toEqual([
      'dante:after',
    ]);
  });

  it('rejects hidden replace and promote mutations below a blocking surface', () => {
    let state = createWorldFocusWorkspaceState<'insight' | 'confirmation'>(
      'music',
    );
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'insight:mix',
        kind: 'insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'dante',
      },
    });
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'confirmation:mix',
        kind: 'confirmation',
        depth: 'insight',
        presentation: 'modal',
        origin: 'application',
      },
    });

    const hiddenPromotion = reduceWorldFocusWorkspaceState(state, {
      type: 'promote-surface',
      instanceId: 'insight:mix',
      depth: 'explore',
      presentation: 'full-screen',
    });
    const hiddenReplacement = reduceWorldFocusWorkspaceState(state, {
      type: 'replace-surface',
      instanceId: 'insight:mix',
      surface: {
        instanceId: 'insight:replacement',
        kind: 'insight',
        depth: 'explore',
        presentation: 'full-screen',
        origin: 'application',
      },
    });

    expect(hiddenPromotion).toBe(state);
    expect(hiddenReplacement).toBe(state);

    state = reduceWorldFocusWorkspaceState(state, { type: 'close-top-surface' });
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'promote-surface',
      instanceId: 'insight:mix',
      depth: 'explore',
      presentation: 'full-screen',
    });

    expect(state.surfaces[0]).toMatchObject({
      instanceId: 'insight:mix',
      presentation: 'full-screen',
      depth: 'explore',
    });
  });

  it('does not replace a nested top blocker with a weaker surface while an earlier blocker remains below it', () => {
    let state = createWorldFocusWorkspaceState<'confirmation' | 'result'>(
      'finance',
    );
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'confirmation:first',
        kind: 'confirmation',
        depth: 'insight',
        presentation: 'modal',
        origin: 'application',
      },
    });
    state = reduceWorldFocusWorkspaceState(state, {
      type: 'open-surface',
      surface: {
        instanceId: 'confirmation:second',
        kind: 'confirmation',
        depth: 'insight',
        presentation: 'modal',
        origin: 'application',
      },
    });

    const weakened = reduceWorldFocusWorkspaceState(state, {
      type: 'replace-surface',
      instanceId: 'confirmation:second',
      surface: {
        instanceId: 'result:sidecar',
        kind: 'result',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'application',
      },
    });

    expect(weakened).toBe(state);
  });

  it('blocks Escape ownership at a non-dismissible top surface instead of allowing the World to close underneath it', () => {
    const state = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('body'),
      {
        type: 'open-surface',
        surface: {
          instanceId: 'confirmation:1',
          kind: 'confirmation',
          depth: 'insight',
          presentation: 'modal',
          origin: 'application',
          dismissible: false,
        },
      },
    );

    expect(getWorldFocusEscapeDisposition(state)).toBe('surface-blocked');
    expect(
      reduceWorldFocusWorkspaceState(state, {
        type: 'close-top-surface',
      }),
    ).toBe(state);
  });

  it('rejects empty workspace/context/surface identifiers before they can enter orchestration state', () => {
    expect(() => createWorldFocusWorkspaceState('   ')).toThrowError(
      'World Focus workspace world id must not be empty',
    );

    expect(() =>
      reduceWorldFocusWorkspaceState(createWorldFocusWorkspaceState('music'), {
        type: 'select-context',
        reference: { kind: 'projection', key: '   ' },
      }),
    ).toThrowError('World Focus context reference key must not be empty');

    expect(() =>
      reduceWorldFocusWorkspaceState(createWorldFocusWorkspaceState('music'), {
        type: 'open-surface',
        surface: {
          instanceId: ' ',
          kind: 'insight',
          depth: 'insight',
          presentation: 'sidecar',
          origin: 'dante',
        },
      }),
    ).toThrowError('World Focus surface instance id must not be empty');
  });
});
