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

function exposesSessionRuntime(value: unknown): boolean {
  const constraint = record(value);
  if (
    constraint === null ||
    constraint.subject_kind !== 'activity' ||
    constraint.status !== 'active'
  ) {
    return false;
  }

  const rule = record(constraint.current_rule);
  return (
    rule !== null &&
    rule.family === 'duration' &&
    rule.constrained_facet === 'session.active_duration'
  );
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
          `/api/v1/temporal/constraints?subject_ref=${encodeURIComponent(activityRef)}`,
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

      const envelope = record(payload);
      if (envelope === null || !Array.isArray(envelope.items)) {
        throw new TemporalSessionCapabilityRemoteError(
          'protocol',
          'Session capability response has an unsupported representation.',
          response.status,
        );
      }

      return envelope.items.some(exposesSessionRuntime);
    },
  });
}
