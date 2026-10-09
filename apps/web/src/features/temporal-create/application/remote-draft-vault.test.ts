import { describe, expect, it, vi } from 'vitest';

import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createTemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import { createRemoteDraftVault } from './remote-draft-vault';

function response(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status, headers: { 'Content-Type': 'application/json' },
  });
}

describe('Draft Vault remote owner boundary', () => {
  it('saves an inert Activity configuration without any product authoring call', async () => {
    const requests: Array<{ path: string; method: string; body?: Record<string, unknown> }> = [];
    const fetchFn = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/auth/session')) return response({
        authenticated: true, csrf_token: 'csrf',
      });
      if (path.endsWith('/temporal/drafts/draft-1') && init?.method === 'PUT') {
        expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('csrf');
        const body = JSON.parse(String(init.body)) as Record<string, unknown>;
        requests.push({ path, method: init.method, body });
        return response({
          draft_ref: 'draft-1', subject_kind: 'activity',
          title: 'Allenamento', payload: body.payload,
          revision: 1, created_at: '2026-10-09T20:00:00Z',
          updated_at: '2026-10-09T20:00:00Z',
        });
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const fields = { ...createTemporalCreateFields(), title: 'Allenamento' };
    const advanced = createTemporalCreateU2AuthoringDraft(fields);
    const saved = await createRemoteDraftVault(fetchFn).save({
      version: 1, fields, advanced, surface: 'full',
    }, { draftRef: 'draft-1', revision: null, operationId: 'save-op' });
    expect(requests).toHaveLength(1);
    expect(requests[0]?.body).toMatchObject({
      expected_revision: null, operation_id: 'save-op',
      subject_kind: 'activity',
      payload: { version: 1, fields: { title: 'Allenamento' },
        advanced: { activityStructure: { plannedSlices: [] } } },
    });
    expect(saved.revision).toBe(1);
    expect(saved.payload.fields.title).toBe('Allenamento');
    expect(fetchFn.mock.calls.every(([path]) => String(path).includes('/drafts')
      || String(path).includes('/auth/session'))).toBe(true);
  });
});
