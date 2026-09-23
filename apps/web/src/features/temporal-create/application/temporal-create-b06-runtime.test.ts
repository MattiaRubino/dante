import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import {
  createB06TemporalCreateRuntime,
} from './temporal-create-b06-runtime';
import type {
  RecurringAuthoringDataSource,
  RecurringAuthoringRecurrence,
} from './remote-recurring-authoring';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

const AREA_REF = '0199d5f0-6e71-7bc0-8ad0-a2f403f5617d';
const EVENT_REF = '0199d5f0-6e72-7bc0-8ad0-a2f403f5617d';
const ROUTINE_REF = '0199d5f0-6e73-7bc0-8ad0-a2f403f5617d';
const STATE_REF = '0199d5f0-6e74-7bc0-8ad0-a2f403f5617d';
const NOW = Temporal.Instant.from('2026-09-23T08:00:00Z');

function runtimeWithAuthoring() {
  const createEvent = vi.fn<RecurringAuthoringDataSource['createEvent']>(
    (request) =>
      Promise.resolve(
        Object.freeze({
          ownerKind: 'event' as const,
          sourceRef: EVENT_REF,
          title: request.title,
          createdAt: NOW,
          recurrenceMaterialStateRef: STATE_REF,
          replayed: false,
        }),
      ),
  );
  const createRoutine = vi.fn<RecurringAuthoringDataSource['createRoutine']>(
    (request) =>
      Promise.resolve(
        Object.freeze({
          ownerKind: 'routine' as const,
          sourceRef: ROUTINE_REF,
          title: request.title,
          createdAt: NOW,
          recurrenceMaterialStateRef: STATE_REF,
          replayed: false,
        }),
      ),
  );
  const source: RecurringAuthoringDataSource = Object.freeze({
    createEvent,
    createRoutine,
  });
  const ids = createDeterministicTemporalIdFactory('b06-runtime');
  const baseRuntime = createLocalTemporalCreateRuntime({
    mode: 'test',
    ids: createDeterministicTemporalIdFactory('b06-base'),
    clock: createFixedTemporalClock(NOW, 'Europe/Rome'),
  });
  return Object.freeze({
    runtime: createB06TemporalCreateRuntime({
      baseRuntime,
      recurringAuthoringDataSource: source,
      ids,
    }),
    createEvent,
    createRoutine,
  });
}

function eventFields(
  recurrence: Partial<ReturnType<typeof createTemporalCreateFields>['eventRecurrence']>,
) {
  const baseline = createTemporalCreateFields({
    title: 'Sync progetto',
    kind: 'event',
    date: '2026-10-01',
    timeSemantics: 'timed',
    startTime: '09:30',
    timeMode: 'floating',
    timeZoneId: 'Europe/Rome',
    contextId: AREA_REF,
  });
  return createTemporalCreateFields({
    ...baseline,
    eventRecurrence: Object.freeze({
      ...baseline.eventRecurrence,
      patternKind: 'calendar-wall-clock',
      ...recurrence,
    }),
  });
}

async function executeEvent(
  recurrence: Partial<ReturnType<typeof createTemporalCreateFields>['eventRecurrence']>,
) {
  const sources = runtimeWithAuthoring();
  const preparation = sources.runtime.prepare(eventFields(recurrence));
  if (preparation.status !== 'ready') {
    throw new Error('Expected B06 recurring preparation to be ready.');
  }
  return Object.freeze({
    ...sources,
    execution: await sources.runtime.execute(preparation.prepared),
  });
}

function capturedRecurrence(
  mock: ReturnType<typeof runtimeWithAuthoring>['createEvent'],
): RecurringAuthoringRecurrence {
  const request = mock.mock.calls[0]?.[0];
  if (request === undefined) throw new Error('Expected recurring authoring call.');
  return request.recurrence;
}

describe('B06 Temporal Create runtime', () => {
  it('authors a recurring Event source without creating local Schedule geometry', async () => {
    const { execution, createEvent } = await executeEvent({
      patternKind: 'calendar-wall-clock',
      calendarFrequency: 'weekly',
      weekdays: Object.freeze(['MO', 'WE']),
      endMode: 'count',
      count: 5,
    });

    expect(execution.result.status).toBe('applied');
    expect(execution.effect?.undoAvailable).toBe(false);
    expect(execution.effect?.projection.placement).toBeNull();
    expect(execution.effect?.projection.subject).toEqual({
      source: 'native',
      kind: 'event',
      id: EVENT_REF,
    });
    expect(createEvent).toHaveBeenCalledTimes(1);
    expect(capturedRecurrence(createEvent)).toMatchObject({
      family_code: 'calendar_wall_clock',
      range_kind: 'expected_count',
      expected_occurrence_count: 5,
      pattern_code: 'weekly_weekdays',
      weekdays: [1, 3],
      wall_times: ['09:30'],
      clock_basis_code: 'floating_local',
    });
  });

  it('maps elapsed, quota and cyclic intent to their canonical B06 families', async () => {
    const elapsed = await executeEvent({
      patternKind: 'elapsed-interval',
      elapsedIntervalMinutes: 90,
      endMode: 'none',
    });
    expect(capturedRecurrence(elapsed.createEvent)).toMatchObject({
      family_code: 'elapsed_interval',
      range_kind: 'open',
      elapsed_seconds: '5400',
      anchor_mode_code: 'fixed_anchor',
    });

    const quota = await executeEvent({
      patternKind: 'quota-per-period',
      quotaCount: 3,
      quotaPeriodKind: 'week',
      quotaPeriodInterval: 1,
      quotaFrame: 'floating-local',
      quotaWeekStart: 'MO',
      endMode: 'none',
    });
    expect(capturedRecurrence(quota.createEvent)).toMatchObject({
      family_code: 'quota_per_period',
      range_kind: 'open',
      quota_count: 3,
      period_unit_code: 'week',
      week_start: 1,
    });

    const cyclic = await executeEvent({
      patternKind: 'cyclic-positional',
      cycleLength: 4,
      cyclePositions: Object.freeze([1, 3]),
      cycleUnit: 'day',
      endMode: 'none',
    });
    expect(capturedRecurrence(cyclic.createEvent)).toMatchObject({
      family_code: 'cyclic_positional',
      cycle_length: 4,
      position_unit_code: 'day',
      generates_expected: [true, false, true, false],
    });
  });

  it('routes Activity recurrence to Routine authoring, not Activity creation', async () => {
    const sources = runtimeWithAuthoring();
    const baseline = createTemporalCreateFields({
      title: 'Allenamento',
      kind: 'activity',
      date: '2026-10-01',
      timeSemantics: 'timed',
      startTime: '18:00',
      timeZoneId: 'Europe/Rome',
      contextId: AREA_REF,
    });
    const fields = createTemporalCreateFields({
      ...baseline,
      eventRecurrence: Object.freeze({
        ...baseline.eventRecurrence,
        owner: 'routine',
        patternKind: 'calendar-wall-clock',
        calendarFrequency: 'daily',
        endMode: 'none',
      }),
    });
    const preparation = sources.runtime.prepare(fields);
    if (preparation.status !== 'ready') {
      throw new Error('Expected Routine preparation to be ready.');
    }
    const execution = await sources.runtime.execute(preparation.prepared);

    expect(execution.result.status).toBe('applied');
    expect(sources.createRoutine).toHaveBeenCalledTimes(1);
    expect(sources.createEvent).not.toHaveBeenCalled();
    expect(execution.effect?.projection.subject).toEqual({
      source: 'native',
      kind: 'routine',
      id: ROUTINE_REF,
    });
  });

  it('rejects quota expected-count because canonical quota has no expected-count range', async () => {
    const { execution, createEvent } = await executeEvent({
      patternKind: 'quota-per-period',
      quotaCount: 2,
      quotaPeriodKind: 'week',
      quotaPeriodInterval: 1,
      endMode: 'count',
      count: 4,
    });

    expect(execution.result.status).toBe('rejected');
    expect(createEvent).not.toHaveBeenCalled();
  });
});
