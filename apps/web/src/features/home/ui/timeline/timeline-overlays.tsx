import type { PlainDate } from '@dante/time';
import {
  type KeyboardEvent,
  type PointerEvent as ReactPointerEvent,
  type RefObject,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import {
  buildCalendarMonthGrid,
  buildCalendarYearPage,
  calendarCursorFromDate,
  calendarYearPageBase,
  moveCalendarDay,
  shiftCalendarCursorMonth,
  shiftCalendarCursorYear,
  type TimelineCalendarCursor,
  type TimelineCalendarLevel,
} from './model/timeline-calendar';
import type { TimelineViewOptions } from './model/timeline-state';
import {
  formatTimelineMinute,
  isSameTimelineDate,
  parseTimelineDate,
  timelineDateKey,
} from './model/timeline-temporal';
import type { TimelineEvent, TimelineGroup } from './model/timeline-types';

type PopoverPosition = Readonly<{
  left: number;
  top: number;
  placement: 'top' | 'bottom';
}>;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function positionNearAnchor(
  anchor: HTMLElement,
  width: number,
  height: number,
  bounds?: DOMRect,
): PopoverPosition {
  const anchorRect = anchor.getBoundingClientRect();
  const visibleLeft = Math.max(4, bounds?.left ?? 4);
  const visibleRight = Math.min(
    window.innerWidth - 4,
    bounds?.right ?? window.innerWidth - 4,
  );
  const visibleTop = Math.max(4, bounds?.top ?? 4);
  const visibleBottom = Math.min(
    window.innerHeight - 4,
    bounds?.bottom ?? window.innerHeight - 4,
  );
  const maxLeft = Math.max(visibleLeft, visibleRight - width);
  const left = clamp(anchorRect.left, visibleLeft, maxLeft);
  const below = anchorRect.bottom + 8;
  const above = anchorRect.top - height - 8;
  const useTop = below + height > visibleBottom && above >= visibleTop;
  const top = clamp(
    useTop ? above : below,
    visibleTop,
    Math.max(visibleTop, visibleBottom - height),
  );
  return { left, top, placement: useTop ? 'top' : 'bottom' };
}

function useDismissablePopover(
  open: boolean,
  popoverRef: RefObject<HTMLElement | null>,
  anchorRef: RefObject<HTMLElement | null>,
  onClose: (restoreFocus?: boolean) => void,
) {
  useEffect(() => {
    if (!open) {
      return;
    }
    const onPointerDown = (event: PointerEvent) => {
      const target = event.target;
      if (!(target instanceof Node)) {
        return;
      }
      if (
        popoverRef.current?.contains(target) ||
        anchorRef.current?.contains(target)
      ) {
        return;
      }
      onClose(false);
    };
    const onKeyDown = (event: globalThis.KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        onClose(true);
      }
    };
    document.addEventListener('pointerdown', onPointerDown, true);
    document.addEventListener('keydown', onKeyDown, true);
    return () => {
      document.removeEventListener('pointerdown', onPointerDown, true);
      document.removeEventListener('keydown', onKeyDown, true);
    };
  }, [anchorRef, onClose, open, popoverRef]);
}

type CalendarPopoverProps = Readonly<{
  open: boolean;
  locale: string;
  today: PlainDate;
  viewDate: PlainDate;
  triggerRef: RefObject<HTMLButtonElement | null>;
  onClose: (restoreFocus?: boolean) => void;
  onDateSelect: (date: PlainDate) => void;
  onGoToday: () => void;
}>;

export function CalendarPopover({
  open,
  locale,
  today,
  viewDate,
  triggerRef,
  onClose,
  onDateSelect,
  onGoToday,
}: CalendarPopoverProps) {
  const { t } = useTranslation('common');
  const popoverRef = useRef<HTMLDivElement | null>(null);
  const [level, setLevel] = useState<TimelineCalendarLevel>('days');
  const [cursor, setCursor] = useState<TimelineCalendarCursor>(() =>
    calendarCursorFromDate(viewDate),
  );
  const [focusedDateKey, setFocusedDateKey] = useState<string | null>(null);
  const [position, setPosition] = useState<PopoverPosition>({
    left: 0,
    top: 0,
    placement: 'bottom',
  });

  useEffect(() => {
    if (!open) {
      return;
    }
    const frame = requestAnimationFrame(() => {
      setLevel('days');
      setCursor(calendarCursorFromDate(viewDate));
      setFocusedDateKey(timelineDateKey(viewDate));
    });
    return () => cancelAnimationFrame(frame);
  }, [open, viewDate]);

  useLayoutEffect(() => {
    if (!open || !triggerRef.current) {
      return;
    }
    const update = () => {
      if (triggerRef.current) {
        setPosition(
          positionNearAnchor(
            triggerRef.current,
            300,
            level === 'days' ? 356 : 272,
          ),
        );
      }
    };
    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);
    return () => {
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
    };
  }, [level, open, triggerRef]);

  useDismissablePopover(open, popoverRef, triggerRef, onClose);

  useLayoutEffect(() => {
    if (!open || !popoverRef.current) {
      return;
    }
    const escaped = focusedDateKey?.replaceAll('"', '\\"');
    const selected = escaped
      ? popoverRef.current.querySelector<HTMLButtonElement>(
          `[data-calendar-date="${escaped}"]`,
        )
      : null;
    const fallback = popoverRef.current.querySelector<HTMLButtonElement>(
      '.timeline-calendar-cell.is-selected, .timeline-calendar-cell',
    );
    (selected ?? fallback)?.focus();
  }, [focusedDateKey, level, open]);

  const monthGrid = useMemo(() => buildCalendarMonthGrid(cursor), [cursor]);
  const yearPage = useMemo(
    () => buildCalendarYearPage(cursor.year),
    [cursor.year],
  );

  if (!open) {
    return null;
  }

  const monthName = new Intl.DateTimeFormat(locale, {
    month: 'long',
    timeZone: 'UTC',
  }).format(new Date(Date.UTC(cursor.year, cursor.month - 1, 1, 12)));
  const monthShort = new Intl.DateTimeFormat(locale, {
    month: 'short',
    timeZone: 'UTC',
  });
  const weekDays = Array.from({ length: 7 }, (_, index) => {
    const monday = new Date(Date.UTC(2026, 7, 3 + index, 12));
    return new Intl.DateTimeFormat(locale, {
      weekday: 'short',
      timeZone: 'UTC',
    })
      .format(monday)
      .replace('.', '')
      .slice(0, 2);
  });

  const step = (direction: -1 | 1) => {
    if (level === 'days') {
      setCursor((value) => shiftCalendarCursorMonth(value, direction));
    } else if (level === 'months') {
      setCursor((value) => shiftCalendarCursorYear(value, direction));
    } else {
      setCursor((value) => shiftCalendarCursorYear(value, direction * 12));
    }
    setFocusedDateKey(null);
  };

  const onDayKeyDown = (
    event: KeyboardEvent<HTMLButtonElement>,
    date: PlainDate,
  ) => {
    const deltaByKey: Partial<Record<string, number>> = {
      ArrowLeft: -1,
      ArrowRight: 1,
      ArrowUp: -7,
      ArrowDown: 7,
    };
    const delta = deltaByKey[event.key];
    if (delta === undefined) {
      return;
    }
    event.preventDefault();
    const next = moveCalendarDay(date, delta);
    setCursor(calendarCursorFromDate(next));
    setFocusedDateKey(timelineDateKey(next));
  };

  return createPortal(
    <div
      ref={popoverRef}
      className="timeline-calendar-popover"
      role="dialog"
      aria-label={t(($) => $.common.home.timeline.calendar.dialogLabel)}
      data-placement={position.placement}
      style={{ left: position.left, top: position.top }}
    >
      <div className="timeline-calendar-head">
        <button
          type="button"
          onClick={() => step(-1)}
          aria-label={t(($) =>
            level === 'days'
              ? $.common.home.timeline.calendar.previousMonth
              : level === 'months'
                ? $.common.home.timeline.calendar.previousYear
                : $.common.home.timeline.calendar.previousPeriod,
          )}
        >
          ‹
        </button>
        {level === 'days' ? (
          <button
            className="timeline-calendar-level"
            type="button"
            onClick={() => setLevel('months')}
            aria-label={t(($) => $.common.home.timeline.calendar.chooseMonth)}
          >
            {monthName} {cursor.year}
          </button>
        ) : level === 'months' ? (
          <button
            className="timeline-calendar-level"
            type="button"
            onClick={() => setLevel('years')}
            aria-label={t(($) => $.common.home.timeline.calendar.chooseYear)}
          >
            {cursor.year}
          </button>
        ) : (
          <span className="timeline-calendar-level is-static">
            {calendarYearPageBase(cursor.year)}–
            {calendarYearPageBase(cursor.year) + 11}
          </span>
        )}
        <button
          type="button"
          onClick={() => step(1)}
          aria-label={t(($) =>
            level === 'days'
              ? $.common.home.timeline.calendar.nextMonth
              : level === 'months'
                ? $.common.home.timeline.calendar.nextYear
                : $.common.home.timeline.calendar.nextPeriod,
          )}
        >
          ›
        </button>
      </div>

      {level === 'days' ? (
        <>
          <div className="timeline-calendar-weekdays" aria-hidden="true">
            {weekDays.map((label, index) => (
              <span key={`${label}-${index}`}>{label}</span>
            ))}
          </div>
          <div className="timeline-calendar-grid is-days">
            {monthGrid.map((date) => {
              const selected = isSameTimelineDate(date, viewDate);
              const current = isSameTimelineDate(date, today);
              const outside = date.month !== cursor.month;
              const key = timelineDateKey(date);
              return (
                <button
                  className={`timeline-calendar-cell${selected ? ' is-selected' : ''}${current ? ' is-today' : ''}${outside ? ' is-outside' : ''}`}
                  key={key}
                  type="button"
                  data-calendar-date={key}
                  onKeyDown={(event) => onDayKeyDown(event, date)}
                  onClick={() => {
                    onDateSelect(date);
                    onClose(false);
                  }}
                  aria-current={selected ? 'date' : undefined}
                  aria-label={date.toLocaleString(locale, {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                  })}
                >
                  {date.day}
                </button>
              );
            })}
          </div>
        </>
      ) : level === 'months' ? (
        <div className="timeline-calendar-grid is-blocks">
          {Array.from({ length: 12 }, (_, index) => index + 1).map((month) => {
            const selected =
              viewDate.year === cursor.year && viewDate.month === month;
            const current = today.year === cursor.year && today.month === month;
            const label = monthShort.format(
              new Date(Date.UTC(cursor.year, month - 1, 1, 12)),
            );
            return (
              <button
                className={`timeline-calendar-cell${selected ? ' is-selected' : ''}${current ? ' is-today' : ''}`}
                key={month}
                type="button"
                onClick={() => {
                  setCursor({ year: cursor.year, month });
                  setLevel('days');
                  setFocusedDateKey(null);
                }}
              >
                {label}
              </button>
            );
          })}
        </div>
      ) : (
        <div className="timeline-calendar-grid is-blocks">
          {yearPage.map((year) => {
            const selected = viewDate.year === year;
            const current = today.year === year;
            return (
              <button
                className={`timeline-calendar-cell${selected ? ' is-selected' : ''}${current ? ' is-today' : ''}`}
                key={year}
                type="button"
                onClick={() => {
                  setCursor({ year, month: cursor.month });
                  setLevel('months');
                  setFocusedDateKey(null);
                }}
              >
                {year}
              </button>
            );
          })}
        </div>
      )}

      <div className="timeline-calendar-foot">
        <button type="button" onClick={() => onClose(true)}>
          {t(($) => $.common.home.timeline.calendar.close)}
        </button>
        <button
          className="is-primary"
          type="button"
          onClick={() => {
            onGoToday();
            onClose(false);
          }}
        >
          {t(($) => $.common.home.timeline.calendar.today)}
        </button>
      </div>
    </div>,
    document.body,
  );
}

type ViewOptionsPopoverProps = Readonly<{
  open: boolean;
  triggerRef: RefObject<HTMLButtonElement | null>;
  options: TimelineViewOptions;
  onChange: (option: keyof TimelineViewOptions, value: boolean) => void;
  onReset: () => void;
  onClose: (restoreFocus?: boolean) => void;
}>;

export function ViewOptionsPopover({
  open,
  triggerRef,
  options,
  onChange,
  onReset,
  onClose,
}: ViewOptionsPopoverProps) {
  const { t } = useTranslation('common');
  const popoverRef = useRef<HTMLDivElement | null>(null);
  const [position, setPosition] = useState<PopoverPosition>({
    left: 0,
    top: 0,
    placement: 'bottom',
  });

  useLayoutEffect(() => {
    if (!open || !triggerRef.current) {
      return;
    }
    const update = () => {
      if (triggerRef.current) {
        setPosition(positionNearAnchor(triggerRef.current, 232, 196));
      }
    };
    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);
    return () => {
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
    };
  }, [open, triggerRef]);

  useDismissablePopover(open, popoverRef, triggerRef, onClose);

  if (!open) {
    return null;
  }

  return createPortal(
    <div
      ref={popoverRef}
      className="timeline-view-popover"
      role="dialog"
      aria-label={t(($) => $.common.home.timeline.viewOptions.label)}
      data-placement={position.placement}
      style={{ left: position.left, top: position.top }}
    >
      <strong>{t(($) => $.common.home.timeline.viewOptions.label)}</strong>
      <label>
        <input
          type="checkbox"
          checked={options.showMargins}
          onChange={(event) =>
            onChange('showMargins', event.currentTarget.checked)
          }
        />
        {t(($) => $.common.home.timeline.viewOptions.margins)}
      </label>
      <label>
        <input
          type="checkbox"
          checked={options.showNow}
          onChange={(event) => onChange('showNow', event.currentTarget.checked)}
        />
        {t(($) => $.common.home.timeline.viewOptions.now)}
      </label>
      <label>
        <input
          type="checkbox"
          checked={options.showMilestones}
          onChange={(event) =>
            onChange('showMilestones', event.currentTarget.checked)
          }
        />
        {t(($) => $.common.home.timeline.viewOptions.milestones)}
      </label>
      <button type="button" onClick={onReset}>
        {t(($) => $.common.home.timeline.viewOptions.reset)}
      </button>
    </div>,
    document.body,
  );
}

type TimeEditorPopoverProps = Readonly<{
  event: TimelineEvent;
  dateKey: string;
  anchor: HTMLButtonElement;
  gridRef: RefObject<HTMLDivElement | null>;
  onSave: (
    dateKey: string,
    eventId: string,
    startMinute: number,
    endMinute: number,
  ) => void;
  onClose: (restoreFocus?: boolean) => void;
}>;

function TimeSegment({
  label,
  minute,
  isEnd,
  onChange,
  onMarkDirty,
  onSubmit,
}: Readonly<{
  label: string;
  minute: number;
  isEnd: boolean;
  onChange: (minute: number) => void;
  onMarkDirty: () => void;
  onSubmit: () => void;
}>) {
  const { t } = useTranslation('common');
  const hour = Math.floor(minute / 60);
  const minutePart = minute % 60;
  const maximum = isEnd ? 1440 : 1439;

  const applyDelta = (amount: number) => {
    if (isEnd) {
      onMarkDirty();
    }
    onChange(clamp(minute + amount, 0, maximum));
  };

  const changePart = (part: 'hour' | 'minute', raw: string) => {
    const numeric = Number.parseInt(raw, 10);
    if (!Number.isFinite(numeric)) {
      return;
    }
    if (isEnd) {
      onMarkDirty();
    }
    if (part === 'hour') {
      const maxHour = isEnd ? 24 : 23;
      const nextHour = clamp(numeric, 0, maxHour);
      const nextMinute = nextHour === 24 ? 0 : minutePart;
      onChange(nextHour * 60 + nextMinute);
      return;
    }
    const nextMinute = clamp(numeric, 0, 59);
    const safeHour = hour === 24 ? 23 : hour;
    onChange(safeHour * 60 + nextMinute);
  };

  const step = (
    event: KeyboardEvent<HTMLInputElement>,
    segment: 'hour' | 'minute',
  ) => {
    if (!['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown'].includes(event.key)) {
      if (event.key === 'Enter') {
        event.preventDefault();
        onSubmit();
      }
      return;
    }
    event.preventDefault();
    const positive = event.key === 'ArrowUp' || event.key === 'PageUp';
    const amount = event.altKey
      ? 1
      : event.key.startsWith('Page')
        ? segment === 'hour'
          ? 120
          : 15
        : segment === 'hour'
          ? 60
          : 5;
    applyDelta(positive ? amount : -amount);
  };

  return (
    <div className="timeline-time-field">
      <label>{label}</label>
      <div className="timeline-time-spin">
        <input
          className="timeline-time-hour"
          inputMode="numeric"
          value={String(hour).padStart(2, '0')}
          onChange={(event) => changePart('hour', event.currentTarget.value)}
          onKeyDown={(event) => step(event, 'hour')}
          onWheel={(event) => {
            event.preventDefault();
            applyDelta(event.deltaY < 0 ? 60 : -60);
          }}
          aria-label={t(($) => $.common.home.timeline.timeEditor.hourPart, {
            label,
          })}
        />
        <b>:</b>
        <input
          className="timeline-time-minute"
          inputMode="numeric"
          value={String(minutePart).padStart(2, '0')}
          onChange={(event) => changePart('minute', event.currentTarget.value)}
          onKeyDown={(event) => step(event, 'minute')}
          onWheel={(event) => {
            event.preventDefault();
            applyDelta(event.deltaY < 0 ? 5 : -5);
          }}
          aria-label={t(($) => $.common.home.timeline.timeEditor.minutePart, {
            label,
          })}
        />
      </div>
      <div className="timeline-time-steps">
        <button
          type="button"
          onClick={() => applyDelta(5)}
          aria-label={t(($) => $.common.home.timeline.timeEditor.increase, {
            label,
          })}
        >
          ▲
        </button>
        <button
          type="button"
          onClick={() => applyDelta(-5)}
          aria-label={t(($) => $.common.home.timeline.timeEditor.decrease, {
            label,
          })}
        >
          ▼
        </button>
      </div>
    </div>
  );
}

export function TimeEditorPopover({
  event,
  dateKey,
  anchor,
  gridRef,
  onSave,
  onClose,
}: TimeEditorPopoverProps) {
  const { t } = useTranslation('common');
  const popoverRef = useRef<HTMLDivElement | null>(null);
  const anchorRef = useMemo<RefObject<HTMLElement | null>>(
    () => ({ current: anchor }),
    [anchor],
  );
  const [startMinute, setStartMinute] = useState(event.startMinute);
  const [endMinute, setEndMinute] = useState(event.endMinute);
  const [endDirty, setEndDirty] = useState(false);
  const [error, setError] = useState(false);
  const [position, setPosition] = useState<PopoverPosition>({
    left: 0,
    top: 0,
    placement: 'bottom',
  });
  const originalDuration = event.endMinute - event.startMinute;

  const updateStart = (value: number) => {
    const next = clamp(value, 0, 1439);
    setStartMinute(next);
    if (!endDirty) {
      setEndMinute(clamp(next + originalDuration, 1, 1440));
    }
    setError(false);
  };

  const updateEnd = (value: number) => {
    setEndDirty(true);
    setEndMinute(clamp(value, 1, 1440));
    setError(false);
  };

  const save = () => {
    if (endMinute <= startMinute) {
      setError(true);
      return;
    }
    onSave(dateKey, event.id, startMinute, endMinute);
    onClose(true);
  };

  useLayoutEffect(() => {
    const update = () => {
      setPosition(
        positionNearAnchor(
          anchor,
          286,
          246,
          gridRef.current?.getBoundingClientRect(),
        ),
      );
    };
    update();
    window.addEventListener('resize', update);
    window.addEventListener('scroll', update, true);
    return () => {
      window.removeEventListener('resize', update);
      window.removeEventListener('scroll', update, true);
    };
  }, [anchor, gridRef]);

  useDismissablePopover(true, popoverRef, anchorRef, onClose);

  return createPortal(
    <div
      ref={popoverRef}
      className="timeline-time-popover"
      role="dialog"
      aria-label={t(($) => $.common.home.timeline.timeEditor.title)}
      data-placement={position.placement}
      style={{ left: position.left, top: position.top }}
    >
      <strong>{t(($) => $.common.home.timeline.timeEditor.title)}</strong>
      <TimeSegment
        label={t(($) => $.common.home.timeline.timeEditor.start)}
        minute={startMinute}
        isEnd={false}
        onChange={updateStart}
        onMarkDirty={() => undefined}
        onSubmit={save}
      />
      <TimeSegment
        label={t(($) => $.common.home.timeline.timeEditor.end)}
        minute={endMinute}
        isEnd
        onChange={updateEnd}
        onMarkDirty={() => setEndDirty(true)}
        onSubmit={save}
      />
      <div className="timeline-time-duration">
        {Math.max(0, endMinute - startMinute)} min
      </div>
      <div
        className={`timeline-time-error${error ? ' is-visible' : ''}`}
        role="alert"
      >
        {t(($) => $.common.home.timeline.timeEditor.invalid)}
      </div>
      <div className="timeline-time-actions">
        <button type="button" onClick={() => onClose(true)}>
          {t(($) => $.common.home.timeline.timeEditor.cancel)}
        </button>
        <button className="is-primary" type="button" onClick={save}>
          {t(($) => $.common.home.timeline.timeEditor.save)}
        </button>
      </div>
    </div>,
    document.body,
  );
}

export type TimelineDetail = Readonly<{
  title: string;
  startMinute: number;
  endMinute: number;
  groupLabel: string;
  meta: string;
  subitemsCount?: number;
}>;

type EventDetailDialogProps = Readonly<{
  detail: TimelineDetail | null;
  opener: HTMLElement | null;
  onClose: () => void;
}>;

export function EventDetailDialog({
  detail,
  opener,
  onClose,
}: EventDetailDialogProps) {
  const { t } = useTranslation('common');
  const closeButtonRef = useRef<HTMLButtonElement | null>(null);

  useEffect(() => {
    if (!detail) {
      return;
    }
    closeButtonRef.current?.focus();
    const keydown = (event: globalThis.KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        onClose();
      } else if (event.key === 'Tab') {
        event.preventDefault();
        closeButtonRef.current?.focus();
      }
    };
    document.addEventListener('keydown', keydown, true);
    return () => {
      document.removeEventListener('keydown', keydown, true);
      opener?.focus();
    };
  }, [detail, onClose, opener]);

  if (!detail) {
    return null;
  }

  return createPortal(
    <div
      className="timeline-modal-backdrop is-open"
      role="presentation"
      onPointerDown={(event: ReactPointerEvent<HTMLDivElement>) => {
        if (event.currentTarget === event.target) {
          onClose();
        }
      }}
    >
      <div
        className="timeline-event-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="timeline-event-dialog-title"
      >
        <h3 id="timeline-event-dialog-title">{detail.title}</h3>
        <p>
          {formatTimelineMinute(detail.startMinute)}–
          {formatTimelineMinute(detail.endMinute)} · {detail.groupLabel}
          {detail.meta ? ` · ${detail.meta}` : ''}
        </p>
        {detail.subitemsCount ? (
          <p>
            {t(($) => $.common.home.timeline.detail.subitems, {
              count: detail.subitemsCount,
            })}
          </p>
        ) : null}
        <div className="timeline-event-ai-note">
          {t(($) => $.common.home.timeline.detail.aiNote)}
        </div>
        <button ref={closeButtonRef} type="button" onClick={onClose}>
          {t(($) => $.common.home.timeline.detail.close)}
        </button>
      </div>
    </div>,
    document.body,
  );
}

type UndoToastProps = Readonly<{
  visible: boolean;
  message: string;
  onUndo: () => void;
}>;

export function UndoToast({ visible, message, onUndo }: UndoToastProps) {
  const { t } = useTranslation('common');
  return (
    <div
      className={`timeline-move-toast${visible ? ' is-on' : ''}`}
      role="status"
      aria-live="polite"
    >
      <span>{message}</span>
      <button type="button" onClick={onUndo}>
        {t(($) => $.common.home.timeline.undo)}
      </button>
    </div>
  );
}

export function detailFromEvent(
  event: TimelineEvent,
  groups: readonly TimelineGroup[],
): TimelineDetail {
  const group = groups.find((candidate) => candidate.id === event.groupId);
  const base: TimelineDetail = {
    title: event.title,
    startMinute: event.startMinute,
    endMinute: event.endMinute,
    groupLabel: group?.label ?? event.groupId,
    meta: event.meta ?? '',
  };
  return event.subitems?.length
    ? { ...base, subitemsCount: event.subitems.length }
    : base;
}

export function detailFromSubitem(
  event: TimelineEvent,
  subitem: string,
  groups: readonly TimelineGroup[],
  parentLabel: string,
): TimelineDetail {
  const group = groups.find((candidate) => candidate.id === event.groupId);
  return {
    title: subitem,
    startMinute: event.startMinute,
    endMinute: event.endMinute,
    groupLabel: group?.label ?? event.groupId,
    meta: `${parentLabel} ${event.title}`,
  };
}

export function parseCalendarDateKey(value: string): PlainDate {
  return parseTimelineDate(value);
}
