import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
  type TemporalActivityDataSource,
  type TemporalActivityRecord,
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

function activitySource(
  unplaced: readonly TemporalActivityRecord[] = Object.freeze([]),
): Readonly<{
  source: TemporalActivityDataSource;
  createActivity: ReturnType<
    typeof vi.fn<TemporalActivityDataSource['createActivity']>
  >;
  loadUnplaced: ReturnType<
    typeof vi.fn<TemporalActivityDataSource['loadUnplaced']>
  >;
}> {
  const createActivity = vi.fn<TemporalActivityDataSource['createActivity']>(
    (request) =>
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
  );
  const loadUnplaced = vi.fn<TemporalActivityDataSource['loadUnplaced']>(() =>
    Promise.resolve(Object.freeze([...unplaced])),
  );

  return Object.freeze({
    source: Object.freeze({ createActivity, loadUnplaced }),
    createActivity,
    loadUnplaced,
  });
}

describe('Temporal Create normal-runtime boundary', () => {
  it.each(['production', 'development'])(
    'creates only the canonical B01 unplaced Activity through the remote source in %s',
    async (mode) => {
      const activity = activitySource();
      const runtime = createLocalTemporalCreateRuntime({
        ...runtimeOptions(`runtime-boundary-${mode}`),
        mode,
        activityDataSource: activity.source,
      });

      const execution = await runtime.execute(preparedActivity(runtime));

      expect(activity.createActivity).toHaveBeenCalledTimes(1);
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
        expect(undoResult.failure.code).toBe(
          'temporal.create.undo_unavailable',
        );
      }
    },
  );

  it('refetches canonical unplaced Activities with the backend identity unchanged', async () => {
    const canonical = Object.freeze({
      activityRef: CANONICAL_ACTIVITY_REF,
      title: 'Persistita nel Planning Tray',
      createdAt: Temporal.Instant.from('2026-09-07T12:00:00Z'),
    });
    const activity = activitySource(Object.freeze([canonical]));
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-unplaced-refetch'),
      mode: 'production',
      activityDataSource: activity.source,
    });

    const first = await runtime.list();
    const second = await runtime.list();

    expect(activity.loadUnplaced).toHaveBeenCalledTimes(2);
    expect(first).toHaveLength(1);
    expect(second).toHaveLength(1);
    expect(first[0]).toMatchObject({
      id: CANONICAL_ACTIVITY_REF,
      subject: {
        source: 'native',
        kind: 'activity',
        id: CANONICAL_ACTIVITY_REF,
      },
      title: 'Persistita nel Planning Tray',
      placement: null,
    });
    expect(second[0]?.id).toBe(first[0]?.id);
  });

  it('fails closed for B02/B03 intent instead of dropping unsupported temporal meaning', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-unsupported'),
      mode: 'production',
      activityDataSource: activity.source,
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

    expect(activity.createActivity).not.toHaveBeenCalled();
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

  it('fails closed instead of dropping unpersisted estimated-effort intent in B01', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-estimated-effort'),
      mode: 'production',
      activityDataSource: activity.source,
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Activity con effort non ancora supportato',
        kind: 'activity',
        date: '2026-09-07',
        timeSemantics: 'unscheduled',
        durationMinutes: 60,
        timeZoneId: 'Europe/Rome',
        contextId: 'personale',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected a valid Create preparation');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(activity.createActivity).not.toHaveBeenCalled();
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
