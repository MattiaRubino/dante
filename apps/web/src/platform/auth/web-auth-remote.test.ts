import { describe, expect, it } from 'vitest';

import { createWebAuthRemote } from './web-auth-remote';

const REQUEST_ID = '019d0000-0000-7000-8000-000000000001';
const ACCOUNT_REF = '00000000-0000-4000-8000-000000000001';
const AUTH_SESSION_REF = '00000000-0000-4000-8000-000000000002';
const SIGNUP_REF = '00000000-0000-4000-8000-000000000003';

function response(
  status: number,
  body: unknown,
  contentType: string | null,
): Response {
  const headers = new Headers({
    'Cache-Control': 'no-store',
    'X-Request-ID': REQUEST_ID,
  });
  if (contentType !== null) {
    headers.set('Content-Type', contentType);
  }
  return new Response(body === undefined ? null : JSON.stringify(body), {
    status,
    headers,
  });
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

describe('Web Auth remote transport', () => {
  it('uses same-origin credentials and governed Web headers for public auth mutations', async () => {
    const captures: Array<{ input: RequestInfo | URL; init?: RequestInit }> = [];
    const responses = [
      response(200, authenticatedSession(), 'application/json'),
      response(
        200,
        {
          signup_ref: SIGNUP_REF,
          signup_expires_at: '2026-08-29T20:00:00Z',
          verification_expires_at: '2026-08-29T19:15:00Z',
          verification_required: true,
        },
        'application/json',
      ),
      response(202, { accepted: true }, 'application/json'),
    ];
    const fetchFn: typeof globalThis.fetch = (input, init) => {
      captures.push({ input, init });
      const next = responses.shift();
      if (!next) {
        throw new Error('Unexpected test request.');
      }
      return Promise.resolve(next);
    };

    const remote = createWebAuthRemote(fetchFn);
    await remote.signIn({
      email: 'person@example.com',
      password: 'correct horse battery staple',
    });
    await remote.beginSignup({
      email: 'person@example.com',
      password: 'correct horse battery staple',
    });
    await remote.requestPasswordRecovery({ email: 'person@example.com' });

    expect(captures.map(({ input }) => input)).toEqual([
      '/api/v1/auth/signin',
      '/api/v1/auth/signup',
      '/api/v1/auth/recovery',
    ]);
    for (const { init } of captures) {
      expect(init?.credentials).toBe('same-origin');
      expect(init?.method).toBe('POST');
      const headers = new Headers(init?.headers);
      expect(headers.get('Accept')).toBe(
        'application/json, application/problem+json',
      );
      expect(headers.get('X-Dante-Client')).toBe('web');
      expect(headers.get('Content-Type')).toBe('application/json');
      expect(headers.has('X-Dante-CSRF')).toBe(false);
    }
  });

  it('injects the in-memory session CSRF token only for authenticated mutations', async () => {
    const captures: Array<{ input: RequestInfo | URL; init?: RequestInit }> = [];
    const responses = [
      response(204, undefined, null),
      response(200, authenticatedSession(), 'application/json'),
    ];
    const fetchFn: typeof globalThis.fetch = (input, init) => {
      captures.push({ input, init });
      const next = responses.shift();
      if (!next) {
        throw new Error('Unexpected test request.');
      }
      return Promise.resolve(next);
    };

    const remote = createWebAuthRemote(fetchFn);
    await remote.logOut('logout-csrf-token');
    await remote.reauthenticate(
      { password: 'correct horse battery staple' },
      'reauth-csrf-token',
    );

    expect(captures[0]?.input).toBe('/api/v1/auth/session');
    expect(captures[0]?.init?.method).toBe('DELETE');
    expect(new Headers(captures[0]?.init?.headers).get('X-Dante-CSRF')).toBe(
      'logout-csrf-token',
    );

    expect(captures[1]?.input).toBe('/api/v1/auth/reauthenticate');
    expect(captures[1]?.init?.method).toBe('POST');
    expect(new Headers(captures[1]?.init?.headers).get('X-Dante-CSRF')).toBe(
      'reauth-csrf-token',
    );
  });

  it('rejects authenticated mutations without a CSRF token before transport', async () => {
    let called = false;
    const fetchFn: typeof globalThis.fetch = () => {
      called = true;
      return Promise.resolve(response(204, undefined, null));
    };
    const remote = createWebAuthRemote(fetchFn);

    await expect(remote.logOut('')).rejects.toThrow('requires a CSRF token');
    await expect(
      remote.reauthenticate({ password: 'password' }, ''),
    ).rejects.toThrow('requires a CSRF token');
    expect(called).toBe(false);
  });
});
