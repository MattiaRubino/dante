import { describe, expect, it } from 'vitest';

import { createWorldFocusContextReferenceSet } from './world-focus-context-reference';
import {
  createWorldFocusWorkspaceState,
  getWorldFocusInteractionCursor,
  reduceWorldFocusWorkspaceState,
} from './world-focus-workspace';

describe('World Focus workspace bounded reference-set materialization', () => {
  it('stores primary plus bounded ordered supporting references and advances generation once', () => {
    const initial = createWorldFocusWorkspaceState('future-craft');
    const references = createWorldFocusContextReferenceSet({
      primary: { kind: 'artifact', key: 'draft:1' },
      supporting: [
        { kind: 'source', key: 'brief:1' },
        { kind: 'source', key: 'note:2' },
      ],
    });

    const selected = reduceWorldFocusWorkspaceState(initial, {
      type: 'set-context',
      references,
    });

    expect(selected.generation).toBe(1);
    expect(selected.contextReferences).toEqual(references);
    expect(selected.selection).toEqual(references.primary);

    const repeated = reduceWorldFocusWorkspaceState(selected, {
      type: 'set-context',
      references: createWorldFocusContextReferenceSet({
        primary: { kind: 'artifact', key: 'draft:1' },
        supporting: [
          { kind: 'source', key: 'brief:1' },
          { kind: 'source', key: 'note:2' },
        ],
      }),
    });

    expect(repeated).toBe(selected);
  });

  it('exposes the full set to the cursor while surfaces inherit only the primary reference', () => {
    const selected = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('future-craft'),
      {
        type: 'set-context',
        references: createWorldFocusContextReferenceSet({
          primary: { kind: 'artifact', key: 'draft:1' },
          supporting: [{ kind: 'source', key: 'brief:1' }],
        }),
      },
    );
    const opened = reduceWorldFocusWorkspaceState(selected, {
      type: 'open-surface',
      surface: {
        instanceId: 'explore:draft',
        kind: 'artifact-explore',
        depth: 'explore',
        presentation: 'sidecar',
        origin: 'user',
      },
    });

    const cursor = getWorldFocusInteractionCursor(opened);
    expect(cursor.contextReferences).toEqual({
      primary: { kind: 'artifact', key: 'draft:1' },
      supporting: [{ kind: 'source', key: 'brief:1' }],
    });
    expect(cursor.activeSurface?.contextReference).toEqual({
      kind: 'artifact',
      key: 'draft:1',
    });
  });

  it('clears the whole reference set atomically', () => {
    const selected = reduceWorldFocusWorkspaceState(
      createWorldFocusWorkspaceState('future-craft'),
      {
        type: 'set-context',
        references: createWorldFocusContextReferenceSet({
          primary: { kind: 'artifact', key: 'draft:1' },
          supporting: [{ kind: 'source', key: 'brief:1' }],
        }),
      },
    );

    const cleared = reduceWorldFocusWorkspaceState(selected, {
      type: 'clear-context',
    });

    expect(cleared.generation).toBe(2);
    expect(cleared.contextReferences).toBeNull();
    expect(cleared.selection).toBeNull();
  });
});
