import { fetchRequestBody } from '../../../test-support/fetch-request';
import { describe, expect, it, vi } from 'vitest';

import { createRemoteRecurringAuthoringDataSource } from './remote-recurring-authoring';

const eventRef = '0199a111-1111-7111-8111-111111111111';
const stateRef = '0199a222-2222-7222-8222-222222222222';

const response = (body: unknown): Response =>
  Response.json(body, { headers: { 'Content-Type': 'application/json' } });

describe('Recurring Event Create placement-lock contract', () => {
  it.each([true, false] as const)(
    'sends placement_protected=%s only in the authenticated Create command',
    async (locked) => {
      const fetchFn = vi
        .fn<typeof fetch>()
        .mockResolvedValueOnce(
          response({ authenticated: true, csrf_token: 'csrf-recurring-event' }),
        )
        .mockResolvedValueOnce(
          response({
            owner_kind: 'event',
            source_ref: eventRef,
            title: 'Riunione',
            created_at: '2027-01-02T08:00:00Z',
            recurrence_material_state_ref: stateRef,
            replayed: false,
          }),
        );
      const remote = createRemoteRecurringAuthoringDataSource(fetchFn);

      const created = await remote.createEvent({
        operationId: 'event:create:lock',
        title: 'Riunione',
        recurrence: {
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
        },
        placementKind: 'timed',
        durationMinutes: 30,
        placementProtected: locked,
      });

      expect(created.sourceRef).toBe(eventRef);
      expect(created.ownerKind).toBe('event');
      expect(fetchFn).toHaveBeenCalledTimes(2);
      expect(fetchFn.mock.calls[0]?.[0]).toBe('/api/v1/auth/session');

      const [url, request] = fetchFn.mock.calls[1] ?? [];
      expect(url).toBe('/api/v1/temporal/recurring/events');
      expect(request?.method).toBe('POST');
      expect(request?.credentials).toBe('same-origin');
      const headers = new Headers(request?.headers);
      expect(headers.get('X-Dante-CSRF')).toBe('csrf-recurring-event');
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('X-Dante-Time-Zone')).toBeTruthy();
      const body = JSON.parse(fetchRequestBody(request?.body)) as Record<
        string,
        unknown
      >;
      expect(body).toMatchObject({
        operation_id: 'event:create:lock',
        title: 'Riunione',
        placement_kind: 'timed',
        duration_minutes: 30,
        placement_protected: locked,
      });
      expect(
        Object.keys(body).filter((key) => key === 'placement_protected'),
      ).toEqual(['placement_protected']);
    },
  );
});
