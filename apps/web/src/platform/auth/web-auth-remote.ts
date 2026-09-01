import {
  createDanteApiClient,
  type AppleAuthenticationBegun,
  type AuthenticatedSession,
  type AuthenticationMethods,
  type AuthSession,
  type ExistingAccountSignup,
  type GoogleAuthenticationBegun,
  type GoogleAuthenticationCompleteRequest,
  type PasskeyAuthenticationCompleteRequest,
  type PasskeyCeremony,
  type PasskeyReauthenticationCompleteRequest,
  type PasskeyRegistrationCompleteRequest,
  type PasskeyUpdateRequest,
  type PasswordEstablishRequest,
  type PasswordRecoveryRequest,
  type PasswordRecoveryValidationRequest,
  type PasswordResetRequest,
  type ProviderAuthenticationResult,
  type ProviderBeginRequest,
  type ProviderEnrollmentEmailRequest,
  type ProviderEnrollmentRequired,
  type ProviderEnrollmentVerificationRequest,
  type ProviderEnrollmentVerificationResult,
  type ProviderLink,
  type ProviderPurpose,
  type ProviderReturnTarget,
  type ReauthenticateRequest,
  type RecoveryAccepted,
  type RecoveryValidation,
  type RemoteFailure,
  type RemoteResult,
  type SignInRequest,
  type SignupAuthenticated,
  type SignupCreated,
  type SignupRequest,
  type SignupResendRequest,
  type SignupVerificationRequest,
  type SignupVerificationResult,
} from '@dante/api-client';

const WEB_CLIENT_HEADER_NAME = 'X-Dante-Client';
const WEB_CLIENT_HEADER_VALUE = 'web';
const CSRF_HEADER_NAME = 'X-Dante-CSRF';
const ACCEPT_HEADER_VALUE = 'application/json, application/problem+json';

export type WebAuthSession = AuthSession;
export type WebAuthenticatedSession = AuthenticatedSession;
export type WebAuthSignInRequest = SignInRequest;
export type WebSignupRequest = SignupRequest;
export type WebSignupCreated = SignupCreated;
export type WebSignupVerificationRequest = SignupVerificationRequest;
export type WebSignupVerificationResult = SignupVerificationResult;
export type WebSignupAuthenticated = SignupAuthenticated;
export type WebExistingAccountSignup = ExistingAccountSignup;
export type WebSignupResendRequest = SignupResendRequest;
export type WebPasswordRecoveryRequest = PasswordRecoveryRequest;
export type WebPasswordRecoveryValidationRequest =
  PasswordRecoveryValidationRequest;
export type WebPasswordResetRequest = PasswordResetRequest;
export type WebReauthenticateRequest = ReauthenticateRequest;
export type WebRecoveryAccepted = RecoveryAccepted;
export type WebRecoveryValidation = RecoveryValidation;
export type WebAuthRemoteFailure = RemoteFailure;
export type WebAuthenticationMethods = AuthenticationMethods;
export type WebPasswordEstablishRequest = PasswordEstablishRequest;
export type WebProviderPurpose = ProviderPurpose;
export type WebProviderReturnTarget = ProviderReturnTarget;
export type WebProviderBeginRequest = ProviderBeginRequest;
export type WebGoogleAuthenticationBegun = GoogleAuthenticationBegun;
export type WebGoogleAuthenticationCompleteRequest =
  GoogleAuthenticationCompleteRequest;
export type WebAppleAuthenticationBegun = AppleAuthenticationBegun;
export type WebProviderAuthenticationResult = ProviderAuthenticationResult;
export type WebProviderEnrollmentRequired = ProviderEnrollmentRequired;
export type WebProviderEnrollmentEmailRequest = ProviderEnrollmentEmailRequest;
export type WebProviderEnrollmentVerificationRequest =
  ProviderEnrollmentVerificationRequest;
export type WebProviderEnrollmentVerificationResult =
  ProviderEnrollmentVerificationResult;
export type WebProviderLink = ProviderLink;
export type WebPasskeyCeremony = PasskeyCeremony;
export type WebPasskeyRegistrationCompleteRequest =
  PasskeyRegistrationCompleteRequest;
export type WebPasskeyAuthenticationCompleteRequest =
  PasskeyAuthenticationCompleteRequest;
export type WebPasskeyReauthenticationCompleteRequest =
  PasskeyReauthenticationCompleteRequest;
export type WebPasskeyUpdateRequest = PasskeyUpdateRequest;

export class WebAuthRemoteError extends Error {
  constructor(readonly failure: WebAuthRemoteFailure) {
    super(`DANTE Auth remote failure: ${failure.kind}`);
    this.name = 'WebAuthRemoteError';
  }
}

function governedHeaders(headersInit?: HeadersInit): Headers {
  const headers = new Headers(headersInit);
  headers.set('Accept', ACCEPT_HEADER_VALUE);
  headers.set(WEB_CLIENT_HEADER_NAME, WEB_CLIENT_HEADER_VALUE);
  return headers;
}

export function createWebFetch(
  fetchFn: typeof globalThis.fetch,
): typeof globalThis.fetch {
  return (input, init) =>
    fetchFn(input, {
      ...init,
      credentials: 'same-origin',
      headers: governedHeaders(init?.headers),
    });
}

function requestOptions(
  signal?: AbortSignal,
  headers?: HeadersInit,
): RequestInit {
  const options: RequestInit = {};
  if (signal !== undefined) {
    options.signal = signal;
  }
  if (headers !== undefined) {
    options.headers = headers;
  }
  return options;
}

function csrfRequestOptions(
  csrfToken: string,
  signal?: AbortSignal,
): RequestInit {
  if (!csrfToken) {
    throw new Error('Authenticated Auth mutation requires a CSRF token.');
  }
  const headers = new Headers();
  headers.set(CSRF_HEADER_NAME, csrfToken);
  return requestOptions(signal, headers);
}

function providerBeginRequestOptions(
  purpose: WebProviderPurpose,
  csrfToken: string | undefined,
  signal?: AbortSignal,
): RequestInit {
  if (purpose === 'sign_in') {
    return requestOptions(signal);
  }
  if (csrfToken === undefined) {
    throw new Error(
      'Authenticated provider begin requires the current session CSRF token.',
    );
  }
  return csrfRequestOptions(csrfToken, signal);
}

function unwrapRemoteResult<T>(result: RemoteResult<T>): T {
  if (result.ok) {
    return result.value;
  }
  throw new WebAuthRemoteError(result.failure);
}

export function createWebAuthRemote(
  fetchFn: typeof globalThis.fetch = globalThis.fetch,
) {
  const client = createDanteApiClient({ fetchFn: createWebFetch(fetchFn) });

  return {
    async getSession(signal?: AbortSignal): Promise<WebAuthSession> {
      return unwrapRemoteResult(
        await client.getSession(requestOptions(signal)),
      );
    },

    async signIn(
      request: WebAuthSignInRequest,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.signIn(request, requestOptions(signal)),
      );
    },

    async getAuthenticationMethods(
      signal?: AbortSignal,
    ): Promise<WebAuthenticationMethods> {
      return unwrapRemoteResult(
        await client.getAuthenticationMethods(requestOptions(signal)),
      );
    },

    async establishPassword(
      request: WebPasswordEstablishRequest,
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.establishPassword(
          request,
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async removePassword(
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.removePassword(csrfRequestOptions(csrfToken, signal)),
      );
    },

    async logOut(csrfToken: string, signal?: AbortSignal): Promise<void> {
      return unwrapRemoteResult(
        await client.logOut(csrfRequestOptions(csrfToken, signal)),
      );
    },

    async beginSignup(
      request: WebSignupRequest,
      signal?: AbortSignal,
    ): Promise<WebSignupCreated> {
      return unwrapRemoteResult(
        await client.beginSignup(request, requestOptions(signal)),
      );
    },

    async verifySignup(
      request: WebSignupVerificationRequest,
      signal?: AbortSignal,
    ): Promise<WebSignupVerificationResult> {
      return unwrapRemoteResult(
        await client.verifySignup(request, requestOptions(signal)),
      );
    },

    async resendSignupVerification(
      request: WebSignupResendRequest,
      signal?: AbortSignal,
    ): Promise<WebSignupCreated> {
      return unwrapRemoteResult(
        await client.resendSignupVerification(request, requestOptions(signal)),
      );
    },

    async requestPasswordRecovery(
      request: WebPasswordRecoveryRequest,
      signal?: AbortSignal,
    ): Promise<WebRecoveryAccepted> {
      return unwrapRemoteResult(
        await client.requestPasswordRecovery(request, requestOptions(signal)),
      );
    },

    async validatePasswordRecovery(
      request: WebPasswordRecoveryValidationRequest,
      signal?: AbortSignal,
    ): Promise<WebRecoveryValidation> {
      return unwrapRemoteResult(
        await client.validatePasswordRecovery(request, requestOptions(signal)),
      );
    },

    async resetPassword(
      request: WebPasswordResetRequest,
      signal?: AbortSignal,
    ): Promise<void> {
      return unwrapRemoteResult(
        await client.resetPassword(request, requestOptions(signal)),
      );
    },

    async reauthenticate(
      request: WebReauthenticateRequest,
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.reauthenticate(
          request,
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async beginGoogleAuthentication(
      request: WebProviderBeginRequest,
      csrfToken?: string,
      signal?: AbortSignal,
    ): Promise<WebGoogleAuthenticationBegun> {
      return unwrapRemoteResult(
        await client.beginGoogleAuthentication(
          request,
          providerBeginRequestOptions(request.purpose, csrfToken, signal),
        ),
      );
    },

    async completeGoogleAuthentication(
      request: WebGoogleAuthenticationCompleteRequest,
      signal?: AbortSignal,
    ): Promise<WebProviderAuthenticationResult> {
      return unwrapRemoteResult(
        await client.completeGoogleAuthentication(request, requestOptions(signal)),
      );
    },

    async beginAppleAuthentication(
      request: WebProviderBeginRequest,
      csrfToken?: string,
      signal?: AbortSignal,
    ): Promise<WebAppleAuthenticationBegun> {
      return unwrapRemoteResult(
        await client.beginAppleAuthentication(
          request,
          providerBeginRequestOptions(request.purpose, csrfToken, signal),
        ),
      );
    },

    async getProviderEnrollment(
      signal?: AbortSignal,
    ): Promise<WebProviderEnrollmentRequired> {
      return unwrapRemoteResult(
        await client.getProviderEnrollment(requestOptions(signal)),
      );
    },

    async setProviderEnrollmentEmail(
      request: WebProviderEnrollmentEmailRequest,
      signal?: AbortSignal,
    ): Promise<WebProviderEnrollmentRequired> {
      return unwrapRemoteResult(
        await client.setProviderEnrollmentEmail(request, requestOptions(signal)),
      );
    },

    async resendProviderEnrollmentVerification(
      signal?: AbortSignal,
    ): Promise<WebProviderEnrollmentRequired> {
      return unwrapRemoteResult(
        await client.resendProviderEnrollmentVerification(requestOptions(signal)),
      );
    },

    async verifyProviderEnrollment(
      request: WebProviderEnrollmentVerificationRequest,
      signal?: AbortSignal,
    ): Promise<WebProviderEnrollmentVerificationResult> {
      return unwrapRemoteResult(
        await client.verifyProviderEnrollment(request, requestOptions(signal)),
      );
    },

    async getProviderLink(signal?: AbortSignal): Promise<WebProviderLink> {
      return unwrapRemoteResult(
        await client.getProviderLink(requestOptions(signal)),
      );
    },

    async confirmProviderLink(
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      const result = unwrapRemoteResult(
        await client.confirmProviderLink(csrfRequestOptions(csrfToken, signal)),
      );
      return result;
    },

    async unlinkProvider(
      externalIdentityRef: string,
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.unlinkProvider(
          externalIdentityRef,
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async beginPasskeyRegistration(
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebPasskeyCeremony> {
      return unwrapRemoteResult(
        await client.beginPasskeyRegistration(
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async completePasskeyRegistration(
      request: WebPasskeyRegistrationCompleteRequest,
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.completePasskeyRegistration(
          request,
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async beginPasskeyAuthentication(
      signal?: AbortSignal,
    ): Promise<WebPasskeyCeremony> {
      return unwrapRemoteResult(
        await client.beginPasskeyAuthentication(requestOptions(signal)),
      );
    },

    async completePasskeyAuthentication(
      request: WebPasskeyAuthenticationCompleteRequest,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.completePasskeyAuthentication(request, requestOptions(signal)),
      );
    },

    async beginPasskeyReauthentication(
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebPasskeyCeremony> {
      return unwrapRemoteResult(
        await client.beginPasskeyReauthentication(
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async completePasskeyReauthentication(
      request: WebPasskeyReauthenticationCompleteRequest,
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.completePasskeyReauthentication(
          request,
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async updatePasskey(
      passkeyCredentialRef: string,
      request: WebPasskeyUpdateRequest,
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<void> {
      return unwrapRemoteResult(
        await client.updatePasskey(
          passkeyCredentialRef,
          request,
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },

    async removePasskey(
      passkeyCredentialRef: string,
      csrfToken: string,
      signal?: AbortSignal,
    ): Promise<WebAuthenticatedSession> {
      return unwrapRemoteResult(
        await client.removePasskey(
          passkeyCredentialRef,
          csrfRequestOptions(csrfToken, signal),
        ),
      );
    },
  };
}

export const webAuthRemote = createWebAuthRemote();
