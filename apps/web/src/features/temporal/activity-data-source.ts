import type { Instant } from '@dante/time';

import type {
  TemporalAcceptedSchedulePlacement,
  TemporalSchedulePlacementInput,
} from './schedule-data-source';

export type TemporalActivityRecord = Readonly<{
  activityRef: string;
  title: string;
  createdAt: Instant;
}>;

export type TemporalActivityCreateRequest = Readonly<{
  operationId: string;
  title: string;
  lifeAreaRef?: string;
}>;

export type TemporalActivityCreateResult = Readonly<{
  activity: TemporalActivityRecord;
  replayed: boolean;
}>;

export type TemporalActivityConstraintRuleInput =
  | Readonly<{
      family: 'boundary';
      boundaryKind: 'earliest_start';
      constrainedFacet: 'schedule.start';
      strength: 'hard' | 'soft';
      boundaryAt: Instant;
    }>
  | Readonly<{
      family: 'boundary';
      boundaryKind: 'latest_completion';
      constrainedFacet: 'schedule.completion';
      strength: 'hard' | 'soft';
      boundaryAt: Instant;
    }>
  | Readonly<{
      family: 'window';
      relationship: 'full_placement_contained';
      constrainedFacet: 'schedule.placement';
      strength: 'hard' | 'soft';
      startsAt: Instant;
      endsAt: Instant;
    }>;

export type TemporalConstrainedActivityCreateRequest = Readonly<{
  operationId: string;
  title: string;
  lifeAreaRef?: string;
  rules: readonly TemporalActivityConstraintRuleInput[];
}>;

export type TemporalCreatedActivityConstraint = Readonly<{
  constraintRef: string;
  materialStateRef: string;
}>;

export type TemporalConstrainedActivityCreateResult = Readonly<{
  activity: TemporalActivityRecord;
  constraints: readonly TemporalCreatedActivityConstraint[];
  replayed: boolean;
}>;

export interface TemporalConstrainedActivityDataSource {
  createConstrainedActivity(
    request: TemporalConstrainedActivityCreateRequest,
    signal?: AbortSignal,
  ): Promise<TemporalConstrainedActivityCreateResult>;
}

export type TemporalScheduleRecord = Readonly<{
  scheduleRef: string;
  placementMaterialStateRef: string;
  placement: TemporalAcceptedSchedulePlacement;
}>;

/** Compatibility alias retained for callers that narrow the accepted placement. */
export type TemporalFloatingLocalScheduleRecord = TemporalScheduleRecord &
  Readonly<{
    placement: Extract<
      TemporalAcceptedSchedulePlacement,
      Readonly<{ kind: 'floating-local-interval' }>
    >;
  }>;

export type TemporalScheduledActivityCreateRequest = Readonly<{
  operationId: string;
  title: string;
  lifeAreaRef?: string;
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalActivityScheduleEstablishRequest = Readonly<{
  activityRef: string;
  operationId: string;
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalScheduledActivityCreateResult = Readonly<{
  activity: TemporalActivityRecord;
  schedule: TemporalScheduleRecord;
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
  establishActivitySchedule(
    request: TemporalActivityScheduleEstablishRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduledActivityCreateResult>;
  loadUnplaced(
    signal?: AbortSignal,
  ): Promise<readonly TemporalActivityRecord[]>;
}
