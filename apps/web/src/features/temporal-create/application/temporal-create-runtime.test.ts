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
  it('retains rich Activity intent separately from the minimal Timeline projection', async () => {
    const createRuntime = runtime();
    const baseline = createTemporalCreateFields({
      title: 'Montare video',
      date: '2026-09-01',
      durationMinutes: 180,
      notes: 'Export finale',
      tags: 'video, musica',
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
      recurrence: {
        ...baseline.recurrence,
        frequency: 'weekly',
        weekdays: Object.freeze(['MO', 'WE'] as const),
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
    expect(execution.effect?.projection.capabilities).toContain('recurrence');
    expect(records).toHaveLength(1);
    expect(records[0]?.metadata.specification.scheduling.constraintKind).toBe(
      'bounded-window',
    );
    expect(records[0]?.metadata.specification.execution.minSessionMinutes).toBe(
      45,
    );
    expect(records[0]?.metadata.specification.tags).toBe('video, musica');
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

  it('rejects operation-id reuse when only the rich Create intent changes', async () => {
    const createRuntime = runtime();
    const preparation = createRuntime.prepare(
      createTemporalCreateFields({
        title: 'Call',
        kind: 'event',
        date: '2026-09-01',
        notes: 'Original note',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }

    const first = await createRuntime.execute(preparation.prepared);
    expect(first.result.status).toBe('applied');

    const changedSpecification = createTemporalCreateFields({
      ...preparation.prepared.metadata.specification,
      notes: 'Changed on replay',
    });
    const tampered = Object.freeze({
      ...preparation.prepared,
      metadata: Object.freeze({
        ...preparation.prepared.metadata,
        notes: 'Changed on replay',
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
    expect(records[0]?.metadata.specification.notes).toBe('Original note');
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
