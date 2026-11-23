// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { VaultMoveConfirmation } from './vault-move-confirmation';

afterEach(cleanup);

describe('Vault Move review inside the Inspector', () => {
  it('moves an unrecorded standalone Event directly, with no additional modal', () => {
    const onConfirm = vi.fn();
    const onCancel = vi.fn();
    render(
      <VaultMoveConfirmation
        subject="evento"
        itemTitle="Riunione"
        busy={false}
        onConfirm={onConfirm}
        onCancel={onCancel}
      />,
    );
    const review = screen.getByRole('region', {
      name: 'Sposta evento in Bozze',
    });
    expect(within(review).getByText('Riunione')).toBeTruthy();
    expect(within(review).queryByRole('note')).toBeNull();
    expect(screen.queryByRole('alertdialog')).toBeNull();
    fireEvent.click(within(review).getByRole('button', { name: 'Annulla' }));
    expect(onCancel).toHaveBeenCalledOnce();
    expect(onConfirm).not.toHaveBeenCalled();
    fireEvent.click(within(review).getByRole('button', {
      name: 'Conferma spostamento in Bozze',
    }));
    expect(onConfirm).toHaveBeenCalledOnce();
    expect(screen.queryByRole('alertdialog')).toBeNull();
  });

  it('requires an additional confirmation when active/recorded Sessions or Objectives will be lost', () => {
    const onConfirm = vi.fn();
    render(
      <VaultMoveConfirmation
        subject="attività"
        itemTitle="Allenamento"
        scheduleLabel="Lunedì 23 novembre · 16:00–16:30"
        recordedSessions={3}
        recordedObjectives={1}
        busy={false}
        onConfirm={onConfirm}
        onCancel={vi.fn()}
      />,
    );
    const review = screen.getByRole('region', {
      name: 'Sposta attività in Bozze',
    });
    expect(review.textContent).toContain('3 Sessioni e 1 risultato di Obiettivi');
    const move = within(review).getByRole('button', {
      name: 'Conferma spostamento in Bozze',
    });
    expect(move.className).toContain('is-destructive');
    fireEvent.click(move);
    expect(onConfirm).not.toHaveBeenCalled();
    const second = screen.getByRole('alertdialog', {
      name: 'Conferma perdita registrazioni',
    });
    expect(within(second).getByText('Allenamento')).toBeTruthy();
    expect(within(second).getByText(/3 Sessioni e 1 risultato di Obiettivi/)).toBeTruthy();
    fireEvent.click(within(second).getByRole('button', { name: 'Annulla' }));
    expect(onConfirm).not.toHaveBeenCalled();
    expect(screen.queryByRole('alertdialog')).toBeNull();
    fireEvent.click(move);
    const final = screen.getByRole('alertdialog', {
      name: 'Conferma perdita registrazioni',
    });
    fireEvent.click(within(final).getByRole('button', {
      name: 'Elimina registrazioni e sposta',
    }));
    expect(onConfirm).toHaveBeenCalledOnce();
  });

  it('requires additional confirmation for an Event with recorded Objectives only', () => {
    const onConfirm = vi.fn();
    render(
      <VaultMoveConfirmation
        subject="evento"
        itemTitle="Evento"
        recordedObjectives={2}
        busy={false}
        onConfirm={onConfirm}
        onCancel={vi.fn()}
      />,
    );
    fireEvent.click(screen.getByRole('button', {
      name: 'Conferma spostamento in Bozze',
    }));
    expect(onConfirm).not.toHaveBeenCalled();
    expect(screen.getByRole('alertdialog', {
      name: 'Conferma perdita registrazioni',
    }).textContent).toContain('2 risultati di Obiettivi');
  });
});
