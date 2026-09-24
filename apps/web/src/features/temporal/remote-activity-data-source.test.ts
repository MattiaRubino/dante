import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  TemporalActivityRemoteError,
  createRemoteTemporalActivityDataSource,
} from './remote-activity-data-source';
import { subscribeTemporalTimelineInvalidation } from './timeline-invalidation';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

function requestJsonBody(
  init: RequestInit | undefined,
): Readonly<Record<string, unknown>> {
  if (typeof init?.body !== 'string') {
    throw new Error('Expected JSON string request body.');
  }
  const parsed = JSON.parse(init.body) as unknown;
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed)) {
    throw new Error('Expected JSON object request body.');
  }
  return parsed as Readonly<Record<string, unknown>>;
}

const ACTIVITY = Object.freeze({
  activity_ref: '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d',
  title: 'Prima Activity',
  created_at: '2026-09-08T07:40:00Z',
  replayed: false,
});

const SCHEDULED_ACTIVITY = Object.freeze({
  ...ACTIVITY,
  schedule_ref: '0199a8c0-6e72-7cd1-9be1-b3f51406728e',
  placement_material_state_ref: '0199a8c0-7e73-7de2-8cf2-c4062517839f',
  temporal_form: 'floating_local',
  starts_local_at: '2026-09-09T14:15:00',
  ends_local_at: '2026-09-09T15:00:00',
});

describe('remote temporal Activity data source', () => {
  it('creates through authenticated governed fetch with CSRF and canonical B01 payload', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      const headers = new Headers(init?.headers);
      expect(init?.credentials).toBe('same-origin');
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('X-Dante-Time-Zone')).toBe('Europe/Rome');

      if (input === '/api/v1/auth/session') {
        expect(init?.method).toBeUndefined();
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b01' }),
        );
      }

      expect(input).toBe('/api/v1/temporal/activities');
      expect(init?.method).toBe('POST');
      expect(headers.get('X-Dante-CSRF')).toBe('csrf-b01');
      expect(headers.get('Content-Type')).toBe('application/json');
      expect(init?.body).toBe(
        JSON.stringify({
          operation_id: 'operation:b01-web-1',
          title: 'Prima Activity',
        }),
      );
      return Promise.resolve(jsonResponse(ACTIVITY, 201));
    });
    const source = createRemoteTemporalActivityDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    const invalidation = vi.fn();
    const unsubscribe = subscribeTemporalTimelineInvalidation(invalidation);
    const result = await source.createActivity({
      operationId: ' operation:b01-web-1 ',
      title: ' Prima Activity ',
    });
    unsubscribe();
    expect(invalidation).toHaveBeenCalledOnce();

    expect(result.activity.activityRef).toBe(ACTIVITY.activity_ref);
    expect(result.activity.title).toBe('Prima Activity');
    expect(result.activity.createdAt.toString()).toBe('2026-09-08T07:40:00Z');
    expect(result.replayed).toBe(false);
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });

  it('creates Activity plus accepted Schedule atomically through the generalized B02-E endpoint', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      const headers = new Headers(init?.headers);
      expect(init?.credentials).toBe('same-origin');
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('X-Dante-Time-Zone')).toBe('Europe/Rome');

      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b02' }),
        );
      }

      expect(input).toBe('/api/v1/temporal/activities/scheduled');
      expect(init?.method).toBe('POST');
      expect(headers.get('X-Dante-CSRF')).toBe('csrf-b02');
      expect(init?.body).toBe(
        JSON.stringify({
          operation_id: 'operation:b02-web-1',
          title: 'Prima Activity',
          placement: {
            kind: 'floating_local_interval',
            starts_local_at: '2026-09-09T14:15:00',
            ends_local_at: '2026-09-09T15:00:00',
          },
        }),
      );
      return Promise.resolve(jsonResponse(SCHEDULED_ACTIVITY, 201));
    });
    const source = createRemoteTemporalActivityDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    const result = await source.createScheduledActivity({
      operationId: 'operation:b02-web-1',
      title: 'Prima Activity',
      placement: {
        kind: 'floating-local-interval',
        startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T14:15:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T15:00:00'),
      },
    });

    expect(result.activity.activityRef).toBe(ACTIVITY.activity_ref);
    expect(result.schedule).toMatchObject({
      scheduleRef: SCHEDULED_ACTIVITY.schedule_ref,
      placementMaterialStateRef:
        SCHEDULED_ACTIVITY.placement_material_state_ref,
    });
    expect(result.schedule.placement.kind).toBe('floating-local-interval');
    if (result.schedule.placement.kind !== 'floating-local-interval') {
      throw new Error('Expected floating-local placement.');
    }
    expect(result.schedule.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T14:15:00',
    );
    expect(result.schedule.placement.endsLocalAt.toString()).toBe(
      '2026-09-09T15:00:00',
    );
    expect(result.replayed).toBe(false);
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });

  it('creates a cross-midnight floating-local Activity Schedule without attaching a timezone', async () => {
    const response = Object.freeze({
      ...SCHEDULED_ACTIVITY,
      starts_local_at: '2026-09-09T23:30:00',
      ends_local_at: '2026-09-10T00:15:00',
    });
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b02-e' }),
        );
      }
      expect(input).toBe('/api/v1/temporal/activities/scheduled');
      expect(requestJsonBody(init).placement).toEqual({
        kind: 'floating_local_interval',
        starts_local_at: '2026-09-09T23:30:00',
        ends_local_at: '2026-09-10T00:15:00',
      });
      return Promise.resolve(jsonResponse(response, 201));
    });
    const source = createRemoteTemporalActivityDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    const result = await source.createScheduledActivity({
      operationId: 'operation:b02-e:cross-day',
      title: 'Cross midnight',
      placement: {
        kind: 'floating-local-interval',
        startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T23:30:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-09-10T00:15:00'),
      },
    });

    expect(result.schedule.placement.kind).toBe('floating-local-interval');
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });

  it('creates coarse Activity placement without manufacturing clock boundaries', async () => {
    const response = Object.freeze({
      activity_ref: ACTIVITY.activity_ref,
      title: 'Pomeriggio',
      created_at: ACTIVITY.created_at,
      replayed: false,
      schedule_ref: SCHEDULED_ACTIVITY.schedule_ref,
      placement_material_state_ref:
        SCHEDULED_ACTIVITY.placement_material_state_ref,
      temporal_form: 'coarse_local_period',
      local_date: '2026-09-16',
      period: 'afternoon',
    });
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b02-e' }),
        );
      }
      expect(requestJsonBody(init).placement).toEqual({
        kind: 'coarse_local_period',
        local_date: '2026-09-16',
        period: 'afternoon',
      });
      return Promise.resolve(jsonResponse(response, 201));
    });
    const source = createRemoteTemporalActivityDataSource(fetchFn);

    const result = await source.createScheduledActivity({
      operationId: 'operation:b02-e:coarse',
      title: 'Pomeriggio',
      placement: {
        kind: 'coarse-local-period',
        localDate: Temporal.PlainDate.from('2026-09-16'),
        period: 'afternoon',
      },
    });

    expect(result.schedule.placement).toMatchObject({
      kind: 'coarse-local-period',
      period: 'afternoon',
    });
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });

  it('reads canonical unplaced Activities without inventing temporal fields', async () => {
    const source = createRemoteTemporalActivityDataSource(
      vi.fn<typeof globalThis.fetch>((input) => {
        expect(input).toBe('/api/v1/temporal/activities/unplaced');
        return Promise.resolve(
          jsonResponse({ kind: 'unplaced', items: [ACTIVITY] }),
        );
      }),
      () => 'Europe/Rome',
    );

    const items = await source.loadUnplaced();

    expect(items).toHaveLength(1);
    expect(items[0]).toMatchObject({
      activityRef: ACTIVITY.activity_ref,
      title: 'Prima Activity',
    });
    expect(Object.keys(items[0] ?? {}).sort()).toEqual([
      'activityRef',
      'createdAt',
      'title',
    ]);
  });

  it('preserves server conflict instead of reporting fake Activity success', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b01' }),
        );
      }
      return Promise.resolve(
        jsonResponse({ code: 'temporal.activity.operation_id_reused' }, 409),
      );
    });
    const source = createRemoteTemporalActivityDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    await expect(
      source.createActivity({
        operationId: 'operation:b01-web-conflict',
        title: 'Activity',
      }),
    ).rejects.toMatchObject({
      name: 'TemporalActivityRemoteError',
      kind: 'http',
      status: 409,
      code: 'temporal.activity.operation_id_reused',
    });
  });

  it('preserves Schedule operation-id conflict instead of reporting fake success', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b02' }),
        );
      }
      return Promise.resolve(
        jsonResponse({ code: 'temporal.schedule.operation_id_reused' }, 409),
      );
    });
    const source = createRemoteTemporalActivityDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    await expect(
      source.createScheduledActivity({
        operationId: 'operation:b02-web-conflict',
        title: 'Activity',
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T14:15:00'),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T15:00:00'),
        },
      }),
    ).rejects.toMatchObject({
      name: 'TemporalActivityRemoteError',
      kind: 'http',
      status: 409,
      code: 'temporal.schedule.operation_id_reused',
    });
  });

  it('rejects malformed Activity identity instead of widening the transport contract', async () => {
    const source = createRemoteTemporalActivityDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse({
            kind: 'unplaced',
            items: [{ ...ACTIVITY, activity_ref: 'not-a-native-ref' }],
          }),
        ),
      ),
      () => 'Europe/Rome',
    );

    await expect(source.loadUnplaced()).rejects.toBeInstanceOf(
      TemporalActivityRemoteError,
    );
  });

  it('attaches a Schedule to the exact existing Activity and invalidates Timeline', async () => {
    const invalidated = vi.fn();
    const unsubscribe = subscribeTemporalTimelineInvalidation(invalidated);
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b02-b' }),
        );
      }
      expect(input).toBe(
        `/api/v1/temporal/activities/${ACTIVITY.activity_ref}/schedule`,
      );
      expect(init?.method).toBe('POST');
      expect(init?.body).toBe(
        JSON.stringify({
          operation_id: 'operation:b02-b:place-1',
          placement: {
            kind: 'floating_local_interval',
            starts_local_at: '2026-09-09T14:15:00',
            ends_local_at: '2026-09-09T15:00:00',
          },
        }),
      );
      return Promise.resolve(jsonResponse(SCHEDULED_ACTIVITY, 201));
    });
    const source = createRemoteTemporalActivityDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    try {
      const result = await source.establishActivitySchedule({
        activityRef: ACTIVITY.activity_ref,
        operationId: ' operation:b02-b:place-1 ',
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from(
            '2026-09-09T14:15:00',
          ),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T15:00:00'),
        },
      });

      expect(result.activity.activityRef).toBe(ACTIVITY.activity_ref);
      expect(result.schedule.scheduleRef).toBe(
        SCHEDULED_ACTIVITY.schedule_ref,
      );
      expect(invalidated).toHaveBeenCalledTimes(1);
      expect(fetchFn).toHaveBeenCalledTimes(2);
    } finally {
      unsubscribe();
    }
  });

  it('attaches a cross-midnight placement to an existing Activity', async () => {
    const response = Object.freeze({
      ...SCHEDULED_ACTIVITY,
      starts_local_at: '2026-09-09T23:30:00',
      ends_local_at: '2026-09-10T00:15:00',
    });
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b02-e' }),
        );
      }
      expect(input).toBe(
        `/api/v1/temporal/activities/${ACTIVITY.activity_ref}/schedule`,
      );
      expect(requestJsonBody(init).placement).toEqual({
        kind: 'floating_local_interval',
        starts_local_at: '2026-09-09T23:30:00',
        ends_local_at: '2026-09-10T00:15:00',
      });
      return Promise.resolve(jsonResponse(response, 201));
    });
    const source = createRemoteTemporalActivityDataSource(fetchFn);

    const result = await source.establishActivitySchedule({
      activityRef: ACTIVITY.activity_ref,
      operationId: 'operation:b02-e:place-cross-day',
      placement: {
        kind: 'floating-local-interval',
        startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T23:30:00'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-09-10T00:15:00'),
      },
    });

    expect(result.schedule.placement.kind).toBe('floating-local-interval');
  });

  it('rejects B02-E response identity drift instead of moving a different Activity', async () => {
    const otherActivityRef = '0199a8c0-8e74-7ef3-9df3-d517362894a0';
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          jsonResponse({ authenticated: true, csrf_token: 'csrf-b02-b' }),
        );
      }
      return Promise.resolve(
        jsonResponse({
          ...SCHEDULED_ACTIVITY,
          activity_ref: otherActivityRef,
        }),
      );
    });
    const source = createRemoteTemporalActivityDataSource(fetchFn);

    await expect(
      source.establishActivitySchedule({
        activityRef: ACTIVITY.activity_ref,
        operationId: 'operation:b02-b:identity-drift',
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from(
            '2026-09-09T14:15:00',
          ),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T15:00:00'),
        },
      }),
    ).rejects.toMatchObject({
      name: 'TemporalActivityRemoteError',
      kind: 'protocol',
    });
  });

  it('rejects invalid Activity identity before network I/O', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>();
    const source = createRemoteTemporalActivityDataSource(fetchFn);

    await expect(
      source.establishActivitySchedule({
        activityRef: 'not-a-native-ref',
        operationId: 'operation:b02-b:invalid',
        placement: {
          kind: 'floating-local-interval',
          startsLocalAt: Temporal.PlainDateTime.from(
            '2026-09-09T23:30:00',
          ),
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-10T00:15:00'),
        },
      }),
    ).rejects.toBeInstanceOf(RangeError);
    expect(fetchFn).not.toHaveBeenCalled();
  });
});
