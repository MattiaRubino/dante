import { Temporal } from '@dante/time';

import type { ActivityProfile } from '../../temporal/remote-activity-inspector';
import type {
  ActivityEditSchedule,
  ActivityEditSettings,
} from '../../temporal/remote-activity-edit-settings';
import type { TemporalCreateFieldSeed } from './temporal-create-seed';
import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';

export type ActivityDuplicateSeed = Readonly<{
  fields: TemporalCreateFieldSeed;
  advanced: Partial<TemporalCreateU2AuthoringDraft>;
}>;

function localWindow(schedule: ActivityEditSchedule) {
  if (
    !schedule.start ||
    !schedule.end ||
    !['floating_local', 'named_zone_local'].includes(schedule.temporalForm)
  ) {
    throw new Error(
      'Questa programmazione non può ancora essere duplicata fedelmente.',
    );
  }
  const start = Temporal.PlainDateTime.from(schedule.start);
  const end = Temporal.PlainDateTime.from(schedule.end);
  if (Temporal.PlainDateTime.compare(end, start) <= 0) {
    throw new Error('Intervallo salvato non valido.');
  }
  return { start, end };
}

export function buildActivityDuplicateSeed(
  profile: ActivityProfile,
  settings: ActivityEditSettings,
): ActivityDuplicateSeed {
  const intervals = settings.schedules
    .filter((schedule) => schedule.role === 'interval')
    .sort((left, right) => (left.order ?? 0) - (right.order ?? 0));
  const envelope =
    settings.schedules.find((schedule) => schedule.role === 'envelope') ??
    settings.schedules.find((schedule) => schedule.role === null);
  const occupied = intervals.length ? intervals : envelope ? [envelope] : [];
  const primary = occupied[0];
  const planned = settings.schedules
    .filter((schedule) => schedule.role === 'planned')
    .sort((left, right) => (left.order ?? 0) - (right.order ?? 0));
  if (!primary && planned.length) {
    throw new Error(
      'Le sessioni pianificate non hanno un intervallo di riferimento.',
    );
  }

  const first =
    primary?.temporalForm === 'date_span'
      ? null
      : primary
        ? localWindow(primary)
        : null;
  if (
    primary &&
    primary.temporalForm !== 'date_span' &&
    occupied.some(
      (schedule) =>
        schedule.temporalForm !== primary.temporalForm ||
        schedule.zoneId !== primary.zoneId,
    )
  ) {
    throw new Error(
      'Gli intervalli hanno fusi diversi e non possono essere duplicati fedelmente.',
    );
  }
  if (
    primary?.temporalForm === 'date_span' &&
    (!primary.start || !primary.end || intervals.length)
  ) {
    throw new Error('L’intervallo a giorni non è duplicabile in questa forma.');
  }
  if (primary?.temporalForm === 'date_span' && planned.length) {
    throw new Error(
      'Le sessioni pianificate richiedono un’attività con orario.',
    );
  }

  const fields: TemporalCreateFieldSeed = {
    kind: 'activity',
    title: profile.title,
    notes: profile.description ?? '',
    contextId: settings.lifeAreaRef ?? '',
    event: { location: profile.location ?? '' },
    ...(settings.reminderLeadMinutes !== null
      ? { confirmation: { reminderLeadMinutes: settings.reminderLeadMinutes } }
      : {}),
    timeSemantics: !primary ? 'unscheduled' : first ? 'timed' : 'all-day',
    ...(first
      ? {
          date: first.start.toPlainDate().toString(),
          startTime: first.start
            .toPlainTime()
            .toString({ smallestUnit: 'minute' }),
          durationMinutes: first.end
            .since(first.start)
            .total({ unit: 'minutes' }),
          timeMode:
            primary?.temporalForm === 'named_zone_local'
              ? ('zoned' as const)
              : ('floating' as const),
          ...(primary?.zoneId ? { timeZoneId: primary.zoneId } : {}),
        }
      : primary
        ? { date: primary.start!.slice(0, 10) }
        : {}),
  };
  const activityIntervals = intervals.slice(1).map((schedule) => {
    const { start, end } = localWindow(schedule);
    return {
      id: crypto.randomUUID(),
      date: start.toPlainDate().toString(),
      startTime: start.toPlainTime().toString({ smallestUnit: 'minute' }),
      endDate: end.toPlainDate().toString(),
      endTime: end.toPlainTime().toString({ smallestUnit: 'minute' }),
    };
  });
  const plannedSlices = planned.map((schedule) => {
    const { start, end } = localWindow(schedule);
    if (
      primary &&
      (schedule.temporalForm !== primary.temporalForm ||
        schedule.zoneId !== primary.zoneId)
    ) {
      throw new Error(
        'Una sessione pianificata usa un fuso diverso dall’attività.',
      );
    }
    return {
      id: crypto.randomUUID(),
      title: schedule.name ?? `Sessione ${schedule.order ?? 1}`,
      date: start.toPlainDate().toString(),
      startTime: start.toPlainTime().toString({ smallestUnit: 'minute' }),
      endTime: end.toPlainTime().toString({ smallestUnit: 'minute' }),
    };
  });
  if (
    planned.some((schedule) => {
      const { start, end } = localWindow(schedule);
      return start.toPlainDate().toString() !== end.toPlainDate().toString();
    })
  ) {
    throw new Error(
      'Una sessione attraversa la mezzanotte e richiede una modifica manuale.',
    );
  }
  const objectives = settings.objectives.map((objective) => ({
    id: crypto.randomUUID(),
    label: objective.label,
    resultKind: objective.resultKind,
    comparatorCode: objective.comparatorCode,
    targetValue: objective.targetValue?.toString() ?? '',
    targetMin: objective.targetMin?.toString() ?? '',
    targetMax: objective.targetMax?.toString() ?? '',
    unitCode: objective.unitCode ?? '',
  }));
  return {
    fields,
    advanced: {
      ...(primary?.temporalForm === 'date_span'
        ? {
            endDate: Temporal.PlainDate.from(primary.end!)
              .subtract({ days: 1 })
              .toString(),
          }
        : {}),
      itemColorCode: profile.colorCode,
      realityMode: settings.reality.mode,
      objectives,
      activityStructure: {
        captureMode: settings.capture.mode,
        realityMode: settings.reality.mode,
        placementProtected: settings.placementProtected,
        childGuardMode: settings.childGuardMode,
        children: [],
        plannedSlices,
        activityIntervals,
      },
    },
  };
}
