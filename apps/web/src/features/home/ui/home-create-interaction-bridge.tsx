import { useEffect } from 'react';

import { TIMELINE_POLICY } from './timeline/model/timeline-policy';

function parsePixel(value: string): number {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function emptyTimelineSection(target: EventTarget | null): HTMLElement | null {
  if (!(target instanceof Element)) {
    return null;
  }
  if (
    target.closest(
      'button, input, select, textarea, a, .timeline-event-card, .timeline-all-day-lane, .timeline-all-day-item, .temporal-create-projection-card, .temporal-create-all-day',
    )
  ) {
    return null;
  }
  return target.closest<HTMLElement>(
    '.timeline-day-section[data-timeline-date]',
  );
}

function minuteAtClientY(section: HTMLElement, clientY: number): number {
  const rect = section.getBoundingClientRect();
  const localY = clientY - rect.top;
  const lines = Array.from(
    section.querySelectorAll<HTMLElement>('.timeline-hour-line'),
  );
  const interval = TIMELINE_POLICY.grid.minorLineIntervalMinutes;

  if (lines.length < 2) {
    return Math.max(
      0,
      Math.min(1439, (localY / Math.max(1, rect.height)) * 1440),
    );
  }

  for (let index = 0; index < lines.length - 1; index += 1) {
    const current = parsePixel(lines[index]?.style.top ?? '0');
    const next = parsePixel(lines[index + 1]?.style.top ?? String(current));
    if (localY <= next) {
      const progress =
        next <= current ? 0 : (localY - current) / (next - current);
      return Math.max(
        0,
        Math.min(1439, (index + Math.max(0, Math.min(1, progress))) * interval),
      );
    }
  }

  return 1439;
}

function snapMinute(minute: number): number {
  return Math.max(0, Math.min(1425, Math.round(minute / 15) * 15));
}

function formatMinute(minute: number): string {
  return `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(
    minute % 60,
  ).padStart(2, '0')}`;
}

function setControlledInput(input: HTMLInputElement, value: string): void {
  const setter = Object.getOwnPropertyDescriptor(
    HTMLInputElement.prototype,
    'value',
  )?.set;
  setter?.call(input, value);
  input.dispatchEvent(new Event('input', { bubbles: true }));
  input.dispatchEvent(new Event('change', { bubbles: true }));
}

function reseedOpenCreate(section: HTMLElement, clientY: number): void {
  const date = section.dataset.timelineDate;
  if (!date) {
    return;
  }

  const minute = snapMinute(minuteAtClientY(section, clientY));
  const composerSelector = '[data-temporal-create="composer"]';
  const apply = () => {
    const dateInput = document.querySelector<HTMLInputElement>(
      `${composerSelector} [data-create-path="date"]`,
    );
    const timeInput = document.querySelector<HTMLInputElement>(
      `${composerSelector} [data-create-path="startTime"]`,
    );
    if (!dateInput || !timeInput) {
      return;
    }
    setControlledInput(dateInput, date);
    setControlledInput(timeInput, formatMinute(minute));
  };

  const timedButton = document.querySelector<HTMLButtonElement>(
    `${composerSelector} [data-create-path="timeSemantics"] button[role="radio"]`,
  );
  if (timedButton?.getAttribute('aria-checked') !== 'true') {
    timedButton?.click();
    requestAnimationFrame(apply);
    return;
  }
  apply();
}

export function HomeCreateInteractionBridge() {
  useEffect(() => {
    const onPointerDown = (event: PointerEvent) => {
      const composer = document.querySelector<HTMLElement>(
        '[data-temporal-create="composer"]',
      );
      if (!composer) {
        return;
      }

      if (document.querySelector('.temporal-create-discard')) {
        return;
      }

      const target = event.target;
      if (!(target instanceof Node) || composer.contains(target)) {
        return;
      }

      if (
        target instanceof Element &&
        target.closest('.dante-timeline-quick-add')
      ) {
        return;
      }

      const timelineSection = emptyTimelineSection(target);
      if (timelineSection) {
        reseedOpenCreate(timelineSection, event.clientY);
        return;
      }

      composer.dispatchEvent(
        new KeyboardEvent('keydown', {
          key: 'Escape',
          bubbles: true,
          cancelable: true,
        }),
      );
    };

    // When Create is already open, Timeline clicks are only a temporal reseed.
    // Consume the resulting dblclick before TimelineCreateBridge can enqueue a
    // second invocation which would otherwise reopen Create after dismissal.
    const onDoubleClick = (event: MouseEvent) => {
      const composer = document.querySelector<HTMLElement>(
        '[data-temporal-create="composer"]',
      );
      if (!composer || document.querySelector('.temporal-create-discard')) {
        return;
      }
      const timelineSection = emptyTimelineSection(event.target);
      if (!timelineSection) {
        return;
      }
      reseedOpenCreate(timelineSection, event.clientY);
      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
    };

    document.addEventListener('pointerdown', onPointerDown, true);
    window.addEventListener('dblclick', onDoubleClick, true);
    return () => {
      document.removeEventListener('pointerdown', onPointerDown, true);
      window.removeEventListener('dblclick', onDoubleClick, true);
    };
  }, []);

  return null;
}
