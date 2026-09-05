import type { WorldFocusDanteProposalReadAdapter } from './world-focus-dante-proposal';
import { WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION } from './world-focus-dante-proposal';

function createAbortError(): Error {
  const error = new Error('World Focus DANTE Proposal fixture read aborted');
  error.name = 'AbortError';
  return error;
}

function clampChangeSummary(prefix: string, sourceSummary: string): string {
  const available = Math.max(0, 2_000 - prefix.length);
  return `${prefix}${sourceSummary.slice(0, available)}`;
}

/**
 * Deterministic pre-backend D6 fixture. It materializes only a candidate-change
 * Proposal presentation artifact. It performs no model call, authorization,
 * persistence, provider operation or effect execution.
 */
export const worldFocusDanteProposalFixtureAdapter: WorldFocusDanteProposalReadAdapter =
  Object.freeze({
    read: async ({ request, signal }) => {
      await Promise.resolve();
      if (signal.aborted) throw createAbortError();

      const italian = request.locale.toLowerCase().startsWith('it');
      const prefix = italian
        ? 'Rivedi il prossimo passo usando questo Insight come base: '
        : 'Review the next step using this Insight as its basis: ';

      return Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
        status: 'ready' as const,
        requestId: request.requestId,
        worldId: request.worldId,
        workspaceGeneration: request.workspaceGeneration,
        proposalId: `${request.sourceInsightId}:proposal`,
        title: italian ? 'Proposta contestuale' : 'Contextual proposal',
        targetLabel: italian ? 'Prossimo passo' : 'Next step',
        changeSummary: clampChangeSummary(prefix, request.sourceSummary),
      });
    },
  });
