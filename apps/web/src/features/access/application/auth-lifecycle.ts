import { useMutation, useQueryClient } from '@tanstack/react-query';

import {
  webAuthRemote,
  type WebAuthenticatedSession,
  type WebPasswordRecoveryRequest,
  type WebPasswordRecoveryValidationRequest,
  type WebPasswordResetRequest,
  type WebSignupRequest,
  type WebSignupResendRequest,
  type WebSignupVerificationRequest,
  type WebSignupVerificationResult,
} from '../../../platform/auth/web-auth-remote';
import { commitAuthoritativeAuthSession } from './auth-session';

export type { RecoveryProofStore } from '../../../platform/auth/recovery-proof';

export function authenticatedSessionFromSignup(
  result: WebSignupVerificationResult,
): WebAuthenticatedSession | null {
  if (result.outcome !== 'authenticated') {
    return null;
  }
  return {
    authenticated: result.authenticated,
    account_ref: result.account_ref,
    auth_session_ref: result.auth_session_ref,
    recent_auth_at: result.recent_auth_at,
    expires_at: result.expires_at,
    csrf_token: result.csrf_token,
  };
}

export function useBeginSignupMutation() {
  return useMutation({
    mutationFn: (request: WebSignupRequest) =>
      webAuthRemote.beginSignup(request),
    retry: false,
  });
}

export function useVerifySignupMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: WebSignupVerificationRequest) =>
      webAuthRemote.verifySignup(request),
    retry: false,
    onSuccess: async (result) => {
      const session = authenticatedSessionFromSignup(result);
      if (session !== null) {
        await commitAuthoritativeAuthSession(queryClient, session);
      }
    },
  });
}

export function useResendSignupVerificationMutation() {
  return useMutation({
    mutationFn: (request: WebSignupResendRequest) =>
      webAuthRemote.resendSignupVerification(request),
    retry: false,
  });
}

export function useRequestPasswordRecoveryMutation() {
  return useMutation({
    mutationFn: (request: WebPasswordRecoveryRequest) =>
      webAuthRemote.requestPasswordRecovery(request),
    retry: false,
  });
}

export function useValidatePasswordRecoveryMutation() {
  return useMutation({
    mutationFn: (request: WebPasswordRecoveryValidationRequest) =>
      webAuthRemote.validatePasswordRecovery(request),
    retry: false,
  });
}

export function useResetPasswordMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (request: WebPasswordResetRequest) =>
      webAuthRemote.resetPassword(request),
    retry: false,
    onSuccess: () =>
      commitAuthoritativeAuthSession(queryClient, { authenticated: false }),
  });
}

export function useReauthenticateMutation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({
      password,
      csrfToken,
    }: {
      password: string;
      csrfToken: string;
    }) => webAuthRemote.reauthenticate({ password }, csrfToken),
    retry: false,
    onSuccess: (session) =>
      commitAuthoritativeAuthSession(queryClient, session),
  });
}
