import { describe, expect, it, vi } from 'vitest';

import {
  createRemoteTemporalEventAgendaDataSource,
  TemporalEventAgendaRemoteError,
} from './remote-event-agenda-data-source';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

const EVENT_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';

function eventResponse(revision = 2, agendaParts: readonly string[] = ['A', 'B']) {
  return {
    event_ref: EVENT_REF,
    title: 'Evento B03-D',
    agenda_revision: revision,
    agenda_parts: agendaParts,
    created_at: '2026-09-17T10:00:00Z',
    replayed: false,
  } as const;
}

describe('remote Event Agenda data source', () => {
  it('loads canonical ordered Agenda from Event read', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      expect(input).toBe(`/api/v1/temporal/events/${EVENT_REF}`);
      expect(init?.method).toBeUndefined();
      return Promise.resolve(jsonResponse(eventResponse()));
    });
    const source = createRemoteTemporalEventAgendaDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    const result = await source.loadEvent(EVENT_REF);

    expect(result).toMatchObject({
      eventRef: EVENT_REF,
      title: 'Evento B03-D',
      agendaRevision: 2,
      agendaParts: ['A', 'B'],
    });
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('replaces Agenda through CSRF with exact CAS payload', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b03-d' }),
        );
      }
      expect(input).toBe(`/api/v1/temporal/events/${EVENT_REF}/agenda`);
      expect(init?.method).toBe('PUT');
      const headers = new Headers(init?.headers);
      expect(headers.get('X-Dante-CSRF')).toBe('csrf-b03-d');
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('X-Dante-Time-Zone')).toBe('Europe/Rome');
      expect(JSON.parse(String(init?.body))).toEqual({
        operation_id: 'operation:b03-d:web',
        expected_revision: 2,
        agenda_parts: ['A', 'B2'],
      });
      return Promise.resolve(
        jsonResponse({
          event_ref: EVENT_REF,
          agenda_revision: 3,
          agenda_parts: ['A', 'B2'],
          replayed: false,
        }),
      );
    });
    const source = createRemoteTemporalEventAgendaDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    const result = await source.replaceAgenda({
      eventRef: EVENT_REF,
      operationId: ' operation:b03-d:web ',
      expectedRevision: 2,
      agendaParts: [' A ', 'B2'],
    });

    expect(result).toEqual({
      eventRef: EVENT_REF,
      agendaRevision: 3,
      agendaParts: ['A', 'B2'],
      replayed: false,
    });
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });

  it('preserves revision-conflict problem code for authoritative reload handling', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b03-d' }),
        );
      }
      return Promise.resolve(
        jsonResponse(
          { code: 'temporal.event.agenda_revision_conflict' },
          409,
        ),
      );
    });
    const source = createRemoteTemporalEventAgendaDataSource(fetchFn);

    await expect(
      source.replaceAgenda({
        eventRef: EVENT_REF,
        operationId: 'operation:b03-d:stale',
        expectedRevision: 1,
        agendaParts: ['stale'],
      }),
    ).rejects.toMatchObject({
      kind: 'http',
      status: 409,
      code: 'temporal.event.agenda_revision_conflict',
    });
  });

  it('fails closed on malformed Agenda read payload', async () => {
    const source = createRemoteTemporalEventAgendaDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse({
            ...eventResponse(),
            agenda_parts: [' padded '],
          }),
        ),
      ),
    );

    await expect(source.loadEvent(EVENT_REF)).rejects.toBeInstanceOf(
      TemporalEventAgendaRemoteError,
    );
  });
});
