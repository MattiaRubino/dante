import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createLocalTemporalCreateRuntime,
  type TemporalCreatePreparedOperation,
} from './temporal-create-runtime';

function runtime() {
  const ids = createDeterministicTemporalIdFactory('c1-rich');
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

describe('Temporal Create rich application runtime', () => {
  it('retains rich Activity scheduling/execution intent without fake recurrence or placement', async () => {
    const createRuntime = runtime();
    const baseline = createTemporalCreateFields({
      title: 'Montare video',
      date: '2026-09-01',
      durationMinutes: 180,
      notes: 'Export finale',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      scheduling: {
        ...baseline.scheduling,
        constraintKind: 'bounded-window',
        windowStartDate: '2026-09-01',
        windowStartTime: '18:00',
        windowEndDate: '2026-09-03',
        windowEndTime: '23:00',
        movementPolicy: 'window',
      },
      execution: {
        ...baseline.execution,
        sessionMode: 'splittable',
        minSessionMinutes: 45,
      },
    });
    const preparation = createRuntime.prepare(fields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready rich Create operation');
    }

    const execution = await createRuntime.execute(preparation.prepared);
    const records = await createRuntime.listRecords();

    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.projection.placement).toBeNull();
    expect(execution.effect?.projection.capabilities).not.toContain('recurrence');
    expect(execution.effect?.projection.capabilities).toContain('execution');
    expect(records).toHaveLength(1);
    expect(records[0]?.metadata.recurrenceOwner).toBeNull();
    expect(records[0]?.metadata.specification.scheduling.constraintKind).toBe(
      'bounded-window',
    );
    expect(records[0]?.metadata.specification.execution.minSessionMinutes).toBe(
      45,
    );
    expect(records[0]?.metadata.specification.eventRecurrence.patternKind).toBe(
      'none',
    );
  });

  it('marks Event recurrence capability only for an Event recurrence owner', async () => {
    const createRuntime = runtime();
    const baseline = createTemporalCreateFields({
      title: 'Call settimanale',
      kind: 'event',
      date: '2026-09-01',
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'calendar-wall-clock',
        calendarFrequency: 'weekly',
        weekdays: Object.freeze(['TU'] as const),
      },
    });
    const preparation = createRuntime.prepare(fields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready recurring Event');
    }

    const execution = await createRuntime.execute(preparation.prepared);
    const record = (await createRuntime.listRecords())[0];

    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.projection.capabilities).toContain('recurrence');
    expect(record?.metadata.recurrenceOwner).toBe('event');
    expect(record?.metadata.specification.eventRecurrence.patternKind).toBe(
      'calendar-wall-clock',
    );
  });

  it('preserves repeated Activity intent as Routine-backed without pretending the Activity owns recurrence', async () => {
    const createRuntime = runtime();
    const baseline = createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-09-01',
      startTime: '18:00',
      durationMinutes: 60,
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: {
        ...baseline.eventRecurrence,
        patternKind: 'quota-per-period',
        quotaCount: 3,
        quotaPeriodKind: 'week',
        quotaPeriodInterval: 1,
        quotaFrame: 'floating-local',
        quotaWeekStart: 'MO',
      },
    });
    const preparation = createRuntime.prepare(fields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Routine-backed Activity repetition');
    }

    const execution = await createRuntime.execute(preparation.prepared);
    const records = await createRuntime.listRecords();

    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.projection.capabilities).not.toContain('recurrence');
    expect(records).toHaveLength(1);
    expect(records[0]?.metadata.recurrenceOwner).toBe('routine');
    expect(records[0]?.metadata.specification.eventRecurrence.patternKind).toBe(
      'quota-per-period',
    );
    expect(records[0]?.metadata.specification.eventRecurrence.quotaCount).toBe(3);
  });

  it('keeps exact prepared-command replay idempotent without duplicating rich records', async () => {
    const createRuntime = runtime();
    const preparation = createRuntime.prepare(
      createTemporalCreateFields({
        title: 'Call',
        kind: 'event',
        date: '2026-09-01',
        startTime: '11:00',
        durationMinutes: 30,
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }

    const first = await createRuntime.execute(preparation.prepared);
    const replay = await createRuntime.execute(preparation.prepared);

    expect(replay.result).toBe(first.result);
    expect(await createRuntime.list()).toHaveLength(1);
    expect(await createRuntime.listRecords()).toHaveLength(1);
  });

  it('rejects operation-id reuse when only deep Event intent changes', async () => {
    const createRuntime = runtime();
    const base = createTemporalCreateFields({
      title: 'Call',
      kind: 'event',
      date: '2026-09-01',
      notes: 'Original note',
    });
    const original = createTemporalCreateFields({
      ...base,
      event: {
        ...base.event,
        purpose: 'Review',
        requiredParticipants: 'cliente@example.com',
      },
    });
    const preparation = createRuntime.prepare(original);
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }

    const first = await createRuntime.execute(preparation.prepared);
    expect(first.result.status).toBe('applied');

    const changedSpecification = createTemporalCreateFields({
      ...preparation.prepared.metadata.specification,
      event: {
        ...preparation.prepared.metadata.specification.event,
        purpose: 'Changed on replay',
      },
    });
    const tampered = Object.freeze({
      ...preparation.prepared,
      metadata: Object.freeze({
        ...preparation.prepared.metadata,
        specification: changedSpecification,
      }),
    }) satisfies TemporalCreatePreparedOperation;

    const collision = await createRuntime.execute(tampered);
    const records = await createRuntime.listRecords();

    expect(collision.effect).toBeNull();
    expect(collision.result.status).toBe('rejected');
    if (collision.result.status === 'rejected') {
      expect(collision.result.code).toBe('operation-id-reused');
    }
    expect(records).toHaveLength(1);
    expect(records[0]?.metadata.notes).toBe('Original note');
    expect(records[0]?.metadata.specification.event.purpose).toBe('Review');
    expect(
      records[0]?.metadata.specification.event.requiredParticipants,
    ).toContain('cliente@example.com');
  });

  it('rejects operation-id reuse when only Event recurrence semantics change', async () => {
    const createRuntime = runtime();
    const base = createTemporalCreateFields({
      title: 'Recurring review',
      kind: 'event',
      date: '2026-09-01',
    });
    const original = createTemporalCreateFields({
      ...base,
      eventRecurrence: {
        ...base.eventRecurrence,
        patternKind: 'elapsed-interval',
        elapsedIntervalMinutes: 1440,
      },
    });
    const preparation = createRuntime.prepare(original);
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready recurring Event');
    }
    await createRuntime.execute(preparation.prepared);

    const changedSpecification = createTemporalCreateFields({
      ...original,
      eventRecurrence: {
        ...original.eventRecurrence,
        elapsedIntervalMinutes: 2880,
      },
    });
    const tampered = Object.freeze({
      ...preparation.prepared,
      metadata: Object.freeze({
        ...preparation.prepared.metadata,
        specification: changedSpecification,
      }),
    }) satisfies TemporalCreatePreparedOperation;

    const collision = await createRuntime.execute(tampered);

    expect(collision.effect).toBeNull();
    expect(collision.result.status).toBe('rejected');
  });

  it('undo removes both F0 projection and its local rich specification', async () => {
    const createRuntime = runtime();
    const preparation = createRuntime.prepare(
      createTemporalCreateFields({
        title: 'Allenamento',
        date: '2026-09-01',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }

    const execution = await createRuntime.execute(preparation.prepared);
    expect(await createRuntime.listRecords()).toHaveLength(1);

    const undo = await execution.effect?.undo();
    expect(undo?.status).toBe('applied');
    expect(await createRuntime.list()).toHaveLength(0);
    expect(await createRuntime.listRecords()).toHaveLength(0);
  });
});
