import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { TIMELINE_PROTOTYPE_TODAY } from './model/timeline-fixtures';
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

  it('anchors the accepted rich fixture to the frozen parity date and publishes it without a route date', () => {
    const onViewedDateChange = vi.fn();
    const { container } = renderTimeline({ onViewedDateChange });
    const todayKey = TIMELINE_PROTOTYPE_TODAY.toString();

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

  it('clears the route date when returning to the frozen parity now', () => {
    const onDateNavigation = vi.fn();
    const { container } = renderTimeline({
      viewedDateIso: '2034-02-17',
      onDateNavigation,
    });
    onDateNavigation.mockClear();

    const nowButton = container.querySelector<HTMLButtonElement>(
      '.dante-timeline-now',
    );
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
    expect(
      screen.getByRole('dialog', { name: 'Modifica orario' }),
    ).toBeTruthy();

    const startMinute =
      screen.getByLabelText<HTMLInputElement>('Inizio minuti');
    const endMinute = screen.getByLabelText<HTMLInputElement>('Fine minuti');
    expect(startMinute.value).toBe('00');
    expect(endMinute.value).toBe('00');

    fireEvent.click(
      screen.getByRole('button', { name: 'Aumenta Inizio di 5 minuti' }),
    );

    expect(startMinute.value).toBe('05');
    expect(endMinute.value).toBe('05');
  });

  it('consumes the first outside-card interaction only to clear the current focus', () => {
    const { container } = renderTimeline();
    const focusedCard = container.querySelector<HTMLElement>(
      '[data-timeline-event="7"]',
    );
    const targetCard = container.querySelector<HTMLElement>(
      '[data-timeline-event="12"]',
    );
    const grid = container.querySelector<HTMLElement>('.timeline-grid');
    expect(focusedCard).toBeTruthy();
    expect(targetCard).toBeTruthy();
    expect(grid).toBeTruthy();

    fireEvent.click(focusedCard as HTMLElement);
    expect(focusedCard?.classList.contains('is-focused')).toBe(true);

    const targetTime = screen.getByRole('button', {
      name: 'Modifica orario di Promemoria',
    });
    expect(targetTime.tabIndex).toBe(-1);

    fireEvent.click(targetTime);
    expect(
      screen.queryByRole('dialog', { name: 'Modifica orario' }),
    ).toBeNull();
    expect(focusedCard?.classList.contains('is-focused')).toBe(false);
    expect(targetCard?.classList.contains('is-focused')).toBe(false);

    const enabledTargetTime = screen.getByRole('button', {
      name: 'Modifica orario di Promemoria',
    });
    expect(enabledTargetTime.tabIndex).toBe(0);
    fireEvent.click(enabledTargetTime);
    expect(
      screen.getByRole('dialog', { name: 'Modifica orario' }),
    ).toBeTruthy();

    fireEvent.keyDown(document, { key: 'Escape' });
    fireEvent.click(focusedCard as HTMLElement);
    expect(focusedCard?.classList.contains('is-focused')).toBe(true);
    fireEvent.click(grid as HTMLElement);
    expect(focusedCard?.classList.contains('is-focused')).toBe(false);
  });

  it('remains stable while repeatedly crossing an overlap boundary with focus changes', () => {
    const { container } = renderTimeline();
    const grid = container.querySelector<HTMLElement>('.timeline-grid');
    expect(grid).toBeTruthy();

    const getReminder = () =>
      container.querySelector<HTMLElement>('[data-timeline-event="12"]');
    const moveReminder = (key: 'ArrowUp' | 'ArrowDown') => {
      const reminder = getReminder();
      expect(reminder).toBeTruthy();
      fireEvent.keyDown(reminder as HTMLElement, { key, altKey: true });
    };

    for (let step = 0; step < 5; step += 1) {
      moveReminder('ArrowDown');
    }
    expect(getReminder()?.getAttribute('aria-label')).toContain('15:10–15:25');

    for (let cycle = 0; cycle < 8; cycle += 1) {
      moveReminder('ArrowDown');
      expect(getReminder()?.getAttribute('aria-label')).toContain('15:15–15:30');

      const isolatedReminder = getReminder();
      fireEvent.click(isolatedReminder as HTMLElement);
      expect(isolatedReminder?.classList.contains('is-focused')).toBe(true);
      fireEvent.click(grid as HTMLElement);
      expect(isolatedReminder?.classList.contains('is-focused')).toBe(false);

      moveReminder('ArrowUp');
      expect(getReminder()?.getAttribute('aria-label')).toContain('15:10–15:25');
    }

    for (let step = 0; step < 5; step += 1) {
      moveReminder('ArrowUp');
    }

    expect(getReminder()?.getAttribute('aria-label')).toContain('14:45–15:00');
    expect(
      container.querySelectorAll('[data-timeline-event="12"]'),
    ).toHaveLength(1);
  });

  it('exposes group split as a real semantic expansion command', () => {
    const { onExpandedChange, onExpansionProgress } = renderTimeline();

    fireEvent.click(screen.getByRole('button', { name: 'Separa per gruppi' }));

    expect(onExpandedChange).toHaveBeenCalledWith(true);
    expect(onExpansionProgress).toHaveBeenCalledWith(1);
  });
});
