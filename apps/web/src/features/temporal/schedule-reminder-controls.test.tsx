import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../bootstrap/i18n';
import { ScheduleReminderControls } from './schedule-reminder-controls';

const SCHEDULE = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const REMINDER = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e';
const STATE_1 = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';
const STATE_2 = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';

function json(body: unknown, status = 200): Response {
  return Response.json(body, { status });
}

describe('Schedule Reminder controls', () => {
  beforeAll(async () => {
    await i18n.changeLanguage('it');
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
  });

  it('retries an uncertain write with the same operation and exact expected state', async () => {
    const writes: Array<Record<string, unknown>> = [];
    let attempts = 0;
    const fetchFn = vi.fn<typeof fetch>(async (input, init) => {
      const url = String(input);
      if (url.endsWith('/api/v1/auth/session')) {
        return json({ authenticated: true, csrf_token: 'csrf' });
      }
      if (url.endsWith(`/schedules/${SCHEDULE}/reminder`)) {
        if (init?.method === 'PUT') {
          writes.push(JSON.parse(String(init.body)) as Record<string, unknown>);
          attempts += 1;
          if (attempts === 1) {
            return json({ code: 'temporal.reminder.unavailable', detail: 'Retry' }, 503);
          }
          return json({
            reminder_ref: REMINDER,
            schedule_ref: SCHEDULE,
            material_state_ref: STATE_2,
            enabled: true,
            lead_minutes: 30,
            schedule_starts_at: '2026-10-10T10:00:00Z',
            due_at: '2026-10-10T09:30:00Z',
            disposition_code: 'pending',
            replayed: false,
          });
        }
        return json({
          reminder_ref: REMINDER,
          schedule_ref: SCHEDULE,
          material_state_ref: STATE_1,
          enabled: true,
          lead_minutes: 15,
          schedule_starts_at: '2026-10-10T10:00:00Z',
          due_at: '2026-10-10T09:45:00Z',
          disposition_code: 'pending',
          replayed: false,
        });
      }
      throw new Error(`Unexpected request: ${url}`);
    });
    vi.stubGlobal('fetch', fetchFn);

    render(<ScheduleReminderControls scheduleRef={SCHEDULE} />);
    await screen.findByText(/In attesa/);
    fireEvent.change(screen.getByLabelText('Minuti prima dell’inizio'), {
      target: { value: '30' },
    });
    fireEvent.click(screen.getByText('Salva promemoria'));
    await screen.findByRole('alert');
    await waitFor(() => {
      expect(
        (screen.getByRole('button', { name: 'Salva promemoria' }) as HTMLButtonElement)
          .disabled,
      ).toBe(false);
    });
    fireEvent.click(screen.getByText('Salva promemoria'));

    await waitFor(() => expect(writes).toHaveLength(2));
    expect(writes[0]).toEqual(writes[1]);
    expect(writes[1]).toMatchObject({
      operation_id: expect.any(String),
      expected_material_state_ref: STATE_1,
      enabled: true,
      lead_minutes: 30,
    });
    await waitFor(() => expect(screen.queryByRole('alert')).toBeNull());
    expect(screen.getByRole('status').textContent).toContain('In attesa');
  });
});
