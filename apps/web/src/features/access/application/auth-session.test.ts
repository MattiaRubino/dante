import { describe, expect, it } from 'vitest';

import type { RemoteFailure } from '@dante/api-client';
import { WebAuthRemoteError } from '../../../platform/auth/web-auth-remote';
import { accessEventForAuthError } from './auth-session';

function serverProblem(
  code: string,
  category: string,
  status: number,
  retryAfter: string | null = null,
): RemoteFailure {
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
          serverProblem('rate_limit.exceeded', 'rate_limit', 429, '17'),
        ),
      ),
    ).toEqual({ type: 'SERVER_RATE_LIMITED', retryAfterSeconds: 17 });
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
