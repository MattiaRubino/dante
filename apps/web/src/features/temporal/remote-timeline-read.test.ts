import { describe, expect, it, vi } from 'vitest';

import {
  TemporalTimelineRemoteError,
  createRemoteTemporalTimelineDataSource,
} from './remote-timeline-read';

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}

describe('remote temporal Timeline data source', () => {
  it('uses the governed same-origin fetch path and preserves the server effective timezone', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>(async (input, init) => {
      expect(String(input)).toBe(
        '/api/v1/temporal/timeline/window?start_date=2026-09-07&end_date_exclusive=2026-09-14',
      );
      expect(init?.credentials).toBe('same-origin');

      const headers = new Headers(init?.headers);
      expect(headers.get('Accept')).toBe(
        'application/json, application/problem+json',
      );
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('X-Dante-Time-Zone')).toBe('Europe/Rome');

      return jsonResponse({
        kind: 'empty',
        start_date: '2026-09-07',
        end_date_exclusive: '2026-09-14',
        effective_zone_id: 'Europe/Rome',
      });
    });
    const source = createRemoteTemporalTimelineDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    await expect(
      source.loadWindow({
        startDate: '2026-09-07',
        endDateExclusive: '2026-09-14',
      }),
    ).resolves.toEqual({
      kind: 'empty',
      startDate: '2026-09-07',
      endDateExclusive: '2026-09-14',
      effectiveZoneId: 'Europe/Rome',
    });
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('does not replace backend failure with an empty success', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(async () => jsonResponse({}, 503)),
      () => 'Europe/Rome',
    );

    const failure = source.loadWindow({
      startDate: '2026-09-07',
      endDateExclusive: '2026-09-14',
    });

    await expect(failure).rejects.toMatchObject({
      name: 'TemporalTimelineRemoteError',
      kind: 'http',
      status: 503,
    });
  });

  it('rejects a premature non-empty or widened response instead of inferring semantics', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(async () =>
        jsonResponse({
          kind: 'items',
          start_date: '2026-09-07',
          end_date_exclusive: '2026-09-14',
          effective_zone_id: 'Europe/Rome',
          items: [{ id: 'fake' }],
        }),
      ),
      () => 'Europe/Rome',
    );

    await expect(
      source.loadWindow({
        startDate: '2026-09-07',
        endDateExclusive: '2026-09-14',
      }),
    ).rejects.toBeInstanceOf(TemporalTimelineRemoteError);
  });

  it('rejects invalid windows before network I/O', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>();
    const source = createRemoteTemporalTimelineDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    await expect(
      source.loadWindow({
        startDate: '2026-09-07',
        endDateExclusive: '2026-09-07',
      }),
    ).rejects.toBeInstanceOf(RangeError);
    expect(fetchFn).not.toHaveBeenCalled();
  });
});
