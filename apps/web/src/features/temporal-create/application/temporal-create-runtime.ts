import type { PlainDate } from '@dante/time';

import {
  InMemoryTemporalWorkspace,
  TemporalActivityRemoteError,
  createRemoteTemporalActivityDataSource,
  systemTemporalClock,
  systemTemporalIdFactory,
  temporalOperationId,
  temporalProjectionId,
  temporalValidationIssue,
  type GetTemporalProjectionQuery,
  type GetTemporalProjectionResult,
  type ListTemporalProjectionsQuery,
  type ListTemporalProjectionsResult,
  type TemporalActivityDataSource,
  type TemporalActivityRecord,
  type TemporalClock,
  type TemporalCommand,
  type TemporalIdFactory,
  type TemporalOperationId,
  type TemporalOperationResult,
  type TemporalPlacement,
  type TemporalProjectionItem,
  type TemporalQuery,
  type TemporalQueryResult,
  type TemporalSchedulePlacementInput,
  type TemporalScheduleRecord,
  type TemporalUndoToken,
  type TemporalValidationIssue,
  type TemporalWorkspacePort,
} from '../../temporal';
import {
  buildTemporalCreatePlacement,
  createTemporalCreateFields,
  validateTemporalCreateFields,
  type TemporalCreateFields,
  type TemporalCreateKind,
  type TemporalCreateTimeSemantics,
} from '../model/temporal-create-session';

export type TemporalCreateRecurrenceOwner = 'event' | 'routine' | null;

const LIFE_AREA_REF = /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export function isCanonicalLifeAreaRef(value: string): boolean {
  return LIFE_AREA_REF.test(value);
}

export type TemporalCreateMetadata = Readonly<{
  kind: TemporalCreateKind;
  contextId: string;
  notes: string;
  timeSemantics: TemporalCreateTimeSemantics;
  timeZoneId: string;
  recurrenceOwner: TemporalCreateRecurrenceOwner;
  specification: TemporalCreateFields;
}>;

export type TemporalCreatePreparedOperation = Readonly<{
  operationId: TemporalOperationId;
  command: Readonly<{
    type: 'temporal.projection.create';
    operationId: TemporalOperationId;
    source: 'manual';
    issuedAt: ReturnType<TemporalClock['now']>;
    payload: Readonly<{
      id: ReturnType<TemporalIdFactory['projectionId']>;
      subject: Readonly<{
        source: 'native';
        kind: TemporalCreateKind;
        id: string;
      }>;
      title: string;
      placement: ReturnType<typeof buildTemporalCreatePlacement>;
      capabilities: readonly (
        | 'placement'
        | 'recurrence'
        | 'execution'
        | 'actual'
        | 'confirmation'
        | 'replanning'
        | 'history'
        | 'notes'
      )[];
    }>;
  }>;
  metadata: TemporalCreateMetadata;
}>;

export type TemporalCreatePreparation =
  | Readonly<{
      status: 'invalid';
      issues: readonly TemporalValidationIssue[];
    }>
  | Readonly<{
      status: 'ready';
      prepared: TemporalCreatePreparedOperation;
    }>;

export type TemporalCreateRecord = Readonly<{
  projection: TemporalProjectionItem;
  metadata: TemporalCreateMetadata;
}>;

export type TemporalCreateMutationEffect = Readonly<{
  projection: TemporalProjectionItem | null;
  metadata: TemporalCreateMetadata;
  undoToken: TemporalUndoToken;
  undo: () => Promise<TemporalOperationResult>;
}>;

export type TemporalCreateMutationExecution = Readonly<{
  result: TemporalOperationResult;
  effect: TemporalCreateMutationEffect | null;
}>;

export type TemporalCreateAppliedEffect = Readonly<{
  projection: TemporalProjectionItem;
  metadata: TemporalCreateMetadata;
  undoToken: TemporalUndoToken | null;
  undoAvailable: boolean;
  undo: () => Promise<TemporalOperationResult>;
  replacePlacement: (
    placement: TemporalPlacement | null,
  ) => Promise<TemporalCreateMutationExecution>;
  remove: () => Promise<TemporalCreateMutationExecution>;
}>;

export type TemporalCreateExecution = Readonly<{
  result: TemporalOperationResult;
  effect: TemporalCreateAppliedEffect | null;
}>;

export interface TemporalCreateRuntime {
  readonly clock: TemporalClock;
  prepare(
    fields: TemporalCreateFields,
    operationId?: TemporalOperationId,
  ): TemporalCreatePreparation;
  execute(
    prepared: TemporalCreatePreparedOperation,
  ): Promise<TemporalCreateExecution>;
  placeExistingActivity(
    activityRef: string,
    placement: TemporalPlacement,
  ): Promise<TemporalOperationResult>;
  list(): Promise<readonly TemporalProjectionItem[]>;
  listRecords(): Promise<readonly TemporalCreateRecord[]>;
}

function recurrenceOwnerForFields(
  fields: TemporalCreateFields,
): TemporalCreateRecurrenceOwner {
  if (fields.eventRecurrence.patternKind === 'none') {
    return null;
  }
  return fields.kind === 'event' ? 'event' : 'routine';
}

function capabilitiesForFields(
  fields: TemporalCreateFields,
): TemporalCreatePreparedOperation['command']['payload']['capabilities'] {
  const capabilities: TemporalCreatePreparedOperation['command']['payload']['capabilities'][number][] =
    ['placement', 'confirmation', 'history', 'notes'];
  if (
    fields.kind === 'event' &&
    fields.eventRecurrence.patternKind !== 'none'
  ) {
    capabilities.push('recurrence');
  }
  if (fields.kind === 'activity') {
    capabilities.push('execution', 'actual', 'replanning');
  }
  return Object.freeze(capabilities);
}

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

function richIntentFingerprint(metadata: TemporalCreateMetadata): string {
  return JSON.stringify(canonicalJsonValue(metadata));
}

function sameStructuredIntent(left: unknown, right: unknown): boolean {
  return (
    JSON.stringify(canonicalJsonValue(left)) ===
    JSON.stringify(canonicalJsonValue(right))
  );
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

function notFoundResult(
  operationId: TemporalOperationId,
): TemporalOperationResult {
  return Object.freeze({
    operationId,
    status: 'rejected' as const,
    code: 'not-found' as const,
    issues: Object.freeze([
      temporalValidationIssue('temporal.projection.not_found', [
        'payload',
        'id',
      ]),
    ]),
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

function b01ActivityIntentSupported(
  prepared: TemporalCreatePreparedOperation,
): boolean {
  const specification = prepared.metadata.specification;
  const baseline = createTemporalCreateFields({
    date: specification.date,
    timeZoneId: specification.timeZoneId,
    contextId: specification.contextId,
    timeSemantics: 'unscheduled',
  });

  return (
    prepared.metadata.kind === 'activity' &&
    prepared.command.payload.placement === null &&
    prepared.metadata.timeSemantics === 'unscheduled' &&
    (prepared.metadata.contextId === 'personale' || isCanonicalLifeAreaRef(prepared.metadata.contextId)) &&
    prepared.metadata.notes.length === 0 &&
    specification.durationMinutes === baseline.durationMinutes &&
    specification.appearanceTone === null &&
    specification.eventRecurrence.patternKind === 'none' &&
    specification.scheduling.constraintKind === 'none' &&
    JSON.stringify(specification.execution) ===
      JSON.stringify(baseline.execution) &&
    JSON.stringify(specification.confirmation) ===
      JSON.stringify(baseline.confirmation)
  );
}

function b02eScheduledActivityIntentSupported(
  prepared: TemporalCreatePreparedOperation,
): boolean {
  const specification = prepared.metadata.specification;
  const placement = prepared.command.payload.placement;
  if (
    prepared.metadata.kind !== 'activity' ||
    placement === null ||
    (prepared.metadata.contextId !== 'personale' && !isCanonicalLifeAreaRef(prepared.metadata.contextId)) ||
    prepared.metadata.notes.length !== 0 ||
    specification.appearanceTone !== null ||
    specification.eventRecurrence.patternKind !== 'none' ||
    specification.scheduling.constraintKind !== 'none'
  ) {
    return false;
  }

  const baseline = createTemporalCreateFields({
    title: specification.title,
    kind: 'activity',
    date: specification.date,
    timeSemantics: specification.timeSemantics,
    startTime: specification.startTime,
    durationMinutes: specification.durationMinutes,
    timeMode: specification.timeMode,
    timeZoneId: specification.timeZoneId,
    timeDisambiguation: specification.timeDisambiguation,
    coarsePeriod: specification.coarsePeriod,
    contextId: specification.contextId,
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

function canonicalActivityIntentSupported(
  prepared: TemporalCreatePreparedOperation,
): boolean {
  return (
    b01ActivityIntentSupported(prepared) ||
    b02eScheduledActivityIntentSupported(prepared)
  );
}

function activityProjection(
  activity: TemporalActivityRecord,
  operationId: TemporalOperationId,
): TemporalProjectionItem {
  const id = temporalProjectionId(activity.activityRef);
  return Object.freeze({
    id,
    subject: Object.freeze({
      source: 'native' as const,
      kind: 'activity',
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

function zonedDisambiguation(
  placement: Extract<TemporalPlacement, Readonly<{ kind: 'zoned' }>>,
): 'reject' | 'earlier' | 'later' | null {
  const zoneId = placement.start.timeZoneId;
  if (placement.end.timeZoneId !== zoneId) {
    return null;
  }
  const localStart =
    placement.sourceStartsLocalAt ?? placement.start.toPlainDateTime();
  const localEnd = placement.sourceEndsLocalAt ?? placement.end.toPlainDateTime();
  const candidates =
    placement.disambiguation === undefined
      ? (['reject', 'earlier', 'later'] as const)
      : ([placement.disambiguation] as const);
  for (const disambiguation of candidates) {
    try {
      const resolvedStart = localStart.toZonedDateTime(zoneId, {
        disambiguation,
      });
      const resolvedEnd = localEnd.toZonedDateTime(zoneId, { disambiguation });
      if (
        resolvedStart.toInstant().equals(placement.start.toInstant()) &&
        resolvedEnd.toInstant().equals(placement.end.toInstant())
      ) {
        return disambiguation;
      }
    } catch {
      // Try the next explicit policy when the accepted placement did not carry one.
    }
  }
  return null;
}

function acceptedPlacementProjection(
  schedule: TemporalScheduleRecord,
): TemporalPlacement {
  const placement = schedule.placement;
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
    case 'named-zone-local-interval': {
      const projected = Object.freeze({
        kind: 'zoned' as const,
        start: placement.resolvedStartAt.toZonedDateTimeISO(placement.zoneId),
        end: placement.resolvedEndAt.toZonedDateTimeISO(placement.zoneId),
        sourceStartsLocalAt: placement.startsLocalAt,
        sourceEndsLocalAt: placement.endsLocalAt,
      });
      const disambiguation = zonedDisambiguation(projected);
      return Object.freeze({
        ...projected,
        ...(disambiguation === null ? {} : { disambiguation }),
      });
    }
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
      kind: 'activity',
      id: activity.activityRef,
    }),
    title: activity.title,
    placement: acceptedPlacementProjection(schedule),
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
    case 'zoned': {
      const disambiguation = zonedDisambiguation(placement);
      if (disambiguation === null) {
        return null;
      }
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

class RemoteActivityTemporalWorkspace implements TemporalWorkspacePort {
  public constructor(private readonly source: TemporalActivityDataSource) {}

  public async execute(
    command: TemporalCommand,
    lifeAreaRef?: string,
  ): Promise<TemporalOperationResult> {
    if (command.type === 'temporal.placement.replace') {
      const placement = command.payload.placement;
      const schedulePlacement =
        placement === null ? null : schedulePlacementInput(placement);
      if (
        command.payload.expectedRevision !== 0 ||
        placement === null ||
        schedulePlacement === null
      ) {
        return unavailableResult(
          command.operationId,
          'temporal.schedule.capability_not_available',
        );
      }

      try {
        const result = await this.source.establishActivitySchedule({
          activityRef: command.payload.id,
          operationId: command.operationId,
          placement: schedulePlacement,
        });
        return Object.freeze({
          operationId: command.operationId,
          status: 'applied' as const,
          item: scheduledActivityProjection(
            result.activity,
            result.schedule,
            command.operationId,
          ),
          snapshotRevision: 0,
          reconciliation: Object.freeze({ status: 'confirmed' as const }),
        });
      } catch (error) {
        if (
          error instanceof TemporalActivityRemoteError &&
          error.status === 404
        ) {
          return notFoundResult(command.operationId);
        }
        if (
          error instanceof TemporalActivityRemoteError &&
          error.status === 409 &&
          error.code === 'temporal.schedule.operation_id_reused'
        ) {
          return operationIdReuseResult(command.operationId);
        }
        if (
          error instanceof TemporalActivityRemoteError &&
          error.status === 422
        ) {
          return Object.freeze({
            operationId: command.operationId,
            status: 'rejected' as const,
            code: 'validation' as const,
            issues: Object.freeze([
              temporalValidationIssue(
                'temporal.schedule.invalid_establish',
                ['payload', 'placement'],
              ),
            ]),
          });
        }
        return Object.freeze({
          operationId: command.operationId,
          status: 'failed' as const,
          failure: Object.freeze({
            kind:
              error instanceof TemporalActivityRemoteError &&
              error.kind === 'transport'
                ? ('transport' as const)
                : ('unavailable' as const),
            code: 'temporal.schedule.remote_unavailable',
            retryable:
              error instanceof TemporalActivityRemoteError
                ? error.kind === 'transport' || (error.status ?? 0) >= 500
                : false,
          }),
        });
      }
    }

    if (
      command.type !== 'temporal.projection.create' ||
      command.payload.subject.kind !== 'activity'
    ) {
      return unavailableResult(
        command.operationId,
        'temporal.create.capability_not_available',
      );
    }

    const placement = command.payload.placement;
    const schedulePlacement =
      placement === null ? null : schedulePlacementInput(placement);
    if (placement !== null && schedulePlacement === null) {
      return unavailableResult(
        command.operationId,
        'temporal.create.capability_not_available',
      );
    }

    try {
      if (placement === null) {
        const result = await this.source.createActivity({
          operationId: command.operationId,
          title: command.payload.title,
          ...(lifeAreaRef === undefined ? {} : { lifeAreaRef }),
        });
        return Object.freeze({
          operationId: command.operationId,
          status: 'applied' as const,
          item: activityProjection(result.activity, command.operationId),
          snapshotRevision: 0,
          reconciliation: Object.freeze({ status: 'confirmed' as const }),
        });
      }

      const result = await this.source.createScheduledActivity({
        operationId: command.operationId,
        title: command.payload.title,
        ...(lifeAreaRef === undefined ? {} : { lifeAreaRef }),
        placement: schedulePlacement as TemporalSchedulePlacementInput,
      });
      return Object.freeze({
        operationId: command.operationId,
        status: 'applied' as const,
        item: scheduledActivityProjection(
          result.activity,
          result.schedule,
          command.operationId,
        ),
        snapshotRevision: 0,
        reconciliation: Object.freeze({ status: 'confirmed' as const }),
      });
    } catch (error) {
      if (
        error instanceof TemporalActivityRemoteError &&
        error.status === 409 &&
        (error.code === 'temporal.activity.operation_id_reused' ||
          error.code === 'temporal.schedule.operation_id_reused')
      ) {
        return operationIdReuseResult(command.operationId);
      }
      if (
        error instanceof TemporalActivityRemoteError &&
        error.status === 422
      ) {
        return Object.freeze({
          operationId: command.operationId,
          status: 'rejected' as const,
          code: 'validation' as const,
          issues: Object.freeze([
            temporalValidationIssue(
              placement === null
                ? 'temporal.activity.invalid_create'
                : 'temporal.schedule.invalid_establish',
              ['payload'],
            ),
          ]),
        });
      }
      return Object.freeze({
        operationId: command.operationId,
        status: 'failed' as const,
        failure: Object.freeze({
          kind:
            error instanceof TemporalActivityRemoteError &&
            error.kind === 'transport'
              ? ('transport' as const)
              : ('unavailable' as const),
          code:
            placement === null
              ? 'temporal.activity.remote_unavailable'
              : 'temporal.schedule.remote_unavailable',
          retryable:
            error instanceof TemporalActivityRemoteError
              ? error.kind === 'transport' || (error.status ?? 0) >= 500
              : false,
        }),
      });
    }
  }

  public query(
    request: GetTemporalProjectionQuery,
  ): Promise<GetTemporalProjectionResult>;
  public query(
    request: ListTemporalProjectionsQuery,
  ): Promise<ListTemporalProjectionsResult>;
  public async query(request: TemporalQuery): Promise<TemporalQueryResult> {
    const records = await this.source.loadUnplaced();
    const projections = Object.freeze(
      records.map((activity) =>
        activityProjection(
          activity,
          temporalOperationId(`activity-read:${activity.activityRef}`),
        ),
      ),
    );
    if (request.type === 'temporal.projection.get') {
      const item = projections.find((candidate) => candidate.id === request.id);
      return item
        ? Object.freeze({
            type: 'temporal.projection.get' as const,
            status: 'ok' as const,
            item,
          })
        : Object.freeze({
            type: 'temporal.projection.get' as const,
            status: 'not-found' as const,
          });
    }
    return Object.freeze({
      type: 'temporal.projection.list' as const,
      status: 'ok' as const,
      snapshot: Object.freeze({ revision: 0, items: projections }),
    });
  }

  public subscribe(): () => void {
    return () => undefined;
  }
}

class LocalTemporalCreateRuntime implements TemporalCreateRuntime {
  public readonly clock: TemporalClock;
  private readonly records = new Map<
    TemporalProjectionItem['id'],
    TemporalCreateRecord
  >();
  private readonly richOperationFingerprints = new Map<
    TemporalOperationId,
    string
  >();

  public constructor(
    private readonly workspace: TemporalWorkspacePort,
    private readonly ids: TemporalIdFactory,
    clock: TemporalClock,
    private readonly canonicalActivityOnly = false,
  ) {
    this.clock = clock;
  }

  public prepare(
    fields: TemporalCreateFields,
    operationId = this.ids.operationId(),
  ): TemporalCreatePreparation {
    const specification = createTemporalCreateFields(fields);
    const issues = validateTemporalCreateFields(specification);
    if (issues.length > 0) {
      return Object.freeze({ status: 'invalid', issues });
    }

    const projectionId = this.ids.projectionId();
    const metadata = Object.freeze({
      kind: specification.kind,
      contextId: specification.contextId,
      notes: specification.notes.trim(),
      timeSemantics: specification.timeSemantics,
      timeZoneId: specification.timeZoneId,
      recurrenceOwner: recurrenceOwnerForFields(specification),
      specification,
    }) satisfies TemporalCreateMetadata;

    const command = Object.freeze({
      type: 'temporal.projection.create' as const,
      operationId,
      source: 'manual' as const,
      issuedAt: this.clock.now(),
      payload: Object.freeze({
        id: projectionId,
        subject: Object.freeze({
          source: 'native' as const,
          kind: specification.kind,
          id: `create-subject:${projectionId}`,
        }),
        title: specification.title.trim(),
        placement: buildTemporalCreatePlacement(specification),
        capabilities: capabilitiesForFields(specification),
      }),
    });

    return Object.freeze({
      status: 'ready',
      prepared: Object.freeze({ operationId, command, metadata }),
    });
  }

  private async currentProjection(
    projectionId: TemporalProjectionItem['id'],
  ): Promise<TemporalProjectionItem | null> {
    const result = await this.workspace.query({
      type: 'temporal.projection.get',
      id: projectionId,
    });
    return result.status === 'ok' ? result.item : null;
  }

  private mutationEffect(
    projectionId: TemporalProjectionItem['id'],
    metadata: TemporalCreateMetadata,
    result: Extract<TemporalOperationResult, { status: 'applied' }>,
  ): TemporalCreateMutationEffect | null {
    const undoToken = result.undoToken;
    if (!undoToken) {
      return null;
    }

    return Object.freeze({
      projection: result.item,
      metadata,
      undoToken,
      undo: async () => {
        const undoResult = await this.workspace.execute({
          type: 'temporal.operation.undo',
          operationId: this.ids.operationId(),
          source: 'manual',
          issuedAt: this.clock.now(),
          payload: Object.freeze({ undoToken }),
        });
        if (undoResult.status === 'applied') {
          if (undoResult.item) {
            this.records.set(
              projectionId,
              Object.freeze({ projection: undoResult.item, metadata }),
            );
          } else {
            this.records.delete(projectionId);
          }
        }
        return undoResult;
      },
    });
  }

  private async replacePlacement(
    projectionId: TemporalProjectionItem['id'],
    metadata: TemporalCreateMetadata,
    placement: TemporalPlacement | null,
  ): Promise<TemporalCreateMutationExecution> {
    const operationId = this.ids.operationId();
    const current = await this.currentProjection(projectionId);
    if (!current) {
      return Object.freeze({
        result: notFoundResult(operationId),
        effect: null,
      });
    }

    const result = await this.workspace.execute({
      type: 'temporal.placement.replace',
      operationId,
      source: 'manual',
      issuedAt: this.clock.now(),
      payload: Object.freeze({
        id: projectionId,
        expectedRevision: current.revision,
        placement,
      }),
    });

    if (result.status === 'applied' && result.item) {
      this.records.set(
        projectionId,
        Object.freeze({ projection: result.item, metadata }),
      );
      return Object.freeze({
        result,
        effect: this.mutationEffect(projectionId, metadata, result),
      });
    }

    return Object.freeze({ result, effect: null });
  }

  private async removeProjection(
    projectionId: TemporalProjectionItem['id'],
    metadata: TemporalCreateMetadata,
  ): Promise<TemporalCreateMutationExecution> {
    const operationId = this.ids.operationId();
    const current = await this.currentProjection(projectionId);
    if (!current) {
      return Object.freeze({
        result: notFoundResult(operationId),
        effect: null,
      });
    }

    const result = await this.workspace.execute({
      type: 'temporal.projection.remove',
      operationId,
      source: 'manual',
      issuedAt: this.clock.now(),
      payload: Object.freeze({
        id: projectionId,
        expectedRevision: current.revision,
      }),
    });

    if (result.status === 'applied') {
      this.records.delete(projectionId);
      return Object.freeze({
        result,
        effect: this.mutationEffect(projectionId, metadata, result),
      });
    }

    return Object.freeze({ result, effect: null });
  }

  public async execute(
    prepared: TemporalCreatePreparedOperation,
  ): Promise<TemporalCreateExecution> {
    if (
      this.canonicalActivityOnly &&
      (!isCanonicalLifeAreaRef(prepared.metadata.contextId) ||
        !canonicalActivityIntentSupported(prepared))
    ) {
      return Object.freeze({
        result: unavailableResult(
          prepared.operationId,
          'temporal.create.capability_not_available',
        ),
        effect: null,
      });
    }

    const richFingerprint = richIntentFingerprint(prepared.metadata);
    const previousFingerprint = this.richOperationFingerprints.get(
      prepared.operationId,
    );
    if (
      previousFingerprint !== undefined &&
      previousFingerprint !== richFingerprint
    ) {
      return Object.freeze({
        result: operationIdReuseResult(prepared.operationId),
        effect: null,
      });
    }
    if (previousFingerprint === undefined) {
      this.richOperationFingerprints.set(prepared.operationId, richFingerprint);
    }

    const result = this.workspace instanceof RemoteActivityTemporalWorkspace
      ? await this.workspace.execute(
          prepared.command,
          isCanonicalLifeAreaRef(prepared.metadata.contextId)
            ? prepared.metadata.contextId
            : undefined,
        )
      : await this.workspace.execute(prepared.command);
    if (result.status !== 'applied' || !result.item) {
      return Object.freeze({ result, effect: null });
    }

    const projection = result.item;
    const undoToken = result.undoToken ?? null;
    this.records.set(
      projection.id,
      Object.freeze({ projection, metadata: prepared.metadata }),
    );

    const effect = Object.freeze({
      projection,
      metadata: prepared.metadata,
      undoToken,
      undoAvailable: undoToken !== null,
      undo: async () => {
        if (undoToken === null) {
          return unavailableResult(
            this.ids.operationId(),
            'temporal.create.undo_unavailable',
          );
        }
        const undoResult = await this.workspace.execute({
          type: 'temporal.operation.undo',
          operationId: this.ids.operationId(),
          source: 'manual',
          issuedAt: this.clock.now(),
          payload: Object.freeze({ undoToken }),
        });
        if (undoResult.status === 'applied') {
          this.records.delete(projection.id);
        }
        return undoResult;
      },
      replacePlacement: (placement: TemporalPlacement | null) =>
        this.replacePlacement(projection.id, prepared.metadata, placement),
      remove: () => this.removeProjection(projection.id, prepared.metadata),
    }) satisfies TemporalCreateAppliedEffect;

    return Object.freeze({ result, effect });
  }

  public async placeExistingActivity(
    activityRef: string,
    placement: TemporalPlacement,
  ): Promise<TemporalOperationResult> {
    return await this.workspace.execute({
      type: 'temporal.placement.replace',
      operationId: this.ids.operationId(),
      source: 'manual',
      issuedAt: this.clock.now(),
      payload: Object.freeze({
        id: temporalProjectionId(activityRef),
        expectedRevision: 0,
        placement,
      }),
    });
  }

  public async list(): Promise<readonly TemporalProjectionItem[]> {
    const result = await this.workspace.query({
      type: 'temporal.projection.list',
    });
    return result.snapshot.items;
  }

  public async listRecords(): Promise<readonly TemporalCreateRecord[]> {
    const projections = await this.list();
    return Object.freeze(
      projections.flatMap((projection) => {
        const record = this.records.get(projection.id);
        return record ? [record] : [];
      }),
    );
  }
}

export type TemporalCreateRuntimeOptions = Readonly<{
  clock?: TemporalClock;
  ids?: TemporalIdFactory;
  workspace?: TemporalWorkspacePort;
  activityDataSource?: TemporalActivityDataSource;
  mode?: string;
}>;

export function createLocalTemporalCreateRuntime(
  options: TemporalCreateRuntimeOptions = {},
): TemporalCreateRuntime {
  const ids = options.ids ?? systemTemporalIdFactory;
  const mode = options.mode ?? import.meta.env.MODE;
  if (options.workspace) {
    return new LocalTemporalCreateRuntime(
      options.workspace,
      ids,
      options.clock ?? systemTemporalClock,
    );
  }
  if (mode === 'test') {
    return new LocalTemporalCreateRuntime(
      new InMemoryTemporalWorkspace(ids),
      ids,
      options.clock ?? systemTemporalClock,
    );
  }

  const activitySource =
    options.activityDataSource ?? createRemoteTemporalActivityDataSource();
  return new LocalTemporalCreateRuntime(
    new RemoteActivityTemporalWorkspace(activitySource),
    ids,
    options.clock ?? systemTemporalClock,
    true,
  );
}

export function temporalCreateRevealDate(
  effect: TemporalCreateAppliedEffect,
): PlainDate | null {
  const placement = effect.projection.placement;
  if (!placement) {
    return null;
  }
  switch (placement.kind) {
    case 'date-span':
      return placement.startDate;
    case 'floating-local':
      return placement.start.toPlainDate();
    case 'zoned':
      return placement.start.toPlainDate();
    case 'absolute':
      return placement.start
        .toZonedDateTimeISO(effect.metadata.timeZoneId)
        .toPlainDate();
    case 'coarse-local-period':
      return placement.localDate;
  }
}
