import type { Instant } from '@dante/time';

import type {
  TemporalAcceptedSchedulePlacement,
  TemporalSchedulePlacementInput,
} from './schedule-data-source';

export type TemporalAuthoringLifeAreaInput = Readonly<{
  lifeAreaRef?: string;
  newName?: string;
  expectedRevision?: number;
  colorCode?: string;
}>;

export type TemporalAuthoringBaseRequest = Readonly<{
  operationId: string;
  title: string;
  description?: string;
  location?: string;
  itemColorCode?: string;
  lifeArea?: TemporalAuthoringLifeAreaInput;
  placement?: TemporalSchedulePlacementInput;
}>;

export type TemporalAuthorActivityRequest = TemporalAuthoringBaseRequest;

export type TemporalAuthorEventRequest = TemporalAuthoringBaseRequest &
  Readonly<{
    agendaParts: readonly string[];
  }>;

export type TemporalAuthoringItem = Readonly<{
  subjectRef: string;
  title: string;
  createdAt: Instant;
  description: string | null;
  location: string | null;
  colorCode: string | null;
  lifeAreaRef: string | null;
  lifeAreaAssignmentRevision: number | null;
  lifeAreaColorCode: string | null;
  lifeAreaRevision: number | null;
}>;

export type TemporalAuthoringSchedule = Readonly<{
  scheduleRef: string;
  placementMaterialStateRef: string;
  placement: TemporalAcceptedSchedulePlacement;
}>;

export type TemporalAuthoredActivityResult = Readonly<{
  item: TemporalAuthoringItem;
  schedule: TemporalAuthoringSchedule | null;
  replayed: boolean;
}>;

export type TemporalAuthoredEventResult = TemporalAuthoredActivityResult &
  Readonly<{
    agendaRevision: number;
    agendaParts: readonly string[];
  }>;

export interface TemporalAuthoringDataSource {
  authorActivity(
    request: TemporalAuthorActivityRequest,
    signal?: AbortSignal,
  ): Promise<TemporalAuthoredActivityResult>;
  authorEvent(
    request: TemporalAuthorEventRequest,
    signal?: AbortSignal,
  ): Promise<TemporalAuthoredEventResult>;
}
