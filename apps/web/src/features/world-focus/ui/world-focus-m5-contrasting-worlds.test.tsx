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
import { readWorldFocusAdaptiveCompositionSnapshot } from '../application/world-focus-adaptive-composition';
import { getWorldFocusWorld } from '../model/world-focus-fixtures';
import { createWorldFocusIdentityDescriptor } from '../model/world-focus-identity';
import { WorldFocusPage } from './world-focus-page';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

function requireWorld(id: 'music' | 'travel') {
  const world = getWorldFocusWorld(id);
  if (world === undefined) {
    throw new Error(`Missing World Focus fixture: ${id}`);
  }
  return world;
}

function requireIdentity(id: 'music' | 'travel') {
  return createWorldFocusIdentityDescriptor(
    id === 'music'
      ? { id, label: 'Musica', description: 'Il tuo mondo musicale' }
      : { id, label: 'Viaggi', description: 'Il tuo mondo dei viaggi' },
  );
}

function readStatuses(snapshot: Awaited<ReturnType<typeof readWorldFocusAdaptiveCompositionSnapshot>>) {
  return Object.freeze({
    situation: snapshot.situation.status,
    continuity: snapshot.continuity.status,
    attention: snapshot.attention.status,
    next: snapshot.next.status,
    comparison: snapshot.comparison.status,
    trajectory: snapshot.trajectory.status,
    evidenceHistory: snapshot.evidenceHistory.status,
  });
}

async function waitForTravelContinuity(container: HTMLElement) {
  await waitFor(() => {
    expect(
      container.querySelector('[data-world-focus-composition-id="continuity"]'),
    ).not.toBeNull();
  });

  const continuity = container.querySelector<HTMLElement>(
    '[data-world-focus-composition-id="continuity"]',
  );
  if (continuity === null) {
    throw new Error('Expected Travel Continuity composition item');
  }
  return continuity;
}

describe('World Focus M5 contrasting complete Worlds falsification', () => {
  it('requires Travel to materialize a truthful four-output shape rather than cloning Music', async () => {
    const [music, travel] = await Promise.all([
      readWorldFocusAdaptiveCompositionSnapshot('music'),
      readWorldFocusAdaptiveCompositionSnapshot('travel'),
    ]);

    expect(music.worldId).toBe('music');
    expect(travel.worldId).toBe('travel');

    expect(readStatuses(music)).toEqual({
      situation: 'ready',
      continuity: 'ready',
      attention: 'ready',
      next: 'ready',
      comparison: 'ready',
      trajectory: 'ready',
      evidenceHistory: 'ready',
    });

    expect(readStatuses(travel)).toEqual({
      situation: 'ready',
      continuity: 'ready',
      attention: 'empty',
      next: 'ready',
      comparison: 'empty',
      trajectory: 'empty',
      evidenceHistory: 'ready',
    });

    expect(
      travel.opportunitySet.opportunities.map((opportunity) => opportunity.instanceId),
    ).toEqual(['situation', 'continuity', 'next', 'evidence-history']);

    const serializedTravel = JSON.stringify(travel);
    expect(serializedTravel).not.toContain('neon-static');
    expect(serializedTravel).not.toContain('music-');
  });

  it('renders Travel through the same real WorldFocusPage with exactly the intended modules', async () => {
    const { container } = render(
      <WorldFocusPage
        world={requireWorld('travel')}
        identity={requireIdentity('travel')}
        source="worlds"
        onClose={vi.fn()}
      />,
    );

    await waitForTravelContinuity(container);

    expect(
      container
        .querySelector('.world-focus-composition')
        ?.getAttribute('data-world-focus-composition-count'),
    ).toBe('4');

    for (const instanceId of [
      'situation',
      'continuity',
      'next',
      'evidence-history',
    ]) {
      expect(
        container.querySelector(
          `[data-world-focus-composition-id="${instanceId}"]`,
        ),
      ).not.toBeNull();
    }

    for (const kind of ['attention', 'comparison', 'trajectory']) {
      expect(
        container.querySelector(`[data-world-focus-module-kind="${kind}"]`),
      ).toBeNull();
    }

    expect(container.textContent).not.toContain('Neon Static');
    expect(container.textContent).not.toContain('Artwork approval');
  });

  it('runs the full contextual DANTE D4-D6 path from Travel Continuity without a World-specific owner', async () => {
    const { container } = render(
      <WorldFocusPage
        world={requireWorld('travel')}
        identity={requireIdentity('travel')}
        source="worlds"
        onClose={vi.fn()}
      />,
    );

    const continuity = await waitForTravelContinuity(container);
    const contextualInvoker = within(continuity).getByRole('button', {
      name: 'Chiedi a DANTE: Continua da qui',
    });
    fireEvent.click(contextualInvoker);

    const composer = screen.getByRole<HTMLTextAreaElement>('textbox', {
      name: 'Scrivi una richiesta per DANTE',
    });
    fireEvent.change(composer, {
      target: {
        value: 'Continua da qui: prepara un prossimo passo per questo viaggio',
      },
    });
    fireEvent.click(screen.getByRole('button', { name: 'Invia richiesta' }));

    await screen.findByText(
      'Modalità locale: richiesta ricevuta. Nessun modello o fonte esterna è stato interrogato.',
    );

    fireEvent.click(screen.getByRole('button', { name: 'Apri come Insight' }));
    await screen.findByRole('dialog', { name: 'Insight contestuale' });

    fireEvent.click(screen.getByRole('button', { name: 'Prepara proposta' }));
    const proposal = await screen.findByRole('dialog', {
      name: 'Proposta contestuale',
    });
    expect(proposal.getAttribute('data-world-focus-dante-surface')).toBe(
      'proposal',
    );

    fireEvent.click(screen.getByRole('button', { name: 'Rivedi conferma' }));
    const confirmation = await screen.findByRole('alertdialog', {
      name: 'Conferma proposta',
    });
    expect(confirmation.getAttribute('data-world-focus-dante-surface')).toBe(
      'confirmation',
    );

    fireEvent.click(screen.getByRole('button', { name: 'Conferma' }));
    const receipt = await screen.findByRole('dialog', {
      name: 'Ricevuta decisione',
    });

    expect(receipt.getAttribute('data-world-focus-dante-decision')).toBe(
      'confirmed',
    );
    expect(receipt.getAttribute('data-world-focus-dante-effect-execution')).toBe(
      'not-executed',
    );
    expect(receipt.textContent).toContain('Nessuna operazione è stata eseguita');
    expect(receipt.textContent).not.toContain('Operazione completata');
  });
});
