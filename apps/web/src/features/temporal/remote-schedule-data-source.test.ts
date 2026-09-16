import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  TemporalScheduleRemoteError,
  createRemoteTemporalScheduleDataSource,
} from './remote-schedule-data-source';
import type {
  TemporalScheduleRevisionRequest,
  TemporalScheduleUnscheduleRequest,
  TemporalScheduleUnscheduleUndoRequest,
} from './schedule-data-source';

const SCHEDULE_REF = '0199a8c0-5e72-7bc0-8ad0-a2f403f5617d';
const CURRENT_STATE_REF = '0199a8c0-5e73-7bc0-8ad0-a2f403f5617d';
const NEXT_STATE_REF = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const RESTORED_STATE_REF = '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d';

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

function revisionRequest(): TemporalScheduleRevisionRequest {
  return {
    operationId: 'b02-c:revision:1',
    scheduleRef: SCHEDULE_REF,
    expectedPlacementMaterialStateRef: CURRENT_STATE_REF,
    placement: {
      kind: 'floating-local-interval',
      startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T14:00'),
      endsLocalAt: Temporal.PlainDateTime.from('2026-09-09T15:30'),
    },
  };
}

describe('remote Schedule data source', () => {
  it('sends the exact expected MaterialState basis and preserves the returned revision', async () => {
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          schedule_ref: SCHEDULE_REF,
          previous_placement_material_state_ref: CURRENT_STATE_REF,
          placement_material_state_ref: NEXT_STATE_REF,
          temporal_form: 'floating_local',
          starts_local_at: '2026-09-09T14:00:00',
          ends_local_at: '2026-09-09T15:30:00',
          replayed: false,
        }),
      );
    const source = createRemoteTemporalScheduleDataSource(
      fetchFn,
      () => 'Europe/Rome',
    );

    const result = await source.reviseSchedule(revisionRequest());

    expect(result).toMatchObject({
      scheduleRef: SCHEDULE_REF,
      previousPlacementMaterialStateRef: CURRENT_STATE_REF,
      placementMaterialStateRef: NEXT_STATE_REF,
      replayed: false,
    });
    expect(result.placement.kind).toBe('floating-local-interval');
    if (result.placement.kind !== 'floating-local-interval') {
      throw new Error('Expected floating-local placement.');
    }
    expect(result.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T14:00:00',
    );
    expect(fetchFn).toHaveBeenCalledTimes(2);
    const [url, init] = fetchFn.mock.calls[1] ?? [];
    expect(url).toBe(`/api/v1/temporal/schedules/${SCHEDULE_REF}/placement`);
    expect(init?.method).toBe('PATCH');
    expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf-token');
    expect(requestJsonBody(init)).toEqual({
      operation_id: 'b02-c:revision:1',
      expected_placement_material_state_ref: CURRENT_STATE_REF,
      placement: {
        kind: 'floating_local_interval',
        starts_local_at: '2026-09-09T14:00:00',
        ends_local_at: '2026-09-09T15:30:00',
      },
    });
  });

  it('preserves a stale expected-state conflict without converting it to success', async () => {
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({ code: 'temporal.schedule.revision_conflict' }, 409),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    await expect(
      source.reviseSchedule(revisionRequest()),
    ).rejects.toMatchObject({
      name: 'TemporalScheduleRemoteError',
      kind: 'http',
      status: 409,
      code: 'temporal.schedule.revision_conflict',
    } satisfies Partial<TemporalScheduleRemoteError>);
  });

  it('rejects a response that changes Schedule identity or expected-state basis', async () => {
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          schedule_ref: '0199a8c0-5e75-7bc0-8ad0-a2f403f5617d',
          previous_placement_material_state_ref: CURRENT_STATE_REF,
          placement_material_state_ref: NEXT_STATE_REF,
          temporal_form: 'floating_local',
          starts_local_at: '2026-09-09T14:00:00',
          ends_local_at: '2026-09-09T15:30:00',
          replayed: false,
        }),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    await expect(
      source.reviseSchedule(revisionRequest()),
    ).rejects.toMatchObject({
      kind: 'protocol',
    });
  });

  it('accepts a cross-midnight floating-local revision without attaching a timezone', async () => {
    const request: TemporalScheduleRevisionRequest = {
      ...revisionRequest(),
      operationId: 'b02-e:revision:cross-midnight',
      placement: {
        kind: 'floating-local-interval',
        startsLocalAt: Temporal.PlainDateTime.from('2026-09-09T23:30'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-09-10T01:15'),
      },
    };
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          schedule_ref: SCHEDULE_REF,
          previous_placement_material_state_ref: CURRENT_STATE_REF,
          placement_material_state_ref: NEXT_STATE_REF,
          temporal_form: 'floating_local',
          starts_local_at: '2026-09-09T23:30:00',
          ends_local_at: '2026-09-10T01:15:00',
          replayed: false,
        }),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    await expect(source.reviseSchedule(request)).resolves.toMatchObject({
      placement: {
        kind: 'floating-local-interval',
      },
    });
    const [, init] = fetchFn.mock.calls[1] ?? [];
    expect(requestJsonBody(init).placement).toEqual({
      kind: 'floating_local_interval',
      starts_local_at: '2026-09-09T23:30:00',
      ends_local_at: '2026-09-10T01:15:00',
    });
  });

  it('round-trips coarse precision without manufacturing clock boundaries', async () => {
    const request: TemporalScheduleRevisionRequest = {
      ...revisionRequest(),
      operationId: 'b02-e:revision:coarse',
      placement: {
        kind: 'coarse-local-period',
        localDate: Temporal.PlainDate.from('2026-09-16'),
        period: 'afternoon',
      },
    };
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          schedule_ref: SCHEDULE_REF,
          previous_placement_material_state_ref: CURRENT_STATE_REF,
          placement_material_state_ref: NEXT_STATE_REF,
          temporal_form: 'coarse_local_period',
          local_date: '2026-09-16',
          period: 'afternoon',
          replayed: false,
        }),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    const result = await source.reviseSchedule(request);

    expect(result.placement).toMatchObject({
      kind: 'coarse-local-period',
      period: 'afternoon',
    });
    const [, init] = fetchFn.mock.calls[1] ?? [];
    expect(requestJsonBody(init).placement).toEqual({
      kind: 'coarse_local_period',
      local_date: '2026-09-16',
      period: 'afternoon',
    });
  });

  it('retains named-zone local intent and the server-resolved overlap instants', async () => {
    const request: TemporalScheduleRevisionRequest = {
      ...revisionRequest(),
      operationId: 'b02-e:revision:named-zone',
      placement: {
        kind: 'named-zone-local-interval',
        startsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:10'),
        endsLocalAt: Temporal.PlainDateTime.from('2026-10-25T02:40'),
        zoneId: 'Europe/Rome',
        disambiguation: 'later',
      },
    };
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          schedule_ref: SCHEDULE_REF,
          previous_placement_material_state_ref: CURRENT_STATE_REF,
          placement_material_state_ref: NEXT_STATE_REF,
          temporal_form: 'named_zone_local',
          starts_local_at: '2026-10-25T02:10:00',
          ends_local_at: '2026-10-25T02:40:00',
          zone_id: 'Europe/Rome',
          resolved_start_at: '2026-10-25T01:10:00Z',
          resolved_end_at: '2026-10-25T01:40:00Z',
          replayed: false,
        }),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    const result = await source.reviseSchedule(request);

    expect(result.placement).toMatchObject({
      kind: 'named-zone-local-interval',
      zoneId: 'Europe/Rome',
    });
    if (result.placement.kind !== 'named-zone-local-interval') {
      throw new Error('Expected named-zone placement.');
    }
    expect(result.placement.resolvedStartAt.toString()).toBe(
      '2026-10-25T01:10:00Z',
    );
    const [, init] = fetchFn.mock.calls[1] ?? [];
    expect(requestJsonBody(init).placement).toEqual({
      kind: 'named_zone_local_interval',
      starts_local_at: '2026-10-25T02:10:00',
      ends_local_at: '2026-10-25T02:40:00',
      zone_id: 'Europe/Rome',
      disambiguation: 'later',
    });
  });

  it('posts an exact unschedule command and preserves its operation receipt', async () => {
    const request: TemporalScheduleUnscheduleRequest = {
      operationId: 'b02-d:unschedule:1',
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: CURRENT_STATE_REF,
    };
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          schedule_ref: SCHEDULE_REF,
          previous_placement_material_state_ref: CURRENT_STATE_REF,
          unschedule_operation_id: request.operationId,
          replayed: false,
        }),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    await expect(source.unscheduleSchedule(request)).resolves.toEqual({
      scheduleRef: SCHEDULE_REF,
      previousPlacementMaterialStateRef: CURRENT_STATE_REF,
      unscheduleOperationId: request.operationId,
      replayed: false,
    });
    const [url, init] = fetchFn.mock.calls[1] ?? [];
    expect(url).toBe(`/api/v1/temporal/schedules/${SCHEDULE_REF}/unschedule`);
    expect(init?.method).toBe('POST');
    expect(requestJsonBody(init)).toEqual({
      operation_id: request.operationId,
      expected_placement_material_state_ref: CURRENT_STATE_REF,
    });
  });

  it('posts the exact unschedule receipt and accepts only a new restored state', async () => {
    const request: TemporalScheduleUnscheduleUndoRequest = {
      operationId: 'b02-d:undo:1',
      scheduleRef: SCHEDULE_REF,
      unscheduleOperationId: 'b02-d:unschedule:1',
    };
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({
          schedule_ref: SCHEDULE_REF,
          restored_from_placement_material_state_ref: CURRENT_STATE_REF,
          placement_material_state_ref: RESTORED_STATE_REF,
          temporal_form: 'floating_local',
          starts_local_at: '2026-09-09T10:00:00',
          ends_local_at: '2026-09-09T11:00:00',
          replayed: false,
        }),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    const result = await source.undoScheduleUnschedule(request);

    expect(result).toMatchObject({
      scheduleRef: SCHEDULE_REF,
      restoredFromPlacementMaterialStateRef: CURRENT_STATE_REF,
      placementMaterialStateRef: RESTORED_STATE_REF,
      replayed: false,
    });
    const [url, init] = fetchFn.mock.calls[1] ?? [];
    expect(url).toBe(
      `/api/v1/temporal/schedules/${SCHEDULE_REF}/unschedule/undo`,
    );
    expect(init?.method).toBe('POST');
    expect(requestJsonBody(init)).toEqual({
      operation_id: request.operationId,
      unschedule_operation_id: request.unscheduleOperationId,
    });
  });

  it('does not turn a guarded unschedule Undo conflict into success', async () => {
    const fetchFn = vi
      .fn<typeof globalThis.fetch>()
      .mockResolvedValueOnce(
        jsonResponse({ authenticated: true, csrf_token: 'csrf-token' }),
      )
      .mockResolvedValueOnce(
        jsonResponse({ code: 'temporal.schedule.undo_conflict' }, 409),
      );
    const source = createRemoteTemporalScheduleDataSource(fetchFn);

    await expect(
      source.undoScheduleUnschedule({
        operationId: 'b02-d:undo:conflict',
        scheduleRef: SCHEDULE_REF,
        unscheduleOperationId: 'b02-d:unschedule:1',
      }),
    ).rejects.toMatchObject({
      name: 'TemporalScheduleRemoteError',
      kind: 'http',
      status: 409,
      code: 'temporal.schedule.undo_conflict',
    } satisfies Partial<TemporalScheduleRemoteError>);
  });
});
