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

const EVENT_REF = '0199a8c0-8e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199a8c0-8e72-7bc0-8ad0-a2f403f5617d';
const STATE_REF = '0199a8c0-8e73-7bc0-8ad0-a2f403f5617d';

describe('B03 Event create latent-field semantics', () => {
  it('does not reject a timed Event because an unused all-day end date still reflects the previous viewed date', async () => {
    const initial = createTemporalCreateFields({
      date: '2026-09-09',
      timeSemantics: 'unscheduled',
      timeZoneId: 'Europe/Rome',
      contextId: 'personale',
    });
    const fields = createTemporalCreateFields({
      ...initial,
      title: 'Evento timed dopo cambio data',
      kind: 'event',
      date: '2026-09-18',
      timeSemantics: 'timed',
      startTime: '10:00',
      durationMinutes: 30,
      event: Object.freeze({
        ...initial.event,
        allDayEndDate: '2026-09-09',
      }),
    });

    const createScheduledEvent = vi.fn<
      TemporalEventDataSource['createScheduledEvent']
    >((request) => {
      if (request.placement.kind !== 'floating-local-interval') {
        return Promise.reject(new Error('Expected floating-local Event.'));
      }
      return Promise.resolve(
        Object.freeze({
          event: Object.freeze({
            eventRef: EVENT_REF,
            title: request.title,
            agendaParts: Object.freeze([...request.agendaParts]),
            createdAt: Temporal.Instant.from('2026-09-18T08:00:00Z'),
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
    });
    const eventDataSource: TemporalEventDataSource = Object.freeze({
      createScheduledEvent,
    });
    const scheduleDataSource: TemporalScheduleDataSource = Object.freeze({
      reviseSchedule: vi.fn(() => Promise.reject(new Error('not expected'))),
      unscheduleSchedule: vi.fn(() => Promise.reject(new Error('not expected'))),
      undoScheduleUnschedule: vi.fn(() =>
        Promise.reject(new Error('not expected')),
      ),
    });
    const baseRuntime = createLocalTemporalCreateRuntime({
      mode: 'test',
      ids: createDeterministicTemporalIdFactory('b03-latent-base'),
      clock: createFixedTemporalClock(
        Temporal.Instant.from('2026-09-18T08:00:00Z'),
        'Europe/Rome',
      ),
    });
    const runtime = createB03TemporalCreateRuntime({
      baseRuntime,
      eventDataSource,
      scheduleDataSource,
      ids: createDeterministicTemporalIdFactory('b03-latent-event'),
    });

    const preparation = runtime.prepare(fields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected structurally valid timed Event preparation.');
    }
    const execution = await runtime.execute(preparation.prepared);

    expect(execution.result.status).toBe('applied');
    expect(createScheduledEvent).toHaveBeenCalledTimes(1);
    const request = createScheduledEvent.mock.calls[0]?.[0];
    expect(request?.placement.kind).toBe('floating-local-interval');
    if (request?.placement.kind === 'floating-local-interval') {
      expect(request.placement.startsLocalAt.toString()).toBe(
        '2026-09-18T10:00:00',
      );
    }
  });
});
