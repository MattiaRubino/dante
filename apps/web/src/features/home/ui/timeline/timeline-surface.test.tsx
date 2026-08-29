import { Temporal } from '@dante/time';
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

type RenderTimelineOptions = Readonly<{
  viewedDateIso?: string | undefined;
  onViewedDateChange?: ((isoDate: string | undefined) => void) | undefined;
  onDateNavigation?: ((isoDate: string | undefined) => void) | undefined;
}>;

function renderTimeline(options: RenderTimelineOptions = {}) {
  const onExpandedChange = vi.fn();
  const onExpansionProgress = vi.fn();
  const onViewedDateChange = options.onViewedDateChange ?? vi.fn();
  const onDateNavigation = options.onDateNavigation ?? vi.fn();
  const view = render(
    <TimelineSurface
      expanded={false}
      onExpandedChange={onExpandedChange}
      onExpansionProgress={onExpansionProgress}
      viewedDateIso={options.viewedDateIso}
      onViewedDateChange={onViewedDateChange}
      onDateNavigation={onDateNavigation}
    />,
  );
  return {
    ...view,
    onExpandedChange,
    onExpansionProgress,
    onViewedDateChange,
    onDateNavigation,
  };
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

  it('anchors the accepted rich fixture to runtime today and publishes today without a route date', () => {
    const onViewedDateChange = vi.fn();
    const { container } = renderTimeline({ onViewedDateChange });
    const todayKey = Temporal.Now.plainDateISO().toString();

    expect(
      container.querySelector(`[data-timeline-date="${todayKey}"]`),
    ).toBeTruthy();
    expect(screen.getByText('Redesign LifeOS — sessione focus')).toBeTruthy();
    expect(onViewedDateChange).toHaveBeenCalledWith(undefined);
  });

  it('opens the three-level calendar and keeps today distinct from the viewed date', () => {
    renderTimeline({ viewedDateIso: '2026-08-04' });

    fireEvent.click(screen.getByRole('button', { name: 'Apri il calendario' }));
    expect(screen.getByRole('dialog', { name: 'Vai a una data' })).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: 'Scegli il mese' }));
    expect(screen.getByRole('button', { name: "Scegli l'anno" })).toBeTruthy();

    fireEvent.click(screen.getByRole('button', { name: "Scegli l'anno" }));
    expect(screen.getByText('2016')).toBeTruthy();
    expect(screen.getByText('2027')).toBeTruthy();
  });

  it('clears the route date when returning to runtime now', () => {
    const onDateNavigation = vi.fn();
    const { container } = renderTimeline({
      viewedDateIso: '2034-02-17',
      onDateNavigation,
    });
    onDateNavigation.mockClear();

    const nowButton = container.querySelector<HTMLButtonElement>('.home-timeline-now');
    expect(nowButton).toBeTruthy();
    fireEvent.click(nowButton as HTMLButtonElement);

    expect(onDateNavigation).toHaveBeenCalledWith(undefined);
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

  it('expands event subitems and exposes precise keyboard, wheel and pointer time controls', () => {
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

    const startMinute = screen.getByLabelText('Inizio minuti');
    const endMinute = screen.getByLabelText('Fine minuti');
    expect(startMinute).toHaveValue('00');
    expect(endMinute).toHaveValue('00');

    fireEvent.click(
      screen.getByRole('button', { name: 'Aumenta Inizio di 5 minuti' }),
    );

    expect(startMinute).toHaveValue('05');
    expect(endMinute).toHaveValue('05');
  });

  it('exposes group split as a real semantic expansion command', () => {
    const { onExpandedChange, onExpansionProgress } = renderTimeline();

    fireEvent.click(screen.getByRole('button', { name: 'Separa per gruppi' }));

    expect(onExpandedChange).toHaveBeenCalledWith(true);
    expect(onExpansionProgress).toHaveBeenCalledWith(1);
  });
});
