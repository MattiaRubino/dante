import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
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
import { getWorldFocusWorld } from '../model/world-focus-fixtures';
import { createWorldFocusIdentityDescriptor } from '../model/world-focus-identity';
import {
  clearWorldFocusEntry,
  primeWorldFocusEntry,
} from '../model/world-focus-transition';
import { WorldFocusPage } from './world-focus-page';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
  clearWorldFocusEntry();
});

afterAll(() => {
  vi.restoreAllMocks();
});

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

describe('WorldFocusPage', () => {
  it('keeps WF0/WF-G3 frozen while mounting the integrated adaptive composition and performance-safe peripheral VFX surface', async () => {
    primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: { left: 500, top: 320, width: 118, height: 118 },
    });
    const onClose = vi.fn();

    const { container } = render(
      <WorldFocusPage
        world={requireWorld('music')}
        identity={requireIdentity('music')}
        source="home"
        onClose={onClose}
      />,
    );

    const shell = screen.getByRole('main', { name: 'Mondo Musica' });
    expect(shell.getAttribute('data-world-focus-structure-version')).toBe('1.0.0');
    expect(shell.getAttribute('data-world-focus-geometry-version')).toBe('wf-g3');
    expect(shell.getAttribute('data-world-focus-visual-version')).toBe(
      'wf-v4-candidate',
    );
    expect(shell.getAttribute('data-world-focus-region')).toBe('shell');
    expect(shell.getAttribute('data-entry-origin')).toBe('live');

    expect(
      container.querySelectorAll('[data-world-focus-region="visual-frame"]'),
    ).toHaveLength(1);
    expect(
      container.querySelectorAll('[data-world-focus-region="workspace"]'),
    ).toHaveLength(1);
    expect(
      container.querySelectorAll('[data-world-focus-region="shell-controls"]'),
    ).toHaveLength(1);
    expect(container.querySelectorAll('.world-focus-energy-canvas')).toHaveLength(1);
    expect(
      container.querySelectorAll('.world-focus-corona-reference'),
    ).toHaveLength(3);
    expect(container.querySelector('.world-focus-corona-fallback-svg')).toBeNull();

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
    expect(continuity).not.toBeNull();
    expect(continuity?.getAttribute('data-world-focus-origin')).toBe(
      'application-derived',
    );
    expect(continuity?.getAttribute('data-world-focus-prominence')).toBe('primary');
    expect(continuity?.getAttribute('data-world-focus-footprint')).toBe('standard');
    expect(continuity?.getAttribute('data-world-focus-grid-span')).toBe('6');
    expect(continuity?.getAttribute('data-world-focus-grid-row')).toBe('0');

    const energy = container.querySelector<HTMLElement>(
      '[data-world-focus-energy-renderer]',
    );
    expect(energy).not.toBeNull();
    expect(['webgl2', 'fallback']).toContain(
      energy?.getAttribute('data-world-focus-energy-renderer'),
    );
    expect(['animated', 'reduced', 'static']).toContain(
      energy?.getAttribute('data-world-focus-energy-motion'),
    );
    if (energy?.getAttribute('data-world-focus-energy-renderer') === 'fallback') {
      expect(energy.getAttribute('data-world-focus-energy-motion')).toBe('static');
    }

    expect(
      container.querySelector(
        '[data-world-focus-vfx-coverage="peripheral-outside-workspace"]',
      ),
    ).toBeTruthy();
    expect(
      container.querySelector('[data-world-focus-vfx-boundary="workspace-protected"]'),
    ).toBeTruthy();
    expect(screen.queryByRole('button', { name: 'Torna indietro' })).toBeNull();
    expect(container.querySelector('.world-focus-portal')).toBeNull();
    expect(container.querySelector('.world-focus-entry-effect')).toBeNull();

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalledWith({ preferHistory: true });
  });

  it('falls back safely for a direct route load and supports Escape', () => {
    const onClose = vi.fn();

    const { container } = render(
      <WorldFocusPage
        world={requireWorld('travel')}
        identity={requireIdentity('travel')}
        source="worlds"
        onClose={onClose}
      />,
    );

    const shell = container.querySelector('.world-focus-shell');
    expect(shell?.getAttribute('data-entry-origin')).toBe('fallback');
    expect(shell?.getAttribute('data-world-focus-structure-version')).toBe('1.0.0');
    expect(shell?.getAttribute('data-world-focus-geometry-version')).toBe('wf-g3');
    expect(shell?.getAttribute('data-world-focus-visual-version')).toBe(
      'wf-v4-candidate',
    );

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenCalledWith({ preferHistory: false });
  });

  it('rebinds entry provenance and close policy when the same page instance changes World', () => {
    primeWorldFocusEntry({
      worldId: 'music',
      source: 'home',
      origin: { left: 500, top: 320, width: 118, height: 118 },
    });
    const onClose = vi.fn();

    const { rerender } = render(
      <WorldFocusPage
        world={requireWorld('music')}
        identity={requireIdentity('music')}
        source="home"
        onClose={onClose}
      />,
    );

    expect(
      screen
        .getByRole('main', { name: 'Mondo Musica' })
        .getAttribute('data-entry-origin'),
    ).toBe('live');

    rerender(
      <WorldFocusPage
        world={requireWorld('travel')}
        identity={requireIdentity('travel')}
        source="worlds"
        onClose={onClose}
      />,
    );

    expect(
      screen
        .getByRole('main', { name: 'Mondo Viaggi' })
        .getAttribute('data-entry-origin'),
    ).toBe('fallback');

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(onClose).toHaveBeenLastCalledWith({ preferHistory: false });
  });

  it('renders truthful loading, error and unavailable states inside the workspace', () => {
    const onClose = vi.fn();
    const world = requireWorld('music');
    const identity = requireIdentity('music');
    const { container, rerender } = render(
      <WorldFocusPage
        world={world}
        identity={identity}
        source="worlds"
        status="loading"
        onClose={onClose}
      />,
    );

    const shell = container.querySelector('.world-focus-shell');
    expect(shell?.getAttribute('data-world-focus-status')).toBe('loading');
    expect(screen.getByRole('status').textContent).toBe('Caricamento del Mondo Musica');

    rerender(
      <WorldFocusPage
        world={world}
        identity={identity}
        source="worlds"
        status="error"
        onClose={onClose}
      />,
    );
    expect(shell?.getAttribute('data-world-focus-status')).toBe('error');
    expect(screen.getByRole('alert').textContent).toBe('Impossibile aprire il Mondo Musica');

    rerender(
      <WorldFocusPage
        world={world}
        identity={identity}
        source="worlds"
        status="unavailable"
        onClose={onClose}
      />,
    );
    expect(shell?.getAttribute('data-world-focus-status')).toBe('unavailable');
    expect(screen.getByRole('alert').textContent).toBe('Mondo Musica non disponibile');
  });

  it('restores focus to a still-mounted opener when the focus surface unmounts', async () => {
    const opener = document.createElement('button');
    opener.type = 'button';
    opener.textContent = 'Apri Musica';
    document.body.append(opener);
    opener.focus();

    try {
      const { unmount } = render(
        <WorldFocusPage
          world={requireWorld('music')}
          identity={requireIdentity('music')}
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
