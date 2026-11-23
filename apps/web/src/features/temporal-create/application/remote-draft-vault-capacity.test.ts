import { describe, expect, it, vi } from 'vitest';

import { fetchRequestUrl } from '../../../test-support/fetch-request';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createTemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import {
  createRemoteDraftVault,
  DraftVaultCapacityError,
  DRAFT_VAULT_CAPACITY_MESSAGE,
} from './remote-draft-vault';

function response(body: unknown, status = 200): Promise<Response> {
  return Promise.resolve(
    new Response(JSON.stringify(body), {
      status,
      headers: { 'Content-Type': 'application/json' },
    }),
  );
}

describe('Draft Vault 100-item boundary', () => {
  it.each(['save', 'move'] as const)(
    'reports quota exhaustion for %s without falsely committing or deleting the source',
    async (operation) => {
      const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const path = fetchRequestUrl(input);
        if (path.endsWith('/auth/session')) {
          return response({ authenticated: true, csrf_token: 'csrf' });
        }
        if (
          path.includes('/temporal/drafts') &&
          (init?.method === 'PUT' || init?.method === 'POST')
        ) {
          return response(
            {
              code: 'temporal.drafts.capacity',
              detail: DRAFT_VAULT_CAPACITY_MESSAGE,
            },
            409,
          );
        }
        throw new Error(`Unexpected request: ${path}`);
      });
      const fields = createTemporalCreateFields({
        kind: 'activity',
        title: 'New activity',
      });
      const snapshot = {
        version: 1 as const,
        fields,
        advanced: createTemporalCreateU2AuthoringDraft(fields),
        surface: 'full' as const,
      };
      const committed = vi.fn();
      const source = createRemoteDraftVault(fetchFn);
      const action =
        operation === 'save'
          ? source.save(snapshot, {
              draftRef: 'draft-new',
              operationId: 'capacity:save',
              revision: null,
            })
          : source.move(snapshot, 'activity-1', 'a'.repeat(64), 1, committed);
      await expect(action).rejects.toBeInstanceOf(DraftVaultCapacityError);
      expect(committed).not.toHaveBeenCalled();
      expect(
        fetchFn.mock.calls.filter(([, init]) => init?.method === 'DELETE'),
      ).toHaveLength(0);
    },
  );

  it('keeps ordinary revision conflicts distinct from quota errors', async () => {
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = fetchRequestUrl(input);
      if (path.endsWith('/auth/session')) {
        return response({ authenticated: true, csrf_token: 'csrf' });
      }
      if (init?.method === 'PUT') {
        return response({ code: 'temporal.drafts.conflict' }, 409);
      }
      throw new Error(`Unexpected request: ${path}`);
    });
    const fields = createTemporalCreateFields({ title: 'Updated draft' });
    const source = createRemoteDraftVault(fetchFn);
    await expect(
      source.save(
        {
          version: 1,
          fields,
          advanced: createTemporalCreateU2AuthoringDraft(fields),
          surface: 'full',
        },
        { draftRef: 'existing', revision: 1, operationId: 'retry' },
      ),
    ).rejects.toThrow('La bozza è cambiata');
  });
});
