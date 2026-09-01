import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { getWorldFocusWorld } from '../model/world-focus-fixtures';
import { WorldFocusContext } from './world-focus-context';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function requireWorld(id: 'music' | 'travel') {
  const world = getWorldFocusWorld(id);
  if (world === undefined) {
    throw new Error(`Missing World Focus fixture: ${id}`);
  }
  return world;
}

describe('WorldFocusContext', () => {
  it('renders a quiet first-open orientation surface', () => {
    const { container } = render(<WorldFocusContext world={requireWorld('music')} />);

    expect(screen.getByRole('heading', { level: 1 }).textContent).toBe('Musica');
    expect(container.textContent).toContain('Creatività, ascolto e progetti musicali.');
    expect(
      container.querySelector('[data-world-focus-context-id="music"]'),
    ).not.toBeNull();
    expect(container.querySelector('.world-focus-lens')).toBeNull();
    expect(container.querySelector('select')).toBeNull();
  });

  it('does not invent analytical controls for a contrasting World', () => {
    const { container } = render(<WorldFocusContext world={requireWorld('travel')} />);

    expect(screen.getByRole('heading', { level: 1 }).textContent).toBe('Viaggi');
    expect(container.querySelector('button')).toBeNull();
    expect(container.querySelector('select')).toBeNull();
  });
});
