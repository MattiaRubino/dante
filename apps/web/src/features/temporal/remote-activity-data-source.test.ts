import { describe, expect, it, vi } from 'vitest';

import {
  TemporalActivityRemoteError,
  createRemoteTemporalActivityDataSource,
} from './remote-activity-data-source';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

const ACTIVITY = Object.freeze({
  activity_ref: '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d',
  title: 'Prima Activity',
  created_at: '2026-09-08T07:40:00Z',
  replayed: false,
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

    const result = await source.createActivity({
      operationId: ' operation:b01-web-1 ',
      title: ' Prima Activity ',
    });

    expect(result.activity.activityRef).toBe(ACTIVITY.activity_ref);
    expect(result.activity.title).toBe('Prima Activity');
    expect(result.activity.createdAt.toString()).toBe(
      '2026-09-08T07:40:00Z',
    );
    expect(result.replayed).toBe(false);
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
});
