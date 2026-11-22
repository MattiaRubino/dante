import { Temporal } from '@dante/time';
import { type CSSProperties, useId, useMemo, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { formatDateWithCapitalizedMonth } from '../../../../platform/format-localized-date';

import { createRemoteTemporalOccurrenceScheduleDataSource } from '../../../temporal/remote-occurrence-schedule-data-source';
import { ActivitySessionCardControls } from '../../../temporal/activity-session-card-controls';
import { SessionSubjectControls } from '../../../temporal/session-subject-controls';
import { TemporalKindMarker } from '../../../temporal-create/ui/temporal-kind-marker';
import { invalidateTemporalTimelineRead } from '../../../temporal/timeline-invalidation';
import {
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
  timelineAllDayRangePosition,
  TIMELINE_ALL_DAY_VISIBLE_ROWS,
} from './model/timeline-all-day-layout';
import { timelineCardIdentity } from './model/timeline-card-identity';
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
  onOpenItemDetail?: (
    item: TimelineAllDayItem,
    opener: HTMLElement,
    point?: Readonly<{ clientX: number; clientY: number }>,
  ) => void;
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
  const overflowId = useId();
  const overflowTriggerRef = useRef<HTMLButtonElement | null>(null);
  const visibleItems = useMemo(() => {
    const filtered = timelineAllDayItemsForVisibleDate(items, filters, dateKey);
    if (dateKey !== todayKey) return filtered;
    // A main Session that can be acted on must not be hidden in +N merely
    // because its plan arrived after two ordinary all-day entries.
    const priority = (item: TimelineAllDayItem) =>
      item.mainSession?.state === 'running'
        ? 0
        : item.mainSession?.state === 'paused'
          ? 1
          : 2;
    return [...filtered].sort((left, right) => priority(left) - priority(right));
  }, [dateKey, filters, items, todayKey]);
  const groupMap = useMemo(
    () => new Map(groups.map((group) => [group.id, group])),
    [groups],
  );
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
    formatDateWithCapitalizedMonth(
      new Intl.DateTimeFormat(language, {
        day: 'numeric',
        month: 'short',
        timeZone: 'UTC',
      }),
      new Date(`${value}T12:00:00Z`),
    );
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
    const identity = timelineCardIdentity(
      basis,
      item.occurrenceBasis?.sourceKind,
    );
    const kindLabel =
      identity.kind === 'activity'
        ? english
          ? 'Activity'
          : 'Attività'
        : english
          ? 'Event'
          : 'Evento';
    const recurringLabel = english
      ? 'Recurring instance'
      : 'Istanza ricorrente';
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
    // The date lane is only a compact navigator. Session durations, status,
    // planned children and Objectives belong to the dedicated surfaces.
    const compactPeriod =
      laneKind === 'all-day' || laneKind === 'multi-day'
        ? `${period}${plannedTime}`
        : `${precisionLabel} · ${period}`;
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
          data-timeline-kind={identity.kind}
          data-recurring-instance={
            identity.recurringInstance ? 'true' : 'false'
          }
          data-range-position={position}
          data-range-start={startsHere || undefined}
          data-range-end={endsHere || undefined}
          style={itemStyle}
          aria-label={`${kindLabel}${identity.recurringInstance ? `, ${recurringLabel}` : ''}: ${item.title} · ${precisionLabel} · ${group?.label ?? item.groupId}`}
          onClick={(event) =>
            onOpenItemDetail?.(
              item,
              event.currentTarget,
              event.detail > 0
                ? { clientX: event.clientX, clientY: event.clientY }
                : undefined,
            )
          }
        >
          <span
            className="timeline-all-day-item__continuation"
            aria-hidden="true"
          >
            {startsHere ? '' : '‹'}
          </span>
          <strong className="timeline-all-day-item__identity">
            <TemporalKindMarker kind={identity.kind} />
            <span className="timeline-all-day-item__title">{item.title}</span>
          </strong>
          <span className="timeline-all-day-item__meta" title={compactPeriod}>
            {compactPeriod}
          </span>
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
            variant="card"
            compactRuntime
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
            ref={overflowTriggerRef}
            type="button"
            aria-expanded={showOverflow}
            aria-controls={showOverflow ? overflowId : undefined}
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
          id={overflowId}
          className="timeline-all-day-lane__overflow"
          role="region"
          aria-label={english ? 'More date bars' : 'Altre barre'}
          onKeyDown={(event) => {
            if (event.key === 'Escape') {
              event.stopPropagation();
              setShowOverflow(false);
              overflowTriggerRef.current?.focus();
            }
          }}
        >
          {visibleItems.slice(TIMELINE_ALL_DAY_VISIBLE_ROWS).map(renderItem)}
        </div>
      ) : null}
    </section>
  );
}
