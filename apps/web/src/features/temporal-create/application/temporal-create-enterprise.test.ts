import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
} from '../../temporal';
import {
  buildTemporalCreatePlacement,
  createTemporalCreateFields,
  validateTemporalCreateFields,
} from '../model/temporal-create-session';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

function enterpriseRuntime() {
  const ids = createDeterministicTemporalIdFactory('create-enterprise');
  const clock = createFixedTemporalClock(
    Temporal.Instant.from('2026-09-01T08:00:00Z'),
    'Europe/Rome',
  );
  return createLocalTemporalCreateRuntime({
    ids,
    clock,
    workspace: new InMemoryTemporalWorkspace(ids),
  });
}

describe('Temporal Create enterprise authoring semantics', () => {
  it('creates a true multi-day all-day Event date span', () => {
    const baseline = createTemporalCreateFields({
      title: 'Lucca Comics',
      kind: 'event',
      date: '2026-10-28',
      timeSemantics: 'all-day',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      event: {
        ...baseline.event,
        allDayEndDate: '2026-11-01',
      },
    });

    expect(validateTemporalCreateFields(fields)).toEqual([]);
    const placement = buildTemporalCreatePlacement(fields);
    expect(placement?.kind).toBe('date-span');
    if (placement?.kind === 'date-span') {
      expect(placement.startDate.toString()).toBe('2026-10-28');
      expect(placement.endDateExclusive.toString()).toBe('2026-11-02');
    }
  });

  it('rejects an inverted all-day Event range', () => {
    const baseline = createTemporalCreateFields({
      title: 'Fiera',
      kind: 'event',
      date: '2026-09-05',
      timeSemantics: 'all-day',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      event: { ...baseline.event, allDayEndDate: '2026-09-04' },
    });

    expect(validateTemporalCreateFields(fields).map((issue) => issue.code)).toContain(
      'temporal.create.all_day_range.invalid',
    );
  });

  it('keeps expected duration on an open Activity without fabricating placement', () => {
    const baseline = createTemporalCreateFields({
      title: 'Montare il video',
      durationMinutes: 210,
      date: '2026-09-01',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      scheduling: {
        ...baseline.scheduling,
        constraintKind: 'open',
        movementPolicy: 'free',
      },
    });

    expect(fields.durationMinutes).toBe(210);
    expect(fields.timeSemantics).toBe('unscheduled');
    expect(buildTemporalCreatePlacement(fields)).toBeNull();
    expect(validateTemporalCreateFields(fields)).toEqual([]);
  });

  it('preserves provider intent and deep Activity policy in the local rich record', async () => {
    const runtime = enterpriseRuntime();
    const eventBase = createTemporalCreateFields({
      title: 'Call cliente',
      kind: 'event',
      date: '2026-09-01',
      startTime: '16:00',
      durationMinutes: 60,
    });
    const eventFields = createTemporalCreateFields({
      ...eventBase,
      event: {
        ...eventBase.event,
        location: 'Studio / remoto',
        visibility: 'private',
        participants: 'cliente@example.com\ncollega@example.com',
        resources: 'Sala Atlas',
        conferenceMode: 'provider-default',
      },
    });
    const preparation = runtime.prepare(eventFields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected Event Create to be ready');
    }
    await runtime.execute(preparation.prepared);

    const record = (await runtime.listRecords())[0];
    expect(record?.metadata.specification.event.participants).toContain(
      'cliente@example.com',
    );
    expect(record?.metadata.specification.event.resources).toBe('Sala Atlas');
    expect(record?.metadata.specification.event.conferenceMode).toBe(
      'provider-default',
    );
  });

  it('keeps fallback and session limits as planning intent, not Session records', async () => {
    const runtime = enterpriseRuntime();
    const baseline = createTemporalCreateFields({
      title: 'Studio intensivo',
      durationMinutes: 180,
      date: '2026-09-01',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      scheduling: {
        ...baseline.scheduling,
        constraintKind: 'deadline',
        earliestStartDate: '2026-09-01',
        earliestStartTime: '09:00',
        deadlineDate: '2026-09-05',
        deadlineTime: '22:00',
        fallbackPolicy: 'shorten-or-split',
      },
      execution: {
        ...baseline.execution,
        sessionMode: 'splittable',
        minSessionMinutes: 45,
        maxSessions: 4,
      },
      recurrence: {
        ...baseline.recurrence,
        frequency: 'weekly',
        weekdays: Object.freeze(['MO', 'WE', 'FR'] as const),
        endMode: 'count',
        count: 8,
      },
    });

    const preparation = runtime.prepare(fields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected Activity Create to be ready');
    }
    const execution = await runtime.execute(preparation.prepared);
    expect(execution.effect?.projection.placement).toBeNull();
    expect(execution.effect?.projection.capabilities).toContain('recurrence');
    expect(execution.effect?.projection.capabilities).toContain('execution');

    const specification = (await runtime.listRecords())[0]?.metadata.specification;
    expect(specification?.scheduling.fallbackPolicy).toBe('shorten-or-split');
    expect(specification?.execution.maxSessions).toBe(4);
    expect(specification?.recurrence.weekdays).toEqual(['MO', 'WE', 'FR']);
  });
});
