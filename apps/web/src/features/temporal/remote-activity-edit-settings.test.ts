import { describe, expect, it, vi } from 'vitest';

import { createRemoteActivityEditSettings } from './remote-activity-edit-settings';

const ref = '0199a111-1111-7111-8111-111111111111';
const response = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

describe('Activity editor settings remote contract', () => {
  it('loads one snapshot and saves core changes in one guarded request', async () => {
    const paths: string[] = [];
    const requests: Record<string, unknown>[] = [];
    const fetchFn = vi.fn(
      (input: RequestInfo | URL, init?: RequestInit): Promise<Response> => {
        const path =
          typeof input === 'string'
            ? input
            : input instanceof URL
              ? input.href
              : input.url;
        paths.push(path);
        if (init?.method === 'PUT') {
          if (typeof init.body !== 'string') throw new Error('Expected JSON body');
          expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('token');
          requests.push(JSON.parse(init.body) as Record<string, unknown>);
          return Promise.resolve(response({
            profile: { activity_ref: ref, title: 'Dopo', description: null,
              location: null, color_code: null, revision: 2 },
            capture: { activity_ref: ref, mode_code: 'live', state_ref: 'new-capture' },
            reality: { subject_kind: 'activity', subject_native_ref: ref,
              mode_code: 'review_on_end', state_ref: 'new-reality' },
            reminder: { schedule_ref: 'schedule', material_state_ref: 'new-reminder',
              enabled: true, lead_minutes: 30 },
          }));
        }
        if (path.endsWith('/auth/session'))
          return Promise.resolve(
            response({ authenticated: true, csrf_token: 'token' }),
          );
        if (path.endsWith('/edit-snapshot'))
          return Promise.resolve(
            response({
              activity_ref: ref,
              execution_policy: { activity_ref: ref, mode_code: 'disabled', state_ref: 'old-capture' },
              reality_policy: { subject_kind: 'activity', subject_native_ref: ref,
                mode_code: 'manual', state_ref: 'old-reality' },
              child_guard_mode: 'none',
              life_area_ref: null,
              objectives: [],
              placement_lock: null,
              reminder: { schedule_ref: 'schedule', material_state_ref: 'old-reminder',
                enabled: true, lead_minutes: 15 },
              schedules: [
                {
                  schedule_ref: 'schedule',
                  role_code: 'envelope',
                  display_name: 'Mattina',
                  presentation_order: 1,
                  placement_material_state_ref: 'placement',
                  temporal_form: 'named_zone_local',
                  zone_id: 'Europe/Rome',
                  starts_local_at: '2026-10-07T09:00:00',
                  ends_local_at: '2026-10-07T10:00:00',
                },
              ],
            }),
          );
        throw new Error(`Unexpected path ${path}`);
      },
    );
    const source = createRemoteActivityEditSettings(fetchFn);
    const settings = await source.load(ref);
    expect(paths).toEqual([`/api/v1/temporal/activities/${ref}/edit-snapshot`]);
    expect(settings.schedules[0]).toMatchObject({
      role: 'envelope',
      name: 'Mattina',
      start: '2026-10-07T09:00:00',
    });
    const saved = await source.saveCore({ activityRef: ref, title: 'Prima',
      description: null, location: null, colorCode: null, revision: 1 },
    settings, { profile: { title: 'Dopo', description: null, location: null,
      colorCode: null }, capture: 'live', reality: 'review_on_end',
      reminderLeadMinutes: 30 }, 'edit-op');
    expect(saved.profile).toMatchObject({ title: 'Dopo', revision: 2 });
    expect(saved.settings.capture).toEqual({ mode: 'live', stateRef: 'new-capture' });
    expect(saved.settings.reminderStateRef).toBe('new-reminder');
    expect(requests[0]).toEqual({
      operation_id: 'edit-op',
      profile: { expected_revision: 1, title: 'Dopo', description: null,
        location: null, color_code: null },
      capture: { mode_code: 'live', expected_state_ref: 'old-capture' },
      reality: { mode_code: 'review_on_end', expected_state_ref: 'old-reality' },
      reminder: { schedule_ref: 'schedule', expected_state_ref: 'old-reminder',
        enabled: true, lead_minutes: 30 },
    });
  });

  it('updates Activity placement protection through the canonical CAS endpoint', async () => {
    const received: Record<string, unknown>[] = [];
    const fetchFn = vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const path = typeof input === 'string' ? input :
        input instanceof URL ? input.href : input.url;
      if (path.endsWith('/edit-snapshot')) return Promise.resolve(response({
        activity_ref: ref,
        execution_policy: { activity_ref: ref, mode_code: 'disabled', state_ref: null },
        reality_policy: { subject_kind: 'activity', subject_native_ref: ref,
          mode_code: 'manual', state_ref: null },
        child_guard_mode: 'none',
        life_area_ref: null,
        objectives: [],
        placement_lock: { schedule_ref: 'schedule', locked: false, revision: 3 },
        reminder: null,
        schedules: [{ schedule_ref: 'schedule', role_code: 'envelope',
          display_name: null, presentation_order: 0,
          placement_material_state_ref: 'state', temporal_form: 'named_zone_local',
          zone_id: 'Europe/Rome', starts_local_at: '2026-10-08T09:00:00',
          ends_local_at: '2026-10-08T10:00:00' }],
      }));
      if (path.endsWith('/auth/session'))
        return Promise.resolve(response({ authenticated: true, csrf_token: 'token' }));
      if (path.endsWith('/placement-lock') && init?.method === 'PUT') {
        received.push(JSON.parse(String(init.body)) as Record<string, unknown>);
        expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('token');
        return Promise.resolve(response({
          schedule_ref: 'schedule', locked: true, revision: 4,
          updated_at: '2026-10-08T09:00:00Z', replayed: false,
        }));
      }
      throw new Error(`Unexpected path: ${path}`);
    });
    const source = createRemoteActivityEditSettings(fetchFn);
    const before = await source.load(ref);
    expect(before.placementLockRevision).toBe(3);
    const after = await source.setPlacementProtected(before, true);
    expect(received).toEqual([{ locked: true, expected_revision: 3 }]);
    expect(after.placementProtected).toBe(true);
    expect(after.placementLockRevision).toBe(4);
  });
});
