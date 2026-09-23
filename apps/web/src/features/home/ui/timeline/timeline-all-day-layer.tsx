import { Temporal } from '@dante/time';
import { useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { createRemoteTemporalOccurrenceScheduleDataSource } from '../../../temporal/remote-occurrence-schedule-data-source';
import { invalidateTemporalTimelineRead } from '../../../temporal/timeline-invalidation';
import {
  timelineAllDayItemsForVisibleDate,
  timelineAllDayLaneHeightPx,
  timelineAllDayRangePosition,
} from './model/timeline-all-day-layout';
import type {
  TimelineAllDayItem,
  TimelineCoarsePeriod,
  TimelineGroup,
  TimelineGroupId,
} from './model/timeline-types';
import { useTimelineCanonicalActions } from './timeline-canonical-actions';

import './timeline-all-day-layer.css';

type TimelineAllDayLaneProps = Readonly<{
  dateKey: string;
  items: readonly TimelineAllDayItem[];
  groups: readonly TimelineGroup[];
  filters: ReadonlySet<TimelineGroupId>;
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
    window.alert(english ? 'Enter a valid time (HH:MM).' : 'Inserisci un orario valido (HH:MM).');
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

  const startsLocalAt = Temporal.PlainDate.from(dateKey).toPlainDateTime(startTime);
  return Object.freeze({
    kind: 'floating-local-interval' as const,
    startsLocalAt,
    endsLocalAt: startsLocalAt.add({ minutes: durationMinutes }),
  });
}

export function TimelineAllDayLane({
  dateKey,
  items,
  groups,
  filters,
}: TimelineAllDayLaneProps) {
  const { t, i18n } = useTranslation('common');
  const canonicalActions = useTimelineCanonicalActions();
  const occurrenceScheduleSource = useMemo(
    () => createRemoteTemporalOccurrenceScheduleDataSource(),
    [],
  );
  const [pendingOccurrenceRef, setPendingOccurrenceRef] = useState<string | null>(
    null,
  );
  const visibleItems = useMemo(
    () => timelineAllDayItemsForVisibleDate(items, filters, dateKey),
    [dateKey, filters, items],
  );
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

  return (
    <section
      className="timeline-all-day-lane"
      data-timeline-all-day-lane={dateKey}
      aria-label={laneLabel}
      style={{ height: timelineAllDayLaneHeightPx(visibleItems.length) }}
    >
      <div className="timeline-all-day-lane__label">
        <span>{laneLabel}</span>
      </div>

      <div className="timeline-all-day-lane__items">
        {visibleItems.map((item) => {
          const group = groupMap.get(item.groupId);
          const tone = item.appearanceTone ?? group?.tone ?? 'personal';
          const position = timelineAllDayRangePosition(item, dateKey);
          const startsHere = position === 'single' || position === 'start';
          const endsHere = position === 'single' || position === 'end';
          const laneKind = item.laneKind ?? 'all-day';
          const precisionLabel =
            laneKind === 'coarse' && item.coarsePeriod !== undefined
              ? coarsePeriodLabel(item.coarsePeriod, language)
              : laneKind === 'expectation'
                ? t(($) => $.common.home.timeline.create.timeSemantics.expected)
                : laneKind === 'flexible'
                  ? t(
                      ($) =>
                        $.common.home.timeline.create.timeSemantics.flexible,
                    )
                  : t(
                      ($) => $.common.home.timeline.create.timeSemantics.allDay,
                    );
          const basis = item.canonicalBasis;
          const canUnschedule =
            basis !== undefined && canonicalActions !== null;
          const pending =
            basis !== undefined &&
            canonicalActions?.pendingScheduleRef === basis.scheduleRef;
          const occurrencePending =
            item.occurrenceBasis?.occurrenceRef === pendingOccurrenceRef;
          const eventPostpone = basis?.kind === 'scheduled-event';
          const withdrawalLabel = pending
            ? eventPostpone
              ? t(($) => $.common.home.timeline.detail.eventPostponing)
              : t(($) => $.common.home.timeline.detail.unscheduling)
            : eventPostpone
              ? t(($) => $.common.home.timeline.detail.eventPostpone)
              : t(($) => $.common.home.timeline.detail.unschedule);
          const scheduleLabel = occurrencePending
            ? english
              ? 'Scheduling…'
              : 'Pianificazione…'
            : english
              ? 'Schedule'
              : 'Pianifica';

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
                aria-label={`${item.title} · ${precisionLabel} · ${group?.label ?? item.groupId}`}
                onClick={(event) => event.currentTarget.focus()}
              >
                <span
                  className="timeline-all-day-item__continuation"
                  aria-hidden="true"
                >
                  {startsHere ? '' : '‹'}
                </span>
                <strong>{item.title}</strong>
                <span className="timeline-all-day-item__meta">
                  {precisionLabel} · {group?.label ?? item.groupId}
                  {item.meta ? ` · ${item.meta}` : ''}
                </span>
                <span
                  className="timeline-all-day-item__continuation"
                  aria-hidden="true"
                >
                  {endsHere ? '' : '›'}
                </span>
              </button>
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
              ) : canUnschedule ? (
                <button
                  className="timeline-all-day-item__unschedule"
                  type="button"
                  disabled={pending}
                  data-timeline-unschedule-schedule={basis.scheduleRef}
                  aria-label={`${withdrawalLabel} · ${item.title}`}
                  onClick={() => canonicalActions.unschedule(basis)}
                >
                  {withdrawalLabel}
                </button>
              ) : null}
            </div>
          );
        })}
      </div>
    </section>
  );
}
