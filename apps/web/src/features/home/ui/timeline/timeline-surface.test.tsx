import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { TimelineSurface } from './timeline-surface';

beforeAll(async () => {
  await i18n.changeLanguage('it');
  Object.defineProperty(window, 'innerWidth', {
    configurable: true,
    value: 1440,
    writable: true,
  });
});

afterEach(() => {
  cleanup();
  document.body.innerHTML = '';
});

function renderTimeline() {
  const onExpandedChange = vi.fn();
  const onExpansionProgress = vi.fn();
  const view = render(
    <TimelineSurface
      expanded={false}
      onExpandedChange={onExpandedChange}
      onExpansionProgress={onExpansionProgress}
    />,
  );
  return { ...view, onExpandedChange, onExpansionProgress };
}

describe('TimelineSurface production parity', () => {
  it('renders the bounded multi-day stream with real timeline controls', () => {
    const { container } = renderTimeline();

    expect(
      container.querySelectorAll('[data-timeline-date]').length,
    ).toBeGreaterThanOrEqual(5);
    expect(
      screen.getByRole('button', { name: 'Apri il calendario' }),
    ).toBeTruthy();
    expect(
      screen.getByRole('button', { name: 'Separa per gruppi' }),
    ).toBeTruthy();
    expect(screen.getByRole('button', { name: 'Aumenta zoom' })).toBeTruthy();
    expect(screen.getByText('Redesign LifeOS — sessione focus')).toBeTruthy();
  });

  it('opens the three-level calendar and keeps today distinct from the viewed date', () => {
    renderTimeline();

    fireEvent.click(screen.getByRole('button', { name: 'Apri il calendario' }));
    expect(screen.getByRole('dialog', { name: 'Vai a una data' })).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Scegli il mese' }));
    expect(screen.getByRole('button', { name: "Scegli l'anno" })).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: "Scegli l'anno" }));
    expect(screen.getByText('2016')).toBeTruthy();
    expect(screen.getByText('2027')).toBeTruthy();
  });

  it('filters groups without rebuilding the timeline as fake server state', () => {
    renderTimeline();
    expect(screen.getByText('Team sync')).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', { name: /Focus \/ lavoro profondo/ }),
    );

    expect(screen.queryByText('Team sync')).toBeNull();
    expect(screen.getByText('Redesign LifeOS — sessione focus')).toBeTruthy();
  });

  it('expands event subitems and opens the precise time editor', () => {
    renderTimeline();

    fireEvent.click(
      screen.getByRole('button', { name: '3 sotto-attività · espandi' }),
    );
    expect(screen.getByText('• Rivedi layout Home')).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Modifica orario di Redesign LifeOS — sessione focus',
      }),
    );
    expect(screen.getByRole('dialog', { name: 'Modifica orario' })).toBeTruthy();
    expect(screen.getByLabelText('Inizio ore')).toBeTruthy();
    expect(screen.getByLabelText('Fine minuti')).toBeTruthy();
  });

  it('exposes group split as a real semantic expansion command', () => {
    const { onExpandedChange, onExpansionProgress } = renderTimeline();

    fireEvent.click(screen.getByRole('button', { name: 'Separa per gruppi' }));

    expect(onExpandedChange).toHaveBeenCalledWith(true);
    expect(onExpansionProgress).toHaveBeenCalledWith(1);
  });
});
