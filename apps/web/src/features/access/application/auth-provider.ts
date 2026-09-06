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
  type WebGoogleAuthenticationBegun,
  type WebProviderAuthenticationResult,
  type WebProviderEnrollmentRequired,
  type WebProviderEnrollmentVerificationResult,
  type WebProviderLink,
  type WebProviderPurpose,
  type WebProviderReturnTarget,
} from '../../../platform/auth/web-auth-remote';
import {
  googleClientIdFromBuild,
  redirectToAppleAuthorization,
} from '../../../platform/auth/web-auth-provider';
import { commitAuthoritativeAuthSession } from './auth-session';

export type AccessProviderCode = 'google' | 'apple';

export type ProviderAuthenticationInput = Readonly<{
  purpose: WebProviderPurpose;
  returnTarget: WebProviderReturnTarget;
  csrfToken?: string;
  signal?: AbortSignal;
}>;

export type GoogleAuthenticationPreparation = Readonly<{
  clientId: string;
  begun: WebGoogleAuthenticationBegun;
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

function continuationMissing(error: unknown, code: string): boolean {
  return (
    error instanceof WebAuthRemoteError &&
    error.failure.kind === 'server_problem' &&
    error.failure.code === code
  );
}

function providerRequest(input: ProviderAuthenticationInput) {
  return {
    purpose: input.purpose,
    return_target: input.returnTarget,
  } as const;
}

export async function prepareGoogleAuthentication(
  input: ProviderAuthenticationInput,
): Promise<GoogleAuthenticationPreparation | null> {
  const clientId = googleClientIdFromBuild();
  if (clientId.length === 0) {
    return null;
  }
  const begun = await webAuthRemote.beginGoogleAuthentication(
    providerRequest(input),
    input.csrfToken,
    input.signal,
  );
  return { clientId, begun };
}

export async function completeGoogleAuthentication({
  preparation,
  credential,
  signal,
}: Readonly<{
  preparation: GoogleAuthenticationPreparation;
  credential: string;
  signal?: AbortSignal;
}>): Promise<WebProviderAuthenticationResult> {
  return webAuthRemote.completeGoogleAuthentication(
    {
      external_auth_transaction_ref:
        preparation.begun.external_auth_transaction_ref,
      state: preparation.begun.state,
      credential,
    },
    signal,
  );
}

export async function beginAppleAuthentication(
  input: ProviderAuthenticationInput,
): Promise<void> {
  const begun = await webAuthRemote.beginAppleAuthentication(
    providerRequest(input),
    input.csrfToken,
    input.signal,
  );
  redirectToAppleAuthorization(begun.authorization_url);
}

export async function resolveProviderContinuation(
  signal?: AbortSignal,
): Promise<ProviderContinuation> {
  try {
    const enrollment = await webAuthRemote.getProviderEnrollment(signal);
    return { kind: 'enrollment', enrollment };
  } catch (error) {
    if (
      !continuationMissing(error, 'auth.provider_enrollment_invalid_or_expired')
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

async function cacheAuthenticatedSession(
  queryClient: ReturnType<typeof useQueryClient>,
  session: WebAuthenticatedSession,
): Promise<void> {
  await commitAuthoritativeAuthSession(queryClient, session);
}

export function usePrepareGoogleAuthenticationMutation() {
  return useMutation({
    mutationFn: prepareGoogleAuthentication,
    retry: false,
  });
}

export function useCompleteGoogleAuthenticationMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: completeGoogleAuthentication,
    retry: false,
    onSuccess: async (result) => {
      if (result.outcome === 'authenticated') {
        await cacheAuthenticatedSession(queryClient, result);
      }
    },
  });
}

export function useAppleAuthenticationMutation() {
  return useMutation({
    mutationFn: beginAppleAuthentication,
    retry: false,
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
    onSuccess: async (result: WebProviderEnrollmentVerificationResult) => {
      if (result.outcome === 'authenticated') {
        await cacheAuthenticatedSession(queryClient, result);
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
