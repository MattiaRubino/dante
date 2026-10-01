import type { Instant } from '@dante/time';

import type { TemporalSchedulePlacementInput } from './schedule-data-source';

export type TemporalPlanningTrayKind = 'activity' | 'event';
export type TemporalPlanningTrayState = 'unplaced' | 'postponed';

export type TemporalPlanningTrayItem = Readonly<{
  kind: TemporalPlanningTrayKind;
  state: TemporalPlanningTrayState;
  subjectRef: string;
  title: string;
  createdAt: Instant;
  lifeAreaRef: string | null;
  lifeAreaAssignmentRevision: number | null;
  scheduleRef: string | null;
}>;

export type TemporalPlanningTrayPlaceRequest = Readonly<{
  kind: TemporalPlanningTrayKind;
  subjectRef: string;
  operationId: string;
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalPlanningTrayPlaceResult = Readonly<{
  kind: TemporalPlanningTrayKind;
  subjectRef: string;
  scheduleRef: string;
  placementMaterialStateRef: string;
  replayed: boolean;
}>;

export interface TemporalPlanningTrayDataSource {
  listItems(signal?: AbortSignal): Promise<readonly TemporalPlanningTrayItem[]>;
  placeItem(
    request: TemporalPlanningTrayPlaceRequest,
    signal?: AbortSignal,
  ): Promise<TemporalPlanningTrayPlaceResult>;
}
