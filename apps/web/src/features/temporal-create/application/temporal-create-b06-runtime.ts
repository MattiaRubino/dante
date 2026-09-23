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
import {
  createTemporalCreateFields,
  type TemporalCreateFields,
  type TemporalCreateWeekday,
} from '../model/temporal-create-session';
import {
  createB04TemporalCreateRuntime,
  type B04TemporalCreateRuntimeOptions,
} from './temporal-create-b04-runtime';
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

export type B06TemporalCreateRuntimeOptions = B04TemporalCreateRuntimeOptions &
  Readonly<{
    recurringAuthoringDataSource?: RecurringAuthoringDataSource;
  }>;

const WEEKDAY_NUMBER: Readonly<Record<TemporalCreateWeekday, number>> =
  Object.freeze({ MO: 1, TU: 2, WE: 3, TH: 4, FR: 5, SA: 6, SU: 7 });

class B06CreateValidationError extends Error {
  constructor(
    readonly code: string,
    readonly path: readonly string[],
  ) {
    super(code);
    this.name = 'B06CreateValidationError';
  }
}

function canonicalJsonValue(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalJsonValue);
  if (value !== null && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([left], [right]) => left.localeCompare(right))
        .map(([key, child]) => [key, canonicalJsonValue(child)]),
    );
  }
  return value;
}

function sameStructuredIntent(left: unknown, right: unknown): boolean {
  return (
    JSON.stringify(canonicalJsonValue(left)) ===
    JSON.stringify(canonicalJsonValue(right))
  );
}

function unsupportedEventIntent(
  event: TemporalCreateFields['event'],
): Readonly<Record<string, unknown>> {
  return Object.freeze(
    Object.fromEntries(
      Object.entries(event).filter(
        ([key]) => key !== 'agendaParts' && key !== 'allDayEndDate',
      ),
    ),
  );
}

function recurringIntentSupported(
  prepared: TemporalCreatePreparedOperation,
): boolean {
  const fields = prepared.metadata.specification;
  const owner = prepared.metadata.recurrenceOwner;
  if (
    owner === null ||
    fields.eventRecurrence.patternKind === 'none' ||
    (owner === 'event' && prepared.metadata.kind !== 'event') ||
    (owner === 'routine' && prepared.metadata.kind !== 'activity') ||
    !isCanonicalLifeAreaRef(prepared.metadata.contextId) ||
    fields.notes.length !== 0 ||
    fields.appearanceTone !== null ||
    fields.scheduling.constraintKind !== 'none' ||
    fields.scheduling.fallbackPolicy !== 'inherit' ||
    fields.confirmation.outcomePolicy !== 'inherit' ||
    fields.confirmation.reminderLeadMinutes !== null
  ) {
    return false;
  }

  const baseline = createTemporalCreateFields({
    title: fields.title,
    kind: fields.kind,
    date: fields.date,
    timeSemantics: fields.timeSemantics,
    startTime: fields.startTime,
    durationMinutes: fields.durationMinutes,
    timeMode: fields.timeMode,
    timeZoneId: fields.timeZoneId,
    timeDisambiguation: fields.timeDisambiguation,
    coarsePeriod: fields.coarsePeriod,
    contextId: fields.contextId,
  });

  return (
    sameStructuredIntent(fields.execution, baseline.execution) &&
    sameStructuredIntent(
      unsupportedEventIntent(fields.event),
      unsupportedEventIntent(baseline.event),
    )
  );
}

function rangeForDateFamily(fields: TemporalCreateFields) {
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
        // Product "until" is inclusive; canonical recurrence ranges are half-open.
        effectiveUntil: Temporal.PlainDate.from(recurrence.untilDate)
          .add({ days: 1 })
          .toString(),
      });
  }
}

function localAnchorInstant(fields: TemporalCreateFields) {
  const local = Temporal.PlainDateTime.from(`${fields.date}T${fields.startTime}`);
  return local
    .toZonedDateTime(fields.timeZoneId, {
      disambiguation: fields.timeDisambiguation,
    })
    .toInstant();
}

function elapsedRange(fields: TemporalCreateFields) {
  const recurrence = fields.eventRecurrence;
  const anchor = localAnchorInstant(fields);
  switch (recurrence.endMode) {
    case 'none':
      return Object.freeze({
        rangeKind: 'open' as const,
        expectedCount: null,
        effectiveUntil: null,
        anchor,
      });
    case 'count':
      return Object.freeze({
        rangeKind: 'expected_count' as const,
        expectedCount: recurrence.count,
        effectiveUntil: null,
        anchor,
      });
    case 'until-date': {
      const boundaryDate = Temporal.PlainDate.from(recurrence.untilDate).add({
        days: 1,
      });
      const boundary = boundaryDate
        .toPlainDateTime('00:00')
        .toZonedDateTime(fields.timeZoneId, {
          disambiguation: fields.timeDisambiguation,
        })
        .toInstant();
      return Object.freeze({
        rangeKind: 'until_boundary' as const,
        expectedCount: null,
        effectiveUntil: boundary,
        anchor,
      });
    }
  }
}

function wallTimes(fields: TemporalCreateFields): readonly string[] {
  return fields.timeSemantics === 'timed'
    ? Object.freeze([fields.startTime])
    : Object.freeze([]);
}

function calendarRecurrence(
  fields: TemporalCreateFields,
): RecurringAuthoringRecurrence {
  const recurrence = fields.eventRecurrence;
  const range = rangeForDateFamily(fields);
  const date = Temporal.PlainDate.from(fields.date);
  const namedZone = fields.timeMode === 'zoned';
  if (namedZone && fields.timeDisambiguation === 'reject') {
    throw new B06CreateValidationError(
      'temporal.create.recurrence.named_zone_resolution_required',
      ['timeDisambiguation'],
    );
  }

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
    clock_basis_code: namedZone ? 'named_zone' : 'floating_local',
    zone_id: namedZone ? fields.timeZoneId : null,
    pattern_anchor_date:
      recurrence.calendarInterval > 1 ? fields.date : null,
    wall_times: wallTimes(fields),
    weekdays,
    month_days: monthDays,
    ordinal_weekdays: ordinalWeekdays,
    year_month_days: yearMonthDays,
    nonexistent_local_time_policy: namedZone ? 'skip_civil_candidate' : null,
    ambiguous_local_time_policy: namedZone
      ? (fields.timeDisambiguation as 'earlier' | 'later')
      : null,
    step_unit_code: null,
  });
}

function elapsedRecurrence(
  fields: TemporalCreateFields,
): RecurringAuthoringRecurrence {
  if (fields.timeSemantics !== 'timed') {
    throw new B06CreateValidationError(
      'temporal.create.recurrence.elapsed_requires_time',
      ['timeSemantics'],
    );
  }
  const recurrence = fields.eventRecurrence;
  const range = elapsedRange(fields);
  return Object.freeze({
    family_code: 'elapsed_interval' as const,
    range_kind: range.rangeKind,
    expected_occurrence_count: range.expectedCount,
    effective_from: range.anchor.toString(),
    effective_until: range.effectiveUntil?.toString() ?? null,
    elapsed_seconds: String(recurrence.elapsedIntervalMinutes * 60),
    anchor_mode_code: 'fixed_anchor' as const,
    anchor_at: range.anchor.toString(),
  });
}

function quotaRecurrence(
  fields: TemporalCreateFields,
): RecurringAuthoringRecurrence {
  const recurrence = fields.eventRecurrence;
  if (recurrence.endMode === 'count') {
    throw new B06CreateValidationError(
      'temporal.create.recurrence.quota_count_range_unsupported',
      ['eventRecurrence.endMode'],
    );
  }
  const range = rangeForDateFamily(fields);
  const frame = {
    'floating-local': 'floating_local',
    'named-zone': 'named_zone',
    'absolute-utc': 'absolute_utc',
  }[recurrence.quotaFrame] as
    | 'floating_local'
    | 'named_zone'
    | 'absolute_utc';
  return Object.freeze({
    family_code: 'quota_per_period' as const,
    range_kind: range.rangeKind as 'open' | 'until_boundary',
    expected_occurrence_count: null,
    effective_from: fields.date,
    effective_until: range.effectiveUntil,
    quota_count: recurrence.quotaCount,
    period_unit_code: recurrence.quotaPeriodKind,
    period_span: recurrence.quotaPeriodInterval,
    frame_code: frame,
    zone_id:
      recurrence.quotaFrame === 'named-zone'
        ? recurrence.quotaTimeZoneId
        : null,
    week_start:
      recurrence.quotaPeriodKind === 'week'
        ? WEEKDAY_NUMBER[recurrence.quotaWeekStart]
        : null,
    pattern_anchor_date:
      recurrence.quotaPeriodInterval > 1 ? fields.date : null,
  });
}

function cyclicRecurrence(
  fields: TemporalCreateFields,
): RecurringAuthoringRecurrence {
  const recurrence = fields.eventRecurrence;
  const range = rangeForDateFamily(fields);
  const selected = new Set(recurrence.cyclePositions);
  return Object.freeze({
    family_code: 'cyclic_positional' as const,
    range_kind: range.rangeKind,
    expected_occurrence_count: range.expectedCount,
    effective_from: fields.date,
    effective_until: range.effectiveUntil,
    cycle_length: recurrence.cycleLength,
    position_unit_code: recurrence.cycleUnit,
    pattern_anchor_date: fields.date,
    generates_expected: Object.freeze(
      Array.from({ length: recurrence.cycleLength }, (_, index) =>
        selected.has(index + 1),
      ),
    ),
  });
}

function recurrencePayload(
  fields: TemporalCreateFields,
): RecurringAuthoringRecurrence {
  switch (fields.eventRecurrence.patternKind) {
    case 'calendar-wall-clock':
      return calendarRecurrence(fields);
    case 'elapsed-interval':
      return elapsedRecurrence(fields);
    case 'quota-per-period':
      return quotaRecurrence(fields);
    case 'cyclic-positional':
      return cyclicRecurrence(fields);
    case 'none':
      throw new B06CreateValidationError(
        'temporal.create.recurrence.required',
        ['eventRecurrence.patternKind'],
      );
  }
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

function recurringProjection(
  created: RecurringAuthoringResult,
  operationId: TemporalOperationId,
): TemporalProjectionItem {
  return Object.freeze({
    id: temporalProjectionId(created.sourceRef),
    subject: Object.freeze({
      source: 'native' as const,
      kind: created.ownerKind,
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

function appliedEffect(
  prepared: TemporalCreatePreparedOperation,
  projection: TemporalProjectionItem,
  ids: TemporalIdFactory,
): TemporalCreateAppliedEffect {
  return Object.freeze({
    projection,
    metadata: prepared.metadata,
    undoToken: null,
    // Source+Recurrence creation is deliberately not represented as a local
    // optimistic Timeline item. The caller closes Create and the canonical
    // checkpoint/refetch path renders Occurrences.
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

function remoteFailure(
  operationId: TemporalOperationId,
  error: unknown,
): TemporalCreateExecution {
  if (error instanceof B06CreateValidationError) {
    return Object.freeze({
      result: Object.freeze({
        operationId,
        status: 'rejected' as const,
        code: 'validation' as const,
        issues: Object.freeze([
          temporalValidationIssue(error.code, error.path),
        ]),
      }),
      effect: null,
    });
  }
  if (error instanceof RangeError) {
    return Object.freeze({
      result: Object.freeze({
        operationId,
        status: 'rejected' as const,
        code: 'validation' as const,
        issues: Object.freeze([
          temporalValidationIssue(
            'temporal.create.recurrence.temporal_resolution_invalid',
            ['eventRecurrence'],
          ),
        ]),
      }),
      effect: null,
    });
  }
  if (error instanceof RecurringAuthoringRemoteError) {
    if (
      error.status === 409 &&
      error.code === 'temporal.recurring_authoring.operation_id_reused'
    ) {
      return Object.freeze({
        result: Object.freeze({
          operationId,
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
          operationId,
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
        operationId,
        status: 'failed' as const,
        failure: Object.freeze({
          kind:
            error.kind === 'transport'
              ? ('transport' as const)
              : ('unavailable' as const),
          code: 'temporal.recurring_authoring.remote_unavailable',
          retryable: error.kind === 'transport' || (error.status ?? 0) >= 500,
        }),
      }),
      effect: null,
    });
  }
  return Object.freeze({
    result: Object.freeze({
      operationId,
      status: 'failed' as const,
      failure: Object.freeze({
        kind: 'unknown' as const,
        code: 'temporal.recurring_authoring.failed',
        retryable: false,
      }),
    }),
    effect: null,
  });
}

class B06TemporalCreateRuntime implements TemporalCreateRuntime {
  public readonly clock: TemporalCreateRuntime['clock'];

  public constructor(
    private readonly base: TemporalCreateRuntime,
    private readonly authoring: RecurringAuthoringDataSource,
    private readonly ids: TemporalIdFactory,
  ) {
    this.clock = base.clock;
  }

  public prepare(
    fields: TemporalCreateFields,
    operationId?: TemporalOperationId,
  ): TemporalCreatePreparation {
    return this.base.prepare(fields, operationId);
  }

  public async execute(
    prepared: TemporalCreatePreparedOperation,
  ): Promise<TemporalCreateExecution> {
    const owner = prepared.metadata.recurrenceOwner;
    if (owner === null) {
      return await this.base.execute(prepared);
    }
    if (!recurringIntentSupported(prepared)) {
      return Object.freeze({
        result: unavailableResult(
          prepared.operationId,
          'temporal.create.capability_not_available',
        ),
        effect: null,
      });
    }

    try {
      const recurrence = recurrencePayload(prepared.metadata.specification);
      const common = {
        operationId: prepared.operationId,
        title: prepared.command.payload.title,
        lifeAreaRef: prepared.metadata.contextId,
        recurrence,
      } as const;
      const created =
        owner === 'event'
          ? await this.authoring.createEvent({
              ...common,
              agendaParts: prepared.metadata.specification.event.agendaParts,
            })
          : await this.authoring.createRoutine({
              ...common,
              tagRefs: Object.freeze([]),
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
      return remoteFailure(prepared.operationId, error);
    }
  }

  public async placeExistingActivity(
    activityRef: string,
    placement: TemporalPlacement,
  ): Promise<TemporalOperationResult> {
    return await this.base.placeExistingActivity(activityRef, placement);
  }

  public async list(): Promise<readonly TemporalProjectionItem[]> {
    return await this.base.list();
  }

  public async listRecords(): Promise<readonly TemporalCreateRecord[]> {
    return await this.base.listRecords();
  }
}

export function createB06TemporalCreateRuntime(
  options: B06TemporalCreateRuntimeOptions = {},
): TemporalCreateRuntime {
  const ids = options.ids ?? systemTemporalIdFactory;
  return new B06TemporalCreateRuntime(
    createB04TemporalCreateRuntime(options),
    options.recurringAuthoringDataSource ??
      createRemoteRecurringAuthoringDataSource(),
    ids,
  );
}
