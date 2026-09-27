import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type ScheduleReminderView = Readonly<{
  reminderRef: string;
  scheduleRef: string;
  materialStateRef: string;
  enabled: boolean;
  leadMinutes: number;
  scheduleStartsAt: string | null;
  dueAt: string | null;
  disposition: 'pending' | 'due' | 'unavailable';
  replayed: boolean;
}>;

export class ScheduleReminderRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'ScheduleReminderRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new ScheduleReminderRemoteError('protocol', 'Invalid Reminder response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new ScheduleReminderRemoteError('protocol', `Invalid ${field}.`);
  }
  return value.toLowerCase();
}

function instant(value: unknown, field: string): string | null {
  if (value === null) return null;
  if (typeof value !== 'string' || !Number.isFinite(Date.parse(value))) {
    throw new ScheduleReminderRemoteError('protocol', `Invalid ${field}.`);
  }
  return value;
}

function reminder(value: unknown): ScheduleReminderView {
  const payload = record(value);
  if (
    typeof payload.enabled !== 'boolean' ||
    typeof payload.replayed !== 'boolean' ||
    typeof payload.lead_minutes !== 'number' ||
    !Number.isInteger(payload.lead_minutes) ||
    payload.lead_minutes < 0 ||
    payload.lead_minutes > 10080 ||
    (payload.disposition_code !== 'pending' &&
      payload.disposition_code !== 'due' &&
      payload.disposition_code !== 'unavailable')
  ) {
    throw new ScheduleReminderRemoteError('protocol', 'Invalid Reminder configuration.');
  }
  const starts = instant(payload.schedule_starts_at, 'schedule start');
  const due = instant(payload.due_at, 'due instant');
  if (
    (payload.enabled && starts !== null && due === null) ||
    ((!payload.enabled || starts === null) && due !== null) ||
    (payload.disposition_code !== 'unavailable' && due === null)
  ) {
    throw new ScheduleReminderRemoteError('protocol', 'Inconsistent Reminder disposition.');
  }
  return Object.freeze({
    reminderRef: uuid(payload.reminder_ref, 'reminder_ref'),
    scheduleRef: uuid(payload.schedule_ref, 'schedule_ref'),
    materialStateRef: uuid(payload.material_state_ref, 'material_state_ref'),
    enabled: payload.enabled,
    leadMinutes: payload.lead_minutes,
    scheduleStartsAt: starts,
    dueAt: due,
    disposition: payload.disposition_code,
    replayed: payload.replayed,
  });
}

export function createRemoteScheduleReminderDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function problem(response: Response): Promise<ScheduleReminderRemoteError> {
    let payload: Record<string, unknown> = {};
    try {
      payload = record(await response.json());
    } catch {
      return new ScheduleReminderRemoteError('http', 'Reminder request rejected.', response.status);
    }
    return new ScheduleReminderRemoteError(
      'http',
      typeof payload.detail === 'string' ? payload.detail : 'Reminder request rejected.',
      response.status,
      typeof payload.code === 'string' ? payload.code : null,
    );
  }

  async function csrf(): Promise<string> {
    let response: Response;
    try {
      response = await webFetch('/api/v1/auth/session');
    } catch (error) {
      throw new ScheduleReminderRemoteError(
        'transport', error instanceof Error ? error.message : 'Session unavailable.',
      );
    }
    const payload = record(await response.json());
    if (
      !response.ok || payload.authenticated !== true ||
      typeof payload.csrf_token !== 'string' || !payload.csrf_token
    ) {
      throw new ScheduleReminderRemoteError(
        'authentication', 'Reminder requires an authenticated session.', response.status,
      );
    }
    return payload.csrf_token;
  }

  function endpoint(scheduleRef: string): string {
    return `/api/v1/temporal/schedules/${encodeURIComponent(uuid(scheduleRef, 'schedule_ref'))}/reminder`;
  }

  return Object.freeze({
    async get(scheduleRef: string): Promise<ScheduleReminderView | null> {
      let response: Response;
      try {
        response = await webFetch(endpoint(scheduleRef));
      } catch (error) {
        throw new ScheduleReminderRemoteError(
          'transport', error instanceof Error ? error.message : 'Reminder unavailable.',
        );
      }
      if (!response.ok) {
        const error = await problem(response);
        if (response.status === 404 && error.code === 'temporal.reminder.schedule_unavailable') {
          return null;
        }
        throw error;
      }
      return reminder(await response.json());
    },

    async configure(
      scheduleRef: string,
      command: Readonly<{
        operationId: string;
        expectedMaterialStateRef: string | null;
        enabled: boolean;
        leadMinutes: number;
      }>,
    ): Promise<ScheduleReminderView> {
      if (!Number.isInteger(command.leadMinutes) || command.leadMinutes < 0 ||
          command.leadMinutes > 10080 || !command.operationId.trim()) {
        throw new ScheduleReminderRemoteError('protocol', 'Invalid Reminder command.');
      }
      let response: Response;
      try {
        response = await webFetch(endpoint(scheduleRef), {
          method: 'PUT',
          headers: new Headers({
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          }),
          body: JSON.stringify({
            operation_id: command.operationId,
            expected_material_state_ref: command.expectedMaterialStateRef === null
              ? null : uuid(command.expectedMaterialStateRef, 'expected_material_state_ref'),
            enabled: command.enabled,
            lead_minutes: command.leadMinutes,
          }),
        });
      } catch (error) {
        if (error instanceof ScheduleReminderRemoteError) throw error;
        throw new ScheduleReminderRemoteError(
          'transport', error instanceof Error ? error.message : 'Reminder unavailable.',
        );
      }
      if (!response.ok) throw await problem(response);
      return reminder(await response.json());
    },
  });
}
