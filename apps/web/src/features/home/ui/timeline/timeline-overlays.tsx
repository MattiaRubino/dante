import { Temporal, type PlainDate } from '@dante/time';
import {
  type CSSProperties,
  type KeyboardEvent,
  type PointerEvent as ReactPointerEvent,
  type RefObject,
  useCallback,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import { ResponsibilityControls } from '../../../temporal/responsibility-controls';
import { ActivitySessionCardControls } from '../../../temporal/activity-session-card-controls';
import { ActivityPlannedSessionsCardDetail } from '../../../temporal/activity-planned-sessions-card-detail';
import { ScheduleReminderControls } from '../../../temporal/schedule-reminder-controls';
import { PlacementLockControls } from '../../../temporal/placement-lock-controls';
import type { ActivityProfile } from '../../../temporal/remote-activity-inspector';
import { createRemoteActivityInspector } from '../../../temporal/remote-activity-inspector';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import { ActivityEditPanel } from './activity-edit-panel';
import { RecurringActivitySeriesEditor } from './recurring-series-editor';
import { requestTemporalCreateDuplicate } from '../../../temporal-create/ui/temporal-create-duplicate-request';
import { TemporalPanelCloseButton } from '../../../temporal-create/ui/temporal-panel-close-button';
import { ActivityInspectorActions } from './activity-inspector-actions';
import { EventInspectorActions } from './event-inspector-actions';
import { TimelineInspectorReality } from './timeline-inspector-reality';
import { TimelineInspectorOccurrenceSession } from './timeline-inspector-occurrence-session';
import { LEGACY_UNASSIGNED_GROUP } from './timeline-organization';

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
import type {
  TimelineEvent,
  TimelineGroup,
  TimelineCanonicalSchedulePlacement,
} from './model/timeline-types';
import { TimelineEventAgendaEditor } from './timeline-event-agenda-editor';
import { RecurringEditScopeDialog } from './recurring-edit-scope-dialog';

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

export type TimelineDetail = Readonly<{
  title: string;
  startMinute: number;
  endMinute: number;
  groupLabel: string;
  contextLabel?: string;
  dateKey?: string;
  accentColorCode?: string;
  ownerKind?: 'activity' | 'event';
  eventRef?: string;
  occurrenceRef?: string;
  eventPlacement?: TimelineCanonicalSchedulePlacement;
  schedulePlacement?: TimelineCanonicalSchedulePlacement;
  realitySubject?: Readonly<{
    kind: 'activity' | 'event' | 'occurrence';
    ref: string;
  }>;
  subitemsCount?: number;
}>;

type EventDetailDialogProps = Readonly<{
  detail: TimelineDetail | null;
  opener: HTMLElement | null;
  sessionSubject?: Readonly<{
    kind: 'activity' | 'occurrence';
    ref: string;
  }> | null;
  responsibilitySubject?: Readonly<{
    kind: 'activity' | 'event';
    ref: string;
  }> | null;
  reminderScheduleRef?: string | null;
  placementLockScheduleRef?: string | null;
  locale?: string;
  timeZone?: string;
  openActivityEdit?: boolean;
  initialActivityEditScope?: 'this_and_following' | undefined;
  onActivitySaved?: (profile: ActivityProfile) => void;
  onActivityDeleted?: () => void;
  onClose: () => void;
}>;

function detailScheduleLabel(
  detail: TimelineDetail,
  locale: string,
  timeZone?: string,
): string {
  const dateLabel = (
    dateKey: string,
    options: Intl.DateTimeFormatOptions = {},
  ) =>
    new Intl.DateTimeFormat(locale, {
      day: 'numeric',
      month: 'short',
      timeZone: 'UTC',
      ...options,
    }).format(new Date(`${dateKey}T12:00:00Z`));
  const placement = detail.schedulePlacement;
  if (placement?.kind === 'date-span') {
    return `${dateLabel(placement.startDate.toString())}–${dateLabel(placement.endDateExclusive.subtract({ days: 1 }).toString())} · ${locale.startsWith('it') ? 'Tutto il giorno' : 'All day'}`;
  }
  if (
    placement &&
    detail.startMinute === 0 &&
    detail.endMinute === 1440 &&
    placement.kind !== 'coarse-local-period'
  ) {
    const start =
      placement.kind === 'absolute'
        ? placement.startsAt
            .toZonedDateTimeISO(timeZone ?? 'UTC')
            .toPlainDateTime()
        : placement.startsLocalAt;
    const end =
      placement.kind === 'absolute'
        ? placement.endsAt
            .toZonedDateTimeISO(timeZone ?? 'UTC')
            .toPlainDateTime()
        : placement.endsLocalAt;
    const boundary = (value: Temporal.PlainDateTime) =>
      `${dateLabel(value.toPlainDate().toString())} ${value.toPlainTime().toString({ smallestUnit: 'minute' })}`;
    return `${boundary(start)} → ${boundary(end)}`;
  }
  const day = detail.dateKey
    ? `${new Intl.DateTimeFormat(locale, {
        weekday: 'long',
        day: 'numeric',
        month: 'long',
        ...(Number(detail.dateKey.slice(0, 4)) !== new Date().getFullYear()
          ? { year: 'numeric' }
          : {}),
        timeZone: 'UTC',
      })
        .format(new Date(`${detail.dateKey}T12:00:00Z`))
        .replace(/^./, (letter) => letter.toLocaleUpperCase(locale))} · `
    : '';
  return `${day}${formatTimelineMinute(detail.startMinute)}–${formatTimelineMinute(detail.endMinute)}`;
}

export function EventDetailDialog({
  detail,
  opener,
  sessionSubject = null,
  responsibilitySubject = null,
  reminderScheduleRef = null,
  placementLockScheduleRef = null,
  locale = 'it-IT',
  timeZone,
  openActivityEdit = false,
  initialActivityEditScope,
  onActivitySaved,
  onActivityDeleted,
  onClose,
}: EventDetailDialogProps) {
  const { t } = useTranslation('common');
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const closeButtonRef = useRef<HTMLButtonElement | null>(null);
  const editCloseRequestRef = useRef<(() => void) | null>(null);
  const [editingProfile, setEditingProfile] = useState<ActivityProfile | null>(
    null,
  );
  const [activityEditScope, setActivityEditScope] = useState<
    'only_this' | 'this_and_following' | 'from_next'
  >('only_this');
  const [activityEditChoice, setActivityEditChoice] = useState<{
    profile: ActivityProfile;
    selectedHasFacts: boolean;
  } | null>(null);
  const [inspectorPosition, setInspectorPosition] = useState({
    left: 12,
    top: 12,
  });
  const [toolbarTarget, setToolbarTarget] = useState<HTMLDivElement | null>(
    null,
  );
  const [activityDescription, setActivityDescription] = useState<{
    ref: string;
    value: string | null;
  } | null>(null);
  const activityRef =
    sessionSubject?.kind === 'activity' ? sessionSubject.ref : null;
  useEffect(() => {
    if (!activityRef || !openActivityEdit) return;
    let active = true;
    const activitySource = createRemoteActivityInspector();
    const recurringSource = createRemoteRecurringProfileEdit();
    void Promise.all([
      activitySource.get(activityRef),
      recurringSource.loadActivityContext(activityRef),
    ])
      .then(async ([profile, recurring]) => {
        if (!active) return;
        if (initialActivityEditScope) {
          setActivityEditScope(initialActivityEditScope);
          setEditingProfile(profile);
          return;
        }
        if (recurring === null) {
          setEditingProfile(profile);
          return;
        }
        const preview = await recurringSource.loadPreview(
          recurring,
          'only_this',
        );
        if (active) {
          setActivityEditChoice({
            profile,
            selectedHasFacts: preview.selectedProtection === 'registration',
          });
        }
      })
      .catch(() => undefined);
    return () => {
      active = false;
    };
  }, [activityRef, openActivityEdit, initialActivityEditScope]);
  useEffect(() => {
    if (!activityRef) return;
    let active = true;
    void createRemoteActivityInspector()
      .get(activityRef)
      .then((profile) => {
        if (active)
          setActivityDescription({
            ref: activityRef,
            value: profile.description,
          });
      })
      .catch(() => undefined);
    return () => {
      active = false;
    };
  }, [activityRef]);
  const currentEditingProfile =
    editingProfile?.activityRef === sessionSubject?.ref ? editingProfile : null;

  const requestCloseCurrent = useCallback(() => {
    if (currentEditingProfile) editCloseRequestRef.current?.();
    else onClose();
  }, [currentEditingProfile, onClose]);

  useEffect(() => {
    if (!detail) return;
    const previousBody = document.body.style.overflow;
    const previousRoot = document.documentElement.style.overflow;
    document.body.style.overflow = 'hidden';
    document.documentElement.style.overflow = 'hidden';
    const siblings = Array.from(document.body.children).filter(
      (element) => !element.classList.contains('timeline-modal-backdrop'),
    );
    const previousInert = siblings.map((element) =>
      element.hasAttribute('inert'),
    );
    siblings.forEach((element) => element.setAttribute('inert', ''));
    return () => {
      document.body.style.overflow = previousBody;
      document.documentElement.style.overflow = previousRoot;
      siblings.forEach((element, index) => {
        if (!previousInert[index]) element.removeAttribute('inert');
      });
    };
  }, [detail]);

  useLayoutEffect(() => {
    if (!detail || currentEditingProfile || !opener) return;
    const updatePosition = () => {
      const anchor =
        opener.closest<HTMLElement>('[data-timeline-event]') ?? opener;
      const rect = anchor.getBoundingClientRect();
      const panel = dialogRef.current;
      const width = panel?.offsetWidth || Math.min(420, window.innerWidth - 24);
      const height = panel?.offsetHeight || 320;
      const gap = 12;
      const right = rect.right + gap;
      const left = rect.left - width - gap;
      const preferredLeft =
        right + width <= window.innerWidth - 12
          ? right
          : left >= 12
            ? left
            : right;
      setInspectorPosition({
        left: clamp(
          preferredLeft,
          12,
          Math.max(12, window.innerWidth - width - 12),
        ),
        top: clamp(
          rect.top,
          12,
          Math.max(12, window.innerHeight - height - 12),
        ),
      });
    };
    updatePosition();
    window.addEventListener('resize', updatePosition);
    const observer =
      typeof ResizeObserver === 'undefined' || !dialogRef.current
        ? null
        : new ResizeObserver(updatePosition);
    if (dialogRef.current) observer?.observe(dialogRef.current);
    return () => {
      window.removeEventListener('resize', updatePosition);
      observer?.disconnect();
    };
  }, [detail, opener, currentEditingProfile]);

  useEffect(() => {
    if (!detail) {
      return;
    }
    closeButtonRef.current?.focus();
    const keydown = (event: globalThis.KeyboardEvent) => {
      if (
        event.target instanceof Element &&
        event.target.closest('.timeline-recurring-edit-scope-dialog__backdrop')
      ) {
        return;
      }
      if (event.key === 'Escape') {
        event.preventDefault();
        requestCloseCurrent();
      } else if (event.key === 'Tab') {
        const focusable = Array.from(
          dialogRef.current?.querySelectorAll<HTMLElement>(
            'button:not([disabled]), input:not([disabled]), textarea:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])',
          ) ?? [],
        ).filter((element) => !element.closest('[inert]'));
        if (focusable.length === 0) {
          return;
        }
        event.preventDefault();
        const activeIndex = focusable.indexOf(
          document.activeElement as HTMLElement,
        );
        const offset = event.shiftKey ? -1 : 1;
        const nextIndex =
          (activeIndex + offset + focusable.length) % focusable.length;
        focusable[nextIndex]?.focus();
      }
    };
    document.addEventListener('keydown', keydown, true);
    return () => {
      document.removeEventListener('keydown', keydown, true);
    };
  }, [detail, requestCloseCurrent]);

  const isOpen = detail !== null;
  useEffect(() => {
    if (!isOpen) return;
    return () => opener?.focus({ preventScroll: true });
  }, [isOpen, opener]);

  if (!detail) {
    return null;
  }

  return createPortal(
    <div
      className={`timeline-modal-backdrop is-open${currentEditingProfile ? '' : ' timeline-modal-backdrop--inspector'}`}
      role="presentation"
      onPointerDown={(event: ReactPointerEvent<HTMLDivElement>) => {
        if (event.currentTarget === event.target) {
          requestCloseCurrent();
        }
      }}
    >
      <div
        ref={dialogRef}
        className={`timeline-event-modal${currentEditingProfile ? ' timeline-event-modal--edit' : ' timeline-event-modal--inspector'}`}
        style={
          currentEditingProfile
            ? undefined
            : {
                ...inspectorPosition,
                ...(detail.accentColorCode
                  ? ({
                      '--timeline-inspector-accent': detail.accentColorCode,
                    } as CSSProperties)
                  : {}),
              }
        }
        role="dialog"
        aria-modal="true"
        aria-labelledby="timeline-event-dialog-title"
      >
        <div className="timeline-event-modal__header">
          <div className="timeline-event-modal__header-actions">
            {currentEditingProfile ? null : placementLockScheduleRef ===
              null ? null : (
              <PlacementLockControls
                key={placementLockScheduleRef}
                scheduleRef={placementLockScheduleRef}
                variant="icon"
              />
            )}
            {currentEditingProfile ? null : (
              <div
                ref={setToolbarTarget}
                className="timeline-event-modal__owner-actions"
              />
            )}
            <TemporalPanelCloseButton
              buttonRef={closeButtonRef}
              label={
                currentEditingProfile
                  ? 'Torna all’Inspector'
                  : 'Chiudi Inspector'
              }
              onClick={requestCloseCurrent}
            />
          </div>
        </div>
        <div className="timeline-event-modal__title-row">
          <h3
            id="timeline-event-dialog-title"
            className="timeline-event-modal__title"
            title={detail.title}
          >
            {currentEditingProfile ? 'Modifica attività' : detail.title}
          </h3>
        </div>
        {!currentEditingProfile && detail.contextLabel ? (
          <p className="timeline-event-modal__context">{detail.contextLabel}</p>
        ) : null}
        {currentEditingProfile && activityEditScope !== 'only_this' ? (
          <RecurringActivitySeriesEditor
            activityRef={currentEditingProfile.activityRef}
            scope={activityEditScope}
            closeRequestRef={editCloseRequestRef}
            onSaved={() => {
              onActivitySaved?.(currentEditingProfile);
              setEditingProfile(null);
            }}
            onCancel={() => setEditingProfile(null)}
          />
        ) : currentEditingProfile ? (
          <ActivityEditPanel
            key={`${currentEditingProfile.activityRef}:${currentEditingProfile.revision}`}
            profile={currentEditingProfile}
            initialScope={activityEditScope}
            {...(timeZone ? { timeZone } : {})}
            closeRequestRef={editCloseRequestRef}
            onSaved={(saved) => {
              onActivitySaved?.(saved);
              setActivityDescription({
                ref: saved.activityRef,
                value: saved.description,
              });
              setEditingProfile(null);
            }}
            onCancel={() => setEditingProfile(null)}
          />
        ) : (
          <>
            {sessionSubject?.kind === 'activity' &&
            onActivitySaved &&
            onActivityDeleted ? (
              <ActivityInspectorActions
                toolbarTarget={toolbarTarget}
                activityRef={sessionSubject.ref}
                subitemsCount={detail.subitemsCount ?? 0}
                onEdit={(profile, scope) => {
                  setActivityEditScope(scope);
                  setEditingProfile(profile);
                }}
                onCancelScope={onClose}
                onDeleted={onActivityDeleted}
                onDuplicate={(seed) => {
                  onClose();
                  requestTemporalCreateDuplicate(seed);
                }}
              />
            ) : null}
            <div className="timeline-event-modal__schedule-row">
              <p className="timeline-event-modal__time">
                {detailScheduleLabel(detail, locale, timeZone)}
              </p>
              {sessionSubject?.kind === 'activity' ? (
                <ActivitySessionCardControls
                  activityRef={sessionSubject.ref}
                  label={detail.title}
                  variant="inspector"
                  showPlanned={false}
                  locale={locale}
                  {...(timeZone ? { timeZone } : {})}
                />
              ) : null}
            </div>
            {sessionSubject?.kind === 'activity' ? (
              <ActivityPlannedSessionsCardDetail
                activityRef={sessionSubject.ref}
                visible
                locale={locale}
                {...(timeZone ? { timeZone } : {})}
              />
            ) : null}
            {detail.groupLabel &&
            detail.groupLabel !== LEGACY_UNASSIGNED_GROUP &&
            detail.groupLabel !== 'Senza Life Area' ? (
              <section
                className="timeline-event-modal__life-area"
                aria-label="Life Area"
              >
                <h4>Life Area</h4>
                <p className="timeline-event-modal__group">
                  <span
                    className="timeline-event-modal__life-area-dot"
                    aria-hidden="true"
                  />
                  {detail.groupLabel}
                </p>
              </section>
            ) : null}
            {sessionSubject?.kind === 'occurrence' ? (
              <TimelineInspectorOccurrenceSession
                occurrenceRef={sessionSubject.ref}
                label={detail.title}
              />
            ) : null}
            {detail.ownerKind === 'event' && detail.eventRef ? (
              <>
                {detail.eventPlacement ? (
                  <EventInspectorActions
                    toolbarTarget={toolbarTarget}
                    eventRef={detail.eventRef}
                    occurrenceRef={detail.occurrenceRef ?? null}
                    placement={detail.eventPlacement}
                    onCancelScope={onClose}
                    onDuplicate={(seed) => {
                      onClose();
                      requestTemporalCreateDuplicate(seed);
                    }}
                  />
                ) : null}
              </>
            ) : null}
            {detail.ownerKind === undefined ? (
              <div className="timeline-event-ai-note">
                {t(($) => $.common.home.timeline.detail.aiNote)}
              </div>
            ) : null}
            {reminderScheduleRef === null ? null : (
              <ScheduleReminderControls
                key={reminderScheduleRef}
                scheduleRef={reminderScheduleRef}
                hideWhenAbsent
              />
            )}
            {detail.realitySubject === undefined ? null : (
              <TimelineInspectorReality
                kind={detail.realitySubject.kind}
                subjectRef={detail.realitySubject.ref}
              />
            )}
            {activityRef &&
            activityDescription?.ref === activityRef &&
            activityDescription.value?.trim() ? (
              <section
                className="timeline-event-modal__description"
                aria-label="Descrizione"
              >
                <h4>Descrizione</h4>
                <p>{activityDescription.value}</p>
              </section>
            ) : null}
            {detail.ownerKind === 'event' && detail.eventRef ? (
              <TimelineEventAgendaEditor
                eventRef={detail.eventRef}
                {...(detail.occurrenceRef
                  ? { occurrenceRef: detail.occurrenceRef }
                  : {})}
                readOnly={detail.occurrenceRef !== undefined}
                hideWhenEmpty
                showDescription
              />
            ) : null}
            {responsibilitySubject === null ? null : (
              <div className="timeline-event-modal__actions">
                <ResponsibilityControls
                  kind={responsibilitySubject.kind}
                  subjectRef={responsibilitySubject.ref}
                  hideWhenEmpty
                />
              </div>
            )}
          </>
        )}
        {activityEditChoice ? (
          <RecurringEditScopeDialog
            subjectLabel="attività"
            selectedHasFacts={activityEditChoice.selectedHasFacts}
            onOnlyThis={() => {
              setActivityEditScope('only_this');
              setEditingProfile(activityEditChoice.profile);
              setActivityEditChoice(null);
            }}
            onFollowing={() => {
              setActivityEditScope(
                activityEditChoice.selectedHasFacts
                  ? 'from_next'
                  : 'this_and_following',
              );
              setEditingProfile(activityEditChoice.profile);
              setActivityEditChoice(null);
            }}
            onCancel={() => {
              setActivityEditChoice(null);
              onClose();
            }}
          />
        ) : null}
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
      aria-hidden={!visible}
    >
      <span>{message}</span>
      <button type="button" onClick={onUndo} tabIndex={visible ? 0 : -1}>
        {t(($) => $.common.home.timeline.undo)}
      </button>
    </div>
  );
}

export function detailFromEvent(
  event: TimelineEvent,
  groups: readonly TimelineGroup[],
  dateKey?: string,
): TimelineDetail {
  const group = groups.find((candidate) => candidate.id === event.groupId);
  const ownerKind =
    event.canonicalBasis?.kind === 'scheduled-event'
      ? ('event' as const)
      : event.canonicalBasis?.kind === 'scheduled-occurrence' &&
          event.canonicalBasis.sourceKind === 'event'
        ? ('event' as const)
        : event.canonicalBasis?.kind === 'scheduled-activity'
          ? ('activity' as const)
          : undefined;
  const eventRef =
    event.canonicalBasis?.kind === 'scheduled-event'
      ? event.canonicalBasis.eventRef
      : event.canonicalBasis?.kind === 'scheduled-occurrence' &&
          event.canonicalBasis.sourceKind === 'event'
        ? event.canonicalBasis.sourceNativeRef
        : undefined;
  const realitySubject =
    event.canonicalBasis?.kind === 'scheduled-activity'
      ? Object.freeze({
          kind: 'activity' as const,
          ref: event.canonicalBasis.activityRef,
        })
      : event.canonicalBasis?.kind === 'scheduled-event'
        ? Object.freeze({
            kind: 'event' as const,
            ref: event.canonicalBasis.eventRef,
          })
        : event.canonicalBasis?.kind === 'scheduled-occurrence'
          ? Object.freeze({
              kind: 'occurrence' as const,
              ref: event.canonicalBasis.occurrenceRef,
            })
          : undefined;
  const base: TimelineDetail = {
    title: event.title,
    startMinute: event.startMinute,
    endMinute: event.endMinute,
    groupLabel: group?.label ?? event.groupId,
    ...(dateKey ? { dateKey } : {}),
    ...(group?.colorCode || event.appearanceColorCode
      ? { accentColorCode: group?.colorCode ?? event.appearanceColorCode }
      : {}),
    ...(ownerKind === undefined ? {} : { ownerKind }),
    ...(eventRef === undefined ? {} : { eventRef }),
    ...(event.canonicalBasis?.kind === 'scheduled-occurrence'
      ? { occurrenceRef: event.canonicalBasis.occurrenceRef }
      : {}),
    ...(event.canonicalBasis?.kind === 'scheduled-event' ||
    (event.canonicalBasis?.kind === 'scheduled-occurrence' &&
      event.canonicalBasis.sourceKind === 'event')
      ? { eventPlacement: event.canonicalBasis.placement }
      : {}),
    ...(event.canonicalBasis
      ? { schedulePlacement: event.canonicalBasis.placement }
      : {}),
    ...(realitySubject === undefined ? {} : { realitySubject }),
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
  dateKey?: string,
): TimelineDetail {
  const group = groups.find((candidate) => candidate.id === event.groupId);
  return {
    title: subitem,
    startMinute: event.startMinute,
    endMinute: event.endMinute,
    groupLabel: group?.label ?? event.groupId,
    contextLabel: `${parentLabel} ${event.title}`,
    ...(dateKey ? { dateKey } : {}),
    ...(group?.colorCode || event.appearanceColorCode
      ? { accentColorCode: group?.colorCode ?? event.appearanceColorCode }
      : {}),
  };
}

export function parseCalendarDateKey(value: string): PlainDate {
  return parseTimelineDate(value);
}
