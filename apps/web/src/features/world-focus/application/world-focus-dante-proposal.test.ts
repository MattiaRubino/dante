import { describe, expect, it } from 'vitest';

import { WorldFocusBoundaryValidationError } from './world-focus-foundation';
import {
  createWorldFocusDanteProposalReader,
  createWorldFocusDanteProposalRequest,
  WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
} from './world-focus-dante-proposal';

function createRequest() {
  return createWorldFocusDanteProposalRequest({
    requestId: 'proposal-request-1',
    worldId: 'music',
    workspaceGeneration: 4,
    sourceInsightId: 'insight-1',
    sourceInsightKind: 'observation',
    sourceTitle: 'Insight contestuale',
    sourceSummary: 'Una lettura bounded da cui preparare un prossimo passo.',
    locale: 'it-IT',
    contextReferences: {
      primary: { kind: 'continuity', key: 'secret-primary' },
      supporting: [{ kind: 'project', key: 'secret-supporting' }],
    },
  });
}

function readyResult(request: ReturnType<typeof createRequest>) {
  return {
    schemaVersion: WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
    status: 'ready',
    requestId: request.requestId,
    worldId: request.worldId,
    workspaceGeneration: request.workspaceGeneration,
    proposalId: 'proposal-1',
    title: 'Proposta contestuale',
    targetLabel: 'Prossimo passo',
    changeSummary: 'Rivedi il prossimo passo da questo Insight.',
  } as const;
}

describe('World Focus D6 Proposal boundary', () => {
  it('keeps the validated Insight source distinct from the Proposal artifact and requires explicit confirmation', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteProposalReader({
      read: ({ request: current }) => Promise.resolve(readyResult(current)),
    });

    const result = await reader(request);
    expect(result.status).toBe('ready');
    if (result.status !== 'ready') {
      throw new Error('Expected ready Proposal result');
    }

    expect(result.proposal.sourceInsightId).toBe(request.sourceInsightId);
    expect(result.proposal.proposalId).not.toBe(request.sourceInsightId);
    expect(result.proposal.decisionRequirement).toBe('explicit-confirmation');
    expect(result.proposal.basisReferences).toEqual(request.contextReferences);
    expect(result.proposal).not.toHaveProperty('decision');
    expect(result.proposal).not.toHaveProperty('effect');
    expect(result.proposal).not.toHaveProperty('providerCompletion');
  });

  it('fails closed when the adapter tries to widen Proposal into Decision, effect, completion or adapter-owned basis', async () => {
    const request = createRequest();

    for (const extra of [
      { decision: 'confirmed' },
      { effect: 'completed' },
      { providerCompletion: true },
      {
        basisReferences: {
          primary: { kind: 'forged', key: 'forged' },
          supporting: [],
        },
      },
    ]) {
      const reader = createWorldFocusDanteProposalReader({
        read: () => Promise.resolve({ ...readyResult(request), ...extra }),
      });

      await expect(reader(request)).rejects.toBeInstanceOf(
        WorldFocusBoundaryValidationError,
      );
    }
  });

  it('fails closed on request, World or generation correlation drift', async () => {
    const request = createRequest();

    for (const drift of [
      { requestId: 'wrong-request' },
      { worldId: 'travel' },
      { workspaceGeneration: request.workspaceGeneration + 1 },
    ]) {
      const reader = createWorldFocusDanteProposalReader({
        read: () => Promise.resolve({ ...readyResult(request), ...drift }),
      });

      await expect(reader(request)).rejects.toBeInstanceOf(
        WorldFocusBoundaryValidationError,
      );
    }
  });

  it('relays cancellation without manufacturing a Proposal result', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteProposalReader({
      read: ({ signal }) =>
        new Promise((_, reject) => {
          signal.addEventListener(
            'abort',
            () => {
              const error = new Error('aborted');
              error.name = 'AbortError';
              reject(error);
            },
            { once: true },
          );
        }),
    });
    const controller = new AbortController();
    const pending = reader(request, controller.signal);
    controller.abort();

    await expect(pending).rejects.toMatchObject({ name: 'AbortError' });
  });
});
