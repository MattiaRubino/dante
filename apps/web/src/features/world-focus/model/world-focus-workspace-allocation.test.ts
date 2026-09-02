import { describe, expect, it } from 'vitest';

import {
  DEFAULT_WORLD_FOCUS_WORKSPACE_ALLOCATION_POLICY,
  resolveWorldFocusWorkspaceAllocation,
} from './world-focus-workspace-allocation';
import type { WorldFocusPresentationSurface } from './world-focus-platform';
import {
  createWorldFocusWorkspaceState,
  isWorldFocusBlockingPresentation,
  reduceWorldFocusWorkspaceState,
  type WorldFocusWorkspaceState,
} from './world-focus-workspace';

function openSurface(
  state: WorldFocusWorkspaceState,
  instanceId: string,
  presentation: WorldFocusPresentationSurface,
): WorldFocusWorkspaceState {
  return reduceWorldFocusWorkspaceState(state, {
    type: 'open-surface',
    surface: {
      instanceId,
      kind: `test:${presentation}`,
      depth: presentation === 'full-screen' ? 'explore' : 'insight',
      presentation,
      origin: 'application',
    },
  });
}

function getPlacement(
  plan: ReturnType<typeof resolveWorldFocusWorkspaceAllocation>,
  instanceId: string,
) {
  const placement = plan.placements.find(
    (candidate) => candidate.instanceId === instanceId,
  );
  if (placement === undefined) {
    throw new Error(`Missing placement ${instanceId}`);
  }
  return placement;
}

function createDeterministicRandom(seed: number): () => number {
  let state = seed >>> 0;
  return () => {
    state = (Math.imul(state, 1664525) + 1013904223) >>> 0;
    return state / 0x1_0000_0000;
  };
}

describe('World Focus workspace surface allocation', () => {
  it('keeps an empty workspace as full interactive content with no transient layer', () => {
    const plan = resolveWorldFocusWorkspaceAllocation(
      createWorldFocusWorkspaceState('music'),
      1280,
    );

    expect(plan).toMatchObject({
      mainAllocation: 'full',
      topLayer: 'none',
      mainInteraction: 'interactive',
      workspaceInlineSize: 1280,
      mainInlineSize: 1280,
      sidecarInlineSize: null,
      splitGap: 0,
      activeSidecarInstanceId: null,
      activeOverlayInstanceId: null,
      activeFocusInstanceId: null,
    });
  });

  it('allocates a wide sidecar beside the main canvas without creating an overlay layer', () => {
    const state = openSurface(
      createWorldFocusWorkspaceState('music'),
      'dante:thread',
      'sidecar',
    );
    const plan = resolveWorldFocusWorkspaceAllocation(state, 1280);

    expect(plan.mainAllocation).toBe('split');
    expect(plan.topLayer).toBe('none');
    expect(plan.mainInteraction).toBe('interactive');
    expect(plan.activeSidecarInstanceId).toBe('dante:thread');
    expect(plan.sidecarInlineSize).toBe(420);
    expect(plan.mainInlineSize).toBe(844);
    expect(plan.splitGap).toBe(16);
    expect(getPlacement(plan, 'dante:thread')).toMatchObject({
      slot: 'sidecar',
      activeInSlot: true,
      interaction: 'interactive',
    });
  });

  it('degrades a sidecar to a non-modal overlay when preserving a useful main canvas would fail', () => {
    const state = openSurface(
      createWorldFocusWorkspaceState('travel'),
      'insight:trip',
      'sidecar',
    );
    const plan = resolveWorldFocusWorkspaceAllocation(state, 899);

    expect(plan).toMatchObject({
      mainAllocation: 'full',
      topLayer: 'overlay',
      mainInteraction: 'interactive',
      mainInlineSize: 899,
      sidecarInlineSize: null,
      splitGap: 0,
      activeSidecarInstanceId: null,
      activeOverlayInstanceId: 'insight:trip',
    });
    expect(getPlacement(plan, 'insight:trip')).toMatchObject({
      slot: 'overlay',
      activeInSlot: true,
      interaction: 'interactive',
    });
  });

  it('preserves split allocation underneath a modal while making main and sidecar inert', () => {
    let state = createWorldFocusWorkspaceState('finance');
    state = openSurface(state, 'dante:finance', 'sidecar');
    state = openSurface(state, 'confirm:transfer', 'modal');

    const plan = resolveWorldFocusWorkspaceAllocation(state, 1280);

    expect(plan).toMatchObject({
      mainAllocation: 'split',
      topLayer: 'overlay',
      mainInteraction: 'inert',
      activeSidecarInstanceId: 'dante:finance',
      activeOverlayInstanceId: 'confirm:transfer',
      activeFocusInstanceId: null,
    });
    expect(getPlacement(plan, 'dante:finance')).toMatchObject({
      slot: 'sidecar',
      activeInSlot: true,
      interaction: 'inert',
    });
    expect(getPlacement(plan, 'confirm:transfer')).toMatchObject({
      slot: 'overlay',
      activeInSlot: true,
      interaction: 'interactive',
    });
  });

  it('preserves the underlying sidecar allocation while full focus makes main and sidecar inert', () => {
    let state = createWorldFocusWorkspaceState('projects');
    state = openSurface(state, 'dante:project', 'sidecar');
    state = openSurface(state, 'explore:project-history', 'full-screen');

    const plan = resolveWorldFocusWorkspaceAllocation(state, 1440);

    expect(plan).toMatchObject({
      mainAllocation: 'split',
      topLayer: 'focus',
      mainInteraction: 'inert',
      activeSidecarInstanceId: 'dante:project',
      activeOverlayInstanceId: null,
      activeFocusInstanceId: 'explore:project-history',
    });
    expect(getPlacement(plan, 'dante:project')).toMatchObject({
      slot: 'sidecar',
      activeInSlot: true,
      interaction: 'inert',
    });
    expect(getPlacement(plan, 'explore:project-history')).toMatchObject({
      slot: 'focus',
      activeInSlot: true,
      interaction: 'interactive',
    });
  });

  it('keeps a narrow sidecar dormant while a newer modal owns the only active overlay slot', () => {
    let state = createWorldFocusWorkspaceState('relationships');
    state = openSurface(state, 'dante:relationship', 'sidecar');
    state = openSurface(state, 'confirm:note', 'modal');

    const plan = resolveWorldFocusWorkspaceAllocation(state, 720);

    expect(plan).toMatchObject({
      mainAllocation: 'full',
      topLayer: 'overlay',
      mainInteraction: 'inert',
      activeSidecarInstanceId: null,
      activeOverlayInstanceId: 'confirm:note',
    });
    expect(getPlacement(plan, 'dante:relationship')).toMatchObject({
      slot: 'dormant',
      activeInSlot: false,
      interaction: 'inert',
    });
    expect(getPlacement(plan, 'confirm:note')).toMatchObject({
      slot: 'overlay',
      activeInSlot: true,
      interaction: 'interactive',
    });
  });

  it('allocates only the most recent sidecar and leaves earlier sidecars dormant', () => {
    let state = createWorldFocusWorkspaceState('study');
    state = openSurface(state, 'insight:first', 'sidecar');
    state = openSurface(state, 'insight:second', 'sidecar');

    const plan = resolveWorldFocusWorkspaceAllocation(state, 1200);

    expect(plan.activeSidecarInstanceId).toBe('insight:second');
    expect(plan.mainInteraction).toBe('interactive');
    expect(getPlacement(plan, 'insight:first')).toMatchObject({
      slot: 'dormant',
      activeInSlot: false,
      interaction: 'inert',
    });
    expect(getPlacement(plan, 'insight:second')).toMatchObject({
      slot: 'sidecar',
      activeInSlot: true,
      interaction: 'interactive',
    });
  });

  it('keeps route presentation external to workspace geometry and interaction', () => {
    const state = openSurface(
      createWorldFocusWorkspaceState('travel'),
      'route:details',
      'route',
    );
    const plan = resolveWorldFocusWorkspaceAllocation(state, 1024);

    expect(plan).toMatchObject({
      mainAllocation: 'full',
      topLayer: 'none',
      mainInteraction: 'interactive',
      mainInlineSize: 1024,
      sidecarInlineSize: null,
    });
    expect(getPlacement(plan, 'route:details')).toMatchObject({
      slot: 'external',
      activeInSlot: true,
      interaction: 'interactive',
    });
  });

  it('keeps a blocker authoritative even if a malformed legacy stack places weaker surfaces above it', () => {
    const malformedState: WorldFocusWorkspaceState = Object.freeze({
      worldId: 'finance',
      generation: 4,
      selection: null,
      contextReferences: null,
      surfaces: Object.freeze([
        Object.freeze({
          instanceId: 'dante:under',
          kind: 'assistant',
          depth: 'insight',
          presentation: 'sidecar',
          origin: 'dante',
          boundGeneration: 4,
          contextReference: null,
          dismissible: true,
        }),
        Object.freeze({
          instanceId: 'confirm:blocker',
          kind: 'confirmation',
          depth: 'insight',
          presentation: 'modal',
          origin: 'application',
          boundGeneration: 4,
          contextReference: null,
          dismissible: true,
        }),
        Object.freeze({
          instanceId: 'dante:illegal-late',
          kind: 'assistant',
          depth: 'insight',
          presentation: 'sidecar',
          origin: 'dante',
          boundGeneration: 4,
          contextReference: null,
          dismissible: true,
        }),
        Object.freeze({
          instanceId: 'route:illegal-late',
          kind: 'route',
          depth: 'explore',
          presentation: 'route',
          origin: 'user',
          boundGeneration: 4,
          contextReference: null,
          dismissible: true,
        }),
      ]),
    });

    const plan = resolveWorldFocusWorkspaceAllocation(malformedState, 1280);

    expect(plan).toMatchObject({
      mainAllocation: 'split',
      topLayer: 'overlay',
      mainInteraction: 'inert',
      activeSidecarInstanceId: 'dante:under',
      activeOverlayInstanceId: 'confirm:blocker',
      topSurfaceInstanceId: 'confirm:blocker',
    });
    expect(getPlacement(plan, 'dante:under')).toMatchObject({
      slot: 'sidecar',
      activeInSlot: true,
      interaction: 'inert',
    });
    expect(getPlacement(plan, 'confirm:blocker')).toMatchObject({
      slot: 'overlay',
      activeInSlot: true,
      interaction: 'interactive',
    });
    expect(getPlacement(plan, 'dante:illegal-late')).toMatchObject({
      slot: 'dormant',
      activeInSlot: false,
      interaction: 'inert',
    });
    expect(getPlacement(plan, 'route:illegal-late')).toMatchObject({
      slot: 'dormant',
      activeInSlot: false,
      interaction: 'inert',
    });
  });

  it('rejects allocation policies that cannot satisfy their own split minima', () => {
    expect(() =>
      resolveWorldFocusWorkspaceAllocation(
        createWorldFocusWorkspaceState('music'),
        1200,
        {
          ...DEFAULT_WORLD_FOCUS_WORKSPACE_ALLOCATION_POLICY,
          minSplitInlineSize: 800,
        },
      ),
    ).toThrowError(
      'World Focus minimum split inline size cannot satisfy main, sidecar and gap minima',
    );

    expect(() =>
      resolveWorldFocusWorkspaceAllocation(
        createWorldFocusWorkspaceState('music'),
        1200,
        {
          ...DEFAULT_WORLD_FOCUS_WORKSPACE_ALLOCATION_POLICY,
          preferredSidecarFraction: 1,
        },
      ),
    ).toThrowError(
      'World Focus preferred sidecar fraction must be greater than 0 and less than 1',
    );
  });

  it('stays bounded and deterministic across 500 synthetic users, widths and surface stacks', () => {
    const random = createDeterministicRandom(0x5f3759df);
    const presentations: readonly WorldFocusPresentationSurface[] = [
      'inline',
      'popover',
      'sidecar',
      'modal',
      'full-screen',
      'route',
    ];

    for (let scenario = 0; scenario < 500; scenario += 1) {
      const width = Math.floor(random() * 1901);
      const surfaceCount = Math.floor(random() * 9);
      let state = createWorldFocusWorkspaceState(`synthetic-${scenario}`);

      for (let index = 0; index < surfaceCount; index += 1) {
        const presentation =
          presentations[Math.floor(random() * presentations.length)];
        if (presentation === undefined) {
          throw new Error('Expected deterministic presentation');
        }
        state = openSurface(
          state,
          `surface:${scenario}:${index}`,
          presentation,
        );
      }

      let blockingTailStarted = false;
      for (const surface of state.surfaces) {
        if (isWorldFocusBlockingPresentation(surface.presentation)) {
          blockingTailStarted = true;
        } else {
          expect(blockingTailStarted).toBe(false);
        }
      }

      const first = resolveWorldFocusWorkspaceAllocation(state, width);
      const second = resolveWorldFocusWorkspaceAllocation(state, width);

      expect(second).toEqual(first);
      expect(first.workspaceInlineSize).toBe(width);
      expect(first.mainInlineSize).toBeGreaterThanOrEqual(0);
      expect(first.mainInlineSize).toBeLessThanOrEqual(width);

      const activeSidecars = first.placements.filter(
        (placement) =>
          placement.slot === 'sidecar' && placement.activeInSlot,
      );
      const activeOverlays = first.placements.filter(
        (placement) =>
          placement.slot === 'overlay' && placement.activeInSlot,
      );
      const activeFocus = first.placements.filter(
        (placement) => placement.slot === 'focus' && placement.activeInSlot,
      );

      expect(activeSidecars.length).toBeLessThanOrEqual(1);
      expect(activeOverlays.length).toBeLessThanOrEqual(1);
      expect(activeFocus.length).toBeLessThanOrEqual(1);

      if (first.mainAllocation === 'split') {
        expect(first.sidecarInlineSize).not.toBeNull();
        expect(first.activeSidecarInstanceId).not.toBeNull();
        expect(activeSidecars).toHaveLength(1);
        expect(
          first.mainInlineSize +
            (first.sidecarInlineSize ?? 0) +
            first.splitGap,
        ).toBeCloseTo(width, 8);
      } else {
        expect(first.sidecarInlineSize).toBeNull();
        expect(first.activeSidecarInstanceId).toBeNull();
        expect(first.splitGap).toBe(0);
        expect(activeSidecars).toHaveLength(0);
      }

      if (first.topLayer === 'focus') {
        expect(first.activeFocusInstanceId).not.toBeNull();
        expect(first.activeOverlayInstanceId).toBeNull();
        expect(activeFocus).toHaveLength(1);
        expect(activeOverlays).toHaveLength(0);
      } else if (first.topLayer === 'overlay') {
        expect(first.activeOverlayInstanceId).not.toBeNull();
        expect(first.activeFocusInstanceId).toBeNull();
        expect(activeOverlays).toHaveLength(1);
        expect(activeFocus).toHaveLength(0);
      } else {
        expect(first.activeOverlayInstanceId).toBeNull();
        expect(first.activeFocusInstanceId).toBeNull();
        expect(activeOverlays).toHaveLength(0);
        expect(activeFocus).toHaveLength(0);
      }

      const activeBlockingPlacement = first.placements.find(
        (placement) =>
          placement.activeInSlot &&
          (placement.requestedPresentation === 'modal' ||
            placement.requestedPresentation === 'full-screen'),
      );
      const expectedBackgroundInteraction =
        activeBlockingPlacement === undefined ? 'interactive' : 'inert';
      expect(first.mainInteraction).toBe(expectedBackgroundInteraction);
      expect(
        activeSidecars.every(
          (placement) => placement.interaction === expectedBackgroundInteraction,
        ),
      ).toBe(true);
      expect(
        [...activeOverlays, ...activeFocus].every(
          (placement) => placement.interaction === 'interactive',
        ),
      ).toBe(true);
      expect(
        first.placements
          .filter((placement) => placement.slot === 'dormant')
          .every((placement) => placement.interaction === 'inert'),
      ).toBe(true);
    }
  });
});
