import { describe, expect, it, vi } from 'vitest';

import { WorldFocusBoundaryValidationError } from './world-focus-foundation';
import {
  createWorldFocusDanteConversationReader,
  createWorldFocusDanteConversationRequest,
  WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
  type WorldFocusDanteConversationReadAdapter,
} from './world-focus-dante-conversation';

function createRequest() {
  return createWorldFocusDanteConversationRequest({
    requestId: 'music:local-dante:1',
    worldId: 'music',
    workspaceGeneration: 3,
    input: '  Perché questo progetto è in pausa?  ',
    history: [
      { role: 'user', text: 'Prima domanda' },
      {
        role: 'assistant',
        resultClass: 'explanation',
        text: 'Prima risposta',
      },
    ],
    locale: 'it-IT',
  });
}

describe('World Focus D3 deterministic conversation boundary', () => {
  it('normalizes only bounded transient conversation fields and does not manufacture contextual or governed authority fields', () => {
    const request = createRequest();

    expect(request).toEqual({
      schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
      requestId: 'music:local-dante:1',
      worldId: 'music',
      workspaceGeneration: 3,
      input: 'Perché questo progetto è in pausa?',
      history: [
        { role: 'user', text: 'Prima domanda' },
        {
          role: 'assistant',
          resultClass: 'explanation',
          text: 'Prima risposta',
        },
      ],
      locale: 'it-IT',
    });
    expect('contextReference' in request).toBe(false);
    expect('selection' in request).toBe(false);
    expect('authorization' in request).toBe(false);
    expect('proposal' in request).toBe(false);
    expect('tool' in request).toBe(false);
    expect('effect' in request).toBe(false);
    expect(Object.isFrozen(request)).toBe(true);
    expect(Object.isFrozen(request.history)).toBe(true);
  });

  it('accepts an exactly correlated answer/explanation result and rejects extra semantic surface', async () => {
    const request = createRequest();
    const adapter: WorldFocusDanteConversationReadAdapter = {
      read: vi.fn(() =>
        Promise.resolve({
          schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
          status: 'ready',
          requestId: request.requestId,
          worldId: request.worldId,
          workspaceGeneration: request.workspaceGeneration,
          resultClass: 'answer',
          output: 'Risposta locale',
        }),
      ),
    };
    const reader = createWorldFocusDanteConversationReader(adapter);

    await expect(reader(request)).resolves.toEqual({
      schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
      status: 'ready',
      requestId: request.requestId,
      worldId: request.worldId,
      workspaceGeneration: request.workspaceGeneration,
      resultClass: 'answer',
      output: 'Risposta locale',
    });

    const widened = createWorldFocusDanteConversationReader({
      read: () =>
        Promise.resolve({
          schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
          status: 'ready',
          requestId: request.requestId,
          worldId: request.worldId,
          workspaceGeneration: request.workspaceGeneration,
          resultClass: 'answer',
          output: 'Risposta locale',
          proposal: { action: 'mutate' },
        }),
    });

    await expect(widened(request)).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });

  it('fails closed when request, World or workspace generation correlation does not match', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteConversationReader({
      read: () =>
        Promise.resolve({
          schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
          status: 'ready',
          requestId: 'another-request',
          worldId: request.worldId,
          workspaceGeneration: request.workspaceGeneration,
          resultClass: 'explanation',
          output: 'Late answer',
        }),
    });

    await expect(reader(request)).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });

  it('relays cancellation to the adapter and never validates a late aborted result', async () => {
    const request = createRequest();
    let release: (() => void) | null = null;
    let receivedSignal: AbortSignal | null = null;
    const adapter: WorldFocusDanteConversationReadAdapter = {
      read: ({ signal }) => {
        receivedSignal = signal;
        return new Promise((resolve) => {
          release = () =>
            resolve({
              schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
              status: 'ready',
              requestId: request.requestId,
              worldId: request.worldId,
              workspaceGeneration: request.workspaceGeneration,
              resultClass: 'answer',
              output: 'Too late',
            });
        });
      },
    };
    const reader = createWorldFocusDanteConversationReader(adapter);
    const controller = new AbortController();
    const pending = reader(request, controller.signal);

    await Promise.resolve();
    controller.abort();
    release?.();

    await expect(pending).rejects.toMatchObject({ name: 'AbortError' });
    expect(receivedSignal?.aborted).toBe(true);
  });

  it('keeps unavailable as a technical result rather than fabricating assistant output', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteConversationReader({
      read: () =>
        Promise.resolve({
          schemaVersion: WORLD_FOCUS_DANTE_CONVERSATION_SCHEMA_VERSION,
          status: 'unavailable',
          requestId: request.requestId,
          worldId: request.worldId,
          workspaceGeneration: request.workspaceGeneration,
          reasonCode: 'local_unavailable',
          retryable: true,
        }),
    });

    const result = await reader(request);
    expect(result.status).toBe('unavailable');
    expect('output' in result).toBe(false);
    expect('resultClass' in result).toBe(false);
  });
});
