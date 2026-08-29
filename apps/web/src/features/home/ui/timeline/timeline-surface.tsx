import type { CSSProperties } from 'react';
import { useTranslation } from 'react-i18next';

import {
  buildIsoWeek,
  formatTimelineMinute,
  parseTimelineDate,
} from './model/timeline-temporal';

type TimelineSurfaceProps = {
  expanded: boolean;
  onToggleExpanded: () => void;
};

const MATERIALIZED_VIEW_DATE = parseTimelineDate('2026-08-28');
const MATERIALIZED_NOW_MINUTE = 15 * 60;
const HOURS = ['00', '03', '06', '09', '12', '15', '18', '21', '24'] as const;
const GROUPS = [
  ['Focus', '#8a74ff'],
  ['Riunioni', '#27d9f5'],
  ['Salute', '#8bdc47'],
  ['Creatività', '#ffad34'],
] as const;
const EVENTS = [
  {
    className: 'timeline-event-focus',
    time: '09:30 – 11:15',
    title: 'Revisione concept',
    meta: 'Focus',
    color: '#8a74ff',
  },
  {
    className: 'timeline-event-call',
    time: '12:10 – 13:00',
    title: 'Call progetto',
    meta: 'Riunioni',
    color: '#27d9f5',
  },
  {
    className: 'timeline-event-health',
    time: '16:20 – 17:00',
    title: 'Allenamento',
    meta: 'Salute',
    color: '#8bdc47',
  },
  {
    className: 'timeline-event-creative',
    time: '18:40 – 20:00',
    title: 'Uscita fotografica',
    meta: 'Creatività',
    color: '#ffad34',
  },
] as const;

function TimelineIcon({
  type,
}: {
  type: 'calendar' | 'filter' | 'group' | 'zoom-out' | 'zoom-in';
}) {
  switch (type) {
    case 'calendar':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M7 3v3M17 3v3M4 8h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Z" />
        </svg>
      );
    case 'filter':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <path d="M4 6h16M7 12h10M10 18h4" />
        </svg>
      );
    case 'group':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="5" width="16" height="5" rx="2" />
          <rect x="4" y="14" width="10" height="5" rx="2" />
        </svg>
      );
    case 'zoom-out':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="10.5" cy="10.5" r="6" />
          <path d="M7.5 10.5h6M15 15l5 5" />
        </svg>
      );
    case 'zoom-in':
      return (
        <svg viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="10.5" cy="10.5" r="6" />
          <path d="M7.5 10.5h6M10.5 7.5v6M15 15l5 5" />
        </svg>
      );
  }
}

export function TimelineSurface({
  expanded,
  onToggleExpanded,
}: TimelineSurfaceProps) {
  const { t, i18n } = useTranslation('common');
  const locale = i18n.resolvedLanguage ?? i18n.language;
  const week = buildIsoWeek(MATERIALIZED_VIEW_DATE);
  const monthLabel = MATERIALIZED_VIEW_DATE.toLocaleString(locale, {
    month: 'long',
  }).toLocaleUpperCase(locale);

  return (
    <section
      className="home-timeline"
      data-home-region="timeline"
      data-home-timeline-state={expanded ? 'expanded' : 'normal'}
      aria-label={t(($) => $.common.home.timeline.label)}
    >
      <header className="home-timeline-head">
        <div className="home-timeline-primary-controls">
          <button
            className="home-timeline-quick-add"
            type="button"
            disabled
            aria-label="Aggiungi alla timeline"
          >
            +
          </button>
          <button
            className="home-timeline-month"
            type="button"
            disabled
            aria-label="Apri calendario"
          >
            <TimelineIcon type="calendar" />
            <span>
              <small>{monthLabel}</small>
              <strong>{MATERIALIZED_VIEW_DATE.year}</strong>
            </span>
          </button>
          <button
            className="home-timeline-now"
            type="button"
            disabled
            aria-label="Torna a ora"
          >
            <span className="home-timeline-now-dot" aria-hidden="true" />
            Ora
          </button>
        </div>
        <div className="home-timeline-week" aria-label="Settimana corrente">
          {week.map((date) => (
            <span
              className={date.equals(MATERIALIZED_VIEW_DATE) ? 'is-active' : ''}
              key={date.toString()}
            >
              <small>
                {date.toLocaleString(locale, { weekday: 'narrow' })}
              </small>
              <strong>{date.day}</strong>
            </span>
          ))}
        </div>
        <div className="home-timeline-actions">
          <button type="button" disabled aria-label="Filtri timeline">
            <TimelineIcon type="filter" />
          </button>
          <button type="button" disabled aria-label="Gruppi timeline">
            <TimelineIcon type="group" />
          </button>
          <button type="button" disabled aria-label="Riduci zoom">
            <TimelineIcon type="zoom-out" />
          </button>
          <button type="button" disabled aria-label="Aumenta zoom">
            <TimelineIcon type="zoom-in" />
          </button>
        </div>
        <div className="home-timeline-groups" aria-label="Gruppi visibili">
          {GROUPS.map(([name, color]) => (
            <span
              key={name}
              style={{ '--group-color': color } as CSSProperties}
            >
              <i aria-hidden="true" />
              {name}
            </span>
          ))}
        </div>
      </header>
      <div className="home-timeline-frame">
        <div className="home-timeline-ruler" aria-hidden="true">
          {HOURS.map((hour) => (
            <span key={hour}>{hour}:00</span>
          ))}
        </div>
        <div className="home-timeline-grid">
          <span className="home-timeline-now-line" aria-hidden="true">
            <i>{formatTimelineMinute(MATERIALIZED_NOW_MINUTE)}</i>
          </span>
          {EVENTS.map((event) => (
            <article
              className={`home-timeline-event ${event.className}`}
              key={event.title}
              style={{ '--event-color': event.color } as CSSProperties}
            >
              <time>{event.time}</time>
              <strong>{event.title}</strong>
              <span>{event.meta}</span>
            </article>
          ))}
        </div>
      </div>
      <button
        className="home-timeline-expand-handle"
        type="button"
        onClick={onToggleExpanded}
        aria-label={t(($) =>
          expanded
            ? $.common.home.timeline.collapse
            : $.common.home.timeline.expand,
        )}
        aria-pressed={expanded}
      >
        <span aria-hidden="true">{expanded ? '‹' : '›'}</span>
      </button>
    </section>
  );
}
