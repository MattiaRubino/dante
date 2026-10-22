import { fetchRequestBody } from '../../test-support/fetch-request';
import { describe, expect, it, vi } from 'vitest';

import { createRemoteRecurringProfileEdit } from './remote-recurring-profile-edit';
import { createRemoteRecurringSeriesEdit } from './remote-recurring-series-edit';

const activityRef = '0199a111-1111-7111-8111-111111111111';
const occurrenceRef = '0199a222-2222-7222-8222-222222222222';
const sourceRef = '0199a333-3333-7333-8333-333333333333';
const recurrenceStateRef = '0199a444-4444-7444-8444-444444444444';

const response = (value: unknown, status = 200): Response =>
  new Response(JSON.stringify(value), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

describe('Structural recurring series remote contract', () => {
  it('reviews one complete source revision and accepts only its matching fingerprint', async () => {
    const bodies: Record<string, unknown>[] = [];
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const path =
          typeof input === 'string'
            ? input
            : input instanceof URL
              ? input.href
              : input.url;
        if (path.endsWith('/series-edit-source'))
          return Promise.resolve(
            response({
              source_native_ref: sourceRef,
              owner_kind: 'event',
              selected_date: '2027-01-02',
              edit_revision: 2,
              recurrence_state_ref: recurrenceStateRef,
              title: 'Conferenza',
              description: null,
              location: null,
              color_code: null,
              recurrence: {
                family_code: 'calendar_wall_clock',
                ordinal_weekdays: [{ weekday_number: 2, ordinal: -1 }],
              },
              structure_snapshot: {
                version: 1,
                agenda_parts: ['Introduzione'],
              },
            }),
          );
        if (path.endsWith('/auth/session'))
          return Promise.resolve(
            response({ authenticated: true, csrf_token: 'csrf' }),
          );
        if (path.endsWith('/series-edit-preview')) {
          expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf');
          bodies.push(
            JSON.parse(fetchRequestBody(init?.body)) as Record<string, unknown>,
          );
          return Promise.resolve(
            response({
              source_native_ref: sourceRef,
              owner_kind: 'event',
              selected_occurrence_ref: occurrenceRef,
              target_occurrence_refs: [occurrenceRef],
              protected_occurrences: [
                {
                  occurrence_ref: '0199a555-5555-7555-8555-555555555555',
                  expected_at: '2027-01-03T08:00:00Z',
                  reason: 'registration',
                },
              ],
              new_expected_count: 1,
              fingerprint: 'a'.repeat(64),
            }),
          );
        }
        if (path.endsWith('/series-edit')) {
          bodies.push(
            JSON.parse(fetchRequestBody(init?.body)) as Record<string, unknown>,
          );
          return Promise.resolve(
            response({
              source_native_ref: sourceRef,
              recurrence_state_ref: '0199a777-7777-7777-8777-777777777777',
              superseded_count: 1,
              protected_count: 1,
            }),
          );
        }
        throw new Error(`Unexpected request ${path}`);
      },
    );
    const remote = createRemoteRecurringSeriesEdit(fetchFn);
    const source = await remote.load(occurrenceRef);
    const intent = {
      selectedRef: occurrenceRef,
      source,
      scope: 'this_and_following' as const,
      recurrence: source.recurrence,
      structure: { ...source.structure, agenda_parts: ['Nuova introduzione'] },
      profilePatch: { title: 'Nuova conferenza' },
      operationId: 'series:one',
    };
    const preview = await remote.preview(intent);
    expect(preview.protected).toHaveLength(1);
    await remote.accept(intent, preview);
    expect(bodies).toEqual([
      expect.objectContaining({
        operation_id: 'series:one',
        expected_revision: 2,
        recurrence: source.recurrence,
        structure_snapshot: intent.structure,
        profile_patch: intent.profilePatch,
      }),
      expect.objectContaining({
        operation_id: 'series:one',
        expected_preview_fingerprint: 'a'.repeat(64),
      }),
    ]);
  });
});

describe('Recurring Activity metadata edit remote contract', () => {
  it('uses canonical origin/state and a single idempotent scoped POST', async () => {
    const requests: Record<string, unknown>[] = [];
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const path =
          typeof input === 'string'
            ? input
            : input instanceof URL
              ? input.href
              : input.url;
        if (path.endsWith('/recurrence-origin'))
          return Promise.resolve(
            response({
              activity_ref: activityRef,
              occurrence_ref: occurrenceRef,
            }),
          );
        if (path.endsWith('/profile-edit-state'))
          return Promise.resolve(
            response({
              selected_occurrence_ref: occurrenceRef,
              source_native_ref: sourceRef,
              edit_revision: 4,
              recurrence_state_ref: recurrenceStateRef,
              current_profile_patch: {},
            }),
          );
        if (path.includes('/profile-edit-preview?'))
          return Promise.resolve(
            response({
              source_native_ref: sourceRef,
              edit_revision: 4,
              recurrence_state_ref: recurrenceStateRef,
              selected_protection: null,
              target_occurrence_refs: [occurrenceRef],
              protected_occurrences: [],
              fingerprint: 'a'.repeat(32),
            }),
          );
        if (path.endsWith('/auth/session'))
          return Promise.resolve(
            response({
              authenticated: true,
              csrf_token: 'csrf-token',
            }),
          );
        if (path.endsWith('/profile-edit') && init?.method === 'POST') {
          expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe(
            'csrf-token',
          );
          requests.push(
            JSON.parse(fetchRequestBody(init.body)) as Record<string, unknown>,
          );
          return Promise.resolve(
            response({
              revision: 5,
              source_native_ref: sourceRef,
              selected_occurrence_ref: occurrenceRef,
              target_occurrence_refs: [occurrenceRef],
              accepted_at: '2026-10-08T12:00:00Z',
              replayed: false,
            }),
          );
        }
        if (path.endsWith('/profile'))
          return Promise.resolve(
            response({
              activity_ref: activityRef,
              title: 'Nuovo titolo',
              description: null,
              location: 'Milano',
              color_code: '#ABCDEF',
              revision: 0,
            }),
          );
        throw new Error(`Unexpected endpoint: ${path}`);
      },
    );
    const remote = createRemoteRecurringProfileEdit(fetchFn);
    const context = await remote.loadActivityContext(activityRef);
    expect(context).toEqual({
      occurrenceRef,
      sourceRef,
      editRevision: 4,
      recurrenceStateRef,
    });
    if (!context) throw new Error('Expected recurring context');
    const preview = await remote.loadPreview(context, 'this_and_following');
    const next = await remote.saveActivityProfile(
      activityRef,
      context,
      'this_and_following',
      {
        title: 'Nuovo titolo',
        description: null,
        location: 'Milano',
        colorCode: '#ABCDEF',
      },
      'operation-1',
      preview,
    );
    expect(next.title).toBe('Nuovo titolo');
    expect(requests).toEqual([
      {
        operation_id: 'operation-1',
        expected_revision: 4,
        expected_recurrence_state_ref: recurrenceStateRef,
        scope_code: 'this_and_following',
        expected_preview_fingerprint: 'a'.repeat(32),
        profile_patch: {
          title: 'Nuovo titolo',
          description: null,
          location: 'Milano',
          color_code: '#ABCDEF',
        },
      },
    ]);
    expect(fetchFn).toHaveBeenCalledTimes(6);
  });

  it('does not present a recurrence scope for a one-off Activity', async () => {
    const fetchFn = vi.fn(() =>
      Promise.resolve(
        response({
          activity_ref: activityRef,
          occurrence_ref: null,
        }),
      ),
    );
    const remote = createRemoteRecurringProfileEdit(fetchFn);
    expect(await remote.loadActivityContext(activityRef)).toBeNull();
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('does not treat a conflict as success and does not re-read a false result', async () => {
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const path =
          typeof input === 'string'
            ? input
            : input instanceof URL
              ? input.href
              : input.url;
        if (path.endsWith('/auth/session'))
          return Promise.resolve(
            response({
              authenticated: true,
              csrf_token: 'token',
            }),
          );
        if (path.endsWith('/profile-edit') && init?.method === 'POST') {
          return Promise.resolve(
            response({ code: 'temporal.recurrence_edit.conflict' }, 409),
          );
        }
        throw new Error(`Unexpected call ${path}`);
      },
    );
    const remote = createRemoteRecurringProfileEdit(fetchFn);
    await expect(
      remote.saveActivityProfile(
        activityRef,
        { occurrenceRef, sourceRef, editRevision: 4, recurrenceStateRef },
        'only_this',
        {
          title: 'Corretto',
          description: null,
          location: null,
          colorCode: null,
        },
        'same-op',
      ),
    ).rejects.toThrow('ricorrenza');
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });
});
