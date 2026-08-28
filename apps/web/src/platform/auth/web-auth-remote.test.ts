import { describe, expect, it } from 'vitest';

import { createWebAuthRemote } from './web-auth-remote';

const REQUEST_ID = '019d0000-0000-7000-8000-000000000001';
const ACCOUNT_REF = '00000000-0000-4000-8000-000000000001';
const AUTH_SESSION_REF = '00000000-0000-4000-8000-000000000002';

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

describe('Web Auth remote transport', () => {
  it('uses same-origin credentials and the governed Web headers for signin', async () => {
    let capturedInput: RequestInfo | URL | undefined;
    let capturedInit: RequestInit | undefined;
    const fetchFn: typeof globalThis.fetch = (input, init) => {
      capturedInput = input;
      capturedInit = init;
      return Promise.resolve(
        response(
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
      );
    };

    const remote = createWebAuthRemote(fetchFn);
    const session = await remote.signIn({
      email: 'person@example.com',
      password: 'correct horse battery staple',
    });

    expect(session.authenticated).toBe(true);
    expect(capturedInput).toBe('/api/v1/auth/signin');
    expect(capturedInit?.credentials).toBe('same-origin');
    expect(capturedInit?.method).toBe('POST');

    const headers = new Headers(capturedInit?.headers);
    expect(headers.get('Accept')).toBe(
      'application/json, application/problem+json',
    );
    expect(headers.get('X-Dante-Client')).toBe('web');
    expect(headers.get('Content-Type')).toBe('application/json');
    expect(headers.has('X-Dante-CSRF')).toBe(false);
  });

  it('injects the in-memory session CSRF token only for logout', async () => {
    let capturedInput: RequestInfo | URL | undefined;
    let capturedInit: RequestInit | undefined;
    const fetchFn: typeof globalThis.fetch = (input, init) => {
      capturedInput = input;
      capturedInit = init;
      return Promise.resolve(response(204, undefined, null));
    };

    const remote = createWebAuthRemote(fetchFn);
    await remote.logOut('session-csrf-token');

    expect(capturedInput).toBe('/api/v1/auth/session');
    expect(capturedInit?.credentials).toBe('same-origin');
    expect(capturedInit?.method).toBe('DELETE');

    const headers = new Headers(capturedInit?.headers);
    expect(headers.get('X-Dante-Client')).toBe('web');
    expect(headers.get('X-Dante-CSRF')).toBe('session-csrf-token');
  });
});
