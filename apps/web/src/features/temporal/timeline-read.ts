import type { Instant, PlainDate, PlainDateTime, PlainTime } from '@dante/time';

export type TemporalTimelineWindowRequest = Readonly<{
  startDate: string;
  endDateExclusive: string;
}>;

export type TemporalTimelineEmptyWindow = Readonly<{
  kind: 'empty';
  startDate: string;
  endDateExclusive: string;
  effectiveZoneId: string;
}>;

type TemporalTimelineScheduledActivityBase = Readonly<{
  kind: 'scheduled_activity';
  activityRef: string;
  scheduleRef: string;
  placementMaterialStateRef: string;
  title: string;
}>;

type TemporalTimelineScheduledEventBase = Readonly<{
  kind: 'scheduled_event';
  eventRef: string;
  scheduleRef: string;
  placementMaterialStateRef: string;
  title: string;
}>;

type TemporalTimelineDateSpanFields = Readonly<{
  temporalForm: 'date-span';
  startDate: PlainDate;
  endDateExclusive: PlainDate;
}>;

type TemporalTimelineFloatingLocalFields = Readonly<{
  temporalForm: 'floating-local';
  startsLocalAt: PlainDateTime;
  endsLocalAt: PlainDateTime;
}>;

type TemporalTimelineNamedZoneLocalFields = Readonly<{
  temporalForm: 'named-zone-local';
  startsLocalAt: PlainDateTime;
  endsLocalAt: PlainDateTime;
  zoneId: string;
  resolvedStartAt: Instant;
  resolvedEndAt: Instant;
  displayStartsLocalAt: PlainDateTime;
  displayEndsLocalAt: PlainDateTime;
}>;

type TemporalTimelineAbsoluteFields = Readonly<{
  temporalForm: 'absolute';
  startsAt: Instant;
  endsAt: Instant;
  displayStartsLocalAt: PlainDateTime;
  displayEndsLocalAt: PlainDateTime;
}>;

export type TemporalTimelineCoarseLocalPeriod =
  'morning' | 'afternoon' | 'evening';

type TemporalTimelineCoarseLocalPeriodFields = Readonly<{
  temporalForm: 'coarse-local-period';
  localDate: PlainDate;
  period: TemporalTimelineCoarseLocalPeriod;
}>;

export type TemporalTimelineDateSpanActivityItem =
  TemporalTimelineScheduledActivityBase & TemporalTimelineDateSpanFields;
export type TemporalTimelineFloatingLocalActivityItem =
  TemporalTimelineScheduledActivityBase & TemporalTimelineFloatingLocalFields;
export type TemporalTimelineNamedZoneLocalActivityItem =
  TemporalTimelineScheduledActivityBase & TemporalTimelineNamedZoneLocalFields;
export type TemporalTimelineAbsoluteActivityItem =
  TemporalTimelineScheduledActivityBase & TemporalTimelineAbsoluteFields;
export type TemporalTimelineCoarseLocalPeriodActivityItem =
  TemporalTimelineScheduledActivityBase &
    TemporalTimelineCoarseLocalPeriodFields;

export type TemporalTimelineScheduledActivityItem =
  | TemporalTimelineDateSpanActivityItem
  | TemporalTimelineFloatingLocalActivityItem
  | TemporalTimelineNamedZoneLocalActivityItem
  | TemporalTimelineAbsoluteActivityItem
  | TemporalTimelineCoarseLocalPeriodActivityItem;

export type TemporalTimelineDateSpanEventItem =
  TemporalTimelineScheduledEventBase & TemporalTimelineDateSpanFields;
export type TemporalTimelineFloatingLocalEventItem =
  TemporalTimelineScheduledEventBase & TemporalTimelineFloatingLocalFields;
export type TemporalTimelineNamedZoneLocalEventItem =
  TemporalTimelineScheduledEventBase & TemporalTimelineNamedZoneLocalFields;
export type TemporalTimelineAbsoluteEventItem =
  TemporalTimelineScheduledEventBase & TemporalTimelineAbsoluteFields;
export type TemporalTimelineCoarseLocalPeriodEventItem =
  TemporalTimelineScheduledEventBase & TemporalTimelineCoarseLocalPeriodFields;

export type TemporalTimelineScheduledEventItem =
  | TemporalTimelineDateSpanEventItem
  | TemporalTimelineFloatingLocalEventItem
  | TemporalTimelineNamedZoneLocalEventItem
  | TemporalTimelineAbsoluteEventItem
  | TemporalTimelineCoarseLocalPeriodEventItem;

export type TemporalTimelineOccurrenceCoordinate =
  | Readonly<{
      familyCode: 'calendar-wall-clock';
      generatedDate: PlainDate;
      generatedWallTime: PlainTime | null;
      clockBasis: 'floating-local' | 'named-zone' | 'absolute-utc';
      zoneId: string | null;
      resolvedAt: Instant | null;
    }>
  | Readonly<{
      familyCode: 'elapsed-interval';
      expectedAt: Instant;
    }>
  | Readonly<{
      familyCode: 'quota-per-period';
      periodStartDate: PlainDate;
      periodEndDateExclusive: PlainDate;
      frame: 'floating-local' | 'named-zone' | 'absolute-utc';
      zoneId: string | null;
    }>
  | Readonly<{
      familyCode: 'cyclic-positional';
      generatedDate: PlainDate;
      positionIndex: number;
    }>;

type TemporalTimelineScheduledOccurrenceBase = Readonly<{
  kind: 'scheduled_occurrence';
  occurrenceRef: string;
  sourceKind: 'routine' | 'event';
  sourceNativeRef: string;
  scheduleRef: string;
  placementMaterialStateRef: string;
  title: string;
  coordinate: TemporalTimelineOccurrenceCoordinate | null;
}>;

export type TemporalTimelineScheduledOccurrenceItem =
  TemporalTimelineScheduledOccurrenceBase &
    (
      | TemporalTimelineDateSpanFields
      | TemporalTimelineFloatingLocalFields
      | TemporalTimelineNamedZoneLocalFields
      | TemporalTimelineAbsoluteFields
      | TemporalTimelineCoarseLocalPeriodFields
    );

export type TemporalTimelineExpectedOccurrenceItem = Readonly<{
  kind: 'expected_occurrence';
  occurrenceRef: string;
  sourceKind: 'routine' | 'event';
  sourceNativeRef: string;
  title: string;
  coordinate: TemporalTimelineOccurrenceCoordinate;
}>;

export type TemporalTimelineScheduledItem =
  | TemporalTimelineScheduledActivityItem
  | TemporalTimelineScheduledEventItem
  | TemporalTimelineScheduledOccurrenceItem;

export type TemporalTimelineItem =
  TemporalTimelineScheduledItem | TemporalTimelineExpectedOccurrenceItem;

export type TemporalTimelineItemsWindow = Readonly<{
  kind: 'window';
  startDate: string;
  endDateExclusive: string;
  effectiveZoneId: string;
  items: readonly TemporalTimelineItem[];
}>;

export type TemporalTimelineWindow =
  TemporalTimelineEmptyWindow | TemporalTimelineItemsWindow;

export interface TemporalTimelineDataSource {
  loadWindow(
    request: TemporalTimelineWindowRequest,
    signal?: AbortSignal,
  ): Promise<TemporalTimelineWindow>;
}
