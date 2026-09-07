import { Temporal } from '@dante/time';
import { describe, expect, it } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

function runtimeOptions(seed: string) {
  return {
    ids: createDeterministicTemporalIdFactory(seed),
    clock: createFixedTemporalClock(
      Temporal.Instant.from('2026-09-07T12:00:00Z'),
      'Europe/Rome',
    ),
  } as const;
}

function preparedCreate(
  runtime: ReturnType<typeof createLocalTemporalCreateRuntime>,
) {
  const preparation = runtime.prepare(
    createTemporalCreateFields({
      title: 'Attività reale',
      kind: 'activity',
      date: '2026-09-07',
      startTime: '15:00',
      durationMinutes: 60,
    }),
  );
  if (preparation.status !== 'ready') {
    throw new Error('Expected a valid Create preparation');
  }
  return preparation.prepared;
}

describe('Temporal Create normal-runtime boundary', () => {
  it.each(['production', 'development'])(
    'never reports local applied success in %s without an explicit authoritative workspace',
    async (mode) => {
      const runtime = createLocalTemporalCreateRuntime({
        ...runtimeOptions(`runtime-boundary-${mode}`),
        mode,
      });

      const execution = await runtime.execute(preparedCreate(runtime));

      expect(execution.effect).toBeNull();
      expect(execution.result.status).toBe('failed');
      if (execution.result.status === 'failed') {
        expect(execution.result.failure).toEqual({
          kind: 'unavailable',
          code: 'temporal.create.backend_unavailable',
          retryable: false,
        });
      }
      expect(await runtime.list()).toEqual([]);
      expect(await runtime.listRecords()).toEqual([]);
    },
  );

  it('keeps the in-memory workspace as the explicit test-mode default only', async () => {
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-test'),
      mode: 'test',
    });

    const execution = await runtime.execute(preparedCreate(runtime));

    expect(execution.result.status).toBe('applied');
    expect(execution.effect).not.toBeNull();
    expect(await runtime.list()).toHaveLength(1);
  });

  it('honors an explicitly injected workspace regardless of process mode', async () => {
    const options = runtimeOptions('runtime-boundary-injected');
    const runtime = createLocalTemporalCreateRuntime({
      ...options,
      mode: 'production',
      workspace: new InMemoryTemporalWorkspace(options.ids),
    });

    const execution = await runtime.execute(preparedCreate(runtime));

    expect(execution.result.status).toBe('applied');
    expect(execution.effect).not.toBeNull();
    expect(await runtime.listRecords()).toHaveLength(1);
  });
});
