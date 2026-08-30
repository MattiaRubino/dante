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

  it('keeps timeline selection separate from focus and exposes focus as an explicit peek action', () => {
    const { container } = renderTimeline();
    const titleButton = screen.getByRole('button', {
      name: 'Redesign LifeOS — sessione focus',
    });
    const card = titleButton.closest<HTMLElement>('[data-timeline-event]');
    expect(card).toBeTruthy();

    fireEvent.click(titleButton);

    expect(
      screen.getByRole('dialog', {
        name: 'Ispezione rapida di Redesign LifeOS — sessione focus',
      }),
    ).toBeTruthy();
    expect(card?.classList.contains('is-selected')).toBe(true);
    expect(card?.classList.contains('is-focused')).toBe(false);
    expect(container.querySelectorAll('.timeline-event-card.is-dim')).toHaveLength(
      0,
    );

    fireEvent.click(screen.getByRole('button', { name: 'Focus' }));

    expect(card?.classList.contains('is-selected')).toBe(true);
    expect(card?.classList.contains('is-focused')).toBe(true);
    expect(
      container.querySelectorAll('.timeline-event-card.is-dim').length,
    ).toBeGreaterThan(0);

    fireEvent.keyDown(document, { key: 'Escape' });

    expect(
      screen.queryByRole('dialog', {
        name: 'Ispezione rapida di Redesign LifeOS — sessione focus',
      }),
    ).toBeNull();
    expect(card?.classList.contains('is-selected')).toBe(false);
    expect(card?.classList.contains('is-focused')).toBe(true);
  });

  it('moves one quick peek between cards and clears selection from empty timeline space', () => {
    const { container } = renderTimeline();
    const focusTitle = screen.getByRole('button', {
      name: 'Redesign LifeOS — sessione focus',
    });
    const focusCard = focusTitle.closest<HTMLElement>('[data-timeline-event]');
    const meetingTitle = screen.getByRole('button', { name: 'Team sync' });
    const meetingCard = meetingTitle.closest<HTMLElement>('[data-timeline-event]');
    expect(focusCard).toBeTruthy();
    expect(meetingCard).toBeTruthy();

    fireEvent.click(focusTitle);
    fireEvent.click(meetingTitle);

    expect(
      screen.queryByRole('dialog', {
        name: 'Ispezione rapida di Redesign LifeOS — sessione focus',
      }),
    ).toBeNull();
    expect(
      screen.getAllByRole('dialog', { name: 'Ispezione rapida di Team sync' }),
    ).toHaveLength(1);
    expect(focusCard?.classList.contains('is-selected')).toBe(false);
    expect(meetingCard?.classList.contains('is-selected')).toBe(true);

    const grid = container.querySelector<HTMLElement>('.timeline-grid');
    expect(grid).toBeTruthy();
    fireEvent.pointerDown(grid as HTMLElement);

    expect(screen.queryByRole('dialog', { name: /Ispezione rapida/ })).toBeNull();
    expect(meetingCard?.classList.contains('is-selected')).toBe(false);
  });

  it('opens the quick peek from keyboard, moves focus into it, restores focus on Escape and hands off to full detail', () => {
    renderTimeline();
    const titleButton = screen.getByRole('button', {
      name: 'Redesign LifeOS — sessione focus',
    });
    const card = titleButton.closest<HTMLElement>('[data-timeline-event]');
    expect(card).toBeTruthy();

    card?.focus();
    fireEvent.keyDown(card as HTMLElement, { key: 'Enter' });
    expect(
      screen.getByRole('dialog', {
        name: 'Ispezione rapida di Redesign LifeOS — sessione focus',
      }),
    ).toBeTruthy();
    expect(document.activeElement).toBe(
      screen.getByRole('button', { name: 'Apri dettagli' }),
    );

    fireEvent.keyDown(document, { key: 'Escape' });
    expect(document.activeElement).toBe(card);

    fireEvent.click(titleButton);
    fireEvent.click(screen.getByRole('button', { name: 'Apri dettagli' }));

    expect(
      screen.queryByRole('dialog', {
        name: 'Ispezione rapida di Redesign LifeOS — sessione focus',
      }),
    ).toBeNull();
    expect(
      screen.getByRole('dialog', {
        name: 'Redesign LifeOS — sessione focus',
      }),
    ).toBeTruthy();
    expect(card?.classList.contains('is-selected')).toBe(true);
  });

  it('hands selection off to the time editor without reopening the quick peek', () => {
    renderTimeline();
    const titleButton = screen.getByRole('button', {
      name: 'Redesign LifeOS — sessione focus',
    });
    const card = titleButton.closest<HTMLElement>('[data-timeline-event]');
    expect(card).toBeTruthy();

    fireEvent.click(titleButton);
    expect(
      screen.getByRole('dialog', {
        name: 'Ispezione rapida di Redesign LifeOS — sessione focus',
      }),
    ).toBeTruthy();

    fireEvent.click(
      screen.getByRole('button', {
        name: 'Modifica orario di Redesign LifeOS — sessione focus',
      }),
    );

    expect(
      screen.queryByRole('dialog', {
        name: 'Ispezione rapida di Redesign LifeOS — sessione focus',
      }),
    ).toBeNull();
    expect(
      screen.getByRole('dialog', { name: 'Modifica orario' }),
    ).toBeTruthy();
    expect(card?.classList.contains('is-selected')).toBe(true);
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

  it('exposes group split as a real semantic expansion command', () => {
    const { onExpandedChange, onExpansionProgress } = renderTimeline();

    fireEvent.click(screen.getByRole('button', { name: 'Separa per gruppi' }));

    expect(onExpandedChange).toHaveBeenCalledWith(true);
    expect(onExpansionProgress).toHaveBeenCalledWith(1);
  });
});
