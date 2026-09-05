import { describe, expect, it } from 'vitest';

import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  prepareTemporalCreateHandoff,
  temporalCreateHandoffRegistry,
} from './temporal-create-handoff';

describe('Temporal Create owner handoff boundary', () => {
  it('publishes one explicit deferred descriptor for every supported owning vertical', () => {
    const registry = temporalCreateHandoffRegistry();
    const targets = registry.map((descriptor) => descriptor.target);

    expect(targets).toEqual([
      'project',
      'goal',
      'routine',
      'program',
      'world',
      'template',
      'reminder',
      'block',
      'asset',
    ]);
    expect(new Set(targets).size).toBe(targets.length);
    expect(
      registry.every((descriptor) => descriptor.availability === 'deferred'),
    ).toBe(true);
    expect(registry.every((descriptor) => descriptor.preservesDraft)).toBe(
      true,
    );
    expect(Object.isFrozen(registry)).toBe(true);
    expect(registry.every((descriptor) => Object.isFrozen(descriptor))).toBe(
      true,
    );
    expect(registry.some((descriptor) => 'route' in descriptor)).toBe(false);
  });

  it('prepares an immutable normalized snapshot without fabricating navigation or execution', () => {
    const baseline = createTemporalCreateFields({
      title: 'Review cliente',
      kind: 'event',
      date: '2026-09-02',
      startTime: '16:00',
      durationMinutes: 90,
      timeMode: 'zoned',
      timeZoneId: 'Europe/Rome',
      contextId: 'focus',
      notes: 'Portare decisioni e rischi',
    });
    const fields = {
      ...baseline,
      event: {
        ...baseline.event,
        purpose: 'Chiudere il piano',
        requiredParticipants: 'cliente@example.com',
      },
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'cyclic-positional' as const,
        cycleLength: 4,
        cyclePositions: [1, 3],
      },
    };

    const handoff = prepareTemporalCreateHandoff('project', fields);

    expect(handoff.source).toBe('timeline-create');
    expect(handoff.target).toBe('project');
    expect(handoff.availability).toBe('deferred');
    expect(handoff.draftSnapshot.title).toBe('Review cliente');
    expect(handoff.draftSnapshot.contextId).toBe('focus');
    expect(handoff.draftSnapshot.date).toBe('2026-09-02');
    expect(handoff.draftSnapshot.startTime).toBe('16:00');
    expect(handoff.draftSnapshot.durationMinutes).toBe(90);
    expect(handoff.draftSnapshot.notes).toBe('Portare decisioni e rischi');
    expect(handoff.draftSnapshot.event.purpose).toBe('Chiudere il piano');
    expect(handoff.draftSnapshot.event.requiredParticipants).toContain(
      'cliente@example.com',
    );
    expect(handoff.draftSnapshot.eventRecurrence.cyclePositions).toEqual([
      1, 3,
    ]);
    expect(Object.isFrozen(handoff)).toBe(true);
    expect(Object.isFrozen(handoff.draftSnapshot)).toBe(true);
    expect(Object.isFrozen(handoff.draftSnapshot.event)).toBe(true);
    expect(Object.isFrozen(handoff.draftSnapshot.eventRecurrence)).toBe(true);
    expect(
      Object.isFrozen(handoff.draftSnapshot.eventRecurrence.cyclePositions),
    ).toBe(true);
    expect('route' in handoff).toBe(false);
    expect('href' in handoff).toBe(false);
  });

  it('re-normalizes ownership invariants so an Activity handoff cannot carry Event recurrence', () => {
    const baseline = createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-09-02',
    });
    const contaminated = {
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'elapsed-interval' as const,
        elapsedIntervalMinutes: 1440,
      },
    };

    const handoff = prepareTemporalCreateHandoff('routine', contaminated);

    expect(handoff.draftSnapshot.kind).toBe('activity');
    expect(handoff.draftSnapshot.eventRecurrence.patternKind).toBe('none');
  });
});
