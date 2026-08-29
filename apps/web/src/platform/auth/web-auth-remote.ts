import {
  createDanteApiClient,
  type AuthenticatedSession,
  type AuthSession,
  type ExistingAccountSignup,
  type PasswordRecoveryRequest,
  type PasswordRecoveryValidationRequest,
  type PasswordResetRequest,
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

function csrfRequestOptions(csrfToken: string, signal?: AbortSignal): RequestInit {
  if (!csrfToken) {
    throw new Error('Authenticated Auth mutation requires a CSRF token.');
  }
  const headers = new Headers();
  headers.set(CSRF_HEADER_NAME, csrfToken);
  return requestOptions(signal, headers);
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
  };
}

export const webAuthRemote = createWebAuthRemote();
