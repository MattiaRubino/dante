import type { Instant, PlainDateTime } from '@dante/time';

export type TemporalActivityRecord = Readonly<{
  activityRef: string;
  title: string;
  createdAt: Instant;
}>;

export type TemporalActivityCreateRequest = Readonly<{
  operationId: string;
  title: string;
}>;

export type TemporalActivityCreateResult = Readonly<{
  activity: TemporalActivityRecord;
  replayed: boolean;
}>;

export type TemporalFloatingLocalScheduleRecord = Readonly<{
  scheduleRef: string;
  placementMaterialStateRef: string;
  temporalForm: 'floating-local';
  startsLocalAt: PlainDateTime;
  endsLocalAt: PlainDateTime;
}>;

export type TemporalScheduledActivityCreateRequest = Readonly<{
  operationId: string;
  title: string;
  placement: Readonly<{
    kind: 'floating-local-interval';
    startsLocalAt: PlainDateTime;
    endsLocalAt: PlainDateTime;
  }>;
}>;

export type TemporalScheduledActivityCreateResult = Readonly<{
  activity: TemporalActivityRecord;
  schedule: TemporalFloatingLocalScheduleRecord;
  replayed: boolean;
}>;

export interface TemporalActivityDataSource {
  createActivity(
    request: TemporalActivityCreateRequest,
    signal?: AbortSignal,
  ): Promise<TemporalActivityCreateResult>;
  createScheduledActivity(
    request: TemporalScheduledActivityCreateRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduledActivityCreateResult>;
  loadUnplaced(
    signal?: AbortSignal,
  ): Promise<readonly TemporalActivityRecord[]>;
}
