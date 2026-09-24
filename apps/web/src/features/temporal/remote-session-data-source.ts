import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type SessionSubjectKind = 'activity' | 'occurrence';

export type TemporalSessionView = Readonly<{
  sessionRef: string;
  subjectNativeRef: string;
  timingMaterialStateRef: string;
  startedAt: string;
  endedAt: string | null;
  open: boolean;
  replayed: boolean;
  paused: boolean;
}>;

export class TemporalSessionRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalSessionRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalSessionRemoteError('protocol', 'Invalid Session response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalSessionRemoteError('protocol', `${field} must be a UUIDv7.`);
  }
  return value.toLowerCase();
}

function view(value: unknown): TemporalSessionView {
  const payload = record(value);
  const ended = payload.ended_at;
  if (
    typeof payload.open !== 'boolean' ||
    typeof payload.replayed !== 'boolean' ||
    typeof payload.paused !== 'boolean'
  ) {
    throw new TemporalSessionRemoteError('protocol', 'Invalid Session state.');
  }
  if (ended !== null && typeof ended !== 'string') {
    throw new TemporalSessionRemoteError('protocol', 'Invalid Session end.');
  }
  if (typeof payload.started_at !== 'string') {
    throw new TemporalSessionRemoteError('protocol', 'Invalid Session start.');
  }
  return Object.freeze({
    sessionRef: uuid(payload.session_ref, 'session_ref'),
    subjectNativeRef: uuid(payload.subject_native_ref, 'subject_native_ref'),
    timingMaterialStateRef: uuid(
      payload.timing_material_state_ref,
      'timing_material_state_ref',
    ),
    startedAt: payload.started_at,
    endedAt: ended,
    open: payload.open,
    replayed: payload.replayed,
    paused: payload.paused,
  });
}

export function createRemoteTemporalSessionDataSource(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const webFetch = createWebFetch(fetchFn);

  async function csrf(): Promise<string> {
    const response = await webFetch('/api/v1/auth/session');
    const payload = record(await response.json());
    if (
      !response.ok ||
      payload.authenticated !== true ||
      typeof payload.csrf_token !== 'string' ||
      !payload.csrf_token
    ) {
      throw new TemporalSessionRemoteError(
        'authentication',
        'Session commands require an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function send(
    path: string,
    method: 'GET' | 'POST',
    body?: unknown,
  ): Promise<unknown> {
    const headers = new Headers();
    if (method === 'POST') {
      headers.set('Content-Type', 'application/json');
      headers.set('X-Dante-CSRF', await csrf());
    }
    const response = await webFetch(path, {
      method,
      headers,
      ...(body === undefined ? {} : { body: JSON.stringify(body) }),
    });
    const value: unknown = await response.json();
    if (!response.ok) {
      const problem = record(value);
      throw new TemporalSessionRemoteError(
        'http',
        typeof problem.detail === 'string' ? problem.detail : 'Session command rejected.',
        response.status,
        typeof problem.code === 'string' ? problem.code : null,
      );
    }
    return value;
  }

  return Object.freeze({
    async list(kind: SessionSubjectKind, subjectRef: string): Promise<TemporalSessionView[]> {
      const path =
        kind === 'activity'
          ? `/api/v1/temporal/activities/${encodeURIComponent(subjectRef)}/sessions`
          : `/api/v1/temporal/occurrences/${encodeURIComponent(subjectRef)}/sessions`;
      const value = await send(path, 'GET');
      if (!Array.isArray(value)) {
        throw new TemporalSessionRemoteError('protocol', 'Session list must be an array.');
      }
      return value.map(view);
    },
    async start(
      kind: SessionSubjectKind,
      subjectRef: string,
      operationId: string,
    ): Promise<TemporalSessionView> {
      const path =
        kind === 'activity'
          ? `/api/v1/temporal/activities/${encodeURIComponent(subjectRef)}/sessions`
          : `/api/v1/temporal/occurrences/${encodeURIComponent(subjectRef)}/sessions`;
      return view(await send(path, 'POST', { operation_id: operationId }));
    },
    async end(
      sessionRef: string,
      expectedMaterialStateRef: string,
      operationId: string,
    ): Promise<TemporalSessionView> {
      return view(
        await send(`/api/v1/temporal/sessions/${encodeURIComponent(sessionRef)}/end`, 'POST', {
          operation_id: operationId,
          expected_material_state_ref: expectedMaterialStateRef,
        }),
      );
    },
    async pause(
      sessionRef: string,
      expectedMaterialStateRef: string,
      operationId: string,
    ): Promise<TemporalSessionView> {
      return view(
        await send('/api/v1/temporal/sessions/' + encodeURIComponent(sessionRef) + '/pause', 'POST', {
          operation_id: operationId,
          expected_material_state_ref: expectedMaterialStateRef,
        }),
      );
    },
    async resume(
      sessionRef: string,
      expectedMaterialStateRef: string,
      operationId: string,
    ): Promise<TemporalSessionView> {
      return view(
        await send('/api/v1/temporal/sessions/' + encodeURIComponent(sessionRef) + '/resume', 'POST', {
          operation_id: operationId,
          expected_material_state_ref: expectedMaterialStateRef,
        }),
      );
    },
  });
}
