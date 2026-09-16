import type { Instant, PlainDate, PlainDateTime } from '@dante/time';

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

export type TemporalTimelineDateSpanActivityItem =
  TemporalTimelineScheduledActivityBase &
    Readonly<{
      temporalForm: 'date-span';
      startDate: PlainDate;
      endDateExclusive: PlainDate;
    }>;

export type TemporalTimelineFloatingLocalActivityItem =
  TemporalTimelineScheduledActivityBase &
    Readonly<{
      temporalForm: 'floating-local';
      startsLocalAt: PlainDateTime;
      endsLocalAt: PlainDateTime;
    }>;

export type TemporalTimelineNamedZoneLocalActivityItem =
  TemporalTimelineScheduledActivityBase &
    Readonly<{
      temporalForm: 'named-zone-local';
      startsLocalAt: PlainDateTime;
      endsLocalAt: PlainDateTime;
      zoneId: string;
      resolvedStartAt: Instant;
      resolvedEndAt: Instant;
      displayStartsLocalAt: PlainDateTime;
      displayEndsLocalAt: PlainDateTime;
    }>;

export type TemporalTimelineAbsoluteActivityItem =
  TemporalTimelineScheduledActivityBase &
    Readonly<{
      temporalForm: 'absolute';
      startsAt: Instant;
      endsAt: Instant;
      displayStartsLocalAt: PlainDateTime;
      displayEndsLocalAt: PlainDateTime;
    }>;

export type TemporalTimelineCoarseLocalPeriod =
  | 'morning'
  | 'afternoon'
  | 'evening';

export type TemporalTimelineCoarseLocalPeriodActivityItem =
  TemporalTimelineScheduledActivityBase &
    Readonly<{
      temporalForm: 'coarse-local-period';
      localDate: PlainDate;
      period: TemporalTimelineCoarseLocalPeriod;
    }>;

export type TemporalTimelineScheduledActivityItem =
  | TemporalTimelineDateSpanActivityItem
  | TemporalTimelineFloatingLocalActivityItem
  | TemporalTimelineNamedZoneLocalActivityItem
  | TemporalTimelineAbsoluteActivityItem
  | TemporalTimelineCoarseLocalPeriodActivityItem;

export type TemporalTimelineItemsWindow = Readonly<{
  kind: 'window';
  startDate: string;
  endDateExclusive: string;
  effectiveZoneId: string;
  items: readonly TemporalTimelineScheduledActivityItem[];
}>;

export type TemporalTimelineWindow =
  | TemporalTimelineEmptyWindow
  | TemporalTimelineItemsWindow;

export interface TemporalTimelineDataSource {
  loadWindow(
    request: TemporalTimelineWindowRequest,
    signal?: AbortSignal,
  ): Promise<TemporalTimelineWindow>;
}
