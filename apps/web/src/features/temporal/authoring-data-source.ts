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

export type TemporalAuthorActivityChildRequest = Readonly<{
  title: string;
  description?: string;
  requirementCode?: 'required' | 'optional';
  presentationOrder?: number;
  placement?: TemporalSchedulePlacementInput;
  plannedSlices?: readonly TemporalSchedulePlacementInput[];
  sessionCaptureMode?: TemporalSessionCaptureMode;
}>;

export type TemporalSessionCaptureMode =
  'disabled' | 'record' | 'live' | 'record_and_live';

export type TemporalAuthorActivityRequest = TemporalAuthoringBaseRequest &
  Readonly<{
    sessionCaptureMode?: TemporalSessionCaptureMode;
    plannedSlices?: readonly TemporalSchedulePlacementInput[];
    children?: readonly TemporalAuthorActivityChildRequest[];
  }>;

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

type TemporalAuthoredItemResult = Readonly<{
  item: TemporalAuthoringItem;
  schedule: TemporalAuthoringSchedule | null;
  replayed: boolean;
}>;

export type TemporalAuthoredActivityChild = Readonly<{
  activityRef: string;
  title: string;
  decompositionRef: string;
  decompositionStateRef: string;
  requirementCode: 'required' | 'optional';
  presentationOrder: number;
  schedule: TemporalAuthoringSchedule | null;
  plannedSlices: readonly TemporalAuthoringSchedule[];
  sessionCaptureMode: TemporalSessionCaptureMode;
}>;

export type TemporalAuthoredActivityResult = TemporalAuthoredItemResult &
  Readonly<{
    sessionCaptureMode: TemporalSessionCaptureMode;
    plannedSlices: readonly TemporalAuthoringSchedule[];
    children: readonly TemporalAuthoredActivityChild[];
  }>;

export type TemporalAuthoredEventResult = TemporalAuthoredItemResult &
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
