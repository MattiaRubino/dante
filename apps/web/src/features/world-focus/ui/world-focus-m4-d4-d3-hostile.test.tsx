import { useState, type ReactNode } from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type {
  WorldFocusDanteConversationReader,
  WorldFocusDanteConversationRequest,
} from '../application/world-focus-dante-conversation';
import { createWorldFocusContextReferenceSet } from '../model/world-focus-context-reference';
import { resolveWorldFocusWorkspaceAllocation } from '../model/world-focus-workspace-allocation';
import { getCoreWorldFocusSurfaceRegistry } from './world-focus-core-surfaces';
import { WorldFocusDanteConversationPresentationController } from './world-focus-dante-conversation';
import {
  WorldFocusDanteConversationProvider,
  useWorldFocusDanteConversation,
} from './world-focus-dante-conversation-context';
import { WorldFocusDanteContextualEntry } from './world-focus-dante-contextual-entry';
import {
  WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID,
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

const OWNED_D4_REFERENCES = createWorldFocusContextReferenceSet({
  primary: { kind: 'project', key: 'owned-d4-primary' },
  supporting: [{ kind: 'checkpoint', key: 'owned-d4-supporting' }],
});

const FORGED_SAME_GENERATION_REFERENCES = createWorldFocusContextReferenceSet({
  primary: { kind: 'project', key: 'forged-d4-primary' },
  supporting: [{ kind: 'checkpoint', key: 'forged-d4-supporting' }],
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

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

function D4ToD3BindingProbe() {
  const workspace = useWorldFocusWorkspace();
  const conversation = useWorldFocusDanteConversation();
  const [accepted, setAccepted] = useState<boolean | null>(null);

  return (
    <div>
      <output data-testid="forged-context-seed-accepted">
        {accepted === null ? 'unattempted' : String(accepted)}
      </output>
      <button
        type="button"
        onClick={() => {
          const hostileRuntimeCall = conversation.beginFromComposer as unknown as (
            composerInstanceId: string,
            input: string,
            contextSeed: unknown,
          ) => boolean;
          setAccepted(
            hostileRuntimeCall(
              WORLD_FOCUS_DANTE_COMPOSER_INSTANCE_ID,
              'Richiesta ostile con contesto sostituito',
              Object.freeze({
                references: FORGED_SAME_GENERATION_REFERENCES,
                workspaceGeneration: workspace.state.generation,
              }),
            ),
          );
        }}
      >
        Try forged D4 context seed
      </button>
    </div>
  );
}

function HostileHarness({
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
          <WorldFocusDanteContextualEntry
            intent="continue"
            contextReferences={OWNED_D4_REFERENCES}
          />
          <D4ToD3BindingProbe />
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

describe('World Focus M4 D4 to D3 hostile binding', () => {
  it('ignores a valid same-generation context seed that is not owned by the current D4 composer invocation', () => {
    const requests: WorldFocusDanteConversationRequest[] = [];
    const reader: WorldFocusDanteConversationReader = (request) => {
      requests.push(request);
      return new Promise(() => {
        // Keep the read pending; this test only proves request ownership/binding.
      });
    };

    render(
      <WorldFocusWorkspaceHost worldId="music">
        <HostileHarness reader={reader} />
      </WorldFocusWorkspaceHost>,
    );

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Chiedi a DANTE: Continua da qui',
      }),
    );
    expect(screen.getByRole('dialog', { name: 'DANTE' })).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: 'Try forged D4 context seed' }),
    );

    expect(screen.getByTestId('forged-context-seed-accepted').textContent).toBe(
      'true',
    );
    expect(requests).toHaveLength(1);
    expect(requests[0]?.contextReferences).toEqual(OWNED_D4_REFERENCES);
    expect(requests[0]?.contextReferences).not.toEqual(
      FORGED_SAME_GENERATION_REFERENCES,
    );
  });
});
