import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  type TemporalEventDataSource,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createB03TemporalCreateRuntime } from './temporal-create-b03-runtime';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

const EVENT_REF = '0199a8c0-6e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-6e72-7bc0-8ad0-a2f403f5617d';
const STATE_REF = '0199a8c0-6e73-7bc0-8ad0-a2f403f5617d';

function runtimeWithEventSource() {
  const createScheduledEvent = vi.fn<TemporalEventDataSource['createScheduledEvent']>(
    (request) => {
      if (request.placement.kind !== 'floating-local-interval') {
        throw new Error('Expected floating-local Event placement.');
      }
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
  const baseRuntime = createLocalTemporalCreateRuntime({
    mode: 'test',
    ids: createDeterministicTemporalIdFactory('b03-runtime'),
    clock: createFixedTemporalClock(
      Temporal.Instant.from('2026-09-17T12:00:00Z'),
      'Europe/Rome',
    ),
  });

  return Object.freeze({
    runtime: createB03TemporalCreateRuntime({ baseRuntime, eventDataSource }),
    createScheduledEvent,
  });
}

describe('B03 Temporal Create runtime', () => {
  it('creates a scheduled Event through the canonical Event data source and projects Event identity', async () => {
    const { runtime, createScheduledEvent } = runtimeWithEventSource();
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Evento B03-B',
        kind: 'event',
        date: '2026-09-17',
        timeSemantics: 'timed',
        startTime: '18:30',
        durationMinutes: 90,
        timeMode: 'floating',
        timeZoneId: 'Europe/Rome',
        contextId: 'personale',
      }),
    );
    if (preparation.status !== 'ready') {
      throw new Error('Expected B03-B Event preparation to be ready.');
    }

    const execution = await runtime.execute(preparation.prepared);

    expect(createScheduledEvent).toHaveBeenCalledTimes(1);
    const request = createScheduledEvent.mock.calls[0]?.[0];
    expect(request?.title).toBe('Evento B03-B');
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
      title: 'Evento B03-B',
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

  it('fails closed for an unscheduled Event because B03-B only authorizes scheduled Event creation', async () => {
    const { runtime, createScheduledEvent } = runtimeWithEventSource();
    const preparation = runtime.prepare(
      createTemporalCreateFields({
        title: 'Evento senza placement',
        kind: 'event',
        date: '2026-09-17',
        timeSemantics: 'unscheduled',
        contextId: 'personale',
        timeZoneId: 'Europe/Rome',
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
