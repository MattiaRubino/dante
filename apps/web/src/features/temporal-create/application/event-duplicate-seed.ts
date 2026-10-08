import { Temporal } from '@dante/time';

import type { TimelineCanonicalSchedulePlacement } from '../../home/ui/timeline/model/timeline-types';
import type { TemporalEventDetailRecord } from '../../temporal/event-data-source';
import type { TemporalCreateEventParticipantDraft } from '../model/temporal-create-u2-authoring';
import type { ActivityDuplicateSeed } from './activity-duplicate-seed';

function resolveSourceZoneDisambiguation(
  placement: Extract<TimelineCanonicalSchedulePlacement, { kind: 'named-zone-local' }>,
): 'reject' | 'earlier' | 'later' {
  const match = (local: Temporal.PlainDateTime, instant: Temporal.Instant) => {
    const early = local.toZonedDateTime(placement.zoneId, { disambiguation: 'earlier' }).toInstant();
    const late = local.toZonedDateTime(placement.zoneId, { disambiguation: 'later' }).toInstant();
    const earlier = Temporal.Instant.compare(early, instant) === 0;
    const later = Temporal.Instant.compare(late, instant) === 0;
    if (!earlier && !later) {
      throw new Error('Il fuso e gli istanti salvati non sono ricostruibili fedelmente.');
    }
    return earlier && later ? 'reject' : earlier ? 'earlier' : 'later';
  };
  const start = match(placement.startsLocalAt, placement.resolvedStartAt);
  const end = match(placement.endsLocalAt, placement.resolvedEndAt);
  if (start !== 'reject' && end !== 'reject' && start !== end) {
    throw new Error('L’intervallo attraversa due scelte DST incompatibili nel Create attuale.');
  }
  return start !== 'reject' ? start : end;
}

/**
 * A new Event Create draft, not a copy of identity, accepted operations,
 * observations, assessments, execution or mutable Schedule state.
 * Unsupported stored forms fail closed instead of being silently normalized.
 */
export function buildEventDuplicateSeed(
  event: TemporalEventDetailRecord,
  placement: TimelineCanonicalSchedulePlacement,
  expectedParticipants: readonly TemporalCreateEventParticipantDraft[] = [],
): ActivityDuplicateSeed {
  const shared = {
    kind: 'event' as const,
    title: event.title,
    contextId: event.lifeAreaRef ?? '',
    notes: event.description ?? '',
    event: { agendaParts: [...event.agendaParts], location: event.location ?? '' },
  };

  if (placement.kind === 'absolute') {
    throw new Error(
      'La programmazione assoluta UTC non è duplicabile fedelmente nel Create attuale.',
    );
  }
  if (placement.kind === 'date-span') {
    if (Temporal.PlainDate.compare(
      placement.endDateExclusive, placement.startDate,
    ) <= 0) {
      throw new Error('L’intervallo a giorni non è valido.');
    }
    const finalDate = placement.endDateExclusive.subtract({ days: 1 }).toString();
    return {
      fields: {
        ...shared,
        date: placement.startDate.toString(),
        timeSemantics: 'all-day',
        event: { ...shared.event, allDayEndDate: finalDate },
      },
      advanced: {
        endDate: finalDate,
        itemColorCode: event.colorCode ?? null,
        eventParticipants: [...expectedParticipants],
      },
    };
  }
  if (placement.kind === 'coarse-local-period') {
    return {
      fields: {
        ...shared,
        date: placement.localDate.toString(),
        timeSemantics: 'coarse',
        coarsePeriod: placement.period,
      },
      advanced: { itemColorCode: event.colorCode ?? null, eventParticipants: [...expectedParticipants] },
    };
  }

  const start = placement.startsLocalAt;
  const end = placement.endsLocalAt;
  const duration = end.since(start).total({ unit: 'minutes' });
  if (!Number.isSafeInteger(duration) || duration < 1 ||
      start.second !== 0 || end.second !== 0 ||
      start.millisecond !== 0 || end.millisecond !== 0 ||
      start.microsecond !== 0 || end.microsecond !== 0 ||
      start.nanosecond !== 0 || end.nanosecond !== 0) {
    throw new Error('La precisione originale dell’orario non può essere duplicata fedelmente.');
  }

  const zone = placement.kind === 'named-zone-local' ? placement.zoneId : null;
  const disambiguation = placement.kind === 'named-zone-local'
    ? resolveSourceZoneDisambiguation(placement)
    : null;
  return {
    fields: {
      ...shared,
      date: start.toPlainDate().toString(),
      timeSemantics: 'timed',
      startTime: start.toPlainTime().toString({ smallestUnit: 'minute' }),
      durationMinutes: duration,
      timeMode: zone ? 'zoned' : 'floating',
      ...(zone ? { timeZoneId: zone, timeDisambiguation: disambiguation ?? 'reject' } : {}),
    },
    advanced: { itemColorCode: event.colorCode ?? null, eventParticipants: [...expectedParticipants] },
  };
}
