import { describe, expect, it, vi } from 'vitest';

import {
  ScheduleReminderRemoteError,
  createRemoteScheduleReminderDataSource,
} from './remote-schedule-reminder-data-source';

const SCHEDULE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const REMINDER = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e';
const STATE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';

const canonical = {
  reminder_ref: REMINDER,
  schedule_ref: SCHEDULE,
  material_state_ref: STATE,
  enabled: true,
  lead_minutes: 15,
  schedule_starts_at: '2026-10-10T10:00:00Z',
  due_at: '2026-10-10T09:45:00Z',
  disposition_code: 'pending',
  replayed: false,
};

function json(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': status >= 400 ? 'application/problem+json' : 'application/json' },
  });
}

describe('remote Schedule Reminder', () => {
  it('reads canonical due disposition and distinguishes an absent Reminder', async () => {
    const fetcher = vi.fn<typeof fetch>()
      .mockResolvedValueOnce(json(canonical))
      .mockResolvedValueOnce(json({ code: 'temporal.reminder.schedule_unavailable' }, 404));
    const source = createRemoteScheduleReminderDataSource(fetcher);
    const view = await source.get(SCHEDULE);
    expect(view).toMatchObject({
      reminderRef: REMINDER, scheduleRef: SCHEDULE, materialStateRef: STATE,
      dueAt: canonical.due_at, disposition: 'pending',
    });
    expect(await source.get(SCHEDULE)).toBeNull();
    expect(fetcher).toHaveBeenCalledWith(
      `/api/v1/temporal/schedules/${SCHEDULE}/reminder`, expect.anything(),
    );
  });

  it('sends a guarded command with CSRF and exact expected state', async () => {
    const fetcher = vi.fn<typeof fetch>()
      .mockResolvedValueOnce(json({ authenticated: true, csrf_token: 'csrf-value' }))
      .mockResolvedValueOnce(json({ ...canonical, replayed: true }));
    const result = await createRemoteScheduleReminderDataSource(fetcher).configure(
      SCHEDULE,
      { operationId: 'b11c:configure', expectedMaterialStateRef: STATE, enabled: true, leadMinutes: 15 },
    );
    expect(result.replayed).toBe(true);
    const request = fetcher.mock.calls[1];
    expect(request?.[1]).toMatchObject({ method: 'PUT' });
    expect((request?.[1]?.headers as Headers).get('X-Dante-CSRF')).toBe('csrf-value');
    expect(JSON.parse(String(request?.[1]?.body))).toEqual({
      operation_id: 'b11c:configure', expected_material_state_ref: STATE,
      enabled: true, lead_minutes: 15,
    });
  });

  it('rejects a fabricated delivery claim and leaves conflict visible', async () => {
    const invalid = vi.fn<typeof fetch>().mockResolvedValue(json({
      ...canonical, disposition_code: 'sent',
    }));
    await expect(createRemoteScheduleReminderDataSource(invalid).get(SCHEDULE))
      .rejects.toBeInstanceOf(ScheduleReminderRemoteError);
    const conflict = vi.fn<typeof fetch>()
      .mockResolvedValueOnce(json({ authenticated: true, csrf_token: 'csrf-value' }))
      .mockResolvedValueOnce(json({ code: 'temporal.reminder.conflict', detail: 'Stale' }, 409));
    await expect(createRemoteScheduleReminderDataSource(conflict).configure(
      SCHEDULE, { operationId: 'b11c:stale', expectedMaterialStateRef: STATE, enabled: false, leadMinutes: 15 },
    )).rejects.toMatchObject({ status: 409, code: 'temporal.reminder.conflict' });
  });
});
