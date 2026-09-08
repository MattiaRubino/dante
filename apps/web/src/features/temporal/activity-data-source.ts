import type { Instant } from '@dante/time';

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

export interface TemporalActivityDataSource {
  createActivity(
    request: TemporalActivityCreateRequest,
    signal?: AbortSignal,
  ): Promise<TemporalActivityCreateResult>;
  loadUnplaced(
    signal?: AbortSignal,
  ): Promise<readonly TemporalActivityRecord[]>;
}
