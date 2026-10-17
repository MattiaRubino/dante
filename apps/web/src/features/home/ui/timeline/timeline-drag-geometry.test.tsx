// @vitest-environment jsdom
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
    };
    const { container, rerender } = render(
      <TimelineDayStream {...props} days={original} nowMinute={14 * 60 + 20} />,
    );
    const section = () =>
      container.querySelector<HTMLElement>('.timeline-day-section');
    const card = container.querySelector<HTMLElement>('[data-timeline-event="7"]');
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
    const pointerEvent = (type: string, target: EventTarget, clientY: number) => {
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
    expect(document.querySelector('.timeline-event-drag-overlay')).not.toBeNull();

    rerender(
      <TimelineDayStream
        {...props}
        days={[stretched]}
        nowMinute={14 * 60 + 25}
      />,
    );
    expect(section()?.style.height).toBe(`${first.height}px`);
    expect(
      container.querySelector('.timeline-now-line')?.getAttribute('style'),
    ).toContain(`${first.mapper.map(14 * 60 + 20)}px`);

    pointerEvent('pointerup', document, 190);
    expect(document.querySelector('.timeline-event-drag-overlay')).toBeNull();
    expect(section()?.style.height).toBe(`${stretched.height}px`);
  });
});
