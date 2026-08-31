import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import {
  afterAll,
  afterEach,
  beforeAll,
  describe,
  expect,
  it,
  vi,
} from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { writeWorldFocusMotionPreference } from '../model/world-focus-motion-preference';
import {
  clearWorldFocusEntry,
  primeWorldFocusEntry,
} from '../model/world-focus-transition';
import { getWorldFocusWorld } from '../model/world-focus-fixtures';
import { WorldFocusPage } from './world-focus-page';

beforeAll(async () => {
  vi.stubGlobal(
    'matchMedia',
    vi.fn().mockImplementation((query: string) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(),
    })),
  );
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  clearWorldFocusEntry();
  window.localStorage.clear();
});

afterAll(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

function requireWorld(id: 'music' | 'travel') {
  const world = getWorldFocusWorld(id);
  if (world === undefined) {
    throw new Error(`Missing World Focus fixture: ${id}`);
  }
  return world;
}

describe('WorldFocusPage', () => {
  it('uses a live opener handoff for the optional immersive entry and closes through history', () => {
    primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: { left: 500, top: 320, width: 118, height: 118 },
    });
    const onClose = vi.fn();

    const { container } = render(
      <WorldFocusPage
        world={requireWorld('music')}
        source="home"
        onClose={onClose}
      />,
    );

    expect(screen.getByRole('main', { name: 'Mondo Musica' })).toBeTruthy();
    expect(screen.getByRole('heading', { name: 'Musica' })).toBeTruthy();
    expect(
      container
        .querySelector('.world-focus-shell')
        ?.getAttribute('data-entry-origin'),
    ).toBe('live');
    expect(
      container
        .querySelector('.world-focus-shell')
        ?.getAttribute('data-entry-presentation'),
    ).toBe('immersive');
    expect(container.querySelector('.world-focus-anchor')).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Torna indietro' }));
    expect(onClose).toHaveBeenCalledWith({ preferHistory: true });
  });

  it('falls back safely for a direct route load and supports Escape', () => {
    const onClose = vi.fn();

    const { container } = render(
      <WorldFocusPage
        world={requireWorld('travel')}
        source="home"
        onClose={onClose}
      />,
    );

    const shell = container.querySelector('.world-focus-shell');
    expect(shell?.getAttribute('data-entry-origin')).toBe('fallback');
    expect(shell?.getAttribute('data-entry-presentation')).toBe('instant');
    expect(shell?.getAttribute('data-entry-phase')).toBe('end');

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalledWith({ preferHistory: false });
  });

  it('skips the middle effect when the persisted preference is instant', () => {
    writeWorldFocusMotionPreference('instant');
    primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: { left: 500, top: 320, width: 118, height: 118 },
    });

    const { container } = render(
      <WorldFocusPage
        world={requireWorld('music')}
        source="home"
        onClose={vi.fn()}
      />,
    );

    const shell = container.querySelector('.world-focus-shell');
    expect(shell?.getAttribute('data-entry-origin')).toBe('live');
    expect(shell?.getAttribute('data-entry-presentation')).toBe('instant');
    expect(shell?.getAttribute('data-entry-phase')).toBe('end');
    expect(container.querySelector('.world-focus-entry-effect')).toBeNull();
    expect(container.querySelector('.world-focus-anchor')).toBeTruthy();
  });

  it('renders truthful loading, error and unavailable shell states', () => {
    const onClose = vi.fn();
    const world = requireWorld('music');
    const { container, rerender } = render(
      <WorldFocusPage
        world={world}
        source="home"
        status="loading"
        onClose={onClose}
      />,
    );

    const shell = container.querySelector('.world-focus-shell');
    expect(shell?.getAttribute('data-world-focus-status')).toBe('loading');
    expect(screen.getByRole('status').textContent).toBe(
      'Caricamento del Mondo Musica',
    );

    rerender(
      <WorldFocusPage
        world={world}
        source="home"
        status="error"
        onClose={onClose}
      />,
    );
    expect(shell?.getAttribute('data-world-focus-status')).toBe('error');
    expect(screen.getByRole('alert').textContent).toBe(
      'Impossibile aprire il Mondo Musica',
    );

    rerender(
      <WorldFocusPage
        world={world}
        source="home"
        status="unavailable"
        onClose={onClose}
      />,
    );
    expect(shell?.getAttribute('data-world-focus-status')).toBe('unavailable');
    expect(screen.getByRole('alert').textContent).toBe(
      'Mondo Musica non disponibile',
    );
  });

  it('restores focus to the live opener after the focus surface unmounts', async () => {
    const opener = document.createElement('button');
    opener.type = 'button';
    opener.textContent = 'Apri Musica';
    document.body.append(opener);
    opener.focus();

    try {
      const { unmount } = render(
        <WorldFocusPage
          world={requireWorld('music')}
          source="home"
          onClose={vi.fn()}
        />,
      );

      expect(document.activeElement).toBe(
        screen.getByRole('main', { name: 'Mondo Musica' }),
      );

      unmount();
      await Promise.resolve();
      expect(document.activeElement).toBe(opener);
    } finally {
      opener.remove();
    }
  });
});
