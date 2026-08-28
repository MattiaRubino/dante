import { describe, expect, it } from 'vitest';

import * as publicApi from '../src';
import { createDanteApiClient } from '../src';

const REQUEST_ID = '019d0000-0000-7000-8000-000000000001';
const ACCOUNT_REF = '00000000-0000-4000-8000-000000000001';
const AUTH_SESSION_REF = '00000000-0000-4000-8000-000000000002';

function apiResponse(
  status: number,
  body: unknown,
  contentType: string | null,
  extraHeaders: HeadersInit = {},
): Response {
  const headers = new Headers({
    'Cache-Control': 'no-store',
    'X-Request-ID': REQUEST_ID,
    ...Object.fromEntries(new Headers(extraHeaders).entries()),
  });
  if (contentType !== null) {
    headers.set('Content-Type', contentType);
  }
  return new Response(body === undefined ? null : JSON.stringify(body), {
    status,
    headers,
  });
}

function fetchReturning(response: Response): typeof globalThis.fetch {
  return async () => response.clone();
}

describe('@dante/api-client governed boundary', () => {
  it('does not expose raw generated operations from the package root', () => {
    expect('authSignIn' in publicApi).toBe(false);
    expect('authGetSession' in publicApi).toBe(false);
    expect('authLogOut' in publicApi).toBe(false);
    expect(typeof publicApi.createDanteApiClient).toBe('function');
  });

  it('validates a successful signin response before returning it', async () => {
    const client = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            authenticated: true,
            account_ref: ACCOUNT_REF,
            auth_session_ref: AUTH_SESSION_REF,
            recent_auth_at: '2026-08-28T16:00:00Z',
            expires_at: '2026-09-27T16:00:00Z',
            csrf_token: 'csrf-token',
          },
          'application/json',
        ),
      ),
    });

    const result = await client.signIn({
      email: 'person@example.com',
      password: 'correct horse battery staple',
    });

    expect(result.ok).toBe(true);
    if (result.ok) {
      expect(result.requestId).toBe(REQUEST_ID);
      expect(result.value.authenticated).toBe(true);
      expect(result.value.account_ref).toBe(ACCOUNT_REF);
    }
  });

  it('normalizes a valid RFC 9457 failure and rejects malformed session payloads', async () => {
    const problemClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          401,
          {
            type: 'urn:dante:problem:auth.invalid_credentials',
            title: 'Authentication failed',
            status: 401,
            detail: 'The supplied credentials could not be accepted.',
            code: 'auth.invalid_credentials',
            category: 'authentication',
            request_id: REQUEST_ID,
            retryable: false,
          },
          'application/problem+json',
        ),
      ),
    });

    const problem = await problemClient.signIn({
      email: 'person@example.com',
      password: 'wrong password',
    });
    expect(problem).toMatchObject({
      ok: false,
      failure: {
        kind: 'server_problem',
        status: 401,
        code: 'auth.invalid_credentials',
        requestId: REQUEST_ID,
      },
    });

    const malformedClient = createDanteApiClient({
      fetchFn: fetchReturning(apiResponse(200, {}, 'application/json')),
    });
    const malformed = await malformedClient.getSession();
    expect(malformed).toMatchObject({
      ok: false,
      failure: {
        kind: 'contract_violation',
        reason: 'invalid_payload',
        status: 200,
      },
    });
  });

  it('handles logout success and classifies transport failure separately', async () => {
    const logoutClient = createDanteApiClient({
      fetchFn: fetchReturning(apiResponse(204, undefined, null)),
    });
    const logout = await logoutClient.logOut();
    expect(logout).toMatchObject({ ok: true, status: 204, requestId: REQUEST_ID });

    const offlineFetch: typeof globalThis.fetch = async () => {
      throw new TypeError('network unavailable');
    };
    const offlineClient = createDanteApiClient({ fetchFn: offlineFetch });
    const offline = await offlineClient.getSession();
    expect(offline).toEqual({
      ok: false,
      failure: { kind: 'network_unavailable' },
    });
  });
});
