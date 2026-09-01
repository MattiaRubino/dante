import { Temporal } from '@dante/time';

import {
  createTemporalDraft,
  temporalValidationIssue,
  updateTemporalDraft,
  type TemporalDraft,
  type TemporalPlacement,
  type TemporalValidationIssue,
} from '../../temporal';

export type TemporalCreateKind = 'activity' | 'event';
export type TemporalCreateTimeSemantics = 'timed' | 'all-day' | 'unscheduled';
export type TemporalCreateTimeMode = 'floating' | 'zoned';

export type TemporalCreateFields = Readonly<{
  title: string;
  kind: TemporalCreateKind;
  date: string;
  timeSemantics: TemporalCreateTimeSemantics;
  startTime: string;
  durationMinutes: number;
  timeMode: TemporalCreateTimeMode;
  timeZoneId: string;
  contextId: string;
  notes: string;
}>;

export type TemporalCreateCloseDecision = 'none' | 'confirm-discard';

export type TemporalCreateSession = Readonly<{
  draft: TemporalDraft<TemporalCreateFields>;
  closeDecision: TemporalCreateCloseDecision;
  detailsOpen: boolean;
}>;

export type TemporalCreateCloseRequest = Readonly<{
  session: TemporalCreateSession;
  shouldClose: boolean;
}>;

export type TemporalCreateFieldOptions = Partial<TemporalCreateFields>;

export function createTemporalCreateFields(
  options: TemporalCreateFieldOptions = {},
): TemporalCreateFields {
  return Object.freeze({
    title: options.title ?? '',
    kind: options.kind ?? 'activity',
    date: options.date ?? '1970-01-01',
    timeSemantics: options.timeSemantics ?? 'timed',
    startTime: options.startTime ?? '09:00',
    durationMinutes: options.durationMinutes ?? 30,
    timeMode: options.timeMode ?? 'floating',
    timeZoneId: options.timeZoneId ?? 'UTC',
    contextId: options.contextId ?? 'personale',
    notes: options.notes ?? '',
  });
}

function temporalCreateFieldsEqual(
  left: TemporalCreateFields,
  right: TemporalCreateFields,
): boolean {
  return (
    left.title === right.title &&
    left.kind === right.kind &&
    left.date === right.date &&
    left.timeSemantics === right.timeSemantics &&
    left.startTime === right.startTime &&
    left.durationMinutes === right.durationMinutes &&
    left.timeMode === right.timeMode &&
    left.timeZoneId === right.timeZoneId &&
    left.contextId === right.contextId &&
    left.notes === right.notes
  );
}

function freezeSession(
  draft: TemporalDraft<TemporalCreateFields>,
  closeDecision: TemporalCreateCloseDecision,
  detailsOpen: boolean,
): TemporalCreateSession {
  return Object.freeze({ draft, closeDecision, detailsOpen });
}

export function createTemporalCreateSession(
  fields: TemporalCreateFields = createTemporalCreateFields(),
): TemporalCreateSession {
  return freezeSession(createTemporalDraft(fields), 'none', false);
}

export function updateTemporalCreateFields(
  session: TemporalCreateSession,
  patch: Partial<TemporalCreateFields>,
): TemporalCreateSession {
  const current = session.draft.current;
  const next = Object.freeze({ ...current, ...patch });
  return freezeSession(
    updateTemporalDraft(session.draft, next, temporalCreateFieldsEqual),
    'none',
    session.detailsOpen,
  );
}

export function updateTemporalCreateTitle(
  session: TemporalCreateSession,
  title: string,
): TemporalCreateSession {
  return updateTemporalCreateFields(session, { title });
}

export function setTemporalCreateDetailsOpen(
  session: TemporalCreateSession,
  detailsOpen: boolean,
): TemporalCreateSession {
  return freezeSession(session.draft, session.closeDecision, detailsOpen);
}

export function requestTemporalCreateClose(
  session: TemporalCreateSession,
): TemporalCreateCloseRequest {
  if (!session.draft.dirty) {
    return Object.freeze({ session, shouldClose: true });
  }

  return Object.freeze({
    session: freezeSession(
      session.draft,
      'confirm-discard',
      session.detailsOpen,
    ),
    shouldClose: false,
  });
}

export function continueTemporalCreateEditing(
  session: TemporalCreateSession,
): TemporalCreateSession {
  return freezeSession(session.draft, 'none', session.detailsOpen);
}

export function discardTemporalCreateSession(
  fields: TemporalCreateFields = createTemporalCreateFields(),
): TemporalCreateSession {
  return createTemporalCreateSession(fields);
}

function parseDate(value: string): ReturnType<typeof Temporal.PlainDate.from> | null {
  try {
    return Temporal.PlainDate.from(value);
  } catch {
    return null;
  }
}

function parseTime(value: string): Readonly<{ hour: number; minute: number }> | null {
  const match = /^(\d{2}):(\d{2})$/.exec(value);
  if (!match) {
    return null;
  }
  const hour = Number(match[1]);
  const minute = Number(match[2]);
  if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
    return null;
  }
  return Object.freeze({ hour, minute });
}

export function validateTemporalCreateFields(
  fields: TemporalCreateFields,
): readonly TemporalValidationIssue[] {
  const issues: TemporalValidationIssue[] = [];
  const date = parseDate(fields.date);

  if (fields.title.trim().length === 0) {
    issues.push(
      temporalValidationIssue('temporal.projection.title.required', ['title']),
    );
  }
  if (!date) {
    issues.push(temporalValidationIssue('temporal.create.date.invalid', ['date']));
  }
  if (fields.kind === 'event' && fields.timeSemantics === 'unscheduled') {
    issues.push(
      temporalValidationIssue('temporal.create.event.requires_placement', [
        'timeSemantics',
      ]),
    );
  }

  if (fields.timeSemantics === 'timed') {
    const time = parseTime(fields.startTime);
    if (!time) {
      issues.push(
        temporalValidationIssue('temporal.create.start_time.invalid', [
          'startTime',
        ]),
      );
    }
    if (
      !Number.isInteger(fields.durationMinutes) ||
      fields.durationMinutes < 5 ||
      fields.durationMinutes > 1440
    ) {
      issues.push(
        temporalValidationIssue('temporal.create.duration.invalid', [
          'durationMinutes',
        ]),
      );
    }

    if (date && time && fields.timeMode === 'zoned') {
      try {
        Temporal.PlainDateTime.from({
          year: date.year,
          month: date.month,
          day: date.day,
          hour: time.hour,
          minute: time.minute,
        }).toZonedDateTime(fields.timeZoneId);
      } catch {
        issues.push(
          temporalValidationIssue('temporal.create.timezone.invalid', [
            'timeZoneId',
          ]),
        );
      }
    }
  }

  if (fields.contextId.trim().length === 0) {
    issues.push(
      temporalValidationIssue('temporal.create.context.required', ['contextId']),
    );
  }

  return Object.freeze(issues);
}

export function buildTemporalCreatePlacement(
  fields: TemporalCreateFields,
): TemporalPlacement | null {
  if (fields.timeSemantics === 'unscheduled') {
    return null;
  }

  const date = Temporal.PlainDate.from(fields.date);
  if (fields.timeSemantics === 'all-day') {
    return Object.freeze({
      kind: 'date-span' as const,
      startDate: date,
      endDateExclusive: date.add({ days: 1 }),
    });
  }

  const time = parseTime(fields.startTime);
  if (!time) {
    throw new Error('Cannot build placement from an invalid start time');
  }
  const start = Temporal.PlainDateTime.from({
    year: date.year,
    month: date.month,
    day: date.day,
    hour: time.hour,
    minute: time.minute,
  });

  if (fields.timeMode === 'zoned') {
    const zonedStart = start.toZonedDateTime(fields.timeZoneId);
    return Object.freeze({
      kind: 'zoned' as const,
      start: zonedStart,
      end: zonedStart.add({ minutes: fields.durationMinutes }),
    });
  }

  return Object.freeze({
    kind: 'floating-local' as const,
    start,
    end: start.add({ minutes: fields.durationMinutes }),
  });
}
