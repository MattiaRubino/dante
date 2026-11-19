// @vitest-environment jsdom
import { Temporal } from '@dante/time';
import { createRef } from 'react';
import { cleanup, fireEvent, render } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../../bootstrap/i18n';
import { TIMELINE_PROTOTYPE_TODAY } from './model/timeline-fixtures';
import { createInitialTimelineState } from './model/timeline-state';
import type { TimelineRenderedDay } from './timeline-day-stream';
import { TimelineDayStream } from './timeline-day-stream';
import { buildTimelineRenderedDays } from './timeline-viewport-runtime';

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(cleanup);

describe('Timeline pointer drag geometry stability', () => {
  it('keeps the original elastic mapper while real-time geometry changes and restores it after drop', () => {
    const state = createInitialTimelineState();
    const original = buildTimelineRenderedDays(TIMELINE_PROTOTYPE_TODAY, 0, 0, {
      eventsByDate: state.eventsByDate,
      groups: state.groups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    });
    const first = original[0];
    expect(first).toBeDefined();
    if (!first) return;

    // A Session tick can produce a large local elastic stretch around now.
    // It must not move the visual mapping mid-gesture.
    const stretched: TimelineRenderedDay = {
      ...first,
      height: first.height * 2,
      mapper: {
        height: first.mapper.height * 2,
        pxPerMinute: first.mapper.pxPerMinute * 2,
        map: (minute) => first.mapper.map(minute) * 2,
        inv: (pixel) => first.mapper.inv(pixel / 2),
      },
      layouts: first.layouts.map((layout) => ({
        ...layout,
        top: layout.top * 2,
        height: layout.height * 2,
      })),
    };

    const gridRef = createRef<HTMLDivElement>();
    const props = {
      view: 'day' as const,
      today: TIMELINE_PROTOTYPE_TODAY,
      state,
      expanded: false,
      gridRef,
      onScroll: vi.fn(),
      onZoomAt: vi.fn(),
      onFocusEvent: vi.fn(),
      onToggleSubitems: vi.fn(),
      onOpenEventDetail: vi.fn(),
      onOpenSubitemDetail: vi.fn(),
      onMoveEvent: vi.fn(),
      onMoveFeedback: vi.fn(),
      onDragActiveChange: vi.fn(),
    };
    const { container, rerender } = render(
      <TimelineDayStream {...props} days={original}
        primaryZoneId="Europe/Rome"
        secondaryZoneIds={['America/New_York']}
        nowMinute={14 * 60 + 20} />,
    );
    expect(container.querySelectorAll('.timeline-ruler-column--secondary')).toHaveLength(1);
    // Every secondary must inherit the EXACT same nonlinear positions as the
    // primary ruler, rather than constructing its own equidistant hour axis.
    const assertAlignedRulers = (day: TimelineRenderedDay) => {
      const primary = container.querySelector<HTMLElement>(
        '.timeline-ruler-column--primary',
      );
      const secondary = Array.from(container.querySelectorAll<HTMLElement>(
        '.timeline-ruler-column--secondary',
      ));
      expect(primary).not.toBeNull();
      const clockTicks = (column: HTMLElement | null) =>
        Array.from(column?.querySelectorAll<HTMLElement>(
          '.timeline-ruler-label',
        ) ?? []).map((label) => Number.parseFloat(label.style.top));
      const mainTicks = clockTicks(primary);
      expect(mainTicks.length).toBeGreaterThanOrEqual(25);
      for (const column of secondary) {
        expect(clockTicks(column)).toEqual(mainTicks);
      }
      // The vertical axis is the original per-day elastic mapper, including
      // the nonuniform extra height introduced by dense/active cards.
      const ticks = Array.from(primary?.querySelectorAll<HTMLElement>(
        '.timeline-ruler-label',
      ) ?? []);
      const positionAt = (minute: number) => day.mapper.map(minute);
      const firstHour = ticks.find((label) => label.textContent === '10:00');
      if (firstHour) {
        expect(Number.parseFloat(firstHour.style.top)).toBeCloseTo(positionAt(600), 5);
      }
    };
    assertAlignedRulers(first);
    const section = () =>
      container.querySelector<HTMLElement>('.timeline-day-section');
    const card = container.querySelector<HTMLElement>(
      '[data-timeline-event="7"]',
    );
    expect(card).not.toBeNull();
    if (!card) return;
    const pointer = {
      pointerId: 3,
      pointerType: 'mouse',
      isPrimary: true,
      button: 0,
      clientX: 140,
      clientY: 120,
    };
    // JSDOM's PointerEvent implementation varies across Node versions.
    // Dispatch with explicit PointerEvent properties so React and the native
    // document listeners receive the same primary mouse pointer identity.
    const pointerEvent = (
      type: string,
      target: Document | HTMLElement,
      clientY: number,
    ) => {
      const event = new MouseEvent(type, {
        bubbles: true,
        cancelable: true,
        button: pointer.button,
        clientX: pointer.clientX,
        clientY,
      });
      Object.defineProperties(event, {
        pointerId: { value: pointer.pointerId },
        pointerType: { value: pointer.pointerType },
        isPrimary: { value: pointer.isPrimary },
      });
      fireEvent(target, event);
    };
    pointerEvent('pointerdown', card, pointer.clientY);
    pointerEvent('pointermove', document, 190);
    expect(
      document.querySelector('.timeline-event-drag-overlay'),
    ).not.toBeNull();
    expect(props.onDragActiveChange).toHaveBeenCalledWith(true);

    rerender(
      <TimelineDayStream
        {...props}
        days={[stretched]}
        primaryZoneId="Europe/Rome"
        secondaryZoneIds={['America/New_York', 'Asia/Tokyo']}
        nowMinute={14 * 60 + 25}
      />,
    );
    expect(container.querySelectorAll('.timeline-ruler-column--secondary')).toHaveLength(2);
    assertAlignedRulers(first);
    expect(container.querySelectorAll('[data-timeline-event="7"]')).toHaveLength(1);
    expect(section()?.style.height).toBe(`${first.height}px`);
    expect(
      container.querySelector('.timeline-ruler-day')?.getAttribute('style'),
    ).toContain(`${first.height}px`);
    expect(
      container.querySelector('.timeline-now-line')?.getAttribute('style'),
    ).toContain(`${first.mapper.map(14 * 60 + 20)}px`);

    pointerEvent('pointerup', document, 190);
    expect(document.querySelector('.timeline-event-drag-overlay')).toBeNull();
    expect(props.onDragActiveChange).toHaveBeenLastCalledWith(false);
    expect(section()?.style.height).toBe(`${stretched.height}px`);
    expect(
      container.querySelector('.timeline-ruler-day')?.getAttribute('style'),
    ).toContain(`${stretched.height}px`);
    assertAlignedRulers(stretched);
  });
});

describe('Timeline rulers at a continuous day boundary', () => {
  it('shows one midnight label in Timeline, no terminal label in Day, and dates only at local midnight', () => {
    const state = createInitialTimelineState();
    const anchor = Temporal.PlainDate.from('2026-11-19');
    const days = buildTimelineRenderedDays(anchor, 0, 1, {
      eventsByDate: state.eventsByDate,
      groups: state.groups,
      zoom: state.zoom,
      expandedEventIds: state.expandedEventIds,
    });
    const first = days[0];
    const next = days[1];
    expect(first).toBeDefined();
    expect(next).toBeDefined();
    if (!first || !next) return;

    const zones = ['Europe/London', 'America/Los_Angeles'];
    const props = {
      days,
      view: 'timeline' as const,
      today: anchor,
      state,
      expanded: false,
      gridRef: createRef<HTMLDivElement>(),
      primaryZoneId: 'Europe/Rome',
      secondaryZoneIds: zones,
      nowMinute: 12 * 60,
      onScroll: vi.fn(),
      onZoomAt: vi.fn(),
      onFocusEvent: vi.fn(),
      onToggleSubitems: vi.fn(),
      onOpenEventDetail: vi.fn(),
      onOpenSubitemDetail: vi.fn(),
      onMoveEvent: vi.fn(),
      onMoveFeedback: vi.fn(),
      onDragActiveChange: vi.fn(),
    };
    const { container, rerender } = render(<TimelineDayStream {...props} />);
    const primaryDays = Array.from(container.querySelectorAll<HTMLElement>(
      '.timeline-ruler-column--primary .timeline-ruler-day',
    ));
    expect(primaryDays).toHaveLength(2);
    const labels = (day: HTMLElement | undefined) =>
      Array.from(day?.querySelectorAll<HTMLElement>('.timeline-ruler-label') ?? []);
    const at = (day: HTMLElement | undefined, pixel: number) =>
      labels(day).filter((label) =>
        Math.abs(Number.parseFloat(label.style.top) - pixel) < 0.001,
      );
    expect(at(primaryDays[0], first.mapper.map(1440))).toHaveLength(0);
    const primaryMidnight = at(primaryDays[1], next.mapper.map(0));
    expect(primaryMidnight).toHaveLength(1);
    expect(primaryMidnight[0]?.textContent).toBe('00:00');
    expect(at(primaryDays[1], next.mapper.map(1440))).toHaveLength(0);

    for (const [zone, expectedClock] of [
      ['Europe/London', '23:00'],
      ['America/Los_Angeles', '15:00'],
    ] as const) {
      const column = Array.from(container.querySelectorAll<HTMLElement>(
        '.timeline-ruler-column--secondary',
      )).find((element) => element.dataset.secondaryTimeZone === zone);
      const rulerDays = Array.from(column?.querySelectorAll<HTMLElement>(
        '.timeline-ruler-day',
      ) ?? []);
      expect(rulerDays).toHaveLength(2);
      expect(at(rulerDays[0], first.mapper.map(1440))).toHaveLength(0);
      for (const [index, primaryDay] of primaryDays.entries()) {
        expect(labels(rulerDays[index]).map((label) => label.style.top))
          .toEqual(labels(primaryDay).map((label) => label.style.top));
      }
      const nextMidnight = at(rulerDays[1], next.mapper.map(0));
      expect(nextMidnight).toHaveLength(1);
      expect(nextMidnight[0]?.textContent).toContain(expectedClock);
      expect(nextMidnight[0]?.className).toBe(primaryMidnight[0]?.className);
      expect(nextMidnight[0]?.querySelector('.timeline-ruler-label__day-shift'))
        .toBeNull();
      for (const rulerDay of rulerDays) {
        for (const label of labels(rulerDay)) {
          const date = label.querySelector('.timeline-ruler-label__day-shift');
          if (label.firstChild?.textContent === '00:00') {
            expect(date?.textContent).toMatch(/^nov-(19|20)$/);
          } else {
            expect(date).toBeNull();
          }
        }
      }
      expect(at(rulerDays[0], first.mapper.map(1380))).toHaveLength(1);
    }

    // Day ends with the 23:00 label and an unlabeled boundary line.
    rerender(<TimelineDayStream {...props} view="day" days={[first]} />);
    const singleDayPrimary = container.querySelector<HTMLElement>(
      '.timeline-ruler-column--primary .timeline-ruler-day',
    );
    for (const column of container.querySelectorAll<HTMLElement>(
      '.timeline-ruler-column',
    )) {
      const rulerDay = column.querySelector<HTMLElement>('.timeline-ruler-day');
      expect(at(rulerDay, first.mapper.map(1440))).toHaveLength(0);
      expect(at(rulerDay, first.mapper.map(1380))).toHaveLength(1);
    }
    expect(at(singleDayPrimary, first.mapper.map(1380))[0]?.textContent)
      .toBe('23:00');

    // The auxiliary Week view is not part of the Day presentation change.
    rerender(<TimelineDayStream {...props} view="week" days={[first]} />);
    const weekPrimary = container.querySelector<HTMLElement>(
      '.timeline-ruler-column--primary .timeline-ruler-day',
    );
    expect(at(weekPrimary, first.mapper.map(1440))).toHaveLength(1);
  });
});
