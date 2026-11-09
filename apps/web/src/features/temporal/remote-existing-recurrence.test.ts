import { describe, expect, it, vi } from 'vitest';

import { createRemoteExistingRecurrence } from './remote-existing-recurrence';

const EVENT = '0199a111-1111-7111-8111-111111111111';
const SOURCE = '0199a222-2222-7222-8222-222222222222';
const SCHEDULE = '0199a333-3333-7333-8333-333333333333';
const MATERIAL = '0199a444-4444-7444-8444-444444444444';

const recurrence = {
  family_code: 'calendar_wall_clock',
  range_kind: 'open',
  expected_occurrence_count: null,
  effective_from: '2027-01-02',
  effective_until: null,
  pattern_code: 'daily',
  interval_count: 1,
  clock_basis_code: 'named_zone',
  zone_id: 'Europe/Rome',
  pattern_anchor_date: null,
  wall_times: ['09:00:00'],
  weekdays: [],
  month_days: [],
  ordinal_weekdays: [],
  year_month_days: [],
  nonexistent_local_time_policy: 'skip_civil_candidate',
  ambiguous_local_time_policy: 'earlier',
  step_unit_code: null,
} as const;

describe('Existing Event recurrence Start response', () => {
  it('uses the accepted source identity without a subsequent seed lookup', async () => {
    const fetchFn = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(
        Response.json({ authenticated: true, csrf_token: 'csrf-test' }),
      )
      .mockResolvedValueOnce(
        Response.json({
          owner_kind: 'event',
          source_ref: SOURCE,
          title: 'Visita',
          created_at: '2027-01-02T09:00:00Z',
          recurrence_material_state_ref: MATERIAL,
          replayed: false,
        }),
      );
    const remote = createRemoteExistingRecurrence(fetchFn);
    const sourceRef = await remote.startEvent(
      {
        eventRef: EVENT,
        expectedProfileRevision: 3,
        scheduleRef: SCHEDULE,
        expectedPlacementStateRef: MATERIAL,
      },
      recurrence,
      'conversion:operation:1',
    );

    expect(sourceRef).toBe(SOURCE);
    expect(fetchFn).toHaveBeenCalledTimes(2);
    expect(fetchFn.mock.calls[0]?.[0]).toBe('/api/v1/auth/session');
    const [url, init] = fetchFn.mock.calls[1] ?? [];
    expect(url).toBe(`/api/v1/temporal/recurring/events/${EVENT}/start`);
    expect(init?.method).toBe('POST');
    expect(init?.credentials).toBe('same-origin');
    expect(new Headers(init?.headers).get('X-Dante-CSRF')).toBe('csrf-test');
    // BodyInit also permits Blob/FormData; never silently stringify one
    // into "[object Object]" when asserting the authored JSON command.
    const requestBody: unknown = init?.body;
    expect(typeof requestBody).toBe('string');
    if (typeof requestBody !== 'string') {
      throw new Error('The recurrence command must send a JSON string body.');
    }
    const body: unknown = JSON.parse(requestBody);
    expect(body).toMatchObject({
      operation_id: 'conversion:operation:1',
      expected_profile_revision: 3,
      schedule_ref: SCHEDULE,
      expected_placement_state_ref: MATERIAL,
      recurrence: expect.objectContaining({
        family_code: 'calendar_wall_clock',
      }),
    });
  });

  it('rejects a response without a confirmed Event series source', async () => {
    const fetchFn = vi
      .fn<typeof fetch>()
      .mockResolvedValueOnce(
        Response.json({ authenticated: true, csrf_token: 'csrf-test' }),
      )
      .mockResolvedValueOnce(
        Response.json({ owner_kind: 'event', source_ref: null }),
      );
    const remote = createRemoteExistingRecurrence(fetchFn);
    await expect(
      remote.startEvent(
        {
          eventRef: EVENT,
          expectedProfileRevision: 3,
          scheduleRef: SCHEDULE,
          expectedPlacementStateRef: MATERIAL,
        },
        recurrence,
        'conversion:invalid-response',
      ),
    ).rejects.toThrow('Conferma della serie Event non valida.');
    expect(fetchFn).toHaveBeenCalledTimes(2);
  });
});
