import type { PlainDate } from '@dante/time';
import {
  type CSSProperties,
  type DragEvent,
  type KeyboardEvent,
  type RefObject,
  useRef,
  useState,
} from 'react';
import { useTranslation } from 'react-i18next';

import './timeline-material.css';
import './timeline-reference-lock.css';

import {
  addTimelineDays,
  buildIsoWeek,
  isSameTimelineDate,
  timelineDateKey,
} from './model/timeline-temporal';
import type { TimelineGroup, TimelineGroupId } from './model/timeline-types';
import { TimelineCreateBridge } from './timeline-create-bridge';

function displayDate(date: PlainDate): Date {
  return new Date(Date.UTC(date.year, date.month - 1, date.day, 12));
}

function monthLabel(date: PlainDate, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    month: 'long',
    timeZone: 'UTC',
  }).format(displayDate(date));
}

function weekdayLabel(date: PlainDate, locale: string): string {
  return new Intl.DateTimeFormat(locale, {
    weekday: 'short',
    timeZone: 'UTC',
  })
    .format(displayDate(date))
    .replace('.', '')
    .slice(0, 2)
    .toLocaleUpperCase(locale);
}

function TimelineIcon({ type }: { type: 'view' | 'group' | 'reset' }) {
  switch (type) {
    case 'view':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M5 6h14M5 12h14M5 18h14" />
          <path d="M8 4v4M15 10v4M11 16v4" />
        </svg>
      );
    case 'group':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="5" width="16" height="5" rx="2" />
          <rect x="4" y="14" width="10" height="5" rx="2" />
        </svg>
      );
    case 'reset':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4.5 9A8 8 0 1 1 6 17" />
          <path d="M4 4v5h5" />
        </svg>
      );
  }
}

type TimelineHeaderProps = Readonly<{
  locale: string;
  today: PlainDate;
  viewDate: PlainDate;
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
  nowNeeded: boolean;
  split: boolean;
  calendarOpen: boolean;
  viewOptionsOpen: boolean;
  calendarTriggerRef: RefObject<HTMLButtonElement | null>;
  viewOptionsTriggerRef: RefObject<HTMLButtonElement | null>;
  groupScrollerRef: RefObject<HTMLDivElement | null>;
  onCalendarToggle: () => void;
  onDateSelect: (date: PlainDate) => void;
  onGoNow: () => void;
  onViewOptionsToggle: () => void;
  onSplitToggle: () => void;
  onResetGroupsFocus: () => void;
  onToggleFilter: (groupId: TimelineGroupId) => void;
  onReorderGroup: (groupId: TimelineGroupId, targetIndex: number) => void;
  onGroupScroll: (scrollLeft: number) => void;
}>;

export function TimelineHeader({
  locale,
  today,
  viewDate,
  groups,
  filters,
  nowNeeded,
  split,
  calendarOpen,
  viewOptionsOpen,
  calendarTriggerRef,
  viewOptionsTriggerRef,
  groupScrollerRef,
  onCalendarToggle,
  onDateSelect,
  onGoNow,
  onViewOptionsToggle,
  onSplitToggle,
  onResetGroupsFocus,
  onToggleFilter,
  onReorderGroup,
  onGroupScroll,
}: TimelineHeaderProps) {
  const { t } = useTranslation('common');
  const week = buildIsoWeek(viewDate);
  const [draggingGroupId, setDraggingGroupId] =
    useState<TimelineGroupId | null>(null);
  const [dropTargetId, setDropTargetId] = useState<TimelineGroupId | null>(
    null,
  );
  const suppressFilterClickRef = useRef(false);

  const reorderFromDrop = (
    event: DragEvent<HTMLButtonElement>,
    targetGroupId: TimelineGroupId,
  ) => {
    event.preventDefault();
    const sourceId = draggingGroupId;
    setDropTargetId(null);
    setDraggingGroupId(null);
    if (!sourceId || sourceId === targetGroupId) {
      return;
    }
    const targetIndex = groups.findIndex((group) => group.id === targetGroupId);
    if (targetIndex >= 0) {
      onReorderGroup(sourceId, targetIndex);
    }
  };

  const reorderFromKeyboard = (
    event: KeyboardEvent<HTMLButtonElement>,
    groupId: TimelineGroupId,
  ) => {
    if (!event.altKey || !['ArrowLeft', 'ArrowRight'].includes(event.key)) {
      return;
    }
    const currentIndex = groups.findIndex((group) => group.id === groupId);
    if (currentIndex < 0) {
      return;
    }
    const delta = event.key === 'ArrowRight' ? 1 : -1;
    const targetIndex = Math.max(
      0,
      Math.min(groups.length - 1, currentIndex + delta),
    );
    if (targetIndex === currentIndex) {
      return;
    }
    event.preventDefault();
    onReorderGroup(groupId, targetIndex);
  };

  const hasGroupFocus = filters.size > 0;
  const groupTrackStyle = {
    '--timeline-group-count': groups.length,
  } as CSSProperties;
  const previousWeekDate = addTimelineDays(viewDate, -7);
  const nextWeekDate = addTimelineDays(viewDate, 7);

  return (
    <header className="dante-timeline-header">
      <div className="dante-timeline-header-row">
        <TimelineCreateBridge
          defaultDate={viewDate}
          groups={groups}
          filters={filters}
          onRevealDate={onDateSelect}
          onBeforeOpen={() => {
            if (calendarOpen) {
              onCalendarToggle();
            }
            if (viewOptionsOpen) {
              onViewOptionsToggle();
            }
          }}
        />

        <button
          ref={calendarTriggerRef}
          className="dante-timeline-month"
          type="button"
          onClick={onCalendarToggle}
          aria-label={t(($) => $.common.home.timeline.calendar.open)}
          aria-haspopup="dialog"
          aria-expanded={calendarOpen}
        >
          <span>
            {monthLabel(viewDate, locale)} {viewDate.year}
          </span>
          <i aria-hidden="true">▾</i>
        </button>

        <button
          className={`dante-timeline-now${nowNeeded ? ' is-needed' : ''}`}
          type="button"
          onClick={onGoNow}
          aria-label={t(($) =>
            nowNeeded
              ? $.common.home.timeline.now.go
              : $.common.home.timeline.now.visible,
          )}
        >
          <span className="dante-timeline-now-dot" aria-hidden="true" />
          {t(($) => $.common.home.timeline.now.label)}
        </button>

        <div className="dante-timeline-week-nav">
          <button
            className="dante-timeline-week-step"
            type="button"
            onClick={() => onDateSelect(previousWeekDate)}
            aria-label={`${t(($) => $.common.home.timeline.calendar.previousPeriod)} · ${previousWeekDate.toLocaleString(
              locale,
              {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
              },
            )}`}
          >
            ‹
          </button>
          <div
            className="dante-timeline-week"
            role="group"
            aria-label={t(($) => $.common.home.timeline.weekLabel)}
          >
            {week.map((date) => {
              const viewing = isSameTimelineDate(date, viewDate);
              const isToday = isSameTimelineDate(date, today);
              return (
                <button
                  className={`${viewing ? 'is-viewing' : ''}${isToday ? ' is-today' : ''}`}
                  key={timelineDateKey(date)}
                  type="button"
                  onClick={() => onDateSelect(date)}
                  aria-current={viewing ? 'date' : undefined}
                  aria-label={date.toLocaleString(locale, {
                    weekday: 'long',
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                  })}
                >
                  <b>{weekdayLabel(date, locale)}</b>
                  <strong>{date.day}</strong>
                  <span
                    className="dante-timeline-week-mark"
                    aria-hidden="true"
                  />
                </button>
              );
            })}
          </div>
          <button
            className="dante-timeline-week-step"
            type="button"
            onClick={() => onDateSelect(nextWeekDate)}
            aria-label={`${t(($) => $.common.home.timeline.calendar.nextPeriod)} · ${nextWeekDate.toLocaleString(
              locale,
              {
                day: 'numeric',
                month: 'long',
                year: 'numeric',
              },
            )}`}
          >
            ›
          </button>
        </div>

        <div className="dante-timeline-actions">
          <button
            ref={viewOptionsTriggerRef}
            className={viewOptionsOpen ? 'is-active' : ''}
            type="button"
            onClick={onViewOptionsToggle}
            aria-label={t(($) => $.common.home.timeline.viewOptions.label)}
            aria-haspopup="dialog"
            aria-expanded={viewOptionsOpen}
          >
            <TimelineIcon type="view" />
          </button>
          <button
            className={split ? 'is-active' : ''}
            type="button"
            onClick={onSplitToggle}
            aria-label={t(($) =>
              split
                ? $.common.home.timeline.groups.merge
                : $.common.home.timeline.groups.split,
            )}
            aria-pressed={split}
          >
            <TimelineIcon type="group" />
          </button>
        </div>
      </div>

      <div className="dante-timeline-group-row">
        <button
          className={`dante-timeline-group-reset${hasGroupFocus ? ' is-active' : ''}`}
          type="button"
          onClick={onResetGroupsFocus}
          aria-label={t(($) => $.common.home.timeline.groups.reset)}
        >
          <TimelineIcon type="reset" />
        </button>
        <div
          ref={groupScrollerRef}
          className="dante-timeline-group-scroller"
          onScroll={(event) => onGroupScroll(event.currentTarget.scrollLeft)}
        >
          <div className="dante-timeline-group-track" style={groupTrackStyle}>
            {groups.map((group, index) => {
              const active = filters.has(group.id);
              const dimmed = filters.size > 0 && !active;
              return (
                <button
                  className={`dante-timeline-group-chip${active ? ' is-active' : ''}${dimmed ? ' is-dimmed' : ''}${draggingGroupId === group.id ? ' is-reordering' : ''}${dropTargetId === group.id ? ' is-drop-target' : ''}`}
                  data-timeline-tone={group.tone}
                  data-group-id={group.id}
                  key={group.id}
                  type="button"
                  draggable
                  onClick={() => {
                    if (suppressFilterClickRef.current) {
                      suppressFilterClickRef.current = false;
                      return;
                    }
                    onToggleFilter(group.id);
                  }}
                  onKeyDown={(event) => reorderFromKeyboard(event, group.id)}
                  onDragStart={(event) => {
                    suppressFilterClickRef.current = true;
                    setDraggingGroupId(group.id);
                    event.dataTransfer.effectAllowed = 'move';
                    event.dataTransfer.setData('text/plain', group.id);
                  }}
                  onDragOver={(event) => {
                    event.preventDefault();
                    event.dataTransfer.dropEffect = 'move';
                    setDropTargetId(group.id);
                  }}
                  onDragLeave={() => {
                    if (dropTargetId === group.id) {
                      setDropTargetId(null);
                    }
                  }}
                  onDrop={(event) => reorderFromDrop(event, group.id)}
                  onDragEnd={() => {
                    setDraggingGroupId(null);
                    setDropTargetId(null);
                    window.setTimeout(() => {
                      suppressFilterClickRef.current = false;
                    }, 0);
                  }}
                  aria-pressed={active}
                  aria-keyshortcuts="Alt+ArrowLeft Alt+ArrowRight"
                  title={t(($) => $.common.home.timeline.groups.reorderHint)}
                >
                  <span>{group.label}</span>
                  <span className="home-visually-hidden">
                    {t(($) => $.common.home.timeline.groups.position, {
                      position: index + 1,
                      total: groups.length,
                    })}
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </header>
  );
}
