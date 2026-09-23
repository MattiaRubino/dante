import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  InMemoryTemporalWorkspace,
  type TemporalActivityDataSource,
  type TemporalActivityRecord,
  type TemporalAcceptedSchedulePlacement,
  type TemporalSchedulePlacementInput,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

const CANONICAL_ACTIVITY_REF = '0199a8c0-5e71-7bc0-8ad0-a2f403f5617d';
const CANONICAL_SCHEDULE_REF = '0199a8c0-6e72-7cd1-9be1-b3f51406728e';
const CANONICAL_PLACEMENT_STATE_REF = '0199a8c0-7e73-7de2-8cf2-c4062517839f';
const CANONICAL_LIFE_AREA_REF = '0199a8c0-8e74-7ee3-8df2-d5073628940a';

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
      contextId: CANONICAL_LIFE_AREA_REF,
      timeZoneId: 'Europe/Rome',
    }),
  );
  if (preparation.status !== 'ready') {
    throw new Error('Expected a valid Create preparation');
  }
  return preparation.prepared;
}

function acceptedPlacement(
  placement: TemporalSchedulePlacementInput,
): TemporalAcceptedSchedulePlacement {
  switch (placement.kind) {
    case 'date-span':
      return Object.freeze({ ...placement });
    case 'floating-local-interval':
      return Object.freeze({ ...placement });
    case 'named-zone-local-interval':
      return Object.freeze({
        kind: placement.kind,
        startsLocalAt: placement.startsLocalAt,
        endsLocalAt: placement.endsLocalAt,
        zoneId: placement.zoneId,
        resolvedStartAt: placement.startsLocalAt
          .toZonedDateTime(placement.zoneId, {
            disambiguation: placement.disambiguation,
          })
          .toInstant(),
        resolvedEndAt: placement.endsLocalAt
          .toZonedDateTime(placement.zoneId, {
            disambiguation: placement.disambiguation,
          })
          .toInstant(),
      });
    case 'absolute-interval':
      return Object.freeze({ ...placement });
    case 'coarse-local-period':
      return Object.freeze({ ...placement });
  }
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
  establishActivitySchedule: ReturnType<
    typeof vi.fn<TemporalActivityDataSource['establishActivitySchedule']>
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
          placement: acceptedPlacement(request.placement),
        }),
        replayed: false,
      }),
    ),
  );
  const establishActivitySchedule = vi.fn<
    TemporalActivityDataSource['establishActivitySchedule']
  >((request) =>
    Promise.resolve(
      Object.freeze({
        activity: Object.freeze({
          activityRef: request.activityRef,
          title: 'Persistita nel Planning Tray',
          createdAt: Temporal.Instant.from('2026-09-07T12:00:00Z'),
        }),
        schedule: Object.freeze({
          scheduleRef: CANONICAL_SCHEDULE_REF,
          placementMaterialStateRef: CANONICAL_PLACEMENT_STATE_REF,
          placement: acceptedPlacement(request.placement),
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
      establishActivitySchedule,
      loadUnplaced,
    }),
    createActivity,
    createScheduledActivity,
    establishActivitySchedule,
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

  it('creates an exact floating-local Activity through the canonical B02-E path', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-b02e-floating'),
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
        contextId: CANONICAL_LIFE_AREA_REF,
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected a valid B02-E Create preparation');
    }
    const execution = await runtime.execute(preparation.prepared);

    expect(activity.createActivity).not.toHaveBeenCalled();
    expect(activity.createScheduledActivity).toHaveBeenCalledTimes(1);
    const scheduledRequest = activity.createScheduledActivity.mock.calls[0]?.[0];
    expect(scheduledRequest?.placement.kind).toBe('floating-local-interval');
    if (scheduledRequest?.placement.kind !== 'floating-local-interval') {
      throw new Error('Expected floating-local request.');
    }
    expect(scheduledRequest.placement.startsLocalAt.toString()).toBe(
      '2026-09-07T15:00:00',
    );
    expect(scheduledRequest.placement.endsLocalAt.toString()).toBe(
      '2026-09-07T15:30:00',
    );
    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.projection.placement?.kind).toBe('floating-local');
  });

  it('preserves named-zone gap wall-clock intent and explicit resolution through the remote boundary', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-b02e-gap'),
      mode: 'production',
      activityDataSource: activity.source,
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'DST gap',
        kind: 'activity',
        date: '2026-03-29',
        timeSemantics: 'timed',
        startTime: '01:30',
        durationMinutes: 60,
        timeMode: 'zoned',
        timeZoneId: 'Europe/Rome',
        timeDisambiguation: 'later',
        contextId: CANONICAL_LIFE_AREA_REF,
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected explicit DST resolution to be valid.');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(activity.createScheduledActivity).toHaveBeenCalledTimes(1);
    const request = activity.createScheduledActivity.mock.calls[0]?.[0];
    expect(request?.placement.kind).toBe('named-zone-local-interval');
    if (request?.placement.kind !== 'named-zone-local-interval') {
      throw new Error('Expected named-zone request.');
    }
    expect(request.placement.startsLocalAt.toString()).toBe(
      '2026-03-29T01:30:00',
    );
    expect(request.placement.endsLocalAt.toString()).toBe(
      '2026-03-29T02:30:00',
    );
    expect(request.placement.zoneId).toBe('Europe/Rome');
    expect(request.placement.disambiguation).toBe('later');
    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.projection.placement?.kind).toBe('zoned');
    if (execution.effect?.projection.placement?.kind === 'zoned') {
      expect(
        execution.effect.projection.placement.sourceEndsLocalAt?.toString(),
      ).toBe('2026-03-29T02:30:00');
      expect(
        execution.effect.projection.placement.end.toPlainDateTime().toString(),
      ).toBe('2026-03-29T03:30:00');
    }
  });

  it('creates coarse Activity precision without manufacturing exact time', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-b02e-coarse'),
      mode: 'production',
      activityDataSource: activity.source,
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Relazione',
        kind: 'activity',
        date: '2026-09-07',
        timeSemantics: 'coarse',
        coarsePeriod: 'afternoon',
        contextId: CANONICAL_LIFE_AREA_REF,
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected coarse B02-E preparation.');
    }

    const execution = await runtime.execute(preparation.prepared);

    const request = activity.createScheduledActivity.mock.calls[0]?.[0];
    expect(request?.placement).toMatchObject({
      kind: 'coarse-local-period',
      period: 'afternoon',
    });
    expect(execution.effect?.projection.placement).toMatchObject({
      kind: 'coarse-local-period',
      period: 'afternoon',
    });
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

  it('places an existing Activity without creating or changing its identity', async () => {
    const canonical = Object.freeze({
      activityRef: CANONICAL_ACTIVITY_REF,
      title: 'Persistita nel Planning Tray',
      createdAt: Temporal.Instant.from('2026-09-07T12:00:00Z'),
    });
    const activity = activitySource(Object.freeze([canonical]));
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-b02e-place'),
      mode: 'production',
      activityDataSource: activity.source,
    });
    const start = Temporal.PlainDateTime.from('2026-09-07T23:30:00');
    const end = Temporal.PlainDateTime.from('2026-09-08T00:15:00');

    const result = await runtime.placeExistingActivity(
      CANONICAL_ACTIVITY_REF,
      Object.freeze({ kind: 'floating-local', start, end }),
    );

    expect(activity.createActivity).not.toHaveBeenCalled();
    expect(activity.createScheduledActivity).not.toHaveBeenCalled();
    expect(activity.establishActivitySchedule).toHaveBeenCalledTimes(1);
    const establishRequest = activity.establishActivitySchedule.mock.calls[0]?.[0];
    expect(establishRequest?.activityRef).toBe(CANONICAL_ACTIVITY_REF);
    expect(typeof establishRequest?.operationId).toBe('string');
    expect(establishRequest?.placement).toEqual({
      kind: 'floating-local-interval',
      startsLocalAt: start,
      endsLocalAt: end,
    });
    expect(result.status).toBe('applied');
    if (result.status === 'applied') {
      expect(result.item).toMatchObject({
        id: CANONICAL_SCHEDULE_REF,
        subject: {
          source: 'native',
          kind: 'activity',
          id: CANONICAL_ACTIVITY_REF,
        },
        placement: { kind: 'floating-local', start, end },
      });
      expect(result.reconciliation).toEqual({ status: 'confirmed' });
    }
  });

  it('still fails closed for owner semantics outside B02', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-event-unsupported'),
      mode: 'production',
      activityDataSource: activity.source,
    });
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Evento B03 non anticipato',
        kind: 'event',
        date: '2026-09-07',
        timeSemantics: 'timed',
        startTime: '15:00',
        timeMode: 'zoned',
        timeZoneId: 'Europe/Rome',
        contextId: CANONICAL_LIFE_AREA_REF,
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected a valid Event draft preparation.');
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

  it('fails closed instead of dropping unpersisted rich B02 intent', async () => {
    const activity = activitySource();
    const runtime = createLocalTemporalCreateRuntime({
      ...runtimeOptions('runtime-boundary-b02-rich'),
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
      contextId: CANONICAL_LIFE_AREA_REF,
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
        contextId: CANONICAL_LIFE_AREA_REF,
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