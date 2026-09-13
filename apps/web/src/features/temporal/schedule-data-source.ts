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

export interface TemporalScheduleDataSource {
  reviseSchedule(
    request: TemporalScheduleRevisionRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduleRevisionResult>;
}
