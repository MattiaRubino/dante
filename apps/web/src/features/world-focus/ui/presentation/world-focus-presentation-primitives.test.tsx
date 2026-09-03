import { cleanup, render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it } from 'vitest';

import {
  WorldFocusPresentationSection,
  WorldFocusPresentationState,
  WorldFocusPresentationSubsection,
} from './world-focus-presentation-primitives';

afterEach(cleanup);

describe('World Focus M2 presentation primitives', () => {
  it('uses semantic section structure and visible state text without turning the primitive into a generic card', () => {
    const { container } = render(
      <WorldFocusPresentationSection title="Confronto" qualification="Base aggiornata">
        <WorldFocusPresentationState state="current">Corrente</WorldFocusPresentationState>
        <p>Contenuto</p>
      </WorldFocusPresentationSection>,
    );

    expect(screen.getByRole('heading', { level: 2, name: 'Confronto' })).toBeTruthy();
    expect(screen.getByText('Base aggiornata')).toBeTruthy();
    expect(screen.getByText('Corrente')).toBeTruthy();
    expect(container.querySelector('[data-world-focus-presentation="section"]')).toBeTruthy();
    expect(container.querySelector('.card')).toBeNull();
  });

  it('keeps state meaning in visible text rather than color-only decoration', () => {
    render(
      <WorldFocusPresentationState state="blocked">Bloccato</WorldFocusPresentationState>,
    );

    expect(screen.getByText('Bloccato')).toBeTruthy();
  });

  it('gives nested presentation roles their own accessible group heading', () => {
    render(
      <WorldFocusPresentationSubsection title="Evidenze">
        <p>Revisione mix</p>
      </WorldFocusPresentationSubsection>,
    );

    expect(screen.getByRole('heading', { level: 3, name: 'Evidenze' })).toBeTruthy();
    expect(screen.getByRole('group', { name: 'Evidenze' })).toBeTruthy();
  });
});
