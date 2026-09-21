import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  TemporalEventRemoteError,
  createRemoteTemporalEventDataSource,
} from './remote-event-data-source';
import { subscribeTemporalTimelineInvalidation } from './timeline-invalidation';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

const EVENT_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
const STATE_REF = '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d';

function commonResponse(agendaParts: readonly string[] = []) {
  return {
    event_ref: EVENT_REF,
    title: 'Evento B03-B',
    agenda_revision: 0,
    agenda_parts: agendaParts,
    created_at: '2026-09-17T10:00:00Z',
    schedule_ref: SCHEDULE_REF,
    placement_material_state_ref: STATE_REF,
    replayed: false,
  } as const;
}

describe('remote temporal Event data source', () => {
  it('creates a floating-local Event with ordered Agenda through the governed CSRF boundary and invalidates Timeline', async () => {
    let invalidations = 0;
    const unsubscribe = subscribeTemporalTimelineInvalidation(() => {
      invalidations += 1;
    });
    const agendaParts = Object.freeze([
      'Confermare decisione',
      'Assegnare azioni',
    ]);
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b03-b' }),
        );
      }
      expect(input).toBe('/api/v1/temporal/events/scheduled');
      expect(init?.method).toBe('POST');
      const headers = new Headers(init?.headers);
      expect(headers.get('X-Dante-CSRF')).toBe('csrf-b03-b');
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('X-Dante-Time-Zone')).toBe('Europe/Rome');
      expect(JSON.parse(String(init?.body))).toEqual({
        operation_id: 'operation:b03-b:web-floating',
        title: 'Evento B03-B',
        agenda_parts: agendaParts,
        placement: {
          kind: 'floating_local_interval',
          starts_local_at: '2026-09-17T18:30:00',
          ends_local_at: '2026-09-17T20:00:00',
        },
      });
      return Promise.resolve(
        jsonResponse(
          {
            ...commonResponse(agendaParts),
            temporal_form: 'floating_local',
            starts_local_at: '2026-09-17T18:30:00',
            ends_local_at: '2026-09-17T20:00:00',
          },
          201,
        ),
      );
    });
    const source = createRemoteTemporalEventDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    try {
      const result = await source.createScheduledEvent({
        operationId: ' operation:b03-b:web-floating ',
        title: ' Evento B03-B ',
        agendaParts: Object.freeze([
          ' Confermare decisione ',
          'Assegnare azioni',
        ]),
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from('2026-09-17T18:30:00'),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-17T20:00:00'),
        },
      });

      expect(result.event).toMatchObject({
        eventRef: EVENT_REF,
        title: 'Evento B03-B',
        agendaParts,
      });
      expect(result.schedule).toMatchObject({
        scheduleRef: SCHEDULE_REF,
        placementMaterialStateRef: STATE_REF,
      });
      expect(result.schedule.placement.kind).toBe('floating-local-interval');
      expect(result.replayed).toBe(false);
      expect(fetchFn).toHaveBeenCalledTimes(2);
      expect(invalidations).toBe(1);
    } finally {
      unsubscribe();
    }
  });

  it('preserves named-zone source intent plus resolved instants', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b03-b' }),
        );
      }
      return Promise.resolve(
        jsonResponse(
          {
            ...commonResponse(),
            temporal_form: 'named_zone_local',
            starts_local_at: '2026-10-25T02:10:00',
            ends_local_at: '2026-10-25T02:40:00',
            zone_id: 'Europe/Rome',
            resolved_start_at: '2026-10-25T01:10:00Z',
            resolved_end_at: '2026-10-25T01:40:00Z',
          },
          201,
        ),
      );
    });
    const source = createRemoteTemporalEventDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    const result = await source.createScheduledEvent({
      operationId: 'operation:b03-b:web-zone',
      title: 'Evento B03-B',
      agendaParts: Object.freeze([]),
      placement: {
        kind: 'named-zone-local-interval',
        startsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:10:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:40:00'),
        zoneId: 'Europe/Rome',
        disambiguation: 'later',
      },
    });

    expect(result.schedule.placement.kind).toBe('named-zone-local-interval');
    if (result.schedule.placement.kind !== 'named-zone-local-interval') {
      throw new Error('Expected named-zone Event placement.');
    }
    expect(result.schedule.placement.startsLocalAt.toString()).toBe(
      '2026-10-25T02:10:00',
    );
    expect(result.schedule.placement.zoneId).toBe('Europe/Rome');
    expect(result.schedule.placement.resolvedStartAt.toString()).toBe(
      '2026-10-25T01:10:00Z',
    );
  });

  it('preserves a multi-day date span without manufacturing clock time', async () => {
    const source = createRemoteTemporalEventDataSource(
      vi.fn<typeof globalThis.fetch>((input) => {
        if (input === '/api/v1/auth/session') {
          return Promise.resolve(
            jsonResponse({ authenticated: true, csrf_token: 'csrf-b03-b' }),
          );
        }
        return Promise.resolve(
          jsonResponse(
            {
              ...commonResponse(),
              temporal_form: 'date_span',
              start_date: '2026-09-19',
              end_date_exclusive: '2026-09-22',
            },
            201,
          ),
        );
      }),
    );

    const result = await source.createScheduledEvent({
      operationId: 'operation:b03-b:web-date-span',
      title: 'Evento B03-B',
      agendaParts: Object.freeze([]),
      placement: {
        kind: 'date-span',
        startDate: Temporal.PlainDate.from('2026-09-19'),
        endDateExclusive: Temporal.PlainDate.from('2026-09-22'),
      },
    });

    expect(result.schedule.placement.kind).toBe('date-span');
    if (result.schedule.placement.kind !== 'date-span') {
      throw new Error('Expected date-span Event placement.');
    }
    expect(result.schedule.placement.startDate.toString()).toBe('2026-09-19');
    expect(result.schedule.placement.endDateExclusive.toString()).toBe(
      '2026-09-22',
    );
  });

  it('keeps server rejection as rejection instead of fabricating Event success', async () => {
    const source = createRemoteTemporalEventDataSource(
      vi.fn<typeof globalThis.fetch>((input) => {
        if (input === '/api/v1/auth/session') {
          return Promise.resolve(
            jsonResponse({ authenticated: true, csrf_token: 'csrf-b03-b' }),
          );
        }
        return Promise.resolve(
          jsonResponse({ code: 'temporal.event.invalid_schedule_create' }, 422),
        );
      }),
    );

    await expect(
      source.createScheduledEvent({
        operationId: 'operation:b03-b:web-rejected',
        title: 'Evento B03-B',
        agendaParts: Object.freeze([]),
        placement: {
          kind: 'coarse-local-period',
          localDate: Temporal.PlainDate.from('2026-09-20'),
          period: 'morning',
        },
      }),
    ).rejects.toMatchObject({
      name: 'TemporalEventRemoteError',
      kind: 'http',
      status: 422,
      code: 'temporal.event.invalid_schedule_create',
    } satisfies Partial<TemporalEventRemoteError>);
  });

  it('rejects widened or hybrid response payloads at the protocol boundary', async () => {
    const source = createRemoteTemporalEventDataSource(
      vi.fn<typeof globalThis.fetch>((input) => {
        if (input === '/api/v1/auth/session') {
          return Promise.resolve(
            jsonResponse({ authenticated: true, csrf_token: 'csrf-b03-b' }),
          );
        }
        return Promise.resolve(
          jsonResponse(
            {
              ...commonResponse(),
              temporal_form: 'floating_local',
              starts_local_at: '2026-09-17T18:30:00',
              ends_local_at: '2026-09-17T20:00:00',
              activity_ref: '0199a8c0-7e74-7bc0-8ad0-a2f403f5617d',
            },
            201,
          ),
        );
      }),
    );

    await expect(
      source.createScheduledEvent({
        operationId: 'operation:b03-b:web-hybrid',
        title: 'Evento B03-B',
        agendaParts: Object.freeze([]),
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from('2026-09-17T18:30:00'),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-17T20:00:00'),
        },
      }),
    ).rejects.toBeInstanceOf(TemporalEventRemoteError);
  });

  it('discovers and replans a real postponed Event without fabricating a placement', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b05-d' }),
        );
      }
      if (input === '/api/v1/temporal/events/postponed') {
        expect(init?.method).toBeUndefined();
        expect(new Headers(init?.headers).get('X-Dante-Client')).toBe('web');
        return Promise.resolve(
          jsonResponse([
            {
              event_ref: EVENT_REF,
              schedule_ref: SCHEDULE_REF,
              title: 'Evento posticipato',
              created_at: '2026-09-20T10:00:00Z',
              life_area_ref: '0199a8c0-6e74-7bc0-8ad0-a2f403f5617d',
              life_area_assignment_revision: 1,
              unschedule_operation_id: 'operation:b05-d:postpone',
            },
          ]),
        );
      }
      expect(input).toBe(
        `/api/v1/temporal/events/${EVENT_REF}/schedules/${SCHEDULE_REF}/replan`,
      );
      expect(init?.method).toBe('PUT');
      expect(JSON.parse(String(init?.body))).toEqual({
        operation_id: 'operation:b05-d:replan',
        unschedule_operation_id: 'operation:b05-d:postpone',
        placement: {
          kind: 'coarse_local_period',
          local_date: '2026-09-25',
          period: 'evening',
        },
      });
      return Promise.resolve(
        jsonResponse({
          ...commonResponse(),
          temporal_form: 'coarse_local_period',
          local_date: '2026-09-25',
          period: 'evening',
        }),
      );
    });
    const source = createRemoteTemporalEventDataSource(fetchFn);
    const [postponed] = await source.listPostponedEvents();
    expect(postponed).toMatchObject({
      eventRef: EVENT_REF,
      scheduleRef: SCHEDULE_REF,
      title: 'Evento posticipato',
      unscheduleOperationId: 'operation:b05-d:postpone',
    });
    await expect(
      source.replanPostponedEvent({
        eventRef: EVENT_REF,
        scheduleRef: SCHEDULE_REF,
        unscheduleOperationId: 'operation:b05-d:postpone',
        operationId: 'operation:b05-d:replan',
        placement: {
          kind: 'coarse-local-period',
          localDate: Temporal.PlainDate.from('2026-09-25'),
          period: 'evening',
        },
      }),
    ).resolves.toMatchObject({ schedule: { scheduleRef: SCHEDULE_REF } });
  });
});
