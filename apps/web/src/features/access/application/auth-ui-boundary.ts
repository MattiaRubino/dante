import {
  WebAuthRemoteError,
  type WebAuthRemoteFailure,
  type WebProviderAuthenticationResult,
} from '../../../platform/auth/web-auth-remote';

export {
  appleAuthenticationEnabledFromBuild,
  googleAuthenticationEnabledFromBuild,
  passkeyAuthenticationEnabledFromBuild,
  ProviderBrowserUnavailableError,
  renderGoogleIdentityButton,
} from '../../../platform/auth/web-auth-provider';

export { WebAuthRemoteError };
export type { WebProviderAuthenticationResult };

export function authRemoteFailureFromUnknown(
  error: unknown,
): WebAuthRemoteFailure | null {
  if (error instanceof WebAuthRemoteError) {
    return error.failure;
  }
  if (
    typeof error !== 'object' ||
    error === null ||
    !('name' in error) ||
    error.name !== 'WebAuthRemoteError' ||
    !('failure' in error)
  ) {
    return null;
  }
  const failure = error.failure;
  if (typeof failure !== 'object' || failure === null || !('kind' in failure)) {
    return null;
  }
  switch (failure.kind) {
    case 'aborted':
    case 'network_unavailable':
    case 'contract_violation':
    case 'server_problem':
      return failure as WebAuthRemoteFailure;
    default:
      return null;
  }
}
