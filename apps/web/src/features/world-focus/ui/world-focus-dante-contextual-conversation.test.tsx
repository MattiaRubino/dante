import { useState, type ReactNode } from 'react';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import {
  WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
  type WorldFocusDanteConversationReader,
  type WorldFocusDanteConversationRequest,
} from '../application/world-focus-dante-conversation';
import { createWorldFocusContextReferenceSet } from '../model/world-focus-context-reference';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import { WorldFocusDanteConversationPresentationController } from './world-focus-dante-conversation';
import { WorldFocusDanteConversationProvider } from './world-focus-dante-conversation-context';
import { WorldFocusDanteContextualEntry } from './world-focus-dante-contextual-entry';
import {
  WorldFocusDanteEntryProvider,
  useWorldFocusDanteEntry,
} from './world-focus-dante-entry';
import { WorldFocusRouteSurfaceLayer } from './world-focus-route-surface-layer';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

const CONTEXTUAL_REFERENCES = createWorldFocusContextReferenceSet({
  primary: { kind: 'project', key: 'neon-static' },
  supporting: [{ kind: 'checkpoint', key: 'master-v3' }],
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

function readyResult(request: WorldFocusDanteConversationRequest, output: string) {
  return Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
    status: 'ready' as const,
    requestId: request.requestId,
    worldId: request.worldId,
    workspaceGeneration: request.workspaceGeneration,
    resultClass: 'explanation' as const,
    output,
  });
}

function ConversationOwner({
  reader,
  children,
}: Readonly<{
  reader: WorldFocusDanteConversationReader;
  children: ReactNode;
}>) {
  const { composerInvocation, restoreInvokerFocus } = useWorldFocusDanteEntry();
  const composerContextSeed =
    composerInvocation?.contextReferences == null
      ? null
      : Object.freeze({
          references: composerInvocation.contextReferences,
          workspaceGeneration: composerInvocation.workspaceGeneration,
        });

  return (
    <WorldFocusDanteConversationProvider
      worldId="music"
      restoreInvokerFocus={restoreInvokerFocus}
      reader={reader}
      composerContextSeed={composerContextSeed}
    >
      {children}
    </WorldFocusDanteConversationProvider>
  );
}

function ContextualConversationHarness({
  reader,
}: Readonly<{ reader: WorldFocusDanteConversationReader }>) {
  const workspace = useWorldFocusWorkspace();
  const allocation = resolveWorldFocusWorkspaceAllocation(workspace.state, 1280);
  const [routeHost, setRouteHost] = useState<HTMLDivElement | null>(null);
  const registry = getCoreWorldFocusSurfaceRegistry();

  return (
    <WorldFocusWorkspaceAllocationProvider plan={allocation}>
      <WorldFocusDanteEntryProvider
        worldId="music"
        worldLabel="Musica"
        availability={{ status: 'available' }}
      >
        <ConversationOwner reader={reader}>
          <button
            type="button"
            onClick={() =>
              workspace.selectContext({
                kind: 'project',
                key: 'generation-change',
              })
            }
          >
            Change generation
          </button>
          <output data-testid="workspace-generation">
            {workspace.state.generation}
          </output>
          <WorldFocusDanteContextualEntry
            intent="continue"
            contextReferences={CONTEXTUAL_REFERENCES}
          />
          <div ref={setRouteHost} />
          <WorldFocusDanteConversationPresentationController>
            <WorldFocusSurfaceLayer registry={registry} />
            <WorldFocusRouteSurfaceLayer registry={registry} host={routeHost} />
          </WorldFocusDanteConversationPresentationController>
        </ConversationOwner>
      </WorldFocusDanteEntryProvider>
    </WorldFocusWorkspaceAllocationProvider>
  );
}

function renderHarness(reader: WorldFocusDanteConversationReader) {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <ContextualConversationHarness reader={reader} />
    </WorldFocusWorkspaceHost>,
  );
}

function openContextualComposer() {
  const invoker = screen.getByRole('button', {
    name: 'Chiedi a DANTE: Continua da qui',
  });
  invoker.focus();
  fireEvent.click(invoker);
  return invoker;
}

describe('World Focus D4 contextual conversation session', () => {
  it('carries the exact explicit reference set through the initial request and follow-up, then restores the exact contextual invoker', async () => {
    const requests: WorldFocusDanteConversationRequest[] = [];
    const reader: WorldFocusDanteConversationReader = (request) => {
      requests.push(request);
      return Promise.resolve(readyResult(request, `Contestuale ${requests.length}`));
    };
    renderHarness(reader);

    const invoker = openContextualComposer();
    const composerInput = screen.getByRole<HTMLTextAreaElement>('textbox', {
      name: 'Scrivi una richiesta per DANTE',
    });
    expect(composerInput.value).toBe('Continua da qui');
    fireEvent.change(composerInput, {
      target: { value: 'Continua da qui nel progetto' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));

    expect(await screen.findByText('Contestuale 1')).toBeTruthy();
    expect(requests).toHaveLength(1);
    expect(requests[0]?.contextReferences).toEqual(CONTEXTUAL_REFERENCES);

    const followUp = screen.getByRole<HTMLTextAreaElement>('textbox', {
      name: 'Continua la conversazione',
    });
    fireEvent.change(followUp, { target: { value: 'E il passo successivo?' } });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));

    expect(await screen.findByText('Contestuale 2')).toBeTruthy();
    expect(requests).toHaveLength(2);
    expect(requests[1]?.contextReferences).toEqual(CONTEXTUAL_REFERENCES);

    fireEvent.click(
      screen.getByRole('button', { name: 'Chiudi conversazione DANTE' }),
    );
    await waitFor(() => {
      expect(
        screen.queryByRole('dialog', { name: 'Conversazione con DANTE' }),
      ).toBeNull();
      expect(invoker).toBe(document.activeElement);
    });
  });

  it('invalidates a settled contextual session when workspace generation changes and refuses a stale follow-up', async () => {
    const requests: WorldFocusDanteConversationRequest[] = [];
    const reader: WorldFocusDanteConversationReader = (request) => {
      requests.push(request);
      return Promise.resolve(readyResult(request, 'Contesto iniziale'));
    };
    renderHarness(reader);

    openContextualComposer();
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));
    expect(await screen.findByText('Contesto iniziale')).toBeTruthy();
    expect(requests).toHaveLength(1);

    fireEvent.click(screen.getByRole('button', { name: 'Change generation' }));
    await waitFor(() => {
      expect(screen.getByTestId('workspace-generation').textContent).toBe('1');
      expect(
        screen.getByText(
          'Il contesto del Mondo è cambiato. La risposta precedente non è stata aggiunta.',
        ),
      ).toBeTruthy();
    });

    const followUp = screen.getByRole<HTMLTextAreaElement>('textbox', {
      name: 'Continua la conversazione',
    });
    fireEvent.change(followUp, {
      target: { value: 'Non usare il vecchio contesto' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));
    await Promise.resolve();

    expect(requests).toHaveLength(1);
    expect(followUp.value).toBe('Non usare il vecchio contesto');
  });
});
