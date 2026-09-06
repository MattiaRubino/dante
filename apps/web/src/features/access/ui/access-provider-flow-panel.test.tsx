import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { AccessProviderFlowPanel } from './access-provider-flow-panel';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function handlers() {
  return {
    onSetEnrollmentEmail: vi.fn(),
    onVerifyEnrollment: vi.fn(),
    onResendEnrollment: vi.fn(),
    onAuthenticateExistingAccount: vi.fn(),
    onAuthenticateExistingPasskey: vi.fn(),
    onConfirmLink: vi.fn(),
  };
}

const linkContinuation = {
  kind: 'link' as const,
  link: {
    external_link_challenge_ref: '00000000-0000-4000-8000-000000000001',
    provider_code: 'google',
    expires_at: '2026-09-02T10:30:00Z',
  } as never,
};

function enrollmentContinuation(
  emailAddress: string | null,
  verificationExpiresAt: string | null,
) {
  return {
    kind: 'enrollment' as const,
    enrollment: {
      email_address: emailAddress,
      verification_expires_at: verificationExpiresAt,
    } as never,
  };
}

describe('AccessProviderFlowPanel', () => {
  it('requires explicit DANTE authentication before an unauthenticated provider link can continue', () => {
    const actions = handlers();
    render(
      <AccessProviderFlowPanel
        continuation={linkContinuation}
        authenticated={false}
        errorMessage={null}
        pending={false}
        {...actions}
      />,
    );

    expect(
      screen.getByRole('heading', { name: 'Conferma il collegamento' }),
    ).toBeTruthy();
    expect(screen.getByText('Google')).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: 'Autentica con password' }),
    );
    expect(actions.onAuthenticateExistingAccount).not.toHaveBeenCalled();
    expect(
      screen.getByText('Inserisci un indirizzo email valido.'),
    ).toBeTruthy();

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: ' person@example.com ' },
    });
    fireEvent.change(screen.getByLabelText('Password'), {
      target: { value: 'correct horse battery staple' },
    });
    fireEvent.click(
      screen.getByRole('button', { name: 'Autentica con password' }),
    );

    expect(actions.onAuthenticateExistingAccount).toHaveBeenCalledWith(
      'person@example.com',
      'correct horse battery staple',
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Autentica con passkey' }),
    );
    expect(actions.onAuthenticateExistingPasskey).toHaveBeenCalledTimes(1);
  });

  it('offers only the explicit link confirmation after the existing account is authenticated', () => {
    const actions = handlers();
    render(
      <AccessProviderFlowPanel
        continuation={linkContinuation}
        authenticated
        errorMessage={null}
        pending={false}
        {...actions}
      />,
    );

    expect(screen.queryByLabelText('Email')).toBeNull();
    expect(screen.queryByLabelText('Password')).toBeNull();

    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma collegamento' }),
    );
    expect(actions.onConfirmLink).toHaveBeenCalledTimes(1);
  });

  it('validates enrollment email locally and submits only the normalized address', () => {
    const actions = handlers();
    render(
      <AccessProviderFlowPanel
        continuation={enrollmentContinuation(null, null)}
        authenticated={false}
        errorMessage={null}
        pending={false}
        {...actions}
      />,
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Invia codice di verifica' }),
    );
    expect(actions.onSetEnrollmentEmail).not.toHaveBeenCalled();
    expect(
      screen.getByText('Inserisci un indirizzo email valido.'),
    ).toBeTruthy();

    fireEvent.change(screen.getByLabelText('Email'), {
      target: { value: ' person@example.com ' },
    });
    fireEvent.click(
      screen.getByRole('button', { name: 'Invia codice di verifica' }),
    );

    expect(actions.onSetEnrollmentEmail).toHaveBeenCalledWith(
      'person@example.com',
    );
  });

  it('sanitizes verification codes and resets local challenge state when authoritative continuation changes', () => {
    const actions = handlers();
    const { rerender } = render(
      <AccessProviderFlowPanel
        continuation={enrollmentContinuation(
          'person@example.com',
          '2026-09-02T10:30:00Z',
        )}
        authenticated={false}
        errorMessage={null}
        pending={false}
        {...actions}
      />,
    );

    const codeInput =
      screen.getByLabelText<HTMLInputElement>('Codice di verifica');
    fireEvent.change(codeInput, { target: { value: '12a34-56' } });
    expect(codeInput.value).toBe('123456');

    fireEvent.click(
      screen.getByRole('button', { name: 'Verifica e continua' }),
    );
    expect(actions.onVerifyEnrollment).toHaveBeenCalledWith('123456');

    fireEvent.click(screen.getByRole('button', { name: 'Invia di nuovo' }));
    expect(actions.onResendEnrollment).toHaveBeenCalledTimes(1);

    rerender(
      <AccessProviderFlowPanel
        continuation={enrollmentContinuation(
          'person@example.com',
          '2026-09-02T10:45:00Z',
        )}
        authenticated={false}
        errorMessage={null}
        pending={false}
        {...actions}
      />,
    );

    expect(
      screen.getByLabelText<HTMLInputElement>('Codice di verifica').value,
    ).toBe('');
  });
});
