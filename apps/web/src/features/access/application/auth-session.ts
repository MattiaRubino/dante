import {
  queryOptions,
  useMutation,
  useQuery,
  useQueryClient,
} from '@tanstack/react-query';

import {
  WebAuthRemoteError,
  webAuthRemote,
  type WebAuthenticatedSession,
  type WebAuthSession,
  type WebAuthSignInRequest,
} from '../../../platform/auth/web-auth-remote';
import type { AccessFlowEvent } from '../model/access-flow';

export const authSessionQueryKey = ['auth', 'session'] as const;

export type AccessAuthSession =
  | WebAuthenticatedSession
  | Readonly<{ authenticated: false }>;

function accessAuthSession(session: WebAuthSession): AccessAuthSession {
  if ('csrf_token' in session) {
    return session;
  }
  return { authenticated: false };
}

function isRetryableSessionRead(error: unknown): boolean {
  if (!(error instanceof WebAuthRemoteError)) {
    return false;
  }

  const failure = error.failure;
  if (failure.kind === 'network_unavailable') {
    return true;
  }
  return (
    failure.kind === 'server_problem' &&
    failure.retryable &&
    failure.status >= 500
  );
}

function retryAfterSeconds(value: string | null): number | undefined {
  if (value === null || !/^\d+$/.test(value)) {
    return undefined;
  }
  const parsed = Number(value);
  return Number.isSafeInteger(parsed) && parsed >= 0 ? parsed : undefined;
}

function rateLimitedEvent(retryAfter: string | null): AccessFlowEvent {
  const seconds = retryAfterSeconds(retryAfter);
  return seconds === undefined
    ? { type: 'SERVER_RATE_LIMITED' }
    : { type: 'SERVER_RATE_LIMITED', retryAfterSeconds: seconds };
}

export function accessEventForAuthError(
  error: unknown,
  online = typeof navigator === 'undefined' ? true : navigator.onLine,
): AccessFlowEvent | null {
  if (!(error instanceof WebAuthRemoteError)) {
    return { type: 'SERVER_UNEXPECTED' };
  }

  const failure = error.failure;
  switch (failure.kind) {
    case 'aborted':
      return null;
    case 'network_unavailable':
      return online
        ? { type: 'SERVER_UNAVAILABLE' }
        : { type: 'NETWORK_OFFLINE' };
    case 'contract_violation':
      return { type: 'SERVER_UNEXPECTED' };
    case 'server_problem':
      switch (failure.code) {
        case 'auth.invalid_credentials':
          return { type: 'SERVER_INVALID_CREDENTIALS' };
        case 'auth.account_unavailable':
          return { type: 'SERVER_ACCOUNT_UNAVAILABLE' };
        case 'auth.password_compromised':
          return { type: 'SERVER_PASSWORD_COMPROMISED' };
        case 'auth.verification_invalid_or_expired':
        case 'auth.verification_attempts_exhausted':
          return { type: 'SERVER_VERIFICATION_INVALID_OR_EXPIRED' };
        case 'auth.recovery_invalid_or_expired':
          return { type: 'SERVER_RECOVERY_INVALID_OR_EXPIRED' };
        case 'auth.reauthentication_required':
          return { type: 'SERVER_REAUTH_REQUIRED' };
        case 'request.validation_failed':
        case 'request.malformed':
          return { type: 'SERVER_REQUEST_INVALID' };
        case 'rate_limit.exceeded':
        case 'auth.signup_rate_limited':
        case 'auth.signup_resend_cooldown':
        case 'auth.recovery_rate_limited':
        case 'auth.reauthentication_rate_limited':
          return rateLimitedEvent(failure.retryAfter);
        case 'auth.email_delivery_unavailable':
        case 'service.unavailable':
        case 'dependency.unavailable':
          return { type: 'SERVER_UNAVAILABLE' };
        default:
          if (failure.category === 'rate_limit') {
            return rateLimitedEvent(failure.retryAfter);
          }
          if (failure.category === 'validation') {
            return { type: 'SERVER_REQUEST_INVALID' };
          }
          if (failure.status >= 500) {
            return { type: 'SERVER_UNAVAILABLE' };
          }
          return { type: 'SERVER_UNEXPECTED' };
      }
  }
}

export function authSessionQueryOptions() {
  return queryOptions({
    queryKey: authSessionQueryKey,
    queryFn: async ({ signal }): Promise<AccessAuthSession> =>
      accessAuthSession(await webAuthRemote.getSession(signal)),
    retry: (failureCount, error) =>
      failureCount < 1 && isRetryableSessionRead(error),
    staleTime: 1_000,
    refetchOnReconnect: true,
    refetchOnWindowFocus: true,
  });
}

export function useAuthSessionQuery() {
  return useQuery(authSessionQueryOptions());
}

export function useSignInMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (request: WebAuthSignInRequest) =>
      webAuthRemote.signIn(request),
    retry: false,
    onSuccess: (session) => {
      queryClient.setQueryData<AccessAuthSession>(authSessionQueryKey, session);
    },
  });
}

export function useLogOutMutation() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ csrfToken }: { csrfToken: string }) =>
      webAuthRemote.logOut(csrfToken),
    retry: false,
    onSuccess: () => {
      queryClient.setQueryData<AccessAuthSession>(authSessionQueryKey, {
        authenticated: false,
      });
    },
  });
}
