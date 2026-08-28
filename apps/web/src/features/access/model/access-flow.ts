export type AccessProvider = 'google' | 'apple';

export type AccessScreen =
  | { id: 'SIGN_IN' }
  | { id: 'SIGN_UP_EMAIL'; email: string }
  | { id: 'SIGN_UP_PASSWORD'; email: string }
  | { id: 'VERIFY_EMAIL'; email: string }
  | { id: 'FORGOT_PASSWORD'; email: string }
  | { id: 'RECOVERY_SENT'; email: string }
  | { id: 'RESET_PASSWORD' }
  | { id: 'RESET_COMPLETE' }
  | { id: 'PROVIDER_PENDING'; provider: AccessProvider }
  | { id: 'PROVIDER_ERROR'; provider: AccessProvider }
  | { id: 'ACCOUNT_LINK'; provider: AccessProvider; email?: string }
  | { id: 'AUTHENTICATED_RETURN' }
  | { id: 'REAUTH' }
  | { id: 'SETUP_NAME'; preferredName: string }
  | { id: 'SETUP_LOCALE' }
  | { id: 'SETUP_START' }
  | { id: 'FIRST_ACTION' }
  | { id: 'IMPORT' }
  | { id: 'DEMO' }
  | { id: 'HOME_HANDOFF' };

export type AccessBackendOperation =
  | 'sign-in'
  | 'log-out'
  | 'provider-google'
  | 'provider-apple'
  | 'sign-up'
  | 'verify-email'
  | 'resend-verification'
  | 'recovery'
  | 'reset-password'
  | 'account-link'
  | 'reauth'
  | 'first-action'
  | 'import';

export type AccessCondition =
  | { kind: 'idle' }
  | { kind: 'backend-required'; operation: AccessBackendOperation }
  | { kind: 'offline' }
  | { kind: 'server-unavailable' }
  | { kind: 'rate-limited'; retryAfterSeconds?: number }
  | { kind: 'invalid-credentials' }
  | { kind: 'account-unavailable' }
  | { kind: 'password-compromised' }
  | { kind: 'request-invalid' }
  | { kind: 'unexpected' };

export type AccessFlowState = Readonly<{
  screen: AccessScreen;
  condition: AccessCondition;
}>;

export type AccessFlowEvent =
  | { type: 'CREATE_ACCOUNT' }
  | { type: 'FORGOT_PASSWORD' }
  | { type: 'BACK_TO_SIGN_IN' }
  | { type: 'SIGN_UP_EMAIL_ACCEPTED'; email: string }
  | { type: 'CHANGE_SIGN_UP_EMAIL' }
  | { type: 'REQUEST_SIGN_IN' }
  | { type: 'REQUEST_LOG_OUT' }
  | { type: 'REQUEST_PROVIDER'; provider: AccessProvider }
  | { type: 'REQUEST_SIGN_UP' }
  | { type: 'REQUEST_VERIFY_EMAIL' }
  | { type: 'REQUEST_RESEND_VERIFICATION' }
  | { type: 'REQUEST_RECOVERY'; email: string }
  | { type: 'REQUEST_RESET_PASSWORD' }
  | { type: 'REQUEST_ACCOUNT_LINK' }
  | { type: 'REQUEST_REAUTH' }
  | { type: 'REQUEST_FIRST_ACTION' }
  | { type: 'REQUEST_IMPORT' }
  | { type: 'CLEAR_CONDITION' }
  | { type: 'NETWORK_OFFLINE' }
  | { type: 'NETWORK_ONLINE' }
  | { type: 'SERVER_UNAVAILABLE' }
  | { type: 'SERVER_RATE_LIMITED'; retryAfterSeconds?: number }
  | { type: 'SERVER_INVALID_CREDENTIALS' }
  | { type: 'SERVER_ACCOUNT_UNAVAILABLE' }
  | { type: 'SERVER_PASSWORD_COMPROMISED' }
  | { type: 'SERVER_REQUEST_INVALID' }
  | { type: 'SERVER_UNEXPECTED' }
  | { type: 'SERVER_PROVIDER_STARTED'; provider: AccessProvider }
  | { type: 'SERVER_PROVIDER_FAILED'; provider: AccessProvider }
  | {
      type: 'SERVER_ACCOUNT_LINK_REQUIRED';
      provider: AccessProvider;
      email?: string;
    }
  | { type: 'SERVER_AUTHENTICATED' }
  | { type: 'SERVER_LOGGED_OUT' }
  | { type: 'SERVER_SIGN_UP_CREATED' }
  | { type: 'SERVER_EMAIL_VERIFIED' }
  | { type: 'SERVER_RECOVERY_SENT'; email: string }
  | { type: 'SERVER_RECOVERY_PROOF_VALID' }
  | { type: 'SERVER_RESET_SUCCEEDED' }
  | { type: 'SERVER_REAUTH_REQUIRED' }
  | { type: 'SERVER_REAUTH_SUCCEEDED' }
  | { type: 'RECOVERY_SENT_CONTINUE' }
  | { type: 'RESET_COMPLETE_CONTINUE' }
  | { type: 'PROVIDER_RETRY' }
  | { type: 'ACCOUNT_LINK_OTHER_ACCOUNT' }
  | { type: 'REAUTH_CANCEL' }
  | { type: 'SETUP_NAME_ACCEPTED'; preferredName: string }
  | { type: 'SETUP_LOCALE_ACCEPTED' }
  | { type: 'SETUP_START_CHOICE'; choice: 'real' | 'import' | 'demo' | 'skip' }
  | { type: 'DEMO_COMPLETE' };

export const initialAccessFlowState: AccessFlowState = {
  screen: { id: 'SIGN_IN' },
  condition: { kind: 'idle' },
};

function withServerScreen(screen: AccessScreen): AccessFlowState {
  return { screen, condition: { kind: 'idle' } };
}

function hasBlockingTransportCondition(condition: AccessCondition): boolean {
  return (
    condition.kind === 'offline' ||
    condition.kind === 'server-unavailable' ||
    condition.kind === 'rate-limited'
  );
}

function moveLocally(
  state: AccessFlowState,
  screen: AccessScreen,
): AccessFlowState {
  return {
    screen,
    condition: hasBlockingTransportCondition(state.condition)
      ? state.condition
      : { kind: 'idle' },
  };
}

function requireBackend(
  state: AccessFlowState,
  operation: AccessBackendOperation,
): AccessFlowState {
  if (hasBlockingTransportCondition(state.condition)) {
    return state;
  }

  return {
    ...state,
    condition: { kind: 'backend-required', operation },
  };
}

export function accessFlowReducer(
  state: AccessFlowState,
  event: AccessFlowEvent,
): AccessFlowState {
  switch (event.type) {
    case 'CREATE_ACCOUNT':
      return moveLocally(state, { id: 'SIGN_UP_EMAIL', email: '' });
    case 'FORGOT_PASSWORD':
      return moveLocally(state, { id: 'FORGOT_PASSWORD', email: '' });
    case 'BACK_TO_SIGN_IN':
    case 'RESET_COMPLETE_CONTINUE':
    case 'RECOVERY_SENT_CONTINUE':
    case 'PROVIDER_RETRY':
    case 'ACCOUNT_LINK_OTHER_ACCOUNT':
    case 'REAUTH_CANCEL':
      return moveLocally(state, { id: 'SIGN_IN' });
    case 'SIGN_UP_EMAIL_ACCEPTED':
      return moveLocally(state, {
        id: 'SIGN_UP_PASSWORD',
        email: event.email,
      });
    case 'CHANGE_SIGN_UP_EMAIL':
      return state.screen.id === 'SIGN_UP_PASSWORD'
        ? moveLocally(state, {
            id: 'SIGN_UP_EMAIL',
            email: state.screen.email,
          })
        : state;
    case 'REQUEST_SIGN_IN':
      return requireBackend(state, 'sign-in');
    case 'REQUEST_LOG_OUT':
      return requireBackend(state, 'log-out');
    case 'REQUEST_PROVIDER':
      return requireBackend(state, `provider-${event.provider}`);
    case 'REQUEST_SIGN_UP':
      return requireBackend(state, 'sign-up');
    case 'REQUEST_VERIFY_EMAIL':
      return requireBackend(state, 'verify-email');
    case 'REQUEST_RESEND_VERIFICATION':
      return requireBackend(state, 'resend-verification');
    case 'REQUEST_RECOVERY': {
      const nextState: AccessFlowState = {
        screen:
          state.screen.id === 'FORGOT_PASSWORD'
            ? { ...state.screen, email: event.email }
            : state.screen,
        condition: state.condition,
      };
      return requireBackend(nextState, 'recovery');
    }
    case 'REQUEST_RESET_PASSWORD':
      return requireBackend(state, 'reset-password');
    case 'REQUEST_ACCOUNT_LINK':
      return requireBackend(state, 'account-link');
    case 'REQUEST_REAUTH':
      return requireBackend(state, 'reauth');
    case 'REQUEST_FIRST_ACTION':
      return requireBackend(state, 'first-action');
    case 'REQUEST_IMPORT':
      return requireBackend(state, 'import');
    case 'CLEAR_CONDITION':
      return { ...state, condition: { kind: 'idle' } };
    case 'NETWORK_ONLINE':
      return state.condition.kind === 'offline'
        ? { ...state, condition: { kind: 'idle' } }
        : state;
    case 'NETWORK_OFFLINE':
      return { ...state, condition: { kind: 'offline' } };
    case 'SERVER_UNAVAILABLE':
      return { ...state, condition: { kind: 'server-unavailable' } };
    case 'SERVER_RATE_LIMITED':
      return {
        ...state,
        condition:
          event.retryAfterSeconds === undefined
            ? { kind: 'rate-limited' }
            : {
                kind: 'rate-limited',
                retryAfterSeconds: event.retryAfterSeconds,
              },
      };
    case 'SERVER_INVALID_CREDENTIALS':
      return { ...state, condition: { kind: 'invalid-credentials' } };
    case 'SERVER_ACCOUNT_UNAVAILABLE':
      return { ...state, condition: { kind: 'account-unavailable' } };
    case 'SERVER_PASSWORD_COMPROMISED':
      return { ...state, condition: { kind: 'password-compromised' } };
    case 'SERVER_REQUEST_INVALID':
      return { ...state, condition: { kind: 'request-invalid' } };
    case 'SERVER_UNEXPECTED':
      return { ...state, condition: { kind: 'unexpected' } };
    case 'SERVER_PROVIDER_STARTED':
      return withServerScreen({
        id: 'PROVIDER_PENDING',
        provider: event.provider,
      });
    case 'SERVER_PROVIDER_FAILED':
      return withServerScreen({
        id: 'PROVIDER_ERROR',
        provider: event.provider,
      });
    case 'SERVER_ACCOUNT_LINK_REQUIRED':
      return withServerScreen(
        event.email === undefined
          ? {
              id: 'ACCOUNT_LINK',
              provider: event.provider,
            }
          : {
              id: 'ACCOUNT_LINK',
              provider: event.provider,
              email: event.email,
            },
      );
    case 'SERVER_AUTHENTICATED':
    case 'SERVER_REAUTH_SUCCEEDED':
      return withServerScreen({ id: 'AUTHENTICATED_RETURN' });
    case 'SERVER_LOGGED_OUT':
      return withServerScreen({ id: 'SIGN_IN' });
    case 'SERVER_SIGN_UP_CREATED':
      return state.screen.id === 'SIGN_UP_PASSWORD'
        ? withServerScreen({ id: 'VERIFY_EMAIL', email: state.screen.email })
        : state;
    case 'SERVER_EMAIL_VERIFIED':
      return withServerScreen({ id: 'SETUP_NAME', preferredName: '' });
    case 'SERVER_RECOVERY_SENT':
      return withServerScreen({ id: 'RECOVERY_SENT', email: event.email });
    case 'SERVER_RECOVERY_PROOF_VALID':
      return withServerScreen({ id: 'RESET_PASSWORD' });
    case 'SERVER_RESET_SUCCEEDED':
      return withServerScreen({ id: 'RESET_COMPLETE' });
    case 'SERVER_REAUTH_REQUIRED':
      return withServerScreen({ id: 'REAUTH' });
    case 'SETUP_NAME_ACCEPTED':
      return moveLocally(state, { id: 'SETUP_LOCALE' });
    case 'SETUP_LOCALE_ACCEPTED':
      return moveLocally(state, { id: 'SETUP_START' });
    case 'SETUP_START_CHOICE':
      if (event.choice === 'real') {
        return moveLocally(state, { id: 'FIRST_ACTION' });
      }
      if (event.choice === 'import') {
        return moveLocally(state, { id: 'IMPORT' });
      }
      if (event.choice === 'demo') {
        return moveLocally(state, { id: 'DEMO' });
      }
      return moveLocally(state, { id: 'HOME_HANDOFF' });
    case 'DEMO_COMPLETE':
      return moveLocally(state, { id: 'HOME_HANDOFF' });
    default:
      return state;
  }
}

export function isValidAccessEmail(value: string): boolean {
  const email = value.trim();
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

export function isValidNewPassword(value: string): boolean {
  return value.length >= 12;
}
