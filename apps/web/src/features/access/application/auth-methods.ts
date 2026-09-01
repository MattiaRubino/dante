import {
  queryOptions,
  useMutation,
  useQuery,
  useQueryClient,
} from '@tanstack/react-query';

import {
  webAuthRemote,
  type WebAuthenticationMethods,
} from '../../../platform/auth/web-auth-remote';
import { authSessionQueryKey } from './auth-session';

export const authenticationMethodsQueryKey = ['auth', 'methods'] as const;

export function authenticationMethodsQueryOptions(enabled = true) {
  return queryOptions({
    queryKey: authenticationMethodsQueryKey,
    queryFn: ({ signal }) => webAuthRemote.getAuthenticationMethods(signal),
    enabled,
    retry: false,
    staleTime: 1_000,
    refetchOnReconnect: true,
    refetchOnWindowFocus: true,
  });
}

export function useAuthenticationMethodsQuery(enabled = true) {
  return useQuery(authenticationMethodsQueryOptions(enabled));
}

function cacheMethodsAfterMutation(
  queryClient: ReturnType<typeof useQueryClient>,
): Promise<void> {
  return queryClient.invalidateQueries({
    queryKey: authenticationMethodsQueryKey,
  });
}

export function useEstablishPasswordMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      newPassword,
      csrfToken,
    }: {
      newPassword: string;
      csrfToken: string;
    }) =>
      webAuthRemote.establishPassword(
        { new_password: newPassword },
        csrfToken,
      ),
    retry: false,
    onSuccess: async (session) => {
      queryClient.setQueryData(authSessionQueryKey, session);
      await cacheMethodsAfterMutation(queryClient);
    },
  });
}

export function useRemovePasswordMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ csrfToken }: { csrfToken: string }) =>
      webAuthRemote.removePassword(csrfToken),
    retry: false,
    onSuccess: async (session) => {
      queryClient.setQueryData(authSessionQueryKey, session);
      await cacheMethodsAfterMutation(queryClient);
    },
  });
}

export type { WebAuthenticationMethods };
