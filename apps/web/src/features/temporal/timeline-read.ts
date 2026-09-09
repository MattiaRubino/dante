import type { PlainDateTime } from '@dante/time';

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

export type TemporalTimelineScheduledActivityItem = Readonly<{
  kind: 'scheduled_activity';
  activityRef: string;
  scheduleRef: string;
  placementMaterialStateRef: string;
  title: string;
  temporalForm: 'floating-local';
  startsLocalAt: PlainDateTime;
  endsLocalAt: PlainDateTime;
}>;

export type TemporalTimelineItemsWindow = Readonly<{
  kind: 'window';
  startDate: string;
  endDateExclusive: string;
  effectiveZoneId: string;
  items: readonly TemporalTimelineScheduledActivityItem[];
}>;

export type TemporalTimelineWindow =
  TemporalTimelineEmptyWindow | TemporalTimelineItemsWindow;

export interface TemporalTimelineDataSource {
  loadWindow(
    request: TemporalTimelineWindowRequest,
    signal?: AbortSignal,
  ): Promise<TemporalTimelineWindow>;
}
