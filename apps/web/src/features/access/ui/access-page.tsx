import { useEffect, useReducer } from 'react';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';
import {
  accessEventForAuthError,
  useAuthSessionQuery,
  useLogOutMutation,
  useSignInMutation,
} from '../application/auth-session';
import {
  accessFlowReducer,
  initialAccessFlowState,
} from '../model/access-flow';
import { AccessBrandStage } from './access-brand-stage';
import { AccessFlowPanel } from './access-flow-panel';
import { AccessLocaleSwitcher } from './access-locale-switcher';
import '../access.css';
import '../access-composition.css';
import '../access-flow.css';

export function AccessPage() {
  const [flow, dispatch] = useReducer(
    accessFlowReducer,
    initialAccessFlowState,
  );
  const sessionQuery = useAuthSessionQuery();
  const signInMutation = useSignInMutation();
  const logOutMutation = useLogOutMutation();

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
    if (sessionQuery.data?.authenticated === true) {
      dispatch({ type: 'SERVER_AUTHENTICATED' });
      return;
    }

    if (
      sessionQuery.data?.authenticated === false &&
      flow.screen.id === 'AUTHENTICATED_RETURN'
    ) {
      dispatch({ type: 'SERVER_LOGGED_OUT' });
    }
  }, [flow.screen.id, sessionQuery.data]);

  useEffect(() => {
    if (!sessionQuery.error) {
      return;
    }
    const event = accessEventForAuthError(sessionQuery.error);
    if (event !== null) {
      dispatch(event);
    }
  }, [sessionQuery.error]);

  function signIn(email: string, password: string) {
    if (signInMutation.isPending) {
      return;
    }
    if (!window.navigator.onLine) {
      dispatch({ type: 'NETWORK_OFFLINE' });
      return;
    }

    dispatch({ type: 'CLEAR_CONDITION' });
    dispatch({ type: 'REQUEST_SIGN_IN' });
    signInMutation.mutate(
      { email, password },
      {
        onSuccess: () => dispatch({ type: 'SERVER_AUTHENTICATED' }),
        onError: (error) => {
          const event = accessEventForAuthError(error);
          if (event !== null) {
            dispatch(event);
          }
        },
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
        onError: (error) => {
          const event = accessEventForAuthError(error);
          if (event !== null) {
            dispatch(event);
          }
        },
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
            onCredentialSubmit={signIn}
            onLogOut={logOut}
            signInPending={signInMutation.isPending || sessionQuery.isPending}
            logOutPending={logOutMutation.isPending}
          />
        </div>
      </main>
    </div>
  );
}
