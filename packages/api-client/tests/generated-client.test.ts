import { describe, expect, it } from 'vitest';

import * as publicApi from '../src';
import { createDanteApiClient } from '../src';

const REQUEST_ID = '019d0000-0000-7000-8000-000000000001';
const OTHER_REQUEST_ID = '019d0000-0000-7000-8000-000000000002';
const ACCOUNT_REF = '00000000-0000-4000-8000-000000000001';
const AUTH_SESSION_REF = '00000000-0000-4000-8000-000000000002';
const SIGNUP_REF = '00000000-0000-4000-8000-000000000003';
const RECOVERY_REF = '00000000-0000-4000-8000-000000000004';

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
  return () => Promise.resolve(response.clone());
}

function authenticatedSession() {
  return {
    authenticated: true as const,
    account_ref: ACCOUNT_REF,
    auth_session_ref: AUTH_SESSION_REF,
    recent_auth_at: '2026-08-28T16:00:00Z',
    expires_at: '2026-09-27T16:00:00Z',
    csrf_token: 'csrf-token',
  };
}

function problem(status = 401, requestId = REQUEST_ID) {
  return {
    type: 'urn:dante:problem:auth.invalid_credentials',
    title: 'Authentication failed',
    status,
    detail: 'The supplied credentials could not be accepted.',
    code: 'auth.invalid_credentials',
    category: 'authentication',
    request_id: requestId,
    retryable: false,
  };
}

describe('@dante/api-client governed boundary', () => {
  it('does not expose raw generated operations from the package root', () => {
    for (const operation of [
      'authSignIn',
      'authGetSession',
      'authLogOut',
      'authBeginSignup',
      'authVerifySignup',
      'authResendSignupVerification',
      'authRequestPasswordRecovery',
      'authValidatePasswordRecovery',
      'authResetPassword',
      'authReauthenticate',
    ]) {
      expect(operation in publicApi).toBe(false);
    }
    expect(typeof publicApi.createDanteApiClient).toBe('function');
  });

  it('validates successful signin and session responses before returning them', async () => {
    const client = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, authenticatedSession(), 'application/json'),
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

  it('validates each M4 success contract and signup outcome discriminator', async () => {
    const signupClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            signup_ref: SIGNUP_REF,
            signup_expires_at: '2026-08-29T20:00:00Z',
            verification_expires_at: '2026-08-29T19:15:00Z',
            verification_required: true,
          },
          'application/json',
        ),
      ),
    });
    const signup = await signupClient.beginSignup({
      email: 'person@example.com',
      password: 'correct horse battery staple',
    });
    expect(signup).toMatchObject({
      ok: true,
      status: 200,
      value: { signup_ref: SIGNUP_REF, verification_required: true },
    });

    const authenticatedClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          { ...authenticatedSession(), outcome: 'authenticated' },
          'application/json',
        ),
      ),
    });
    const authenticated = await authenticatedClient.verifySignup({
      signup_ref: SIGNUP_REF,
      code: '123456',
    });
    expect(authenticated).toMatchObject({
      ok: true,
      value: { outcome: 'authenticated', account_ref: ACCOUNT_REF },
    });

    const existingClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, { outcome: 'existing_account' }, 'application/json'),
      ),
    });
    const existing = await existingClient.verifySignup({
      signup_ref: SIGNUP_REF,
      code: '123456',
    });
    expect(existing).toMatchObject({
      ok: true,
      value: { outcome: 'existing_account' },
    });

    const recoveryClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(202, { accepted: true }, 'application/json'),
      ),
    });
    expect(
      await recoveryClient.requestPasswordRecovery({
        email: 'person@example.com',
      }),
    ).toMatchObject({ ok: true, status: 202, value: { accepted: true } });

    const validationClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, { valid: true }, 'application/json'),
      ),
    });
    expect(
      await validationClient.validatePasswordRecovery({
        password_recovery_ref: RECOVERY_REF,
        secret: 'recovery-secret',
      }),
    ).toMatchObject({ ok: true, value: { valid: true } });

    const resetClient = createDanteApiClient({
      fetchFn: fetchReturning(apiResponse(204, undefined, null)),
    });
    expect(
      await resetClient.resetPassword({
        password_recovery_ref: RECOVERY_REF,
        secret: 'recovery-secret',
        new_password: 'correct horse battery staple replacement',
      }),
    ).toMatchObject({ ok: true, status: 204 });

    const reauthClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, authenticatedSession(), 'application/json'),
      ),
    });
    expect(
      await reauthClient.reauthenticate({ password: 'correct horse battery staple' }),
    ).toMatchObject({
      ok: true,
      value: { authenticated: true, auth_session_ref: AUTH_SESSION_REF },
    });
  });

  it('rejects unknown success payload keys instead of silently widening contracts', async () => {
    const client = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            signup_ref: SIGNUP_REF,
            signup_expires_at: '2026-08-29T20:00:00Z',
            verification_expires_at: '2026-08-29T19:15:00Z',
            verification_required: true,
            secret: 'must-never-be-public',
          },
          'application/json',
        ),
      ),
    });

    expect(
      await client.beginSignup({
        email: 'person@example.com',
        password: 'correct horse battery staple',
      }),
    ).toMatchObject({
      ok: false,
      failure: { kind: 'contract_violation', reason: 'invalid_payload' },
    });
  });

  it('normalizes RFC 9457 failures and distinguishes status from request-id mismatch', async () => {
    const problemClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(401, problem(), 'application/problem+json'),
      ),
    });
    expect(
      await problemClient.signIn({
        email: 'person@example.com',
        password: 'wrong password',
      }),
    ).toMatchObject({
      ok: false,
      failure: {
        kind: 'server_problem',
        status: 401,
        code: 'auth.invalid_credentials',
        requestId: REQUEST_ID,
      },
    });

    const statusMismatchClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(401, problem(403), 'application/problem+json'),
      ),
    });
    expect(
      await statusMismatchClient.signIn({
        email: 'person@example.com',
        password: 'wrong password',
      }),
    ).toMatchObject({
      ok: false,
      failure: { kind: 'contract_violation', reason: 'status_mismatch' },
    });

    const requestIdMismatchClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(401, problem(401, OTHER_REQUEST_ID), 'application/problem+json'),
      ),
    });
    expect(
      await requestIdMismatchClient.signIn({
        email: 'person@example.com',
        password: 'wrong password',
      }),
    ).toMatchObject({
      ok: false,
      failure: { kind: 'contract_violation', reason: 'request_id_mismatch' },
    });
  });

  it('rejects malformed session payloads', async () => {
    const malformedClient = createDanteApiClient({
      fetchFn: fetchReturning(apiResponse(200, {}, 'application/json')),
    });
    expect(await malformedClient.getSession()).toMatchObject({
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
    expect(await logoutClient.logOut()).toMatchObject({
      ok: true,
      status: 204,
      requestId: REQUEST_ID,
    });

    const offlineFetch: typeof globalThis.fetch = () =>
      Promise.reject(new TypeError('network unavailable'));
    const offlineClient = createDanteApiClient({ fetchFn: offlineFetch });
    expect(await offlineClient.getSession()).toEqual({
      ok: false,
      failure: { kind: 'network_unavailable' },
    });
  });
});
