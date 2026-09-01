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
    expect(session.draft.current.title).toBe('');
    expect(session.draft.current.kind).toBe('activity');
    expect(session.draft.current.timeSemantics).toBe('timed');
    expect(session.draft.dirty).toBe(false);
  });

  it('marks edits dirty and returning to baseline clean', () => {
    const initial = createTemporalCreateSession();
    const edited = updateTemporalCreateTitle(initial, 'Allenamento');
    const restored = updateTemporalCreateTitle(edited, '');

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

  it('continues editing and toggles details without losing draft state', () => {
    const edited = updateTemporalCreateTitle(
      createTemporalCreateSession(),
      'Scrivere una canzone',
    );
    const protectedSession = requestTemporalCreateClose(edited).session;
    const resumed = continueTemporalCreateEditing(protectedSession);
    const expanded = setTemporalCreateDetailsOpen(resumed, true);

    expect(expanded.closeDecision).toBe('none');
    expect(expanded.detailsOpen).toBe(true);
    expect(expanded.draft.current.title).toBe('Scrivere una canzone');
    expect(expanded.draft.dirty).toBe(true);
  });

  it('rejects event-without-placement while allowing an unscheduled Activity', () => {
    const activity = createTemporalCreateFields({
      title: 'Leggere',
      kind: 'activity',
      timeSemantics: 'unscheduled',
      date: '2026-09-01',
    });
    const event = { ...activity, kind: 'event' as const };

    expect(validateTemporalCreateFields(activity)).toEqual([]);
    expect(
      validateTemporalCreateFields(event).map((issue) => issue.code),
    ).toContain('temporal.create.event.requires_placement');
    expect(buildTemporalCreatePlacement(activity)).toBeNull();
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

  it('discard creates a fresh clean session', () => {
    const discarded = discardTemporalCreateSession(
      createTemporalCreateFields({ date: '2026-09-01' }),
    );

    expect(discarded.closeDecision).toBe('none');
    expect(discarded.draft.current.title).toBe('');
    expect(discarded.draft.dirty).toBe(false);
  });
});
