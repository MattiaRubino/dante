import { describe, expect, it } from 'vitest';

import { resolveWorldFocusWorkspaceAllocation } from './world-focus-workspace-allocation';
import {
  createWorldFocusWorkspaceState,
  reduceWorldFocusWorkspaceState,
} from './world-focus-workspace';

describe('World Focus D2 route focus allocation RED gate', () => {
  it('makes the World main plane inert while an active route-owned focus surface covers it', () => {
    const base = createWorldFocusWorkspaceState('music');
    const state = reduceWorldFocusWorkspaceState(base, {
      type: 'open-surface',
      surface: {
        instanceId: 'dante:conversation',
        kind: 'dante-conversation',
        depth: 'explore',
        presentation: 'route',
        origin: 'user',
        contextReference: null,
        expectedWorkspace: {
          worldId: base.worldId,
          generation: base.generation,
        },
      },
    });

    const plan = resolveWorldFocusWorkspaceAllocation(state, 1280);

    expect(plan.placements).toContainEqual(
      expect.objectContaining({
        instanceId: 'dante:conversation',
        slot: 'external',
        activeInSlot: true,
      }),
    );
    expect(plan.mainInteraction).toBe('inert');
  });
});
