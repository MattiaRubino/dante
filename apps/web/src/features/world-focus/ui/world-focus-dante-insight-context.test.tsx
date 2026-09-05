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
import {
  WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
  type WorldFocusDanteInsightReader,
  type WorldFocusDanteInsightRequest,
  type WorldFocusDanteInsightReadResult,
} from '../application/world-focus-dante-insight';
import { createWorldFocusContextReferenceSet } from '../model/world-focus-context-reference';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import { WorldFocusDanteConversationPresentationController } from './world-focus-dante-conversation';
import { WorldFocusDanteConversationProvider } from './world-focus-dante-conversation-context';
import { WorldFocusDanteContextualEntry } from './world-focus-dante-contextual-entry';
import {
  WorldFocusDanteEntryProvider,
  WorldFocusDanteInvoke,
  useWorldFocusDanteEntry,
} from './world-focus-dante-entry';
import { WorldFocusDanteInsightProvider } from './world-focus-dante-insight-context';
import { WorldFocusRouteSurfaceLayer } from './world-focus-route-surface-layer';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

const CONTEXTUAL_REFERENCES = createWorldFocusContextReferenceSet({
  primary: { kind: 'project', key: 'secret-primary-key' },
  supporting: [{ kind: 'checkpoint', key: 'secret-supporting-key' }],
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

function conversationResult(
  request: WorldFocusDanteConversationRequest,
  output: string,
) {
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

function insightResult(
  request: WorldFocusDanteInsightRequest,
): WorldFocusDanteInsightReadResult {
  return Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
    status: 'ready' as const,
    requestId: request.requestId,
    worldId: request.worldId,
    workspaceGeneration: request.workspaceGeneration,
    insight: Object.freeze({
      schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
      insightId: `${request.sourceMessageId}:insight`,
      worldId: request.worldId,
      workspaceGeneration: request.workspaceGeneration,
      kind: 'observation' as const,
      title: 'Insight contestuale',
      summary: request.sourceText,
      basisReferences: request.contextReferences,
    }),
  });
}

function ConversationOwner({
  reader,
  children,
}: Readonly<{
  reader: WorldFocusDanteConversationReader;
  children: ReactNode;
}>) {
  const { restoreInvokerFocus } = useWorldFocusDanteEntry();

  return (
    <WorldFocusDanteConversationProvider
      worldId="music"
      restoreInvokerFocus={restoreInvokerFocus}
      reader={reader}
    >
      {children}
    </WorldFocusDanteConversationProvider>
  );
}

type InsightHarnessMode = 'contextual' | 'global';

function InsightHarness({
  conversationReader,
  insightReader,
  mode,
}: Readonly<{
  conversationReader: WorldFocusDanteConversationReader;
  insightReader: WorldFocusDanteInsightReader;
  mode: InsightHarnessMode;
}>) {
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
        <ConversationOwner reader={conversationReader}>
          <WorldFocusDanteInsightProvider
            worldId="music"
            reader={insightReader}
          >
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
            {mode === 'contextual' ? (
              <WorldFocusDanteContextualEntry
                intent="continue"
                contextReferences={CONTEXTUAL_REFERENCES}
              />
            ) : (
              <WorldFocusDanteInvoke />
            )}
            <div ref={setRouteHost} />
            <WorldFocusDanteConversationPresentationController>
              <WorldFocusSurfaceLayer registry={registry} />
              <WorldFocusRouteSurfaceLayer registry={registry} host={routeHost} />
            </WorldFocusDanteConversationPresentationController>
          </WorldFocusDanteInsightProvider>
        </ConversationOwner>
      </WorldFocusDanteEntryProvider>
    </WorldFocusWorkspaceAllocationProvider>
  );
}

function renderHarness(
  conversationReader: WorldFocusDanteConversationReader,
  insightReader: WorldFocusDanteInsightReader,
  mode: InsightHarnessMode = 'contextual',
) {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <InsightHarness
        conversationReader={conversationReader}
        insightReader={insightReader}
        mode={mode}
      />
    </WorldFocusWorkspaceHost>,
  );
}

function readyConversationReader(
  output = 'Risposta contestuale pronta',
): WorldFocusDanteConversationReader {
  return (request) => Promise.resolve(conversationResult(request, output));
}

async function openContextualConversation() {
  fireEvent.click(
    screen.getByRole('button', {
      name: 'Chiedi a DANTE: Continua da qui',
    }),
  );
  fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));
  await screen.findByText('Risposta contestuale pronta');
  return screen.getByRole('button', { name: 'Apri come Insight' });
}

describe('World Focus D5 standalone Insight ownership', () => {
  it('materializes a validated Insight without exposing bounded reference keys and restores the exact logical invoker on close', async () => {
    const insightRequests: WorldFocusDanteInsightRequest[] = [];
    const insightReader: WorldFocusDanteInsightReader = (request) => {
      insightRequests.push(request);
      return Promise.resolve(insightResult(request));
    };
    renderHarness(readyConversationReader(), insightReader);

    const invoker = await openContextualConversation();
    invoker.focus();
    fireEvent.click(invoker);

    const dialog = await screen.findByRole('dialog', {
      name: 'Insight contestuale',
    });
    expect(insightRequests).toHaveLength(1);
    expect(insightRequests[0]?.contextReferences).toEqual(CONTEXTUAL_REFERENCES);
    expect(dialog.textContent).toContain('Riferimenti contestuali espliciti: 2.');
    expect(dialog.textContent).not.toContain('secret-primary-key');
    expect(dialog.textContent).not.toContain('secret-supporting-key');
    expect(
      screen.queryByRole('button', { name: 'Invia richiesta' }),
    ).toBeNull();

    fireEvent.click(
      screen.getByRole('button', { name: 'Chiudi Insight DANTE' }),
    );
    await waitFor(() => {
      expect(
        screen.queryByRole('dialog', { name: 'Insight contestuale' }),
      ).toBeNull();
      expect(invoker).toBe(document.activeElement);
    });
  });

  it('does not let a late Insight result attach after the workspace generation changes', async () => {
    let resolveInsight:
      | ((result: WorldFocusDanteInsightReadResult) => void)
      | undefined;
    let capturedRequest: WorldFocusDanteInsightRequest | undefined;
    const insightReader: WorldFocusDanteInsightReader = (request) => {
      capturedRequest = request;
      return new Promise((resolve) => {
        resolveInsight = resolve;
      });
    };
    renderHarness(readyConversationReader(), insightReader);

    const invoker = await openContextualConversation();
    fireEvent.click(invoker);
    expect(
      await screen.findByText('Preparazione locale dell’Insight in corso.'),
    ).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Change generation' }));
    await waitFor(() => {
      expect(screen.getByTestId('workspace-generation').textContent).toBe('1');
      expect(
        screen.getByText(
          'Il contesto del Mondo è cambiato. L’Insight non è stato aperto.',
        ),
      ).toBeTruthy();
    });

    if (capturedRequest === undefined || resolveInsight === undefined) {
      throw new Error('Expected deferred D5 Insight request');
    }
    resolveInsight(insightResult(capturedRequest));
    await Promise.resolve();
    await Promise.resolve();

    expect(
      screen.queryByRole('dialog', { name: 'Insight contestuale' }),
    ).toBeNull();
  });

  it('never offers Insight promotion for a global DANTE conversation without explicit contextual references', async () => {
    const insightReader: WorldFocusDanteInsightReader = (request) =>
      Promise.resolve(insightResult(request));
    renderHarness(
      readyConversationReader('Risposta globale pronta'),
      insightReader,
      'global',
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Apri DANTE per il Mondo Musica' }),
    );
    const composer = screen.getByRole<HTMLTextAreaElement>('textbox', {
      name: 'Scrivi una richiesta per DANTE',
    });
    fireEvent.change(composer, { target: { value: 'Domanda globale' } });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));

    expect(await screen.findByText('Risposta globale pronta')).toBeTruthy();
    expect(
      screen.queryByRole('button', { name: 'Apri come Insight' }),
    ).toBeNull();
  });
});
