// @vitest-environment jsdom

import { Temporal } from '@dante/time';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import type { TimelineAllDayItem, TimelineGroup } from './model/timeline-types';
import { TimelineAllDayLane } from './timeline-all-day-layer';

vi.mock('../../../temporal/activity-session-card-controls', () => ({
  ActivitySessionCardControls: ({
    activityRef,
  }: {
    activityRef: string;
  }) => (
    <div data-testid="main-controls" data-activity-ref={activityRef}>
      <button type="button" aria-label="Avvia">
        ▶
      </button>
      <button type="button" aria-label="Termina">
        ■
      </button>
    </div>
  ),
}));

vi.mock('../../../temporal/session-subject-controls', () => ({
  SessionSubjectControls: () => (
    <div data-testid="occurrence-controls">
      <button type="button" aria-label="Avvia">
        ▶
      </button>
      <button type="button" aria-label="Termina">
        ■
      </button>
    </div>
  ),
}));

const groups: readonly TimelineGroup[] = [
  { id: 'work', label: 'Lavoro', tone: 'meeting' },
];

const base: TimelineAllDayItem = Object.freeze({
  id: 'event-a',
  startDateKey: '2026-11-22',
  endDateExclusiveKey: '2026-11-23',
  title: 'Riunione annuale',
  groupId: 'work',
  meta: 'Dettaglio non necessario nella barra',
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  cleanup();
});

function renderLane(
  items: readonly TimelineAllDayItem[],
  onOpenItemDetail = vi.fn(),
) {
  render(
    <TimelineAllDayLane
      dateKey="2026-11-22"
      todayKey="2026-11-22"
      items={items}
      groups={groups}
      filters={new Set()}
      onOpenItemDetail={onOpenItemDetail}
    />,
  );
  return onOpenItemDetail;
}

describe('Timeline date-lane one-line contract', () => {
  it('shows two readable rows and overflows the rest without expanding the lane', () => {
    const items = [
      base,
      {
        ...base,
        id: 'event-b',
        title: 'Fiera',
        endDateExclusiveKey: '2026-11-25',
      },
      { ...base, id: 'event-c', title: 'Terza voce' },
    ] satisfies readonly TimelineAllDayItem[];
    const onOpen = renderLane(items);

    const lane = document.querySelector<HTMLElement>('.timeline-all-day-lane');
    expect(lane?.style.height).toBe('150px'); // 34 header + 2 × 42 + 32 for show-more
    expect(lane?.querySelectorAll('.timeline-all-day-lane__items .timeline-all-day-item'))
      .toHaveLength(2);
    const expand = screen.getByRole('button', { name: 'Mostra altri 1' });
    expect(expand.closest('.timeline-all-day-lane__more')).toBeTruthy();
    expect(expand.getAttribute('aria-expanded')).toBe('false');
    expect(lane?.textContent).not.toContain('Dettaglio non necessario');
    expect(lane?.querySelector('.timeline-all-day-item__indicators')).toBeNull();
    expect(lane?.querySelector('.timeline-all-day-item__session-state')).toBeNull();

    fireEvent.click(expand);
    expect(expand.getAttribute('aria-expanded')).toBe('true');
    expect(lane?.querySelectorAll('.timeline-all-day-lane__overflow .timeline-all-day-item'))
      .toHaveLength(1);
    expect(lane?.style.height).toBe('150px');
    expect(screen.getByText('Terza voce')).toBeTruthy();
    const overflowBar = screen.getByRole('button', { name: /Terza voce/ });
    fireEvent.click(overflowBar, { detail: 1, clientX: 450, clientY: 320 });
    expect(onOpen).toHaveBeenLastCalledWith(items[2], overflowBar, {
      clientX: 450,
      clientY: 320,
    });
    const overflow = screen.getByRole('region', { name: 'Altre barre' });
    fireEvent.keyDown(overflow, { key: 'Escape' });
    expect(screen.queryByRole('region', { name: 'Altre barre' })).toBeNull();
    expect(document.activeElement).toBe(
      screen.getByRole('button', { name: 'Mostra altri 1' }),
    );
  });

  it('keeps the show-more list temporary, bounded to one overlay, and closes on outside pointer', () => {
    const items: readonly TimelineAllDayItem[] = [
      base,
      ...Array.from({ length: 20 }, (_, index) => ({
        ...base,
        id: `overflow-${index}`,
        title: `Extra ${index + 1}`,
      })),
    ];
    renderLane(items);
    const lane = document.querySelector<HTMLElement>('.timeline-all-day-lane');
    const expand = screen.getByRole('button', { name: 'Mostra altri 19' });
    expect(lane?.style.height).toBe('150px');
    fireEvent.click(expand);
    expect(screen.getByRole('region', { name: 'Altre barre' })).toBeTruthy();
    expect(
      lane?.querySelectorAll('.timeline-all-day-lane__overflow .timeline-all-day-item'),
    ).toHaveLength(19);
    fireEvent.pointerDown(document.body);
    expect(screen.queryByRole('region', { name: 'Altre barre' })).toBeNull();
    expect(lane?.style.height).toBe('150px');
  });

  it('keeps identity, title and period on one row; no Area/Objective metadata', () => {
    renderLane([base]);
    const bar = document.querySelector<HTMLElement>('.timeline-all-day-item');
    expect(bar?.querySelector('.timeline-all-day-item__title')?.textContent)
      .toBe('Riunione annuale');
    expect(bar?.querySelector('.timeline-all-day-item__meta')?.textContent)
      .toMatch(/22\s+nov/i);
    expect(bar?.textContent).not.toContain('Lavoro');
    expect(bar?.textContent).not.toContain('Dettaglio non necessario');
    expect(bar?.querySelectorAll('.timeline-all-day-item__identity')).toHaveLength(1);
  });

  it('provides the exact pointer coordinate, with a keyboard fallback', () => {
    const onOpen = renderLane([base]);
    const bar = document.querySelector<HTMLButtonElement>('.timeline-all-day-item');
    if (!bar) throw new Error('Date bar missing');

    fireEvent.click(bar, { detail: 1, clientX: 315, clientY: 156 });
    expect(onOpen).toHaveBeenLastCalledWith(base, bar, {
      clientX: 315,
      clientY: 156,
    });
    fireEvent.click(bar, { detail: 0 });
    expect(onOpen).toHaveBeenLastCalledWith(base, bar, undefined);
  });

  it('prioritizes active and paused main Sessions ahead of ordinary overflow rows', () => {
    const runningSession = {
      state: 'running' as const,
      startedAt: '2026-11-22T08:00:00Z',
      endedAt: null,
      activeSeconds: 60,
      evaluatedAt: '2026-11-22T08:01:00Z',
    };
    const running: TimelineAllDayItem = {
      ...base,
      id: 'active',
      title: 'Attiva',
      mainSession: runningSession,
    };
    const paused: TimelineAllDayItem = {
      ...running,
      id: 'paused',
      title: 'In pausa',
      mainSession: { ...runningSession, state: 'paused' },
    };
    renderLane([base, paused, running]);
    const visible = document.querySelectorAll(
      '.timeline-all-day-lane__items .timeline-all-day-item',
    );
    expect(visible).toHaveLength(2);
    expect(visible[0]?.textContent).toContain('Attiva');
    expect(visible[1]?.textContent).toContain('In pausa');
    fireEvent.click(screen.getByRole('button', { name: 'Mostra altri 1' }));
    expect(document.querySelector('.timeline-all-day-lane__overflow')?.textContent)
      .toContain('Riunione annuale');
  });

  it('preserves exactly two main live controls without showing the timer', () => {
    const item: TimelineAllDayItem = {
      ...base,
      id: 'activity-a',
      title: 'Allenamento',
      canonicalBasis: {
        kind: 'scheduled-activity',
        activityRef: 'activity-a',
        scheduleRef: 'schedule-a',
        placementMaterialStateRef: 'state-a',
        placement: {
          kind: 'date-span',
          startDate: Temporal.PlainDate.from('2026-11-22'),
          endDateExclusive: Temporal.PlainDate.from('2026-11-23'),
        },
      },
      mainSession: {
        state: 'running',
        startedAt: '2026-11-22T08:00:00Z',
        endedAt: null,
        activeSeconds: 123,
        evaluatedAt: '2026-11-22T08:02:03Z',
      },
    };
    const openInspector = renderLane([item]);
    const controls = screen.getByTestId('main-controls');
    expect(controls.querySelectorAll('button')).toHaveLength(2);
    expect(controls.getAttribute('data-activity-ref')).toBe('activity-a');
    const row = controls.closest('.timeline-all-day-item-row');
    expect(row).toBeTruthy();
    expect(row?.contains(document.querySelector('.timeline-all-day-item'))).toBe(true);
    expect(row?.querySelectorAll('button')).toHaveLength(3); // detail + two main controls
    fireEvent.click(screen.getByRole('button', { name: 'Avvia' }));
    expect(openInspector).not.toHaveBeenCalled();
    expect(document.querySelector('.timeline-all-day-lane__more')).toBeNull();
    const lane = document.querySelector('.timeline-all-day-lane');
    expect(lane?.textContent).not.toContain('00:02');
    expect(lane?.querySelector('.timeline-all-day-item__session-state')).toBeNull();
  });
});
