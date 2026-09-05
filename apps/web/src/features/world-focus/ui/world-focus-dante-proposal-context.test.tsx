import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type { WorldFocusDanteInsight } from '../application/world-focus-dante-insight';
import type {
  WorldFocusDanteProposalReadResult,
  WorldFocusDanteProposalReader,
  WorldFocusDanteProposalRequest,
} from '../application/world-focus-dante-proposal';
import {
  WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
  WORLD_FOCUS_DANTE_INSIGHT_KIND,
} from './world-focus-dante-insight-context';
import {
  WorldFocusDanteProposalProvider,
  useWorldFocusDanteProposal,
} from './world-focus-dante-proposal-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

const d5InsightState = vi.hoisted(() => ({
  current: null as WorldFocusDanteInsight | null,
}));

vi.mock('./world-focus-dante-insight-context', async (importOriginal) => {
  const actual = await importOriginal<
    typeof import('./world-focus-dante-insight-context')
  >();
  return {
    ...actual,
    useWorldFocusDanteInsight: () => ({
      insight: d5InsightState.current,
      requestState: { status: 'idle' as const },
      isOpen: d5InsightState.current !== null,
      canRequestInsight: false,
      requestInsight: () => false,
    }),
  };
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  d5InsightState.current = null;
  cleanup();
});

function createInsight(generation: number): WorldFocusDanteInsight {
  return Object.freeze({
    schemaVersion: 1,
    insightId: `insight-${generation}`,
    worldId: 'music',
    workspaceGeneration: generation,
    kind: 'observation',
    title: 'Insight contestuale',
    summary: 'Una lettura bounded da cui preparare una proposta.',
    basisReferences: Object.freeze({
      primary: Object.freeze({ kind: 'continuity', key: 'secret-primary' }),
      supporting: Object.freeze([
        Object.freeze({ kind: 'project', key: 'secret-supporting' }),
      ]),
    }),
  });
}

function readyResult(
  request: WorldFocusDanteProposalRequest,
): WorldFocusDanteProposalReadResult {
  return Object.freeze({
    schemaVersion: 1,
    status: 'ready',
    requestId: request.requestId,
    worldId: request.worldId,
    workspaceGeneration: request.workspaceGeneration,
    proposal: Object.freeze({
      schemaVersion: 1,
      proposalId: `${request.sourceInsightId}:proposal`,
      worldId: request.worldId,
      workspaceGeneration: request.workspaceGeneration,
      sourceInsightId: request.sourceInsightId,
      title: 'Proposta contestuale',
      targetLabel: 'Prossimo passo',
      changeSummary: 'Rivedi il prossimo passo da questo Insight.',
      decisionRequirement: 'explicit-confirmation',
      basisReferences: request.contextReferences,
    }),
  });
}

function ProposalHarness() {
  const workspace = useWorldFocusWorkspace();
  const proposal = useWorldFocusDanteProposal();

  return (
    <div>
      <output data-testid="generation">{workspace.state.generation}</output>
      <output data-testid="request-status">{proposal.requestState.status}</output>
      <output data-testid="proposal-id">
        {proposal.proposal?.proposalId ?? 'none'}
      </output>
      <output data-testid="receipt-decision">
        {proposal.receipt?.decision ?? 'none'}
      </output>
      <output data-testid="surfaces">
        {workspace.state.surfaces.map((surface) => surface.instanceId).join('|')}
      </output>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
            kind: WORLD_FOCUS_DANTE_INSIGHT_KIND,
            depth: 'insight',
            presentation: 'sidecar',
            origin: 'dante',
            contextReference: { kind: 'continuity', key: 'secret-primary' },
            expectedWorkspace: {
              worldId: workspace.state.worldId,
              generation: workspace.state.generation,
            },
          })
        }
      >
        Open Insight
      </button>
      <button type="button" onClick={proposal.requestProposal}>
        Request Proposal
      </button>
      <button
        type="button"
        onClick={() =>
          workspace.selectContext({ kind: 'continuity', key: 'changed-context' })
        }
      >
        Change Context
      </button>
      <button type="button" onClick={proposal.requestConfirmation}>
        Request Confirmation
      </button>
      <button type="button" onClick={() => proposal.recordDecision('confirmed')}>
        Confirm Decision
      </button>
      <button type="button" onClick={() => proposal.recordDecision('declined')}>
        Decline Decision
      </button>
    </div>
  );
}

function renderHarness(reader: WorldFocusDanteProposalReader) {
  d5InsightState.current = createInsight(0);
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <WorldFocusDanteProposalProvider worldId="music" reader={reader}>
        <ProposalHarness />
      </WorldFocusDanteProposalProvider>
    </WorldFocusWorkspaceHost>,
  );
}

describe('World Focus D6 Proposal owner hostile lifecycle', () => {
  it('supersedes a late Proposal result after the World workspace generation changes', async () => {
    let resolveRead:
      | ((result: WorldFocusDanteProposalReadResult) => void)
      | undefined;
    let capturedRequest: WorldFocusDanteProposalRequest | undefined;
    const reader = vi.fn<WorldFocusDanteProposalReader>(
      (request) =>
        new Promise((resolve) => {
          capturedRequest = request;
          resolveRead = resolve;
        }),
    );

    renderHarness(reader);
    fireEvent.click(screen.getByRole('button', { name: 'Open Insight' }));
    fireEvent.click(screen.getByRole('button', { name: 'Request Proposal' }));
    expect(screen.getByTestId('request-status').textContent).toBe('pending');

    fireEvent.click(screen.getByRole('button', { name: 'Change Context' }));
    await waitFor(() =>
      expect(screen.getByTestId('request-status').textContent).toBe('superseded'),
    );
    expect(screen.getByTestId('generation').textContent).toBe('1');

    if (capturedRequest === undefined || resolveRead === undefined) {
      throw new Error('Expected deferred Proposal read');
    }
    resolveRead(readyResult(capturedRequest));

    await waitFor(() =>
      expect(screen.getByTestId('proposal-id').textContent).toBe('none'),
    );
    expect(screen.getByTestId('surfaces').textContent).not.toContain(
      'dante:proposal',
    );
  });

  it('records confirmed and declined as local decision receipts without adding effect semantics', async () => {
    const reader: WorldFocusDanteProposalReader = (request) =>
      Promise.resolve(readyResult(request));

    for (const decision of ['confirmed', 'declined'] as const) {
      const view = renderHarness(reader);
      fireEvent.click(screen.getByRole('button', { name: 'Open Insight' }));
      fireEvent.click(screen.getByRole('button', { name: 'Request Proposal' }));
      await waitFor(() =>
        expect(screen.getByTestId('proposal-id').textContent).not.toBe('none'),
      );

      fireEvent.click(
        screen.getByRole('button', { name: 'Request Confirmation' }),
      );
      expect(screen.getByTestId('surfaces').textContent).toContain(
        'dante:confirmation',
      );

      fireEvent.click(
        screen.getByRole('button', {
          name: decision === 'confirmed' ? 'Confirm Decision' : 'Decline Decision',
        }),
      );
      expect(screen.getByTestId('receipt-decision').textContent).toBe(decision);
      expect(screen.getByTestId('surfaces').textContent).toContain('dante:receipt');
      expect(screen.getByTestId('surfaces').textContent).not.toContain(
        'dante:confirmation',
      );

      view.unmount();
    }
  });
});
