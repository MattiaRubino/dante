import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { AccessSignInPanel } from './access-sign-in-panel';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

describe('AccessSignInPanel', () => {
  it('exposes localized sign-in controls and a working password visibility control', () => {
    render(<AccessSignInPanel />);

    expect(
      screen.getByRole('heading', { level: 1, name: 'Accedi a DANTE' })
        .textContent,
    ).toBe('Accedi a DANTE');

    const googleButton = screen.getByRole('button', {
      name: 'Continua con Google',
    });
    const appleButton = screen.getByRole('button', {
      name: 'Continua con Apple',
    });

    expect(googleButton.getAttribute('data-provider')).toBe('google');
    expect(appleButton.getAttribute('data-provider')).toBe('apple');

    const emailInput = screen.getByLabelText<HTMLInputElement>('Email');
    const passwordInput = screen.getByLabelText<HTMLInputElement>('Password');

    expect(emailInput.autocomplete).toBe('email');
    expect(emailInput.inputMode).toBe('email');
    expect(emailInput.placeholder).toBe('nome@esempio.com');
    expect(passwordInput.autocomplete).toBe('current-password');
    expect(passwordInput.type).toBe('password');

    const showPasswordButton = screen.getByRole('button', {
      name: 'Mostra password',
    });
    fireEvent.click(showPasswordButton);

    expect(passwordInput.type).toBe('text');
    expect(
      screen
        .getByRole('button', { name: 'Nascondi password' })
        .getAttribute('aria-pressed'),
    ).toBe('true');

    expect(
      screen.getByRole('button', { name: 'Password dimenticata?' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Crea un account' }),
    ).toBeTruthy();
  });
});
