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
    expect(session.draft.current.recurrence.frequency).toBe('none');
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

  it('continues editing and changes presentation depth without losing draft state', () => {
    const edited = updateTemporalCreateTitle(
      createTemporalCreateSession(),
      'Scrivere una canzone',
    );
    const protectedSession = requestTemporalCreateClose(edited).session;
    const resumed = continueTemporalCreateEditing(protectedSession);
    const expanded = setTemporalCreateDetailsOpen(resumed, true);
    const full = setTemporalCreateSurface(expanded, 'full');

    expect(full.closeDecision).toBe('none');
    expect(full.surface).toBe('full');
    expect(full.detailsOpen).toBe(true);
    expect(full.draft.current.title).toBe('Scrivere una canzone');
    expect(full.draft.dirty).toBe(true);
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

  it('validates split-session and recurrence authoring independently from occurrences', () => {
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
      recurrence: {
        ...baseline.recurrence,
        frequency: 'weekly',
        weekdays: Object.freeze([]),
      },
    });
    const valid = createTemporalCreateFields({
      ...invalid,
      execution: {
        ...invalid.execution,
        minSessionMinutes: 30,
      },
      recurrence: {
        ...invalid.recurrence,
        weekdays: Object.freeze(['MO', 'WE', 'FR'] as const),
        endMode: 'count',
        count: 12,
      },
    });

    expect(validateTemporalCreateFields(invalid).map((issue) => issue.code)).toEqual(
      expect.arrayContaining([
        'temporal.create.minimum_session.invalid',
        'temporal.create.recurrence.weekdays_required',
      ]),
    );
    expect(validateTemporalCreateFields(valid)).toEqual([]);
    expect(valid.recurrence.frequency).toBe('weekly');
    expect(valid.recurrence.weekdays).toEqual(['MO', 'WE', 'FR']);
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
