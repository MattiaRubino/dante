import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  type TemporalEventDataSource,
  type TemporalScheduleDataSource,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createB03TemporalCreateRuntime } from './temporal-create-b03-runtime';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

const EVENT_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
const STATE_REF = '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d';
const REVISED_STATE_REF = '0199a8c0-6e74-7bc0-8ad0-a2f403f5617d';
const RESTORED_STATE_REF = '0199a8c0-6e75-7bc0-8ad0-a2f403f5617d';

function runtimeWithEventSource() {
  let acceptedStarts = Temporal.PlainDateTime.from('2026-09-17T18:30:00');
  let acceptedEnds = Temporal.PlainDateTime.from('2026-09-17T20:00:00');

  const createScheduledEvent = vi.fn<TemporalEventDataSource['createScheduledEvent']>(
    (request) => {
      if (request.placement.kind !== 'floating-local-interval') {
        throw new Error('Expected floating-local Event placement.');
      }
      acceptedStarts = request.placement.startsLocalAt;
      acceptedEnds = request.placement.endsLocalAt;
      return Promise.resolve(
        Object.freeze({
          event: Object.freeze({
            eventRef: EVENT_REF,
            title: request.title,
            createdAt: Temporal.Instant.from('2026-09-17T12:00:00Z'),
          }),
          schedule: Object.freeze({
            scheduleRef: SCHEDULE_REF,
            placementMaterialStateRef: STATE_REF,
            placement: Object.freeze({
              kind: 'floating-local-interval' as const,
              startsLocalAt: request.placement.startsLocalAt,
              endsLocalAt: request.placement.endsLocalAt,
            }),
          }),
          replayed: false,
        }),
      );
    },
  );
  const eventDataSource: TemporalEventDataSource = Object.freeze({
    createScheduledEvent,
  });

  const reviseSchedule = vi.fn<TemporalScheduleDataSource['reviseSchedule']>(
    (request) => {
      if (request.placement.kind !== 'floating-local-interval') {
        throw new Error('Expected floating-local revision.');
      }
      acceptedStarts = request.placement.startsLocalAt;
      acceptedEnds = request.placement.endsLocalAt;
      return Promise.resolve(
        Object.freeze({
          scheduleRef: request.scheduleRef,
          previousPlacementMaterialStateRef:
            request.expectedPlacementMaterialStateRef,
          placementMaterialStateRef: REVISED_STATE_REF,
          placement: Object.freeze({
            kind: 'floating-local-interval' as const,
            startsLocalAt: acceptedStarts,
            endsLocalAt: acceptedEnds,
          }),
          replayed: false,
        }),
      );
    },
  );
  const unscheduleSchedule = vi.fn<
    TemporalScheduleDataSource['unscheduleSchedule']
  >((request) =>
    Promise.resolve(
      Object.freeze({
        scheduleRef: request.scheduleRef,
        previousPlacementMaterialStateRef:
          request.expectedPlacementMaterialStateRef,
        unscheduleOperationId: request.operationId,
        replayed: false,
      }),
    ),
  );
  const undoScheduleUnschedule = vi.fn<
    TemporalScheduleDataSource['undoScheduleUnschedule']
  >((request) =>
    Promise.resolve(
      Object.freeze({
        scheduleRef: request.scheduleRef,
        restoredFromPlacementMaterialStateRef: REVISED_STATE_REF,
        placementMaterialStateRef: RESTORED_STATE_REF,
        placement: Object.freeze({
          kind: 'floating-local-interval' as const,
          startsLocalAt: acceptedStarts,
          endsLocalAt: acceptedEnds,
        }),
        replayed: false,
      }),
    ),
  );
  const scheduleDataSource: TemporalScheduleDataSource = Object.freeze({
    reviseSchedule,
    unscheduleSchedule,
    undoScheduleUnschedule,
  });

  const baseRuntime = createLocalTemporalCreateRuntime({
    mode: 'test',
    ids: createDeterministicTemporalIdFactory('b03-runtime'),
    clock: createFixedTemporalClock(
      Temporal.Instant.from('2026-09-17T12:00:00Z'),
      'Europe/Rome',
    ),
  });

  return Object.freeze({
    runtime: createB03TemporalCreateRuntime({
      baseRuntime,
      eventDataSource,
      scheduleDataSource,
      ids: createDeterministicTemporalIdFactory('b03-lifecycle'),
    }),
    createScheduledEvent,
    reviseSchedule,
    unscheduleSchedule,
    undoScheduleUnschedule,
  });
}

function scheduledEventFields() {
  return createTemporalCreateFields({
    title: 'Evento B03-C',
    kind: 'event',
    date: '2026-09-17',
    timeSemantics: 'timed',
    startTime: '18:30',
    durationMinutes: 90,
    timeMode: 'floating',
    timeZoneId: 'Europe/Rome',
    contextId: 'personale',
  });
}

describe('B03 Temporal Create runtime', () => {
  it('creates a scheduled Event through the canonical Event data source and projects Event identity', async () => {
    const { runtime, createScheduledEvent } = runtimeWithEventSource();
    const preparation = runtime.prepare(scheduledEventFields());
    if (preparation.status !== 'ready') {
      throw new Error('Expected B03 Event preparation to be ready.');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(createScheduledEvent).toHaveBeenCalledTimes(1);
    const request = createScheduledEvent.mock.calls[0]?.[0];
    expect(request?.title).toBe('Evento B03-C');
    expect(request?.placement.kind).toBe('floating-local-interval');
    if (request?.placement.kind !== 'floating-local-interval') {
      throw new Error('Expected floating-local Event request.');
    }
    expect(request.placement.startsLocalAt.toString()).toBe(
      '2026-09-17T18:30:00',
    );
    expect(request.placement.endsLocalAt.toString()).toBe(
      '2026-09-17T20:00:00',
    );

    expect(execution.result.status).toBe('applied');
    if (execution.result.status !== 'applied') {
      throw new Error('Expected scheduled Event create to be applied.');
    }
    expect(execution.result.item).toMatchObject({
      subject: {
        source: 'native',
        kind: 'event',
        id: EVENT_REF,
      },
      title: 'Evento B03-C',
    });
    expect(execution.effect?.projection.subject).toEqual({
      source: 'native',
      kind: 'event',
      id: EVENT_REF,
    });
    expect(execution.effect?.undoAvailable).toBe(false);

    const undo = await execution.effect?.undo();
    expect(undo?.status).toBe('failed');
    if (undo?.status === 'failed') {
      expect(undo.failure.code).toBe(
        'temporal.event.lifecycle_capability_not_available',
      );
    }
  });

  it('reschedules, postpones, and guarded-undoes a freshly created Event on its shared Schedule', async () => {
    const {
      runtime,
      reviseSchedule,
      unscheduleSchedule,
      undoScheduleUnschedule,
    } = runtimeWithEventSource();
    const preparation = runtime.prepare(scheduledEventFields());
    if (preparation.status !== 'ready') {
      throw new Error('Expected B03-C Event preparation to be ready.');
    }
    const created = await runtime.execute(preparation.prepared);
    if (created.effect === null) {
      throw new Error('Expected canonical Event create effect.');
    }

    const revised = await created.effect.replacePlacement(
      Object.freeze({
        kind: 'floating-local' as const,
        start: Temporal.PlainDateTime.from('2026-09-18T10:00:00'),
        end: Temporal.PlainDateTime.from('2026-09-18T11:30:00'),
      }),
    );
    expect(reviseSchedule).toHaveBeenCalledTimes(1);
    expect(reviseSchedule.mock.calls[0]?.[0]).toMatchObject({
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: STATE_REF,
    });
    expect(revised.result.status).toBe('applied');
    if (revised.result.status !== 'applied' || revised.result.item === null) {
      throw new Error('Expected Event reschedule to apply.');
    }
    expect(revised.result.item.subject).toMatchObject({
      kind: 'event',
      id: EVENT_REF,
    });
    expect(revised.result.item.placement?.kind).toBe('floating-local');
    if (revised.result.item.placement?.kind !== 'floating-local') {
      throw new Error('Expected revised floating-local projection.');
    }
    expect(revised.result.item.placement.start.toString()).toBe(
      '2026-09-18T10:00:00',
    );

    const postponed = await created.effect.replacePlacement(null);
    expect(unscheduleSchedule).toHaveBeenCalledTimes(1);
    expect(unscheduleSchedule.mock.calls[0]?.[0]).toMatchObject({
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: REVISED_STATE_REF,
    });
    expect(postponed.result.status).toBe('applied');
    if (
      postponed.result.status !== 'applied' ||
      postponed.result.item === null ||
      postponed.effect === null
    ) {
      throw new Error('Expected Event postpone/TBD mutation effect.');
    }
    expect(postponed.result.item.subject).toMatchObject({
      kind: 'event',
      id: EVENT_REF,
    });
    expect(postponed.result.item.placement).toBeNull();

    const restored = await postponed.effect.undo();
    expect(undoScheduleUnschedule).toHaveBeenCalledTimes(1);
    const unscheduleReceipt = unscheduleSchedule.mock.results[0]?.value;
    const undoRequest = undoScheduleUnschedule.mock.calls[0]?.[0];
    expect(undoRequest?.scheduleRef).toBe(SCHEDULE_REF);
    expect(undoRequest?.unscheduleOperationId).toBeTruthy();
    expect(unscheduleReceipt).toBeInstanceOf(Promise);
    expect(restored.status).toBe('applied');
    if (restored.status !== 'applied' || restored.item === null) {
      throw new Error('Expected guarded Event Schedule Undo to apply.');
    }
    expect(restored.item.subject).toMatchObject({
      kind: 'event',
      id: EVENT_REF,
    });
    expect(restored.item.placement?.kind).toBe('floating-local');
    if (restored.item.placement?.kind !== 'floating-local') {
      throw new Error('Expected restored Event placement.');
    }
    expect(restored.item.placement.start.toString()).toBe(
      '2026-09-18T10:00:00',
    );
    expect(restored.item.revision).toBeGreaterThan(
      postponed.result.item.revision,
    );

    const remove = await created.effect.remove();
    expect(remove.effect).toBeNull();
    expect(remove.result.status).toBe('failed');
  });

  it('fails closed for Event intent outside the minimal B03 create contract', async () => {
    const { runtime, createScheduledEvent } = runtimeWithEventSource();
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Evento arricchito',
        kind: 'event',
        date: '2026-09-17',
        timeSemantics: 'timed',
        startTime: '09:00',
        durationMinutes: 30,
        timeMode: 'floating',
        contextId: 'personale',
        timeZoneId: 'Europe/Rome',
        notes: 'Intento non ancora autorizzato dal contratto B03-C',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected Event preparation to be structurally valid.');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(createScheduledEvent).not.toHaveBeenCalled();
    expect(execution.effect).toBeNull();
    expect(execution.result.status).toBe('failed');
    if (execution.result.status === 'failed') {
      expect(execution.result.failure.code).toBe(
        'temporal.create.capability_not_available',
      );
    }
  });
});
