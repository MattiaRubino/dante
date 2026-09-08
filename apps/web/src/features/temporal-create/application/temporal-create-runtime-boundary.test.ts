import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
  type TemporalActivityDataSource,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

const CANONICAL_ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';

function runtimeOptions(seed: string) {
  return {
    ids: createDeterministicTemporalIdFactory(seed),
    clock: createFixedTemporalClock(
      Temporal.Instant.from('2026-09-07T12:00:00Z'),
      'Europe/Rome',
    ),
  } as const;
}

function preparedActivity(
  runtime: ReturnType<typeof createLocalTemporalCreateRuntime>,
) {
  const preparation = runtime.prepare(
    createTemporalCreateFields({
      title: 'Attività reale',
      kind: 'activity',
      date: '2026-09-07',
      timeSemantics: 'unscheduled',
      contextId: 'personale',
      timeZoneId: 'Europe/Rome',
    }),
  );
  if (preparation.status !== 'ready') {
    throw new Error('Expected a valid Create preparation');
  }
  return preparation.prepared;
}

function activitySource(): TemporalActivityDataSource {
  return Object.freeze({
    createActivity: vi.fn((request) =>
      Promise.resolve(
        Object.freeze({
          activity: Object.freeze({
            activityRef: CANONICAL_ACTIVITY_REF,
            title: request.title,
            createdAt: Temporal.Instant.from('2026-09-07T12:00:00Z'),
          }),
          replayed: false,
        }),
      ),
    ),
    loadUnplaced: vi.fn(() => Promise.resolve(Object.freeze([]))),
  });
}

describe('Temporal Create normal-runtime boundary', () => {
  it.each(['production', 'development'])(
    'creates only the canonical B01 unplaced Activity through the remote source in %s',
    async (mode) => {
      const source = activitySource();
      const runtime = createLocalTemporalCreateRuntime({
        ...runtimeOptions(`runtime-boundary-${mode}`),
        mode,
        activityDataSource: source,
      });

      const execution = await runtime.execute(preparedActivity(runtime));

      expect(source.createActivity).toHaveBeenCalledTimes(1);
      expect(execution.result.status).toBe('applied');
      expect(execution.effect).not.toBeNull();
      expect(execution.effect?.projection).toMatchObject({
        id: CANONICAL_ACTIVITY_REF,
        subject: {
          source: 'native',
          kind: 'activity',
          id: CANONICAL_ACTIVITY_REF,
        },
        title: 'Attività reale',
        placement: null,
        capabilities: [],
      });
      expect(execution.effect?.undoAvailable).toBe(false);
      expect(execution.effect?.undoToken).toBeNull();
      const undoResult = await execution.effect?.undo();
      expect(undoResult?.status).toBe('failed');
      if (undoResult?.status === 'failed') {
        expect(undoResult.failure.code).toBe('temporal.create.undo_unavailable');
      }
    },
  );

  it('fails closed for B02/B03 intent instead of dropping unsupported temporal meaning', async () => {
    const source = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-unsupported'),
      mode: 'production',
      activityDataSource: source,
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Activity già collocata',
        kind: 'activity',
        date: '2026-09-07',
        timeSemantics: 'timed',
        startTime: '15:00',
        timeZoneId: 'Europe/Rome',
        contextId: 'personale',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected a valid Create preparation');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(source.createActivity).not.toHaveBeenCalled();
    expect(execution.effect).toBeNull();
    expect(execution.result.status).toBe('failed');
    if (execution.result.status === 'failed') {
      expect(execution.result.failure).toEqual({
        kind: 'unavailable',
        code: 'temporal.create.capability_not_available',
        retryable: false,
      });
    }
  });

  it('keeps the in-memory workspace as the explicit test-mode default only', async () => {
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-test'),
      mode: 'test',
    });

    const execution = await runtime.execute(preparedActivity(runtime));

    expect(execution.result.status).toBe('applied');
    expect(execution.effect).not.toBeNull();
    expect(execution.effect?.undoAvailable).toBe(true);
    expect(await runtime.list()).toHaveLength(1);
  });

  it('honors an explicitly injected workspace regardless of process mode', async () => {
    const options = runtimeOptions('runtime-boundary-injected');
    const runtime = createLocalTemporalCreateRuntime({
      ...options,
      mode: 'production',
      workspace: new InMemoryTemporalWorkspace(options.ids),
    });

    const execution = await runtime.execute(preparedActivity(runtime));

    expect(execution.result.status).toBe('applied');
    expect(execution.effect).not.toBeNull();
    expect(execution.effect?.undoAvailable).toBe(true);
    expect(await runtime.listRecords()).toHaveLength(1);
  });
});
