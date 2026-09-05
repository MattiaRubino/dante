import { useState, type ReactNode } from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import {
  WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
  type WorldFocusDanteConversationReader,
  type WorldFocusDanteConversationRequest,
} from '../application/world-focus-dante-conversation';
import type {
  WorldFocusDanteInsightReader,
  WorldFocusDanteInsightRequest,
} from '../application/world-focus-dante-insight';
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
import {
  WorldFocusDanteInsightProvider,
  useWorldFocusDanteInsight,
} from './world-focus-dante-insight-context';
import { WorldFocusRouteSurfaceLayer } from './world-focus-route-surface-layer';
import { WorldFocusSurfaceLayer } from './world-focus-surface-layer';
import { WorldFocusWorkspaceAllocationProvider } from './world-focus-workspace-allocation-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

const CONTEXTUAL_REFERENCES = createWorldFocusContextReferenceSet({
  primary: { kind: 'project', key: 'd3-d5-primary' },
  supporting: [{ kind: 'checkpoint', key: 'd3-d5-supporting' }],
});

const FORGED_SAME_GENERATION_MESSAGE_ID = 'forged-same-generation-assistant';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

function conversationResult(request: WorldFocusDanteConversationRequest) {
  return Object.freeze({
    schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
    status: 'ready' as const,
    requestId: request.requestId,
    worldId: request.worldId,
    workspaceGeneration: request.workspaceGeneration,
    resultClass: 'explanation' as const,
    output: 'Risposta D3 reale pronta',
  });
}

const conversationReader: WorldFocusDanteConversationReader = (request) =>
  Promise.resolve(conversationResult(request));

function ConversationOwner({ children }: Readonly<{ children: ReactNode }>) {
  const { restoreInvokerFocus } = useWorldFocusDanteEntry();

  return (
    <WorldFocusDanteConversationProvider
      worldId="music"
      restoreInvokerFocus={restoreInvokerFocus}
      reader={conversationReader}
    >
      {children}
    </WorldFocusDanteConversationProvider>
  );
}

function D3ToD5BindingProbe() {
  const insight = useWorldFocusDanteInsight();
  const [accepted, setAccepted] = useState<boolean | null>(null);

  return (
    <div>
      <output data-testid="forged-insight-accepted">
        {accepted === null ? 'unattempted' : String(accepted)}
      </output>
      <button
        type="button"
        onClick={() =>
          setAccepted(
            insight.requestInsight(FORGED_SAME_GENERATION_MESSAGE_ID),
          )
        }
      >
        Try forged D5 Insight
      </button>
    </div>
  );
}

function HostileHarness({
  insightReader,
}: Readonly<{ insightReader: WorldFocusDanteInsightReader }>) {
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
        <ConversationOwner>
          <WorldFocusDanteInsightProvider
            worldId="music"
            reader={insightReader}
          >
            <WorldFocusDanteContextualEntry
              intent="continue"
              contextReferences={CONTEXTUAL_REFERENCES}
            />
            <D3ToD5BindingProbe />
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

describe('World Focus M4 D3 to D5 hostile binding', () => {
  it('rejects a fabricated same-generation assistant message id that is not owned by the current D3 conversation', async () => {
    const insightRequests: WorldFocusDanteInsightRequest[] = [];
    const insightReader: WorldFocusDanteInsightReader = (request) => {
      insightRequests.push(request);
      return new Promise(() => {
        // The hostile contract expects D5 to reject before any Insight read starts.
      });
    };

    render(
      <WorldFocusWorkspaceHost worldId="music">
        <HostileHarness insightReader={insightReader} />
      </WorldFocusWorkspaceHost>,
    );

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Chiedi a DANTE: Continua da qui',
      }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));
    expect(await screen.findByText('Risposta D3 reale pronta')).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: 'Try forged D5 Insight' }),
    );

    expect(screen.getByTestId('forged-insight-accepted').textContent).toBe(
      'false',
    );
    expect(insightRequests).toHaveLength(0);
  });
});
