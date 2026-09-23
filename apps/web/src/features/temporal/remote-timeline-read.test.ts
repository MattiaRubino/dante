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

const WINDOW_REQUEST = Object.freeze({
  startDate: '2026-09-07',
  endDateExclusive: '2026-09-14',
});

const BASE_ITEM = Object.freeze({
  kind: 'scheduled_activity',
  activity_ref: '01991f2a-1234-7abc-8def-1234567890ab',
  schedule_ref: '01991f2a-2345-7bcd-9efa-234567890abc',
  placement_material_state_ref: '01991f2a-3456-7cde-8fab-34567890abcd',
  title: 'Preparare demo',
});

function populated(items: readonly unknown[]) {
  return {
    kind: 'window',
    start_date: WINDOW_REQUEST.startDate,
    end_date_exclusive: WINDOW_REQUEST.endDateExclusive,
    effective_zone_id: 'Europe/Rome',
    items,
  };
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
          start_date: WINDOW_REQUEST.startDate,
          end_date_exclusive: WINDOW_REQUEST.endDateExclusive,
          effective_zone_id: 'Europe/Rome',
        }),
      );
    });
    const source = createRemoteTemporalTimelineDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    await expect(source.loadWindow(WINDOW_REQUEST)).resolves.toEqual({
      kind: 'empty',
      startDate: WINDOW_REQUEST.startDate,
      endDateExclusive: WINDOW_REQUEST.endDateExclusive,
      effectiveZoneId: 'Europe/Rome',
    });
    expect(fetchFn).toHaveBeenCalledTimes(1);
  });

  it('normalizes floating-local placement without losing Schedule state identity', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            populated([
              {
                ...BASE_ITEM,
                temporal_form: 'floating_local',
                starts_local_at: '2026-09-09T14:15:00',
                ends_local_at: '2026-09-09T15:00:00',
              },
            ]),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    const window = await source.loadWindow(WINDOW_REQUEST);

    expect(window.kind).toBe('window');
    if (window.kind !== 'window') {
      throw new Error('expected populated Timeline window');
    }
    const [item] = window.items;
    expect(item).toMatchObject({
      kind: 'scheduled_activity',
      activityRef: BASE_ITEM.activity_ref,
      scheduleRef: BASE_ITEM.schedule_ref,
      placementMaterialStateRef: BASE_ITEM.placement_material_state_ref,
      title: BASE_ITEM.title,
      temporalForm: 'floating-local',
    });
    if (item?.temporalForm !== 'floating-local') {
      throw new Error('expected floating-local item');
    }
    expect(item.startsLocalAt.toString()).toBe('2026-09-09T14:15:00');
    expect(item.endsLocalAt.toString()).toBe('2026-09-09T15:00:00');
  });

  it('accepts cross-midnight floating-local placement without attaching a timezone', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            populated([
              {
                ...BASE_ITEM,
                temporal_form: 'floating_local',
                starts_local_at: '2026-09-09T23:30:00',
                ends_local_at: '2026-09-10T00:30:00',
              },
            ]),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    const window = await source.loadWindow(WINDOW_REQUEST);
    if (window.kind !== 'window') {
      throw new Error('expected populated Timeline window');
    }
    const [item] = window.items;
    if (item?.temporalForm !== 'floating-local') {
      throw new Error('expected floating-local item');
    }
    expect(item.startsLocalAt.toString()).toBe('2026-09-09T23:30:00');
    expect(item.endsLocalAt.toString()).toBe('2026-09-10T00:30:00');
  });

  it('preserves every activated B02-E Timeline form without flattening temporal meaning', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            populated([
              {
                ...BASE_ITEM,
                schedule_ref: '01991f2a-2345-7bcd-9efa-234567890ab1',
                temporal_form: 'date_span',
                start_date: '2026-09-09',
                end_date_exclusive: '2026-09-11',
              },
              {
                ...BASE_ITEM,
                schedule_ref: '01991f2a-2345-7bcd-9efa-234567890ab2',
                temporal_form: 'named_zone_local',
                starts_local_at: '2026-10-25T02:10:00',
                ends_local_at: '2026-10-25T02:40:00',
                zone_id: 'Europe/Rome',
                resolved_start_at: '2026-10-25T01:10:00Z',
                resolved_end_at: '2026-10-25T01:40:00Z',
                display_starts_local_at: '2026-10-25T02:10:00',
                display_ends_local_at: '2026-10-25T02:40:00',
              },
              {
                ...BASE_ITEM,
                schedule_ref: '01991f2a-2345-7bcd-9efa-234567890ab3',
                temporal_form: 'absolute',
                starts_at: '2026-09-09T07:00:00Z',
                ends_at: '2026-09-09T08:00:00Z',
                display_starts_local_at: '2026-09-09T09:00:00',
                display_ends_local_at: '2026-09-09T10:00:00',
              },
              {
                ...BASE_ITEM,
                schedule_ref: '01991f2a-2345-7bcd-9efa-234567890ab4',
                temporal_form: 'coarse_local_period',
                local_date: '2026-09-09',
                period: 'afternoon',
              },
            ]),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    const window = await source.loadWindow(WINDOW_REQUEST);
    if (window.kind !== 'window') {
      throw new Error('expected populated Timeline window');
    }

    expect(
      window.items.map((item) =>
        item.kind === 'expected_occurrence' ? null : item.temporalForm,
      ),
    ).toEqual([
      'date-span',
      'named-zone-local',
      'absolute',
      'coarse-local-period',
    ]);
    const [dateSpan, named, absolute, coarse] = window.items;
    if (dateSpan?.temporalForm !== 'date-span') {
      throw new Error('expected date-span item');
    }
    if (named?.temporalForm !== 'named-zone-local') {
      throw new Error('expected named-zone item');
    }
    if (absolute?.temporalForm !== 'absolute') {
      throw new Error('expected absolute item');
    }
    if (coarse?.temporalForm !== 'coarse-local-period') {
      throw new Error('expected coarse item');
    }

    expect(dateSpan.startDate.toString()).toBe('2026-09-09');
    expect(dateSpan.endDateExclusive.toString()).toBe('2026-09-11');
    expect(named.zoneId).toBe('Europe/Rome');
    expect(named.resolvedStartAt.toString()).toBe('2026-10-25T01:10:00Z');
    expect(absolute.startsAt.toString()).toBe('2026-09-09T07:00:00Z');
    expect(absolute.displayStartsLocalAt.toString()).toBe(
      '2026-09-09T09:00:00',
    );
    expect(coarse.period).toBe('afternoon');
  });

  it('preserves scheduled precedence metadata and flexible expected coordinates', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            populated([
              {
                kind: 'scheduled_occurrence',
                occurrence_ref: '01991f2a-4567-7def-8abc-4567890abcde',
                source_kind: 'routine',
                source_native_ref: '01991f2a-5678-7efa-9bcd-567890abcdef',
                title: 'Farmaco',
                coordinate: {
                  family_code: 'calendar_wall_clock',
                  generated_date: '2026-09-09',
                  generated_wall_time: '08:00:00',
                  clock_basis_code: 'floating_local',
                  zone_id: null,
                  resolved_at: null,
                },
                schedule_ref: '01991f2a-6789-7fab-8cde-67890abcdef1',
                placement_material_state_ref:
                  '01991f2a-789a-7abc-9def-7890abcdef12',
                placement: {
                  temporal_form: 'floating_local',
                  starts_local_at: '2026-09-09T09:00:00',
                  ends_local_at: '2026-09-09T09:30:00',
                },
              },
              {
                kind: 'expected_occurrence',
                occurrence_ref: '01991f2a-89ab-7bcd-8efa-890abcdef123',
                source_kind: 'event',
                source_native_ref: '01991f2a-9abc-7cde-9fab-90abcdef1234',
                title: 'Allenamenti',
                coordinate: {
                  family_code: 'quota_per_period',
                  period_start_date: '2026-09-07',
                  period_end_date_exclusive: '2026-09-14',
                  frame_code: 'floating_local',
                  zone_id: null,
                },
              },
            ]),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    const window = await source.loadWindow(WINDOW_REQUEST);
    if (window.kind !== 'window') {
      throw new Error('expected populated Timeline window');
    }
    const [scheduled, expected] = window.items;
    expect(scheduled).toMatchObject({
      kind: 'scheduled_occurrence',
      sourceKind: 'routine',
      temporalForm: 'floating-local',
      coordinate: {
        familyCode: 'calendar-wall-clock',
        clockBasis: 'floating-local',
      },
    });
    expect(expected).toMatchObject({
      kind: 'expected_occurrence',
      sourceKind: 'event',
      coordinate: {
        familyCode: 'quota-per-period',
        frame: 'floating-local',
      },
    });
  });

  it('does not replace backend failure with an empty success', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(jsonResponse({}, 503)),
      ),
      () => 'Europe/Rome',
    );

    await expect(source.loadWindow(WINDOW_REQUEST)).rejects.toMatchObject({
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
            start_date: WINDOW_REQUEST.startDate,
            end_date_exclusive: WINDOW_REQUEST.endDateExclusive,
            effective_zone_id: 'Europe/Rome',
            items: [{ id: 'fake' }],
          }),
        ),
      ),
      () => 'Europe/Rome',
    );

    await expect(source.loadWindow(WINDOW_REQUEST)).rejects.toBeInstanceOf(
      TemporalTimelineRemoteError,
    );
  });

  it('rejects an offset-bearing timestamp in floating-local semantics', async () => {
    const source = createRemoteTemporalTimelineDataSource(
      vi.fn<typeof globalThis.fetch>(() =>
        Promise.resolve(
          jsonResponse(
            populated([
              {
                ...BASE_ITEM,
                temporal_form: 'floating_local',
                starts_local_at: '2026-09-09T23:30:00+02:00',
                ends_local_at: '2026-09-10T00:30:00',
              },
            ]),
          ),
        ),
      ),
      () => 'Europe/Rome',
    );

    await expect(source.loadWindow(WINDOW_REQUEST)).rejects.toBeInstanceOf(
      TemporalTimelineRemoteError,
    );
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
