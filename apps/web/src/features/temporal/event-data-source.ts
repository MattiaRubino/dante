import type { Instant } from '@dante/time';

import type {
  TemporalAcceptedSchedulePlacement,
  TemporalSchedulePlacementInput,
} from './schedule-data-source';

export type TemporalEventRecord = Readonly<{
  eventRef: string;
  title: string;
  agendaParts: readonly string[];
  createdAt: Instant;
}>;

export type TemporalEventDetailRecord = Readonly<{
  eventRef: string;
  title: string;
  agendaRevision: number;
  agendaParts: readonly string[];
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
  lifeAreaRef?: string;
  agendaParts: readonly string[];
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalScheduledEventCreateResult = Readonly<{
  event: TemporalEventRecord;
  schedule: TemporalEventScheduleRecord;
  replayed: boolean;
}>;

/** A real Event whose Schedule has been explicitly withdrawn. */
export type TemporalPostponedEventRecord = Readonly<{
  eventRef: string;
  scheduleRef: string;
  title: string;
  createdAt: Instant;
  lifeAreaRef: string | null;
  lifeAreaAssignmentRevision: number | null;
  unscheduleOperationId: string;
}>;

export type TemporalPostponedEventReplanRequest = Readonly<{
  eventRef: string;
  scheduleRef: string;
  unscheduleOperationId: string;
  operationId: string;
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalEventAgendaReplaceRequest = Readonly<{
  eventRef: string;
  operationId: string;
  expectedRevision: number;
  agendaParts: readonly string[];
}>;

export type TemporalEventAgendaReplaceResult = Readonly<{
  eventRef: string;
  agendaRevision: number;
  agendaParts: readonly string[];
  replayed: boolean;
}>;

export interface TemporalEventDataSource {
  createScheduledEvent(
    request: TemporalScheduledEventCreateRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduledEventCreateResult>;
  listPostponedEvents(
    signal?: AbortSignal,
  ): Promise<readonly TemporalPostponedEventRecord[]>;
  replanPostponedEvent(
    request: TemporalPostponedEventReplanRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduledEventCreateResult>;
}

export interface TemporalEventAgendaDataSource {
  loadEvent(
    eventRef: string,
    signal?: AbortSignal,
  ): Promise<TemporalEventDetailRecord>;
  replaceAgenda(
    request: TemporalEventAgendaReplaceRequest,
    signal?: AbortSignal,
  ): Promise<TemporalEventAgendaReplaceResult>;
}
