import type { Instant } from '@dante/time';

import type {
  GetTemporalProjectionQuery,
  GetTemporalProjectionResult,
  ListTemporalProjectionsQuery,
  ListTemporalProjectionsResult,
  TemporalCommand,
  TemporalOperationResult,
  TemporalQuery,
  TemporalQueryResult,
  TemporalWorkspaceListener,
  TemporalWorkspacePort,
} from './application';
import {
  freezeTemporalProjectionItem,
  normalizeTemporalCapabilities,
  serializeTemporalPlacement,
  sortTemporalValidationIssues,
  temporalPlacementEquals,
  temporalValidationIssue,
  validateTemporalPlacement,
  type TemporalIdFactory,
  type TemporalOperationId,
  type TemporalProjectionId,
  type TemporalProjectionItem,
  type TemporalUndoToken,
  type TemporalValidationIssue,
  type TemporalWorkspaceSnapshot,
} from './model';

type StoredOperation = Readonly<{
  fingerprint: string;
  result: TemporalOperationResult;
}>;

type UndoRecord = {
  itemId: TemporalProjectionId;
  before: TemporalProjectionItem | null;
  expectedAfterRevision: number | null;
  consumed: boolean;
};

type RejectionCode = Extract<
  TemporalOperationResult,
  { status: 'rejected' }
>['code'];

function temporalCommandFingerprint(command: TemporalCommand): string {
  const envelope = {
    type: command.type,
    source: command.source,
    issuedAt: command.issuedAt.toString(),
  };

  switch (command.type) {
    case 'temporal.projection.create':
      return JSON.stringify({
        ...envelope,
        payload: {
          id: command.payload.id,
          subject: command.payload.subject,
          title: command.payload.title,
          placement: command.payload.placement
            ? serializeTemporalPlacement(command.payload.placement)
            : null,
          capabilities: [...command.payload.capabilities],
        },
      });
    case 'temporal.placement.replace':
      return JSON.stringify({
        ...envelope,
        payload: {
          id: command.payload.id,
          expectedRevision: command.payload.expectedRevision,
          placement: command.payload.placement
            ? serializeTemporalPlacement(command.payload.placement)
            : null,
        },
      });
    case 'temporal.projection.remove':
      return JSON.stringify({
        ...envelope,
        payload: command.payload,
      });
    case 'temporal.operation.undo':
      return JSON.stringify({
        ...envelope,
        payload: command.payload,
      });
  }
}

export class InMemoryTemporalWorkspace implements TemporalWorkspacePort {
  private readonly items = new Map<
    TemporalProjectionId,
    TemporalProjectionItem
  >();

  private readonly operations = new Map<TemporalOperationId, StoredOperation>();
  private readonly undoRecords = new Map<TemporalUndoToken, UndoRecord>();
  private readonly listeners = new Set<TemporalWorkspaceListener>();
  private snapshotRevision = 0;

  public constructor(private readonly ids: TemporalIdFactory) {}

  public execute(command: TemporalCommand): Promise<TemporalOperationResult> {
    const fingerprint = temporalCommandFingerprint(command);
    const previous = this.operations.get(command.operationId);

    if (previous) {
      return Promise.resolve(
        previous.fingerprint === fingerprint
          ? previous.result
          : this.rejected(command.operationId, 'operation-id-reused', [
              temporalValidationIssue('temporal.operation.id_reused', [
                'operationId',
              ]),
            ]),
      );
    }

    const result = this.executeOnce(command);
    this.operations.set(command.operationId, {
      fingerprint,
      result,
    });
    return Promise.resolve(result);
  }

  public query(
    query: GetTemporalProjectionQuery,
  ): Promise<GetTemporalProjectionResult>;
  public query(
    query: ListTemporalProjectionsQuery,
  ): Promise<ListTemporalProjectionsResult>;
  public query(query: TemporalQuery): Promise<TemporalQueryResult> {
    if (query.type === 'temporal.projection.get') {
      const item = this.items.get(query.id);
      return Promise.resolve(
        item
          ? Object.freeze({
              type: query.type,
              status: 'ok' as const,
              item,
            })
          : Object.freeze({
              type: query.type,
              status: 'not-found' as const,
            }),
      );
    }

    return Promise.resolve(
      Object.freeze({
        type: query.type,
        status: 'ok' as const,
        snapshot: this.snapshot(),
      }),
    );
  }

  public subscribe(listener: TemporalWorkspaceListener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private executeOnce(command: TemporalCommand): TemporalOperationResult {
    switch (command.type) {
      case 'temporal.projection.create':
        return this.create(command);
      case 'temporal.placement.replace':
        return this.replacePlacement(command);
      case 'temporal.projection.remove':
        return this.remove(command);
      case 'temporal.operation.undo':
        return this.undo(command);
    }
  }

  private create(
    command: Extract<TemporalCommand, { type: 'temporal.projection.create' }>,
  ): TemporalOperationResult {
    if (this.items.has(command.payload.id)) {
      return this.rejected(command.operationId, 'already-exists', [
        temporalValidationIssue('temporal.projection.already_exists', [
          'payload',
          'id',
        ]),
      ]);
    }

    const issues = this.validateCreate(command);
    if (issues.length > 0) {
      return this.rejected(command.operationId, 'validation', issues);
    }

    const item = freezeTemporalProjectionItem({
      id: command.payload.id,
      subject: command.payload.subject,
      title: command.payload.title.trim(),
      placement: command.payload.placement,
      capabilities: normalizeTemporalCapabilities(command.payload.capabilities),
      revision: 1,
      createdAt: command.issuedAt,
      updatedAt: command.issuedAt,
      lastOperationId: command.operationId,
    });

    this.items.set(item.id, item);
    const undoToken = this.registerUndo(item.id, null, item.revision);
    this.commitMutation();
    return this.applied(command.operationId, item, undoToken);
  }

  private replacePlacement(
    command: Extract<TemporalCommand, { type: 'temporal.placement.replace' }>,
  ): TemporalOperationResult {
    const current = this.items.get(command.payload.id);
    if (!current) {
      return this.notFound(command.operationId);
    }

    if (current.revision !== command.payload.expectedRevision) {
      return this.revisionConflict(
        command.operationId,
        command.payload.expectedRevision,
        current.revision,
      );
    }

    if (command.payload.placement) {
      const validation = validateTemporalPlacement(command.payload.placement);
      if (!validation.valid) {
        return this.rejected(
          command.operationId,
          'validation',
          validation.issues,
        );
      }
    }

    const same =
      current.placement === null
        ? command.payload.placement === null
        : command.payload.placement !== null &&
          temporalPlacementEquals(current.placement, command.payload.placement);

    if (same) {
      return Object.freeze({
        operationId: command.operationId,
        status: 'no-op' as const,
        item: current,
        snapshotRevision: this.snapshotRevision,
      });
    }

    const next = this.nextRevision(
      current,
      command.payload.placement,
      command.issuedAt,
      command.operationId,
    );
    this.items.set(next.id, next);
    const undoToken = this.registerUndo(next.id, current, next.revision);
    this.commitMutation();
    return this.applied(command.operationId, next, undoToken);
  }

  private remove(
    command: Extract<TemporalCommand, { type: 'temporal.projection.remove' }>,
  ): TemporalOperationResult {
    const current = this.items.get(command.payload.id);
    if (!current) {
      return this.notFound(command.operationId);
    }

    if (current.revision !== command.payload.expectedRevision) {
      return this.revisionConflict(
        command.operationId,
        command.payload.expectedRevision,
        current.revision,
      );
    }

    this.items.delete(current.id);
    const undoToken = this.registerUndo(current.id, current, null);
    this.commitMutation();
    return this.applied(command.operationId, null, undoToken);
  }

  private undo(
    command: Extract<TemporalCommand, { type: 'temporal.operation.undo' }>,
  ): TemporalOperationResult {
    const record = this.undoRecords.get(command.payload.undoToken);

    if (!record) {
      return this.rejected(command.operationId, 'undo-not-found', [
        temporalValidationIssue('temporal.undo.not_found', [
          'payload',
          'undoToken',
        ]),
      ]);
    }

    if (record.consumed) {
      return this.rejected(command.operationId, 'undo-consumed', [
        temporalValidationIssue('temporal.undo.consumed', [
          'payload',
          'undoToken',
        ]),
      ]);
    }

    const current = this.items.get(record.itemId) ?? null;
    const matches =
      record.expectedAfterRevision === null
        ? current === null
        : current?.revision === record.expectedAfterRevision;

    if (!matches) {
      return this.rejected(
        command.operationId,
        'undo-conflict',
        [
          temporalValidationIssue('temporal.undo.conflict', [
            'payload',
            'undoToken',
          ]),
        ],
        current?.revision,
      );
    }

    let restored: TemporalProjectionItem | null = null;
    if (record.before === null) {
      this.items.delete(record.itemId);
    } else {
      restored = freezeTemporalProjectionItem({
        ...record.before,
        revision: (current?.revision ?? record.before.revision) + 1,
        updatedAt: command.issuedAt,
        lastOperationId: command.operationId,
      });
      this.items.set(restored.id, restored);
    }

    record.consumed = true;
    this.commitMutation();
    return this.applied(command.operationId, restored);
  }

  private validateCreate(
    command: Extract<TemporalCommand, { type: 'temporal.projection.create' }>,
  ): readonly TemporalValidationIssue[] {
    const issues: TemporalValidationIssue[] = [];

    if (!command.payload.title.trim()) {
      issues.push(
        temporalValidationIssue('temporal.projection.title.required', [
          'payload',
          'title',
        ]),
      );
    }
    if (!command.payload.subject.kind.trim()) {
      issues.push(
        temporalValidationIssue('temporal.projection.subject_kind.required', [
          'payload',
          'subject',
          'kind',
        ]),
      );
    }
    if (!command.payload.subject.id.trim()) {
      issues.push(
        temporalValidationIssue('temporal.projection.subject_id.required', [
          'payload',
          'subject',
          'id',
        ]),
      );
    }
    if (
      command.payload.subject.source === 'external' &&
      !command.payload.subject.provider.trim()
    ) {
      issues.push(
        temporalValidationIssue('temporal.projection.provider.required', [
          'payload',
          'subject',
          'provider',
        ]),
      );
    }
    if (command.payload.placement) {
      const validation = validateTemporalPlacement(command.payload.placement);
      if (!validation.valid) {
        issues.push(...validation.issues);
      }
    }

    return sortTemporalValidationIssues(issues);
  }

  private nextRevision(
    current: TemporalProjectionItem,
    placement: TemporalProjectionItem['placement'],
    updatedAt: Instant,
    operationId: TemporalOperationId,
  ): TemporalProjectionItem {
    return freezeTemporalProjectionItem({
      ...current,
      placement,
      revision: current.revision + 1,
      updatedAt,
      lastOperationId: operationId,
    });
  }

  private registerUndo(
    itemId: TemporalProjectionId,
    before: TemporalProjectionItem | null,
    expectedAfterRevision: number | null,
  ): TemporalUndoToken {
    const token = this.ids.undoToken();
    this.undoRecords.set(token, {
      itemId,
      before,
      expectedAfterRevision,
      consumed: false,
    });
    return token;
  }

  private applied(
    operationId: TemporalOperationId,
    item: TemporalProjectionItem | null,
    undoToken?: TemporalUndoToken,
  ): TemporalOperationResult {
    return Object.freeze({
      operationId,
      status: 'applied' as const,
      item,
      snapshotRevision: this.snapshotRevision,
      ...(undoToken ? { undoToken } : {}),
      reconciliation: Object.freeze({
        status: 'confirmed' as const,
      }),
    });
  }

  private rejected(
    operationId: TemporalOperationId,
    code: RejectionCode,
    issues: readonly TemporalValidationIssue[],
    currentRevision?: number,
  ): TemporalOperationResult {
    return Object.freeze({
      operationId,
      status: 'rejected' as const,
      code,
      issues: sortTemporalValidationIssues(issues),
      ...(currentRevision === undefined ? {} : { currentRevision }),
    });
  }

  private notFound(operationId: TemporalOperationId): TemporalOperationResult {
    return this.rejected(operationId, 'not-found', [
      temporalValidationIssue('temporal.projection.not_found', [
        'payload',
        'id',
      ]),
    ]);
  }

  private revisionConflict(
    operationId: TemporalOperationId,
    expected: number,
    actual: number,
  ): TemporalOperationResult {
    return this.rejected(
      operationId,
      'revision-conflict',
      [
        temporalValidationIssue(
          'temporal.projection.revision_conflict',
          ['payload', 'expectedRevision'],
          'error',
          { expected, actual },
        ),
      ],
      actual,
    );
  }

  private snapshot(): TemporalWorkspaceSnapshot {
    return Object.freeze({
      revision: this.snapshotRevision,
      items: Object.freeze(
        [...this.items.values()].sort((left, right) =>
          left.id.localeCompare(right.id),
        ),
      ),
    });
  }

  private commitMutation(): void {
    this.snapshotRevision += 1;
    for (const listener of [...this.listeners]) {
      try {
        listener();
      } catch {
        // A projection subscriber cannot roll back an already committed
        // application mutation. Consumers own their rendering failures.
      }
    }
  }
}
