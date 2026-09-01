import { describe, expect, it } from 'vitest';

import * as publicApi from '../src';
import { createDanteApiClient } from '../src';

const REQUEST_ID = '019d0000-0000-7000-8000-000000000001';
const OTHER_REQUEST_ID = '019d0000-0000-7000-8000-000000000002';
const ACCOUNT_REF = '00000000-0000-4000-8000-000000000001';
const AUTH_SESSION_REF = '00000000-0000-4000-8000-000000000002';
const SIGNUP_REF = '00000000-0000-4000-8000-000000000003';
const RECOVERY_REF = '00000000-0000-4000-8000-000000000004';
const EXTERNAL_IDENTITY_REF = '00000000-0000-4000-8000-000000000005';
const PASSKEY_REF = '00000000-0000-4000-8000-000000000006';
const TRANSACTION_REF = '00000000-0000-4000-8000-000000000007';
const LINK_REF = '00000000-0000-4000-8000-000000000008';
const WEBAUTHN_CHALLENGE_REF = '00000000-0000-4000-8000-000000000009';

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

function providerAuthenticated() {
  return { ...authenticatedSession(), outcome: 'authenticated' as const };
}

function authenticationProviderMethod() {
  return {
    external_identity_ref: EXTERNAL_IDENTITY_REF,
    provider_code: 'google',
    provider_email_address: 'person@example.com',
    provider_email_private: false,
  };
}

function passkeyMethod() {
  return {
    backup_eligible: true,
    backup_state: false,
    created_at: '2026-08-30T10:00:00Z',
    label: 'Laptop',
    last_used_at: null,
    passkey_credential_ref: PASSKEY_REF,
    transports: ['internal'],
  };
}

function authenticationMethods() {
  return {
    active_passkey_count: 1,
    passkeys: [passkeyMethod()],
    password_established: true,
    providers: [authenticationProviderMethod()],
    recovery_eligible_email_count: 1,
  };
}

function providerEnrollmentRequired() {
  return {
    outcome: 'enrollment_required' as const,
    external_signup_ref: SIGNUP_REF,
    expires_at: '2026-09-01T18:00:00Z',
    email_address: 'person@example.com',
    verification_expires_at: '2026-09-01T17:15:00Z',
  };
}

function providerLinkRequired() {
  return {
    outcome: 'link_required' as const,
    external_link_challenge_ref: LINK_REF,
    expires_at: '2026-09-01T18:00:00Z',
  };
}

function passkeyCeremony() {
  return {
    webauthn_challenge_ref: WEBAUTHN_CHALLENGE_REF,
    expires_at: '2026-09-01T18:00:00Z',
    options: {
      challenge: 'YQ',
      rpId: 'dante.test',
      allowCredentials: [],
    },
  };
}

function assertionRequest() {
  return {
    webauthn_challenge_ref: WEBAUTHN_CHALLENGE_REF,
    response: {
      id: 'YQ',
      rawId: 'YQ',
      type: 'public-key' as const,
      clientExtensionResults: {},
      response: {
        authenticatorData: 'YQ',
        clientDataJSON: 'YQ',
        signature: 'YQ',
        userHandle: null,
      },
    },
  };
}

function registrationRequest() {
  return {
    label: 'Laptop',
    transports: ['internal'],
    webauthn_challenge_ref: WEBAUTHN_CHALLENGE_REF,
    response: {
      id: 'YQ',
      rawId: 'YQ',
      type: 'public-key' as const,
      clientExtensionResults: {},
      response: {
        attestationObject: 'YQ',
        clientDataJSON: 'YQ',
      },
    },
  };
}

function problem(
  status = 401,
  requestId = REQUEST_ID,
  code = 'auth.invalid_credentials',
  category = 'authentication',
) {
  return {
    type: `urn:dante:problem:${code}`,
    title: 'Authentication failed',
    status,
    detail: 'The supplied request could not be accepted.',
    code,
    category,
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
      'authGetAuthenticationMethods',
      'authEstablishPassword',
      'authRemovePassword',
      'authBeginGoogleAuthentication',
      'authCompleteGoogleAuthentication',
      'authBeginAppleAuthentication',
      'authHandleAppleCallback',
      'authProcessAppleNotification',
      'authGetProviderEnrollment',
      'authSetProviderEnrollmentEmail',
      'authResendProviderEnrollmentVerification',
      'authVerifyProviderEnrollment',
      'authGetProviderLink',
      'authConfirmProviderLink',
      'authUnlinkProvider',
      'authBeginPasskeyRegistration',
      'authCompletePasskeyRegistration',
      'authBeginPasskeyAuthentication',
      'authCompletePasskeyAuthentication',
      'authBeginPasskeyReauthentication',
      'authCompletePasskeyReauthentication',
      'authUpdatePasskey',
      'authRemovePasskey',
    ]) {
      expect(operation in publicApi).toBe(false);
    }
    expect(typeof publicApi.createDanteApiClient).toBe('function');
  });

  it('validates successful signin and the M4 lifecycle contracts', async () => {
    const signInClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, authenticatedSession(), 'application/json'),
      ),
    });
    expect(
      await signInClient.signIn({
        email: 'person@example.com',
        password: 'correct horse battery staple',
      }),
    ).toMatchObject({
      ok: true,
      value: { authenticated: true, account_ref: ACCOUNT_REF },
    });

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
    expect(
      await signupClient.beginSignup({
        email: 'person@example.com',
        password: 'correct horse battery staple',
      }),
    ).toMatchObject({
      ok: true,
      status: 200,
      value: { signup_ref: SIGNUP_REF, verification_required: true },
    });

    const verifyClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          { ...authenticatedSession(), outcome: 'authenticated' },
          'application/json',
        ),
      ),
    });
    expect(
      await verifyClient.verifySignup({
        signup_ref: SIGNUP_REF,
        code: '123456',
      }),
    ).toMatchObject({
      ok: true,
      value: { outcome: 'authenticated', account_ref: ACCOUNT_REF },
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
  });

  it('validates M5 methods including safe passkey projection and password lifecycle', async () => {
    const methodsClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, authenticationMethods(), 'application/json'),
      ),
    });
    expect(await methodsClient.getAuthenticationMethods()).toMatchObject({
      ok: true,
      value: {
        password_established: true,
        active_passkey_count: 1,
        passkeys: [
          {
            passkey_credential_ref: PASSKEY_REF,
            label: 'Laptop',
            transports: ['internal'],
          },
        ],
        providers: [
          {
            external_identity_ref: EXTERNAL_IDENTITY_REF,
            provider_code: 'google',
          },
        ],
      },
    });

    const sessionClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, authenticatedSession(), 'application/json'),
      ),
    });
    expect(
      await sessionClient.establishPassword({
        new_password: 'correct horse battery staple',
      }),
    ).toMatchObject({
      ok: true,
      value: { auth_session_ref: AUTH_SESSION_REF },
    });
    expect(await sessionClient.removePassword()).toMatchObject({
      ok: true,
      value: { auth_session_ref: AUTH_SESSION_REF },
    });
  });

  it('rejects unknown provider and passkey inventory metadata instead of silently widening', async () => {
    const providerClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            ...authenticationMethods(),
            providers: [
              {
                ...authenticationProviderMethod(),
                provider_subject: 'must-never-be-public',
              },
            ],
          },
          'application/json',
        ),
      ),
    });
    expect(await providerClient.getAuthenticationMethods()).toMatchObject({
      ok: false,
      failure: { kind: 'contract_violation', reason: 'invalid_payload' },
    });

    const passkeyClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            ...authenticationMethods(),
            passkeys: [
              {
                ...passkeyMethod(),
                credential_id: 'must-never-be-public',
              },
            ],
          },
          'application/json',
        ),
      ),
    });
    expect(await passkeyClient.getAuthenticationMethods()).toMatchObject({
      ok: false,
      failure: { kind: 'contract_violation', reason: 'invalid_payload' },
    });
  });

  it('governs Google and Apple begin plus provider authentication outcome unions', async () => {
    const googleBeginClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            external_auth_transaction_ref: TRANSACTION_REF,
            state: 'opaque-state',
            nonce: 'opaque-nonce',
            expires_at: '2026-09-01T18:00:00Z',
          },
          'application/json',
        ),
      ),
    });
    expect(
      await googleBeginClient.beginGoogleAuthentication({
        purpose: 'sign_in',
        return_target: 'access',
      }),
    ).toMatchObject({
      ok: true,
      value: { external_auth_transaction_ref: TRANSACTION_REF },
    });

    const appleBeginClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            authorization_url:
              'https://appleid.apple.com/auth/authorize?state=opaque',
            expires_at: '2026-09-01T18:00:00Z',
          },
          'application/json',
        ),
      ),
    });
    expect(
      await appleBeginClient.beginAppleAuthentication({
        purpose: 'sign_in',
        return_target: 'access',
      }),
    ).toMatchObject({
      ok: true,
      value: { authorization_url: expect.any(String) },
    });

    for (const outcome of [
      providerAuthenticated(),
      providerLinkRequired(),
      providerEnrollmentRequired(),
    ]) {
      const client = createDanteApiClient({
        fetchFn: fetchReturning(apiResponse(200, outcome, 'application/json')),
      });
      const result = await client.completeGoogleAuthentication({
        external_auth_transaction_ref: TRANSACTION_REF,
        state: 'opaque-state',
        credential: 'provider-credential',
      });
      expect(result).toMatchObject({
        ok: true,
        value: { outcome: outcome.outcome },
      });
    }
  });

  it('rejects widened provider outcome payloads', async () => {
    const client = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            ...providerLinkRequired(),
            continuation_secret: 'must-never-be-public',
          },
          'application/json',
        ),
      ),
    });
    expect(
      await client.completeGoogleAuthentication({
        external_auth_transaction_ref: TRANSACTION_REF,
        state: 'opaque-state',
        credential: 'provider-credential',
      }),
    ).toMatchObject({
      ok: false,
      failure: { kind: 'contract_violation', reason: 'invalid_payload' },
    });
  });

  it('governs provider enrollment, link confirmation and unlink lifecycle', async () => {
    const enrollmentClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, providerEnrollmentRequired(), 'application/json'),
      ),
    });
    expect(await enrollmentClient.getProviderEnrollment()).toMatchObject({
      ok: true,
      value: {
        outcome: 'enrollment_required',
        external_signup_ref: SIGNUP_REF,
      },
    });
    expect(
      await enrollmentClient.setProviderEnrollmentEmail({
        email: 'person@example.com',
      }),
    ).toMatchObject({ ok: true, value: { outcome: 'enrollment_required' } });
    expect(
      await enrollmentClient.resendProviderEnrollmentVerification(),
    ).toMatchObject({ ok: true, value: { outcome: 'enrollment_required' } });

    const verifyClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, providerLinkRequired(), 'application/json'),
      ),
    });
    expect(
      await verifyClient.verifyProviderEnrollment({ code: '123456' }),
    ).toMatchObject({ ok: true, value: { outcome: 'link_required' } });

    const linkClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          {
            external_link_challenge_ref: LINK_REF,
            provider_code: 'google',
            expires_at: '2026-09-01T18:00:00Z',
          },
          'application/json',
        ),
      ),
    });
    expect(await linkClient.getProviderLink()).toMatchObject({
      ok: true,
      value: { external_link_challenge_ref: LINK_REF, provider_code: 'google' },
    });

    const authenticatedClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, providerAuthenticated(), 'application/json'),
      ),
    });
    expect(await authenticatedClient.confirmProviderLink()).toMatchObject({
      ok: true,
      value: { outcome: 'authenticated', account_ref: ACCOUNT_REF },
    });
    expect(
      await authenticatedClient.unlinkProvider(EXTERNAL_IDENTITY_REF),
    ).toMatchObject({
      ok: true,
      value: { outcome: 'authenticated', account_ref: ACCOUNT_REF },
    });
  });

  it('governs passkey begin/complete/update/remove without exposing raw WebAuthn operations', async () => {
    const ceremonyClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, passkeyCeremony(), 'application/json'),
      ),
    });
    expect(await ceremonyClient.beginPasskeyRegistration()).toMatchObject({
      ok: true,
      value: { webauthn_challenge_ref: WEBAUTHN_CHALLENGE_REF },
    });
    expect(await ceremonyClient.beginPasskeyAuthentication()).toMatchObject({
      ok: true,
      value: { webauthn_challenge_ref: WEBAUTHN_CHALLENGE_REF },
    });
    expect(await ceremonyClient.beginPasskeyReauthentication()).toMatchObject({
      ok: true,
      value: { webauthn_challenge_ref: WEBAUTHN_CHALLENGE_REF },
    });

    const completionClient = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(200, authenticatedSession(), 'application/json'),
      ),
    });
    expect(
      await completionClient.completePasskeyRegistration(registrationRequest()),
    ).toMatchObject({
      ok: true,
      value: { auth_session_ref: AUTH_SESSION_REF },
    });
    expect(
      await completionClient.completePasskeyAuthentication(assertionRequest()),
    ).toMatchObject({
      ok: true,
      value: { auth_session_ref: AUTH_SESSION_REF },
    });
    expect(
      await completionClient.completePasskeyReauthentication(
        assertionRequest(),
      ),
    ).toMatchObject({
      ok: true,
      value: { auth_session_ref: AUTH_SESSION_REF },
    });
    expect(await completionClient.removePasskey(PASSKEY_REF)).toMatchObject({
      ok: true,
      value: { auth_session_ref: AUTH_SESSION_REF },
    });

    const updateClient = createDanteApiClient({
      fetchFn: fetchReturning(apiResponse(204, undefined, null)),
    });
    expect(
      await updateClient.updatePasskey(PASSKEY_REF, { label: 'Travel key' }),
    ).toMatchObject({
      ok: true,
      status: 204,
    });
  });

  it('rejects unexpected top-level passkey ceremony metadata', async () => {
    const client = createDanteApiClient({
      fetchFn: fetchReturning(
        apiResponse(
          200,
          { ...passkeyCeremony(), credential_id: 'must-never-be-public' },
          'application/json',
        ),
      ),
    });
    expect(await client.beginPasskeyAuthentication()).toMatchObject({
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
        apiResponse(
          401,
          problem(401, OTHER_REQUEST_ID),
          'application/problem+json',
        ),
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

  it('handles no-content success and classifies transport failure separately', async () => {
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
