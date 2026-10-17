import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { TemporalTimelineRuntimeBoundary } from '../../../temporal/timeline-runtime-boundary';
import { TIMELINE_PROTOTYPE_TODAY } from './model/timeline-fixtures';
import {
  timelineCardTitlePreview,
  timelineDragSnapMinutes,
} from './model/timeline-policy';
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
    <TemporalTimelineRuntimeBoundary mode="test">
      <TimelineSurface
        expanded={false}
        onExpandedChange={onExpandedChange}
        onExpansionProgress={onExpansionProgress}
        viewedDateIso={options.viewedDateIso}
        onViewedDateChange={onViewedDateChange}
        onDateNavigation={onDateNavigation}
      />
    </TemporalTimelineRuntimeBoundary>,
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
  it('uses 15-minute drag slots at both low and high elastic zoom', () => {
    expect(timelineDragSnapMinutes(0.75)).toBe(15);
    expect(timelineDragSnapMinutes(1)).toBe(15);
    expect(timelineDragSnapMinutes(2.1)).toBe(15);
  });


  it('ends long card titles with an ellipsis without splitting a grapheme', () => {
    const title = `${'X'.repeat(71)}👩‍🚀${'Y'.repeat(40)}`;
    expect(timelineCardTitlePreview(title)).toBe(`${'X'.repeat(71)}👩‍🚀…`);
    expect(timelineCardTitlePreview('X'.repeat(72))).toBe('X'.repeat(72));
    expect(timelineCardTitlePreview('Titolo breve')).toBe('Titolo breve');
  });

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

  it('shows an assigned Life Area below the time and keeps it absent when no group is assigned', () => {
    const { container } = renderTimeline();
    const card = container.querySelector<HTMLElement>(
      '[data-timeline-event="7"]',
    );
    const time = card?.querySelector('.timeline-event-card__time');
    const meta = card?.querySelector('.timeline-event-card__meta');
    expect(time).not.toBeNull();
    expect(meta?.textContent).toContain('Focus / lavoro profondo');
    expect(meta?.textContent).toContain('Certificazione B2');
    expect(
      Boolean(
        (time?.compareDocumentPosition(meta as Node) ?? 0) &
          Node.DOCUMENT_POSITION_FOLLOWING,
      ),
    ).toBe(true);
    expect(meta?.textContent).not.toContain('Senza Life Area');
  });

  it('renders non-editable card time and an Event agenda indicator beneath its details', () => {
    const { container } = renderTimeline();
    const card = container.querySelector<HTMLElement>(
      '[data-timeline-event="2"]',
    );
    expect(card?.querySelector('.timeline-event-card__time')?.tagName).toBe(
      'DIV',
    );
    const indicator = card?.querySelector('.timeline-event-card__indicator');
    expect(indicator?.textContent).toBe('Scaletta3');
    expect(
      indicator?.parentElement?.classList.contains(
        'timeline-event-card__indicators',
      ),
    ).toBe(true);
    const dragSurface = card?.querySelector('.timeline-event-card__drag-zone');
    expect(
      Boolean(
        (dragSurface?.compareDocumentPosition(indicator as Node) ?? 0) &
          Node.DOCUMENT_POSITION_FOLLOWING,
      ),
    ).toBe(true);
    expect(card?.querySelector('.timeline-activity-session-card-controls'))
      .toBeNull();
  });

  it('switches between continuous, one-day and seven-column views without changing the frame', () => {
    const { container } = renderTimeline();
    const frame = container.querySelector('.timeline-frame');
    const select = (label: string) => {
      fireEvent.click(
        screen.getByRole('button', { name: 'Scegli vista Timeline' }),
      );
      fireEvent.click(screen.getByRole('menuitemradio', { name: label }));
    };
    select('Giorno');
    expect(container.querySelector('[data-timeline-view="day"]')).toBeTruthy();
    expect(container.querySelectorAll('[data-timeline-date]')).toHaveLength(1);
    select('Settimana');
    expect(
      container.querySelector('.timeline-day-stream.is-week'),
    ).toBeTruthy();
    expect(container.querySelectorAll('[data-timeline-date]')).toHaveLength(7);
    expect(container.querySelector('.timeline-frame')).toBe(frame);
    select('Timeline');
    expect(
      container.querySelectorAll('[data-timeline-date]').length,
    ).toBeGreaterThan(1);
  });

  it('places the current time one third down the viewport after switching views', () => {
    const { container } = renderTimeline();
    const grid = container.querySelector<HTMLElement>('.timeline-grid');
    expect(grid).not.toBeNull();
    const select = (label: string) => {
      fireEvent.click(
        screen.getByRole('button', { name: 'Scegli vista Timeline' }),
      );
      fireEvent.click(screen.getByRole('menuitemradio', { name: label }));
      const now = container.querySelector<HTMLElement>('.timeline-now-line');
      expect(now).not.toBeNull();
      expect(
        Number.parseFloat(now?.style.top ?? '0') - (grid?.scrollTop ?? 0),
      ).toBeCloseTo(80, 0);
    };
    select('Giorno');
    select('Settimana');
  });

  it('stops the zoom controls at their bounds without wrapping', () => {
    renderTimeline();
    const increase = screen.getByRole<HTMLButtonElement>('button', {
      name: 'Aumenta zoom',
    });
    const decrease = screen.getByRole<HTMLButtonElement>('button', {
      name: 'Riduci zoom',
    });
    for (let click = 0; click < 12; click += 1) fireEvent.click(increase);
    expect(increase.disabled).toBe(true);
    fireEvent.click(increase);
    expect(increase.disabled).toBe(true);
    fireEvent.click(decrease);
    expect(increase.disabled).toBe(false);
    for (let click = 0; click < 12; click += 1) fireEvent.click(decrease);
    expect(decrease.disabled).toBe(true);
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

  it('does not scroll back to an unchanged route date after the user scrolls', async () => {
    const onViewedDateChange = vi.fn();
    const { container } = renderTimeline({
      viewedDateIso: TIMELINE_PROTOTYPE_TODAY.toString(),
      onViewedDateChange,
    });
    const grid = container.querySelector<HTMLElement>('.timeline-grid');
    const days = [
      ...container.querySelectorAll<HTMLElement>('[data-timeline-date]'),
    ];
    expect(grid).toBeTruthy();
    expect(days.length).toBeGreaterThan(4);
    Object.defineProperties(grid!, {
      clientHeight: { configurable: true, value: 500 },
      scrollHeight: { configurable: true, value: 100_000 },
    });
    const nextDayTop = days
      .slice(0, 4)
      .reduce((sum, day) => sum + Number.parseFloat(day.style.height), 0);
    grid!.scrollTop = nextDayTop + 100;
    fireEvent.scroll(grid!);
    await new Promise((resolve) => window.setTimeout(resolve, 40));
    expect(grid!.scrollTop).toBe(nextDayTop + 100);
  });

  it('keeps the viewed clock point fixed when a card changes the elastic layout', () => {
    const { container } = renderTimeline();
    fireEvent.click(
      screen.getByRole('button', { name: 'Scegli vista Timeline' }),
    );
    fireEvent.click(screen.getByRole('menuitemradio', { name: 'Giorno' }));
    const grid = container.querySelector<HTMLElement>('.timeline-grid');
    const hour = () =>
      container.querySelectorAll<HTMLElement>(
        `[data-timeline-date="${TIMELINE_PROTOTYPE_TODAY.toString()}"] .timeline-hour-line`,
      )[40];
    expect(grid).not.toBeNull();
    expect(hour()).toBeDefined();
    Object.defineProperty(grid!, 'clientHeight', {
      configurable: true,
      value: 500,
    });
    const before = Number.parseFloat(hour()?.style.top ?? '0');
    grid!.scrollTop = before - 170;
    fireEvent.click(
      screen.getByRole('button', { name: '3 sotto-attività · espandi' }),
    );
    const after = Number.parseFloat(hour()?.style.top ?? '0');
    expect(after).not.toBe(before);
    expect(after - grid!.scrollTop).toBeCloseTo(170, 1);
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

  it('expands Event agenda items while keeping card times read-only', () => {
    const { container } = renderTimeline();

    fireEvent.click(
      screen.getByRole('button', { name: '3 sotto-attività · espandi' }),
    );
    expect(screen.getByText('• Rivedi layout Home')).toBeTruthy();

    const card = container.querySelector<HTMLElement>(
      '[data-timeline-event="2"]',
    );
    const time = card?.querySelector<HTMLElement>('.timeline-event-card__time');
    expect(time?.tagName).toBe('DIV');
    expect(time?.textContent).toContain('09:00–11:00');
    fireEvent.click(time as HTMLElement);
    expect(card?.classList.contains('is-focused')).toBe(true);
    expect(
      screen.queryByRole('dialog', { name: 'Modifica orario' }),
    ).toBeNull();
  });

  it('lets a different card receive a click while another card is focused', () => {
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

    const targetTime = targetCard?.querySelector<HTMLElement>(
      '.timeline-event-card__time',
    );
    expect(targetTime?.tagName).toBe('DIV');
    expect(targetTime?.tabIndex).toBe(-1);

    fireEvent.click(targetTime as HTMLElement);
    expect(
      screen.queryByRole('dialog', { name: 'Modifica orario' }),
    ).toBeNull();
    expect(focusedCard?.classList.contains('is-focused')).toBe(false);
    expect(targetCard?.classList.contains('is-focused')).toBe(true);

    const targetTitle = targetCard?.querySelector<HTMLButtonElement>(
      '.timeline-event-card__title',
    );
    expect(targetTitle).toBeTruthy();
    expect(targetTitle?.tabIndex).toBe(0);
    fireEvent.click(targetTitle as HTMLButtonElement);
    expect(screen.getByRole('dialog')).toBeTruthy();

    fireEvent.keyDown(document, { key: 'Escape' });
    fireEvent.click(focusedCard as HTMLElement);
    expect(focusedCard?.classList.contains('is-focused')).toBe(true);
    fireEvent.click(grid as HTMLElement);
    expect(focusedCard?.classList.contains('is-focused')).toBe(false);
  });

  it('opens a card title directly while a different card is focused', () => {
    const { container } = renderTimeline();
    const focusedCard = container.querySelector<HTMLElement>(
      '[data-timeline-event="7"]',
    );
    const targetTitle = container.querySelector<HTMLButtonElement>(
      '[data-timeline-event="12"] .timeline-event-card__title',
    );
    expect(focusedCard).toBeTruthy();
    expect(targetTitle).toBeTruthy();
    fireEvent.click(focusedCard as HTMLElement);
    expect(focusedCard?.classList.contains('is-focused')).toBe(true);

    fireEvent.click(targetTitle as HTMLButtonElement);
    expect(screen.getByRole('dialog')).toBeTruthy();
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
    // Keyboard placement moves in visible 15-minute slots, independent
    // of focus and elastic Timeline density.
    expect(getReminder()?.getAttribute('aria-label')).toContain('16:00–16:15');

    for (let cycle = 0; cycle < 8; cycle += 1) {
      moveReminder('ArrowDown');
      expect(getReminder()?.getAttribute('aria-label')).toContain(
        '16:15–16:30',
      );

      const isolatedReminder = getReminder();
      fireEvent.click(isolatedReminder as HTMLElement);
      expect(isolatedReminder?.classList.contains('is-focused')).toBe(true);
      fireEvent.click(grid as HTMLElement);
      expect(isolatedReminder?.classList.contains('is-focused')).toBe(false);

      moveReminder('ArrowUp');
      expect(getReminder()?.getAttribute('aria-label')).toContain(
        '16:00–16:15',
      );
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
