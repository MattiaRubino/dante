import type { Instant } from '@dante/time';

import type {
  TemporalAcceptedSchedulePlacement,
  TemporalSchedulePlacementInput,
} from './schedule-data-source';

export type TemporalEventRecord = Readonly<{
  eventRef: string;
  title: string;
  createdAt: Instant;
}>;

export type TemporalEventScheduleRecord = Readonly<{
  scheduleRef: string;
  placementMaterialStateRef: string;
  placement: TemporalAcceptedSchedulePlacement;
}>;

export type TemporalScheduledEventCreateRequest = Readonly<{
  operationId: string;
  title: string;
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalScheduledEventCreateResult = Readonly<{
  event: TemporalEventRecord;
  schedule: TemporalEventScheduleRecord;
  replayed: boolean;
}>;

export interface TemporalEventDataSource {
  createScheduledEvent(
    request: TemporalScheduledEventCreateRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduledEventCreateResult>;
}
