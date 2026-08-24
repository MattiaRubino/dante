import { cleanup, render, screen } from '@testing-library/react';
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
  it('exposes the approved sign-in controls with semantic labels', () => {
    render(<AccessSignInPanel />);

    expect(
      screen.getByRole('heading', { level: 2, name: 'Accedi a DANTE' })
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

    const emailInput = screen.getByLabelText('Email') as HTMLInputElement;
    const passwordInput = screen.getByLabelText('Password') as HTMLInputElement;

    expect(emailInput.autocomplete).toBe('email');
    expect(emailInput.inputMode).toBe('email');
    expect(passwordInput.autocomplete).toBe('current-password');
    expect(passwordInput.type).toBe('password');

    expect(
      screen.getByRole('button', { name: 'Password dimenticata?' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Crea un account' }),
    ).toBeTruthy();
  });
});
