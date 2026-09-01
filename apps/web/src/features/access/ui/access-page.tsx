import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useReducer,
  useRef,
  useState,
} from 'react';
import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';
import {
  type RecoveryProofStore,
  useBeginSignupMutation,
  useReauthenticateMutation,
  useRequestPasswordRecoveryMutation,
  useResendSignupVerificationMutation,
  useResetPasswordMutation,
  useValidatePasswordRecoveryMutation,
  useVerifySignupMutation,
} from '../application/auth-lifecycle';
import { usePasskeySignInMutation } from '../application/auth-passkey';
import {
  type ProviderContinuation,
  useConfirmProviderLinkMutation,
  useProviderAuthenticationMutation,
  useProviderContinuationQuery,
  useResendProviderEnrollmentMutation,
  useSetProviderEnrollmentEmailMutation,
  useVerifyProviderEnrollmentMutation,
} from '../application/auth-provider';
import {
  accessEventForAuthError,
  useAuthSessionQuery,
  useLogOutMutation,
  useSignInMutation,
} from '../application/auth-session';
import {
  accessFlowReducer,
  initialAccessFlowState,
  type AccessFlowEvent,
  type AccessFlowState,
  type AccessProvider,
} from '../model/access-flow';
import { AccessBrandStage } from './access-brand-stage';
import {
  AccessFlowPanel,
  type AccessRecoveryEntryState,
} from './access-flow-panel';
import { AccessLocaleSwitcher } from './access-locale-switcher';
import { AccessProviderFlowPanel } from './access-provider-flow-panel';
import '../access.css';
import '../access-composition.css';
import '../access-flow.css';

function initialFlowState(
  authenticated: boolean,
  sessionError: unknown,
  recoveryProofPresent: boolean,
): AccessFlowState {
  let state =
    authenticated && !recoveryProofPresent
      ? accessFlowReducer(initialAccessFlowState, {
          type: 'SERVER_AUTHENTICATED',
        })
      : initialAccessFlowState;

  if (sessionError === null || sessionError === undefined) {
    return state;
  }

  const event = accessEventForAuthError(sessionError);
  if (event !== null) {
    state = accessFlowReducer(state, event);
  }
  return state;
}

function isRecoveryInvalidEvent(event: AccessFlowEvent | null): boolean {
  return event?.type === 'SERVER_RECOVERY_INVALID_OR_EXPIRED';
}

function requestedProvider(flow: AccessFlowState): AccessProvider | null {
  if (flow.condition.kind !== 'backend-required') {
    return null;
  }
  if (flow.condition.operation === 'provider-google') {
    return 'google';
  }
  if (flow.condition.operation === 'provider-apple') {
    return 'apple';
  }
  return null;
}

export function AccessPage({
  recoveryProofStore,
}: Readonly<{ recoveryProofStore: RecoveryProofStore }>) {
  const { t } = useTranslation('common');
  const sessionQuery = useAuthSessionQuery();
  const [hadRecoveryProofAtMount] = useState(
    () => recoveryProofStore.peek() !== null,
  );
  const [recoveryEntryState, setRecoveryEntryState] =
    useState<AccessRecoveryEntryState>(
      hadRecoveryProofAtMount ? 'validating' : 'none',
    );
  const recoveryValidationStarted = useRef(false);
  const providerStart = useRef<AccessProvider | null>(null);
  const [signupRef, setSignupRef] = useState<string | null>(null);
  const [providerContinuation, setProviderContinuation] =
    useState<ProviderContinuation>({ kind: 'none' });
  const [providerError, setProviderError] = useState<string | null>(null);
  const [flow, dispatch] = useReducer(
    accessFlowReducer,
    initialFlowState(
      sessionQuery.data?.authenticated === true,
      sessionQuery.error,
      hadRecoveryProofAtMount,
    ),
  );

  const signInMutation = useSignInMutation();
  const logOutMutation = useLogOutMutation();
  const beginSignupMutation = useBeginSignupMutation();
  const verifySignupMutation = useVerifySignupMutation();
  const resendSignupMutation = useResendSignupVerificationMutation();
  const recoveryMutation = useRequestPasswordRecoveryMutation();
  const validateRecoveryMutation = useValidatePasswordRecoveryMutation();
  const resetPasswordMutation = useResetPasswordMutation();
  const reauthenticateMutation = useReauthenticateMutation();
  const providerMutation = useProviderAuthenticationMutation();
  const continuationQuery = useProviderContinuationQuery(
    recoveryEntryState === 'none',
  );
  const setEnrollmentEmailMutation = useSetProviderEnrollmentEmailMutation();
  const resendEnrollmentMutation = useResendProviderEnrollmentMutation();
  const verifyEnrollmentMutation = useVerifyProviderEnrollmentMutation();
  const confirmLinkMutation = useConfirmProviderLinkMutation();
  const linkPasskeyMutation = usePasskeySignInMutation();

  const dispatchAuthError = useCallback(
    (error: unknown): AccessFlowEvent | null => {
      const event = accessEventForAuthError(error);
      if (event !== null) {
        if (isRecoveryInvalidEvent(event)) {
          recoveryProofStore.clear();
        }
        dispatch(event);
      }
      return event;
    },
    [recoveryProofStore],
  );

  const providerFailure = useCallback(() => {
    setProviderError(t(($) => $.common.access.providerError.body));
  }, [t]);

  function beginRemote(event: AccessFlowEvent): boolean {
    if (!window.navigator.onLine) {
      dispatch({ type: 'NETWORK_OFFLINE' });
      return false;
    }
    dispatch({ type: 'CLEAR_CONDITION' });
    dispatch(event);
    return true;
  }

  useEffect(() => {
    const goOffline = () => dispatch({ type: 'NETWORK_OFFLINE' });
    const goOnline = () => dispatch({ type: 'NETWORK_ONLINE' });

    if (!window.navigator.onLine) {
      goOffline();
    }

    window.addEventListener('offline', goOffline);
    window.addEventListener('online', goOnline);

    return () => {
      window.removeEventListener('offline', goOffline);
      window.removeEventListener('online', goOnline);
    };
  }, []);

  useEffect(() => {
    if (
      recoveryEntryState !== 'validating' ||
      recoveryValidationStarted.current
    ) {
      return;
    }

    const proof = recoveryProofStore.peek();
    if (proof === null) {
      recoveryValidationStarted.current = true;
      queueMicrotask(() => {
        setRecoveryEntryState('none');
        dispatch({ type: 'SERVER_RECOVERY_INVALID_OR_EXPIRED' });
      });
      return;
    }

    recoveryValidationStarted.current = true;
    validateRecoveryMutation.mutate(proof, {
      onSuccess: (result) => {
        if (result.valid) {
          setRecoveryEntryState('none');
          dispatch({ type: 'SERVER_RECOVERY_PROOF_VALID' });
          return;
        }
        recoveryProofStore.clear();
        setRecoveryEntryState('none');
        dispatch({ type: 'SERVER_RECOVERY_INVALID_OR_EXPIRED' });
      },
      onError: (error) => {
        const event = dispatchAuthError(error);
        if (isRecoveryInvalidEvent(event)) {
          setRecoveryEntryState('none');
          return;
        }
        setRecoveryEntryState('error');
      },
    });
  }, [
    dispatchAuthError,
    recoveryEntryState,
    recoveryProofStore,
    validateRecoveryMutation,
  ]);

  useEffect(() => {
    const continuation = continuationQuery.data;
    if (continuation === undefined || continuation.kind === 'none') {
      return;
    }
    setProviderContinuation(continuation);
    setProviderError(null);
  }, [continuationQuery.data]);

  useEffect(() => {
    const provider = requestedProvider(flow);
    if (
      provider === null ||
      providerStart.current !== null ||
      providerMutation.isPending
    ) {
      return;
    }

    providerStart.current = provider;
    setProviderError(null);
    dispatch({ type: 'SERVER_PROVIDER_STARTED', provider });
    providerMutation.mutate(
      {
        provider,
        purpose: 'sign_in',
        returnTarget: 'access',
      },
      {
        onSuccess: (outcome) => {
          providerStart.current = null;
          if (outcome.kind === 'redirected') {
            return;
          }
          const result = outcome.result;
          if (result.outcome === 'authenticated') {
            setProviderContinuation({ kind: 'none' });
            dispatch({ type: 'SERVER_AUTHENTICATED' });
            return;
          }
          if (result.outcome === 'enrollment_required') {
            setProviderContinuation({ kind: 'enrollment', enrollment: result });
            return;
          }
          setProviderContinuation({
            kind: 'link',
            link: {
              external_link_challenge_ref: result.external_link_challenge_ref,
              provider_code: provider,
              expires_at: result.expires_at,
            },
          });
          dispatch({ type: 'SERVER_ACCOUNT_LINK_REQUIRED', provider });
        },
        onError: () => {
          providerStart.current = null;
          providerFailure();
          dispatch({ type: 'SERVER_PROVIDER_FAILED', provider });
        },
      },
    );
  }, [flow, providerFailure, providerMutation]);

  useLayoutEffect(() => {
    if (
      sessionQuery.data?.authenticated === true &&
      flow.screen.id === 'SIGN_IN' &&
      recoveryEntryState === 'none' &&
      recoveryProofStore.peek() === null &&
      providerContinuation.kind === 'none'
    ) {
      dispatch({ type: 'SERVER_AUTHENTICATED' });
      return;
    }

    if (
      sessionQuery.data?.authenticated === false &&
      flow.screen.id === 'AUTHENTICATED_RETURN'
    ) {
      dispatch({ type: 'SERVER_LOGGED_OUT' });
    }
  }, [
    flow.screen.id,
    providerContinuation.kind,
    recoveryEntryState,
    recoveryProofStore,
    sessionQuery.data,
  ]);

  useEffect(() => {
    if (!sessionQuery.error) {
      return;
    }
    dispatchAuthError(sessionQuery.error);
  }, [dispatchAuthError, sessionQuery.error]);

  function retryRecoveryValidation() {
    recoveryValidationStarted.current = false;
    dispatch({ type: 'CLEAR_CONDITION' });
    setRecoveryEntryState('validating');
  }

  function signIn(email: string, password: string) {
    if (signInMutation.isPending || !beginRemote({ type: 'REQUEST_SIGN_IN' })) {
      return;
    }

    signInMutation.mutate(
      { email, password },
      {
        onSuccess: () => dispatch({ type: 'SERVER_AUTHENTICATED' }),
        onError: dispatchAuthError,
      },
    );
  }

  function beginSignup(email: string, password: string) {
    if (
      beginSignupMutation.isPending ||
      !beginRemote({ type: 'REQUEST_SIGN_UP' })
    ) {
      return;
    }

    setSignupRef(null);
    beginSignupMutation.mutate(
      { email, password },
      {
        onSuccess: (result) => {
          setSignupRef(result.signup_ref);
          dispatch({ type: 'SERVER_SIGN_UP_CREATED' });
        },
        onError: dispatchAuthError,
      },
    );
  }

  function verifySignup(code: string) {
    if (verifySignupMutation.isPending) {
      return;
    }
    if (signupRef === null) {
      dispatch({ type: 'SERVER_UNEXPECTED' });
      return;
    }
    if (!beginRemote({ type: 'REQUEST_VERIFY_EMAIL' })) {
      return;
    }

    verifySignupMutation.mutate(
      { signup_ref: signupRef, code },
      {
        onSuccess: (result) => {
          setSignupRef(null);
          if (result.outcome === 'authenticated') {
            dispatch({ type: 'SERVER_EMAIL_VERIFIED' });
          } else {
            dispatch({ type: 'SERVER_SIGN_UP_EXISTING_ACCOUNT' });
          }
        },
        onError: dispatchAuthError,
      },
    );
  }

  function resendSignupVerification() {
    if (resendSignupMutation.isPending) {
      return;
    }
    if (signupRef === null) {
      dispatch({ type: 'SERVER_UNEXPECTED' });
      return;
    }
    if (!beginRemote({ type: 'REQUEST_RESEND_VERIFICATION' })) {
      return;
    }

    resendSignupMutation.mutate(
      { signup_ref: signupRef },
      {
        onSuccess: (result) => {
          setSignupRef(result.signup_ref);
          dispatch({ type: 'SERVER_SIGN_UP_CREATED' });
        },
        onError: dispatchAuthError,
      },
    );
  }

  function requestRecovery(email: string) {
    if (
      recoveryMutation.isPending ||
      !beginRemote({ type: 'REQUEST_RECOVERY', email })
    ) {
      return;
    }

    recoveryMutation.mutate(
      { email },
      {
        onSuccess: () => dispatch({ type: 'SERVER_RECOVERY_SENT', email }),
        onError: dispatchAuthError,
      },
    );
  }

  function resetPassword(newPassword: string) {
    if (resetPasswordMutation.isPending) {
      return;
    }
    const proof = recoveryProofStore.peek();
    if (proof === null) {
      dispatch({ type: 'SERVER_RECOVERY_INVALID_OR_EXPIRED' });
      return;
    }
    if (!beginRemote({ type: 'REQUEST_RESET_PASSWORD' })) {
      return;
    }

    resetPasswordMutation.mutate(
      { ...proof, new_password: newPassword },
      {
        onSuccess: () => {
          recoveryProofStore.clear();
          dispatch({ type: 'SERVER_RESET_SUCCEEDED' });
        },
        onError: dispatchAuthError,
      },
    );
  }

  function reauthenticate(password: string) {
    if (reauthenticateMutation.isPending) {
      return;
    }
    const session = sessionQuery.data;
    if (session?.authenticated !== true) {
      dispatch({ type: 'SERVER_LOGGED_OUT' });
      return;
    }
    if (!beginRemote({ type: 'REQUEST_REAUTH' })) {
      return;
    }

    reauthenticateMutation.mutate(
      { password, csrfToken: session.csrf_token },
      {
        onSuccess: () => dispatch({ type: 'SERVER_REAUTH_SUCCEEDED' }),
        onError: dispatchAuthError,
      },
    );
  }

  function logOut() {
    if (logOutMutation.isPending) {
      return;
    }
    if (!window.navigator.onLine) {
      dispatch({ type: 'NETWORK_OFFLINE' });
      return;
    }

    const session = sessionQuery.data;
    if (session?.authenticated !== true) {
      dispatch({ type: 'SERVER_LOGGED_OUT' });
      return;
    }

    dispatch({ type: 'CLEAR_CONDITION' });
    dispatch({ type: 'REQUEST_LOG_OUT' });
    logOutMutation.mutate(
      { csrfToken: session.csrf_token },
      {
        onSuccess: () => dispatch({ type: 'SERVER_LOGGED_OUT' }),
        onError: dispatchAuthError,
      },
    );
  }

  function setEnrollmentEmail(email: string) {
    setProviderError(null);
    setEnrollmentEmailMutation.mutate(
      { email },
      {
        onSuccess: (enrollment) =>
          setProviderContinuation({ kind: 'enrollment', enrollment }),
        onError: providerFailure,
      },
    );
  }

  function resendEnrollment() {
    setProviderError(null);
    resendEnrollmentMutation.mutate(undefined, {
      onSuccess: (enrollment) =>
        setProviderContinuation({ kind: 'enrollment', enrollment }),
      onError: providerFailure,
    });
  }

  function verifyEnrollment(code: string) {
    setProviderError(null);
    verifyEnrollmentMutation.mutate(
      { code },
      {
        onSuccess: async (result) => {
          if (result.outcome === 'authenticated') {
            setProviderContinuation({ kind: 'none' });
            dispatch({ type: 'SERVER_EMAIL_VERIFIED' });
            return;
          }
          const refreshed = await continuationQuery.refetch();
          if (refreshed.data?.kind === 'link') {
            setProviderContinuation(refreshed.data);
            return;
          }
          providerFailure();
        },
        onError: providerFailure,
      },
    );
  }

  function authenticateLinkWithPassword(email: string, password: string) {
    setProviderError(null);
    signInMutation.mutate(
      { email, password },
      {
        onError: providerFailure,
      },
    );
  }

  function authenticateLinkWithPasskey() {
    setProviderError(null);
    linkPasskeyMutation.mutate(undefined, {
      onError: providerFailure,
    });
  }

  function confirmLink() {
    const session = sessionQuery.data;
    if (session?.authenticated !== true) {
      providerFailure();
      return;
    }
    setProviderError(null);
    confirmLinkMutation.mutate(
      { csrfToken: session.csrf_token },
      {
        onSuccess: () => {
          setProviderContinuation({ kind: 'none' });
          dispatch({ type: 'SERVER_AUTHENTICATED' });
        },
        onError: providerFailure,
      },
    );
  }

  const providerPanelPending =
    setEnrollmentEmailMutation.isPending ||
    resendEnrollmentMutation.isPending ||
    verifyEnrollmentMutation.isPending ||
    confirmLinkMutation.isPending ||
    signInMutation.isPending ||
    linkPasskeyMutation.isPending;

  return (
    <div className="access-shell">
      <header className="access-topbar">
        <div className="access-brand-lockup">
          <img
            className="access-brand-symbol"
            src={danteSymbolUrl}
            alt=""
            aria-hidden="true"
          />
          <img
            className="access-brand-wordmark"
            src={danteWordmarkUrl}
            alt="DANTE"
          />
        </div>

        <AccessLocaleSwitcher />
      </header>

      <main className="access-main">
        <div className="access-frame">
          <AccessBrandStage />
          {providerContinuation.kind === 'none' ? (
            <AccessFlowPanel
              flow={flow}
              dispatch={dispatch}
              recoveryEntryState={recoveryEntryState}
              onRetryRecoveryValidation={retryRecoveryValidation}
              onCredentialSubmit={signIn}
              onSignupSubmit={beginSignup}
              onVerifySubmit={verifySignup}
              onResendVerification={resendSignupVerification}
              onRecoverySubmit={requestRecovery}
              onResetPassword={resetPassword}
              onReauthenticate={reauthenticate}
              onLogOut={logOut}
              pending={{
                signIn: signInMutation.isPending,
                signUp: beginSignupMutation.isPending,
                verify: verifySignupMutation.isPending,
                resend: resendSignupMutation.isPending,
                recovery: recoveryMutation.isPending,
                reset: resetPasswordMutation.isPending,
                reauth: reauthenticateMutation.isPending,
                logOut: logOutMutation.isPending,
              }}
            />
          ) : (
            <AccessProviderFlowPanel
              continuation={providerContinuation}
              authenticated={sessionQuery.data?.authenticated === true}
              errorMessage={providerError}
              pending={providerPanelPending}
              onSetEnrollmentEmail={setEnrollmentEmail}
              onVerifyEnrollment={verifyEnrollment}
              onResendEnrollment={resendEnrollment}
              onAuthenticateExistingAccount={authenticateLinkWithPassword}
              onAuthenticateExistingPasskey={authenticateLinkWithPasskey}
              onConfirmLink={confirmLink}
            />
          )}
        </div>
      </main>
    </div>
  );
}
