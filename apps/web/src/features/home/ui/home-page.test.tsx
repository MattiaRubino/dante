import { cleanup, fireEvent, render, screen, within } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import { HomePage } from './home-page';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

describe('HomePage shell foundation', () => {
  it('materializes the approved Home macro-regions with localized semantics', () => {
    const { container } = render(<HomePage />);

    expect(screen.getByRole('main', { name: 'Home DANTE' })).toBeTruthy();

    expect(
      screen.getByRole('navigation', { name: 'Navigazione principale' }),
    ).toBeTruthy();

    expect(
      container.querySelector('[data-home-layout="upper-workspace"]'),
    ).toBeTruthy();

    for (const region of [
      'shell',
      'topbar',
      'day-strip',
      'orientation',
      'ai-surface',
      'central-stage',
      'timeline',
      'context-rail',
    ]) {
      expect(
        container.querySelector(`[data-home-region="${region}"]`),
      ).toBeTruthy();
    }

    expect(screen.getByText('Ora e prossimo')).toBeTruthy();
    expect(screen.getByText('In evidenza')).toBeTruthy();
    expect(screen.getByText('Per te')).toBeTruthy();
    expect(screen.getByText('Cattura')).toBeTruthy();
    expect(screen.getByText('Risoluzione')).toBeTruthy();
  });

  it('keeps unresolved global topbar actions truthful and unavailable', () => {
    render(<HomePage />);

    for (const name of ['Cerca', 'Crea', 'Review', 'Apri launcher', 'Account']) {
      const control = screen.getByRole('button', { name });
      expect((control as HTMLButtonElement).disabled).toBe(true);
    }
  });

  it('supports the contracted local AI and Timeline geometry states', () => {
    const { container } = render(<HomePage />);

    const shell = container.querySelector('[data-home-region="shell"]');
    expect(shell?.getAttribute('data-home-ai-state')).toBe('expanded');
    expect(shell?.getAttribute('data-home-timeline-state')).toBe('normal');

    fireEvent.click(
      screen.getByRole('button', { name: 'Comprimi assistente' }),
    );
    expect(shell?.getAttribute('data-home-ai-state')).toBe('collapsed');
    expect(
      screen.getByRole('button', { name: 'Espandi assistente' }),
    ).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: 'Espandi timeline' }),
    );
    expect(shell?.getAttribute('data-home-timeline-state')).toBe('expanded');
    expect(
      screen.getByRole('button', { name: 'Riduci timeline' }),
    ).toBeTruthy();
  });

  it('keeps the Central Stage read/navigate/open-only at this checkpoint', () => {
    const { container } = render(<HomePage />);

    const stage = container.querySelector(
      '[data-home-region="central-stage"]',
    );

    expect(stage).toBeTruthy();

    const stageScope = within(stage as HTMLElement);

    expect(
      stageScope.getByRole('heading', { level: 2, name: 'Mondi' }),
    ).toBeTruthy();

    expect(stageScope.queryByRole('button')).toBeNull();
    expect(stageScope.queryByRole('textbox')).toBeNull();
    expect(stageScope.queryByText('+')).toBeNull();
  });
});
