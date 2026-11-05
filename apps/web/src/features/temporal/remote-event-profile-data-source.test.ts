import { fetchRequestBody } from '../../test-support/fetch-request';
import { fetchRequestUrl } from '../../test-support/fetch-request';
import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import { createRemoteEventProfileDataSource } from './remote-event-profile-data-source';

const EVENT = '0199a111-1111-7111-8111-111111111111';
const AREA = '0199a222-2222-7222-8222-222222222222';
const original = {
  event_ref: EVENT,
  title: 'Conferenza',
  description: null,
  location: null,
  color_code: null,
  profile_revision: 1,
  agenda_revision: 0,
  agenda_parts: [],
  created_at: '2026-10-01T09:00:00Z',
  life_area_ref: AREA,
  life_area_assignment_revision: 2,
  replayed: false,
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('owner-scoped Event profile CAS source', () => {
  it('submits Event profile, Scaletta, Life Area and execution policy as one atomic command', async () => {
    const submitted: unknown[] = [];
    let saved = false;
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      const url = fetchRequestUrl(input);
      if (url === '/api/v1/auth/session') {
        return Promise.resolve(
          json({ authenticated: true, csrf_token: 'csrf' }),
        );
      }
      if (url === '/api/v1/temporal/events/' + EVENT) {
        return Promise.resolve(
          json({
            ...original,
            ...(saved
              ? {
                  title: 'Nuova conferenza',
                  agenda_revision: 1,
                  agenda_parts: ['Apertura'],
                }
              : {}),
          }),
        );
      }
      if (url === '/api/v1/temporal/events/' + EVENT + '/atomic-edit') {
        expect(init?.method).toBe('PUT');
        submitted.push(JSON.parse(fetchRequestBody(init?.body)) as unknown);
        saved = true;
        return Promise.resolve(
          json({ event: { ...original }, objectives: [] }),
        );
      }
      throw new Error('Unexpected Event route ' + url);
    });
    const source = createRemoteEventProfileDataSource(fetchFn);
    const current = await source.load(EVENT);
    const result = await source.reviseAtomic(
      EVENT,
      current,
      {
        profile: {
          title: 'Nuova conferenza',
          description: null,
          location: null,
          colorCode: null,
        },
        agendaParts: ['Apertura'],
        lifeArea: { ref: null, expectedRevision: 2 },
        reality: { mode: 'review_on_end', expectedStateRef: null },
      },
      'event:atomic:1',
    );
    expect(submitted).toEqual([
      {
        operation_id: 'event:atomic:1',
        profile: {
          operation_id: 'event:atomic:1:profile',
          expected_revision: 1,
          title: 'Nuova conferenza',
          description: null,
          location: null,
          color_code: null,
        },
        agenda: {
          operation_id: 'event:atomic:1:agenda',
          expected_revision: 0,
          agenda_parts: ['Apertura'],
        },
        life_area: {
          life_area_ref: null,
          expected_assignment_revision: 2,
        },
        reality: {
          operation_id: 'event:atomic:1:reality',
          mode_code: 'review_on_end',
          expected_state_ref: null,
        },
      },
    ]);
    expect(result.agendaParts).toEqual(['Apertura']);
  });
  it('uses accepted revision + operation ID and refreshes canonical Event', async () => {
    const sent: unknown[] = [];
    let changed = false;
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      const url = fetchRequestUrl(input);
      if (url === '/api/v1/auth/session') {
        return Promise.resolve(
          json({ authenticated: true, csrf_token: 'csrf' }),
        );
      }
      if (
        url === '/api/v1/temporal/events/' + EVENT &&
        init?.method !== 'PUT'
      ) {
        return Promise.resolve(
          json({
            ...original,
            ...(changed
              ? {
                  title: 'Nuova conferenza',
                  description: 'Discussione',
                  location: 'Roma',
                  color_code: '#ABCDEF',
                  profile_revision: 2,
                }
              : {}),
          }),
        );
      }
      if (url === '/api/v1/temporal/events/' + EVENT + '/profile') {
        expect(init?.method).toBe('PUT');
        expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf');
        sent.push(JSON.parse(fetchRequestBody(init?.body)) as unknown);
        changed = true;
        return Promise.resolve(
          json({
            event_ref: EVENT,
            title: 'Nuova conferenza',
            description: 'Discussione',
            location: 'Roma',
            color_code: '#ABCDEF',
            revision: 2,
            replayed: false,
          }),
        );
      }
      throw new Error('Unexpected Event route ' + url);
    });
    const source = createRemoteEventProfileDataSource(fetchFn);
    const current = await source.load(EVENT);
    const accepted = await source.revise(
      EVENT,
      current,
      {
        title: 'Nuova conferenza',
        description: 'Discussione',
        location: 'Roma',
        colorCode: '#ABCDEF',
      },
      'm4:web:1',
    );
    expect(sent).toEqual([
      {
        operation_id: 'm4:web:1',
        expected_revision: 1,
        title: 'Nuova conferenza',
        description: 'Discussione',
        location: 'Roma',
        color_code: '#ABCDEF',
      },
    ]);
    expect(accepted).toMatchObject({
      eventRef: EVENT,
      title: 'Nuova conferenza',
      profileRevision: 2,
    });
  });

  it('does not announce success when CAS is stale', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) =>
      Promise.resolve(
        fetchRequestUrl(input).endsWith('auth/session')
          ? json({ authenticated: true, csrf_token: 'csrf' })
          : json({ code: 'temporal.event.profile_conflict' }, 409),
      ),
    );
    const source = createRemoteEventProfileDataSource(fetchFn);
    await expect(
      source.revise(
        EVENT,
        {
          eventRef: EVENT,
          title: 'Conferenza',
          profileRevision: 1,
          agendaRevision: 0,
          agendaParts: [],
          createdAt: Temporal.Instant.from('2026-10-01T09:00:00Z'),
        },
        {
          title: 'Nuovo',
          description: null,
          location: null,
          colorCode: null,
        },
        'm4:stale',
      ),
    ).rejects.toThrow('è cambiato');
  });
});
