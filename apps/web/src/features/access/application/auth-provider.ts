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
  type WebProviderAuthenticationResult,
  type WebProviderEnrollmentRequired,
  type WebProviderEnrollmentVerificationResult,
  type WebProviderLink,
  type WebProviderPurpose,
  type WebProviderReturnTarget,
} from '../../../platform/auth/web-auth-remote';
import {
  redirectToAppleAuthorization,
  requestGoogleCredential,
} from '../../../platform/auth/web-auth-provider';
import { authSessionQueryKey } from './auth-session';

export type AccessProviderCode = 'google' | 'apple';

export type ProviderAuthenticationInput = Readonly<{
  provider: AccessProviderCode;
  purpose: WebProviderPurpose;
  returnTarget: WebProviderReturnTarget;
  csrfToken?: string;
  signal?: AbortSignal;
}>;

export type ProviderAuthenticationOutcome =
  | Readonly<{
      kind: 'result';
      provider: 'google';
      result: WebProviderAuthenticationResult;
    }>
  | Readonly<{
      kind: 'redirected';
      provider: 'apple';
    }>;

export type ProviderContinuation =
  | Readonly<{ kind: 'none' }>
  | Readonly<{
      kind: 'enrollment';
      enrollment: WebProviderEnrollmentRequired;
    }>
  | Readonly<{
      kind: 'link';
      link: WebProviderLink;
    }>;

export const providerContinuationQueryKey = [
  'auth',
  'provider-continuation',
] as const;

function configuredGoogleClientId(): string {
  const value = import.meta.env.VITE_DANTE_GOOGLE_CLIENT_ID;
  return typeof value === 'string' ? value.trim() : '';
}

function continuationMissing(error: unknown, code: string): boolean {
  return (
    error instanceof WebAuthRemoteError &&
    error.failure.kind === 'server_problem' &&
    error.failure.code === code
  );
}

export async function runProviderAuthentication(
  input: ProviderAuthenticationInput,
): Promise<ProviderAuthenticationOutcome> {
  const request = {
    purpose: input.purpose,
    return_target: input.returnTarget,
  } as const;

  if (input.provider === 'google') {
    const begun = await webAuthRemote.beginGoogleAuthentication(
      request,
      input.csrfToken,
      input.signal,
    );
    const credential = await requestGoogleCredential({
      clientId: configuredGoogleClientId(),
      nonce: begun.nonce,
      signal: input.signal,
    });
    const result = await webAuthRemote.completeGoogleAuthentication(
      {
        external_auth_transaction_ref: begun.external_auth_transaction_ref,
        state: begun.state,
        credential,
      },
      input.signal,
    );
    return { kind: 'result', provider: 'google', result };
  }

  const begun = await webAuthRemote.beginAppleAuthentication(
    request,
    input.csrfToken,
    input.signal,
  );
  redirectToAppleAuthorization(begun.authorization_url);
  return { kind: 'redirected', provider: 'apple' };
}

export async function resolveProviderContinuation(
  signal?: AbortSignal,
): Promise<ProviderContinuation> {
  try {
    const enrollment = await webAuthRemote.getProviderEnrollment(signal);
    return { kind: 'enrollment', enrollment };
  } catch (error) {
    if (
      !continuationMissing(
        error,
        'auth.provider_enrollment_invalid_or_expired',
      )
    ) {
      throw error;
    }
  }

  try {
    const link = await webAuthRemote.getProviderLink(signal);
    return { kind: 'link', link };
  } catch (error) {
    if (!continuationMissing(error, 'auth.provider_link_invalid_or_expired')) {
      throw error;
    }
  }
  return { kind: 'none' };
}

export function providerContinuationQueryOptions(enabled = true) {
  return queryOptions({
    queryKey: providerContinuationQueryKey,
    queryFn: ({ signal }) => resolveProviderContinuation(signal),
    enabled,
    retry: false,
    staleTime: 0,
  });
}

export function useProviderContinuationQuery(enabled = true) {
  return useQuery(providerContinuationQueryOptions(enabled));
}

function cacheAuthenticatedSession(
  queryClient: ReturnType<typeof useQueryClient>,
  session: WebAuthenticatedSession,
): void {
  queryClient.setQueryData(authSessionQueryKey, session);
}

export function useProviderAuthenticationMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: runProviderAuthentication,
    retry: false,
    onSuccess: (outcome) => {
      if (
        outcome.kind === 'result' &&
        outcome.result.outcome === 'authenticated'
      ) {
        cacheAuthenticatedSession(queryClient, outcome.result);
      }
    },
  });
}

export function useSetProviderEnrollmentEmailMutation() {
  return useMutation({
    mutationFn: ({ email }: { email: string }) =>
      webAuthRemote.setProviderEnrollmentEmail({ email }),
    retry: false,
  });
}

export function useResendProviderEnrollmentMutation() {
  return useMutation({
    mutationFn: () => webAuthRemote.resendProviderEnrollmentVerification(),
    retry: false,
  });
}

export function useVerifyProviderEnrollmentMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ code }: { code: string }) =>
      webAuthRemote.verifyProviderEnrollment({ code }),
    retry: false,
    onSuccess: (result: WebProviderEnrollmentVerificationResult) => {
      if (result.outcome === 'authenticated') {
        cacheAuthenticatedSession(queryClient, result);
      }
    },
  });
}

export function useConfirmProviderLinkMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ csrfToken }: { csrfToken: string }) =>
      webAuthRemote.confirmProviderLink(csrfToken),
    retry: false,
    onSuccess: (session) => cacheAuthenticatedSession(queryClient, session),
  });
}

export function useUnlinkProviderMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      externalIdentityRef,
      csrfToken,
    }: {
      externalIdentityRef: string;
      csrfToken: string;
    }) => webAuthRemote.unlinkProvider(externalIdentityRef, csrfToken),
    retry: false,
    onSuccess: (session) => cacheAuthenticatedSession(queryClient, session),
  });
}
