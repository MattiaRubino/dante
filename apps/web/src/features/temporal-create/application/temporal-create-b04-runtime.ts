import { Temporal } from '@dante/time';

import {
  TemporalActivityRemoteError,
  TemporalScheduleRemoteError,
  createRemoteTemporalActivityDataSource,
  createRemoteTemporalConstrainedActivityDataSource,
  createRemoteTemporalScheduleDataSource,
  systemTemporalIdFactory,
  temporalProjectionId,
  temporalValidationIssue,
  type TemporalAcceptedSchedulePlacement,
  type TemporalActivityConstraintRuleInput,
  type TemporalActivityDataSource,
  type TemporalActivityRecord,
  type TemporalConstrainedActivityDataSource,
  type TemporalIdFactory,
  type TemporalOperationId,
  type TemporalOperationResult,
  type TemporalPlacement,
  type TemporalProjectionItem,
  type TemporalScheduleDataSource,
  type TemporalSchedulePlacementInput,
  type TemporalScheduleRecord,
} from '../../temporal';
import {
  createTemporalCreateFields,
  type TemporalCreateFields,
} from '../model/temporal-create-session';
import {
  createB03TemporalCreateRuntime,
  type B03TemporalCreateRuntimeOptions,
} from './temporal-create-b03-runtime';
import {
  createLocalTemporalCreateRuntime,
  type TemporalCreateAppliedEffect,
  type TemporalCreateExecution,
  type TemporalCreateMetadata,
  type TemporalCreateMutationEffect,
  type TemporalCreateMutationExecution,
  type TemporalCreatePreparedOperation,
  type TemporalCreatePreparation,
  type TemporalCreateRecord,
  type TemporalCreateRuntime,
  isCanonicalLifeAreaRef,
} from './temporal-create-runtime';

export type B04TemporalCreateRuntimeOptions = B03TemporalCreateRuntimeOptions &
  Readonly<{
    activityDataSource?: TemporalActivityDataSource;
    constrainedActivityDataSource?: TemporalConstrainedActivityDataSource;
  }>;

type B04ConstraintKind = 'open' | 'bounded-window' | 'deadline';

function sameStructuredIntent(left: unknown, right: unknown): boolean {
  const canonical = (value: unknown): unknown => {
    if (Array.isArray(value)) {
      return value.map(canonical);
    }
    if (value !== null && typeof value === 'object') {
      return Object.fromEntries(
        Object.entries(value as Record<string, unknown>)
          .sort(([leftKey], [rightKey]) => leftKey.localeCompare(rightKey))
          .map(([key, child]) => [key, canonical(child)]),
      );
    }
    return value;
  };
  return JSON.stringify(canonical(left)) === JSON.stringify(canonical(right));
}

function b04ConstraintKind(
  fields: TemporalCreateFields,
): B04ConstraintKind | null {
  const kind = fields.scheduling.constraintKind;
  return kind === 'open' || kind === 'bounded-window' || kind === 'deadline'
    ? kind
    : null;
}

function b04FlexibleActivityIntentSupported(
  prepared: TemporalCreatePreparedOperation,
): boolean {
  const specification = prepared.metadata.specification;
  const constraintKind = b04ConstraintKind(specification);
  const hasSessionMinimum =
    specification.execution.sessionMode === 'splittable';
  const placedSessionMinimum =
    constraintKind === null &&
    hasSessionMinimum &&
    prepared.command.payload.placement !== null;
  if (
    prepared.metadata.kind !== 'activity' ||
    (prepared.command.payload.placement !== null && !placedSessionMinimum) ||
    (import.meta.env.MODE !== 'test' && !isCanonicalLifeAreaRef(prepared.metadata.contextId)) ||
    (constraintKind === null && !hasSessionMinimum) ||
    specification.scheduling.constraintKind === 'preferred-window' ||
    (prepared.metadata.contextId !== 'personale' && !isCanonicalLifeAreaRef(prepared.metadata.contextId)) ||
    prepared.metadata.notes.length !== 0 ||
    specification.appearanceTone !== null ||
    specification.eventRecurrence.patternKind !== 'none'
  ) {
    return false;
  }

  const baseline = createTemporalCreateFields({
    date: specification.date,
    timeZoneId: specification.timeZoneId,
    contextId: specification.contextId,
    timeSemantics: 'unscheduled',
  });

  return (
    (specification.durationMinutes === baseline.durationMinutes ||
      placedSessionMinimum) &&
    specification.scheduling.movementPolicy ===
      baseline.scheduling.movementPolicy &&
    specification.scheduling.fallbackPolicy === 'inherit' &&
    (sameStructuredIntent(specification.execution, baseline.execution) ||
      (specification.execution.sessionMode === 'splittable' &&
        specification.execution.minSessionMinutes >= 1 &&
        specification.execution.maxSessions === baseline.execution.maxSessions &&
        specification.execution.partialAllowed === baseline.execution.partialAllowed &&
        specification.execution.finishEarlyAllowed === baseline.execution.finishEarlyAllowed &&
        specification.execution.mergeCompatible === baseline.execution.mergeCompatible &&
        specification.execution.preparationMinutes === baseline.execution.preparationMinutes &&
        specification.execution.recoveryMinutes === baseline.execution.recoveryMinutes &&
        specification.execution.spacingMinutes === baseline.execution.spacingMinutes)) &&
    sameStructuredIntent(
      specification.eventRecurrence,
      baseline.eventRecurrence,
    ) &&
    sameStructuredIntent(specification.confirmation, baseline.confirmation) &&
    sameStructuredIntent(specification.event, baseline.event)
  );
}

function absoluteInstant(
  date: string,
  time: string,
  specification: TemporalCreateFields,
) {
  return Temporal.PlainDateTime.from(`${date}T${time}`)
    .toZonedDateTime(specification.timeZoneId, {
      disambiguation: specification.timeDisambiguation,
    })
    .toInstant();
}

function constraintRules(
  specification: TemporalCreateFields,
): readonly TemporalActivityConstraintRuleInput[] {
  const schedulingRules: readonly TemporalActivityConstraintRuleInput[] = (() => {
    switch (specification.scheduling.constraintKind) {
      case 'open':
        return Object.freeze([]);
      case 'bounded-window':
        return Object.freeze([
          Object.freeze({
            family: 'window' as const,
            relationship: 'full_placement_contained' as const,
            constrainedFacet: 'schedule.placement' as const,
            strength: 'hard' as const,
            startsAt: absoluteInstant(
              specification.scheduling.windowStartDate,
              specification.scheduling.windowStartTime,
              specification,
            ),
            endsAt: absoluteInstant(
              specification.scheduling.windowEndDate,
              specification.scheduling.windowEndTime,
              specification,
            ),
          }),
        ]);
      case 'deadline':
        return Object.freeze([
          Object.freeze({
            family: 'boundary' as const,
            boundaryKind: 'earliest_start' as const,
            constrainedFacet: 'schedule.start' as const,
            strength: 'hard' as const,
            boundaryAt: absoluteInstant(
              specification.scheduling.earliestStartDate,
              specification.scheduling.earliestStartTime,
              specification,
            ),
          }),
          Object.freeze({
            family: 'boundary' as const,
            boundaryKind: 'latest_completion' as const,
            constrainedFacet: 'schedule.completion' as const,
            strength: 'hard' as const,
            boundaryAt: absoluteInstant(
              specification.scheduling.deadlineDate,
              specification.scheduling.deadlineTime,
              specification,
            ),
          }),
        ]);
      default:
        return Object.freeze([]);
    }
  })();
  const rules = [...schedulingRules];
  if (specification.execution.sessionMode === 'splittable') {
    rules.push(
      Object.freeze({
        family: 'duration' as const,
        durationKind: 'minimum' as const,
        constrainedFacet: 'session.active_duration' as const,
        strength: 'soft' as const,
        durationMicroseconds:
          specification.execution.minSessionMinutes * 60 * 1_000_000,
      }),
    );
  }
  return Object.freeze(rules);
}

function activityProjection(
  activity: TemporalActivityRecord,
  operationId: TemporalOperationId,
): TemporalProjectionItem {
  return Object.freeze({
    id: temporalProjectionId(activity.activityRef),
    subject: Object.freeze({
      source: 'native' as const,
      kind: 'activity' as const,
      id: activity.activityRef,
    }),
    title: activity.title,
    placement: null,
    capabilities: Object.freeze([]),
    revision: 0,
    createdAt: activity.createdAt,
    updatedAt: activity.createdAt,
    lastOperationId: operationId,
  });
}

function acceptedPlacementProjection(
  placement: TemporalAcceptedSchedulePlacement,
): TemporalPlacement {
  switch (placement.kind) {
    case 'date-span':
      return Object.freeze({
        kind: 'date-span' as const,
        startDate: placement.startDate,
        endDateExclusive: placement.endDateExclusive,
      });
    case 'floating-local-interval':
      return Object.freeze({
        kind: 'floating-local' as const,
        start: placement.startsLocalAt,
        end: placement.endsLocalAt,
      });
    case 'named-zone-local-interval':
      return Object.freeze({
        kind: 'zoned' as const,
        start: placement.resolvedStartAt.toZonedDateTimeISO(placement.zoneId),
        end: placement.resolvedEndAt.toZonedDateTimeISO(placement.zoneId),
        sourceStartsLocalAt: placement.startsLocalAt,
        sourceEndsLocalAt: placement.endsLocalAt,
      });
    case 'absolute-interval':
      return Object.freeze({
        kind: 'absolute' as const,
        start: placement.startsAt,
        end: placement.endsAt,
      });
    case 'coarse-local-period':
      return Object.freeze({
        kind: 'coarse-local-period' as const,
        localDate: placement.localDate,
        period: placement.period,
      });
  }
}

function scheduledActivityProjection(
  activity: TemporalActivityRecord,
  schedule: TemporalScheduleRecord,
  operationId: TemporalOperationId,
): TemporalProjectionItem {
  return Object.freeze({
    id: temporalProjectionId(schedule.scheduleRef),
    subject: Object.freeze({
      source: 'native' as const,
      kind: 'activity' as const,
      id: activity.activityRef,
    }),
    title: activity.title,
    placement: acceptedPlacementProjection(schedule.placement),
    capabilities: Object.freeze([]),
    revision: 0,
    createdAt: activity.createdAt,
    updatedAt: activity.createdAt,
    lastOperationId: operationId,
  });
}

function schedulePlacementInput(
  placement: TemporalPlacement,
): TemporalSchedulePlacementInput | null {
  switch (placement.kind) {
    case 'date-span':
      return Object.freeze({
        kind: 'date-span' as const,
        startDate: placement.startDate,
        endDateExclusive: placement.endDateExclusive,
      });
    case 'floating-local':
      return Object.freeze({
        kind: 'floating-local-interval' as const,
        startsLocalAt: placement.start,
        endsLocalAt: placement.end,
      });
    case 'zoned':
      if (placement.start.timeZoneId !== placement.end.timeZoneId) {
        return null;
      }
      return Object.freeze({
        kind: 'named-zone-local-interval' as const,
        startsLocalAt:
          placement.sourceStartsLocalAt ?? placement.start.toPlainDateTime(),
        endsLocalAt:
          placement.sourceEndsLocalAt ?? placement.end.toPlainDateTime(),
        zoneId: placement.start.timeZoneId,
        disambiguation: placement.disambiguation ?? 'reject',
      });
    case 'absolute':
      return Object.freeze({
        kind: 'absolute-interval' as const,
        startsAt: placement.start,
        endsAt: placement.end,
      });
    case 'coarse-local-period':
      return Object.freeze({
        kind: 'coarse-local-period' as const,
        localDate: placement.localDate,
        period: placement.period,
      });
  }
}

function hardConstraintPlacement(
  placement: TemporalPlacement,
  specification: TemporalCreateFields,
): TemporalPlacement | null {
  if (placement.kind === 'absolute') {
    return placement;
  }
  if (placement.kind === 'zoned') {
    return Object.freeze({
      kind: 'absolute' as const,
      start: placement.start.toInstant(),
      end: placement.end.toInstant(),
    });
  }
  if (placement.kind === 'floating-local') {
    try {
      return Object.freeze({
        kind: 'absolute' as const,
        start: placement.start
          .toZonedDateTime(specification.timeZoneId, {
            disambiguation: specification.timeDisambiguation,
          })
          .toInstant(),
        end: placement.end
          .toZonedDateTime(specification.timeZoneId, {
            disambiguation: specification.timeDisambiguation,
          })
          .toInstant(),
      });
    } catch {
      return null;
    }
  }
  return null;
}

function operationIdReuseResult(
  operationId: TemporalOperationId,
): TemporalOperationResult {
  return Object.freeze({
    operationId,
    status: 'rejected' as const,
    code: 'operation-id-reused' as const,
    issues: Object.freeze([
      temporalValidationIssue('temporal.operation.id_reused', ['operationId']),
    ]),
  });
}

function validationResult(
  operationId: TemporalOperationId,
  code: string,
  path: readonly string[],
): TemporalOperationResult {
  return Object.freeze({
    operationId,
    status: 'rejected' as const,
    code: 'validation' as const,
    issues: Object.freeze([temporalValidationIssue(code, path)]),
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

function activityFailureResult(
  operationId: TemporalOperationId,
  error: unknown,
): TemporalOperationResult {
  if (error instanceof TemporalActivityRemoteError) {
    if (
      error.status === 409 &&
      (error.code === 'temporal.activity.operation_id_reused' ||
        error.code === 'temporal.activity.constrained_operation_id_reused' ||
        error.code === 'temporal.schedule.operation_id_reused')
    ) {
      return operationIdReuseResult(operationId);
    }
    if (error.status === 404) {
      return Object.freeze({
        operationId,
        status: 'rejected' as const,
        code: 'not-found' as const,
        issues: Object.freeze([
          temporalValidationIssue('temporal.activity.not_found', ['activityRef']),
        ]),
      });
    }
    if (error.status === 422) {
      return validationResult(
        operationId,
        'temporal.activity.invalid_constrained_create',
        ['payload'],
      );
    }
    return Object.freeze({
      operationId,
      status: 'failed' as const,
      failure: Object.freeze({
        kind:
          error.kind === 'transport'
            ? ('transport' as const)
            : ('unavailable' as const),
        code: 'temporal.activity.remote_unavailable',
        retryable: error.kind === 'transport' || (error.status ?? 0) >= 500,
      }),
    });
  }
  return Object.freeze({
    operationId,
    status: 'failed' as const,
    failure: Object.freeze({
      kind: 'unknown' as const,
      code: 'temporal.activity.lifecycle_failed',
      retryable: false,
    }),
  });
}

function scheduleFailureResult(
  operationId: TemporalOperationId,
  error: unknown,
): TemporalOperationResult {
  if (error instanceof TemporalScheduleRemoteError) {
    if (error.status === 409) {
      return operationIdReuseResult(operationId);
    }
    if (error.status === 404) {
      return Object.freeze({
        operationId,
        status: 'rejected' as const,
        code: 'not-found' as const,
        issues: Object.freeze([
          temporalValidationIssue('temporal.schedule.not_found', ['scheduleRef']),
        ]),
      });
    }
    if (error.status === 422) {
      return validationResult(
        operationId,
        'temporal.schedule.invalid_establish',
        ['payload', 'placement'],
      );
    }
    return Object.freeze({
      operationId,
      status: 'failed' as const,
      failure: Object.freeze({
        kind:
          error.kind === 'transport'
            ? ('transport' as const)
            : ('unavailable' as const),
        code: 'temporal.schedule.remote_unavailable',
        retryable: error.kind === 'transport' || (error.status ?? 0) >= 500,
      }),
    });
  }
  return Object.freeze({
    operationId,
    status: 'failed' as const,
    failure: Object.freeze({
      kind: 'unknown' as const,
      code: 'temporal.schedule.lifecycle_failed',
      retryable: false,
    }),
  });
}

function appliedResult(
  operationId: TemporalOperationId,
  item: TemporalProjectionItem,
): TemporalOperationResult {
  return Object.freeze({
    operationId,
    status: 'applied' as const,
    item,
    snapshotRevision: 0,
    reconciliation: Object.freeze({ status: 'confirmed' as const }),
  });
}

class B04TemporalCreateRuntime implements TemporalCreateRuntime {
  public readonly clock: TemporalCreateRuntime['clock'];
  private readonly flexibleActivities = new Map<string, TemporalCreateMetadata>();
  private readonly records = new Map<string, TemporalCreateRecord>();

  public constructor(
    private readonly base: TemporalCreateRuntime,
    private readonly activitySource: TemporalActivityDataSource,
    private readonly constrainedSource: TemporalConstrainedActivityDataSource,
    private readonly scheduleSource: TemporalScheduleDataSource,
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

  private remember(
    activityRef: string,
    metadata: TemporalCreateMetadata,
    projection: TemporalProjectionItem,
  ): void {
    this.flexibleActivities.set(activityRef, metadata);
    this.records.set(
      projection.id,
      Object.freeze({ projection, metadata }),
    );
  }

  private async establish(
    activityRef: string,
    metadata: TemporalCreateMetadata,
    placement: TemporalPlacement,
  ): Promise<TemporalCreateMutationExecution> {
    const operationId = this.ids.operationId();
    const constraintKind = b04ConstraintKind(metadata.specification);
    const canonicalPlacement =
      constraintKind === 'bounded-window' || constraintKind === 'deadline'
        ? hardConstraintPlacement(placement, metadata.specification)
        : placement;
    const schedulePlacement =
      canonicalPlacement === null
        ? null
        : schedulePlacementInput(canonicalPlacement);
    if (schedulePlacement === null) {
      return Object.freeze({
        result: validationResult(
          operationId,
          'temporal.schedule.hard_constraint_requires_absolute_candidate',
          ['payload', 'placement'],
        ),
        effect: null,
      });
    }

    try {
      const established = await this.activitySource.establishActivitySchedule({
        activityRef,
        operationId,
        placement: schedulePlacement,
      });
      const projection = scheduledActivityProjection(
        established.activity,
        established.schedule,
        operationId,
      );
      const result = appliedResult(operationId, projection);
      const scheduleRef = established.schedule.scheduleRef;
      const expectedMaterialStateRef =
        established.schedule.placementMaterialStateRef;
      const undo = async (): Promise<TemporalOperationResult> => {
        const undoOperationId = this.ids.operationId();
        try {
          await this.scheduleSource.unscheduleSchedule({
            operationId: undoOperationId,
            scheduleRef,
            expectedPlacementMaterialStateRef: expectedMaterialStateRef,
          });
          const restored = activityProjection(established.activity, undoOperationId);
          this.records.delete(projection.id);
          this.remember(activityRef, metadata, restored);
          return appliedResult(undoOperationId, restored);
        } catch (error) {
          return scheduleFailureResult(undoOperationId, error);
        }
      };
      const effect = Object.freeze({
        projection,
        metadata,
        undoToken: this.ids.undoToken(),
        undo,
      }) satisfies TemporalCreateMutationEffect;
      this.records.delete(temporalProjectionId(activityRef));
      this.remember(activityRef, metadata, projection);
      return Object.freeze({ result, effect });
    } catch (error) {
      return Object.freeze({
        result: activityFailureResult(operationId, error),
        effect: null,
      });
    }
  }

  private createEffect(
    prepared: TemporalCreatePreparedOperation,
    activity: TemporalActivityRecord,
    projection: TemporalProjectionItem,
  ): TemporalCreateAppliedEffect {
    const metadata = prepared.metadata;
    const activityRef = activity.activityRef;
    return Object.freeze({
      projection,
      metadata,
      undoToken: null,
      undoAvailable: false,
      undo: async () =>
        unavailableResult(
          this.ids.operationId(),
          'temporal.create.undo_unavailable',
        ),
      replacePlacement: async (placement: TemporalPlacement | null) =>
        placement === null
          ? Object.freeze({
              result: unavailableResult(
                this.ids.operationId(),
                'temporal.schedule.capability_not_available',
              ),
              effect: null,
            })
          : await this.establish(activityRef, metadata, placement),
      remove: async () =>
        Object.freeze({
          result: unavailableResult(
            this.ids.operationId(),
            'temporal.create.remove_unavailable',
          ),
          effect: null,
        }),
    });
  }

  public async execute(
    prepared: TemporalCreatePreparedOperation,
  ): Promise<TemporalCreateExecution> {
    if (prepared.metadata.kind !== 'activity') {
      return await this.base.execute(prepared);
    }

    const constraintKind = b04ConstraintKind(prepared.metadata.specification);
    const hasSessionMinimum =
      prepared.metadata.specification.execution.sessionMode === 'splittable';
    if (constraintKind === null && !hasSessionMinimum) {
      if (prepared.metadata.specification.scheduling.constraintKind === 'preferred-window') {
        return Object.freeze({
          result: unavailableResult(
            prepared.operationId,
            'temporal.create.capability_not_available',
          ),
          effect: null,
        });
      }
      return await this.base.execute(prepared);
    }

    if (!b04FlexibleActivityIntentSupported(prepared)) {
      return Object.freeze({
        result: unavailableResult(
          prepared.operationId,
          'temporal.create.capability_not_available',
        ),
        effect: null,
      });
    }

    try {
      const rules = constraintRules(prepared.metadata.specification);
      const created =
        rules.length === 0
          ? await this.activitySource.createActivity({
              operationId: prepared.operationId,
              title: prepared.command.payload.title,
              ...(isCanonicalLifeAreaRef(prepared.metadata.contextId) ? { lifeAreaRef: prepared.metadata.contextId } : {}),
            })
          : await this.constrainedSource.createConstrainedActivity({
              operationId: prepared.operationId,
              title: prepared.command.payload.title,
              ...(isCanonicalLifeAreaRef(prepared.metadata.contextId) ? { lifeAreaRef: prepared.metadata.contextId } : {}),
              rules,
            });
      const activity = created.activity;
      const projection = activityProjection(activity, prepared.operationId);
      this.remember(activity.activityRef, prepared.metadata, projection);
      const placement = prepared.command.payload.placement;
      if (placement !== null) {
        const scheduled = await this.establish(
          activity.activityRef,
          prepared.metadata,
          placement,
        );
        const accepted = scheduled.effect?.projection;
        if (scheduled.result.status === 'applied' && accepted !== null && accepted !== undefined) {
          return Object.freeze({
            result: appliedResult(prepared.operationId, accepted),
            effect: this.createEffect(prepared, activity, accepted),
          });
        }
        // Creation committed even if the separate Schedule command failed.
        // Report the persisted unplaced Activity so retry cannot duplicate it.
      }
      return Object.freeze({
        result: appliedResult(prepared.operationId, projection),
        effect: this.createEffect(prepared, activity, projection),
      });
    } catch (error) {
      if (error instanceof RangeError) {
        return Object.freeze({
          result: validationResult(
            prepared.operationId,
            'temporal.create.constraint_time_invalid',
            ['scheduling'],
          ),
          effect: null,
        });
      }
      return Object.freeze({
        result: activityFailureResult(prepared.operationId, error),
        effect: null,
      });
    }
  }

  public async placeExistingActivity(
    activityRef: string,
    placement: TemporalPlacement,
  ): Promise<TemporalOperationResult> {
    const metadata = this.flexibleActivities.get(activityRef);
    if (metadata === undefined) {
      return await this.base.placeExistingActivity(activityRef, placement);
    }
    const execution = await this.establish(activityRef, metadata, placement);
    return execution.result;
  }

  public async list(): Promise<readonly TemporalProjectionItem[]> {
    return await this.base.list();
  }

  public async listRecords(): Promise<readonly TemporalCreateRecord[]> {
    const base = await this.base.listRecords();
    const byId = new Map(base.map((record) => [record.projection.id, record]));
    for (const record of this.records.values()) {
      byId.set(record.projection.id, record);
    }
    return Object.freeze([...byId.values()]);
  }
}

export function createB04TemporalCreateRuntime(
  options: B04TemporalCreateRuntimeOptions = {},
): TemporalCreateRuntime {
  const ids = options.ids ?? systemTemporalIdFactory;
  const activitySource =
    options.activityDataSource ?? createRemoteTemporalActivityDataSource();
  const scheduleSource =
    options.scheduleDataSource ?? createRemoteTemporalScheduleDataSource();
  const base =
    options.baseRuntime ??
    createB03TemporalCreateRuntime({
      baseRuntime: createLocalTemporalCreateRuntime({
        activityDataSource: activitySource,
        ids,
      }),
      ...(options.eventDataSource === undefined
        ? {}
        : { eventDataSource: options.eventDataSource }),
      scheduleDataSource: scheduleSource,
      ids,
    });

  return new B04TemporalCreateRuntime(
    base,
    activitySource,
    options.constrainedActivityDataSource ??
      createRemoteTemporalConstrainedActivityDataSource(),
    scheduleSource,
    ids,
  );
}
