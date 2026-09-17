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
  agendaParts: readonly string[];
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalScheduledEventCreateResult = Readonly<{
  event: TemporalEventRecord;
  schedule: TemporalEventScheduleRecord;
  replayed: boolean;
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
}

export interface TemporalEventAgendaDataSource {
  loadEvent(eventRef: string, signal?: AbortSignal): Promise<TemporalEventDetailRecord>;
  replaceAgenda(
    request: TemporalEventAgendaReplaceRequest,
    signal?: AbortSignal,
  ): Promise<TemporalEventAgendaReplaceResult>;
}
