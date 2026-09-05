import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  buildTemporalCreatePlacement,
  continueTemporalCreateEditing,
  createTemporalCreateFields,
  createTemporalCreateSession,
  discardTemporalCreateSession,
  requestTemporalCreateClose,
  setTemporalCreateDetailsOpen,
  setTemporalCreateSurface,
  temporalCreateHasFlexibleIntent,
  updateTemporalCreateFields,
  updateTemporalCreateTitle,
  validateTemporalCreateFields,
} from './temporal-create-session';

describe('temporal create session', () => {
  it('starts with a clean structured draft', () => {
    const session = createTemporalCreateSession(
      createTemporalCreateFields({
        date: '2026-09-01',
        timeZoneId: 'Europe/Rome',
      }),
    );

    expect(session.closeDecision).toBe('none');
    expect(session.surface).toBe('quick');
    expect(session.draft.current.title).toBe('');
    expect(session.draft.current.kind).toBe('activity');
    expect(session.draft.current.timeSemantics).toBe('timed');
    expect(session.draft.current.scheduling.constraintKind).toBe('none');
    expect(session.draft.current.eventRecurrence.patternKind).toBe('none');
    expect(session.draft.current.eventRecurrence.quotaTimeZoneId).toBe(
      'Europe/Rome',
    );
    expect(session.draft.current.event.agendaParts).toEqual([]);
    expect(Object.isFrozen(session.draft.current.event.agendaParts)).toBe(true);
    expect(session.draft.dirty).toBe(false);
  });

  it('marks deep edits dirty and returning to baseline clean', () => {
    const initial = createTemporalCreateSession();
    const edited = updateTemporalCreateFields(initial, {
      scheduling: {
        ...initial.draft.current.scheduling,
        movementPolicy: 'free',
      },
    });
    const restored = updateTemporalCreateFields(edited, {
      scheduling: initial.draft.current.scheduling,
    });

    expect(edited.draft.dirty).toBe(true);
    expect(restored.draft.dirty).toBe(false);
    expect(restored.draft.editRevision).toBe(2);
  });

  it('normalizes Event agenda into ordered non-empty internal parts', () => {
    const baseline = createTemporalCreateFields({
      title: 'Lezione inglese',
      kind: 'event',
      date: '2026-09-01',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      event: {
        ...baseline.event,
        agendaParts: Object.freeze([
          ' Listening ',
          '',
          'Orale',
          '  ',
          'Scritto ',
        ]),
      },
    });

    expect(fields.event.agendaParts).toEqual(['Listening', 'Orale', 'Scritto']);
    expect(Object.isFrozen(fields.event.agendaParts)).toBe(true);

    const session = createTemporalCreateSession(fields);
    const edited = updateTemporalCreateFields(session, {
      event: {
        ...session.draft.current.event,
        agendaParts: Object.freeze(['Listening', 'Scritto', 'Orale']),
      },
    });

    expect(edited.draft.current.event.agendaParts).toEqual([
      'Listening',
      'Scritto',
      'Orale',
    ]);
    expect(edited.draft.dirty).toBe(true);
  });

  it('protects a dirty structured draft behind an explicit discard decision', () => {
    const edited = updateTemporalCreateFields(createTemporalCreateSession(), {
      title: 'Studiare inglese',
      contextId: 'focus',
      durationMinutes: 60,
    });
    const request = requestTemporalCreateClose(edited);

    expect(request.shouldClose).toBe(false);
    expect(request.session.closeDecision).toBe('confirm-discard');
    expect(request.session.draft.current.title).toBe('Studiare inglese');
  });

  it('continues editing and changes presentation depth without losing deep draft state', () => {
    const baseline = createTemporalCreateFields();
    const base = createTemporalCreateFields({
      title: 'Call ricorrente',
      kind: 'event',
      date: '2026-09-01',
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'quota-per-period',
        quotaCount: 3,
        quotaPeriodKind: 'week',
        quotaFrame: 'named-zone',
        quotaWeekStart: 'MO',
        quotaTimeZoneId: 'Europe/Rome',
      },
      event: {
        ...baseline.event,
        purpose: 'Decisione progetto',
        agendaParts: Object.freeze(['Rischi', 'Decisioni']),
      },
    });
    const edited = updateTemporalCreateTitle(
      createTemporalCreateSession(base),
      'Call ricorrente aggiornata',
    );
    const protectedSession = requestTemporalCreateClose(edited).session;
    const resumed = continueTemporalCreateEditing(protectedSession);
    const expanded = setTemporalCreateDetailsOpen(resumed, true);
    const full = setTemporalCreateSurface(expanded, 'full');
    const legacyExpanded = setTemporalCreateSurface(full, 'expanded');
    const compact = setTemporalCreateSurface(legacyExpanded, 'quick');
    const reopened = setTemporalCreateSurface(compact, 'full');

    expect(expanded.surface).toBe('full');
    expect(legacyExpanded.surface).toBe('full');
    expect(reopened.closeDecision).toBe('none');
    expect(reopened.surface).toBe('full');
    expect(reopened.draft.current.title).toBe('Call ricorrente aggiornata');
    expect(reopened.draft.current.eventRecurrence.patternKind).toBe(
      'quota-per-period',
    );
    expect(reopened.draft.current.eventRecurrence.quotaFrame).toBe(
      'named-zone',
    );
    expect(reopened.draft.current.eventRecurrence.quotaWeekStart).toBe('MO');
    expect(reopened.draft.current.eventRecurrence.quotaTimeZoneId).toBe(
      'Europe/Rome',
    );
    expect(reopened.draft.current.event.purpose).toBe('Decisione progetto');
    expect(reopened.draft.current.event.agendaParts).toEqual([
      'Rischi',
      'Decisioni',
    ]);
  });

  it('normalizes Event creation away from Activity-only unscheduled/flexible states', () => {
    const activity = createTemporalCreateFields({
      title: 'Leggere',
      kind: 'activity',
      timeSemantics: 'unscheduled',
      date: '2026-09-01',
      scheduling: {
        ...createTemporalCreateFields().scheduling,
        constraintKind: 'deadline',
        earliestStartDate: '2026-09-01',
        deadlineDate: '2026-09-03',
      },
    });
    const eventSession = updateTemporalCreateFields(
      createTemporalCreateSession(activity),
      { kind: 'event' },
    );

    expect(temporalCreateHasFlexibleIntent(activity)).toBe(true);
    expect(buildTemporalCreatePlacement(activity)).toBeNull();
    expect(eventSession.draft.current.kind).toBe('event');
    expect(eventSession.draft.current.timeSemantics).toBe('timed');
    expect(eventSession.draft.current.scheduling.constraintKind).toBe('none');
  });

  it('drops Event-owned recurrence when switching to Activity without explicit Routine ownership', () => {
    const event = createTemporalCreateFields({
      title: 'Call',
      kind: 'event',
      date: '2026-09-01',
      eventRecurrence: {
        ...createTemporalCreateFields().eventRecurrence,
        patternKind: 'elapsed-interval',
        elapsedIntervalMinutes: 1440,
      },
    });
    const activity = updateTemporalCreateFields(
      createTemporalCreateSession(event),
      { kind: 'activity' },
    );

    expect(event.eventRecurrence.owner).toBe('event');
    expect(event.eventRecurrence.patternKind).toBe('elapsed-interval');
    expect(activity.draft.current.eventRecurrence.owner).toBeNull();
    expect(activity.draft.current.eventRecurrence.patternKind).toBe('none');
    expect(validateTemporalCreateFields(activity.draft.current)).toEqual([]);
  });

  it('validates a Routine-backed Activity quota such as three times per week', () => {
    const baseline = createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-09-01',
    });
    const repeated = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        owner: 'routine',
        patternKind: 'quota-per-period',
        quotaCount: 3,
        quotaPeriodKind: 'week',
        quotaPeriodInterval: 1,
        quotaFrame: 'floating-local',
        quotaWeekStart: 'MO',
      },
    });

    expect(validateTemporalCreateFields(repeated)).toEqual([]);
    expect(repeated.eventRecurrence.owner).toBe('routine');
    expect(repeated.eventRecurrence.patternKind).toBe('quota-per-period');
    expect(repeated.eventRecurrence.quotaCount).toBe(3);
    expect(repeated.eventRecurrence.quotaPeriodKind).toBe('week');
  });

  it('still rejects an externally malformed Event without placement', () => {
    const activity = createTemporalCreateFields({
      title: 'Leggere',
      kind: 'activity',
      timeSemantics: 'unscheduled',
      date: '2026-09-01',
    });
    const malformedEvent = { ...activity, kind: 'event' as const };

    expect(validateTemporalCreateFields(activity)).toEqual([]);
    expect(
      validateTemporalCreateFields(malformedEvent).map((issue) => issue.code),
    ).toContain('temporal.create.event.requires_placement');
  });

  it('builds a true date-span for all-day creation', () => {
    const fields = createTemporalCreateFields({
      title: 'Fiera',
      kind: 'event',
      date: '2026-09-05',
      timeSemantics: 'all-day',
    });
    const placement = buildTemporalCreatePlacement(fields);

    expect(placement?.kind).toBe('date-span');
    if (placement?.kind === 'date-span') {
      expect(placement.startDate.toString()).toBe('2026-09-05');
      expect(placement.endDateExclusive.toString()).toBe('2026-09-06');
    }
  });

  it('preserves floating-local semantics without inventing a timezone', () => {
    const fields = createTemporalCreateFields({
      title: 'Focus',
      date: '2026-09-01',
      startTime: '14:30',
      durationMinutes: 45,
      timeMode: 'floating',
    });
    const placement = buildTemporalCreatePlacement(fields);

    expect(placement?.kind).toBe('floating-local');
    if (placement?.kind === 'floating-local') {
      expect(placement.start.toString()).toBe('2026-09-01T14:30:00');
      expect(placement.end.toString()).toBe('2026-09-01T15:15:00');
    }
  });

  it('builds DST-safe zoned placement through the named timezone', () => {
    const fields = createTemporalCreateFields({
      title: 'DST test',
      date: '2026-03-29',
      startTime: '01:30',
      durationMinutes: 60,
      timeMode: 'zoned',
      timeZoneId: 'Europe/Rome',
    });
    const placement = buildTemporalCreatePlacement(fields);

    expect(placement?.kind).toBe('zoned');
    if (placement?.kind === 'zoned') {
      expect(placement.start.hour).toBe(1);
      expect(placement.end.hour).toBe(3);
      expect(
        Temporal.Instant.compare(
          placement.end.toInstant(),
          placement.start.toInstant(),
        ),
      ).toBeGreaterThan(0);
    }
  });

  it('validates bounded windows and deadline ordering without fabricating placement', () => {
    const baseline = createTemporalCreateFields({
      title: 'Montare video',
      date: '2026-09-01',
      durationMinutes: 180,
    });
    const validWindow = createTemporalCreateFields({
      ...baseline,
      scheduling: {
        ...baseline.scheduling,
        constraintKind: 'bounded-window',
        windowStartDate: '2026-09-02',
        windowStartTime: '18:00',
        windowEndDate: '2026-09-03',
        windowEndTime: '23:00',
        movementPolicy: 'window',
      },
    });
    const invalidDeadline = createTemporalCreateFields({
      ...baseline,
      scheduling: {
        ...baseline.scheduling,
        constraintKind: 'deadline',
        earliestStartDate: '2026-09-05',
        earliestStartTime: '12:00',
        deadlineDate: '2026-09-05',
        deadlineTime: '11:00',
      },
    });

    expect(validateTemporalCreateFields(validWindow)).toEqual([]);
    expect(buildTemporalCreatePlacement(validWindow)).toBeNull();
    expect(
      validateTemporalCreateFields(invalidDeadline).map((issue) => issue.code),
    ).toContain('temporal.create.deadline.invalid');
  });

  it('validates split-session Activity authoring independently from execution instances', () => {
    const baseline = createTemporalCreateFields({
      title: 'Studiare inglese',
      date: '2026-09-01',
      durationMinutes: 90,
    });
    const invalid = createTemporalCreateFields({
      ...baseline,
      execution: {
        ...baseline.execution,
        sessionMode: 'splittable',
        minSessionMinutes: 120,
      },
    });
    const valid = createTemporalCreateFields({
      ...invalid,
      execution: {
        ...invalid.execution,
        minSessionMinutes: 30,
      },
    });

    expect(
      validateTemporalCreateFields(invalid).map((issue) => issue.code),
    ).toContain('temporal.create.minimum_session.invalid');
    expect(validateTemporalCreateFields(valid)).toEqual([]);
  });

  it('validates all four CP6 Event recurrence families', () => {
    const baseline = createTemporalCreateFields({
      title: 'Evento ricorrente',
      kind: 'event',
      date: '2026-09-01',
      timeZoneId: 'Europe/Rome',
    });

    const calendar = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'calendar-wall-clock',
        calendarFrequency: 'weekly',
        weekdays: Object.freeze(['TU', 'TH'] as const),
      },
    });
    const elapsed = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'elapsed-interval',
        elapsedIntervalMinutes: 720,
      },
    });
    const quota = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'quota-per-period',
        quotaCount: 3,
        quotaPeriodKind: 'year',
        quotaPeriodInterval: 1,
        quotaFrame: 'named-zone',
        quotaTimeZoneId: 'Europe/Rome',
      },
    });
    const cycle = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'cyclic-positional',
        cycleLength: 4,
        cyclePositions: Object.freeze([1, 2]),
        cycleUnit: 'day',
        endMode: 'count',
        count: 12,
      },
    });

    expect(validateTemporalCreateFields(calendar)).toEqual([]);
    expect(validateTemporalCreateFields(elapsed)).toEqual([]);
    expect(validateTemporalCreateFields(quota)).toEqual([]);
    expect(validateTemporalCreateFields(cycle)).toEqual([]);
  });

  it('preserves monthly ordinal and yearly calendar intent without generating occurrences', () => {
    const baseline = createTemporalCreateFields({
      title: 'Board review',
      kind: 'event',
      date: '2026-09-15',
    });
    const ordinal = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'calendar-wall-clock',
        calendarFrequency: 'monthly-ordinal',
        calendarOrdinal: -1,
        calendarOrdinalWeekday: 'FR',
      },
    });
    const yearly = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'calendar-wall-clock',
        calendarFrequency: 'yearly',
      },
    });

    expect(validateTemporalCreateFields(ordinal)).toEqual([]);
    expect(validateTemporalCreateFields(yearly)).toEqual([]);
    expect(ordinal.eventRecurrence.calendarOrdinal).toBe(-1);
    expect(ordinal.eventRecurrence.calendarOrdinalWeekday).toBe('FR');
    expect(yearly.eventRecurrence.calendarFrequency).toBe('yearly');
  });

  it('requires a valid explicit quota frame and named zone when selected', () => {
    const baseline = createTemporalCreateFields({
      title: 'Quota',
      kind: 'event',
      date: '2026-09-01',
    });
    const valid = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'quota-per-period',
        quotaCount: 3,
        quotaPeriodKind: 'week',
        quotaFrame: 'named-zone',
        quotaWeekStart: 'MO',
        quotaTimeZoneId: 'Europe/Rome',
      },
    });
    const invalid = createTemporalCreateFields({
      ...valid,
      eventRecurrence: {
        ...valid.eventRecurrence,
        quotaTimeZoneId: 'Europe/Not-A-Zone',
      },
    });

    expect(validateTemporalCreateFields(valid)).toEqual([]);
    expect(
      validateTemporalCreateFields(invalid).map((issue) => issue.code),
    ).toContain('temporal.create.recurrence.quota_timezone_invalid');
  });

  it('rejects malformed CP6 cyclic positions deterministically', () => {
    const baseline = createTemporalCreateFields({
      title: 'Evento ricorrente',
      kind: 'event',
      date: '2026-09-01',
    });
    const duplicate = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'cyclic-positional',
        cycleLength: 4,
        cyclePositions: Object.freeze([1, 1]),
      },
    });
    const outside = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'cyclic-positional',
        cycleLength: 4,
        cyclePositions: Object.freeze([1, 5]),
      },
    });

    expect(
      validateTemporalCreateFields(duplicate).map((issue) => issue.code),
    ).toContain('temporal.create.recurrence.cycle_invalid');
    expect(
      validateTemporalCreateFields(outside).map((issue) => issue.code),
    ).toContain('temporal.create.recurrence.cycle_invalid');
  });

  it('supports infer-provisional without claiming an authoritative Actual', () => {
    const baseline = createTemporalCreateFields({
      title: 'Allenamento',
      date: '2026-09-01',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      confirmation: {
        ...baseline.confirmation,
        outcomePolicy: 'infer-provisional',
      },
    });

    expect(validateTemporalCreateFields(fields)).toEqual([]);
    expect(fields.confirmation.outcomePolicy).toBe('infer-provisional');
  });

  it('discard creates a fresh clean Quick Create session', () => {
    const discarded = discardTemporalCreateSession(
      createTemporalCreateFields({ date: '2026-09-01' }),
    );

    expect(discarded.closeDecision).toBe('none');
    expect(discarded.surface).toBe('quick');
    expect(discarded.draft.current.title).toBe('');
    expect(discarded.draft.dirty).toBe(false);
  });
});
