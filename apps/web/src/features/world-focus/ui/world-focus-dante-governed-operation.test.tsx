import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
  within,
} from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { getWorldFocusWorld } from '../model/world-focus-fixtures';
import { createWorldFocusIdentityDescriptor } from '../model/world-focus-identity';
import { WorldFocusPage } from './world-focus-page';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

function requireMusicWorld() {
  const world = getWorldFocusWorld('music');
  if (world === undefined) {
    throw new Error('Missing World Focus music fixture');
  }
  return world;
}

async function openContextualInsight(container: HTMLElement) {
  await waitFor(() => {
    expect(
      container
        .querySelector('.world-focus-composition')
        ?.getAttribute('data-world-focus-composition-count'),
    ).toBe('4');
  });

  const continuity = container.querySelector<HTMLElement>(
    '[data-world-focus-composition-id="continuity"]',
  );
  if (continuity === null) {
    throw new Error('Expected Continuity composition item');
  }

  const contextualInvoker = within(continuity).getAllByRole('button', {
    name: 'Chiedi a DANTE: Continua da qui',
  })[0];
  if (contextualInvoker === undefined) {
    throw new Error('Expected contextual DANTE invoker');
  }
  fireEvent.click(contextualInvoker);

  const composer = screen.getByRole<HTMLTextAreaElement>('textbox', {
    name: 'Scrivi una richiesta per DANTE',
  });
  fireEvent.change(composer, {
    target: { value: 'Continua da qui: prepara un prossimo passo governato' },
  });
  fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));
  await screen.findByText(
    'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
  );

  fireEvent.click(screen.getByRole('button', { name: 'Apri come Insight' }));
  return screen.findByRole('dialog', { name: 'Insight contestuale' });
}

describe('World Focus D6 governed-operation presentation', () => {
  it('keeps Proposal, explicit blocking confirmation and local decision receipt distinct without executing an effect', async () => {
    const onClose = vi.fn();
    const { container } = render(
      <WorldFocusPage
        world={requireMusicWorld()}
        identity={createWorldFocusIdentityDescriptor({
          id: 'music',
          label: 'Musica',
          description: 'Il tuo mondo musicale',
        })}
        source="worlds"
        onClose={onClose}
      />,
    );

    await openContextualInsight(container);

    fireEvent.click(screen.getByRole('button', { name: 'Prepara proposta' }));
    const proposal = await screen.findByRole('dialog', {
      name: 'Proposta contestuale',
    });
    expect(proposal.getAttribute('data-world-focus-dante-surface')).toBe(
      'proposal',
    );
    expect(proposal.textContent).toContain('Nessuna operazione è stata eseguita');

    fireEvent.click(screen.getByRole('button', { name: 'Rivedi conferma' }));
    const confirmation = await screen.findByRole('alertdialog', {
      name: 'Conferma proposta',
    });
    expect(confirmation.getAttribute('data-world-focus-dante-surface')).toBe(
      'confirmation',
    );
    const workspace = container.querySelector<HTMLElement>(
      '[data-world-focus-region="workspace"]',
    );
    expect(workspace?.hasAttribute('inert')).toBe(true);

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(
      screen.getByRole('alertdialog', { name: 'Conferma proposta' }),
    ).toBeTruthy();
    expect(onClose).not.toHaveBeenCalled();

    fireEvent.click(screen.getByRole('button', { name: 'Conferma' }));
    const receipt = await screen.findByRole('dialog', {
      name: 'Ricevuta decisione',
    });
    expect(receipt.getAttribute('data-world-focus-dante-surface')).toBe('receipt');
    expect(receipt.getAttribute('data-world-focus-dante-decision')).toBe(
      'confirmed',
    );
    expect(receipt.textContent).toContain('Nessuna operazione è stata eseguita');
    expect(receipt.textContent).not.toContain('Operazione completata');
  });
});
