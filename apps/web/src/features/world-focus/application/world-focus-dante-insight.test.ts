import { describe, expect, it } from 'vitest';

import { WorldFocusBoundaryValidationError } from './world-focus-foundation';
import {
  createWorldFocusDanteInsightReader,
  createWorldFocusDanteInsightRequest,
  WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
} from './world-focus-dante-insight';

function createRequest() {
  return createWorldFocusDanteInsightRequest({
    requestId: 'insight-request-1',
    worldId: 'music',
    workspaceGeneration: 3,
    sourceMessageId: 'assistant-7',
    sourceResultClass: 'explanation',
    sourceText: 'A bounded assistant explanation.',
    locale: 'it-IT',
    contextReferences: {
      primary: { kind: 'continuity', key: 'secret-primary' },
      supporting: [{ kind: 'project', key: 'secret-supporting' }],
    },
  });
}

describe('World Focus D5 standalone Insight boundary', () => {
  it('requires an explicit bounded context and keeps conversation source fields distinct from the Insight artifact', () => {
    const request = createRequest();

    expect(request).toEqual({
      schemaVersion: WORLD_FOCUS_DANTE_INSIGHT_SCHEMA_VERSION,
      requestId: 'insight-request-1',
      worldId: 'music',
      workspaceGeneration: 3,
      sourceMessageId: 'assistant-7',
      sourceResultClass: 'explanation',
      sourceText: 'A bounded assistant explanation.',
      locale: 'it-IT',
      contextReferences: {
        primary: { kind: 'continuity', key: 'secret-primary' },
        supporting: [{ kind: 'project', key: 'secret-supporting' }],
      },
    });
    expect('insightId' in request).toBe(false);
    expect('proposal' in request).toBe(false);
    expect('decision' in request).toBe(false);
    expect('effect' in request).toBe(false);
  });

  it('reconstructs the Insight basis from the request instead of accepting adapter-owned references', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteInsightReader({
      read: () =>
        Promise.resolve({
          schemaVersion: 1,
          status: 'ready',
          requestId: request.requestId,
          worldId: request.worldId,
          workspaceGeneration: request.workspaceGeneration,
          insightId: 'insight-1',
          kind: 'observation',
          title: 'Insight contestuale',
          summary: 'A bounded assistant explanation.',
        }),
    });

    const result = await reader(request);
    expect(result.status).toBe('ready');
    if (result.status !== 'ready') {
      throw new Error('Expected ready Insight result');
    }
    expect(result.insight.basisReferences).toEqual(request.contextReferences);
    expect(result.insight).not.toHaveProperty('proposal');
    expect(result.insight).not.toHaveProperty('decision');
    expect(result.insight).not.toHaveProperty('effect');
  });

  it('fails closed when an adapter attempts to widen the ready Insight shape', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteInsightReader({
      read: () =>
        Promise.resolve({
          schemaVersion: 1,
          status: 'ready',
          requestId: request.requestId,
          worldId: request.worldId,
          workspaceGeneration: request.workspaceGeneration,
          insightId: 'insight-1',
          kind: 'observation',
          title: 'Insight contestuale',
          summary: 'Summary',
          basisReferences: {
            primary: { kind: 'forged', key: 'forged' },
            supporting: [],
          },
        }),
    });

    await expect(reader(request)).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });

  it('fails closed on wrong request correlation', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteInsightReader({
      read: () =>
        Promise.resolve({
          schemaVersion: 1,
          status: 'ready',
          requestId: 'wrong-request',
          worldId: request.worldId,
          workspaceGeneration: request.workspaceGeneration,
          insightId: 'insight-1',
          kind: 'observation',
          title: 'Insight contestuale',
          summary: 'Summary',
        }),
    });

    await expect(reader(request)).rejects.toBeInstanceOf(
      WorldFocusBoundaryValidationError,
    );
  });

  it('relays cancellation without manufacturing a semantic result', async () => {
    const request = createRequest();
    const reader = createWorldFocusDanteInsightReader({
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
