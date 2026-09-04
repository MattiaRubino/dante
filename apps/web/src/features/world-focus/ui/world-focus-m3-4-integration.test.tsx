import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { getWorldFocusWorld } from '../model/world-focus-fixtures';
import { createWorldFocusIdentityDescriptor } from '../model/world-focus-identity';
import { WorldFocusPage } from './world-focus-page';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

type TestWorldId = 'music' | 'finance';

function requireWorld(id: TestWorldId) {
  const world = getWorldFocusWorld(id);
  if (world === undefined) {
    throw new Error(`Missing World Focus fixture: ${id}`);
  }
  return world;
}

function identity(id: TestWorldId) {
  return createWorldFocusIdentityDescriptor(
    id === 'music'
      ? { id, label: 'Musica', description: 'Il tuo mondo musicale' }
      : { id, label: 'Finanza', description: 'Il tuo mondo finanziario' },
  );
}

function renderWorld(id: TestWorldId) {
  return render(
    <WorldFocusPage
      world={requireWorld(id)}
      identity={identity(id)}
      source="worlds"
      onClose={vi.fn()}
    />,
  );
}

describe('World Focus M3-4 integrated adaptive composition', () => {
  it('mounts the normal Music World from meaningful M1 opportunities instead of the legacy static Continuity-only plan', async () => {
    const { container } = renderWorld('music');

    await waitFor(() => {
      expect(
        container.querySelector('[data-world-focus-composition-id="situation"]'),
      ).not.toBeNull();
      expect(
        container.querySelector(
          '[data-world-focus-composition-id="attention:music-artwork-attention"]',
        ),
      ).not.toBeNull();
    });

    const composition = container.querySelector<HTMLElement>(
      '.world-focus-composition',
    );
    expect(Number(composition?.dataset.worldFocusCompositionCount ?? '0')).toBeGreaterThan(1);
  });

  it('keeps a truly sparse Finance World sparse instead of mounting the legacy synthetic Continuity candidate', async () => {
    const { container } = renderWorld('finance');

    await waitFor(() => {
      expect(
        container.querySelectorAll('[data-world-focus-composition-id]'),
      ).toHaveLength(0);
    });
  });

  it('reuses the exact accepted Customize config owner in normal composition after Apply', async () => {
    const { container } = renderWorld('music');

    const situationSelector = '[data-world-focus-composition-id="situation"]';
    await waitFor(() => {
      expect(container.querySelector(situationSelector)).not.toBeNull();
    });
    expect(
      container.querySelector(situationSelector)?.getAttribute('data-world-focus-origin'),
    ).toBe('application-derived');

    fireEvent.click(
      screen.getByRole('button', { name: 'Personalizza composizione' }),
    );
    fireEvent.click(
      await screen.findByRole('button', { name: 'Aggiungi Situazione' }),
    );
    fireEvent.click(screen.getByRole('button', { name: 'Applica' }));

    await waitFor(() => {
      expect(
        container.querySelector(situationSelector)?.getAttribute('data-world-focus-origin'),
      ).toBe('user');
    });
  });
});
