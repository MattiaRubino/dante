import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

function runtime() {
  const ids = createDeterministicTemporalIdFactory('c1');
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

describe('Temporal Create application runtime', () => {
  it('rejects an invalid draft before command execution', () => {
    const preparation = runtime().prepare(
      createTemporalCreateFields({
        date: '2026-09-01',
        title: '',
      }),
    );

    expect(preparation.status).toBe('invalid');
    if (preparation.status === 'invalid') {
      expect(preparation.issues.map((issue) => issue.code)).toContain(
        'temporal.projection.title.required',
      );
    }
  });

  it('creates an Activity through F0 with truthful capabilities and metadata', async () => {
    const createRuntime = runtime();
    const preparation = createRuntime.prepare(
      createTemporalCreateFields({
        title: 'Allenamento',
        date: '2026-09-01',
        startTime: '18:00',
        durationMinutes: 60,
        contextId: 'salute',
        notes: 'Circuito',
      }),
    );

    expect(preparation.status).toBe('ready');
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }
    const execution = await createRuntime.execute(preparation.prepared);

    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.projection.title).toBe('Allenamento');
    expect(execution.effect?.metadata.kind).toBe('activity');
    expect(execution.effect?.metadata.contextId).toBe('salute');
    expect(execution.effect?.projection.capabilities).toContain('execution');
    expect(execution.effect?.projection.capabilities).toContain('actual');
  });

  it('replays the exact same prepared operation idempotently', async () => {
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
    expect((await createRuntime.list()).length).toBe(1);
  });

  it('undoes an applied Create through the F0 undo command', async () => {
    const createRuntime = runtime();
    const preparation = createRuntime.prepare(
      createTemporalCreateFields({
        title: 'Promemoria',
        date: '2026-09-01',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected ready Create operation');
    }

    const execution = await createRuntime.execute(preparation.prepared);
    expect((await createRuntime.list()).length).toBe(1);

    const undo = await execution.effect?.undo();
    expect(undo?.status).toBe('applied');
    expect((await createRuntime.list()).length).toBe(0);
  });
});
