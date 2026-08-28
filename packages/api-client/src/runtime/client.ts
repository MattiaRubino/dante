import {
  authGetSession as generatedAuthGetSession,
  authLogOut as generatedAuthLogOut,
  authSignIn as generatedAuthSignIn,
} from '../generated/dante';
import {
  AuthenticatedSessionResponse,
  ProblemDetails,
  UnauthenticatedSessionResponse,
  type AuthenticatedSessionResponseOutput,
  type ProblemDetailsOutput,
  type ProblemFieldErrorOutput,
  type SignInRequest,
  type UnauthenticatedSessionResponseOutput,
} from '../generated/model';

const JSON_MEDIA_TYPE = 'application/json';
const PROBLEM_MEDIA_TYPE = 'application/problem+json';
const AUTHENTICATED_SESSION_KEYS = new Set([
  'account_ref',
  'auth_session_ref',
  'authenticated',
  'csrf_token',
  'expires_at',
  'recent_auth_at',
]);
const UNAUTHENTICATED_SESSION_KEYS = new Set(['authenticated']);
const PROBLEM_KEYS = new Set([
  'category',
  'code',
  'detail',
  'errors',
  'request_id',
  'retryable',
  'status',
  'title',
  'type',
]);
const FIELD_ERROR_KEYS = new Set(['code', 'detail', 'parameters', 'pointer']);

export type AuthenticatedSession = AuthenticatedSessionResponseOutput;
export type UnauthenticatedSession = UnauthenticatedSessionResponseOutput;
export type AuthSession = AuthenticatedSession | UnauthenticatedSession;

export type ContractViolationReason =
  | 'cache_policy_mismatch'
  | 'content_type_mismatch'
  | 'invalid_payload'
  | 'request_id_mismatch'
  | 'unexpected_status'
  | 'unexpected_wire_exception';

export type ServerProblemFailure = {
  kind: 'server_problem';
  status: number;
  code: string;
  category: string;
  requestId: string;
  retryable: boolean;
  fieldErrors: readonly ProblemFieldErrorOutput[];
  retryAfter: string | null;
  problem: ProblemDetailsOutput;
  headers: Headers;
};

export type NetworkUnavailableFailure = {
  kind: 'network_unavailable';
};

export type AbortedFailure = {
  kind: 'aborted';
};

export type ContractViolationFailure = {
  kind: 'contract_violation';
  reason: ContractViolationReason;
  status: number | null;
  headers: Headers | null;
};

export type RemoteFailure =
  | ServerProblemFailure
  | NetworkUnavailableFailure
  | AbortedFailure
  | ContractViolationFailure;

export type RemoteSuccess<T> = {
  ok: true;
  value: T;
  status: number;
  requestId: string;
  headers: Headers;
};

export type RemoteResult<T> =
  RemoteSuccess<T> | { ok: false; failure: RemoteFailure };

type WireResponse = {
  data: unknown;
  status: number;
  headers: Headers;
};

type TransportFailureKind =
  NetworkUnavailableFailure['kind'] | AbortedFailure['kind'];

class TransportFailure extends Error {
  constructor(readonly kind: TransportFailureKind) {
    super(kind);
  }
}

function mediaType(headers: Headers): string | null {
  const contentType = headers.get('content-type');
  if (contentType === null) {
    return null;
  }
  return contentType.split(';', 1)[0]?.trim().toLowerCase() ?? null;
}

function hasNoStore(headers: Headers): boolean {
  return (headers.get('cache-control') ?? '')
    .split(',')
    .map((value) => value.trim().toLowerCase())
    .includes('no-store');
}

function requestId(headers: Headers): string | null {
  const value = headers.get('x-request-id')?.trim();
  return value ? value : null;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function hasOnlyKeys(
  value: unknown,
  allowed: ReadonlySet<string>,
): value is Record<string, unknown> {
  return isRecord(value) && Object.keys(value).every((key) => allowed.has(key));
}

function hasStrictProblemShape(value: unknown): boolean {
  if (!hasOnlyKeys(value, PROBLEM_KEYS)) {
    return false;
  }
  const errors = value.errors;
  if (errors === undefined || errors === null) {
    return true;
  }
  return (
    Array.isArray(errors) &&
    errors.every((fieldError) => hasOnlyKeys(fieldError, FIELD_ERROR_KEYS))
  );
}

function contractViolation(
  reason: ContractViolationReason,
  wire: WireResponse | null = null,
): RemoteResult<never> {
  return {
    ok: false,
    failure: {
      kind: 'contract_violation',
      reason,
      status: wire?.status ?? null,
      headers: wire?.headers ?? null,
    },
  };
}

function trackedFetch(
  fetchFn: typeof globalThis.fetch,
): typeof globalThis.fetch {
  return async (input, init) => {
    try {
      return await fetchFn(input, init);
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        throw new TransportFailure('aborted');
      }
      throw new TransportFailure('network_unavailable');
    }
  };
}

function fromThrown(error: unknown): RemoteResult<never> {
  if (error instanceof TransportFailure) {
    return { ok: false, failure: { kind: error.kind } };
  }
  return contractViolation('unexpected_wire_exception');
}

function responseRequestId(wire: WireResponse): RemoteResult<string> {
  if (!hasNoStore(wire.headers)) {
    return contractViolation('cache_policy_mismatch', wire);
  }
  const id = requestId(wire.headers);
  if (id === null) {
    return contractViolation('request_id_mismatch', wire);
  }
  return {
    ok: true,
    value: id,
    status: wire.status,
    requestId: id,
    headers: wire.headers,
  };
}

function success<T>(wire: WireResponse, value: T): RemoteResult<T> {
  const metadata = responseRequestId(wire);
  if (!metadata.ok) {
    return metadata;
  }
  return {
    ok: true,
    value,
    status: wire.status,
    requestId: metadata.value,
    headers: wire.headers,
  };
}

function serverProblem(wire: WireResponse): RemoteResult<never> {
  if (mediaType(wire.headers) !== PROBLEM_MEDIA_TYPE) {
    return contractViolation('content_type_mismatch', wire);
  }
  const metadata = responseRequestId(wire);
  if (!metadata.ok) {
    return metadata;
  }
  if (!hasStrictProblemShape(wire.data)) {
    return contractViolation('invalid_payload', wire);
  }
  const parsed = ProblemDetails.safeParse(wire.data);
  if (!parsed.success) {
    return contractViolation('invalid_payload', wire);
  }
  if (
    parsed.data.status !== wire.status ||
    parsed.data.request_id !== metadata.value
  ) {
    return contractViolation('request_id_mismatch', wire);
  }
  return {
    ok: false,
    failure: {
      kind: 'server_problem',
      status: wire.status,
      code: parsed.data.code,
      category: parsed.data.category,
      requestId: parsed.data.request_id,
      retryable: parsed.data.retryable,
      fieldErrors: parsed.data.errors ?? [],
      retryAfter: wire.headers.get('retry-after'),
      problem: parsed.data,
      headers: wire.headers,
    },
  };
}

function parseAuthenticatedSession(
  wire: WireResponse,
): RemoteResult<AuthenticatedSession> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE) {
    return contractViolation('content_type_mismatch', wire);
  }
  if (!hasOnlyKeys(wire.data, AUTHENTICATED_SESSION_KEYS)) {
    return contractViolation('invalid_payload', wire);
  }
  const parsed = AuthenticatedSessionResponse.safeParse(wire.data);
  if (!parsed.success) {
    return contractViolation('invalid_payload', wire);
  }
  return success(wire, parsed.data);
}

function parseSession(wire: WireResponse): RemoteResult<AuthSession> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE) {
    return contractViolation('content_type_mismatch', wire);
  }
  if (!isRecord(wire.data)) {
    return contractViolation('invalid_payload', wire);
  }
  if (wire.data.authenticated === true) {
    if (!hasOnlyKeys(wire.data, AUTHENTICATED_SESSION_KEYS)) {
      return contractViolation('invalid_payload', wire);
    }
    const parsed = AuthenticatedSessionResponse.safeParse(wire.data);
    return parsed.success
      ? success(wire, parsed.data)
      : contractViolation('invalid_payload', wire);
  }
  if (wire.data.authenticated === false) {
    if (!hasOnlyKeys(wire.data, UNAUTHENTICATED_SESSION_KEYS)) {
      return contractViolation('invalid_payload', wire);
    }
    const parsed = UnauthenticatedSessionResponse.safeParse(wire.data);
    return parsed.success
      ? success(wire, parsed.data)
      : contractViolation('invalid_payload', wire);
  }
  return contractViolation('invalid_payload', wire);
}

export type DanteApiClient = {
  signIn(
    request: SignInRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
  getSession(options?: RequestInit): Promise<RemoteResult<AuthSession>>;
  logOut(options?: RequestInit): Promise<RemoteResult<void>>;
};

export function createDanteApiClient(
  options: {
    fetchFn?: typeof globalThis.fetch;
  } = {},
): DanteApiClient {
  const fetchFn = trackedFetch(options.fetchFn ?? globalThis.fetch);

  return {
    async signIn(request, requestOptions) {
      let wire: WireResponse;
      try {
        wire = await generatedAuthSignIn(request, requestOptions, fetchFn);
      } catch (error) {
        return fromThrown(error);
      }
      if (wire.status === 200) {
        return parseAuthenticatedSession(wire);
      }
      if (wire.status >= 400) {
        return serverProblem(wire);
      }
      return contractViolation('unexpected_status', wire);
    },

    async getSession(requestOptions) {
      let wire: WireResponse;
      try {
        wire = await generatedAuthGetSession(requestOptions, fetchFn);
      } catch (error) {
        return fromThrown(error);
      }
      if (wire.status === 200) {
        return parseSession(wire);
      }
      if (wire.status >= 400) {
        return serverProblem(wire);
      }
      return contractViolation('unexpected_status', wire);
    },

    async logOut(requestOptions) {
      let wire: WireResponse;
      try {
        wire = await generatedAuthLogOut(requestOptions, fetchFn);
      } catch (error) {
        return fromThrown(error);
      }
      if (wire.status === 204) {
        return success(wire, undefined);
      }
      if (wire.status >= 400) {
        return serverProblem(wire);
      }
      return contractViolation('unexpected_status', wire);
    },
  };
}
