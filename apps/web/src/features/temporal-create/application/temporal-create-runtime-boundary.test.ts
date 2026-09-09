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
const CANONICAL_SCHEDULE_REF = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const CANONICAL_PLACEMENT_STATE_REF =
  '0199a8c0-7e73-7de2-8cf2-c4062517839f';

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
  createScheduledActivity: ReturnType<
    typeof vi.fn<TemporalActivityDataSource['createScheduledActivity']>
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
  const createScheduledActivity = vi.fn<
    TemporalActivityDataSource['createScheduledActivity']
  >((request) =>
    Promise.resolve(
      Object.freeze({
        activity: Object.freeze({
          activityRef: CANONICAL_ACTIVITY_REF,
          title: request.title,
          createdAt: Temporal.Instant.from('2026-09-07T12:00:00Z'),
        }),
        schedule: Object.freeze({
          scheduleRef: CANONICAL_SCHEDULE_REF,
          placementMaterialStateRef: CANONICAL_PLACEMENT_STATE_REF,
          temporalForm: 'floating-local' as const,
          startsLocalAt: request.placement.startsLocalAt,
          endsLocalAt: request.placement.endsLocalAt,
        }),
        replayed: false,
      }),
    ),
  );
  const loadUnplaced = vi.fn<TemporalActivityDataSource['loadUnplaced']>(() =>
    Promise.resolve(Object.freeze([...unplaced])),
  );

  return Object.freeze({
    source: Object.freeze({
      createActivity,
      createScheduledActivity,
      loadUnplaced,
    }),
    createActivity,
    createScheduledActivity,
    loadUnplaced,
  });
}

describe('Temporal Create normal-runtime boundary', () => {
  it.each(['production', 'development'])(
    'creates the canonical B01 unplaced Activity through the remote source in %s',
    async (mode) => {
      const activity = activitySource();
      const runtime = createLocalTemporalCreateRuntime({
        ...runtimeOptions(`runtime-boundary-${mode}`),
        mode,
        activityDataSource: activity.source,
      });

      const execution = await runtime.execute(preparedActivity(runtime));

      expect(activity.createActivity).toHaveBeenCalledTimes(1);
      expect(activity.createScheduledActivity).not.toHaveBeenCalled();
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

  it('activates only the exact B02-A floating-local same-day scheduled Activity path', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-b02a'),
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
        durationMinutes: 30,
        timeMode: 'floating',
        timeZoneId: 'Europe/Rome',
        contextId: 'personale',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected a valid B02-A Create preparation');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(activity.createActivity).not.toHaveBeenCalled();
    expect(activity.createScheduledActivity).toHaveBeenCalledTimes(1);
    expect(activity.createScheduledActivity).toHaveBeenCalledWith({
      operationId: preparation.prepared.operationId,
      title: 'Activity già collocata',
      placement: {
        kind: 'floating-local-interval',
        startsLocalAt: expect.anything(),
        endsLocalAt: expect.anything(),
      },
    });
    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.projection).toMatchObject({
      id: CANONICAL_SCHEDULE_REF,
      subject: {
        source: 'native',
        kind: 'activity',
        id: CANONICAL_ACTIVITY_REF,
      },
      title: 'Activity già collocata',
      placement: {
        kind: 'floating-local',
      },
      capabilities: [],
    });
    expect(
      execution.effect?.projection.placement?.kind === 'floating-local'
        ? execution.effect.projection.placement.start.toString()
        : null,
    ).toBe('2026-09-07T15:00:00');
    expect(
      execution.effect?.projection.placement?.kind === 'floating-local'
        ? execution.effect.projection.placement.end.toString()
        : null,
    ).toBe('2026-09-07T15:30:00');
    expect(execution.effect?.undoAvailable).toBe(false);
  });

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

  it('still fails closed for placement forms and owner semantics outside B02-A', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-unsupported'),
      mode: 'production',
      activityDataSource: activity.source,
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Activity zoned non ancora attivata',
        kind: 'activity',
        date: '2026-09-07',
        timeSemantics: 'timed',
        startTime: '15:00',
        timeMode: 'zoned',
        timeZoneId: 'Europe/Rome',
        contextId: 'personale',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected a valid Create preparation');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(activity.createActivity).not.toHaveBeenCalled();
    expect(activity.createScheduledActivity).not.toHaveBeenCalled();
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

  it('fails closed instead of dropping unpersisted rich B02-A intent', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-b02a-rich'),
      mode: 'production',
      activityDataSource: activity.source,
    });
    const baseline = createTemporalCreateFields({
      title: 'Activity con reminder non ancora supportato',
      kind: 'activity',
      date: '2026-09-07',
      timeSemantics: 'timed',
      startTime: '15:00',
      durationMinutes: 30,
      timeMode: 'floating',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        ...baseline,
        confirmation: {
          ...baseline.confirmation,
          reminderLeadMinutes: 15,
        },
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected a valid Create preparation');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(activity.createScheduledActivity).not.toHaveBeenCalled();
    expect(execution.effect).toBeNull();
    expect(execution.result.status).toBe('failed');
    if (execution.result.status === 'failed') {
      expect(execution.result.failure.code).toBe(
        'temporal.create.capability_not_available',
      );
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
    expect(activity.createScheduledActivity).not.toHaveBeenCalled();
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
