import { describe, expect, it, vi } from 'vitest';

import { createRemoteActivityEditSettings } from './remote-activity-edit-settings';

const ref = '0199a111-1111-7111-8111-111111111111';
const response = (body: unknown, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });

describe('Activity editor settings remote contract', () => {
  it('loads canonical policies and schedules, then sends state guarded updates', async () => {
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
        if (init?.method === 'POST') {
          if (typeof init.body !== 'string')
            throw new Error('Expected JSON body');
          requests.push(JSON.parse(init.body) as Record<string, unknown>);
          expect(new Headers(init.headers).get('X-Dante-CSRF')).toBe('token');
          return Promise.resolve(
            response(
              path.endsWith('execution-policy')
                ? {
                    activity_ref: ref,
                    mode_code: 'live',
                    state_ref: 'new-capture',
                  }
                : {
                    subject_kind: 'activity',
                    subject_native_ref: ref,
                    mode_code: 'review_on_end',
                    state_ref: 'new-reality',
                  },
              201,
            ),
          );
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
              reminder: null,
              schedules: [
                {
                  schedule_ref: 'schedule',
                  role_code: 'interval',
                  display_name: 'Mattina',
                  presentation_order: 1,
                  placement_material_state_ref: 'placement',
                  temporal_form: 'floating_local',
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
      role: 'interval',
      name: 'Mattina',
      start: '2026-10-07T09:00:00',
    });
    expect(
      await source.setCapture(ref, settings.capture, 'live', 'op-capture'),
    ).toEqual({ mode: 'live', stateRef: 'new-capture' });
    expect(
      await source.setReality(
        ref,
        settings.reality,
        'review_on_end',
        'op-reality',
      ),
    ).toEqual({ mode: 'review_on_end', stateRef: 'new-reality' });
    expect(requests).toEqual([
      {
        operation_id: 'op-capture',
        mode_code: 'live',
        expected_state_ref: 'old-capture',
      },
      {
        operation_id: 'op-reality',
        mode_code: 'review_on_end',
        expected_state_ref: 'old-reality',
      },
    ]);
  });
});
