import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

const CONVERSATION_ID = 'dante:conversation';
const CONVERSATION_KIND = 'dante-conversation';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

function D2Harness({ width }: Readonly<{ width: number }>) {
  const workspace = useWorldFocusWorkspace();
  const allocation = resolveWorldFocusWorkspaceAllocation(workspace.state, width);
  const conversation = workspace.state.surfaces.find(
    (surface) => surface.instanceId === CONVERSATION_ID,
  );

  const expectation = {
    worldId: workspace.state.worldId,
    generation: workspace.state.generation,
  } as const;

  return (
    <WorldFocusWorkspaceAllocationProvider plan={allocation}>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: CONVERSATION_ID,
            kind: CONVERSATION_KIND,
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
      <button
        type="button"
        onClick={() =>
          workspace.promoteSurface(
            CONVERSATION_ID,
            'explore',
            'route',
            expectation,
          )
        }
      >
        Maximize conversation
      </button>
      <button
        type="button"
        onClick={() =>
          workspace.promoteSurface(
            CONVERSATION_ID,
            'explore',
            'sidecar',
            expectation,
          )
        }
      >
        Restore conversation
      </button>

      <output data-testid="conversation-presentation">
        {conversation?.presentation ?? 'none'}
      </output>
      <output data-testid="conversation-id">
        {conversation?.instanceId ?? 'none'}
      </output>
      <output data-testid="workspace-slot">
        {allocation.placements.find(
          (placement) => placement.instanceId === CONVERSATION_ID,
        )?.slot ?? 'none'}
      </output>

      <WorldFocusSurfaceLayer registry={getCoreWorldFocusSurfaceRegistry()} />
      <div data-testid="route-surface-host" />
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

describe('World Focus D2 adaptive conversation presentation RED gate', () => {
  it('materializes the finite conversation surface as a non-modal sidecar when a real split is viable', () => {
    renderD2(1280);

    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }));

    expect(screen.getByTestId('conversation-presentation').textContent).toBe(
      'sidecar',
    );
    expect(screen.getByTestId('workspace-slot').textContent).toBe('sidecar');
    expect(screen.getByTestId('conversation-id').textContent).toBe(
      CONVERSATION_ID,
    );

    const conversation = screen.getByRole('dialog', {
      name: 'Conversazione con DANTE',
    });
    expect(conversation.getAttribute('aria-modal')).toBe('false');
    expect(screen.queryByText(/risposta di DANTE/i)).toBeNull();
  });

  it('does not leave ongoing conversation trapped in the workspace-local overlay when split is impossible', () => {
    renderD2(238);

    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }));

    expect(screen.getByTestId('conversation-presentation').textContent).toBe(
      'route',
    );
    expect(screen.getByTestId('workspace-slot').textContent).toBe('external');
    expect(
      screen.getByRole('dialog', { name: 'Conversazione con DANTE' }),
    ).toBeTruthy();
  });

  it('maximizes and restores the same surface identity instead of creating a second conversation surface', () => {
    renderD2(1280);

    fireEvent.click(screen.getByRole('button', { name: 'Open conversation' }));
    expect(screen.getByTestId('workspace-slot').textContent).toBe('sidecar');

    fireEvent.click(
      screen.getByRole('button', { name: 'Maximize conversation' }),
    );
    expect(screen.getByTestId('conversation-presentation').textContent).toBe(
      'route',
    );
    expect(screen.getByTestId('conversation-id').textContent).toBe(
      CONVERSATION_ID,
    );
    expect(
      screen.getByRole('dialog', { name: 'Conversazione con DANTE' }),
    ).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: 'Restore conversation' }),
    );
    expect(screen.getByTestId('conversation-presentation').textContent).toBe(
      'sidecar',
    );
    expect(screen.getByTestId('conversation-id').textContent).toBe(
      CONVERSATION_ID,
    );
  });
});
