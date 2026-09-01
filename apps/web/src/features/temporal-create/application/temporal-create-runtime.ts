import type { PlainDate } from '@dante/time';

import {
  InMemoryTemporalWorkspace,
  systemTemporalClock,
  systemTemporalIdFactory,
  temporalValidationIssue,
  type TemporalClock,
  type TemporalIdFactory,
  type TemporalOperationId,
  type TemporalOperationResult,
  type TemporalProjectionItem,
  type TemporalUndoToken,
  type TemporalValidationIssue,
  type TemporalWorkspacePort,
} from '../../temporal';
import {
  buildTemporalCreatePlacement,
  validateTemporalCreateFields,
  type TemporalCreateFields,
  type TemporalCreateKind,
  type TemporalCreateTimeSemantics,
} from '../model/temporal-create-session';

export type TemporalCreateMetadata = Readonly<{
  kind: TemporalCreateKind;
  contextId: string;
  notes: string;
  timeSemantics: TemporalCreateTimeSemantics;
  timeZoneId: string;
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

export type TemporalCreateAppliedEffect = Readonly<{
  projection: TemporalProjectionItem;
  metadata: TemporalCreateMetadata;
  undoToken: TemporalUndoToken;
  undo: () => Promise<TemporalOperationResult>;
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
  execute(prepared: TemporalCreatePreparedOperation): Promise<TemporalCreateExecution>;
  list(): Promise<readonly TemporalProjectionItem[]>;
  listRecords(): Promise<readonly TemporalCreateRecord[]>;
}

function capabilitiesForFields(
  fields: TemporalCreateFields,
): TemporalCreatePreparedOperation['command']['payload']['capabilities'] {
  const capabilities: TemporalCreatePreparedOperation['command']['payload']['capabilities'][number][] = [
    'placement',
    'confirmation',
    'history',
    'notes',
  ];
  if (fields.kind === 'event' && fields.eventRecurrence.patternKind !== 'none') {
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
  ) {
    this.clock = clock;
  }

  public prepare(
    fields: TemporalCreateFields,
    operationId = this.ids.operationId(),
  ): TemporalCreatePreparation {
    const issues = validateTemporalCreateFields(fields);
    if (issues.length > 0) {
      return Object.freeze({ status: 'invalid', issues });
    }

    const projectionId = this.ids.projectionId();
    const metadata = Object.freeze({
      kind: fields.kind,
      contextId: fields.contextId,
      notes: fields.notes.trim(),
      timeSemantics: fields.timeSemantics,
      timeZoneId: fields.timeZoneId,
      specification: fields,
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
          kind: fields.kind,
          // Frontend-only provisional subject identity. A future backend adapter
          // owns canonical identity and can reconcile it without changing the
          // Create UI/application contract.
          id: `create-subject:${projectionId}`,
        }),
        title: fields.title.trim(),
        placement: buildTemporalCreatePlacement(fields),
        capabilities: capabilitiesForFields(fields),
      }),
    });

    return Object.freeze({
      status: 'ready',
      prepared: Object.freeze({ operationId, command, metadata }),
    });
  }

  public async execute(
    prepared: TemporalCreatePreparedOperation,
  ): Promise<TemporalCreateExecution> {
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

    const result = await this.workspace.execute(prepared.command);
    if (result.status !== 'applied' || !result.item || !result.undoToken) {
      return Object.freeze({ result, effect: null });
    }

    const projection = result.item;
    const undoToken = result.undoToken;
    this.records.set(
      projection.id,
      Object.freeze({ projection, metadata: prepared.metadata }),
    );

    const effect = Object.freeze({
      projection,
      metadata: prepared.metadata,
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
          this.records.delete(projection.id);
        }
        return undoResult;
      },
    }) satisfies TemporalCreateAppliedEffect;

    return Object.freeze({ result, effect });
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
}>;

export function createLocalTemporalCreateRuntime(
  options: TemporalCreateRuntimeOptions = {},
): TemporalCreateRuntime {
  const ids = options.ids ?? systemTemporalIdFactory;
  const workspace = options.workspace ?? new InMemoryTemporalWorkspace(ids);
  return new LocalTemporalCreateRuntime(
    workspace,
    ids,
    options.clock ?? systemTemporalClock,
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
  }
}
