import { useState } from 'react';
import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type { WorldFocusDanteInsight } from '../application/world-focus-dante-insight';
import type {
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

const VALIDATED_INSIGHT: WorldFocusDanteInsight = Object.freeze({
  schemaVersion: 1,
  insightId: 'validated-d5-insight',
  worldId: 'music',
  workspaceGeneration: 0,
  kind: 'observation',
  title: 'Insight validato',
  summary: 'Questo è il solo Insight D5 associato alla surface corrente.',
  basisReferences: Object.freeze({
    primary: Object.freeze({ kind: 'continuity', key: 'validated-primary' }),
    supporting: Object.freeze([]),
  }),
});

const FORGED_SAME_GENERATION_INSIGHT: WorldFocusDanteInsight = Object.freeze({
  schemaVersion: 1,
  insightId: 'forged-same-generation-insight',
  worldId: 'music',
  workspaceGeneration: 0,
  kind: 'change',
  title: 'Insight non validato',
  summary: 'Questo oggetto non è il D5 Insight associato alla surface corrente.',
  basisReferences: Object.freeze({
    primary: Object.freeze({ kind: 'continuity', key: 'forged-primary' }),
    supporting: Object.freeze([
      Object.freeze({ kind: 'project', key: 'forged-supporting' }),
    ]),
  }),
});

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

function readyProposalResult(request: WorldFocusDanteProposalRequest) {
  return Object.freeze({
    schemaVersion: 1 as const,
    status: 'ready' as const,
    requestId: request.requestId,
    worldId: request.worldId,
    workspaceGeneration: request.workspaceGeneration,
    proposal: Object.freeze({
      schemaVersion: 1 as const,
      proposalId: `${request.sourceInsightId}:proposal`,
      worldId: request.worldId,
      workspaceGeneration: request.workspaceGeneration,
      sourceInsightId: request.sourceInsightId,
      title: 'Proposta contestuale',
      targetLabel: 'Prossimo passo',
      changeSummary: 'Rivedi il prossimo passo da questo Insight.',
      decisionRequirement: 'explicit-confirmation' as const,
      basisReferences: request.contextReferences,
    }),
  });
}

function D5ToD6BindingHarness() {
  const workspace = useWorldFocusWorkspace();
  const proposal = useWorldFocusDanteProposal();
  const [proposalAccepted, setProposalAccepted] = useState<boolean | null>(null);
  const [confirmationAccepted, setConfirmationAccepted] = useState<boolean | null>(
    null,
  );
  const [decisionAccepted, setDecisionAccepted] = useState<boolean | null>(null);

  return (
    <div>
      <output data-testid="workspace-generation">
        {workspace.state.generation}
      </output>
      <output data-testid="proposal-id">
        {proposal.proposal?.proposalId ?? 'none'}
      </output>
      <output data-testid="receipt-json">
        {proposal.receipt === null ? 'none' : JSON.stringify(proposal.receipt)}
      </output>
      <output data-testid="d6-surfaces">
        {workspace.state.surfaces.map((surface) => surface.instanceId).join('|')}
      </output>
      <output data-testid="proposal-accepted">
        {proposalAccepted === null ? 'unattempted' : String(proposalAccepted)}
      </output>
      <output data-testid="confirmation-accepted">
        {confirmationAccepted === null
          ? 'unattempted'
          : String(confirmationAccepted)}
      </output>
      <output data-testid="decision-accepted">
        {decisionAccepted === null ? 'unattempted' : String(decisionAccepted)}
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
            contextReference: VALIDATED_INSIGHT.basisReferences.primary,
            expectedWorkspace: {
              worldId: workspace.state.worldId,
              generation: workspace.state.generation,
            },
          })
        }
      >
        Open validated D5 Insight surface
      </button>
      <button
        type="button"
        onClick={() => setProposalAccepted(proposal.requestProposal())}
      >
        Request D6 Proposal
      </button>
      <button
        type="button"
        onClick={() => {
          const hostileRuntimeCall = proposal.requestProposal as unknown as (
            insight: WorldFocusDanteInsight,
          ) => boolean;
          setProposalAccepted(hostileRuntimeCall(FORGED_SAME_GENERATION_INSIGHT));
        }}
      >
        Try forged D6 Proposal
      </button>
      <button
        type="button"
        onClick={() => setConfirmationAccepted(proposal.requestConfirmation())}
      >
        Request D6 Confirmation
      </button>
      <button
        type="button"
        onClick={() => setDecisionAccepted(proposal.recordDecision('confirmed'))}
      >
        Confirm D6 Decision
      </button>
      <button
        type="button"
        onClick={() => setDecisionAccepted(proposal.recordDecision('declined'))}
      >
        Decline D6 Decision
      </button>
      <button
        type="button"
        onClick={() =>
          workspace.selectContext({
            kind: 'continuity',
            key: 'hostile-generation-change',
          })
        }
      >
        Change workspace generation
      </button>
    </div>
  );
}

function renderHarness(reader: WorldFocusDanteProposalReader) {
  return render(
    <WorldFocusWorkspaceHost worldId="music">
      <WorldFocusDanteProposalProvider worldId="music" reader={reader}>
        <D5ToD6BindingHarness />
      </WorldFocusDanteProposalProvider>
    </WorldFocusWorkspaceHost>,
  );
}

function openValidatedInsightSurface() {
  fireEvent.click(
    screen.getByRole('button', { name: 'Open validated D5 Insight surface' }),
  );
}

async function materializeProposal() {
  openValidatedInsightSurface();
  fireEvent.click(screen.getByRole('button', { name: 'Request D6 Proposal' }));
  expect(screen.getByTestId('proposal-accepted').textContent).toBe('true');
  await waitFor(() =>
    expect(screen.getByTestId('proposal-id').textContent).not.toBe('none'),
  );
}

describe('World Focus M4 final hostile sequencing', () => {
  it('does not let a manually opened Insight surface substitute for a validated D5-owned Insight', () => {
    d5InsightState.current = null;
    const reader = vi.fn<WorldFocusDanteProposalReader>(
      () =>
        new Promise(() => {
          // D6 must reject before any Proposal read starts.
        }),
    );

    renderHarness(reader);
    openValidatedInsightSurface();
    fireEvent.click(screen.getByRole('button', { name: 'Request D6 Proposal' }));

    expect(screen.getByTestId('proposal-accepted').textContent).toBe('false');
    expect(reader).toHaveBeenCalledTimes(0);
    expect(screen.getByTestId('proposal-id').textContent).toBe('none');
  });

  it('refuses confirmation or decision sequencing skips before their owned predecessor exists', async () => {
    d5InsightState.current = VALIDATED_INSIGHT;
    const reader: WorldFocusDanteProposalReader = (request) =>
      Promise.resolve(readyProposalResult(request));

    renderHarness(reader);

    fireEvent.click(
      screen.getByRole('button', { name: 'Request D6 Confirmation' }),
    );
    expect(screen.getByTestId('confirmation-accepted').textContent).toBe('false');

    fireEvent.click(screen.getByRole('button', { name: 'Confirm D6 Decision' }));
    expect(screen.getByTestId('decision-accepted').textContent).toBe('false');
    fireEvent.click(screen.getByRole('button', { name: 'Decline D6 Decision' }));
    expect(screen.getByTestId('decision-accepted').textContent).toBe('false');

    await materializeProposal();
    fireEvent.click(screen.getByRole('button', { name: 'Confirm D6 Decision' }));

    expect(screen.getByTestId('decision-accepted').textContent).toBe('false');
    expect(screen.getByTestId('receipt-json').textContent).toBe('none');
    expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
      'dante:confirmation',
    );
    expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
      'dante:receipt',
    );
  });

  it('clears materialized Proposal and Confirmation after generation drift and rejects a stale decision', async () => {
    d5InsightState.current = VALIDATED_INSIGHT;
    const reader: WorldFocusDanteProposalReader = (request) =>
      Promise.resolve(readyProposalResult(request));

    renderHarness(reader);
    await materializeProposal();
    fireEvent.click(
      screen.getByRole('button', { name: 'Request D6 Confirmation' }),
    );
    expect(screen.getByTestId('confirmation-accepted').textContent).toBe('true');
    expect(screen.getByTestId('d6-surfaces').textContent).toContain(
      'dante:confirmation',
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Change workspace generation' }),
    );

    await waitFor(() => {
      expect(screen.getByTestId('workspace-generation').textContent).toBe('1');
      expect(screen.getByTestId('proposal-id').textContent).toBe('none');
      expect(screen.getByTestId('receipt-json').textContent).toBe('none');
      expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
        'dante:proposal',
      );
      expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
        'dante:confirmation',
      );
      expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
        'dante:receipt',
      );
    });

    fireEvent.click(screen.getByRole('button', { name: 'Confirm D6 Decision' }));
    expect(screen.getByTestId('decision-accepted').textContent).toBe('false');
  });

  it('clears an already materialized local Receipt after generation drift', async () => {
    d5InsightState.current = VALIDATED_INSIGHT;
    const reader: WorldFocusDanteProposalReader = (request) =>
      Promise.resolve(readyProposalResult(request));

    renderHarness(reader);
    await materializeProposal();
    fireEvent.click(
      screen.getByRole('button', { name: 'Request D6 Confirmation' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Confirm D6 Decision' }));
    expect(screen.getByTestId('decision-accepted').textContent).toBe('true');
    expect(screen.getByTestId('receipt-json').textContent).not.toBe('none');
    expect(screen.getByTestId('d6-surfaces').textContent).toContain('dante:receipt');

    fireEvent.click(
      screen.getByRole('button', { name: 'Change workspace generation' }),
    );

    await waitFor(() => {
      expect(screen.getByTestId('workspace-generation').textContent).toBe('1');
      expect(screen.getByTestId('proposal-id').textContent).toBe('none');
      expect(screen.getByTestId('receipt-json').textContent).toBe('none');
      expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
        'dante:proposal',
      );
      expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
        'dante:confirmation',
      );
      expect(screen.getByTestId('d6-surfaces').textContent).not.toContain(
        'dante:receipt',
      );
    });
  });

  it('keeps a valid Receipt an exact local decision record with no effect, authorization or completion semantics', async () => {
    d5InsightState.current = VALIDATED_INSIGHT;
    const reader: WorldFocusDanteProposalReader = (request) =>
      Promise.resolve(readyProposalResult(request));

    renderHarness(reader);
    await materializeProposal();
    fireEvent.click(
      screen.getByRole('button', { name: 'Request D6 Confirmation' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Confirm D6 Decision' }));

    expect(screen.getByTestId('decision-accepted').textContent).toBe('true');
    const receiptText = screen.getByTestId('receipt-json').textContent;
    if (receiptText === null || receiptText === 'none') {
      throw new Error('Expected a local D6 decision receipt');
    }
    const receipt = JSON.parse(receiptText) as Record<string, unknown>;
    expect(Object.keys(receipt).sort()).toEqual(
      [
        'schemaVersion',
        'receiptId',
        'proposalId',
        'worldId',
        'workspaceGeneration',
        'decision',
      ].sort(),
    );
    expect(receipt).toMatchObject({
      schemaVersion: 1,
      proposalId: `${VALIDATED_INSIGHT.insightId}:proposal`,
      worldId: 'music',
      workspaceGeneration: 0,
      decision: 'confirmed',
    });
    expect(receipt.receiptId).toBe(
      `${VALIDATED_INSIGHT.insightId}:proposal:decision:confirmed`,
    );
    for (const forbidden of [
      'effect',
      'executed',
      'providerCompletion',
      'runtimeCompletion',
      'canonicalCompletion',
      'authorization',
    ]) {
      expect(receipt).not.toHaveProperty(forbidden);
    }
  });

  it('binds D6 to the exact current validated D5 artifact even when runtime code supplies a forged same-generation Insight argument', () => {
    d5InsightState.current = VALIDATED_INSIGHT;
    let capturedRequest: WorldFocusDanteProposalRequest | undefined;
    const reader = vi.fn<WorldFocusDanteProposalReader>((request) => {
      capturedRequest = request;
      return new Promise(() => {
        // Keep the read pending; this test only proves request ownership/binding.
      });
    });

    renderHarness(reader);
    openValidatedInsightSurface();
    fireEvent.click(
      screen.getByRole('button', { name: 'Try forged D6 Proposal' }),
    );

    expect(screen.getByTestId('proposal-accepted').textContent).toBe('true');
    expect(reader).toHaveBeenCalledTimes(1);
    expect(capturedRequest).toMatchObject({
      sourceInsightId: VALIDATED_INSIGHT.insightId,
      sourceInsightKind: VALIDATED_INSIGHT.kind,
      sourceTitle: VALIDATED_INSIGHT.title,
      sourceSummary: VALIDATED_INSIGHT.summary,
      contextReferences: VALIDATED_INSIGHT.basisReferences,
    });
    expect(JSON.stringify(capturedRequest)).not.toContain(
      FORGED_SAME_GENERATION_INSIGHT.insightId,
    );
    expect(JSON.stringify(capturedRequest)).not.toContain('forged-primary');
  });
});
