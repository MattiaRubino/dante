import { createWebFetch } from '../../platform/api/web-fetch';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type ScheduleMovementPolicyResult = Readonly<{
  scheduleRef: string;
  materialStateRef: string;
  replayed: boolean;
}>;

export class ScheduleMovementPolicyRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'ScheduleMovementPolicyRemoteError';
  }
}

function object(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new ScheduleMovementPolicyRemoteError(
      'protocol',
      'Invalid Movement Policy response.',
    );
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID.test(value)) {
    throw new ScheduleMovementPolicyRemoteError(
      'protocol',
      `Invalid ${field}.`,
    );
  }
  return value.toLowerCase();
}

function result(value: unknown): ScheduleMovementPolicyResult {
  const row = object(value);
  return Object.freeze({
    scheduleRef: uuid(row.schedule_ref, 'schedule_ref'),
    materialStateRef: uuid(row.material_state_ref, 'material_state_ref'),
    replayed: row.replayed === true,
  });
}

export function createRemoteScheduleMovementPolicyDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    const row = object(await response.json());
    if (
      !response.ok ||
      row.authenticated !== true ||
      typeof row.csrf_token !== 'string' ||
      !row.csrf_token
    ) {
      throw new ScheduleMovementPolicyRemoteError(
        'authentication',
        'Movement Policy requires an authenticated session.',
        response.status,
      );
    }
    return row.csrf_token;
  }

  async function problem(
    response: Response,
  ): Promise<ScheduleMovementPolicyRemoteError> {
    try {
      const row = object(await response.json());
      return new ScheduleMovementPolicyRemoteError(
        'http',
        typeof row.detail === 'string'
          ? row.detail
          : 'Movement Policy request rejected.',
        response.status,
        typeof row.code === 'string' ? row.code : null,
      );
    } catch {
      return new ScheduleMovementPolicyRemoteError(
        'http',
        'Movement Policy request rejected.',
        response.status,
      );
    }
  }

  return Object.freeze({
    async protect(
      scheduleRef: string,
      operationId: string,
    ): Promise<ScheduleMovementPolicyResult> {
      const normalizedScheduleRef = uuid(scheduleRef, 'schedule_ref');
      if (!operationId.trim()) {
        throw new ScheduleMovementPolicyRemoteError(
          'protocol',
          'Invalid Movement Policy operation id.',
        );
      }
      let response: Response;
      try {
        response = await webFetch(
          `/api/v1/temporal/schedules/${encodeURIComponent(normalizedScheduleRef)}/movement-policy`,
          {
            method: 'PUT',
            headers: new Headers({
              'Content-Type': 'application/json',
              'X-Dante-CSRF': await csrf(),
            }),
            body: JSON.stringify({
              operation_id: operationId,
              expected_material_state_ref: null,
              automatic_movement: 'blocked',
              acceptance_path: 'direct',
            }),
          },
        );
      } catch (error) {
        if (error instanceof ScheduleMovementPolicyRemoteError) throw error;
        throw new ScheduleMovementPolicyRemoteError(
          'transport',
          error instanceof Error ? error.message : 'Movement Policy unavailable.',
        );
      }
      if (!response.ok) throw await problem(response);
      return result(await response.json());
    },
  });
}
