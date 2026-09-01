import {
  authBeginAppleAuthentication as generatedAuthBeginAppleAuthentication,
  authBeginGoogleAuthentication as generatedAuthBeginGoogleAuthentication,
  authBeginPasskeyAuthentication as generatedAuthBeginPasskeyAuthentication,
  authBeginPasskeyReauthentication as generatedAuthBeginPasskeyReauthentication,
  authBeginPasskeyRegistration as generatedAuthBeginPasskeyRegistration,
  authBeginSignup as generatedAuthBeginSignup,
  authCompleteGoogleAuthentication as generatedAuthCompleteGoogleAuthentication,
  authCompletePasskeyAuthentication as generatedAuthCompletePasskeyAuthentication,
  authCompletePasskeyReauthentication as generatedAuthCompletePasskeyReauthentication,
  authCompletePasskeyRegistration as generatedAuthCompletePasskeyRegistration,
  authConfirmProviderLink as generatedAuthConfirmProviderLink,
  authEstablishPassword as generatedAuthEstablishPassword,
  authGetAuthenticationMethods as generatedAuthGetAuthenticationMethods,
  authGetProviderEnrollment as generatedAuthGetProviderEnrollment,
  authGetProviderLink as generatedAuthGetProviderLink,
  authGetSession as generatedAuthGetSession,
  authLogOut as generatedAuthLogOut,
  authReauthenticate as generatedAuthReauthenticate,
  authRemovePasskey as generatedAuthRemovePasskey,
  authRemovePassword as generatedAuthRemovePassword,
  authRequestPasswordRecovery as generatedAuthRequestPasswordRecovery,
  authResendProviderEnrollmentVerification as generatedAuthResendProviderEnrollmentVerification,
  authResendSignupVerification as generatedAuthResendSignupVerification,
  authResetPassword as generatedAuthResetPassword,
  authSetProviderEnrollmentEmail as generatedAuthSetProviderEnrollmentEmail,
  authSignIn as generatedAuthSignIn,
  authUnlinkProvider as generatedAuthUnlinkProvider,
  authUpdatePasskey as generatedAuthUpdatePasskey,
  authValidatePasswordRecovery as generatedAuthValidatePasswordRecovery,
  authVerifyProviderEnrollment as generatedAuthVerifyProviderEnrollment,
  authVerifySignup as generatedAuthVerifySignup,
} from '../generated/dante';
import {
  AppleAuthenticationBegunResponse,
  AuthenticatedSessionResponse,
  AuthenticationMethodsResponse,
  ExistingAccountSignupResponse,
  GoogleAuthenticationBegunResponse,
  PasskeyCeremonyResponse,
  ProblemDetails,
  ProviderAuthenticatedResponse,
  ProviderEnrollmentRequiredResponse,
  ProviderLinkRequiredResponse,
  ProviderLinkResponse,
  RecoveryAcceptedResponse,
  RecoveryValidationResponse,
  SignupAuthenticatedResponse,
  SignupCreatedResponse,
  UnauthenticatedSessionResponse,
  type AppleAuthenticationBegunResponseOutput,
  type AuthenticatedSessionResponseOutput,
  type AuthenticationMethodsResponseOutput,
  type ExistingAccountSignupResponseOutput,
  type GoogleAuthenticationBegunResponseOutput,
  type GoogleAuthenticationCompleteRequest,
  type PasskeyAuthenticationCompleteRequest,
  type PasskeyCeremonyResponseOutput,
  type PasskeyReauthenticationCompleteRequest,
  type PasskeyRegistrationCompleteRequest,
  type PasskeyUpdateRequest,
  type PasswordEstablishRequest,
  type PasswordRecoveryRequest,
  type PasswordRecoveryValidationRequest,
  type PasswordResetRequest,
  type ProblemDetailsOutput,
  type ProblemFieldErrorOutput,
  type ProviderAuthenticatedResponseOutput,
  type ProviderBeginRequest,
  type ProviderEnrollmentEmailRequest,
  type ProviderEnrollmentRequiredResponseOutput,
  type ProviderEnrollmentVerificationRequest,
  type ProviderLinkRequiredResponseOutput,
  type ProviderLinkResponseOutput,
  type ReauthenticateRequest,
  type RecoveryAcceptedResponseOutput,
  type RecoveryValidationResponseOutput,
  type SignInRequest,
  type SignupAuthenticatedResponseOutput,
  type SignupCreatedResponseOutput,
  type SignupRequest,
  type SignupResendRequest,
  type SignupVerificationRequest,
  type UnauthenticatedSessionResponseOutput,
} from '../generated/model';

const JSON_MEDIA_TYPE = 'application/json';
const PROBLEM_MEDIA_TYPE = 'application/problem+json';
const AUTHENTICATED_SESSION_KEYS = new Set([
  'account_ref',
  'auth_session_ref',
  'authenticated',
  'csrf_token',
  'expires_at',
  'recent_auth_at',
]);
const SIGNUP_AUTHENTICATED_KEYS = new Set([
  ...AUTHENTICATED_SESSION_KEYS,
  'outcome',
]);
const UNAUTHENTICATED_SESSION_KEYS = new Set(['authenticated']);
const SIGNUP_CREATED_KEYS = new Set([
  'signup_expires_at',
  'signup_ref',
  'verification_expires_at',
  'verification_required',
]);
const EXISTING_ACCOUNT_SIGNUP_KEYS = new Set(['outcome']);
const RECOVERY_ACCEPTED_KEYS = new Set(['accepted']);
const RECOVERY_VALIDATION_KEYS = new Set(['valid']);
const AUTHENTICATION_METHODS_KEYS = new Set([
  'active_passkey_count',
  'passkeys',
  'password_established',
  'providers',
  'recovery_eligible_email_count',
]);
const AUTHENTICATION_PROVIDER_METHOD_KEYS = new Set([
  'external_identity_ref',
  'provider_code',
  'provider_email_address',
  'provider_email_private',
]);
const PASSKEY_METHOD_KEYS = new Set([
  'backup_eligible',
  'backup_state',
  'created_at',
  'label',
  'last_used_at',
  'passkey_credential_ref',
  'transports',
]);
const GOOGLE_AUTHENTICATION_BEGUN_KEYS = new Set([
  'expires_at',
  'external_auth_transaction_ref',
  'nonce',
  'state',
]);
const APPLE_AUTHENTICATION_BEGUN_KEYS = new Set([
  'authorization_url',
  'expires_at',
]);
const PROVIDER_AUTHENTICATED_KEYS = new Set([
  ...AUTHENTICATED_SESSION_KEYS,
  'outcome',
]);
const PROVIDER_LINK_REQUIRED_KEYS = new Set([
  'expires_at',
  'external_link_challenge_ref',
  'outcome',
]);
const PROVIDER_ENROLLMENT_REQUIRED_KEYS = new Set([
  'email_address',
  'expires_at',
  'external_signup_ref',
  'outcome',
  'verification_expires_at',
]);
const PROVIDER_LINK_KEYS = new Set([
  'expires_at',
  'external_link_challenge_ref',
  'provider_code',
]);
const PASSKEY_CEREMONY_KEYS = new Set([
  'expires_at',
  'options',
  'webauthn_challenge_ref',
]);
const PROBLEM_KEYS = new Set([
  'category',
  'code',
  'detail',
  'errors',
  'request_id',
  'retryable',
  'status',
  'title',
  'type',
]);
const FIELD_ERROR_KEYS = new Set(['code', 'detail', 'parameters', 'pointer']);

export type AuthenticatedSession = AuthenticatedSessionResponseOutput;
export type UnauthenticatedSession = UnauthenticatedSessionResponseOutput;
export type AuthSession = AuthenticatedSession | UnauthenticatedSession;
export type SignupCreated = SignupCreatedResponseOutput;
export type SignupAuthenticated = SignupAuthenticatedResponseOutput;
export type ExistingAccountSignup = ExistingAccountSignupResponseOutput;
export type SignupVerificationResult = SignupAuthenticated | ExistingAccountSignup;
export type RecoveryAccepted = RecoveryAcceptedResponseOutput;
export type RecoveryValidation = RecoveryValidationResponseOutput;
export type AuthenticationMethods = AuthenticationMethodsResponseOutput;
export type GoogleAuthenticationBegun = GoogleAuthenticationBegunResponseOutput;
export type AppleAuthenticationBegun = AppleAuthenticationBegunResponseOutput;
export type ProviderAuthenticated = ProviderAuthenticatedResponseOutput;
export type ProviderLinkRequired = ProviderLinkRequiredResponseOutput;
export type ProviderEnrollmentRequired = ProviderEnrollmentRequiredResponseOutput;
export type ProviderAuthenticationResult =
  | ProviderAuthenticated
  | ProviderLinkRequired
  | ProviderEnrollmentRequired;
export type ProviderEnrollmentVerificationResult =
  | ProviderAuthenticated
  | ProviderLinkRequired;
export type ProviderLink = ProviderLinkResponseOutput;
export type PasskeyCeremony = PasskeyCeremonyResponseOutput;

export type ContractViolationReason =
  | 'cache_policy_mismatch'
  | 'content_type_mismatch'
  | 'invalid_payload'
  | 'request_id_mismatch'
  | 'status_mismatch'
  | 'unexpected_status'
  | 'unexpected_wire_exception';

export type ServerProblemFailure = {
  kind: 'server_problem';
  status: number;
  code: string;
  category: string;
  requestId: string;
  retryable: boolean;
  fieldErrors: readonly ProblemFieldErrorOutput[];
  retryAfter: string | null;
  problem: ProblemDetailsOutput;
  headers: Headers;
};

export type NetworkUnavailableFailure = {
  kind: 'network_unavailable';
};

export type AbortedFailure = {
  kind: 'aborted';
};

export type ContractViolationFailure = {
  kind: 'contract_violation';
  reason: ContractViolationReason;
  status: number | null;
  headers: Headers | null;
};

export type RemoteFailure =
  | ServerProblemFailure
  | NetworkUnavailableFailure
  | AbortedFailure
  | ContractViolationFailure;

export type RemoteSuccess<T> = {
  ok: true;
  value: T;
  status: number;
  requestId: string;
  headers: Headers;
};

export type RemoteResult<T> = RemoteSuccess<T> | { ok: false; failure: RemoteFailure };

type WireResponse = {
  data: unknown;
  status: number;
  headers: Headers;
};

type TransportFailureKind = NetworkUnavailableFailure['kind'] | AbortedFailure['kind'];
type SuccessParser<T> = (wire: WireResponse) => RemoteResult<T>;

class TransportFailure extends Error {
  constructor(readonly kind: TransportFailureKind) {
    super(kind);
  }
}

function mediaType(headers: Headers): string | null {
  const contentType = headers.get('content-type');
  if (contentType === null) {
    return null;
  }
  return contentType.split(';', 1)[0]?.trim().toLowerCase() ?? null;
}

function hasNoStore(headers: Headers): boolean {
  return (headers.get('cache-control') ?? '')
    .split(',')
    .map((value) => value.trim().toLowerCase())
    .includes('no-store');
}

function requestId(headers: Headers): string | null {
  const value = headers.get('x-request-id')?.trim();
  return value ? value : null;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function hasOnlyKeys(
  value: unknown,
  allowed: ReadonlySet<string>,
): value is Record<string, unknown> {
  return isRecord(value) && Object.keys(value).every((key) => allowed.has(key));
}

function hasStrictAuthenticationMethodsShape(value: unknown): boolean {
  if (!hasOnlyKeys(value, AUTHENTICATION_METHODS_KEYS)) {
    return false;
  }
  const providers = value.providers;
  const passkeys = value.passkeys;
  return (
    Array.isArray(providers) &&
    providers.every((provider) =>
      hasOnlyKeys(provider, AUTHENTICATION_PROVIDER_METHOD_KEYS),
    ) &&
    Array.isArray(passkeys) &&
    passkeys.every((passkey) => hasOnlyKeys(passkey, PASSKEY_METHOD_KEYS))
  );
}

function hasStrictProblemShape(value: unknown): boolean {
  if (!hasOnlyKeys(value, PROBLEM_KEYS)) {
    return false;
  }
  const errors = value.errors;
  if (errors === undefined || errors === null) {
    return true;
  }
  return (
    Array.isArray(errors) &&
    errors.every((fieldError) => hasOnlyKeys(fieldError, FIELD_ERROR_KEYS))
  );
}

function contractViolation(
  reason: ContractViolationReason,
  wire: WireResponse | null = null,
): RemoteResult<never> {
  return {
    ok: false,
    failure: {
      kind: 'contract_violation',
      reason,
      status: wire?.status ?? null,
      headers: wire?.headers ?? null,
    },
  };
}

function trackedFetch(fetchFn: typeof globalThis.fetch): typeof globalThis.fetch {
  return async (input, init) => {
    try {
      return await fetchFn(input, init);
    } catch (error) {
      if (error instanceof Error && error.name === 'AbortError') {
        throw new TransportFailure('aborted');
      }
      throw new TransportFailure('network_unavailable');
    }
  };
}

function fromThrown(error: unknown): RemoteResult<never> {
  if (error instanceof TransportFailure) {
    return { ok: false, failure: { kind: error.kind } };
  }
  return contractViolation('unexpected_wire_exception');
}

function responseRequestId(wire: WireResponse): RemoteResult<string> {
  if (!hasNoStore(wire.headers)) {
    return contractViolation('cache_policy_mismatch', wire);
  }
  const id = requestId(wire.headers);
  if (id === null) {
    return contractViolation('request_id_mismatch', wire);
  }
  return {
    ok: true,
    value: id,
    status: wire.status,
    requestId: id,
    headers: wire.headers,
  };
}

function success<T>(wire: WireResponse, value: T): RemoteResult<T> {
  const metadata = responseRequestId(wire);
  if (!metadata.ok) {
    return metadata;
  }
  return {
    ok: true,
    value,
    status: wire.status,
    requestId: metadata.value,
    headers: wire.headers,
  };
}

function serverProblem(wire: WireResponse): RemoteResult<never> {
  if (mediaType(wire.headers) !== PROBLEM_MEDIA_TYPE) {
    return contractViolation('content_type_mismatch', wire);
  }
  const metadata = responseRequestId(wire);
  if (!metadata.ok) {
    return metadata;
  }
  if (!hasStrictProblemShape(wire.data)) {
    return contractViolation('invalid_payload', wire);
  }
  const parsed = ProblemDetails.safeParse(wire.data);
  if (!parsed.success) {
    return contractViolation('invalid_payload', wire);
  }
  if (parsed.data.status !== wire.status) {
    return contractViolation('status_mismatch', wire);
  }
  if (parsed.data.request_id !== metadata.value) {
    return contractViolation('request_id_mismatch', wire);
  }
  return {
    ok: false,
    failure: {
      kind: 'server_problem',
      status: wire.status,
      code: parsed.data.code,
      category: parsed.data.category,
      requestId: parsed.data.request_id,
      retryable: parsed.data.retryable,
      fieldErrors: parsed.data.errors ?? [],
      retryAfter: wire.headers.get('retry-after'),
      problem: parsed.data,
      headers: wire.headers,
    },
  };
}

function parseJsonSchema<T>(
  wire: WireResponse,
  keys: ReadonlySet<string>,
  schema: {
    safeParse(value: unknown): { success: true; data: T } | { success: false };
  },
): RemoteResult<T> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE) {
    return contractViolation('content_type_mismatch', wire);
  }
  if (!hasOnlyKeys(wire.data, keys)) {
    return contractViolation('invalid_payload', wire);
  }
  const parsed = schema.safeParse(wire.data);
  return parsed.success
    ? success(wire, parsed.data)
    : contractViolation('invalid_payload', wire);
}

function parseAuthenticatedSession(
  wire: WireResponse,
): RemoteResult<AuthenticatedSession> {
  return parseJsonSchema(
    wire,
    AUTHENTICATED_SESSION_KEYS,
    AuthenticatedSessionResponse,
  );
}

function parseSession(wire: WireResponse): RemoteResult<AuthSession> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE || !isRecord(wire.data)) {
    return contractViolation(
      mediaType(wire.headers) === JSON_MEDIA_TYPE
        ? 'invalid_payload'
        : 'content_type_mismatch',
      wire,
    );
  }
  if (wire.data.authenticated === true) {
    return parseJsonSchema(
      wire,
      AUTHENTICATED_SESSION_KEYS,
      AuthenticatedSessionResponse,
    );
  }
  if (wire.data.authenticated === false) {
    return parseJsonSchema(
      wire,
      UNAUTHENTICATED_SESSION_KEYS,
      UnauthenticatedSessionResponse,
    );
  }
  return contractViolation('invalid_payload', wire);
}

function parseSignupCreated(wire: WireResponse): RemoteResult<SignupCreated> {
  return parseJsonSchema(wire, SIGNUP_CREATED_KEYS, SignupCreatedResponse);
}

function parseSignupVerification(
  wire: WireResponse,
): RemoteResult<SignupVerificationResult> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE || !isRecord(wire.data)) {
    return contractViolation(
      mediaType(wire.headers) === JSON_MEDIA_TYPE
        ? 'invalid_payload'
        : 'content_type_mismatch',
      wire,
    );
  }
  if (wire.data.outcome === 'authenticated') {
    return parseJsonSchema(
      wire,
      SIGNUP_AUTHENTICATED_KEYS,
      SignupAuthenticatedResponse,
    );
  }
  if (wire.data.outcome === 'existing_account') {
    return parseJsonSchema(
      wire,
      EXISTING_ACCOUNT_SIGNUP_KEYS,
      ExistingAccountSignupResponse,
    );
  }
  return contractViolation('invalid_payload', wire);
}

function parseRecoveryAccepted(
  wire: WireResponse,
): RemoteResult<RecoveryAccepted> {
  return parseJsonSchema(wire, RECOVERY_ACCEPTED_KEYS, RecoveryAcceptedResponse);
}

function parseRecoveryValidation(
  wire: WireResponse,
): RemoteResult<RecoveryValidation> {
  return parseJsonSchema(
    wire,
    RECOVERY_VALIDATION_KEYS,
    RecoveryValidationResponse,
  );
}

function parseAuthenticationMethods(
  wire: WireResponse,
): RemoteResult<AuthenticationMethods> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE) {
    return contractViolation('content_type_mismatch', wire);
  }
  if (!hasStrictAuthenticationMethodsShape(wire.data)) {
    return contractViolation('invalid_payload', wire);
  }
  const parsed = AuthenticationMethodsResponse.safeParse(wire.data);
  return parsed.success
    ? success(wire, parsed.data)
    : contractViolation('invalid_payload', wire);
}

function parseGoogleAuthenticationBegun(
  wire: WireResponse,
): RemoteResult<GoogleAuthenticationBegun> {
  return parseJsonSchema(
    wire,
    GOOGLE_AUTHENTICATION_BEGUN_KEYS,
    GoogleAuthenticationBegunResponse,
  );
}

function parseAppleAuthenticationBegun(
  wire: WireResponse,
): RemoteResult<AppleAuthenticationBegun> {
  return parseJsonSchema(
    wire,
    APPLE_AUTHENTICATION_BEGUN_KEYS,
    AppleAuthenticationBegunResponse,
  );
}

function parseProviderAuthenticated(
  wire: WireResponse,
): RemoteResult<ProviderAuthenticated> {
  return parseJsonSchema(
    wire,
    PROVIDER_AUTHENTICATED_KEYS,
    ProviderAuthenticatedResponse,
  );
}

function parseProviderLinkRequired(
  wire: WireResponse,
): RemoteResult<ProviderLinkRequired> {
  return parseJsonSchema(
    wire,
    PROVIDER_LINK_REQUIRED_KEYS,
    ProviderLinkRequiredResponse,
  );
}

function parseProviderEnrollmentRequired(
  wire: WireResponse,
): RemoteResult<ProviderEnrollmentRequired> {
  return parseJsonSchema(
    wire,
    PROVIDER_ENROLLMENT_REQUIRED_KEYS,
    ProviderEnrollmentRequiredResponse,
  );
}

function parseProviderAuthentication(
  wire: WireResponse,
): RemoteResult<ProviderAuthenticationResult> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE || !isRecord(wire.data)) {
    return contractViolation(
      mediaType(wire.headers) === JSON_MEDIA_TYPE
        ? 'invalid_payload'
        : 'content_type_mismatch',
      wire,
    );
  }
  if (wire.data.outcome === 'authenticated') {
    return parseProviderAuthenticated(wire);
  }
  if (wire.data.outcome === 'link_required') {
    return parseProviderLinkRequired(wire);
  }
  if (wire.data.outcome === 'enrollment_required') {
    return parseProviderEnrollmentRequired(wire);
  }
  return contractViolation('invalid_payload', wire);
}

function parseProviderEnrollmentVerification(
  wire: WireResponse,
): RemoteResult<ProviderEnrollmentVerificationResult> {
  if (mediaType(wire.headers) !== JSON_MEDIA_TYPE || !isRecord(wire.data)) {
    return contractViolation(
      mediaType(wire.headers) === JSON_MEDIA_TYPE
        ? 'invalid_payload'
        : 'content_type_mismatch',
      wire,
    );
  }
  if (wire.data.outcome === 'authenticated') {
    return parseProviderAuthenticated(wire);
  }
  if (wire.data.outcome === 'link_required') {
    return parseProviderLinkRequired(wire);
  }
  return contractViolation('invalid_payload', wire);
}

function parseProviderLink(wire: WireResponse): RemoteResult<ProviderLink> {
  return parseJsonSchema(wire, PROVIDER_LINK_KEYS, ProviderLinkResponse);
}

function parsePasskeyCeremony(wire: WireResponse): RemoteResult<PasskeyCeremony> {
  return parseJsonSchema(wire, PASSKEY_CEREMONY_KEYS, PasskeyCeremonyResponse);
}

function expectedResult<T>(
  wire: WireResponse,
  expectedStatus: number,
  parser: SuccessParser<T>,
): RemoteResult<T> {
  if (wire.status === expectedStatus) {
    return parser(wire);
  }
  if (wire.status >= 400) {
    return serverProblem(wire);
  }
  return contractViolation('unexpected_status', wire);
}

function expectedVoidResult(
  wire: WireResponse,
  expectedStatus: number,
): RemoteResult<void> {
  if (wire.status === expectedStatus) {
    return success(wire, undefined);
  }
  if (wire.status >= 400) {
    return serverProblem(wire);
  }
  return contractViolation('unexpected_status', wire);
}

export type DanteApiClient = {
  signIn(
    request: SignInRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
  getSession(options?: RequestInit): Promise<RemoteResult<AuthSession>>;
  getAuthenticationMethods(
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticationMethods>>;
  establishPassword(
    request: PasswordEstablishRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
  removePassword(options?: RequestInit): Promise<RemoteResult<AuthenticatedSession>>;
  logOut(options?: RequestInit): Promise<RemoteResult<void>>;
  beginSignup(
    request: SignupRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<SignupCreated>>;
  verifySignup(
    request: SignupVerificationRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<SignupVerificationResult>>;
  resendSignupVerification(
    request: SignupResendRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<SignupCreated>>;
  requestPasswordRecovery(
    request: PasswordRecoveryRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<RecoveryAccepted>>;
  validatePasswordRecovery(
    request: PasswordRecoveryValidationRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<RecoveryValidation>>;
  resetPassword(
    request: PasswordResetRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<void>>;
  reauthenticate(
    request: ReauthenticateRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
  beginGoogleAuthentication(
    request: ProviderBeginRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<GoogleAuthenticationBegun>>;
  completeGoogleAuthentication(
    request: GoogleAuthenticationCompleteRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<ProviderAuthenticationResult>>;
  beginAppleAuthentication(
    request: ProviderBeginRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AppleAuthenticationBegun>>;
  getProviderEnrollment(
    options?: RequestInit,
  ): Promise<RemoteResult<ProviderEnrollmentRequired>>;
  setProviderEnrollmentEmail(
    request: ProviderEnrollmentEmailRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<ProviderEnrollmentRequired>>;
  resendProviderEnrollmentVerification(
    options?: RequestInit,
  ): Promise<RemoteResult<ProviderEnrollmentRequired>>;
  verifyProviderEnrollment(
    request: ProviderEnrollmentVerificationRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<ProviderEnrollmentVerificationResult>>;
  getProviderLink(options?: RequestInit): Promise<RemoteResult<ProviderLink>>;
  confirmProviderLink(
    options?: RequestInit,
  ): Promise<RemoteResult<ProviderAuthenticated>>;
  unlinkProvider(
    externalIdentityRef: string,
    options?: RequestInit,
  ): Promise<RemoteResult<ProviderAuthenticated>>;
  beginPasskeyRegistration(
    options?: RequestInit,
  ): Promise<RemoteResult<PasskeyCeremony>>;
  completePasskeyRegistration(
    request: PasskeyRegistrationCompleteRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
  beginPasskeyAuthentication(
    options?: RequestInit,
  ): Promise<RemoteResult<PasskeyCeremony>>;
  completePasskeyAuthentication(
    request: PasskeyAuthenticationCompleteRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
  beginPasskeyReauthentication(
    options?: RequestInit,
  ): Promise<RemoteResult<PasskeyCeremony>>;
  completePasskeyReauthentication(
    request: PasskeyReauthenticationCompleteRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
  updatePasskey(
    passkeyCredentialRef: string,
    request: PasskeyUpdateRequest,
    options?: RequestInit,
  ): Promise<RemoteResult<void>>;
  removePasskey(
    passkeyCredentialRef: string,
    options?: RequestInit,
  ): Promise<RemoteResult<AuthenticatedSession>>;
};

export function createDanteApiClient(
  options: {
    fetchFn?: typeof globalThis.fetch;
  } = {},
): DanteApiClient {
  const fetchFn = trackedFetch(options.fetchFn ?? globalThis.fetch);

  return {
    async signIn(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthSignIn(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async getSession(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthGetSession(
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async getAuthenticationMethods(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthGetAuthenticationMethods(
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticationMethods);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async establishPassword(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthEstablishPassword(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async removePassword(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthRemovePassword(
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async logOut(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthLogOut(requestOptions, fetchFn);
        return expectedVoidResult(wire, 204);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async beginSignup(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthBeginSignup(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseSignupCreated);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async verifySignup(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthVerifySignup(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseSignupVerification);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async resendSignupVerification(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthResendSignupVerification(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseSignupCreated);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async requestPasswordRecovery(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthRequestPasswordRecovery(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 202, parseRecoveryAccepted);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async validatePasswordRecovery(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthValidatePasswordRecovery(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseRecoveryValidation);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async resetPassword(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthResetPassword(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedVoidResult(wire, 204);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async reauthenticate(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthReauthenticate(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async beginGoogleAuthentication(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthBeginGoogleAuthentication(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseGoogleAuthenticationBegun);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async completeGoogleAuthentication(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthCompleteGoogleAuthentication(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseProviderAuthentication);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async beginAppleAuthentication(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthBeginAppleAuthentication(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAppleAuthenticationBegun);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async getProviderEnrollment(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthGetProviderEnrollment(
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseProviderEnrollmentRequired);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async setProviderEnrollmentEmail(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthSetProviderEnrollmentEmail(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseProviderEnrollmentRequired);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async resendProviderEnrollmentVerification(requestOptions) {
      try {
        const wire: WireResponse =
          await generatedAuthResendProviderEnrollmentVerification(
            {},
            requestOptions,
            fetchFn,
          );
        return expectedResult(wire, 200, parseProviderEnrollmentRequired);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async verifyProviderEnrollment(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthVerifyProviderEnrollment(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseProviderEnrollmentVerification);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async getProviderLink(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthGetProviderLink(
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseProviderLink);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async confirmProviderLink(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthConfirmProviderLink(
          {},
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseProviderAuthenticated);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async unlinkProvider(externalIdentityRef, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthUnlinkProvider(
          externalIdentityRef,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseProviderAuthenticated);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async beginPasskeyRegistration(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthBeginPasskeyRegistration(
          {},
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parsePasskeyCeremony);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async completePasskeyRegistration(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthCompletePasskeyRegistration(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async beginPasskeyAuthentication(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthBeginPasskeyAuthentication(
          {},
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parsePasskeyCeremony);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async completePasskeyAuthentication(request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthCompletePasskeyAuthentication(
          request,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async beginPasskeyReauthentication(requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthBeginPasskeyReauthentication(
          {},
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parsePasskeyCeremony);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async completePasskeyReauthentication(request, requestOptions) {
      try {
        const wire: WireResponse =
          await generatedAuthCompletePasskeyReauthentication(
            request,
            requestOptions,
            fetchFn,
          );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async updatePasskey(passkeyCredentialRef, request, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthUpdatePasskey(
          passkeyCredentialRef,
          request,
          requestOptions,
          fetchFn,
        );
        return expectedVoidResult(wire, 204);
      } catch (error) {
        return fromThrown(error);
      }
    },

    async removePasskey(passkeyCredentialRef, requestOptions) {
      try {
        const wire: WireResponse = await generatedAuthRemovePasskey(
          passkeyCredentialRef,
          requestOptions,
          fetchFn,
        );
        return expectedResult(wire, 200, parseAuthenticatedSession);
      } catch (error) {
        return fromThrown(error);
      }
    },
  };
}
