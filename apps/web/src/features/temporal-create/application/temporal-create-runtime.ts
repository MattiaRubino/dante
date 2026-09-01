import type { PlainDate } from '@dante/time';

import {
  InMemoryTemporalWorkspace,
  systemTemporalClock,
  systemTemporalIdFactory,
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
}

function capabilitiesForKind(
  kind: TemporalCreateKind,
): TemporalCreatePreparedOperation['command']['payload']['capabilities'] {
  return kind === 'activity'
    ? Object.freeze([
        'placement',
        'execution',
        'actual',
        'confirmation',
        'replanning',
        'history',
        'notes',
      ] as const)
    : Object.freeze([
        'placement',
        'confirmation',
        'history',
        'notes',
      ] as const);
}

class LocalTemporalCreateRuntime implements TemporalCreateRuntime {
  public readonly clock: TemporalClock;

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
          // Frontend-only provisional subject identity. The future backend owns
          // canonical domain identity and may reconcile it without changing the
          // Create form contract.
          id: `create-subject:${projectionId}`,
        }),
        title: fields.title,
        placement: buildTemporalCreatePlacement(fields),
        capabilities: capabilitiesForKind(fields.kind),
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
    const result = await this.workspace.execute(prepared.command);
    if (
      result.status !== 'applied' ||
      !result.item ||
      !result.undoToken
    ) {
      return Object.freeze({ result, effect: null });
    }

    const projection = result.item;
    const undoToken = result.undoToken;
    const effect = Object.freeze({
      projection,
      metadata: prepared.metadata,
      undoToken,
      undo: () =>
        this.workspace.execute({
          type: 'temporal.operation.undo',
          operationId: this.ids.operationId(),
          source: 'manual',
          issuedAt: this.clock.now(),
          payload: Object.freeze({ undoToken }),
        }),
    }) satisfies TemporalCreateAppliedEffect;

    return Object.freeze({ result, effect });
  }

  public async list(): Promise<readonly TemporalProjectionItem[]> {
    const result = await this.workspace.query({
      type: 'temporal.projection.list',
    });
    return result.snapshot.items;
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
