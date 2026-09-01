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
export type TemporalCreateSurface = 'quick' | 'expanded' | 'full';
export type TemporalCreateConstraintKind =
  | 'none'
  | 'open'
  | 'bounded-window'
  | 'deadline'
  | 'preferred-window';
export type TemporalCreateMovementPolicy =
  | 'locked'
  | 'window'
  | 'confirm'
  | 'free';
export type TemporalCreateFallbackPolicy =
  | 'inherit'
  | 'skip'
  | 'same-window'
  | 'next-valid-date'
  | 'shorten-or-split'
  | 'replan-dependencies';
export type TemporalCreateSessionMode = 'indivisible' | 'splittable';
export type TemporalCreateRecurrenceFrequency =
  | 'none'
  | 'daily'
  | 'weekly'
  | 'monthly';
export type TemporalCreateRecurrenceEnd = 'never' | 'date' | 'count';
export type TemporalCreateWeekday =
  | 'MO'
  | 'TU'
  | 'WE'
  | 'TH'
  | 'FR'
  | 'SA'
  | 'SU';
export type TemporalCreateOutcomePolicy =
  | 'inherit'
  | 'ask-immediately'
  | 'ask-later'
  | 'daily-review'
  | 'weekly-review'
  | 'silent'
  | 'auto-complete'
  | 'auto-not-completed';
export type TemporalCreateAvailability = 'busy' | 'free';
export type TemporalCreateVisibility = 'default' | 'private' | 'public';
export type TemporalCreateConferenceMode = 'none' | 'provider-default';

export type TemporalCreateSchedulingIntent = Readonly<{
  constraintKind: TemporalCreateConstraintKind;
  windowStartDate: string;
  windowEndDate: string;
  windowStartTime: string;
  windowEndTime: string;
  earliestStartDate: string;
  earliestStartTime: string;
  deadlineDate: string;
  deadlineTime: string;
  preferredStartTime: string;
  preferredEndTime: string;
  movementPolicy: TemporalCreateMovementPolicy;
  fallbackPolicy: TemporalCreateFallbackPolicy;
}>;

export type TemporalCreateExecutionIntent = Readonly<{
  sessionMode: TemporalCreateSessionMode;
  minSessionMinutes: number;
  maxSessions: number | null;
  partialAllowed: boolean;
  finishEarlyAllowed: boolean;
  mergeCompatible: boolean;
  preparationMinutes: number;
  recoveryMinutes: number;
  spacingMinutes: number;
}>;

export type TemporalCreateRecurrenceIntent = Readonly<{
  frequency: TemporalCreateRecurrenceFrequency;
  interval: number;
  weekdays: readonly TemporalCreateWeekday[];
  endMode: TemporalCreateRecurrenceEnd;
  untilDate: string;
  count: number;
}>;

export type TemporalCreateConfirmationIntent = Readonly<{
  outcomePolicy: TemporalCreateOutcomePolicy;
  reminderLeadMinutes: number | null;
}>;

export type TemporalCreateEventIntent = Readonly<{
  allDayEndDate: string;
  location: string;
  availability: TemporalCreateAvailability;
  visibility: TemporalCreateVisibility;
  participants: string;
  resources: string;
  conferenceMode: TemporalCreateConferenceMode;
}>;

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
  tags: string;
  scheduling: TemporalCreateSchedulingIntent;
  execution: TemporalCreateExecutionIntent;
  recurrence: TemporalCreateRecurrenceIntent;
  confirmation: TemporalCreateConfirmationIntent;
  event: TemporalCreateEventIntent;
}>;

export type TemporalCreateCloseDecision = 'none' | 'confirm-discard';

export type TemporalCreateSession = Readonly<{
  draft: TemporalDraft<TemporalCreateFields>;
  closeDecision: TemporalCreateCloseDecision;
  detailsOpen: boolean;
  surface: TemporalCreateSurface;
}>;

export type TemporalCreateCloseRequest = Readonly<{
  session: TemporalCreateSession;
  shouldClose: boolean;
}>;

export type TemporalCreateFieldOptions = Partial<TemporalCreateFields>;

const WEEKDAYS: readonly TemporalCreateWeekday[] = Object.freeze([
  'MO',
  'TU',
  'WE',
  'TH',
  'FR',
  'SA',
  'SU',
]);

function freezeScheduling(
  value: TemporalCreateSchedulingIntent,
): TemporalCreateSchedulingIntent {
  return Object.freeze({ ...value });
}

function freezeExecution(
  value: TemporalCreateExecutionIntent,
): TemporalCreateExecutionIntent {
  return Object.freeze({ ...value });
}

function freezeRecurrence(
  value: TemporalCreateRecurrenceIntent,
): TemporalCreateRecurrenceIntent {
  return Object.freeze({
    ...value,
    weekdays: Object.freeze([...value.weekdays]),
  });
}

function freezeConfirmation(
  value: TemporalCreateConfirmationIntent,
): TemporalCreateConfirmationIntent {
  return Object.freeze({ ...value });
}

function freezeEvent(value: TemporalCreateEventIntent): TemporalCreateEventIntent {
  return Object.freeze({ ...value });
}

function normalizeFields(fields: TemporalCreateFields): TemporalCreateFields {
  let timeSemantics = fields.timeSemantics;
  let scheduling = fields.scheduling;

  if (fields.kind === 'event') {
    if (timeSemantics === 'unscheduled') {
      timeSemantics = 'timed';
    }
    if (
      scheduling.constraintKind !== 'none' ||
      scheduling.fallbackPolicy !== 'inherit'
    ) {
      scheduling = {
        ...scheduling,
        constraintKind: 'none',
        fallbackPolicy: 'inherit',
      };
    }
  } else if (scheduling.constraintKind !== 'none') {
    timeSemantics = 'unscheduled';
  } else if (timeSemantics !== 'unscheduled') {
    scheduling = { ...scheduling, constraintKind: 'none' };
  }

  return Object.freeze({
    ...fields,
    timeSemantics,
    scheduling: freezeScheduling(scheduling),
    execution: freezeExecution(fields.execution),
    recurrence: freezeRecurrence(fields.recurrence),
    confirmation: freezeConfirmation(fields.confirmation),
    event: freezeEvent(fields.event),
  });
}

export function createTemporalCreateFields(
  options: TemporalCreateFieldOptions = {},
): TemporalCreateFields {
  const date = options.date ?? '1970-01-01';
  const scheduling = freezeScheduling(
    options.scheduling ?? {
      constraintKind: 'none',
      windowStartDate: date,
      windowEndDate: date,
      windowStartTime: '09:00',
      windowEndTime: '17:00',
      earliestStartDate: date,
      earliestStartTime: '09:00',
      deadlineDate: date,
      deadlineTime: '18:00',
      preferredStartTime: '18:00',
      preferredEndTime: '22:00',
      movementPolicy: 'confirm',
      fallbackPolicy: 'inherit',
    },
  );
  const execution = freezeExecution(
    options.execution ?? {
      sessionMode: 'indivisible',
      minSessionMinutes: 30,
      maxSessions: null,
      partialAllowed: false,
      finishEarlyAllowed: true,
      mergeCompatible: false,
      preparationMinutes: 0,
      recoveryMinutes: 0,
      spacingMinutes: 0,
    },
  );
  const recurrence = freezeRecurrence(
    options.recurrence ?? {
      frequency: 'none',
      interval: 1,
      weekdays: Object.freeze([]),
      endMode: 'never',
      untilDate: date,
      count: 10,
    },
  );
  const confirmation = freezeConfirmation(
    options.confirmation ?? {
      outcomePolicy: 'inherit',
      reminderLeadMinutes: null,
    },
  );
  const event = freezeEvent(
    options.event ?? {
      allDayEndDate: date,
      location: '',
      availability: 'busy',
      visibility: 'default',
      participants: '',
      resources: '',
      conferenceMode: 'none',
    },
  );

  return normalizeFields(
    Object.freeze({
      title: options.title ?? '',
      kind: options.kind ?? 'activity',
      date,
      timeSemantics: options.timeSemantics ?? 'timed',
      startTime: options.startTime ?? '09:00',
      durationMinutes: options.durationMinutes ?? 30,
      timeMode: options.timeMode ?? 'floating',
      timeZoneId: options.timeZoneId ?? 'UTC',
      contextId: options.contextId ?? 'personale',
      notes: options.notes ?? '',
      tags: options.tags ?? '',
      scheduling,
      execution,
      recurrence,
      confirmation,
      event,
    }),
  );
}

function sameWeekdays(
  left: readonly TemporalCreateWeekday[],
  right: readonly TemporalCreateWeekday[],
): boolean {
  return (
    left.length === right.length &&
    left.every((value, index) => value === right[index])
  );
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
    left.notes === right.notes &&
    left.tags === right.tags &&
    left.scheduling.constraintKind === right.scheduling.constraintKind &&
    left.scheduling.windowStartDate === right.scheduling.windowStartDate &&
    left.scheduling.windowEndDate === right.scheduling.windowEndDate &&
    left.scheduling.windowStartTime === right.scheduling.windowStartTime &&
    left.scheduling.windowEndTime === right.scheduling.windowEndTime &&
    left.scheduling.earliestStartDate === right.scheduling.earliestStartDate &&
    left.scheduling.earliestStartTime === right.scheduling.earliestStartTime &&
    left.scheduling.deadlineDate === right.scheduling.deadlineDate &&
    left.scheduling.deadlineTime === right.scheduling.deadlineTime &&
    left.scheduling.preferredStartTime === right.scheduling.preferredStartTime &&
    left.scheduling.preferredEndTime === right.scheduling.preferredEndTime &&
    left.scheduling.movementPolicy === right.scheduling.movementPolicy &&
    left.scheduling.fallbackPolicy === right.scheduling.fallbackPolicy &&
    left.execution.sessionMode === right.execution.sessionMode &&
    left.execution.minSessionMinutes === right.execution.minSessionMinutes &&
    left.execution.maxSessions === right.execution.maxSessions &&
    left.execution.partialAllowed === right.execution.partialAllowed &&
    left.execution.finishEarlyAllowed === right.execution.finishEarlyAllowed &&
    left.execution.mergeCompatible === right.execution.mergeCompatible &&
    left.execution.preparationMinutes === right.execution.preparationMinutes &&
    left.execution.recoveryMinutes === right.execution.recoveryMinutes &&
    left.execution.spacingMinutes === right.execution.spacingMinutes &&
    left.recurrence.frequency === right.recurrence.frequency &&
    left.recurrence.interval === right.recurrence.interval &&
    sameWeekdays(left.recurrence.weekdays, right.recurrence.weekdays) &&
    left.recurrence.endMode === right.recurrence.endMode &&
    left.recurrence.untilDate === right.recurrence.untilDate &&
    left.recurrence.count === right.recurrence.count &&
    left.confirmation.outcomePolicy === right.confirmation.outcomePolicy &&
    left.confirmation.reminderLeadMinutes ===
      right.confirmation.reminderLeadMinutes &&
    left.event.allDayEndDate === right.event.allDayEndDate &&
    left.event.location === right.event.location &&
    left.event.availability === right.event.availability &&
    left.event.visibility === right.event.visibility &&
    left.event.participants === right.event.participants &&
    left.event.resources === right.event.resources &&
    left.event.conferenceMode === right.event.conferenceMode
  );
}

function freezeSession(
  draft: TemporalDraft<TemporalCreateFields>,
  closeDecision: TemporalCreateCloseDecision,
  surface: TemporalCreateSurface,
): TemporalCreateSession {
  return Object.freeze({
    draft,
    closeDecision,
    detailsOpen: surface !== 'quick',
    surface,
  });
}

export function createTemporalCreateSession(
  fields: TemporalCreateFields = createTemporalCreateFields(),
): TemporalCreateSession {
  return freezeSession(createTemporalDraft(fields), 'none', 'quick');
}

export function updateTemporalCreateFields(
  session: TemporalCreateSession,
  patch: Partial<TemporalCreateFields>,
): TemporalCreateSession {
  const current = session.draft.current;
  const next = normalizeFields(
    Object.freeze({
      ...current,
      ...patch,
      scheduling: patch.scheduling
        ? freezeScheduling(patch.scheduling)
        : current.scheduling,
      execution: patch.execution
        ? freezeExecution(patch.execution)
        : current.execution,
      recurrence: patch.recurrence
        ? freezeRecurrence(patch.recurrence)
        : current.recurrence,
      confirmation: patch.confirmation
        ? freezeConfirmation(patch.confirmation)
        : current.confirmation,
      event: patch.event ? freezeEvent(patch.event) : current.event,
    }),
  );
  return freezeSession(
    updateTemporalDraft(session.draft, next, temporalCreateFieldsEqual),
    'none',
    session.surface,
  );
}

export function updateTemporalCreateTitle(
  session: TemporalCreateSession,
  title: string,
): TemporalCreateSession {
  return updateTemporalCreateFields(session, { title });
}

export function setTemporalCreateSurface(
  session: TemporalCreateSession,
  surface: TemporalCreateSurface,
): TemporalCreateSession {
  return freezeSession(session.draft, session.closeDecision, surface);
}

export function setTemporalCreateDetailsOpen(
  session: TemporalCreateSession,
  detailsOpen: boolean,
): TemporalCreateSession {
  return setTemporalCreateSurface(session, detailsOpen ? 'expanded' : 'quick');
}

export function requestTemporalCreateClose(
  session: TemporalCreateSession,
): TemporalCreateCloseRequest {
  if (!session.draft.dirty) {
    return Object.freeze({ session, shouldClose: true });
  }

  return Object.freeze({
    session: freezeSession(session.draft, 'confirm-discard', session.surface),
    shouldClose: false,
  });
}

export function continueTemporalCreateEditing(
  session: TemporalCreateSession,
): TemporalCreateSession {
  return freezeSession(session.draft, 'none', session.surface);
}

export function discardTemporalCreateSession(
  fields: TemporalCreateFields = createTemporalCreateFields(),
): TemporalCreateSession {
  return createTemporalCreateSession(fields);
}

function parseDate(
  value: string,
): ReturnType<typeof Temporal.PlainDate.from> | null {
  try {
    return Temporal.PlainDate.from(value);
  } catch {
    return null;
  }
}

function parseTime(
  value: string,
): Readonly<{ hour: number; minute: number }> | null {
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

function dateTime(dateValue: string, timeValue: string) {
  const date = parseDate(dateValue);
  const time = parseTime(timeValue);
  if (!date || !time) {
    return null;
  }
  return Temporal.PlainDateTime.from({
    year: date.year,
    month: date.month,
    day: date.day,
    hour: time.hour,
    minute: time.minute,
  });
}

function validNonNegativeMinutes(value: number): boolean {
  return Number.isInteger(value) && value >= 0 && value <= 1440;
}

export function temporalCreateHasFlexibleIntent(
  fields: TemporalCreateFields,
): boolean {
  return (
    fields.kind === 'activity' && fields.scheduling.constraintKind !== 'none'
  );
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
    issues.push(
      temporalValidationIssue('temporal.create.date.invalid', ['date']),
    );
  }
  if (fields.kind === 'event' && fields.timeSemantics === 'unscheduled') {
    issues.push(
      temporalValidationIssue('temporal.create.event.requires_placement', [
        'timeSemantics',
      ]),
    );
  }

  if (fields.timeSemantics === 'all-day' && fields.kind === 'event') {
    const endDate = parseDate(fields.event.allDayEndDate);
    if (
      !date ||
      !endDate ||
      Temporal.PlainDate.compare(endDate, date) < 0
    ) {
      issues.push(
        temporalValidationIssue('temporal.create.all_day_range.invalid', [
          'event.allDayEndDate',
        ]),
      );
    }
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
      fields.durationMinutes > 10080
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

  if (fields.kind === 'activity') {
    const scheduling = fields.scheduling;
    if (scheduling.constraintKind === 'bounded-window') {
      const start = dateTime(
        scheduling.windowStartDate,
        scheduling.windowStartTime,
      );
      const end = dateTime(scheduling.windowEndDate, scheduling.windowEndTime);
      if (!start || !end || Temporal.PlainDateTime.compare(start, end) >= 0) {
        issues.push(
          temporalValidationIssue('temporal.create.window.invalid', [
            'scheduling.window',
          ]),
        );
      }
    }

    if (scheduling.constraintKind === 'deadline') {
      const earliest = dateTime(
        scheduling.earliestStartDate,
        scheduling.earliestStartTime,
      );
      const deadline = dateTime(
        scheduling.deadlineDate,
        scheduling.deadlineTime,
      );
      if (
        !earliest ||
        !deadline ||
        Temporal.PlainDateTime.compare(earliest, deadline) >= 0
      ) {
        issues.push(
          temporalValidationIssue('temporal.create.deadline.invalid', [
            'scheduling.deadline',
          ]),
        );
      }
    }

    if (scheduling.constraintKind === 'preferred-window') {
      const preferredStart = parseTime(scheduling.preferredStartTime);
      const preferredEnd = parseTime(scheduling.preferredEndTime);
      if (
        !preferredStart ||
        !preferredEnd ||
        preferredStart.hour * 60 + preferredStart.minute >=
          preferredEnd.hour * 60 + preferredEnd.minute
      ) {
        issues.push(
          temporalValidationIssue('temporal.create.preferred_window.invalid', [
            'scheduling.preferredWindow',
          ]),
        );
      }
    }

    if (fields.execution.sessionMode === 'splittable') {
      if (
        !Number.isInteger(fields.execution.minSessionMinutes) ||
        fields.execution.minSessionMinutes < 5 ||
        fields.execution.minSessionMinutes > fields.durationMinutes
      ) {
        issues.push(
          temporalValidationIssue('temporal.create.minimum_session.invalid', [
            'execution.minSessionMinutes',
          ]),
        );
      }
      if (
        fields.execution.maxSessions !== null &&
        (!Number.isInteger(fields.execution.maxSessions) ||
          fields.execution.maxSessions < 2 ||
          fields.execution.maxSessions > 99)
      ) {
        issues.push(
          temporalValidationIssue('temporal.create.session_count.invalid', [
            'execution.maxSessions',
          ]),
        );
      }
    }

    if (
      !validNonNegativeMinutes(fields.execution.preparationMinutes) ||
      !validNonNegativeMinutes(fields.execution.recoveryMinutes) ||
      !validNonNegativeMinutes(fields.execution.spacingMinutes)
    ) {
      issues.push(
        temporalValidationIssue('temporal.create.buffer.invalid', [
          'execution.buffers',
        ]),
      );
    }
  }

  const recurrence = fields.recurrence;
  if (recurrence.frequency !== 'none') {
    if (
      !Number.isInteger(recurrence.interval) ||
      recurrence.interval < 1 ||
      recurrence.interval > 365
    ) {
      issues.push(
        temporalValidationIssue('temporal.create.recurrence.interval_invalid', [
          'recurrence.interval',
        ]),
      );
    }
    if (
      recurrence.frequency === 'weekly' &&
      recurrence.weekdays.length === 0
    ) {
      issues.push(
        temporalValidationIssue('temporal.create.recurrence.weekdays_required', [
          'recurrence.weekdays',
        ]),
      );
    }
    if (recurrence.endMode === 'date') {
      const until = parseDate(recurrence.untilDate);
      if (!date || !until || Temporal.PlainDate.compare(until, date) < 0) {
        issues.push(
          temporalValidationIssue('temporal.create.recurrence.until_invalid', [
            'recurrence.untilDate',
          ]),
        );
      }
    }
    if (
      recurrence.endMode === 'count' &&
      (!Number.isInteger(recurrence.count) ||
        recurrence.count < 1 ||
        recurrence.count > 999)
    ) {
      issues.push(
        temporalValidationIssue('temporal.create.recurrence.count_invalid', [
          'recurrence.count',
        ]),
      );
    }
  }

  const reminder = fields.confirmation.reminderLeadMinutes;
  if (
    reminder !== null &&
    (!Number.isInteger(reminder) || reminder < 0 || reminder > 10080)
  ) {
    issues.push(
      temporalValidationIssue('temporal.create.reminder.invalid', [
        'confirmation.reminderLeadMinutes',
      ]),
    );
  }

  return Object.freeze(issues);
}

export function buildTemporalCreatePlacement(
  fields: TemporalCreateFields,
): TemporalPlacement | null {
  if (
    fields.timeSemantics === 'unscheduled' ||
    temporalCreateHasFlexibleIntent(fields)
  ) {
    return null;
  }

  const date = Temporal.PlainDate.from(fields.date);
  if (fields.timeSemantics === 'all-day') {
    const inclusiveEnd =
      fields.kind === 'event'
        ? Temporal.PlainDate.from(fields.event.allDayEndDate)
        : date;
    return Object.freeze({
      kind: 'date-span' as const,
      startDate: date,
      endDateExclusive: inclusiveEnd.add({ days: 1 }),
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

export function temporalCreateWeekdays(): readonly TemporalCreateWeekday[] {
  return WEEKDAYS;
}
