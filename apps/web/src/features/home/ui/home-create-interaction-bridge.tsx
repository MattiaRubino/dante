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

function timeSegmentInput(target: EventTarget | null): HTMLInputElement | null {
  if (!(target instanceof HTMLInputElement)) {
    return null;
  }
  if (!target.closest('[data-temporal-create="composer"]')) {
    return null;
  }
  if (!target.closest('.temporal-create-time-segment')) {
    return null;
  }
  return target;
}

function closeOpenTimePicker(input: HTMLInputElement): void {
  const control = input.closest('.temporal-create-time-control');
  const trigger = control?.querySelector<HTMLButtonElement>(
    '.temporal-create-clock-trigger[aria-expanded="true"]',
  );
  trigger?.click();
}

function selectTimeSegment(target: EventTarget | null): void {
  const input = timeSegmentInput(target);
  if (!input) {
    return;
  }

  closeOpenTimePicker(input);
  queueMicrotask(() => {
    if (input.isConnected) {
      input.select();
    }
  });
}

function advanceHourToMinutes(target: EventTarget | null): void {
  const input = timeSegmentInput(target);
  if (!input || !input.getAttribute('aria-label')?.endsWith(': ore')) {
    return;
  }
  if (!/^\d{2}$/.test(input.value) || Number(input.value) > 23) {
    return;
  }

  const editor = input.closest('.temporal-create-inline-time-editor');
  const segments = editor?.querySelectorAll<HTMLInputElement>(
    '.temporal-create-time-segment input',
  );
  const minuteInput = segments?.[1];
  if (!minuteInput) {
    return;
  }

  queueMicrotask(() => {
    if (!minuteInput.isConnected) {
      return;
    }
    minuteInput.focus({ preventScroll: true });
    minuteInput.select();
  });
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

    const onTimeSegmentFocus = (event: FocusEvent) => {
      selectTimeSegment(event.target);
    };

    const onTimeSegmentClick = (event: MouseEvent) => {
      selectTimeSegment(event.target);
    };

    const onTimeSegmentInput = (event: Event) => {
      advanceHourToMinutes(event.target);
    };

    document.addEventListener('pointerdown', onPointerDown, true);
    document.addEventListener('focusin', onTimeSegmentFocus, true);
    document.addEventListener('click', onTimeSegmentClick, true);
    document.addEventListener('input', onTimeSegmentInput);
    window.addEventListener('dblclick', onDoubleClick, true);
    return () => {
      document.removeEventListener('pointerdown', onPointerDown, true);
      document.removeEventListener('focusin', onTimeSegmentFocus, true);
      document.removeEventListener('click', onTimeSegmentClick, true);
      document.removeEventListener('input', onTimeSegmentInput);
      window.removeEventListener('dblclick', onDoubleClick, true);
    };
  }, []);

  return null;
}
