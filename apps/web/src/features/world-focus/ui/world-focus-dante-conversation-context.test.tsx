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
import type {
  WorldFocusDanteConversationReadResult,
  WorldFocusDanteConversationReader,
  WorldFocusDanteConversationRequest,
} from '../application/world-focus-dante-conversation';
import { WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION } from '../application/world-focus-dante-conversation';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import {
  WorldFocusDanteConversationPresentationController,
  WORLD_FOCUS_DANTE_CONVERSATION_INSTANCE_ID,
  WORLD_FOCUS_DANTE_CONVERSATION_KIND,
} from './world-focus-dante-conversation';
import {
  WorldFocusDanteConversationProvider,
} from './world-focus-dante-conversation-context';
import {
  WorldFocusDanteEntryProvider,
  WorldFocusDanteInvoke,
  useWorldFocusDanteEntry,
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

type Deferred<Value> = Readonly<{
  promise: Promise<Value>;
  resolve: (value: Value) => void;
  reject: (error: unknown) => void;
}>;

function deferred<Value>(): Deferred<Value> {
  let resolve!: (value: Value) => void;
  let reject!: (error: unknown) => void;
  const promise = new Promise<Value>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise;
    reject = rejectPromise;
  });
  return { promise, resolve, reject };
}

function readyResult(
  request: WorldFocusDanteConversationRequest,
  output = 'Risposta locale differita',
): WorldFocusDanteConversationReadResult {
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

function D3ConversationOwner({
  reader,
  children,
}: Readonly<{
  reader?: WorldFocusDanteConversationReader;
  children: ReactNode;
}>) {
  const { restoreInvokerFocus } = useWorldFocusDanteEntry();
  const readerProps = reader === undefined ? {} : { reader };

  return (
    <WorldFocusDanteConversationProvider
      worldId="music"
      restoreInvokerFocus={restoreInvokerFocus}
      {...readerProps}
    >
      {children}
    </WorldFocusDanteConversationProvider>
  );
}

function D3Harness({
  reader,
  width = 1280,
}: Readonly<{
  reader?: WorldFocusDanteConversationReader;
  width?: number;
}>) {
  const workspace = useWorldFocusWorkspace();
  const allocation = resolveWorldFocusWorkspaceAllocation(workspace.state, width);
  const [routeHost, setRouteHost] = useState<HTMLDivElement | null>(null);
  const registry = getCoreWorldFocusSurfaceRegistry();
  const readerProps = reader === undefined ? {} : { reader };

  return (
    <WorldFocusWorkspaceAllocationProvider plan={allocation}>
      <WorldFocusDanteEntryProvider
        worldId="music"
        worldLabel="Musica"
        availability={{ status: 'available' }}
      >
        <D3ConversationOwner {...readerProps}>
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
          <button
            type="button"
            onClick={() =>
              workspace.selectContext({ kind: 'project', key: 'generation-change' })
            }
          >
            Change generation
          </button>
          <output data-testid="surface-count">
            {workspace.state.surfaces.length}
          </output>
          <output data-testid="workspace-generation">
            {workspace.state.generation}
          </output>
          <WorldFocusDanteInvoke />
          <div ref={setRouteHost} data-testid="route-host" />
          <WorldFocusDanteConversationPresentationController>
            <WorldFocusSurfaceLayer registry={registry} />
            <WorldFocusRouteSurfaceLayer registry={registry} host={routeHost} />
          </WorldFocusDanteConversationPresentationController>
        </D3ConversationOwner>
      </WorldFocusDanteEntryProvider>
    </WorldFocusWorkspaceAllocationProvider>
  );
}

function renderD3(
  reader?: WorldFocusDanteConversationReader,
  width = 1280,
) {
  const readerProps = reader === undefined ? {} : { reader };
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <D3Harness width={width} {...readerProps} />
    </WorldFocusWorkspaceHost>,
  );
}

function openAndSubmit(input = 'Perché questo progetto è in pausa?') {
  const invoke = screen.getByRole('button', {
    name: 'Apri DANTE per il Mondo Musica',
  });
  fireEvent.click(invoke);
  const textarea = screen.getByRole('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  fireEvent.change(textarea, { target: { value: input } });
  fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));
  return invoke;
}

describe('World Focus D3 deterministic conversation bridge', () => {
  it('atomically hands the composer request to one conversation, preserves user input and commits one typed local assistant output', async () => {
    renderD3();

    const invoke = openAndSubmit();

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
    expect(screen.getByText('Perché questo progetto è in pausa?')).toBeTruthy();

    await waitFor(() => {
      expect(
        screen.getByText(
          'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
        ),
      ).toBeTruthy();
    });
    const response = document.querySelector('[data-world-focus-dante-response="true"]');
    expect(response?.getAttribute('data-world-focus-dante-result-class')).toBe(
      'explanation',
    );
    expect(invoke.getAttribute('disabled')).not.toBeNull();
  });

  it('treats an active conversation as the existing DANTE interaction and cannot open a second composer beside it', async () => {
    renderD3();

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

  it('supports a second deterministic turn without changing conversation surface identity', async () => {
    renderD3();
    openAndSubmit('Prima domanda');

    await screen.findByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    );
    const followUp = screen.getByRole('textbox', {
      name: 'Continua la conversazione',
    });
    fireEvent.change(followUp, { target: { value: 'Seconda domanda' } });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));

    await waitFor(() => {
      expect(screen.getAllByText('Seconda domanda')).toHaveLength(1);
      expect(
        document.querySelectorAll('[data-world-focus-dante-response="true"]'),
      ).toHaveLength(2);
    });
    expect(screen.getByTestId('surface-count').textContent).toBe('1');
  });

  it('cancels a pending local request, preserves the user turn and ignores a late result', async () => {
    const pending = deferred<WorldFocusDanteConversationReadResult>();
    const observed: {
      request?: WorldFocusDanteConversationRequest;
      signal?: AbortSignal;
    } = {};
    const reader: WorldFocusDanteConversationReader = (request, signal) => {
      observed.request = request;
      if (signal !== undefined) observed.signal = signal;
      return pending.promise;
    };
    renderD3(reader);

    openAndSubmit('Non perdere questa richiesta');
    const cancel = await screen.findByRole('button', {
      name: 'Annulla richiesta',
    });
    fireEvent.click(cancel);

    await waitFor(() => {
      expect(
        screen.getByText(
          'Richiesta annullata. Nessuna risposta è stata aggiunta.',
        ),
      ).toBeTruthy();
    });
    expect(observed.signal?.aborted).toBe(true);
    expect(screen.getByText('Non perdere questa richiesta')).toBeTruthy();

    if (observed.request === undefined) {
      throw new Error('Expected captured D3 request');
    }
    pending.resolve(readyResult(observed.request, 'Risposta troppo tardi'));
    await Promise.resolve();
    await Promise.resolve();

    expect(screen.queryByText('Risposta troppo tardi')).toBeNull();
    expect(
      document.querySelectorAll('[data-world-focus-dante-response="true"]'),
    ).toHaveLength(0);
  });

  it('supersedes a pending request when workspace generation changes and never attaches the old result', async () => {
    const pending = deferred<WorldFocusDanteConversationReadResult>();
    const observed: {
      request?: WorldFocusDanteConversationRequest;
      signal?: AbortSignal;
    } = {};
    const reader: WorldFocusDanteConversationReader = (request, signal) => {
      observed.request = request;
      if (signal !== undefined) observed.signal = signal;
      return pending.promise;
    };
    renderD3(reader);

    openAndSubmit('Richiesta sulla generazione zero');
    await screen.findByRole('button', { name: 'Annulla richiesta' });
    fireEvent.click(screen.getByRole('button', { name: 'Change generation' }));

    await waitFor(() => {
      expect(screen.getByTestId('workspace-generation').textContent).toBe('1');
      expect(
        screen.getByText(
          'Il contesto del Mondo è cambiato. La risposta precedente non è stata aggiunta.',
        ),
      ).toBeTruthy();
    });
    expect(observed.signal?.aborted).toBe(true);

    if (observed.request === undefined) {
      throw new Error('Expected captured D3 request');
    }
    pending.resolve(readyResult(observed.request, 'Risposta della vecchia generazione'));
    await Promise.resolve();
    await Promise.resolve();
    expect(screen.queryByText('Risposta della vecchia generazione')).toBeNull();
  });

  it('does not restore invoke focus during composer-to-conversation handoff, but restores it when the conversation actually closes', async () => {
    renderD3();

    const invoke = screen.getByRole('button', {
      name: 'Apri DANTE per il Mondo Musica',
    });
    invoke.focus();
    openAndSubmit('Apri la conversazione');

    await screen.findByRole('dialog', { name: 'Conversazione con DANTE' });
    expect(invoke).not.toBe(document.activeElement);

    await screen.findByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Chiudi conversazione DANTE' }),
    );

    await waitFor(() => {
      expect(
        screen.queryByRole('dialog', { name: 'Conversazione con DANTE' }),
      ).toBeNull();
      expect(invoke).toBe(document.activeElement);
    });
  });
});
