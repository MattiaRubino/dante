import { describe, expect, it } from 'vitest';

import {
  createWorldFocusWorkspaceState,
  getWorldFocusEscapeDisposition,
  getWorldFocusInteractionCursor,
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

  it('binds a surface to the initiating generation and rejects stale async presentation intents', () => {
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
        expectedGeneration: selected.generation,
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
        expectedGeneration: selected.generation,
      },
    });

    expect(staleIntent).toBe(newerSelection);
    expect(staleIntent.surfaces.map((surface) => surface.instanceId)).toEqual([
      'insight:flight-delay',
    ]);
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
