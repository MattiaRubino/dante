import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { createWorldFocusIdentityDescriptor } from '../model/world-focus-identity';
import { WorldFocusContext } from './world-focus-context';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

describe('WorldFocusContext', () => {
  it('renders a quiet first-open orientation surface from an explicit descriptor', () => {
    const identity = createWorldFocusIdentityDescriptor({
      id: 'music',
      label: 'Musica',
      description: 'Creatività, ascolto e progetti musicali.',
    });
    const { container } = render(<WorldFocusContext identity={identity} />);

    expect(screen.getByRole('heading', { level: 1 }).textContent).toBe('Musica');
    expect(container.textContent).toContain(
      'Creatività, ascolto e progetti musicali.',
    );
    expect(
      container.querySelector('[data-world-focus-context-id="music"]'),
    ).not.toBeNull();
    expect(container.querySelector('.world-focus-lens')).toBeNull();
    expect(container.querySelector('select')).toBeNull();
  });

  it('renders an unknown future World descriptor without inventing analytical controls', () => {
    const identity = createWorldFocusIdentityDescriptor({
      id: 'future-craft',
      label: 'Craft',
      description: 'Un contesto futuro non presente nel catalogo fixture.',
    });
    const { container } = render(<WorldFocusContext identity={identity} />);

    expect(screen.getByRole('heading', { level: 1 }).textContent).toBe('Craft');
    expect(container.textContent).toContain(
      'Un contesto futuro non presente nel catalogo fixture.',
    );
    expect(container.querySelector('button')).toBeNull();
    expect(container.querySelector('select')).toBeNull();
  });
});
