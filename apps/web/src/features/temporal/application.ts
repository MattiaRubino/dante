import type { Instant } from '@dante/time';

import type {
  TemporalCapability,
  TemporalOperationId,
  TemporalPlacement,
  TemporalProjectionId,
  TemporalProjectionItem,
  TemporalSubjectRef,
  TemporalUndoToken,
  TemporalValidationIssue,
  TemporalWorkspaceSnapshot,
} from './model';

/* Commands ---------------------------------------------------------------- */

export type TemporalCommandSource =
  'manual' | 'keyboard' | 'ai' | 'voice' | 'integration' | 'system';

type CommandEnvelope = Readonly<{
  operationId: TemporalOperationId;
  source: TemporalCommandSource;
  issuedAt: Instant;
}>;

export type TemporalCommand =
  | (CommandEnvelope &
      Readonly<{
        type: 'temporal.projection.create';
        payload: Readonly<{
          id: TemporalProjectionId;
          subject: TemporalSubjectRef;
          title: string;
          placement: TemporalPlacement | null;
          capabilities: readonly TemporalCapability[];
        }>;
      }>)
  | (CommandEnvelope &
      Readonly<{
        type: 'temporal.placement.replace';
        payload: Readonly<{
          id: TemporalProjectionId;
          expectedRevision: number;
          placement: TemporalPlacement | null;
        }>;
      }>)
  | (CommandEnvelope &
      Readonly<{
        type: 'temporal.projection.remove';
        payload: Readonly<{
          id: TemporalProjectionId;
          expectedRevision: number;
        }>;
      }>)
  | (CommandEnvelope &
      Readonly<{
        type: 'temporal.operation.undo';
        payload: Readonly<{
          undoToken: TemporalUndoToken;
        }>;
      }>);

/* Results ----------------------------------------------------------------- */

export type TemporalReconciliation =
  | Readonly<{ status: 'confirmed' }>
  | Readonly<{
      status: 'adjusted';
      item: TemporalProjectionItem | null;
      reasonCode: string;
    }>
  | Readonly<{
      status: 'conflict';
      reasonCode: string;
    }>;

export type TemporalOperationResult =
  | Readonly<{
      operationId: TemporalOperationId;
      status: 'applied';
      item: TemporalProjectionItem | null;
      snapshotRevision: number;
      undoToken?: TemporalUndoToken;
      reconciliation: TemporalReconciliation;
    }>
  | Readonly<{
      operationId: TemporalOperationId;
      status: 'no-op';
      item: TemporalProjectionItem | null;
      snapshotRevision: number;
    }>
  | Readonly<{
      operationId: TemporalOperationId;
      status: 'rejected';
      code:
        | 'validation'
        | 'already-exists'
        | 'not-found'
        | 'revision-conflict'
        | 'operation-id-reused'
        | 'undo-not-found'
        | 'undo-consumed'
        | 'undo-conflict';
      issues: readonly TemporalValidationIssue[];
      currentRevision?: number;
    }>
  | Readonly<{
      operationId: TemporalOperationId;
      status: 'failed';
      failure: Readonly<{
        kind: 'transport' | 'unavailable' | 'unknown';
        code: string;
        retryable: boolean;
      }>;
    }>;

export type TemporalOperationLifecycle =
  | Readonly<{ state: 'idle' }>
  | Readonly<{
      state: 'pending';
      operationId: TemporalOperationId;
    }>
  | Readonly<{
      state: 'settled';
      result: TemporalOperationResult;
    }>;

/* Queries ----------------------------------------------------------------- */

export type GetTemporalProjectionQuery = Readonly<{
  type: 'temporal.projection.get';
  id: TemporalProjectionId;
}>;

export type ListTemporalProjectionsQuery = Readonly<{
  type: 'temporal.projection.list';
}>;

export type TemporalQuery =
  GetTemporalProjectionQuery | ListTemporalProjectionsQuery;

export type GetTemporalProjectionResult =
  | Readonly<{
      type: 'temporal.projection.get';
      status: 'ok';
      item: TemporalProjectionItem;
    }>
  | Readonly<{
      type: 'temporal.projection.get';
      status: 'not-found';
    }>;

export type ListTemporalProjectionsResult = Readonly<{
  type: 'temporal.projection.list';
  status: 'ok';
  snapshot: TemporalWorkspaceSnapshot;
}>;

export type TemporalQueryResult =
  GetTemporalProjectionResult | ListTemporalProjectionsResult;

/* Port -------------------------------------------------------------------- */

export type TemporalWorkspaceListener = () => void;

export interface TemporalWorkspacePort {
  execute(command: TemporalCommand): Promise<TemporalOperationResult>;
  query(
    query: GetTemporalProjectionQuery,
  ): Promise<GetTemporalProjectionResult>;
  query(
    query: ListTemporalProjectionsQuery,
  ): Promise<ListTemporalProjectionsResult>;
  subscribe(listener: TemporalWorkspaceListener): () => void;
}
