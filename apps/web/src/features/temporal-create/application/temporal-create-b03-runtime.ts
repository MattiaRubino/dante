import type { PlainDateTime } from '@dante/time';

import {
  TemporalEventRemoteError,
  createRemoteTemporalEventDataSource,
  temporalProjectionId,
  temporalValidationIssue,
  type TemporalEventDataSource,
  type TemporalOperationId,
  type TemporalOperationResult,
  type TemporalPlacement,
  type TemporalProjectionItem,
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
  type TemporalCreateMutationExecution,
  type TemporalCreatePreparedOperation,
  type TemporalCreatePreparation,
  type TemporalCreateRecord,
  type TemporalCreateRuntime,
} from './temporal-create-runtime';

export type B03TemporalCreateRuntimeOptions = Readonly<{
  baseRuntime?: TemporalCreateRuntime;
  eventDataSource?: TemporalEventDataSource;
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

function b03bScheduledEventIntentSupported(
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
    specification.scheduling.constraintKind !== 'none'
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
    sameStructuredIntent(specification.scheduling, baseline.scheduling) &&
    sameStructuredIntent(specification.execution, baseline.execution) &&
    sameStructuredIntent(
      specification.eventRecurrence,
      baseline.eventRecurrence,
    ) &&
    sameStructuredIntent(specification.confirmation, baseline.confirmation) &&
    sameStructuredIntent(specification.event, baseline.event)
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
  placement: Awaited<
    ReturnType<TemporalEventDataSource['createScheduledEvent']>
  >['schedule']['placement'],
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
    if (!b03bScheduledEventIntentSupported(prepared)) {
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
      const unavailableMutation = async (): Promise<TemporalCreateMutationExecution> =>
        Object.freeze({
          result: unsupportedMutationResult(prepared.operationId),
          effect: null,
        });
      const effect = Object.freeze({
        projection,
        metadata: prepared.metadata,
        undoToken: null,
        undoAvailable: false,
        undo: async () => unsupportedMutationResult(prepared.operationId),
        replacePlacement: async (_placement: TemporalPlacement | null) =>
          await unavailableMutation(),
        remove: async () => await unavailableMutation(),
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
  );
}

// Type-only guard: retain a named local-time symbol in this adapter's public
// compilation unit so Temporal placement narrowing stays tied to @dante/time.
void (null as PlainDateTime | null);
