import { describe, expect, it } from 'vitest';

import { resolveWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation';
import {
  createWorldFocusWorkspaceState,
  reduceWorldFocusWorkspaceState,
} from './world-focus-workspace';

function openDanteRouteFocus() {
  const base = createWorldFocusWorkspaceState('music');
  return reduceWorldFocusWorkspaceState(base, {
    type: 'open-surface',
    surface: {
      instanceId: 'dante:conversation',
      kind: 'dante-conversation',
      depth: 'explore',
      presentation: 'route',
      origin: 'user',
      contextReference: null,
      blocksWorkspaceInteraction: true,
      expectedWorkspace: {
        worldId: base.worldId,
        generation: base.generation,
      },
    },
  });
}

describe('World Focus D2 route focus allocation', () => {
  it('makes the World main plane inert while an explicitly blocking route-owned focus surface covers it', () => {
    const state = openDanteRouteFocus();
    const plan = resolveWorldFocusWorkspaceAllocation(state, 1280);

    expect(plan.placements).toContainEqual(
      expect.objectContaining({
        instanceId: 'dante:conversation',
        slot: 'external',
        activeInSlot: true,
        interaction: 'interactive',
      }),
    );
    expect(plan.mainInteraction).toBe('inert');
  });

  it('keeps route focus authoritative against a later weaker surface request', () => {
    const focused = openDanteRouteFocus();
    const afterLateSidecar = reduceWorldFocusWorkspaceState(focused, {
      type: 'open-surface',
      surface: {
        instanceId: 'late:insight',
        kind: 'late-insight',
        depth: 'insight',
        presentation: 'sidecar',
        origin: 'application',
        contextReference: null,
        expectedWorkspace: {
          worldId: focused.worldId,
          generation: focused.generation,
        },
      },
    });

    expect(afterLateSidecar).toBe(focused);
    expect(afterLateSidecar.surfaces).toHaveLength(1);
    expect(afterLateSidecar.surfaces[0]?.instanceId).toBe('dante:conversation');
  });
});
