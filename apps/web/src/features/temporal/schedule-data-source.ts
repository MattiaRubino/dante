import type { Instant, PlainDate, PlainDateTime } from '@dante/time';

export type TemporalScheduleDisambiguation = 'reject' | 'earlier' | 'later';
export type TemporalScheduleCoarsePeriod =
  | 'morning'
  | 'afternoon'
  | 'evening';

export type TemporalSchedulePlacementInput =
  | Readonly<{
      kind: 'date-span';
      startDate: PlainDate;
      endDateExclusive: PlainDate;
    }>
  | Readonly<{
      kind: 'floating-local-interval';
      startsLocalAt: PlainDateTime;
      endsLocalAt: PlainDateTime;
    }>
  | Readonly<{
      kind: 'named-zone-local-interval';
      startsLocalAt: PlainDateTime;
      endsLocalAt: PlainDateTime;
      zoneId: string;
      disambiguation: TemporalScheduleDisambiguation;
    }>
  | Readonly<{
      kind: 'absolute-interval';
      startsAt: Instant;
      endsAt: Instant;
    }>
  | Readonly<{
      kind: 'coarse-local-period';
      localDate: PlainDate;
      period: TemporalScheduleCoarsePeriod;
    }>;

export type TemporalAcceptedSchedulePlacement =
  | Exclude<
      TemporalSchedulePlacementInput,
      Readonly<{ kind: 'named-zone-local-interval' }>
    >
  | Readonly<{
      kind: 'named-zone-local-interval';
      startsLocalAt: PlainDateTime;
      endsLocalAt: PlainDateTime;
      zoneId: string;
      resolvedStartAt: Instant;
      resolvedEndAt: Instant;
    }>;

export type TemporalScheduleRevisionRequest = Readonly<{
  operationId: string;
  scheduleRef: string;
  expectedPlacementMaterialStateRef: string;
  placement: TemporalSchedulePlacementInput;
}>;

export type TemporalScheduleRevisionResult = Readonly<{
  scheduleRef: string;
  previousPlacementMaterialStateRef: string;
  placementMaterialStateRef: string;
  placement: TemporalAcceptedSchedulePlacement;
  replayed: boolean;
}>;

export type TemporalScheduleUnscheduleRequest = Readonly<{
  operationId: string;
  scheduleRef: string;
  expectedPlacementMaterialStateRef: string;
}>;

export type TemporalScheduleUnscheduleResult = Readonly<{
  scheduleRef: string;
  previousPlacementMaterialStateRef: string;
  unscheduleOperationId: string;
  replayed: boolean;
}>;

export type TemporalScheduleUnscheduleUndoRequest = Readonly<{
  operationId: string;
  scheduleRef: string;
  unscheduleOperationId: string;
}>;

export type TemporalScheduleUnscheduleUndoResult = Readonly<{
  scheduleRef: string;
  restoredFromPlacementMaterialStateRef: string;
  placementMaterialStateRef: string;
  placement: TemporalAcceptedSchedulePlacement;
  replayed: boolean;
}>;

export interface TemporalScheduleDataSource {
  reviseSchedule(
    request: TemporalScheduleRevisionRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduleRevisionResult>;

  unscheduleSchedule(
    request: TemporalScheduleUnscheduleRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduleUnscheduleResult>;

  undoScheduleUnschedule(
    request: TemporalScheduleUnscheduleUndoRequest,
    signal?: AbortSignal,
  ): Promise<TemporalScheduleUnscheduleUndoResult>;
}
