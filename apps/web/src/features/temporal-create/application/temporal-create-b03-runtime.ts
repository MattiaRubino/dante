import type { PlainDateTime } from '@dante/time';

import {
  TemporalEventRemoteError,
  TemporalScheduleRemoteError,
  createRemoteTemporalEventDataSource,
  createRemoteTemporalScheduleDataSource,
  systemTemporalIdFactory,
  temporalProjectionId,
  temporalValidationIssue,
  type TemporalAcceptedSchedulePlacement,
  type TemporalEventDataSource,
  type TemporalIdFactory,
  type TemporalOperationId,
  type TemporalOperationResult,
  type TemporalPlacement,
  type TemporalProjectionItem,
  type TemporalScheduleDataSource,
  type TemporalSchedulePlacementInput,
} from '../../temporal';
import {
  createTemporalCreateFields,
  type TemporalCreateFields,
} from '../model/temporal-create-session';
import {
  createLocalTemporalCreateRuntime,
  type TemporalCreateAppliedEffect,
  type TemporalCreateExecution,
  type TemporalCreateMutationEffect,
  type TemporalCreateMutationExecution,
  type TemporalCreatePreparedOperation,
  type TemporalCreatePreparation,
  type TemporalCreateRecord,
  type TemporalCreateRuntime,
} from './temporal-create-runtime';

export type B03TemporalCreateRuntimeOptions = Readonly<{
  baseRuntime?: TemporalCreateRuntime;
  eventDataSource?: TemporalEventDataSource;
  scheduleDataSource?: TemporalScheduleDataSource;
  ids?: TemporalIdFactory;
}>;

function canonicalJsonValue(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(canonicalJsonValue);
  }
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

function b03dScheduledEventIntentSupported(
  prepared: TemporalCreatePreparedOperation,
): boolean {
  const specification = prepared.metadata.specification;
  if (
    prepared.metadata.kind !== 'event' ||
    prepared.command.payload.placement === null ||
    prepared.metadata.contextId !== 'personale' ||
    prepared.metadata.notes.length !== 0 ||
    specification.appearanceTone !== null ||
    specification.eventRecurrence.patternKind !== 'none' ||
    (specification.eventRecurrence.owner ?? null) !== null ||
    specification.scheduling.constraintKind !== 'none' ||
    specification.scheduling.fallbackPolicy !== 'inherit' ||
    specification.confirmation.outcomePolicy !== 'inherit' ||
    specification.confirmation.reminderLeadMinutes !== null
  ) {
    return false;
  }

  const baseline = createTemporalCreateFields({
    title: specification.title,
    kind: 'event',
    date: specification.date,
    timeSemantics: specification.timeSemantics,
    startTime: specification.startTime,
    durationMinutes: specification.durationMinutes,
    timeMode: specification.timeMode,
    timeZoneId: specification.timeZoneId,
    timeDisambiguation: specification.timeDisambiguation,
    coarsePeriod: specification.coarsePeriod,
    contextId: 'personale',
  });

  return (
    sameStructuredIntent(specification.execution, baseline.execution) &&
    sameStructuredIntent(
      unsupportedEventIntent(specification.event),
      unsupportedEventIntent(baseline.event),
    )
  );
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
    case 'zoned': {
      if (placement.start.timeZoneId !== placement.end.timeZoneId) {
        return null;
      }
      const disambiguation = placement.disambiguation ?? 'reject';
      return Object.freeze({
        kind: 'named-zone-local-interval' as const,
        startsLocalAt:
          placement.sourceStartsLocalAt ?? placement.start.toPlainDateTime(),
        endsLocalAt:
          placement.sourceEndsLocalAt ?? placement.end.toPlainDateTime(),
        zoneId: placement.start.timeZoneId,
        disambiguation,
      });
    }
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

function unsupportedMutationResult(
  operationId: TemporalOperationId,
): TemporalOperationResult {
  return Object.freeze({
    operationId,
    status: 'failed' as const,
    failure: Object.freeze({
      kind: 'unavailable' as const,
      code: 'temporal.event.lifecycle_capability_not_available',
      retryable: false,
    }),
  });
}

function invalidPlacementMutationResult(
  operationId: TemporalOperationId,
): TemporalOperationResult {
  return Object.freeze({
    operationId,
    status: 'rejected' as const,
    code: 'validation' as const,
    issues: Object.freeze([
      temporalValidationIssue('temporal.schedule.invalid_revision', [
        'payload',
        'placement',
      ]),
    ]),
  });
}

function scheduleMutationFailureResult(
  operationId: TemporalOperationId,
  error: unknown,
): TemporalOperationResult {
  if (error instanceof TemporalScheduleRemoteError) {
    if (
      error.status === 409 &&
      error.code === 'temporal.schedule.operation_id_reused'
    ) {
      return operationIdReuseResult(operationId);
    }
    if (
      error.status === 409 &&
      (error.code === 'temporal.schedule.revision_conflict' ||
        error.code === 'temporal.schedule.unschedule_conflict')
    ) {
      return Object.freeze({
        operationId,
        status: 'rejected' as const,
        code: 'revision-conflict' as const,
        issues: Object.freeze([
          temporalValidationIssue('temporal.schedule.expected_state_conflict', [
            'expectedPlacementMaterialStateRef',
          ]),
        ]),
      });
    }
    if (
      error.status === 409 &&
      error.code === 'temporal.schedule.undo_conflict'
    ) {
      return Object.freeze({
        operationId,
        status: 'rejected' as const,
        code: 'undo-conflict' as const,
        issues: Object.freeze([
          temporalValidationIssue('temporal.schedule.undo_conflict', [
            'undoToken',
          ]),
        ]),
      });
    }
    if (error.status === 404) {
      return Object.freeze({
        operationId,
        status: 'rejected' as const,
        code:
          error.code === 'temporal.schedule.undo_not_found'
            ? ('undo-not-found' as const)
            : ('not-found' as const),
        issues: Object.freeze([
          temporalValidationIssue('temporal.schedule.not_found', [
            'scheduleRef',
          ]),
        ]),
      });
    }
    if (error.status === 422) {
      return invalidPlacementMutationResult(operationId);
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

function scheduledEventProjection(
  result: Awaited<ReturnType<TemporalEventDataSource['createScheduledEvent']>>,
  operationId: TemporalOperationId,
): TemporalProjectionItem {
  return Object.freeze({
    id: temporalProjectionId(result.schedule.scheduleRef),
    subject: Object.freeze({
      source: 'native' as const,
      kind: 'event',
      id: result.event.eventRef,
    }),
    title: result.event.title,
    placement: acceptedPlacementProjection(result.schedule.placement),
    capabilities: Object.freeze([]),
    revision: 0,
    createdAt: result.event.createdAt,
    updatedAt: result.event.createdAt,
    lastOperationId: operationId,
  });
}

function failureExecution(
  operationId: TemporalOperationId,
  error: unknown,
): TemporalCreateExecution {
  if (
    error instanceof TemporalEventRemoteError &&
    error.status === 409 &&
    error.code === 'temporal.event.operation_id_reused'
  ) {
    return Object.freeze({
      result: operationIdReuseResult(operationId),
      effect: null,
    });
  }
  if (error instanceof TemporalEventRemoteError && error.status === 422) {
    return Object.freeze({
      result: Object.freeze({
        operationId,
        status: 'rejected' as const,
        code: 'validation' as const,
        issues: Object.freeze([
          temporalValidationIssue('temporal.event.invalid_schedule_create', [
            'payload',
          ]),
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
          error instanceof TemporalEventRemoteError &&
          error.kind === 'transport'
            ? ('transport' as const)
            : ('unavailable' as const),
        code: 'temporal.event.remote_unavailable',
        retryable:
          error instanceof TemporalEventRemoteError
            ? error.kind === 'transport' || (error.status ?? 0) >= 500
            : false,
      }),
    }),
    effect: null,
  });
}

class B03TemporalCreateRuntime implements TemporalCreateRuntime {
  public readonly clock: TemporalCreateRuntime['clock'];

  public constructor(
    private readonly base: TemporalCreateRuntime,
    private readonly eventSource: TemporalEventDataSource,
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

  public async execute(
    prepared: TemporalCreatePreparedOperation,
  ): Promise<TemporalCreateExecution> {
    if (prepared.metadata.kind !== 'event') {
      return await this.base.execute(prepared);
    }
    if (!b03dScheduledEventIntentSupported(prepared)) {
      return Object.freeze({
        result: Object.freeze({
          operationId: prepared.operationId,
          status: 'failed' as const,
          failure: Object.freeze({
            kind: 'unavailable' as const,
            code: 'temporal.create.capability_not_available',
            retryable: false,
          }),
        }),
        effect: null,
      });
    }

    const placement = prepared.command.payload.placement;
    const schedulePlacement =
      placement === null ? null : schedulePlacementInput(placement);
    if (schedulePlacement === null) {
      return Object.freeze({
        result: Object.freeze({
          operationId: prepared.operationId,
          status: 'failed' as const,
          failure: Object.freeze({
            kind: 'unavailable' as const,
            code: 'temporal.create.capability_not_available',
            retryable: false,
          }),
        }),
        effect: null,
      });
    }

    try {
      const created = await this.eventSource.createScheduledEvent({
        operationId: prepared.operationId,
        title: prepared.command.payload.title,
        agendaParts: prepared.metadata.specification.event.agendaParts,
        placement: schedulePlacement,
      });
      const projection = scheduledEventProjection(created, prepared.operationId);
      const result = Object.freeze({
        operationId: prepared.operationId,
        status: 'applied' as const,
        item: projection,
        snapshotRevision: 0,
        reconciliation: Object.freeze({ status: 'confirmed' as const }),
      });

      let currentProjection = projection;
      let currentMaterialStateRef: string | null =
        created.schedule.placementMaterialStateRef;
      // Keep the exact accepted authoring policy alongside the display projection.
      // In particular, named-zone overlap choices (earlier/later) must survive
      // revision Undo; reconstructing them from the display projection can silently
      // collapse an accepted ambiguous wall-clock choice to "reject".
      let currentPlacementInput: TemporalSchedulePlacementInput | null =
        schedulePlacement;

      const replaceProjection = (
        nextPlacement: TemporalPlacement | null,
        operationId: TemporalOperationId,
      ): TemporalProjectionItem => {
        currentProjection = Object.freeze({
          ...currentProjection,
          placement: nextPlacement,
          revision: currentProjection.revision + 1,
          updatedAt: this.clock.now(),
          lastOperationId: operationId,
        });
        return currentProjection;
      };

      const appliedMutationResult = (
        operationId: TemporalOperationId,
        item: TemporalProjectionItem,
      ): TemporalOperationResult =>
        Object.freeze({
          operationId,
          status: 'applied' as const,
          item,
          snapshotRevision: item.revision,
          reconciliation: Object.freeze({ status: 'confirmed' as const }),
        });

      const mutationEffect = (
        item: TemporalProjectionItem,
        undo: () => Promise<TemporalOperationResult>,
      ): TemporalCreateMutationEffect =>
        Object.freeze({
          projection: item,
          metadata: prepared.metadata,
          undoToken: this.ids.undoToken(),
          undo,
        });

      const reviseCurrent = async (
        nextPlacement: TemporalPlacement,
      ): Promise<TemporalCreateMutationExecution> => {
        const operationId = this.ids.operationId();
        if (
          currentMaterialStateRef === null ||
          currentProjection.placement === null ||
          currentPlacementInput === null
        ) {
          return Object.freeze({
            result: unsupportedMutationResult(operationId),
            effect: null,
          });
        }
        const requestedPlacement = schedulePlacementInput(nextPlacement);
        const previousPlacementInput = currentPlacementInput;
        if (requestedPlacement === null) {
          return Object.freeze({
            result: invalidPlacementMutationResult(operationId),
            effect: null,
          });
        }

        const expectedMaterialStateRef = currentMaterialStateRef;
        try {
          const revised = await this.scheduleSource.reviseSchedule({
            operationId,
            scheduleRef: created.schedule.scheduleRef,
            expectedPlacementMaterialStateRef: expectedMaterialStateRef,
            placement: requestedPlacement,
          });
          currentMaterialStateRef = revised.placementMaterialStateRef;
          currentPlacementInput = requestedPlacement;
          const item = replaceProjection(
            acceptedPlacementProjection(revised.placement),
            operationId,
          );
          const undoExpectedMaterialStateRef = revised.placementMaterialStateRef;
          const undo = async (): Promise<TemporalOperationResult> => {
            const undoOperationId = this.ids.operationId();
            try {
              const restored = await this.scheduleSource.reviseSchedule({
                operationId: undoOperationId,
                scheduleRef: created.schedule.scheduleRef,
                expectedPlacementMaterialStateRef:
                  undoExpectedMaterialStateRef,
                placement: previousPlacementInput,
              });
              currentMaterialStateRef = restored.placementMaterialStateRef;
              currentPlacementInput = previousPlacementInput;
              return appliedMutationResult(
                undoOperationId,
                replaceProjection(
                  acceptedPlacementProjection(restored.placement),
                  undoOperationId,
                ),
              );
            } catch (error) {
              return scheduleMutationFailureResult(undoOperationId, error);
            }
          };
          return Object.freeze({
            result: appliedMutationResult(operationId, item),
            effect: mutationEffect(item, undo),
          });
        } catch (error) {
          return Object.freeze({
            result: scheduleMutationFailureResult(operationId, error),
            effect: null,
          });
        }
      };

      const postponeCurrent = async (): Promise<TemporalCreateMutationExecution> => {
        const operationId = this.ids.operationId();
        if (
          currentMaterialStateRef === null ||
          currentProjection.placement === null ||
          currentPlacementInput === null
        ) {
          return Object.freeze({
            result: unsupportedMutationResult(operationId),
            effect: null,
          });
        }
        const expectedMaterialStateRef = currentMaterialStateRef;
        const postponedPlacementInput = currentPlacementInput;
        try {
          const postponed = await this.scheduleSource.unscheduleSchedule({
            operationId,
            scheduleRef: created.schedule.scheduleRef,
            expectedPlacementMaterialStateRef: expectedMaterialStateRef,
          });
          currentMaterialStateRef = null;
          currentPlacementInput = null;
          const item = replaceProjection(null, operationId);
          const undo = async (): Promise<TemporalOperationResult> => {
            const undoOperationId = this.ids.operationId();
            try {
              const restored =
                await this.scheduleSource.undoScheduleUnschedule({
                  operationId: undoOperationId,
                  scheduleRef: created.schedule.scheduleRef,
                  unscheduleOperationId: postponed.unscheduleOperationId,
                });
              currentMaterialStateRef = restored.placementMaterialStateRef;
              currentPlacementInput = postponedPlacementInput;
              return appliedMutationResult(
                undoOperationId,
                replaceProjection(
                  acceptedPlacementProjection(restored.placement),
                  undoOperationId,
                ),
              );
            } catch (error) {
              return scheduleMutationFailureResult(undoOperationId, error);
            }
          };
          return Object.freeze({
            result: appliedMutationResult(operationId, item),
            effect: mutationEffect(item, undo),
          });
        } catch (error) {
          return Object.freeze({
            result: scheduleMutationFailureResult(operationId, error),
            effect: null,
          });
        }
      };

      const effect = Object.freeze({
        projection,
        metadata: prepared.metadata,
        undoToken: null,
        undoAvailable: false,
        undo: async () => unsupportedMutationResult(this.ids.operationId()),
        replacePlacement: async (nextPlacement: TemporalPlacement | null) =>
          nextPlacement === null
            ? await postponeCurrent()
            : await reviseCurrent(nextPlacement),
        remove: async () =>
          Object.freeze({
            result: unsupportedMutationResult(this.ids.operationId()),
            effect: null,
          }),
      }) satisfies TemporalCreateAppliedEffect;
      return Object.freeze({ result, effect });
    } catch (error) {
      return failureExecution(prepared.operationId, error);
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

export function createB03TemporalCreateRuntime(
  options: B03TemporalCreateRuntimeOptions = {},
): TemporalCreateRuntime {
  return new B03TemporalCreateRuntime(
    options.baseRuntime ?? createLocalTemporalCreateRuntime(),
    options.eventDataSource ?? createRemoteTemporalEventDataSource(),
    options.scheduleDataSource ?? createRemoteTemporalScheduleDataSource(),
    options.ids ?? systemTemporalIdFactory,
  );
}

// Type-only guard: retain a named local-time symbol in this adapter's public
// compilation unit so Temporal placement narrowing stays tied to @dante/time.
void (null as PlainDateTime | null);
