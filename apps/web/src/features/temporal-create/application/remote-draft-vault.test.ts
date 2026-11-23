import { fetchRequestUrl } from '../../../test-support/fetch-request';
import { fetchRequestBody } from '../../../test-support/fetch-request';
import { describe, expect, it, vi } from 'vitest';

import { subscribeTemporalTimelineInvalidation } from '../../temporal/timeline-invalidation';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createTemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import { createRemoteDraftVault } from './remote-draft-vault';

function response(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function resolvedResponse(body: unknown, status = 200): Promise<Response> {
  return Promise.resolve(response(body, status));
}

describe('Draft Vault remote owner boundary', () => {
  it('saves an inert Activity configuration without any product authoring call', async () => {
    const requests: Array<{
      path: string;
      method: string;
      body?: Record<string, unknown>;
    }> = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path =
        typeof input === 'string'
          ? input
          : input instanceof URL
            ? input.href
            : input.url;
      if (path.endsWith('/auth/session'))
        return resolvedResponse({
          authenticated: true,
          csrf_token: 'csrf',
        });
      if (path.endsWith('/temporal/drafts/draft-1') && init?.method === 'PUT') {
        expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('csrf');
        const body = JSON.parse(fetchRequestBody(init.body)) as Record<
          string,
          unknown
        >;
        requests.push({ path, method: init.method, body });
        return resolvedResponse({
          draft_ref: 'draft-1',
          subject_kind: 'activity',
          title: 'Allenamento',
          payload: body.payload,
          revision: 1,
          created_at: '2026-10-09T20:00:00Z',
          updated_at: '2026-10-09T20:00:00Z',
        });
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const fields = { ...createTemporalCreateFields(), title: 'Allenamento' };
    const advanced = createTemporalCreateU2AuthoringDraft(fields);
    const saved = await createRemoteDraftVault(fetchFn).save(
      {
        version: 1,
        fields,
        advanced,
        surface: 'full',
      },
      { draftRef: 'draft-1', revision: null, operationId: 'save-op' },
    );
    expect(requests).toHaveLength(1);
    expect(requests[0]?.body).toMatchObject({
      expected_revision: null,
      operation_id: 'save-op',
      subject_kind: 'activity',
      payload: {
        version: 1,
        fields: { title: 'Allenamento' },
        advanced: { activityStructure: { plannedSlices: [] } },
      },
    });
    expect(saved.revision).toBe(1);
    expect(saved.payload.fields.title).toBe('Allenamento');
    expect(
      fetchFn.mock.calls.every(
        ([path]) =>
          fetchRequestUrl(path).includes('/drafts') ||
          fetchRequestUrl(path).includes('/auth/session'),
      ),
    ).toBe(true);
  });
  it(
    'moves via a single owner-scoped atomic command, never a separate draft PUT and DELETE',
    async () => {
      const mutations: Array<{ path: string; body: Record<string, unknown> }> = [];
      const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const path = fetchRequestUrl(input);
        if (path.endsWith('/auth/session'))
          return resolvedResponse({ authenticated: true, csrf_token: 'csrf' });
        if (path.includes('/temporal/drafts/move/') && init?.method === 'POST') {
          expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('csrf');
          const body = JSON.parse(fetchRequestBody(init.body)) as Record<
            string,
            unknown
          >;
          mutations.push({ path, body });
          return resolvedResponse({
            draft_ref: body.draft_ref,
            subject_kind: body.subject_kind,
            title: body.title,
            payload: body.payload,
            revision: 1,
            created_at: '2026-10-09T20:00:00Z',
            updated_at: '2026-10-09T20:00:00Z',
          });
        }
        throw new Error(`Unexpected request: ${path}`);
      });
      const fields = { ...createTemporalCreateFields(), title: 'Allenamento' };
      const snapshot = {
        version: 1 as const,
        fields,
        advanced: createTemporalCreateU2AuthoringDraft(fields),
        surface: 'full' as const,
      };
      const order: string[] = [];
      const unsubscribe = subscribeTemporalTimelineInvalidation(() => {
        order.push('timeline-invalidate');
      });
      const moved = await createRemoteDraftVault(fetchFn).move(
        snapshot,
        'activity-1',
        'a'.repeat(64),
        7,
        () => order.push('committed-local-removal'),
      );
      unsubscribe();
      expect(order).toEqual(['committed-local-removal', 'timeline-invalidate']);
      expect(mutations).toHaveLength(1);
      expect(mutations[0]).toMatchObject({
        path: expect.stringContaining('/drafts/move/activity-1'),
        body: {
          subject_kind: 'activity',
          expected_revision: null,
          expected_fingerprint: 'a'.repeat(64),
          expected_profile_revision: 7,
          payload: { version: 1, fields: { title: 'Allenamento' } },
        },
      });
      expect(moved.subjectKind).toBe('activity');
      expect(
        fetchFn.mock.calls.filter(([, init]) => init?.method === 'DELETE'),
      ).toHaveLength(0);
    },
  );

  it.each([
    { status: 409, expected: 'sono cambiati' },
    { status: 500, expected: 'L’originale è rimasto invariato' },
  ])(
    'never removes or invalidates an Event on a failed atomic move ($status)',
    async ({ status, expected }) => {
      const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
        const path = fetchRequestUrl(input);
        if (path.endsWith('/auth/session')) {
          return resolvedResponse({ authenticated: true, csrf_token: 'csrf' });
        }
        if (path.includes('/temporal/drafts/move/') && init?.method === 'POST') {
          return resolvedResponse({ error: 'move rejected' }, status);
        }
        throw new Error(`Unexpected request: ${path}`);
      });
      const fields = createTemporalCreateFields({
        kind: 'event',
        title: 'Visita',
      });
      const snapshot = {
        version: 1 as const,
        fields,
        advanced: createTemporalCreateU2AuthoringDraft(fields),
        surface: 'full' as const,
      };
      const effects: string[] = [];
      const unsubscribe = subscribeTemporalTimelineInvalidation(() => {
        effects.push('timeline-invalidate');
      });
      try {
        await expect(
          createRemoteDraftVault(fetchFn).move(
            snapshot,
            'event-1',
            'a'.repeat(64),
            null,
            () => effects.push('committed-local-removal'),
          ),
        ).rejects.toThrow(expected);
      } finally {
        unsubscribe();
      }
      expect(effects).toEqual([]);
      expect(
        fetchFn.mock.calls.filter(([, init]) => init?.method === 'POST'),
      ).toHaveLength(1);
      expect(
        fetchFn.mock.calls.filter(
          ([, init]) => init?.method === 'DELETE' || init?.method === 'PUT',
        ),
      ).toHaveLength(0);
    },
  );

  it('does not announce a committed move when the success receipt is invalid', async () => {
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = fetchRequestUrl(input);
      if (path.endsWith('/auth/session')) {
        return resolvedResponse({ authenticated: true, csrf_token: 'csrf' });
      }
      if (path.includes('/temporal/drafts/move/') && init?.method === 'POST') {
        // A successful HTTP status is not a validated committed Draft receipt.
        return resolvedResponse({ draft_ref: 'new-draft', subject_kind: 'event' });
      }
      throw new Error(`Unexpected request: ${path}`);
    });
    const fields = createTemporalCreateFields({
      kind: 'event',
      title: 'Visita',
    });
    const snapshot = {
      version: 1 as const,
      fields,
      advanced: createTemporalCreateU2AuthoringDraft(fields),
      surface: 'full' as const,
    };
    const effects: string[] = [];
    const unsubscribe = subscribeTemporalTimelineInvalidation(() => {
      effects.push('timeline-invalidate');
    });
    try {
      await expect(
        createRemoteDraftVault(fetchFn).move(
          snapshot,
          'event-1',
          'a'.repeat(64),
          null,
          () => effects.push('committed-local-removal'),
        ),
      ).rejects.toThrow('La bozza salvata non è compatibile con questo editor.');
    } finally {
      unsubscribe();
    }
    expect(effects).toEqual([]);
  });
});
