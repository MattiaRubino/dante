import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { AccessSignInPanel } from './access-sign-in-panel';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  vi.unstubAllEnvs();
});

type Availability = Readonly<{
  google?: boolean;
  apple?: boolean;
  passkey?: boolean;
}>;

function renderPanel({
  google = true,
  apple = true,
  passkey = true,
}: Availability = {}) {
  vi.stubEnv(
    'VITE_DANTE_GOOGLE_CLIENT_ID',
    google ? 'google-client-id' : '',
  );
  vi.stubEnv('VITE_DANTE_APPLE_ENABLED', apple ? 'true' : 'false');
  vi.stubEnv('VITE_DANTE_PASSKEY_ENABLED', passkey ? 'true' : 'false');

  const handlers = {
    onCreateAccount: vi.fn(),
    onForgotPassword: vi.fn(),
    onCredentialSubmit: vi.fn(),
    onApple: vi.fn(),
    googleCredential: vi.fn(),
    googleError: vi.fn(),
  };
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  render(
    <QueryClientProvider client={queryClient}>
      <AccessSignInPanel
        condition={{ kind: 'idle' }}
        onCreateAccount={handlers.onCreateAccount}
        onForgotPassword={handlers.onForgotPassword}
        onCredentialSubmit={handlers.onCredentialSubmit}
        onApple={handlers.onApple}
        google={{
          clientId: null,
          nonce: null,
          pending: false,
          onCredential: handlers.googleCredential,
          onError: handlers.googleError,
        }}
      />
    </QueryClientProvider>,
  );

  return handlers;
}

describe('AccessSignInPanel', () => {
  it('keeps providers primary and passkey as a distinct secondary authenticator', () => {
    renderPanel();

    expect(
      screen.getByRole('heading', { level: 1, name: 'Accedi a DANTE' })
        .textContent,
    ).toBe('Accedi a DANTE');

    const googleButton = screen.getByRole<HTMLButtonElement>('button', {
      name: 'Continua con Google',
    });
    const appleButton = screen.getByRole('button', {
      name: 'Continua con Apple',
    });
    const passkeyButton = screen.getByRole('button', {
      name: 'Accedi con passkey',
    });

    expect(googleButton.disabled).toBe(true);
    expect(appleButton.getAttribute('data-provider')).toBe('apple');
    expect(passkeyButton.closest('.access-provider-stack')).toBeNull();

    const emailInput = screen.getByLabelText<HTMLInputElement>('Email');
    const passwordInput = screen.getByLabelText<HTMLInputElement>('Password');

    expect(emailInput.autocomplete).toBe('email');
    expect(emailInput.inputMode).toBe('email');
    expect(emailInput.placeholder).toBe('nome@esempio.com');
    expect(passwordInput.autocomplete).toBe('current-password');
    expect(passwordInput.type).toBe('password');

    fireEvent.change(passwordInput, { target: { value: 'secret-value' } });
    fireEvent.click(screen.getByRole('button', { name: 'Mostra password' }));

    expect(passwordInput.type).toBe('text');
    expect(passwordInput.value).toBe('secret-value');
    expect(
      screen
        .getByRole('button', { name: 'Nascondi password' })
        .getAttribute('aria-pressed'),
    ).toBe('true');
  });

  it('wires safe local actions and validates before requesting backend sign-in', () => {
    const handlers = renderPanel();

    fireEvent.click(
      screen.getByRole('button', { name: 'Password dimenticata?' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Crea un account' }));
    fireEvent.click(screen.getByRole('button', { name: 'Continua con Apple' }));

    expect(handlers.onForgotPassword).toHaveBeenCalledTimes(1);
    expect(handlers.onCreateAccount).toHaveBeenCalledTimes(1);
    expect(handlers.onApple).toHaveBeenCalledTimes(1);

    fireEvent.click(screen.getByRole('button', { name: 'Continua' }));
    expect(handlers.onCredentialSubmit).not.toHaveBeenCalled();
    expect(
      screen.getByText('Inserisci un indirizzo email valido.'),
    ).toBeTruthy();
    expect(screen.getByText('Inserisci la password.')).toBeTruthy();

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: 'person@example.com' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'correct horse battery staple' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Continua' }));

    expect(handlers.onCredentialSubmit).toHaveBeenCalledWith(
      'person@example.com',
      'correct horse battery staple',
    );
  });

  it('does not render dead provider or passkey controls when a build disables them', () => {
    renderPanel({ google: false, apple: false, passkey: false });

    expect(
      screen.queryByRole('button', { name: 'Continua con Google' }),
    ).toBeNull();
    expect(
      screen.queryByRole('button', { name: 'Continua con Apple' }),
    ).toBeNull();
    expect(
      screen.queryByRole('button', { name: 'Accedi con passkey' }),
    ).toBeNull();
    expect(screen.getByLabelText('Email')).toBeTruthy();
    expect(screen.getByLabelText('Password')).toBeTruthy();
  });
});
