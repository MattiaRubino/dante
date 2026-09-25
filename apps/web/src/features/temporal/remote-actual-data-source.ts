import { createWebFetch } from '../../platform/api/web-fetch';

const UUID_V7 =
  /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export type ActualSubjectKind = 'activity' | 'event' | 'occurrence';
export type ActualExtent = 'instant' | 'start_only' | 'interval';

export type TemporalActualTiming = Readonly<{
  extentCode: ActualExtent;
  startedAt: string;
  endedAt: string | null;
}>;

export type TemporalActualSessionBasis = Readonly<{
  sessionRef: string;
  sessionTimingMaterialStateRef: string;
}>;

export type TemporalActualView = Readonly<{
  actualRef: string;
  subjectNativeRef: string;
  materialStateRef: string;
  realizationOccurred: boolean;
  timing: TemporalActualTiming | null;
  sessionBases: readonly TemporalActualSessionBasis[];
  replayed: boolean;
}>;

export type RecordActualCommand = Readonly<{
  operationId: string;
  expectedMaterialStateRef: string | null;
  realizationOccurred: boolean;
}>;

export class TemporalActualRemoteError extends Error {
  constructor(
    readonly kind: 'transport' | 'http' | 'protocol' | 'authentication',
    message: string,
    readonly status: number | null = null,
    readonly code: string | null = null,
  ) {
    super(message);
    this.name = 'TemporalActualRemoteError';
  }
}

function record(value: unknown): Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) {
    throw new TemporalActualRemoteError('protocol', 'Invalid Actual response.');
  }
  return value as Record<string, unknown>;
}

function uuid(value: unknown, field: string): string {
  if (typeof value !== 'string' || !UUID_V7.test(value)) {
    throw new TemporalActualRemoteError('protocol', `${field} must be a UUIDv7.`);
  }
  return value.toLowerCase();
}

function timing(value: unknown): TemporalActualTiming | null {
  if (value === null) return null;
  const payload = record(value);
  const extent = payload.extent_code;
  if (
    extent !== 'instant' &&
    extent !== 'start_only' &&
    extent !== 'interval'
  ) {
    throw new TemporalActualRemoteError('protocol', 'Invalid Actual timing extent.');
  }
  if (typeof payload.started_at !== 'string') {
    throw new TemporalActualRemoteError('protocol', 'Invalid Actual timing start.');
  }
  if (payload.ended_at !== null && typeof payload.ended_at !== 'string') {
    throw new TemporalActualRemoteError('protocol', 'Invalid Actual timing end.');
  }
  return Object.freeze({
    extentCode: extent,
    startedAt: payload.started_at,
    endedAt: payload.ended_at as string | null,
  });
}

function sessionBases(value: unknown): readonly TemporalActualSessionBasis[] {
  if (!Array.isArray(value)) {
    throw new TemporalActualRemoteError('protocol', 'Invalid Actual Session bases.');
  }
  return Object.freeze(
    value.map((item) => {
      const payload = record(item);
      return Object.freeze({
        sessionRef: uuid(payload.session_ref, 'session_ref'),
        sessionTimingMaterialStateRef: uuid(
          payload.session_timing_material_state_ref,
          'session_timing_material_state_ref',
        ),
      });
    }),
  );
}

function view(value: unknown): TemporalActualView {
  const payload = record(value);
  if (
    typeof payload.realization_occurred !== 'boolean' ||
    typeof payload.replayed !== 'boolean'
  ) {
    throw new TemporalActualRemoteError('protocol', 'Invalid Actual realization state.');
  }
  return Object.freeze({
    actualRef: uuid(payload.actual_ref, 'actual_ref'),
    subjectNativeRef: uuid(payload.subject_native_ref, 'subject_native_ref'),
    materialStateRef: uuid(payload.material_state_ref, 'material_state_ref'),
    realizationOccurred: payload.realization_occurred,
    timing: timing(payload.timing),
    sessionBases: sessionBases(payload.session_bases),
    replayed: payload.replayed,
  });
}

function subjectPath(kind: ActualSubjectKind, subjectRef: string): string {
  const encoded = encodeURIComponent(subjectRef);
  if (kind === 'activity') return `/api/v1/temporal/activities/${encoded}/actual`;
  if (kind === 'event') return `/api/v1/temporal/events/${encoded}/actual`;
  return `/api/v1/temporal/occurrences/${encoded}/actual`;
}

export function createRemoteTemporalActualDataSource(
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
      throw new TemporalActualRemoteError(
        'authentication',
        'Actual commands require an authenticated browser session.',
        response.status,
      );
    }
    return payload.csrf_token;
  }

  async function problem(response: Response): Promise<TemporalActualRemoteError> {
    let payload: Record<string, unknown> = {};
    try {
      payload = record(await response.json());
    } catch {
      return new TemporalActualRemoteError(
        'http',
        'Actual command rejected.',
        response.status,
      );
    }
    return new TemporalActualRemoteError(
      'http',
      typeof payload.detail === 'string' ? payload.detail : 'Actual command rejected.',
      response.status,
      typeof payload.code === 'string' ? payload.code : null,
    );
  }

  return Object.freeze({
    async get(
      kind: ActualSubjectKind,
      subjectRef: string,
    ): Promise<TemporalActualView | null> {
      const response = await webFetch(subjectPath(kind, subjectRef));
      if (!response.ok) {
        const error = await problem(response);
        if (response.status === 404 && error.code === 'temporal.actual.not_found') {
          return null;
        }
        throw error;
      }
      return view(await response.json());
    },

    async record(
      kind: ActualSubjectKind,
      subjectRef: string,
      command: RecordActualCommand,
    ): Promise<TemporalActualView> {
      const headers = new Headers({
        'Content-Type': 'application/json',
        'X-Dante-CSRF': await csrf(),
      });
      const response = await webFetch(subjectPath(kind, subjectRef), {
        method: 'POST',
        headers,
        body: JSON.stringify({
          operation_id: command.operationId,
          expected_material_state_ref: command.expectedMaterialStateRef,
          realization_occurred: command.realizationOccurred,
          timing: null,
          session_bases: [],
        }),
      });
      if (!response.ok) throw await problem(response);
      return view(await response.json());
    },
  });
}
