import type { PlainDateTime } from '@dante/time';

export type TemporalScheduleRevisionRequest = Readonly<{
  operationId: string;
  scheduleRef: string;
  expectedPlacementMaterialStateRef: string;
  placement: Readonly<{
    kind: 'floating-local-interval';
    startsLocalAt: PlainDateTime;
    endsLocalAt: PlainDateTime;
  }>;
}>;

export type TemporalScheduleRevisionResult = Readonly<{
  scheduleRef: string;
  previousPlacementMaterialStateRef: string;
  placementMaterialStateRef: string;
  placement: Readonly<{
    kind: 'floating-local-interval';
    startsLocalAt: PlainDateTime;
    endsLocalAt: PlainDateTime;
  }>;
  replayed: boolean;
}>;

export type TemporalScheduleUnscheduleRequest = Readonly<{
  operationId: string;
  scheduleRef: string;
  expectedPlacementMaterialStateRef: string;
}>;

export type TemporalScheduleUnscheduleResult = Readonly<{
  scheduleRef: string;
  previousPlacementMaterialStateRef: string;
  unscheduleOperationId: string;
  replayed: boolean;
}>;

export type TemporalScheduleUnscheduleUndoRequest = Readonly<{
  operationId: string;
  scheduleRef: string;
  unscheduleOperationId: string;
}>;

export type TemporalScheduleUnscheduleUndoResult = Readonly<{
  scheduleRef: string;
  restoredFromPlacementMaterialStateRef: string;
  placementMaterialStateRef: string;
  placement: Readonly<{
    kind: 'floating-local-interval';
    startsLocalAt: PlainDateTime;
    endsLocalAt: PlainDateTime;
  }>;
  replayed: boolean;
}>;

export interface TemporalScheduleDataSource {
  reviseSchedule(
    request: TemporalScheduleRevisionRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduleRevisionResult>;

  unscheduleSchedule(
    request: TemporalScheduleUnscheduleRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduleUnscheduleResult>;

  undoScheduleUnschedule(
    request: TemporalScheduleUnscheduleUndoRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduleUnscheduleUndoResult>;
}
