import { cleanup, fireEvent, render, screen } from '@testing-library/react';
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

function requireWorld() {
  const world = getWorldFocusWorld('music');
  if (world === undefined) {
    throw new Error('Missing World Focus music fixture');
  }
  return world;
}

function renderMusicWorld() {
  const onClose = vi.fn();
  const view = render(
    <WorldFocusPage
      world={requireWorld()}
      identity={createWorldFocusIdentityDescriptor({
        id: 'music',
        label: 'Musica',
        description: 'Il tuo mondo musicale',
      })}
      source="worlds"
      onClose={onClose}
    />,
  );
  return { ...view, onClose };
}

describe('World Focus M3-3 manual composition customization', () => {
  it('keeps View mode distinct from Customize mode until explicit invocation', () => {
    const { container } = renderMusicWorld();

    expect(
      screen.getByRole('button', { name: 'Personalizza composizione' }),
    ).toBeVisible();
    expect(
      screen.queryByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeNull();
    expect(
      container.querySelector('[data-world-focus-composition-count]')?.getAttribute(
        'data-world-focus-composition-count',
      ),
    ).toBe('1');
  });

  it('opens an isolated non-modal Customize surface without changing the accepted View composition', () => {
    const { container } = renderMusicWorld();

    fireEvent.click(
      screen.getByRole('button', { name: 'Personalizza composizione' }),
    );

    const dialog = screen.getByRole('dialog', { name: 'Personalizza Musica' });
    expect(dialog).toBeVisible();
    expect(dialog).toHaveAttribute('aria-modal', 'false');
    expect(
      container.querySelector('[data-world-focus-composition-count]')?.getAttribute(
        'data-world-focus-composition-count',
      ),
    ).toBe('1');
  });

  it('exposes explicit Apply and Cancel terminals only after Customize begins', () => {
    renderMusicWorld();

    expect(screen.queryByRole('button', { name: 'Applica' })).toBeNull();
    expect(screen.queryByRole('button', { name: 'Annulla' })).toBeNull();

    fireEvent.click(
      screen.getByRole('button', { name: 'Personalizza composizione' }),
    );

    expect(screen.getByRole('button', { name: 'Applica' })).toBeVisible();
    expect(screen.getByRole('button', { name: 'Annulla' })).toBeVisible();
  });

  it('Cancel closes the draft surface, leaves the World open, and restores focus to the exact invoker', () => {
    const { onClose } = renderMusicWorld();
    const customize = screen.getByRole('button', {
      name: 'Personalizza composizione',
    });

    customize.focus();
    fireEvent.click(customize);
    expect(
      screen.getByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeVisible();

    fireEvent.click(screen.getByRole('button', { name: 'Annulla' }));

    expect(
      screen.queryByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeNull();
    expect(customize).toHaveFocus();
    expect(onClose).not.toHaveBeenCalled();
  });

  it('Escape closes Customize before the World and restores focus to the invoker', () => {
    const { onClose } = renderMusicWorld();
    const customize = screen.getByRole('button', {
      name: 'Personalizza composizione',
    });

    customize.focus();
    fireEvent.click(customize);
    fireEvent.keyDown(document, { key: 'Escape' });

    expect(
      screen.queryByRole('dialog', { name: 'Personalizza Musica' }),
    ).toBeNull();
    expect(customize).toHaveFocus();
    expect(onClose).not.toHaveBeenCalled();
  });
});
