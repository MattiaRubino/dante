import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import {
  initialAccessFlowState,
  type AccessFlowEvent,
  type AccessScreen,
} from '../model/access-flow';
import { AccessFlowPanel } from './access-flow-panel';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => cleanup());

const idlePending = {
  signIn: false,
  signUp: false,
  verify: false,
  resend: false,
  recovery: false,
  reset: false,
  reauth: false,
  logOut: false,
} as const;

function renderPanel(
  screenState: AccessScreen = initialAccessFlowState.screen,
) {
  const dispatch = vi.fn<(event: AccessFlowEvent) => void>();
  const actions = {
    onRetryRecoveryValidation: vi.fn(),
    onCredentialSubmit: vi.fn(),
    onSignupSubmit: vi.fn(),
    onVerifySubmit: vi.fn(),
    onResendVerification: vi.fn(),
    onRecoverySubmit: vi.fn(),
    onResetPassword: vi.fn(),
    onReauthenticate: vi.fn(),
    onLogOut: vi.fn(),
  };

  render(
    <AccessFlowPanel
      flow={{ screen: screenState, condition: { kind: 'idle' } }}
      dispatch={dispatch}
      recoveryEntryState="none"
      pending={idlePending}
      {...actions}
    />,
  );
  return { dispatch, ...actions };
}

describe('AccessFlowPanel M4 wiring surfaces', () => {
  it('passes validated signup credentials to the application boundary', () => {
    const actions = renderPanel({
      id: 'SIGN_UP_PASSWORD',
      email: 'person@example.com',
    });

    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'short' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Crea un account' }));
    expect(actions.onSignupSubmit).not.toHaveBeenCalled();
    expect(screen.getByText('Usa almeno 15 caratteri.')).toBeTruthy();

    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'correct horse battery staple' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Crea un account' }));
    expect(actions.onSignupSubmit).toHaveBeenCalledWith(
      'person@example.com',
      'correct horse battery staple',
    );
  });

  it('normalizes verification input and delegates verify/resend separately', () => {
    const actions = renderPanel({
      id: 'VERIFY_EMAIL',
      email: 'person@example.com',
    });
    const code = screen.getByLabelText<HTMLInputElement>('Codice di verifica');
    fireEvent.change(code, { target: { value: '12a34b56' } });
    expect(code.value).toBe('123456');
    fireEvent.click(screen.getByRole('button', { name: 'Verifica e continua' }));
    expect(actions.onVerifySubmit).toHaveBeenCalledWith('123456');
    fireEvent.click(screen.getByRole('button', { name: 'Invia di nuovo' }));
    expect(actions.onResendVerification).toHaveBeenCalledOnce();
  });

  it('requires fresh password evidence on reauthentication', () => {
    const actions = renderPanel({ id: 'REAUTH' });
    fireEvent.click(screen.getByRole('button', { name: 'Conferma identità' }));
    expect(actions.onReauthenticate).not.toHaveBeenCalled();
    expect(screen.getByText('Inserisci la password.')).toBeTruthy();

    const password = screen.getByLabelText<HTMLInputElement>('Password');
    expect(password.autocomplete).toBe('current-password');
    fireEvent.change(password, { target: { value: 'fresh password evidence' } });
    fireEvent.click(screen.getByRole('button', { name: 'Conferma identità' }));
    expect(actions.onReauthenticate).toHaveBeenCalledWith(
      'fresh password evidence',
    );
  });
});
