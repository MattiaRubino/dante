import { describe, expect, it } from 'vitest';

import {
  accessFlowReducer,
  initialAccessFlowState,
  isValidAccessEmail,
  isValidNewPassword,
} from './access-flow';

describe('accessFlowReducer', () => {
  it('moves through local signup steps without inventing backend success', () => {
    const emailState = accessFlowReducer(initialAccessFlowState, {
      type: 'CREATE_ACCOUNT',
    });
    expect(emailState.screen.id).toBe('SIGN_UP_EMAIL');

    const passwordState = accessFlowReducer(emailState, {
      type: 'SIGN_UP_EMAIL_ACCEPTED',
      email: 'mattia@example.com',
    });
    expect(passwordState.screen).toEqual({
      id: 'SIGN_UP_PASSWORD',
      email: 'mattia@example.com',
    });

    const submitState = accessFlowReducer(passwordState, {
      type: 'REQUEST_SIGN_UP',
    });
    expect(submitState.screen.id).toBe('SIGN_UP_PASSWORD');
    expect(submitState.condition).toEqual({
      kind: 'backend-required',
      operation: 'sign-up',
    });
  });

  it('does not enter provider pending until the backend/provider transaction starts', () => {
    const intentState = accessFlowReducer(initialAccessFlowState, {
      type: 'REQUEST_PROVIDER',
      provider: 'google',
    });

    expect(intentState.screen.id).toBe('SIGN_IN');
    expect(intentState.condition).toEqual({
      kind: 'backend-required',
      operation: 'provider-google',
    });

    const startedState = accessFlowReducer(intentState, {
      type: 'SERVER_PROVIDER_STARTED',
      provider: 'google',
    });
    expect(startedState.screen).toEqual({
      id: 'PROVIDER_PENDING',
      provider: 'google',
    });
  });

  it('keeps recovery neutral until the backend confirms dispatch', () => {
    const forgotState = accessFlowReducer(initialAccessFlowState, {
      type: 'FORGOT_PASSWORD',
    });
    const requestState = accessFlowReducer(forgotState, {
      type: 'REQUEST_RECOVERY',
      email: 'person@example.com',
    });

    expect(requestState.screen).toEqual({
      id: 'FORGOT_PASSWORD',
      email: 'person@example.com',
    });
    expect(requestState.condition).toEqual({
      kind: 'backend-required',
      operation: 'recovery',
    });

    const sentState = accessFlowReducer(requestState, {
      type: 'SERVER_RECOVERY_SENT',
      email: 'person@example.com',
    });
    expect(sentState.screen.id).toBe('RECOVERY_SENT');
  });

  it('materializes authoritative M4 exception outcomes without inventing success', () => {
    const existing = accessFlowReducer(initialAccessFlowState, {
      type: 'SERVER_SIGN_UP_EXISTING_ACCOUNT',
    });
    expect(existing).toEqual({
      screen: { id: 'SIGN_IN' },
      condition: { kind: 'existing-account' },
    });

    const verifyState = {
      screen: { id: 'VERIFY_EMAIL', email: 'person@example.com' } as const,
      condition: { kind: 'idle' } as const,
    };
    expect(
      accessFlowReducer(verifyState, {
        type: 'SERVER_VERIFICATION_INVALID_OR_EXPIRED',
      }).condition,
    ).toEqual({ kind: 'verification-invalid-or-expired' });

    expect(
      accessFlowReducer(initialAccessFlowState, {
        type: 'SERVER_RECOVERY_INVALID_OR_EXPIRED',
      }),
    ).toEqual({
      screen: { id: 'FORGOT_PASSWORD', email: '' },
      condition: { kind: 'recovery-invalid-or-expired' },
    });
  });

  it('preserves offline authority when a transport-dependent action is requested', () => {
    const offlineState = accessFlowReducer(initialAccessFlowState, {
      type: 'NETWORK_OFFLINE',
    });
    const signInRequest = accessFlowReducer(offlineState, {
      type: 'REQUEST_SIGN_IN',
    });

    expect(signInRequest.screen.id).toBe('SIGN_IN');
    expect(signInRequest.condition).toEqual({ kind: 'offline' });
  });

  it('preserves an orthogonal offline condition across local navigation until reconnect', () => {
    const offlineState = accessFlowReducer(initialAccessFlowState, {
      type: 'NETWORK_OFFLINE',
    });
    const emailState = accessFlowReducer(offlineState, {
      type: 'CREATE_ACCOUNT',
    });

    expect(emailState.screen.id).toBe('SIGN_UP_EMAIL');
    expect(emailState.condition).toEqual({ kind: 'offline' });

    const passwordState = accessFlowReducer(emailState, {
      type: 'SIGN_UP_EMAIL_ACCEPTED',
      email: 'person@example.com',
    });
    expect(passwordState.screen.id).toBe('SIGN_UP_PASSWORD');
    expect(passwordState.condition).toEqual({ kind: 'offline' });

    const onlineState = accessFlowReducer(passwordState, {
      type: 'NETWORK_ONLINE',
    });
    expect(onlineState.screen.id).toBe('SIGN_UP_PASSWORD');
    expect(onlineState.condition).toEqual({ kind: 'idle' });
  });

  it('does not clear a server rate limit merely because the browser reports online', () => {
    const limitedState = accessFlowReducer(initialAccessFlowState, {
      type: 'SERVER_RATE_LIMITED',
      retryAfterSeconds: 30,
    });
    const onlineState = accessFlowReducer(limitedState, {
      type: 'NETWORK_ONLINE',
    });

    expect(onlineState.condition).toEqual({
      kind: 'rate-limited',
      retryAfterSeconds: 30,
    });
  });

  it('materializes the approved post-verification setup graph', () => {
    const setupName = accessFlowReducer(initialAccessFlowState, {
      type: 'SERVER_EMAIL_VERIFIED',
    });
    expect(setupName.screen.id).toBe('SETUP_NAME');

    const setupLocale = accessFlowReducer(setupName, {
      type: 'SETUP_NAME_ACCEPTED',
      preferredName: 'Mattia',
    });
    expect(setupLocale.screen.id).toBe('SETUP_LOCALE');

    const setupStart = accessFlowReducer(setupLocale, {
      type: 'SETUP_LOCALE_ACCEPTED',
    });
    expect(setupStart.screen.id).toBe('SETUP_START');

    expect(
      accessFlowReducer(setupStart, {
        type: 'SETUP_START_CHOICE',
        choice: 'demo',
      }).screen.id,
    ).toBe('DEMO');
  });
});

describe('Access local validation', () => {
  it('validates email shape without asserting account existence', () => {
    expect(isValidAccessEmail('person@example.com')).toBe(true);
    expect(isValidAccessEmail(' person@example.com ')).toBe(true);
    expect(isValidAccessEmail('not-an-email')).toBe(false);
  });

  it('enforces the approved 15 Unicode-code-point minimum locally', () => {
    expect(isValidNewPassword('short')).toBe(false);
    expect(isValidNewPassword('a'.repeat(14))).toBe(false);
    expect(isValidNewPassword('a'.repeat(15))).toBe(true);
    expect(isValidNewPassword('😀'.repeat(14))).toBe(false);
    expect(isValidNewPassword('😀'.repeat(15))).toBe(true);
    expect(isValidNewPassword('a'.repeat(80))).toBe(true);
  });
});
