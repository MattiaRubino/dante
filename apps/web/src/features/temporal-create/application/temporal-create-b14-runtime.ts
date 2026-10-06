import { Temporal } from '@dante/time';

import {
  systemTemporalIdFactory,
  temporalProjectionId,
  temporalValidationIssue,
  type TemporalIdFactory,
  type TemporalOperationId,
  type TemporalOperationResult,
  type TemporalPlacement,
  type TemporalProjectionItem,
} from '../../temporal';
import { invalidateTemporalTimelineRead } from '../../temporal/timeline-invalidation';
import type {
  TemporalCreateFields,
  TemporalCreateWeekday,
} from '../model/temporal-create-session';
import {
  createB04TemporalCreateRuntime,
  type B04TemporalCreateRuntimeOptions,
} from './temporal-create-b04-runtime';
import {
  createB06TemporalCreateRuntime,
  type B06TemporalCreateRuntimeOptions,
} from './temporal-create-b06-runtime';
import {
  RecurringAuthoringRemoteError,
  createRemoteRecurringAuthoringDataSource,
  type RecurringAuthoringDataSource,
  type RecurringAuthoringRecurrence,
  type RecurringAuthoringResult,
} from './remote-recurring-authoring';
import {
  isCanonicalLifeAreaRef,
  type TemporalCreateAppliedEffect,
  type TemporalCreateExecution,
  type TemporalCreatePreparedOperation,
  type TemporalCreatePreparation,
  type TemporalCreateRecord,
  type TemporalCreateRuntime,
} from './temporal-create-runtime';

export type B14TemporalCreateRuntimeOptions = B04TemporalCreateRuntimeOptions &
  B06TemporalCreateRuntimeOptions &
  Readonly<{
    recurringAuthoringDataSource?: RecurringAuthoringDataSource;
  }>;

const WEEKDAY_NUMBER: Readonly<Record<TemporalCreateWeekday, number>> =
  Object.freeze({ MO: 1, TU: 2, WE: 3, TH: 4, FR: 5, SA: 6, SU: 7 });

function calendarRange(fields: TemporalCreateFields) {
  const recurrence = fields.eventRecurrence;
  switch (recurrence.endMode) {
    case 'none':
      return Object.freeze({
        rangeKind: 'open' as const,
        expectedCount: null,
        effectiveUntil: null,
      });
    case 'count':
      return Object.freeze({
        rangeKind: 'expected_count' as const,
        expectedCount: recurrence.count,
        effectiveUntil: null,
      });
    case 'until-date':
      return Object.freeze({
        rangeKind: 'until_boundary' as const,
        expectedCount: null,
        effectiveUntil: Temporal.PlainDate.from(recurrence.untilDate)
          .add({ days: 1 })
          .toString(),
      });
  }
}

function activityRecurrence(
  fields: TemporalCreateFields,
): RecurringAuthoringRecurrence {
  if (fields.eventRecurrence.patternKind !== 'calendar-wall-clock') {
    throw new Error('temporal.create.activity_recurrence.calendar_only');
  }
  if (fields.timeSemantics !== 'timed' || fields.timeMode !== 'zoned') {
    throw new Error('temporal.create.activity_recurrence.timed_zoned_required');
  }

  const recurrence = fields.eventRecurrence;
  const range = calendarRange(fields);
  const date = Temporal.PlainDate.from(fields.date);
  let patternCode:
    | 'daily'
    | 'weekly_weekdays'
    | 'monthly_month_days'
    | 'monthly_ordinal_weekdays'
    | 'yearly_month_days';
  let weekdays: readonly number[] = Object.freeze([]);
  let monthDays: readonly number[] = Object.freeze([]);
  let ordinalWeekdays: readonly Readonly<{
    weekday_number: number;
    ordinal: number;
  }>[] = Object.freeze([]);
  let yearMonthDays: readonly Readonly<{
    month_number: number;
    month_day: number;
  }>[] = Object.freeze([]);

  switch (recurrence.calendarFrequency) {
    case 'daily':
      patternCode = 'daily';
      break;
    case 'weekly':
      patternCode = 'weekly_weekdays';
      weekdays = Object.freeze(
        recurrence.weekdays.map((weekday) => WEEKDAY_NUMBER[weekday]),
      );
      break;
    case 'monthly':
      patternCode = 'monthly_month_days';
      monthDays = Object.freeze([date.day]);
      break;
    case 'monthly-ordinal':
      patternCode = 'monthly_ordinal_weekdays';
      ordinalWeekdays = Object.freeze([
        Object.freeze({
          weekday_number: WEEKDAY_NUMBER[recurrence.calendarOrdinalWeekday],
          ordinal: recurrence.calendarOrdinal,
        }),
      ]);
      break;
    case 'yearly':
      patternCode = 'yearly_month_days';
      yearMonthDays = Object.freeze([
        Object.freeze({ month_number: date.month, month_day: date.day }),
      ]);
      break;
  }

  return Object.freeze({
    family_code: 'calendar_wall_clock' as const,
    range_kind: range.rangeKind,
    expected_occurrence_count: range.expectedCount,
    effective_from: fields.date,
    effective_until: range.effectiveUntil,
    pattern_code: patternCode,
    interval_count: recurrence.calendarInterval,
    clock_basis_code: 'named_zone' as const,
    zone_id: fields.timeZoneId,
    pattern_anchor_date:
      recurrence.calendarInterval > 1 ? fields.date : null,
    wall_times: Object.freeze([fields.startTime]),
    weekdays,
    month_days: monthDays,
    ordinal_weekdays: ordinalWeekdays,
    year_month_days: yearMonthDays,
    nonexistent_local_time_policy: 'skip_civil_candidate' as const,
    // Activity Create does not expose a DST-overlap policy. Keep future
    // occurrences deterministic; an explicit `later` choice is still retained.
    ambiguous_local_time_policy:
      fields.timeDisambiguation === 'later' ? ('later' as const) : ('earlier' as const),
    step_unit_code: null,
  });
}

function recurringProjection(
  created: RecurringAuthoringResult,
  operationId: TemporalOperationId,
): TemporalProjectionItem {
  return Object.freeze({
    id: temporalProjectionId(created.sourceRef),
    subject: Object.freeze({
      source: 'native' as const,
      kind: 'routine' as const,
      id: created.sourceRef,
    }),
    title: created.title,
    placement: null,
    capabilities: Object.freeze(['recurrence'] as const),
    revision: 0,
    createdAt: created.createdAt,
    updatedAt: created.createdAt,
    lastOperationId: operationId,
  });
}

function unavailableResult(
  operationId: TemporalOperationId,
  code: string,
): TemporalOperationResult {
  return Object.freeze({
    operationId,
    status: 'failed' as const,
    failure: Object.freeze({
      kind: 'unavailable' as const,
      code,
      retryable: false,
    }),
  });
}

function appliedEffect(
  prepared: TemporalCreatePreparedOperation,
  projection: TemporalProjectionItem,
  ids: TemporalIdFactory,
): TemporalCreateAppliedEffect {
  return Object.freeze({
    projection,
    metadata: prepared.metadata,
    undoToken: null,
    undoAvailable: false,
    undo: async () =>
      unavailableResult(ids.operationId(), 'temporal.create.undo_unavailable'),
    replacePlacement: async (_placement: TemporalPlacement | null) =>
      Object.freeze({
        result: unavailableResult(
          ids.operationId(),
          'temporal.occurrence.schedule_required',
        ),
        effect: null,
      }),
    remove: async () =>
      Object.freeze({
        result: unavailableResult(
          ids.operationId(),
          'temporal.create.remove_unavailable',
        ),
        effect: null,
      }),
  });
}

function failed(
  prepared: TemporalCreatePreparedOperation,
  error: unknown,
): TemporalCreateExecution {
  if (error instanceof RecurringAuthoringRemoteError) {
    if (
      error.status === 409 &&
      error.code === 'temporal.recurring_authoring.operation_id_reused'
    ) {
      return Object.freeze({
        result: Object.freeze({
          operationId: prepared.operationId,
          status: 'rejected' as const,
          code: 'operation-id-reused' as const,
          issues: Object.freeze([
            temporalValidationIssue('temporal.operation.id_reused', [
              'operationId',
            ]),
          ]),
        }),
        effect: null,
      });
    }
    if (error.status === 422) {
      return Object.freeze({
        result: Object.freeze({
          operationId: prepared.operationId,
          status: 'rejected' as const,
          code: 'validation' as const,
          issues: Object.freeze([
            temporalValidationIssue(
              'temporal.create.recurrence.backend_rejected',
              ['eventRecurrence'],
            ),
          ]),
        }),
        effect: null,
      });
    }
    return Object.freeze({
      result: Object.freeze({
        operationId: prepared.operationId,
        status: 'failed' as const,
        failure: Object.freeze({
          kind:
            error.kind === 'transport'
              ? ('transport' as const)
              : ('unavailable' as const),
          code: error.code ?? 'temporal.recurring_authoring.remote_unavailable',
          message: error.code ? `${error.message} (${error.code})` : error.message,
          retryable: error.kind === 'transport' || (error.status ?? 0) >= 500,
        }),
      }),
      effect: null,
    });
  }
  return Object.freeze({
    result: Object.freeze({
      operationId: prepared.operationId,
      status: 'rejected' as const,
      code: 'validation' as const,
      issues: Object.freeze([
        temporalValidationIssue(
          error instanceof Error
            ? error.message
            : 'temporal.create.activity_recurrence.invalid',
          ['eventRecurrence'],
        ),
      ]),
    }),
    effect: null,
  });
}

class B14TemporalCreateRuntime implements TemporalCreateRuntime {
  public readonly clock: TemporalCreateRuntime['clock'];

  public constructor(
    private readonly activityBase: TemporalCreateRuntime,
    private readonly delegate: TemporalCreateRuntime,
    private readonly authoring: RecurringAuthoringDataSource,
    private readonly ids: TemporalIdFactory,
  ) {
    this.clock = delegate.clock;
  }

  public prepare(
    fields: TemporalCreateFields,
    operationId?: TemporalOperationId,
  ): TemporalCreatePreparation {
    if (
      fields.kind === 'activity' &&
      fields.eventRecurrence.patternKind !== 'none'
    ) {
      return this.activityBase.prepare(fields, operationId);
    }
    return this.delegate.prepare(fields, operationId);
  }

  public async execute(
    prepared: TemporalCreatePreparedOperation,
  ): Promise<TemporalCreateExecution> {
    if (prepared.metadata.recurrenceOwner !== 'routine') {
      return await this.delegate.execute(prepared);
    }

    const fields = prepared.metadata.specification;
    if (
      fields.kind !== 'activity' ||
      fields.notes.length !== 0 ||
      fields.appearanceTone !== null ||
      fields.scheduling.constraintKind !== 'none' ||
      fields.scheduling.fallbackPolicy !== 'inherit' ||
      fields.confirmation.outcomePolicy !== 'inherit'
    ) {
      return Object.freeze({
        result: unavailableResult(
          prepared.operationId,
          'temporal.create.capability_not_available',
        ),
        effect: null,
      });
    }

    try {
      const created = await this.authoring.createRoutine({
        operationId: prepared.operationId,
        title: prepared.command.payload.title,
        lifeAreaRef: isCanonicalLifeAreaRef(prepared.metadata.contextId)
          ? prepared.metadata.contextId
          : null,
        tagRefs: Object.freeze([]),
        recurrence: activityRecurrence(fields),
        durationMinutes: fields.durationMinutes,
        reminderLeadMinutes: fields.confirmation.reminderLeadMinutes,
      });
      const projection = recurringProjection(created, prepared.operationId);
      invalidateTemporalTimelineRead();
      return Object.freeze({
        result: Object.freeze({
          operationId: prepared.operationId,
          status: 'applied' as const,
          item: projection,
          snapshotRevision: 0,
          reconciliation: Object.freeze({ status: 'confirmed' as const }),
        }),
        effect: appliedEffect(prepared, projection, this.ids),
      });
    } catch (error) {
      return failed(prepared, error);
    }
  }

  public async placeExistingActivity(
    activityRef: string,
    placement: TemporalPlacement,
  ): Promise<TemporalOperationResult> {
    return await this.delegate.placeExistingActivity(activityRef, placement);
  }

  public async list(): Promise<readonly TemporalProjectionItem[]> {
    return await this.delegate.list();
  }

  public async listRecords(): Promise<readonly TemporalCreateRecord[]> {
    return await this.delegate.listRecords();
  }
}

export function createB14TemporalCreateRuntime(
  options: B14TemporalCreateRuntimeOptions = {},
): TemporalCreateRuntime {
  const ids = options.ids ?? systemTemporalIdFactory;
  return new B14TemporalCreateRuntime(
    createB04TemporalCreateRuntime(options),
    createB06TemporalCreateRuntime(options),
    options.recurringAuthoringDataSource ??
      createRemoteRecurringAuthoringDataSource(),
    ids,
  );
}
