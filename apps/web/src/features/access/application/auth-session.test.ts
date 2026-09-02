import { QueryClient } from '@tanstack/react-query';
import { describe, expect, it, vi } from 'vitest';

import {
  WebAuthRemoteError,
  type WebAuthRemoteFailure,
} from '../../../platform/auth/web-auth-remote';
import {
  accessEventForAuthError,
  authSessionQueryKey,
  commitAuthoritativeAuthSession,
} from './auth-session';

function serverProblem(
  code: string,
  category: string,
  status: number,
  retryAfter: string | null = null,
): WebAuthRemoteFailure {
  return {
    kind: 'server_problem',
    status,
    code,
    category,
    requestId: '019d0000-0000-7000-8000-000000000001',
    retryable: status === 429 || status >= 500,
    fieldErrors: [],
    retryAfter,
    problem: {
      type: `urn:dante:problem:${code}`,
      title: 'Synthetic problem',
      status,
      detail: 'Synthetic problem for application mapping.',
      code,
      category,
      request_id: '019d0000-0000-7000-8000-000000000001',
      retryable: status === 429 || status >= 500,
    },
    headers: new Headers(),
  };
}

describe('Access Auth application error mapping', () => {
  it('maps exact server codes before fallbacks', () => {
    expect(
      accessEventForAuthError(
        new WebAuthRemoteError(
          serverProblem('auth.invalid_credentials', 'authentication', 401),
        ),
      ),
    ).toEqual({ type: 'SERVER_INVALID_CREDENTIALS' });

    expect(
      accessEventForAuthError(
        new WebAuthRemoteError(
          serverProblem('auth.signup_resend_cooldown', 'rate_limit', 429, '17'),
        ),
      ),
    ).toEqual({ type: 'SERVER_RATE_LIMITED', retryAfterSeconds: 17 });

    expect(
      accessEventForAuthError(
        new WebAuthRemoteError(
          serverProblem(
            'auth.verification_invalid_or_expired',
            'authentication',
            400,
          ),
        ),
      ),
    ).toEqual({ type: 'SERVER_VERIFICATION_INVALID_OR_EXPIRED' });

    expect(
      accessEventForAuthError(
        new WebAuthRemoteError(
          serverProblem(
            'auth.recovery_invalid_or_expired',
            'authentication',
            400,
          ),
        ),
      ),
    ).toEqual({ type: 'SERVER_RECOVERY_INVALID_OR_EXPIRED' });

    expect(
      accessEventForAuthError(
        new WebAuthRemoteError(
          serverProblem(
            'auth.reauthentication_required',
            'authentication',
            401,
          ),
        ),
      ),
    ).toEqual({ type: 'SERVER_REAUTH_REQUIRED' });
  });

  it('uses category and status fallbacks without inventing server codes', () => {
    expect(
      accessEventForAuthError(
        new WebAuthRemoteError(
          serverProblem('future.validation_code', 'validation', 422),
        ),
      ),
    ).toEqual({ type: 'SERVER_REQUEST_INVALID' });

    expect(
      accessEventForAuthError(
        new WebAuthRemoteError(
          serverProblem('future.failure', 'future_category', 503),
        ),
      ),
    ).toEqual({ type: 'SERVER_UNAVAILABLE' });
  });

  it('keeps client-local transport and contract failures separate', () => {
    expect(
      accessEventForAuthError(
        new WebAuthRemoteError({ kind: 'network_unavailable' }),
        false,
      ),
    ).toEqual({ type: 'NETWORK_OFFLINE' });

    expect(
      accessEventForAuthError(
        new WebAuthRemoteError({
          kind: 'contract_violation',
          reason: 'invalid_payload',
          status: 200,
          headers: new Headers(),
        }),
      ),
    ).toEqual({ type: 'SERVER_UNEXPECTED' });

    expect(
      accessEventForAuthError(new WebAuthRemoteError({ kind: 'aborted' })),
    ).toBeNull();
  });
});

describe('Access Auth authoritative session cache', () => {
  it('cancels stale session reads before committing a rotated bearer result', async () => {
    const queryClient = new QueryClient();
    const cancelSpy = vi
      .spyOn(queryClient, 'cancelQueries')
      .mockResolvedValue(undefined);
    const setSpy = vi.spyOn(queryClient, 'setQueryData');
    const session = {
      authenticated: true as const,
      account_ref: '00000000-0000-4000-8000-000000000001',
      auth_session_ref: '00000000-0000-4000-8000-000000000002',
      csrf_token: 'rotated-csrf',
      recent_auth_at: '2026-09-02T12:40:00Z',
      expires_at: '2026-10-02T12:40:00Z',
    };

    await commitAuthoritativeAuthSession(queryClient, session);

    expect(cancelSpy).toHaveBeenCalledWith({
      queryKey: authSessionQueryKey,
      exact: true,
    });
    expect(setSpy).toHaveBeenCalledWith(authSessionQueryKey, session);
  });
});
