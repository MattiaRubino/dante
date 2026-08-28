import { describe, expect, it } from 'vitest';

import {
  accessFlowReducer,
  initialAccessFlowState,
  type AccessFlowState,
} from './access-flow';

describe('Access Auth authoritative transitions', () => {
  it('never authenticates from the request intent alone', () => {
    const requested = accessFlowReducer(initialAccessFlowState, {
      type: 'REQUEST_SIGN_IN',
    });

    expect(requested.screen).toEqual({ id: 'SIGN_IN' });
    expect(requested.condition).toEqual({
      kind: 'backend-required',
      operation: 'sign-in',
    });
  });

  it('moves to the authenticated boundary only on the server result', () => {
    const requested = accessFlowReducer(initialAccessFlowState, {
      type: 'REQUEST_SIGN_IN',
    });
    const authenticated = accessFlowReducer(requested, {
      type: 'SERVER_AUTHENTICATED',
    });

    expect(authenticated).toEqual({
      screen: { id: 'AUTHENTICATED_RETURN' },
      condition: { kind: 'idle' },
    });
  });

  it('keeps a failed signin unauthenticated and returns there after logout', () => {
    const invalid = accessFlowReducer(initialAccessFlowState, {
      type: 'SERVER_INVALID_CREDENTIALS',
    });
    expect(invalid.screen).toEqual({ id: 'SIGN_IN' });
    expect(invalid.condition).toEqual({ kind: 'invalid-credentials' });

    const authenticated: AccessFlowState = {
      screen: { id: 'AUTHENTICATED_RETURN' },
      condition: { kind: 'idle' },
    };
    const requestedLogout = accessFlowReducer(authenticated, {
      type: 'REQUEST_LOG_OUT',
    });
    expect(requestedLogout.screen).toEqual({ id: 'AUTHENTICATED_RETURN' });
    expect(requestedLogout.condition).toEqual({
      kind: 'backend-required',
      operation: 'log-out',
    });

    expect(
      accessFlowReducer(requestedLogout, { type: 'SERVER_LOGGED_OUT' }),
    ).toEqual(initialAccessFlowState);
  });
});
