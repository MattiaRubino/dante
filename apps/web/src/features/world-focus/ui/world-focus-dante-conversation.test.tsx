import { useState } from 'react';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import {
  WorldFocusDanteConversationPresentationController,
  WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  WORLD_FOCUS_DANTE_CONVERSATION_KIND,
  useWorldFocusDanteConversationPresentation,
} from './world-focus-dante-conversation';
import { WorldFocusRouteSurfaceLayer } from './world-focus-route-surface-layer';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

function D2Controls() {
  const workspace = useWorldFocusWorkspace();
  const presentation = useWorldFocusDanteConversationPresentation();
  const conversation = workspace.state.surfaces.find(
    (surface) =>
      surface.instanceId === WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  );

  const expectation = {
    worldId: workspace.state.worldId,
    generation: workspace.state.generation,
  } as const;

  return (
    <>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
            kind: WORLD_FOCUS_DANTE_CONVERSATION_KIND,
            depth: 'explore',
            presentation: 'sidecar',
            origin: 'user',
            contextReference: null,
            expectedWorkspace: expectation,
          })
        }
      >
        Open conversation
      </button>
      <button type="button" onClick={presentation.requestMaximize}>
        Maximize conversation
      </button>
      <button type="button" onClick={presentation.requestRestore}>
        Restore conversation
      </button>

      <output data-testid="conversation-presentation">
        {conversation?.presentation ?? 'none'}
      </output>
      <output data-testid="conversation-id">
        {conversation?.instanceId ?? 'none'}
      </output>
      <output data-testid="conversation-blocks-workspace">
        {conversation?.blocksWorkspaceInteraction === true ? 'true' : 'false'}
      </output>
      <output data-testid="surface-count">
        {workspace.state.surfaces.length}
      </output>
    </>
  );
}

function D2Harness({ width }: Readonly<{ width: number }>) {
  const workspace = useWorldFocusWorkspace();
  const allocation = resolveWorldFocusWorkspaceAllocation(workspace.state, width);
  const [routeHost, setRouteHost] = useState<HTMLDivElement | null>(null);
  const registry = getCoreWorldFocusSurfaceRegistry();

  return (
    <WorldFocusWorkspaceAllocationProvider plan={allocation}>
      <WorldFocusDanteConversationPresentationController>
        <D2Controls />
        <output data-testid="workspace-slot">
          {allocation.placements.find(
            (placement) =>
              placement.instanceId ===
              WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
          )?.slot ?? 'none'}
        </output>
        <WorldFocusSurfaceLayer registry={registry} />
        <div ref={setRouteHost} data-testid="route-surface-host" />
        <WorldFocusRouteSurfaceLayer registry={registry} host={routeHost} />
      </WorldFocusDanteConversationPresentationController>
    </WorldFocusWorkspaceAllocationProvider>
  );
}

function renderD2(width: number) {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <D2Harness width={width} />
    </WorldFocusWorkspaceHost>,
  );
}

describe('World Focus D2 adaptive conversation presentation', () => {
  it('materializes the finite conversation surface as a non-modal sidecar when a real split is viable', async () => {
    renderD2(1280);

    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }));

    await waitFor(() => {
      expect(screen.getByTestId('conversation-presentation').textContent).toBe(
        'sidecar',
      );
      expect(screen.getByTestId('workspace-slot').textContent).toBe('sidecar');
      expect(
        screen.getByTestId('conversation-blocks-workspace').textContent,
      ).toBe('false');
    });
    expect(screen.getByTestId('conversation-id').textContent).toBe(
      WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
    );

    const conversation = screen.getByRole('dialog', {
      name: 'Conversazione con DANTE',
    });
    expect(conversation.getAttribute('aria-modal')).toBe('false');
    expect(screen.queryByText(/risposta di DANTE/i)).toBeNull();
  });

  it('moves constrained conversation to route focus, blocks the World and focuses a live route control', async () => {
    renderD2(238);

    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }));

    await waitFor(() => {
      expect(screen.getByTestId('conversation-presentation').textContent).toBe(
        'route',
      );
      expect(screen.getByTestId('workspace-slot').textContent).toBe('external');
      expect(
        screen.getByTestId('conversation-blocks-workspace').textContent,
      ).toBe('true');
    });

    const conversation = screen.getByRole('dialog', {
      name: 'Conversazione con DANTE',
    });
    expect(conversation).toBeTruthy();
    expect(
      screen.getByTestId('route-surface-host').contains(conversation),
    ).toBe(true);
    await waitFor(() => {
      expect(
        screen.getByRole('button', { name: 'Chiudi conversazione DANTE' }),
      ).toBe(document.activeElement);
    });
  });

  it('maximizes and restores the same surface identity instead of creating a second conversation surface', async () => {
    renderD2(1280);

    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }));
    await waitFor(() => {
      expect(screen.getByTestId('workspace-slot').textContent).toBe('sidecar');
    });

    fireEvent.click(
      screen.getByRole('button', { name: 'Maximize conversation' }),
    );
    await waitFor(() => {
      expect(screen.getByTestId('conversation-presentation').textContent).toBe(
        'route',
      );
      expect(screen.getByTestId('workspace-slot').textContent).toBe('external');
      expect(
        screen.getByTestId('conversation-blocks-workspace').textContent,
      ).toBe('true');
    });
    expect(screen.getByTestId('conversation-id').textContent).toBe(
      WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
    );
    expect(screen.getByTestId('surface-count').textContent).toBe('1');
    expect(
      screen.getByRole('dialog', { name: 'Conversazione con DANTE' }),
    ).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: 'Restore conversation' }),
    );
    await waitFor(() => {
      expect(screen.getByTestId('conversation-presentation').textContent).toBe(
        'sidecar',
      );
      expect(screen.getByTestId('workspace-slot').textContent).toBe('sidecar');
      expect(
        screen.getByTestId('conversation-blocks-workspace').textContent,
      ).toBe('false');
    });
    expect(screen.getByTestId('conversation-id').textContent).toBe(
      WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
    );
    expect(screen.getByTestId('surface-count').textContent).toBe('1');
  });

  it('uses the production surface controls and preserves keyboard focus across maximize and restore', async () => {
    renderD2(1280);

    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }));
    const maximize = await screen.findByRole('button', { name: 'Massimizza' });
    maximize.focus();
    fireEvent.click(maximize);

    await waitFor(() => {
      expect(
        screen.getByRole('button', { name: 'Ripristina' }),
      ).toBe(document.activeElement);
    });

    fireEvent.click(screen.getByRole('button', { name: 'Ripristina' }));
    await waitFor(() => {
      expect(
        screen.getByRole('button', { name: 'Massimizza' }),
      ).toBe(document.activeElement);
    });
  });
});
