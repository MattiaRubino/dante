import { describe, expect, it } from 'vitest';

import { authenticatedSessionFromSignup } from './auth-lifecycle';

const ACCOUNT_REF = '00000000-0000-4000-8000-000000000001';
const AUTH_SESSION_REF = '00000000-0000-4000-8000-000000000002';

describe('Access Auth lifecycle application boundary', () => {
  it('projects only authenticated signup outcomes into session state', () => {
    expect(authenticatedSessionFromSignup({ outcome: 'existing_account' })).toBeNull();

    expect(
      authenticatedSessionFromSignup({
        outcome: 'authenticated',
        authenticated: true,
        account_ref: ACCOUNT_REF,
        auth_session_ref: AUTH_SESSION_REF,
        csrf_token: 'csrf-token',
        recent_auth_at: '2026-08-29T16:00:00Z',
        expires_at: '2026-09-28T16:00:00Z',
      }),
    ).toEqual({
      authenticated: true,
      account_ref: ACCOUNT_REF,
      auth_session_ref: AUTH_SESSION_REF,
      csrf_token: 'csrf-token',
      recent_auth_at: '2026-08-29T16:00:00Z',
      expires_at: '2026-09-28T16:00:00Z',
    });
  });
});
