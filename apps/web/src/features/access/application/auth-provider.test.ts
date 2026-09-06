import { afterEach, describe, expect, it, vi } from 'vitest';

vi.mock('../../../platform/auth/web-auth-provider', () => ({
  googleClientIdFromBuild: vi.fn(),
  redirectToAppleAuthorization: vi.fn(),
}));

import {
  WebAuthRemoteError,
  webAuthRemote,
} from '../../../platform/auth/web-auth-remote';
import {
  googleClientIdFromBuild,
  redirectToAppleAuthorization,
} from '../../../platform/auth/web-auth-provider';
import {
  beginAppleAuthentication,
  completeGoogleAuthentication,
  prepareGoogleAuthentication,
  resolveProviderContinuation,
} from './auth-provider';

const SIGNAL = new AbortController().signal;

const googleBegun = {
  external_auth_transaction_ref: '00000000-0000-4000-8000-000000000001',
  state: 'provider-state',
  nonce: 'dante-nonce',
};

const appleBegun = {
  authorization_url:
    'https://appleid.apple.com/auth/authorize?client_id=dante&state=provider-state',
};

function missingContinuation(code: string): WebAuthRemoteError {
  return new WebAuthRemoteError({
    kind: 'server_problem',
    code,
  } as never);
}

afterEach(() => {
  vi.restoreAllMocks();
  vi.clearAllMocks();
});

describe('Provider application boundary', () => {
  it('keeps Google and Apple provider evidence bound to DANTE begin state', async () => {
    vi.mocked(googleClientIdFromBuild).mockReturnValue('google-client-id');
    const beginGoogleSpy = vi
      .spyOn(webAuthRemote, 'beginGoogleAuthentication')
      .mockResolvedValue(googleBegun as never);
    const completeGoogleSpy = vi
      .spyOn(webAuthRemote, 'completeGoogleAuthentication')
      .mockResolvedValue({ outcome: 'authenticated' } as never);
    const beginAppleSpy = vi
      .spyOn(webAuthRemote, 'beginAppleAuthentication')
      .mockResolvedValue(appleBegun as never);

    const preparation = await prepareGoogleAuthentication({
      purpose: 'link',
      returnTarget: 'security',
      csrfToken: 'current-csrf-token',
      signal: SIGNAL,
    });

    expect(preparation).toEqual({
      clientId: 'google-client-id',
      begun: googleBegun,
    });
    expect(beginGoogleSpy).toHaveBeenCalledWith(
      { purpose: 'link', return_target: 'security' },
      'current-csrf-token',
      SIGNAL,
    );

    if (preparation === null) {
      throw new Error(
        'configured Google preparation unexpectedly returned null',
      );
    }
    await completeGoogleAuthentication({
      preparation,
      credential: 'google-credential',
      signal: SIGNAL,
    });

    expect(completeGoogleSpy).toHaveBeenCalledWith(
      {
        external_auth_transaction_ref:
          googleBegun.external_auth_transaction_ref,
        state: googleBegun.state,
        credential: 'google-credential',
      },
      SIGNAL,
    );

    await beginAppleAuthentication({
      purpose: 'link',
      returnTarget: 'security',
      csrfToken: 'current-csrf-token',
      signal: SIGNAL,
    });

    expect(beginAppleSpy).toHaveBeenCalledWith(
      { purpose: 'link', return_target: 'security' },
      'current-csrf-token',
      SIGNAL,
    );
    expect(redirectToAppleAuthorization).toHaveBeenCalledWith(
      appleBegun.authorization_url,
    );
  });

  it('does not create a Google transaction when the build has no Google client ID', async () => {
    vi.mocked(googleClientIdFromBuild).mockReturnValue('');
    const beginGoogleSpy = vi.spyOn(webAuthRemote, 'beginGoogleAuthentication');

    await expect(
      prepareGoogleAuthentication({
        purpose: 'sign_in',
        returnTarget: 'access',
        signal: SIGNAL,
      }),
    ).resolves.toBeNull();
    expect(beginGoogleSpy).not.toHaveBeenCalled();
  });

  it('prefers an enrollment continuation and does not probe link state when enrollment exists', async () => {
    const enrollment = {
      email_address: 'person@example.com',
      verification_expires_at: '2026-09-01T22:30:00Z',
    } as never;
    const enrollmentSpy = vi
      .spyOn(webAuthRemote, 'getProviderEnrollment')
      .mockResolvedValue(enrollment);
    const linkSpy = vi.spyOn(webAuthRemote, 'getProviderLink');

    await expect(resolveProviderContinuation(SIGNAL)).resolves.toEqual({
      kind: 'enrollment',
      enrollment,
    });
    expect(enrollmentSpy).toHaveBeenCalledWith(SIGNAL);
    expect(linkSpy).not.toHaveBeenCalled();
  });

  it('falls through only canonical missing-continuation failures and otherwise preserves remote errors', async () => {
    const link = {
      external_link_challenge_ref: '00000000-0000-4000-8000-000000000002',
      provider_code: 'google',
      expires_at: '2026-09-01T22:30:00Z',
    } as never;
    const enrollmentSpy = vi
      .spyOn(webAuthRemote, 'getProviderEnrollment')
      .mockRejectedValue(
        missingContinuation('auth.provider_enrollment_invalid_or_expired'),
      );
    const linkSpy = vi
      .spyOn(webAuthRemote, 'getProviderLink')
      .mockResolvedValueOnce(link)
      .mockRejectedValueOnce(
        missingContinuation('auth.provider_link_invalid_or_expired'),
      );

    await expect(resolveProviderContinuation(SIGNAL)).resolves.toEqual({
      kind: 'link',
      link,
    });
    expect(enrollmentSpy).toHaveBeenCalledWith(SIGNAL);
    expect(linkSpy).toHaveBeenCalledWith(SIGNAL);

    await expect(resolveProviderContinuation(SIGNAL)).resolves.toEqual({
      kind: 'none',
    });

    const unexpected = new WebAuthRemoteError({
      kind: 'server_problem',
      code: 'service.unavailable',
    } as never);
    enrollmentSpy.mockRejectedValueOnce(unexpected);

    await expect(resolveProviderContinuation(SIGNAL)).rejects.toBe(unexpected);
  });
});
