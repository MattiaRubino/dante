import {
  useCallback,
  useEffect,
  useLayoutEffect,
  useReducer,
  useRef,
  useState,
} from 'react';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';
import type { RecoveryProofStore } from '../../../platform/auth/recovery-proof';
import {
  useBeginSignupMutation,
  useReauthenticateMutation,
  useRequestPasswordRecoveryMutation,
  useResendSignupVerificationMutation,
  useResetPasswordMutation,
  useValidatePasswordRecoveryMutation,
  useVerifySignupMutation,
} from '../application/auth-lifecycle';
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
} from '../model/access-flow';
import { AccessBrandStage } from './access-brand-stage';
import {
  AccessFlowPanel,
  type AccessRecoveryEntryState,
} from './access-flow-panel';
import { AccessLocaleSwitcher } from './access-locale-switcher';
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

export function AccessPage({
  recoveryProofStore,
}: Readonly<{ recoveryProofStore: RecoveryProofStore }>) {
  const sessionQuery = useAuthSessionQuery();
  const [hadRecoveryProofAtMount] = useState(
    () => recoveryProofStore.peek() !== null,
  );
  const [recoveryEntryState, setRecoveryEntryState] =
    useState<AccessRecoveryEntryState>(
      hadRecoveryProofAtMount ? 'validating' : 'none',
    );
  const recoveryValidationStarted = useRef(false);
  const [signupRef, setSignupRef] = useState<string | null>(null);
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
      setRecoveryEntryState('none');
      dispatch({ type: 'SERVER_RECOVERY_INVALID_OR_EXPIRED' });
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

  useLayoutEffect(() => {
    if (
      sessionQuery.data?.authenticated === true &&
      flow.screen.id === 'SIGN_IN' &&
      recoveryEntryState === 'none' &&
      recoveryProofStore.peek() === null
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
    if (
      signInMutation.isPending ||
      !beginRemote({ type: 'REQUEST_SIGN_IN' })
    ) {
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
        </div>
      </main>
    </div>
  );
}
