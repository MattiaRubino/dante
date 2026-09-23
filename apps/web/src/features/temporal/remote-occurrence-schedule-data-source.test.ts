import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import { createRemoteTemporalOccurrenceScheduleDataSource } from './remote-occurrence-schedule-data-source';

const OCCURRENCE_REF = '0199e5f0-6e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199e5f0-6e72-7bc0-8ad0-a2f403f5617d';
const STATE_REF = '0199e5f0-6e73-7bc0-8ad0-a2f403f5617d';

function response(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('remote Occurrence Schedule data source', () => {
  it('establishes a materialized Occurrence through the governed shared Schedule command', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      expect(new Headers(init?.headers).get('X-Dante-Client')).toBe('web');
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          response({ authenticated: true, csrf_token: 'csrf-b06-d' }),
        );
      }

      expect(input).toBe(
        `/api/v1/temporal/occurrences/${OCCURRENCE_REF}/schedule`,
      );
      expect(init?.method).toBe('POST');
      expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf-b06-d');
      expect(JSON.parse(String(init?.body))).toEqual({
        operation_id: 'b06-d:schedule:1',
        placement: {
          kind: 'floating_local_interval',
          starts_local_at: '2026-10-05T08:30:00',
          ends_local_at: '2026-10-05T09:15:00',
        },
      });
      return Promise.resolve(
        response({
          occurrence_ref: OCCURRENCE_REF,
          schedule_ref: SCHEDULE_REF,
          placement_material_state_ref: STATE_REF,
          placement: {
            kind: 'floating_local_interval',
            starts_local_at: '2026-10-05T08:30:00',
            ends_local_at: '2026-10-05T09:15:00',
          },
          replayed: false,
        }),
      );
    });

    const result = await createRemoteTemporalOccurrenceScheduleDataSource(
      fetchFn,
    ).establish({
      operationId: 'b06-d:schedule:1',
      occurrenceRef: OCCURRENCE_REF,
      placement: Object.freeze({
        kind: 'floating-local-interval' as const,
        startsLocalAt: Temporal.PlainDateTime.from('2026-10-05T08:30'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-10-05T09:15'),
      }),
    });

    expect(result).toEqual({
      occurrenceRef: OCCURRENCE_REF,
      scheduleRef: SCHEDULE_REF,
      placementMaterialStateRef: STATE_REF,
      replayed: false,
    });
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });

  it('does not accept a non-positive interval before issuing the Schedule POST', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>((input) => {
      if (input === '/api/v1/auth/session') {
        return Promise.resolve(
          response({ authenticated: true, csrf_token: 'csrf-b06-d' }),
        );
      }
      throw new Error('invalid placement must fail before Schedule POST');
    });

    await expect(
      createRemoteTemporalOccurrenceScheduleDataSource(fetchFn).establish({
        operationId: 'b06-d:schedule:invalid',
        occurrenceRef: OCCURRENCE_REF,
        placement: Object.freeze({
          kind: 'floating-local-interval' as const,
          startsLocalAt: Temporal.PlainDateTime.from('2026-10-05T09:15'),
          endsLocalAt: Temporal.PlainDateTime.from('2026-10-05T09:15'),
        }),
      }),
    ).rejects.toBeInstanceOf(RangeError);
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });
});
