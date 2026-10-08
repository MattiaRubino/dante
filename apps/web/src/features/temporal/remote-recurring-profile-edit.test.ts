import { describe, expect, it, vi } from 'vitest';

import { createRemoteRecurringProfileEdit } from './remote-recurring-profile-edit';

const activityRef = '0199a111-1111-7111-8111-111111111111';
const occurrenceRef = '0199a222-2222-7222-8222-222222222222';
const sourceRef = '0199a333-3333-7333-8333-333333333333';
const recurrenceStateRef = '0199a444-4444-7444-8444-444444444444';

const response = (value: unknown, status = 200): Response =>
  new Response(JSON.stringify(value), {
    status, headers: { 'Content-Type': 'application/json' },
  });

describe('Recurring Activity metadata edit remote contract', () => {
  it('uses canonical origin/state and a single idempotent scoped POST', async () => {
    const requests: Record<string, unknown>[] = [];
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const path = typeof input === 'string' ? input :
          input instanceof URL ? input.href : input.url;
        if (path.endsWith('/recurrence-origin')) return Promise.resolve(response({
          activity_ref: activityRef, occurrence_ref: occurrenceRef,
        }));
        if (path.endsWith('/profile-edit-state')) return Promise.resolve(response({
          selected_occurrence_ref: occurrenceRef,
          source_native_ref: sourceRef,
          edit_revision: 4,
          recurrence_state_ref: recurrenceStateRef,
          current_profile_patch: {},
        }));
        if (path.endsWith('/auth/session')) return Promise.resolve(response({
          authenticated: true, csrf_token: 'csrf-token',
        }));
        if (path.endsWith('/profile-edit') && init?.method === 'POST') {
          expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('csrf-token');
          requests.push(JSON.parse(String(init.body)) as Record<string, unknown>);
          return Promise.resolve(response({
            revision: 5,
            source_native_ref: sourceRef,
            selected_occurrence_ref: occurrenceRef,
            target_occurrence_refs: [occurrenceRef],
            accepted_at: '2026-10-08T12:00:00Z',
            replayed: false,
          }));
        }
        if (path.endsWith('/profile')) return Promise.resolve(response({
          activity_ref: activityRef, title: 'Nuovo titolo',
          description: null, location: 'Milano', color_code: '#ABCDEF',
          revision: 0,
        }));
        throw new Error(`Unexpected endpoint: ${path}`);
      },
    );
    const remote = createRemoteRecurringProfileEdit(fetchFn);
    const context = await remote.loadActivityContext(activityRef);
    expect(context).toEqual({
      occurrenceRef, sourceRef, editRevision: 4, recurrenceStateRef,
    });
    if (!context) throw new Error('Expected recurring context');
    const next = await remote.saveActivityProfile(
      activityRef, context, 'this_and_following',
      { title: 'Nuovo titolo', description: null, location: 'Milano',
        colorCode: '#ABCDEF' }, 'operation-1',
    );
    expect(next.title).toBe('Nuovo titolo');
    expect(requests).toEqual([{
      operation_id: 'operation-1',
      expected_revision: 4,
      expected_recurrence_state_ref: recurrenceStateRef,
      scope_code: 'this_and_following',
      profile_patch: { title: 'Nuovo titolo', description: null,
        location: 'Milano', color_code: '#ABCDEF' },
    }]);
    expect(fetchFn).toHaveBeenCalledTimes(5);
  });

  it('does not present a recurrence scope for a one-off Activity', async () => {
    const fetchFn = vi.fn(() => Promise.resolve(response({
      activity_ref: activityRef, occurrence_ref: null,
    })));
    const remote = createRemoteRecurringProfileEdit(fetchFn);
    expect(await remote.loadActivityContext(activityRef)).toBeNull();
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('does not treat a conflict as success and does not re-read a false result', async () => {
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const path = typeof input === 'string' ? input :
          input instanceof URL ? input.href : input.url;
        if (path.endsWith('/auth/session')) return Promise.resolve(response({
          authenticated: true, csrf_token: 'token',
        }));
        if (path.endsWith('/profile-edit') && init?.method === 'POST') {
          return Promise.resolve(response({ code: 'temporal.recurrence_edit.conflict' }, 409));
        }
        throw new Error(`Unexpected call ${path}`);
      },
    );
    const remote = createRemoteRecurringProfileEdit(fetchFn);
    await expect(remote.saveActivityProfile(
      activityRef, { occurrenceRef, sourceRef, editRevision: 4, recurrenceStateRef },
      'only_this', { title: 'Corretto', description: null,
        location: null, colorCode: null }, 'same-op',
    )).rejects.toThrow('ricorrenza');
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });
});
