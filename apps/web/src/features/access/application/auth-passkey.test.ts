import { afterEach, describe, expect, it, vi } from 'vitest';

vi.mock('../../../platform/auth/web-auth-webauthn', () => ({
  createPasskeyAuthenticationEvidence: vi.fn(),
  createPasskeyReauthenticationEvidence: vi.fn(),
  createPasskeyRegistrationEvidence: vi.fn(),
}));

import { webAuthRemote } from '../../../platform/auth/web-auth-remote';
import {
  createPasskeyAuthenticationEvidence,
  createPasskeyReauthenticationEvidence,
  createPasskeyRegistrationEvidence,
} from '../../../platform/auth/web-auth-webauthn';
import {
  reauthenticateWithPasskey,
  registerPasskey,
  signInWithPasskey,
} from './auth-passkey';

const ACCOUNT_REF = '00000000-0000-4000-8000-000000000001';
const AUTH_SESSION_REF = '00000000-0000-4000-8000-000000000002';

const ceremony = {
  webauthn_challenge_ref: '00000000-0000-4000-8000-000000000003',
  options: {},
} as never;

const authenticationEvidence = {
  webauthn_challenge_ref: '00000000-0000-4000-8000-000000000003',
  response: {},
} as never;

const registrationEvidence = {
  webauthn_challenge_ref: '00000000-0000-4000-8000-000000000003',
  label: 'Laptop',
  transports: [],
  response: {},
} as never;

const authenticatedSession = {
  authenticated: true as const,
  account_ref: ACCOUNT_REF,
  auth_session_ref: AUTH_SESSION_REF,
  recent_auth_at: '2026-09-01T18:00:00Z',
  expires_at: '2026-10-01T18:00:00Z',
  csrf_token: 'rotated-csrf-token',
};

afterEach(() => {
  vi.restoreAllMocks();
  vi.clearAllMocks();
});

describe('Passkey application ceremonies', () => {
  it('keeps passkey sign-in as begin, browser evidence, then backend completion', async () => {
    const signal = new AbortController().signal;
    const beginAuthentication = vi
      .spyOn(webAuthRemote, 'beginPasskeyAuthentication')
      .mockResolvedValue(ceremony);
    vi.mocked(createPasskeyAuthenticationEvidence).mockResolvedValue(
      authenticationEvidence,
    );
    const completeAuthentication = vi
      .spyOn(webAuthRemote, 'completePasskeyAuthentication')
      .mockResolvedValue(authenticatedSession);

    await expect(signInWithPasskey(signal)).resolves.toEqual(
      authenticatedSession,
    );

    expect(beginAuthentication).toHaveBeenCalledWith(signal);
    expect(createPasskeyAuthenticationEvidence).toHaveBeenCalledWith({
      ceremony,
      signal,
    });
    expect(completeAuthentication).toHaveBeenCalledWith(
      authenticationEvidence,
      signal,
    );
  });

  it('binds registration evidence to the requested label and current CSRF token', async () => {
    const signal = new AbortController().signal;
    const beginRegistration = vi
      .spyOn(webAuthRemote, 'beginPasskeyRegistration')
      .mockResolvedValue(ceremony);
    vi.mocked(createPasskeyRegistrationEvidence).mockResolvedValue(
      registrationEvidence,
    );
    const completeRegistration = vi
      .spyOn(webAuthRemote, 'completePasskeyRegistration')
      .mockResolvedValue(authenticatedSession);

    await expect(
      registerPasskey({
        label: 'Laptop',
        csrfToken: 'current-csrf-token',
        signal,
      }),
    ).resolves.toEqual(authenticatedSession);

    expect(beginRegistration).toHaveBeenCalledWith(
      'current-csrf-token',
      signal,
    );
    expect(createPasskeyRegistrationEvidence).toHaveBeenCalledWith({
      ceremony,
      label: 'Laptop',
      signal,
    });
    expect(completeRegistration).toHaveBeenCalledWith(
      registrationEvidence,
      'current-csrf-token',
      signal,
    );
  });

  it('keeps reauthentication separate from ordinary passkey sign-in', async () => {
    const signal = new AbortController().signal;
    const beginReauthentication = vi
      .spyOn(webAuthRemote, 'beginPasskeyReauthentication')
      .mockResolvedValue(ceremony);
    vi.mocked(createPasskeyReauthenticationEvidence).mockResolvedValue(
      authenticationEvidence,
    );
    const completeReauthentication = vi
      .spyOn(webAuthRemote, 'completePasskeyReauthentication')
      .mockResolvedValue(authenticatedSession);

    await expect(
      reauthenticateWithPasskey({
        csrfToken: 'reauth-csrf-token',
        signal,
      }),
    ).resolves.toEqual(authenticatedSession);

    expect(beginReauthentication).toHaveBeenCalledWith(
      'reauth-csrf-token',
      signal,
    );
    expect(createPasskeyReauthenticationEvidence).toHaveBeenCalledWith({
      ceremony,
      signal,
    });
    expect(completeReauthentication).toHaveBeenCalledWith(
      authenticationEvidence,
      'reauth-csrf-token',
      signal,
    );
  });
});
