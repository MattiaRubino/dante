// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { ObjectiveRecordingDeleteDialog } from './objective-recording-delete-dialog';

afterEach(cleanup);

describe('Irreversible Objective recording confirmation', () => {
  it('requires explicit confirmation, keeps the Objective and returns focus', () => {
    const origin = document.createElement('button');
    origin.textContent = 'Apri eliminazione';
    document.body.append(origin);
    origin.focus();
    const onConfirm = vi.fn();
    const onCancel = vi.fn();
    const mounted = render(
      <ObjectiveRecordingDeleteDialog
        objectiveLabel="Mele"
        busy={false}
        onConfirm={onConfirm}
        onCancel={onCancel}
      />,
    );
    const dialog = screen.getByRole('alertdialog', {
      name: 'Eliminare la registrazione?',
    });
    expect(dialog.getAttribute('aria-modal')).toBe('true');
    expect(dialog.parentElement?.parentElement).toBe(document.body);
    expect(within(dialog).getByText(/Mele: il risultato/)).toBeTruthy();
    expect(within(dialog).getByText(/l’obiettivo rimarrà disponibile/i))
      .toBeTruthy();
    const cancel = within(dialog).getByRole('button', { name: 'Annulla' });
    const confirm = within(dialog).getByRole('button', { name: 'Sì, elimina' });
    expect(document.activeElement).toBe(cancel);
    fireEvent.keyDown(window, { key: 'Tab', shiftKey: true });
    expect(document.activeElement).toBe(confirm);
    fireEvent.keyDown(window, { key: 'Tab' });
    expect(document.activeElement).toBe(cancel);
    fireEvent.click(cancel);
    expect(onCancel).toHaveBeenCalledOnce();
    expect(onConfirm).not.toHaveBeenCalled();
    fireEvent.click(confirm);
    expect(onConfirm).toHaveBeenCalledOnce();
    mounted.unmount();
    expect(document.activeElement).toBe(origin);
    origin.remove();
  });

  it('Escape cancels a reversible choice but never invokes destructive confirmation', () => {
    const onCancel = vi.fn();
    const onConfirm = vi.fn();
    render(
      <ObjectiveRecordingDeleteDialog
        objectiveLabel="Allenamento"
        busy={false}
        onConfirm={onConfirm}
        onCancel={onCancel}
      />,
    );
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onCancel).toHaveBeenCalledOnce();
    expect(onConfirm).not.toHaveBeenCalled();
  });

  it('blocks both cancellation and repeated confirmation during an accepted request', () => {
    const onCancel = vi.fn();
    const onConfirm = vi.fn();
    render(
      <ObjectiveRecordingDeleteDialog
        objectiveLabel="Mele"
        busy
        onConfirm={onConfirm}
        onCancel={onCancel}
      />,
    );
    fireEvent.keyDown(window, { key: 'Escape' });
    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));
    fireEvent.click(screen.getByRole('button', { name: 'Eliminazione…' }));
    expect(onCancel).not.toHaveBeenCalled();
    expect(onConfirm).not.toHaveBeenCalled();
    expect(screen.getByRole('button', { name: 'Annulla' }))
      .toHaveProperty('disabled', true);
    expect(screen.getByRole('button', { name: 'Eliminazione…' }))
      .toHaveProperty('disabled', true);
  });
});
