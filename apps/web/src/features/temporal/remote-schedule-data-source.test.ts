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
    expect(result.placement.startsLocalAt.toString()).toBe(
      '2026-09-09T14:00:00',
    );
    expect(fetchFn).toHaveBeenCalledTimes(2);
    const [url, init] = fetchFn.mock.calls[1] ?? [];
    expect(url).toBe(`/api/v1/temporal/schedules/${SCHEDULE_REF}/placement`);
    expect(init?.method).toBe('PATCH');
    expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf-token');
    expect(JSON.parse(String(init?.body))).toEqual({
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

  it('fails locally for cross-day/coarse input before requesting a session', async () => {
    const fetchFn = vi.fn<typeof globalThis.fetch>();
    const source = createRemoteTemporalScheduleDataSource(fetchFn);
    const request = revisionRequest();

    await expect(
      source.reviseSchedule({
        ...request,
        placement: {
          ...request.placement,
          endsLocalAt: Temporal.PlainDateTime.from('2026-09-10T00:30'),
        },
      }),
    ).rejects.toThrow(RangeError);
    expect(fetchFn).not.toHaveBeenCalled();
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
    expect(JSON.parse(String(init?.body))).toEqual({
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
    expect(JSON.parse(String(init?.body))).toEqual({
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
