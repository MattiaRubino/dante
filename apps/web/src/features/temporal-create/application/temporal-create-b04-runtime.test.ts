import { Temporal } from '@dante/time';
import { describe, expect, it, vi } from 'vitest';

import {
  createDeterministicTemporalIdFactory,
  createFixedTemporalClock,
  type TemporalActivityDataSource,
  type TemporalConstrainedActivityDataSource,
  type TemporalScheduleDataSource,
} from '../../temporal';
import { createTemporalCreateFields } from '../model/temporal-create-session';
import { createB04TemporalCreateRuntime } from './temporal-create-b04-runtime';
import { createLocalTemporalCreateRuntime } from './temporal-create-runtime';

const ACTIVITY_REF = '0199c5f0-6e71-7bc0-8ad0-a2f403f5617d';
const SCHEDULE_REF = '0199c5f0-6e72-7bc0-8ad0-a2f403f5617d';
const STATE_REF = '0199c5f0-6e73-7bc0-8ad0-a2f403f5617d';
const CONSTRAINT_REF = '0199c5f0-6e74-7bc0-8ad0-a2f403f5617d';
const CONSTRAINT_STATE_REF = '0199c5f0-6e75-7bc0-8ad0-a2f403f5617d';
const CREATED_AT = Temporal.Instant.from('2026-09-20T08:30:00Z');

function activityRecord(title: string) {
  return Object.freeze({
    activityRef: ACTIVITY_REF,
    title,
    createdAt: CREATED_AT,
  });
}

function runtimeWithSources() {
  const createActivity = vi.fn<TemporalActivityDataSource['createActivity']>(
    (request) =>
      Promise.resolve(
        Object.freeze({
          activity: activityRecord(request.title),
          replayed: false,
        }),
      ),
  );
  const createScheduledActivity = vi.fn<
    TemporalActivityDataSource['createScheduledActivity']
  >(() => {
    throw new Error('B04 flexible create must not create Schedule eagerly.');
  });
  const establishActivitySchedule = vi.fn<
    TemporalActivityDataSource['establishActivitySchedule']
  >((request) => {
    const placement = request.placement;
    if (placement.kind !== 'absolute-interval') {
      throw new Error('Expected B04 hard-constrained placement to be absolute.');
    }
    return Promise.resolve(
      Object.freeze({
        activity: activityRecord('B04 Activity'),
        schedule: Object.freeze({
          scheduleRef: SCHEDULE_REF,
          placementMaterialStateRef: STATE_REF,
          placement,
        }),
        replayed: false,
      }),
    );
  });
  const loadUnplaced = vi.fn<TemporalActivityDataSource['loadUnplaced']>(() =>
    Promise.resolve(Object.freeze([])),
  );
  const activityDataSource: TemporalActivityDataSource = Object.freeze({
    createActivity,
    createScheduledActivity,
    establishActivitySchedule,
    loadUnplaced,
  });

  const createConstrainedActivity = vi.fn<
    TemporalConstrainedActivityDataSource['createConstrainedActivity']
  >((request) =>
    Promise.resolve(
      Object.freeze({
        activity: activityRecord(request.title),
        constraints: Object.freeze(
          request.rules.map((_, index) =>
            Object.freeze({
              constraintRef:
                index === 0
                  ? CONSTRAINT_REF
                  : '0199c5f0-6e76-7bc0-8ad0-a2f403f5617d',
              materialStateRef:
                index === 0
                  ? CONSTRAINT_STATE_REF
                  : '0199c5f0-6e77-7bc0-8ad0-a2f403f5617d',
            }),
          ),
        ),
        replayed: false,
      }),
    ),
  );
  const constrainedActivityDataSource: TemporalConstrainedActivityDataSource =
    Object.freeze({ createConstrainedActivity });

  const reviseSchedule = vi.fn<TemporalScheduleDataSource['reviseSchedule']>(
    () => {
      throw new Error('Revision is outside this focused B04 Create proof.');
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
  >(() => {
    throw new Error('Nested undo is outside this focused B04 Create proof.');
  });
  const scheduleDataSource: TemporalScheduleDataSource = Object.freeze({
    reviseSchedule,
    unscheduleSchedule,
    undoScheduleUnschedule,
  });

  const baseRuntime = createLocalTemporalCreateRuntime({
    mode: 'test',
    ids: createDeterministicTemporalIdFactory('b04-base'),
    clock: createFixedTemporalClock(CREATED_AT, 'Europe/Rome'),
  });

  return Object.freeze({
    runtime: createB04TemporalCreateRuntime({
      baseRuntime,
      activityDataSource,
      constrainedActivityDataSource,
      scheduleDataSource,
      ids: createDeterministicTemporalIdFactory('b04-runtime'),
    }),
    createActivity,
    createConstrainedActivity,
    establishActivitySchedule,
    unscheduleSchedule,
  });
}

function flexibleFields(
  constraintKind: 'open' | 'bounded-window' | 'deadline' | 'preferred-window',
) {
  const baseline = createTemporalCreateFields({
    title: 'B04 Activity',
    kind: 'activity',
    date: '2026-10-20',
    timeSemantics: 'unscheduled',
    timeZoneId: 'Europe/Rome',
    contextId: 'personale',
  });
  return createTemporalCreateFields({
    ...baseline,
    scheduling: Object.freeze({
      ...baseline.scheduling,
      constraintKind,
      windowStartDate: '2026-10-20',
      windowStartTime: '08:00',
      windowEndDate: '2026-10-20',
      windowEndTime: '12:00',
      earliestStartDate: '2026-10-20',
      earliestStartTime: '08:00',
      deadlineDate: '2026-10-20',
      deadlineTime: '12:00',
    }),
  });
}

async function executeKind(
  constraintKind: 'open' | 'bounded-window' | 'deadline' | 'preferred-window',
) {
  const sources = runtimeWithSources();
  const preparation = sources.runtime.prepare(flexibleFields(constraintKind));
  if (preparation.status !== 'ready') {
    throw new Error(`Expected ${constraintKind} preparation to be ready.`);
  }
  return Object.freeze({
    ...sources,
    execution: await sources.runtime.execute(preparation.prepared),
  });
}

describe('B04 Temporal Create runtime', () => {
  it('authors bounded-window as one hard absolute containment rule', async () => {
    const { execution, createConstrainedActivity, createActivity } =
      await executeKind('bounded-window');

    expect(execution.result.status).toBe('applied');
    expect(createActivity).not.toHaveBeenCalled();
    expect(createConstrainedActivity).toHaveBeenCalledTimes(1);
    const request = createConstrainedActivity.mock.calls[0]?.[0];
    expect(request?.rules).toHaveLength(1);
    const rule = request?.rules[0];
    expect(rule).toMatchObject({
      family: 'window',
      relationship: 'full_placement_contained',
      constrainedFacet: 'schedule.placement',
      strength: 'hard',
    });
    if (rule?.family !== 'window') {
      throw new Error('Expected bounded-window rule.');
    }
    expect(rule.startsAt.toString()).toBe('2026-10-20T06:00:00Z');
    expect(rule.endsAt.toString()).toBe('2026-10-20T10:00:00Z');
    expect(execution.effect?.projection.placement).toBeNull();
  });

  it('authors deadline as hard earliest-start plus latest-completion boundaries', async () => {
    const { execution, createConstrainedActivity } =
      await executeKind('deadline');

    expect(execution.result.status).toBe('applied');
    const rules = createConstrainedActivity.mock.calls[0]?.[0].rules;
    expect(rules).toHaveLength(2);
    expect(rules?.map((rule) => rule.family)).toEqual([
      'boundary',
      'boundary',
    ]);
    const earliest = rules?.[0];
    const deadline = rules?.[1];
    expect(earliest).toMatchObject({
      family: 'boundary',
      boundaryKind: 'earliest_start',
      constrainedFacet: 'schedule.start',
      strength: 'hard',
    });
    expect(deadline).toMatchObject({
      family: 'boundary',
      boundaryKind: 'latest_completion',
      constrainedFacet: 'schedule.completion',
      strength: 'hard',
    });
    if (earliest?.family !== 'boundary' || deadline?.family !== 'boundary') {
      throw new Error('Expected deadline boundary rules.');
    }
    expect(earliest.boundaryAt.toString()).toBe('2026-10-20T06:00:00Z');
    expect(deadline.boundaryAt.toString()).toBe('2026-10-20T10:00:00Z');
  });

  it('keeps open Activity unplaced without inventing a Temporal Constraint', async () => {
    const { execution, createActivity, createConstrainedActivity } =
      await executeKind('open');

    expect(execution.result.status).toBe('applied');
    expect(createActivity).toHaveBeenCalledTimes(1);
    expect(createConstrainedActivity).not.toHaveBeenCalled();
    expect(execution.effect?.projection.subject).toEqual({
      source: 'native',
      kind: 'activity',
      id: ACTIVITY_REF,
    });
  });

  it('keeps preferred-window fail-closed until its non-absolute semantics are activated', async () => {
    const { execution, createActivity, createConstrainedActivity } =
      await executeKind('preferred-window');

    expect(execution.result.status).toBe('failed');
    if (execution.result.status === 'failed') {
      expect(execution.result.failure.code).toBe(
        'temporal.create.capability_not_available',
      );
    }
    expect(createActivity).not.toHaveBeenCalled();
    expect(createConstrainedActivity).not.toHaveBeenCalled();
  });

  it('resolves Planning Tray local placement to an absolute candidate before canonical establish', async () => {
    const {
      runtime,
      execution,
      establishActivitySchedule,
      unscheduleSchedule,
    } = await executeKind('bounded-window');
    if (execution.effect === null) {
      throw new Error('Expected B04 Activity effect.');
    }

    const placement = Object.freeze({
      kind: 'floating-local' as const,
      start: Temporal.PlainDateTime.from('2026-10-20T09:00:00'),
      end: Temporal.PlainDateTime.from('2026-10-20T10:00:00'),
    });
    const placed = await execution.effect.replacePlacement(placement);

    expect(placed.result.status).toBe('applied');
    expect(establishActivitySchedule).toHaveBeenCalledTimes(1);
    const request = establishActivitySchedule.mock.calls[0]?.[0];
    expect(request?.placement.kind).toBe('absolute-interval');
    if (request?.placement.kind !== 'absolute-interval') {
      throw new Error('Expected an absolute Schedule candidate.');
    }
    expect(request.placement.startsAt.toString()).toBe('2026-10-20T07:00:00Z');
    expect(request.placement.endsAt.toString()).toBe('2026-10-20T08:00:00Z');
    expect(placed.effect?.projection.placement?.kind).toBe('absolute');

    const undone = await placed.effect?.undo();
    expect(undone?.status).toBe('applied');
    expect(unscheduleSchedule).toHaveBeenCalledTimes(1);
    expect(unscheduleSchedule.mock.calls[0]?.[0]).toMatchObject({
      scheduleRef: SCHEDULE_REF,
      expectedPlacementMaterialStateRef: STATE_REF,
    });

    const productionTrayResult = await runtime.placeExistingActivity(
      ACTIVITY_REF,
      placement,
    );
    expect(productionTrayResult.status).toBe('applied');
    expect(establishActivitySchedule).toHaveBeenCalledTimes(2);
  });
});
