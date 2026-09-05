import type { WorldFocusDanteConversationReadAdapter } from './world-focus-dante-conversation';
import { WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION } from './world-focus-dante-conversation';

function createAbortError(): Error {
  const error = new Error('World Focus DANTE fixture read aborted');
  error.name = 'AbortError';
  return error;
}

/**
 * Deterministic pre-backend adapter. It proves the conversation lifecycle
 * without pretending to run a model, inspect sources, authorize context or
 * perform any tool/effect work.
 */
export const worldFocusDanteConversationFixtureAdapter: WorldFocusDanteConversationReadAdapter =
  Object.freeze({
    read: async ({ request, signal }) => {
      await Promise.resolve();
      if (signal.aborted) throw createAbortError();

      const italian = request.locale.toLowerCase().startsWith('it');
      return Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
        status: 'ready' as const,
        requestId: request.requestId,
        worldId: request.worldId,
        workspaceGeneration: request.workspaceGeneration,
        resultClass: 'explanation' as const,
        output: italian
          ? 'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.'
          : 'Local mode: request received. No model or external source was queried.',
      });
    },
  });
