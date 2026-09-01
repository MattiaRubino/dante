import { useMutation, useQueryClient } from '@tanstack/react-query';

import {
  webAuthRemote,
  type WebAuthenticatedSession,
} from '../../../platform/auth/web-auth-remote';
import {
  createPasskeyAuthenticationEvidence,
  createPasskeyReauthenticationEvidence,
  createPasskeyRegistrationEvidence,
} from '../../../platform/auth/web-auth-webauthn';
import { authenticationMethodsQueryKey } from './auth-methods';
import { authSessionQueryKey } from './auth-session';

function cacheAuthenticatedSession(
  queryClient: ReturnType<typeof useQueryClient>,
  session: WebAuthenticatedSession,
): void {
  queryClient.setQueryData(authSessionQueryKey, session);
}

async function refreshMethods(
  queryClient: ReturnType<typeof useQueryClient>,
): Promise<void> {
  await queryClient.invalidateQueries({
    queryKey: authenticationMethodsQueryKey,
  });
}

export async function signInWithPasskey(
  signal?: AbortSignal,
): Promise<WebAuthenticatedSession> {
  const ceremony = await webAuthRemote.beginPasskeyAuthentication(signal);
  const evidence = await createPasskeyAuthenticationEvidence({
    ceremony,
    ...(signal === undefined ? {} : { signal }),
  });
  return webAuthRemote.completePasskeyAuthentication(evidence, signal);
}

export async function registerPasskey({
  label,
  csrfToken,
  signal,
}: Readonly<{
  label: string;
  csrfToken: string;
  signal?: AbortSignal;
}>): Promise<WebAuthenticatedSession> {
  const ceremony = await webAuthRemote.beginPasskeyRegistration(
    csrfToken,
    signal,
  );
  const evidence = await createPasskeyRegistrationEvidence({
    ceremony,
    label,
    ...(signal === undefined ? {} : { signal }),
  });
  return webAuthRemote.completePasskeyRegistration(evidence, csrfToken, signal);
}

export async function reauthenticateWithPasskey({
  csrfToken,
  signal,
}: Readonly<{
  csrfToken: string;
  signal?: AbortSignal;
}>): Promise<WebAuthenticatedSession> {
  const ceremony = await webAuthRemote.beginPasskeyReauthentication(
    csrfToken,
    signal,
  );
  const evidence = await createPasskeyReauthenticationEvidence({
    ceremony,
    ...(signal === undefined ? {} : { signal }),
  });
  return webAuthRemote.completePasskeyReauthentication(
    evidence,
    csrfToken,
    signal,
  );
}

export function usePasskeySignInMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: () => signInWithPasskey(),
    retry: false,
    onSuccess: (session) => cacheAuthenticatedSession(queryClient, session),
  });
}

export function usePasskeyRegistrationMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      label,
      csrfToken,
    }: {
      label: string;
      csrfToken: string;
    }) => registerPasskey({ label, csrfToken }),
    retry: false,
    onSuccess: async (session) => {
      cacheAuthenticatedSession(queryClient, session);
      await refreshMethods(queryClient);
    },
  });
}

export function usePasskeyReauthenticationMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ csrfToken }: { csrfToken: string }) =>
      reauthenticateWithPasskey({ csrfToken }),
    retry: false,
    onSuccess: (session) => cacheAuthenticatedSession(queryClient, session),
  });
}

export function useUpdatePasskeyMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      passkeyCredentialRef,
      label,
      csrfToken,
    }: {
      passkeyCredentialRef: string;
      label: string;
      csrfToken: string;
    }) =>
      webAuthRemote.updatePasskey(passkeyCredentialRef, { label }, csrfToken),
    retry: false,
    onSuccess: async () => refreshMethods(queryClient),
  });
}

export function useRemovePasskeyMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      passkeyCredentialRef,
      csrfToken,
    }: {
      passkeyCredentialRef: string;
      csrfToken: string;
    }) => webAuthRemote.removePasskey(passkeyCredentialRef, csrfToken),
    retry: false,
    onSuccess: async (session) => {
      cacheAuthenticatedSession(queryClient, session);
      await refreshMethods(queryClient);
    },
  });
}
