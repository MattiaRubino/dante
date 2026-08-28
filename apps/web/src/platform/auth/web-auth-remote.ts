import {
  createDanteApiClient,
  type AuthenticatedSession,
  type AuthSession,
  type RemoteFailure,
  type RemoteResult,
  type SignInRequest,
} from '@dante/api-client';

const WEB_CLIENT_HEADER_NAME = 'X-Dante-Client';
const WEB_CLIENT_HEADER_VALUE = 'web';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const ACCEPT_HEADER_VALUE = 'application/json, application/problem+json';

export class WebAuthRemoteError extends Error {
  constructor(readonly failure: RemoteFailure) {
    super(`DANTE Auth remote failure: ${failure.kind}`);
    this.name = 'WebAuthRemoteError';
  }
}

function governedHeaders(headersInit?: HeadersInit): Headers {
  const headers = new Headers(headersInit);
  headers.set('Accept', ACCEPT_HEADER_VALUE);
  headers.set(WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE);
  return headers;
}

export function createWebFetch(
  fetchFn: typeof globalThis.fetch,
): typeof globalThis.fetch {
  return (input, init) =>
    fetchFn(input, {
      ...init,
      credentials: 'same-origin',
      headers: governedHeaders(init?.headers),
    });
}

function requestOptions(
  signal?: AbortSignal,
  headers?: HeadersInit,
): RequestInit {
  const options: RequestInit = {};
  if (signal !== undefined) {
    options.signal = signal;
  }
  if (headers !== undefined) {
    options.headers = headers;
  }
  return options;
}

function unwrapRemoteResult<T>(result: RemoteResult<T>): T {
  if (result.ok) {
    return result.value;
  }
  throw new WebAuthRemoteError(result.failure);
}

export function createWebAuthRemote(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const client = createDanteApiClient({ fetchFn: createWebFetch(fetchFn) });

  return {
    async getSession(signal?: AbortSignal): Promise<AuthSession> {
      const result = await client.getSession(requestOptions(signal));
      return unwrapRemoteResult(result);
    },

    async signIn(
      request: SignInRequest,
      signal?: AbortSignal,
    ): Promise<AuthenticatedSession> {
      const result = await client.signIn(request, requestOptions(signal));
      return unwrapRemoteResult(result);
    },

    async logOut(csrfToken: string, signal?: AbortSignal): Promise<void> {
      if (!csrfToken) {
        throw new Error('Authenticated logout requires a CSRF token.');
      }

      const headers = new Headers();
      headers.set(CSRF_HEADER_NAME, csrfToken);
      const result = await client.logOut(requestOptions(signal, headers));
      return unwrapRemoteResult(result);
    },
  };
}

export const webAuthRemote = createWebAuthRemote();
