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

export type TemporalTimelineWindow = TemporalTimelineEmptyWindow;

export interface TemporalTimelineDataSource {
  loadWindow(
    request: TemporalTimelineWindowRequest,
    signal?: AbortSignal,
  ): Promise<TemporalTimelineWindow>;
}
