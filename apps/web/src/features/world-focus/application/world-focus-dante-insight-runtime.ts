import {
  createWorldFocusDanteInsightReader,
  WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
  type WorldFocusDanteInsightReadAdapter,
} from './world-focus-dante-insight';

function createAbortError(): Error {
  const error = new Error('World Focus DANTE Insight fixture read aborted');
  error.name = 'AbortError';
  return error;
}

/**
 * Deterministic pre-backend D5 adapter. It creates only a presentation-valid
 * local Insight artifact from an explicitly selected contextual conversation
 * response. It does not inspect external sources, authorize context, run a
 * model, create a Proposal or perform any effect.
 */
export const worldFocusDanteInsightFixtureAdapter: WorldFocusDanteInsightReadAdapter =
  Object.freeze({
    read: async ({ request, signal }) => {
      await Promise.resolve();
      if (signal.aborted) throw createAbortError();

      const italian = request.locale.toLowerCase().startsWith('it');
      return Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
        status: 'ready' as const,
        requestId: request.requestId,
        worldId: request.worldId,
        workspaceGeneration: request.workspaceGeneration,
        insightId: `${request.sourceMessageId}:insight`,
        kind: 'observation' as const,
        title: italian ? 'Insight contestuale' : 'Contextual insight',
        summary: request.sourceText,
      });
    },
  });

export const readWorldFocusDanteInsight = createWorldFocusDanteInsightReader(
  worldFocusDanteInsightFixtureAdapter,
);
