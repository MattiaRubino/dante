import { createWebFetch } from '../../platform/api/web-fetch';

export type TemporalSessionCapabilityDataSource = Readonly<{
  activityEnabled: (activityRef: string, signal?: AbortSignal) => Promise<boolean>;
}>;

export class TemporalSessionCapabilityRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol',
    message: string,
    readonly status: number | null = null,
  ) {
    super(message);
    this.name = 'TemporalSessionCapabilityRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> | null {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : null;
}

export function createRemoteTemporalSessionCapabilityDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
): TemporalSessionCapabilityDataSource {
  const webFetch = createWebFetch(fetchFn);

  return Object.freeze({
    async activityEnabled(
      activityRef: string,
      signal?: AbortSignal,
    ): Promise<boolean> {
      let response: Response;
      try {
        response = await webFetch(
          `/api/v1/temporal/activities/${encodeURIComponent(activityRef)}/execution-policy`,
          signal === undefined ? undefined : { signal },
        );
      } catch (error) {
        if (error instanceof DOMException && error.name === 'AbortError') {
          throw error;
        }
        throw new TemporalSessionCapabilityRemoteError(
          'transport',
          'Session capability read could not reach DANTE.',
        );
      }

      let payload: unknown;
      try {
        payload = await response.json();
      } catch {
        throw new TemporalSessionCapabilityRemoteError(
          'protocol',
          'Session capability response is not valid JSON.',
          response.status,
        );
      }

      if (!response.ok) {
        throw new TemporalSessionCapabilityRemoteError(
          'http',
          `Session capability read failed with HTTP ${response.status}.`,
          response.status,
        );
      }

      const policy = record(payload);
      if (
        policy === null || policy.activity_ref !== activityRef ||
        !['disabled', 'record', 'live', 'record_and_live'].includes(
          String(policy.mode_code),
        )
      ) {
        throw new TemporalSessionCapabilityRemoteError(
          'protocol',
          'Session capability response has an unsupported representation.',
          response.status,
        );
      }

      return policy.mode_code === 'live' || policy.mode_code === 'record_and_live';
    },
  });
}
