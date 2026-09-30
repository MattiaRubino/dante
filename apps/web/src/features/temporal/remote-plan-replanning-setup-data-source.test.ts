import { expect, it, vi } from 'vitest';

import { createRemotePlanReplanningSetupDataSource } from './remote-plan-replanning-setup-data-source';

const scheduleRef = '0199a8c0-5e74-7bc0-8ad0-a2f403f56185';
const policyStateRef = '0199a8c0-5e74-7bc0-8ad0-a2f403f56187';
const activityRef = '0199a8c0-5e74-7bc0-8ad0-a2f403f56184';

it('sends self-scoped Policy CAS and an Activity hard boundary through CSRF writes', async () => {
  const fetchFn = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    if (url.endsWith('/api/v1/auth/session')) {
      return new Response(JSON.stringify({ authenticated: true, csrf_token: 'csrf' }));
    }
    if (url.endsWith(`/schedules/${scheduleRef}/movement-policy`)) {
      return new Response(JSON.stringify({
        schedule_ref: scheduleRef, material_state_ref: policyStateRef,
      }));
    }
    if (url.endsWith(`/schedules/${scheduleRef}/placement`)) {
      return new Response(JSON.stringify({
        schedule_ref: scheduleRef, temporal_form: 'absolute',
      }));
    }
    return new Response(JSON.stringify({
      subject_ref: activityRef, constraint_ref: 'constraint',
    }));
  });
  const source = createRemotePlanReplanningSetupDataSource(fetchFn as typeof fetch);
  await source.requireConfirmation(scheduleRef, null);
  await source.setEarliestStart(activityRef, '2026-10-02T11:00:00.000Z');
  await source.makeScheduleAbsolute(
    scheduleRef, policyStateRef,
    '2026-10-02T10:00:00.000Z', '2026-10-02T11:00:00.000Z',
  );

  const policy = fetchFn.mock.calls[1]!;
  expect(policy[1]?.method).toBe('PUT');
  expect(new Headers(policy[1]?.headers).get('X-Dante-CSRF')).toBe('csrf');
  expect(JSON.parse(String(policy[1]?.body))).toMatchObject({
    expected_material_state_ref: null,
    automatic_movement: 'automatic', acceptance_path: 'confirmation_required',
  });
  const constraint = fetchFn.mock.calls[3]!;
  expect(constraint[1]?.method).toBe('POST');
  expect(JSON.parse(String(constraint[1]?.body))).toMatchObject({
    subject_ref: activityRef,
    rule: { boundary_kind: 'earliest_start', strength: 'hard',
      boundary_at: '2026-10-02T11:00:00.000Z' },
  });
  const fixed = fetchFn.mock.calls[5]!;
  expect(fixed[1]?.method).toBe('PATCH');
  expect(JSON.parse(String(fixed[1]?.body))).toMatchObject({
    expected_placement_material_state_ref: policyStateRef,
    placement: { kind: 'absolute_interval', starts_at: '2026-10-02T10:00:00.000Z' },
  });
});
