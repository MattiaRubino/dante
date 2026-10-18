import { Temporal } from '@dante/time';
import { type CSSProperties, useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { createRemoteTemporalOccurrenceScheduleDataSource } from '../../../temporal/remote-occurrence-schedule-data-source';
import { ActivitySessionCardControls } from '../../../temporal/activity-session-card-controls';
import { SessionSubjectControls } from '../../../temporal/session-subject-controls';
import { invalidateTemporalTimelineRead } from '../../../temporal/timeline-invalidation';
import { useTimelineDateLaneDetails } from './timeline-date-lane-details';
import {
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
  timelineAllDayRangePosition,
  TIMELINE_ALL_DAY_VISIBLE_ROWS,
} from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineCoarsePeriod,
  TimelineGroup,
  TimelineGroupId,
} from './model/timeline-types';

import './timeline-all-day-layer.css';

type TimelineAllDayLaneProps = Readonly<{
  dateKey: string;
  todayKey?: string;
  items: readonly TimelineAllDayItem[];
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
  onOpenItemDetail?: (item: TimelineAllDayItem, opener: HTMLElement) => void;
}>;

function coarsePeriodLabel(
  period: TimelineCoarsePeriod,
  language: string,
): string {
  const english = language.toLowerCase().startsWith('en');
  if (english) {
    return {
      morning: 'Morning',
      afternoon: 'Afternoon',
      evening: 'Evening',
    }[period];
  }
  return {
    morning: 'Mattina',
    afternoon: 'Pomeriggio',
    evening: 'Sera',
  }[period];
}

function itemOrganizationKey(item: TimelineAllDayItem): string | null {
  const basis = item.canonicalBasis;
  if (!basis) return null;
  if (basis.kind === 'scheduled-activity') {
    return `activity:${basis.activityRef}`;
  }
  if (basis.kind === 'scheduled-event') {
    return `event:${basis.eventRef}`;
  }
  return `${basis.sourceKind}:${basis.sourceNativeRef}`;
}

function requestedOccurrencePlacement(
  dateKey: string,
  suggestedStartTime: string | undefined,
  english: boolean,
) {
  const startValue = window.prompt(
    english ? 'Start time (HH:MM)' : 'Ora di inizio (HH:MM)',
    suggestedStartTime ?? '',
  );
  if (startValue === null) return null;

  let startTime: Temporal.PlainTime;
  try {
    startTime = Temporal.PlainTime.from(startValue.trim());
  } catch {
    window.alert(
      english
        ? 'Enter a valid time (HH:MM).'
        : 'Inserisci un orario valido (HH:MM).',
    );
    return null;
  }

  const durationValue = window.prompt(
    english
      ? 'Duration in minutes (required)'
      : 'Durata in minuti (obbligatoria)',
    '',
  );
  if (durationValue === null) return null;
  const durationMinutes = Number(durationValue.trim());
  if (
    !Number.isInteger(durationMinutes) ||
    durationMinutes < 5 ||
    durationMinutes > 10080
  ) {
    window.alert(
      english
        ? 'Enter a duration from 5 to 10080 minutes.'
        : 'Inserisci una durata da 5 a 10080 minuti.',
    );
    return null;
  }

  const startsLocalAt =
    Temporal.PlainDate.from(dateKey).toPlainDateTime(startTime);
  return Object.freeze({
    kind: 'floating-local-interval' as const,
    startsLocalAt,
    endsLocalAt: startsLocalAt.add({ minutes: durationMinutes }),
  });
}

export function TimelineAllDayLane({
  dateKey,
  todayKey,
  items,
  groups,
  filters,
  onOpenItemDetail,
}: TimelineAllDayLaneProps) {
  const { t, i18n } = useTranslation('common');
  const occurrenceScheduleSource = useMemo(
    () => createRemoteTemporalOccurrenceScheduleDataSource(),
    [],
  );
  const [pendingOccurrenceRef, setPendingOccurrenceRef] = useState<
    string | null
  >(null);
  const [showOverflow, setShowOverflow] = useState(false);
  const [clockMs, setClockMs] = useState(() => Date.now());
  const visibleItems = useMemo(
    () => timelineAllDayItemsForVisibleDate(items, filters, dateKey),
    [dateKey, filters, items],
  );
  const groupMap = useMemo(
    () => new Map(groups.map((group) => [group.id, group])),
    [groups],
  );
  const detailsBySubject = useTimelineDateLaneDetails(visibleItems);

  const ticking = visibleItems.some(
    (item) => dateKey === todayKey && item.mainSession?.state === 'running',
  );
  useEffect(() => {
    if (!ticking) return;
    const timer = window.setInterval(() => setClockMs(Date.now()), 1000);
    return () => window.clearInterval(timer);
  }, [ticking]);

  if (visibleItems.length === 0) {
    return null;
  }

  const language = i18n.resolvedLanguage ?? i18n.language;
  const english = language.toLowerCase().startsWith('en');
  const laneLabels = new Set(
    visibleItems.map((item) => {
      switch (item.laneKind ?? 'all-day') {
        case 'multi-day':
          return english ? 'Multiple days' : 'Su più giorni';
        case 'coarse':
          return english ? 'Period' : 'Fascia';
        case 'expectation':
          return t(($) => $.common.home.timeline.create.timeSemantics.expected);
        case 'flexible':
          return t(($) => $.common.home.timeline.create.timeSemantics.flexible);
        case 'all-day':
          return t(($) => $.common.home.timeline.create.timeSemantics.allDay);
      }
    }),
  );
  const laneLabel = [...laneLabels].join(' · ');
  const laneHeight = timelineAllDayLaneHeightPx(visibleItems.length);
  const formatDay = (value: string) =>
    new Intl.DateTimeFormat(language, {
      day: 'numeric',
      month: 'short',
      timeZone: 'UTC',
    }).format(new Date(`${value}T12:00:00Z`));
  const formatDuration = (seconds: number) => {
    const value = Math.max(0, Math.floor(seconds));
    return `${Math.floor(value / 3600)}:${String(Math.floor((value % 3600) / 60)).padStart(2, '0')}:${String(value % 60).padStart(2, '0')}`;
  };

  const scheduleOccurrence = async (item: TimelineAllDayItem) => {
    const occurrence = item.occurrenceBasis;
    if (occurrence === undefined || pendingOccurrenceRef !== null) return;
    const placement = requestedOccurrencePlacement(
      dateKey,
      occurrence.suggestedStartTime,
      english,
    );
    if (placement === null) return;

    setPendingOccurrenceRef(occurrence.occurrenceRef);
    try {
      await occurrenceScheduleSource.establish({
        operationId: `timeline-occurrence-schedule:${crypto.randomUUID()}`,
        occurrenceRef: occurrence.occurrenceRef,
        placement,
      });
      // Never patch expected -> scheduled locally. The authoritative checkpoint/read
      // path applies scheduled-over-expected precedence and returns the one canonical item.
      invalidateTemporalTimelineRead();
    } catch {
      window.alert(
        english
          ? 'The occurrence could not be scheduled. Refresh and try again.'
          : 'Non è stato possibile pianificare l’occorrenza. Aggiorna e riprova.',
      );
    } finally {
      setPendingOccurrenceRef(null);
    }
  };

  const renderItem = (item: TimelineAllDayItem) => {
    const group = groupMap.get(item.groupId);
    const basis = item.canonicalBasis;
    const details =
      basis?.kind === 'scheduled-activity'
        ? detailsBySubject.get(`activity:${basis.activityRef}`)
        : basis?.kind === 'scheduled-event'
          ? detailsBySubject.get(`event:${basis.eventRef}`)
          : undefined;
    const areaLabel = details
      ? details.lifeAreaRef === null
        ? null
        : groups.find((candidate) => candidate.id === details.lifeAreaRef)
            ?.label
      : group?.label;
    const tone = item.appearanceTone ?? group?.tone ?? 'personal';
    const organizationKey = itemOrganizationKey(item);
    const itemColorCode =
      item.appearanceColorCode ??
      (organizationKey === null
        ? undefined
        : group?.itemColorCodes?.[organizationKey]);
    const itemStyle: CSSProperties & {
      '--timeline-group-color'?: string;
    } = itemColorCode ? { '--timeline-group-color': itemColorCode } : {};
    const position = timelineAllDayRangePosition(item, dateKey);
    const startsHere = position === 'single' || position === 'start';
    const endsHere = position === 'single' || position === 'end';
    const laneKind = item.laneKind ?? 'all-day';
    const precisionLabel =
      laneKind === 'coarse' && item.coarsePeriod !== undefined
        ? coarsePeriodLabel(item.coarsePeriod, language)
        : laneKind === 'multi-day'
          ? english
            ? 'Multiple days'
            : 'Su più giorni'
          : laneKind === 'expectation'
            ? t(($) => $.common.home.timeline.create.timeSemantics.expected)
            : laneKind === 'flexible'
              ? t(($) => $.common.home.timeline.create.timeSemantics.flexible)
              : t(($) => $.common.home.timeline.create.timeSemantics.allDay);
    const occurrencePending =
      item.occurrenceBasis?.occurrenceRef === pendingOccurrenceRef;
    const scheduleLabel = occurrencePending
      ? english
        ? 'Scheduling…'
        : 'Pianificazione…'
      : english
        ? 'Schedule'
        : 'Pianifica';

    const plannedEnd = Temporal.PlainDate.from(
      item.plannedEndDateExclusiveKey ?? item.endDateExclusiveKey,
    )
      .subtract({ days: 1 })
      .toString();
    const period =
      item.startDateKey === plannedEnd
        ? formatDay(item.startDateKey)
        : `${formatDay(item.startDateKey)}–${formatDay(plannedEnd)}`;
    const plannedTime =
      laneKind === 'multi-day'
        ? ` · ${item.plannedStartTime ?? ''} → ${item.plannedEndTime ?? ''}`
        : '';
    const main = item.mainSession;
    const showRuntime = dateKey === todayKey && main?.state !== 'ended';
    const showStatus =
      main && (main.state === 'ended' ? endsHere : dateKey === todayKey);
    const seconds = main
      ? main.activeSeconds +
        (main.state === 'running'
          ? Math.max(0, (clockMs - Date.parse(main.evaluatedAt)) / 1000)
          : 0)
      : 0;
    const sessionStatus =
      main?.state === 'ended'
        ? `${english ? 'Stopped' : 'Conclusa'} ${new Intl.DateTimeFormat(language, { hour: '2-digit', minute: '2-digit' }).format(new Date(main.endedAt ?? main.startedAt))} · ${formatDuration(seconds)}`
        : `${main?.state === 'paused' ? '⏸' : '▶'} ${formatDuration(seconds)}`;
    return (
      <div className="timeline-all-day-item-row" key={item.id}>
        <button
          className="timeline-all-day-item"
          type="button"
          data-timeline-all-day-item={item.id}
          data-timeline-date-lane-kind={laneKind}
          data-temporal-create-projection={
            item.origin === 'create' ? item.id : undefined
          }
          data-timeline-tone={tone}
          data-range-position={position}
          data-range-start={startsHere || undefined}
          data-range-end={endsHere || undefined}
          style={itemStyle}
          aria-label={`${item.title} · ${precisionLabel} · ${group?.label ?? item.groupId}`}
          onClick={(event) => onOpenItemDetail?.(item, event.currentTarget)}
          onKeyDown={(event) => {
            if (event.key === 'Enter' && onOpenItemDetail) {
              event.preventDefault();
              onOpenItemDetail(item, event.currentTarget);
            }
          }}
        >
          <span
            className="timeline-all-day-item__continuation"
            aria-hidden="true"
          >
            {startsHere ? '' : '‹'}
          </span>
          <strong>{item.title}</strong>
          <span className="timeline-all-day-item__meta">
            {precisionLabel} · {period}
            {plannedTime}
            {areaLabel ? ` · ${areaLabel}` : ''}
            {item.meta ? ` · ${item.meta}` : ''}
          </span>
          {details && (details.sessions > 0 || details.objectives > 0) ? (
            <span className="timeline-all-day-item__indicators">
              {details.sessions > 0 ? (
                <span title={`${details.sessions} sessioni pianificate`}>
                  S {details.sessions}
                </span>
              ) : null}
              {details.objectives > 0 ? (
                <span title={`${details.objectives} obiettivi`}>
                  O {details.objectives}
                </span>
              ) : null}
            </span>
          ) : null}
          {showStatus ? (
            <span
              className="timeline-all-day-item__session-state"
              title={sessionStatus}
            >
              {sessionStatus}
            </span>
          ) : null}
          <span
            className="timeline-all-day-item__continuation"
            aria-hidden="true"
          >
            {endsHere ? '' : '›'}
          </span>
        </button>
        {item.canonicalBasis?.kind === 'scheduled-activity' && showRuntime ? (
          <ActivitySessionCardControls
            activityRef={item.canonicalBasis.activityRef}
            label={item.title}
            showPlanned={false}
          />
        ) : dateKey === todayKey &&
          (item.canonicalBasis?.kind === 'scheduled-occurrence' ||
            item.occurrenceBasis !== undefined) ? (
          <SessionSubjectControls
            kind="occurrence"
            subjectRef={
              item.canonicalBasis?.kind === 'scheduled-occurrence'
                ? item.canonicalBasis.occurrenceRef
                : (item.occurrenceBasis?.occurrenceRef ?? '')
            }
            label={item.title}
          />
        ) : null}
        {item.occurrenceBasis !== undefined ? (
          <button
            className="timeline-all-day-item__schedule"
            type="button"
            disabled={pendingOccurrenceRef !== null}
            data-timeline-schedule-occurrence={
              item.occurrenceBasis.occurrenceRef
            }
            aria-label={`${scheduleLabel} · ${item.title}`}
            onClick={() => void scheduleOccurrence(item)}
          >
            {scheduleLabel}
          </button>
        ) : null}
      </div>
    );
  };

  return (
    <section
      className="timeline-all-day-lane"
      data-timeline-all-day-lane={dateKey}
      aria-label={laneLabel}
      style={
        {
          height: laneHeight,
          '--timeline-all-day-lane-height': `${laneHeight}px`,
        } as CSSProperties
      }
    >
      <div className="timeline-all-day-lane__label">
        <span>
          {formatDay(dateKey)} · {laneLabel}
        </span>
        {visibleItems.length > TIMELINE_ALL_DAY_VISIBLE_ROWS ? (
          <button
            type="button"
            aria-expanded={showOverflow}
            onClick={() => setShowOverflow((value) => !value)}
          >
            + {visibleItems.length - TIMELINE_ALL_DAY_VISIBLE_ROWS}
          </button>
        ) : null}
      </div>
      <div className="timeline-all-day-lane__items">
        {visibleItems.slice(0, TIMELINE_ALL_DAY_VISIBLE_ROWS).map(renderItem)}
      </div>
      {showOverflow ? (
        <div
          className="timeline-all-day-lane__overflow"
          aria-label={english ? 'More date bars' : 'Altre barre'}
        >
          {visibleItems.slice(TIMELINE_ALL_DAY_VISIBLE_ROWS).map(renderItem)}
        </div>
      ) : null}
    </section>
  );
}
