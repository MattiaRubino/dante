import { createWebFetch } from '../../platform/api/web-fetch';

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type ActivityRealityMode =
  | 'manual'
  | 'review_on_end'
  | 'auto_confirm_outcome';

export type ActivityRealityPolicy = Readonly<{
  activityRef: string;
  stateRef: string | null;
  mode: ActivityRealityMode;
  replayed: boolean;
}>;

export class ActivityRealityPolicyRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'ActivityRealityPolicyRemoteError';
  }
}

function object(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new ActivityRealityPolicyRemoteError('protocol', 'Invalid Reality policy response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID.test(value)) {
    throw new ActivityRealityPolicyRemoteError('protocol', `Invalid ${field}.`);
  }
  return value.toLowerCase();
}

function policy(value: unknown): ActivityRealityPolicy {
  const row = object(value);
  if (
    row.mode_code !== 'manual' &&
    row.mode_code !== 'review_on_end' &&
    row.mode_code !== 'auto_confirm_outcome'
  ) {
    throw new ActivityRealityPolicyRemoteError('protocol', 'Invalid Reality policy mode.');
  }
  return Object.freeze({
    activityRef: uuid(row.activity_ref, 'activity_ref'),
    stateRef: row.state_ref === null ? null : uuid(row.state_ref, 'state_ref'),
    mode: row.mode_code,
    replayed: row.replayed === true,
  });
}

export function createRemoteActivityRealityPolicyDataSource(
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
      throw new ActivityRealityPolicyRemoteError(
        'authentication',
        'Reality policy requires an authenticated session.',
        response.status,
      );
    }
    return row.csrf_token;
  }

  async function problem(response: Response): Promise<ActivityRealityPolicyRemoteError> {
    try {
      const row = object(await response.json());
      return new ActivityRealityPolicyRemoteError(
        'http',
        typeof row.detail === 'string' ? row.detail : 'Reality policy request rejected.',
        response.status,
        typeof row.code === 'string' ? row.code : null,
      );
    } catch {
      return new ActivityRealityPolicyRemoteError(
        'http',
        'Reality policy request rejected.',
        response.status,
      );
    }
  }

  const endpoint = (activityRef: string) =>
    `/api/v1/temporal/activities/${encodeURIComponent(uuid(activityRef, 'activity_ref'))}/outcome-review-policy`;

  return Object.freeze({
    async get(activityRef: string): Promise<ActivityRealityPolicy> {
      let response: Response;
      try {
        response = await webFetch(endpoint(activityRef));
      } catch (error) {
        throw new ActivityRealityPolicyRemoteError(
          'transport',
          error instanceof Error ? error.message : 'Reality policy unavailable.',
        );
      }
      if (!response.ok) throw await problem(response);
      return policy(await response.json());
    },

    async configure(
      activityRef: string,
      command: Readonly<{
        operationId: string;
        mode: ActivityRealityMode;
        expectedStateRef?: string | null;
      }>,
    ): Promise<ActivityRealityPolicy> {
      if (!command.operationId.trim()) {
        throw new ActivityRealityPolicyRemoteError('protocol', 'Invalid Reality policy command.');
      }
      let response: Response;
      try {
        response = await webFetch(endpoint(activityRef), {
          method: 'POST',
          headers: new Headers({
            'Content-Type': 'application/json',
            'X-Dante-CSRF': await csrf(),
          }),
          body: JSON.stringify({
            operation_id: command.operationId,
            mode_code: command.mode,
            expected_state_ref:
              command.expectedStateRef == null
                ? null
                : uuid(command.expectedStateRef, 'expected_state_ref'),
          }),
        });
      } catch (error) {
        if (error instanceof ActivityRealityPolicyRemoteError) throw error;
        throw new ActivityRealityPolicyRemoteError(
          'transport',
          error instanceof Error ? error.message : 'Reality policy unavailable.',
        );
      }
      if (!response.ok) throw await problem(response);
      return policy(await response.json());
    },
  });
}
