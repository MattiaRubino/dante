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
    const fetchFn = vi.fn<typeof globalThis.fetch>((input, init) => {
      expect(input).toBe(
        '/api/v1/temporal/timeline/window?start_date=2026-09-07&end_date_exclusive=2026-09-14',
      );
      expect(init?.credentials).toBe('same-origin');

      const headers = new Headers(init?.headers);
      expect(headers.get('Accept')).toBe(
        'application/json, application/problem+json',
      );
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('X-Dante-Time-Zone')).toBe('Europe/Rome');

      return Promise.resolve(
        jsonResponse({
          kind: 'empty',
          start_date: '2026-09-07',
          end_date_exclusive: '2026-09-14',
          effective_zone_id: 'Europe/Rome',
        }),
      );
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

  it('normalizes the first canonical B02-A scheduled Activity window without losing Schedule state identity', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse({
            kind: 'window',
            start_date: '2026-09-07',
            end_date_exclusive: '2026-09-14',
            effective_zone_id: 'Europe/Rome',
            items: [
              {
                kind: 'scheduled_activity',
                activity_ref: '01991f2a-1234-7abc-8def-1234567890ab',
                schedule_ref: '01991f2a-2345-7bcd-9efa-234567890abc',
                placement_material_state_ref:
                  '01991f2a-3456-7cde-8fab-34567890abcd',
                title: 'Preparare demo',
                temporal_form: 'floating_local',
                starts_local_at: '2026-09-09T14:15:00',
                ends_local_at: '2026-09-09T15:00:00',
              },
            ],
          }),
        ),
      ),
      () => 'Europe/Rome',
    );

    const window = await source.loadWindow({
      startDate: '2026-09-07',
      endDateExclusive: '2026-09-14',
    });

    expect(window.kind).toBe('window');
    if (window.kind !== 'window') {
      throw new Error('expected populated Timeline window');
    }
    expect(window.effectiveZoneId).toBe('Europe/Rome');
    expect(window.items).toHaveLength(1);
    expect(window.items[0]).toMatchObject({
      kind: 'scheduled_activity',
      activityRef: '01991f2a-1234-7abc-8def-1234567890ab',
      scheduleRef: '01991f2a-2345-7bcd-9efa-234567890abc',
      placementMaterialStateRef: '01991f2a-3456-7cde-8fab-34567890abcd',
      title: 'Preparare demo',
      temporalForm: 'floating-local',
    });
    expect(window.items[0]?.startsLocalAt.toString()).toBe(
      '2026-09-09T14:15:00',
    );
    expect(window.items[0]?.endsLocalAt.toString()).toBe(
      '2026-09-09T15:00:00',
    );
  });

  it('does not replace backend failure with an empty success', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(jsonResponse({}, 503)),
      ),
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

  it('rejects unsupported or widened response semantics instead of inferring them', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse({
            kind: 'items',
            start_date: '2026-09-07',
            end_date_exclusive: '2026-09-14',
            effective_zone_id: 'Europe/Rome',
            items: [{ id: 'fake' }],
          }),
        ),
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

  it('rejects a zoned/offset timestamp and cross-day interval in the B02-A floating-local subset', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse({
            kind: 'window',
            start_date: '2026-09-07',
            end_date_exclusive: '2026-09-14',
            effective_zone_id: 'Europe/Rome',
            items: [
              {
                kind: 'scheduled_activity',
                activity_ref: '01991f2a-1234-7abc-8def-1234567890ab',
                schedule_ref: '01991f2a-2345-7bcd-9efa-234567890abc',
                placement_material_state_ref:
                  '01991f2a-3456-7cde-8fab-34567890abcd',
                title: 'Non perdere precisione',
                temporal_form: 'floating_local',
                starts_local_at: '2026-09-09T23:30:00+02:00',
                ends_local_at: '2026-09-10T00:30:00',
              },
            ],
          }),
        ),
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
