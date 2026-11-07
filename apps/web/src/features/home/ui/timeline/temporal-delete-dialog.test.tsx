// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { TemporalDeleteDialog } from './temporal-delete-dialog';

afterEach(cleanup);

describe('Temporal deletion dialog', () => {
  it.each(['attività', 'evento'] as const)(
    'renders %s outside the Inspector with the same date position',
    (subject) => {
      const onCancel = vi.fn();
      const onConfirm = vi.fn();
      render(
        <div data-testid="inspector">
          <TemporalDeleteDialog
            subject={subject}
            itemTitle="Esempio"
            scheduleLabel="Domenica 8 novembre · 21:00–21:30"
            choices={[
              { key: 'instance', label: 'Solo questa istanza', onConfirm },
              { key: 'series', label: 'Tutta la serie', onConfirm },
            ]}
            busy={false}
            onCancel={onCancel}
          />
        </div>,
      );

      const dialog = screen.getByRole('alertdialog', {
        name: `Elimina ${subject}`,
      });
      expect(dialog.parentElement?.parentElement).toBe(document.body);
      expect(within(dialog).getByText('Esempio')).toBeTruthy();
      expect(
        within(dialog).getByText('Domenica 8 novembre · 21:00–21:30'),
      ).toBeTruthy();
      expect(
        within(dialog).getByText('Scegli cosa eliminare. L’operazione è definitiva.'),
      ).toBeTruthy();
      expect(
        within(dialog).getByRole('button', { name: 'Solo questa istanza' }),
      ).toBeTruthy();
      expect(document.activeElement).toBe(
        within(dialog).getByRole('button', { name: 'Annulla' }),
      );
      fireEvent.click(
        within(dialog).getByRole('button', { name: 'Solo questa istanza' }),
      );
      expect(onConfirm).toHaveBeenCalledOnce();
      expect(onCancel).not.toHaveBeenCalled();
    },
  );

  it('cancels with Escape and does not submit a destructive choice', () => {
    const onCancel = vi.fn();
    const onConfirm = vi.fn();
    render(
      <TemporalDeleteDialog
        subject="evento"
        itemTitle="Riunione"
        busy={false}
        choices={[{ key: 'once', label: 'Conferma eliminazione definitiva', onConfirm }]}
        onCancel={onCancel}
      />,
    );
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onCancel).toHaveBeenCalledOnce();
    expect(onConfirm).not.toHaveBeenCalled();
  });

  it('prevents closing while a confirmed deletion is in progress', () => {
    const onCancel = vi.fn();
    const onConfirm = vi.fn();
    render(
      <TemporalDeleteDialog
        subject="attività"
        itemTitle="Allenamento"
        busy
        choices={[{ key: 'once', label: 'Conferma eliminazione definitiva', onConfirm }]}
        onCancel={onCancel}
      />,
    );
    fireEvent.keyDown(window, { key: 'Escape' });
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    fireEvent.click(
      screen.getByRole('button', { name: 'Conferma eliminazione definitiva' }),
    );
    expect(onCancel).not.toHaveBeenCalled();
    expect(onConfirm).not.toHaveBeenCalled();
  });
});
