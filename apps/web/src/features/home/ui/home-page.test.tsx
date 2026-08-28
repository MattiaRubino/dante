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

describe('HomePage M1 visual materialization', () => {
  it('keeps the approved Home ownership regions in the real React tree', () => {
    const { container } = render(<HomePage />);

    expect(screen.getByRole('main', { name: 'Home DANTE' })).toBeTruthy();

    const homeShell = container.querySelector('[data-home-region="shell"]');
    expect(homeShell?.getAttribute('data-home-visual-source')).toBe('b2-v27');

    for (const region of [
      'topbar',
      'day-strip',
      'orientation',
      'ai-surface',
      'central-stage',
      'timeline',
      'context-rail',
    ]) {
      expect(container.querySelector(`[data-home-region="${region}"]`)).toBeTruthy();
    }
  });

  it('materializes the accepted DANTE Home instead of an iframe bridge', () => {
    const { container } = render(<HomePage />);

    expect(container.querySelector('iframe')).toBeNull();
    expect(screen.getByText('Cerca')).toBeTruthy();
    expect(screen.getByText('Crea')).toBeTruthy();
    expect(screen.getByText('Ora e prossimo')).toBeTruthy();
    expect(screen.getByText('In evidenza')).toBeTruthy();
    expect(screen.getByText('Per te')).toBeTruthy();
    expect(screen.getAllByText('Corpo').length).toBeGreaterThan(0);
    expect(screen.getByText('Cattura')).toBeTruthy();
    expect(screen.getByText('Da risolvere')).toBeTruthy();
  });

  it('keeps unresolved backend-dependent controls truthful and unavailable', () => {
    render(<HomePage />);

    for (const name of ['Cerca', 'Crea', 'Review', 'Apri launcher', 'Account']) {
      const control = screen.getByRole('button', { name });
      expect((control as HTMLButtonElement).disabled).toBe(true);
    }
  });

  it('supports the contracted local AI, stage and timeline states', () => {
    const { container } = render(<HomePage />);
    const shell = container.querySelector('[data-home-region="shell"]');

    expect(shell?.getAttribute('data-home-ai-state')).toBe('expanded');
    expect(shell?.getAttribute('data-home-timeline-state')).toBe('normal');

    fireEvent.click(screen.getByRole('button', { name: 'Comprimi assistente' }));
    expect(shell?.getAttribute('data-home-ai-state')).toBe('collapsed');

    const stage = container.querySelector('[data-home-region="central-stage"]');
    const stageScope = within(stage as HTMLElement);
    fireEvent.click(stageScope.getByRole('button', { name: 'Proiezione successiva' }));
    expect(stage?.getAttribute('data-home-stage-mode')).toBe('signals');
    expect(stageScope.getByText('Equilibrio aree')).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Espandi timeline' }));
    expect(shell?.getAttribute('data-home-timeline-state')).toBe('expanded');
  });
});
