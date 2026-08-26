import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type {
  AccessFlowEvent,
  AccessFlowState,
  AccessScreen,
} from '../model/access-flow';
import { AccessDownstreamPanel } from './access-downstream-panel';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function renderScreen(
  screenState: AccessScreen,
  condition: AccessFlowState['condition'] = { kind: 'idle' },
) {
  const dispatch = vi.fn<(event: AccessFlowEvent) => void>();

  render(
    <AccessDownstreamPanel
      flow={{ screen: screenState, condition }}
      dispatch={dispatch}
    />,
  );

  return dispatch;
}

describe('AccessDownstreamPanel', () => {
  it('validates and normalizes the six-digit email verification code', () => {
    const dispatch = renderScreen({
      id: 'VERIFY_EMAIL',
      email: 'person@example.com',
    });

    const input = screen.getByLabelText<HTMLInputElement>('Codice di verifica');
    expect(input.autocomplete).toBe('one-time-code');
    expect(input.inputMode).toBe('numeric');

    fireEvent.change(input, { target: { value: '12a34b56' } });
    expect(input.value).toBe('123456');

    fireEvent.change(input, { target: { value: '123' } });
    fireEvent.click(
      screen.getByRole('button', { name: 'Verifica e continua' }),
    );

    expect(dispatch).not.toHaveBeenCalledWith({ type: 'REQUEST_VERIFY_EMAIL' });
    expect(screen.getByText('Inserisci il codice a 6 cifre.')).toBeTruthy();
    expect(input.getAttribute('aria-describedby')).toBe(
      'access-verification-code-error',
    );

    fireEvent.change(input, { target: { value: '654321' } });
    fireEvent.click(
      screen.getByRole('button', { name: 'Verifica e continua' }),
    );
    expect(dispatch).toHaveBeenCalledWith({ type: 'REQUEST_VERIFY_EMAIL' });

    fireEvent.click(screen.getByRole('button', { name: 'Invia di nuovo' }));
    expect(dispatch).toHaveBeenCalledWith({
      type: 'REQUEST_RESEND_VERIFICATION',
    });
  });

  it('keeps reset-password errors field-specific and exposes independent visibility controls', () => {
    const dispatch = renderScreen({ id: 'RESET_PASSWORD' });

    const password = screen.getByLabelText<HTMLInputElement>('Nuova password');
    const confirm =
      screen.getByLabelText<HTMLInputElement>('Conferma password');

    fireEvent.click(screen.getByRole('button', { name: 'Aggiorna password' }));
    expect(screen.getByText('Usa almeno 12 caratteri.')).toBeTruthy();
    expect(password.getAttribute('aria-invalid')).toBe('true');
    expect(dispatch).not.toHaveBeenCalled();

    fireEvent.change(password, {
      target: { value: 'correct horse battery staple' },
    });
    fireEvent.change(confirm, {
      target: { value: 'different horse battery staple' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiorna password' }));

    expect(screen.getByText('Le password non coincidono.')).toBeTruthy();
    expect(confirm.getAttribute('aria-invalid')).toBe('true');

    fireEvent.click(
      screen.getByRole('button', { name: 'Mostra password: Nuova password' }),
    );
    expect(password.type).toBe('text');
    expect(confirm.type).toBe('password');

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Mostra password: Conferma password',
      }),
    );
    expect(confirm.type).toBe('text');

    fireEvent.change(confirm, {
      target: { value: 'correct horse battery staple' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Aggiorna password' }));

    expect(dispatch).toHaveBeenCalledWith({ type: 'REQUEST_RESET_PASSWORD' });
  });

  it('does not advance setup-name with an empty preferred name', () => {
    const dispatch = renderScreen({ id: 'SETUP_NAME', preferredName: '' });

    fireEvent.click(screen.getByRole('button', { name: 'Continua' }));
    expect(dispatch).not.toHaveBeenCalled();
    expect(
      screen.getByText('Inserisci il nome con cui vuoi essere chiamato.'),
    ).toBeTruthy();

    fireEvent.change(screen.getByLabelText('Nome preferito'), {
      target: { value: '  Mattia  ' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Continua' }));

    expect(dispatch).toHaveBeenCalledWith({
      type: 'SETUP_NAME_ACCEPTED',
      preferredName: 'Mattia',
    });
  });

  it('validates first-action locally before reaching its backend boundary', () => {
    const dispatch = renderScreen({ id: 'FIRST_ACTION' });

    fireEvent.click(screen.getByRole('button', { name: 'Crea e apri Home' }));
    expect(dispatch).not.toHaveBeenCalled();
    expect(
      screen.getByText('Scrivi cosa vuoi aggiungere prima di continuare.'),
    ).toBeTruthy();

    fireEvent.change(screen.getByLabelText('Cosa vuoi aggiungere?'), {
      target: { value: 'Passeggiata serale' },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Crea e apri Home' }));

    expect(dispatch).toHaveBeenCalledWith({ type: 'REQUEST_FIRST_ACTION' });
  });

  it('keeps provider collision and reauthentication actions explicit', () => {
    const linkDispatch = renderScreen({
      id: 'ACCOUNT_LINK',
      provider: 'google',
      email: 'person@example.com',
    });

    expect(screen.getByText('Google')).toBeTruthy();
    expect(screen.getByText('person@example.com')).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Accedi e collega' }));
    expect(linkDispatch).toHaveBeenCalledWith({ type: 'REQUEST_ACCOUNT_LINK' });

    cleanup();

    const reauthDispatch = renderScreen({ id: 'REAUTH' });
    expect(
      screen.getByRole('heading', {
        name: 'Conferma di nuovo la tua identità',
      }),
    ).toBeTruthy();
    fireEvent.click(screen.getByRole('button', { name: 'Continua' }));
    expect(reauthDispatch).toHaveBeenCalledWith({ type: 'REQUEST_REAUTH' });
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    expect(reauthDispatch).toHaveBeenCalledWith({ type: 'REAUTH_CANCEL' });
  });

  it('keeps completion surfaces free of backend/router implementation copy', () => {
    renderScreen({ id: 'HOME_HANDOFF' });

    expect(screen.getByRole('heading', { name: 'Tutto pronto' })).toBeTruthy();
    expect(screen.queryByText(/backend|router|sessione/i)).toBeNull();
  });
});
