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
} from './world-focus-dante-conversation';
import {
  WorldFocusDanteEntryProvider,
  WorldFocusDanteInvoke,
} from './world-focus-dante-entry';
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

function D3RedHarness() {
  const workspace = useWorldFocusWorkspace();
  const allocation = resolveWorldFocusWorkspaceAllocation(workspace.state, 1280);
  const registry = getCoreWorldFocusSurfaceRegistry();

  return (
    <WorldFocusWorkspaceAllocationProvider plan={allocation}>
      <WorldFocusDanteEntryProvider
        worldId="music"
        worldLabel="Musica"
        availability={{ status: 'available' }}
      >
        <WorldFocusDanteConversationPresentationController>
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
                expectedWorkspace: {
                  worldId: workspace.state.worldId,
                  generation: workspace.state.generation,
                },
              })
            }
          >
            Seed conversation
          </button>
          <output data-testid="surface-count">
            {workspace.state.surfaces.length}
          </output>
          <WorldFocusDanteInvoke />
          <WorldFocusSurfaceLayer registry={registry} />
          <WorldFocusRouteSurfaceLayer registry={registry} host={null} />
        </WorldFocusDanteConversationPresentationController>
      </WorldFocusDanteEntryProvider>
    </WorldFocusWorkspaceAllocationProvider>
  );
}

function renderD3RedHarness() {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <D3RedHarness />
    </WorldFocusWorkspaceHost>,
  );
}

describe('World Focus D3 deterministic conversation bridge — RED contract', () => {
  it('hands a submitted composer request to the one conversation surface instead of reporting the old D1 unavailable fallback', async () => {
    renderD3RedHarness();

    const invoke = screen.getByRole('button', {
      name: 'Apri DANTE per il Mondo Musica',
    });
    fireEvent.click(invoke);

    const textarea = screen.getByRole('textbox', {
      name: 'Scrivi una richiesta per DANTE',
    });
    fireEvent.change(textarea, {
      target: { value: 'Perché questo progetto è in pausa?' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));

    await waitFor(() => {
      expect(
        screen.getByRole('dialog', { name: 'Conversazione con DANTE' }),
      ).toBeTruthy();
    });
    expect(screen.queryByRole('dialog', { name: 'DANTE' })).toBeNull();
    expect(screen.getByTestId('surface-count').textContent).toBe('1');
    expect(
      screen.queryByText(
        'DANTE non è disponibile al momento. La richiesta è rimasta qui.',
      ),
    ).toBeNull();
  });

  it('treats an active conversation as the existing DANTE interaction and cannot open a second composer beside it', async () => {
    renderD3RedHarness();

    fireEvent.click(screen.getByRole('button', { name: 'Seed conversation' }));
    await waitFor(() => {
      expect(
        screen.getByRole('dialog', { name: 'Conversazione con DANTE' }),
      ).toBeTruthy();
    });

    const invoke = screen.getByRole('button', {
      name: 'Apri DANTE per il Mondo Musica',
    });
    expect(invoke.getAttribute('disabled')).not.toBeNull();
    fireEvent.click(invoke);

    expect(screen.queryByRole('dialog', { name: 'DANTE' })).toBeNull();
    expect(screen.getByTestId('surface-count').textContent).toBe('1');
  });
});
