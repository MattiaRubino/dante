import { describe, expect, it } from 'vitest';

import {
  authRemoteFailureFromUnknown,
  WebAuthRemoteError,
} from './auth-ui-boundary';

describe('Access Auth UI boundary', () => {
  it('preserves remote failure identity across chunk-like error instances', () => {
    const failure = {
      kind: 'server_problem',
      status: 401,
      code: 'auth.reauthentication_required',
      category: 'authentication',
      requestId: '019d0000-0000-7000-8000-000000000001',
      retryable: false,
      fieldErrors: [],
      retryAfter: null,
      problem: {
        type: 'urn:dante:problem:auth.reauthentication_required',
        title: 'Reauthentication required',
        status: 401,
        detail: 'Fresh authentication evidence is required for this operation.',
        code: 'auth.reauthentication_required',
        category: 'authentication',
        request_id: '019d0000-0000-7000-8000-000000000001',
        retryable: false,
      },
      headers: new Headers(),
    } as const;
    const chunkLikeError = {
      name: 'WebAuthRemoteError',
      failure,
    };

    expect(authRemoteFailureFromUnknown(chunkLikeError)).toBe(failure);
    expect(chunkLikeError instanceof WebAuthRemoteError).toBe(true);
  });

  it('rejects unrelated objects instead of inventing a remote failure', () => {
    expect(authRemoteFailureFromUnknown(new Error('unrelated'))).toBeNull();
  });
});
