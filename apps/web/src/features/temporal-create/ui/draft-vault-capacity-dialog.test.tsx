// @vitest-environment jsdom
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { DraftVaultCapacityDialog } from './draft-vault-capacity-dialog';

afterEach(cleanup);

describe('Draft Vault capacity dialog', () => {
  it('shows the limit, stays in the same Create/Inspector and dismisses safely', () => {
    const onDismiss = vi.fn();
    render(
      <>
        <input aria-label="Titolo compilato" defaultValue="Non perdere questo" />
        <DraftVaultCapacityDialog onDismiss={onDismiss} />
      </>,
    );
    const dialog = screen.getByRole('alertdialog', {
      name: 'Spazio Bozze esaurito',
    });
    expect(dialog.textContent).toContain('limite di 100 Bozze');
    expect(screen.getByRole('textbox', { name: 'Titolo compilato' })).toHaveProperty(
      'value',
      'Non perdere questo',
    );
    fireEvent.click(screen.getByRole('button', { name: 'Chiudi' }));
    expect(onDismiss).toHaveBeenCalledOnce();
  });

  it('Escape dismisses the alert without dismissing the underlying form', () => {
    const onDismiss = vi.fn();
    render(<DraftVaultCapacityDialog onDismiss={onDismiss} />);
    fireEvent.keyDown(screen.getByRole('alertdialog'), { key: 'Escape' });
    expect(onDismiss).toHaveBeenCalledOnce();
  });
});
