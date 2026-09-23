import type { Instant, PlainDate, PlainDateTime } from '@dante/time';

export type TimelineEventId = string;
export type TimelineGroupId = string;

export type TimelineSemanticTone =
  'focus' | 'meeting' | 'health' | 'creative' | 'personal' | 'urgent';

export type TimelineGroup = Readonly<{
  id: TimelineGroupId;
  label: string;
  tone: TimelineSemanticTone;
  /** Actor-local organization preference; not a Schedule or conflict filter. */
  hidden?: boolean;
  archived?: boolean;
}>;

export type TimelineCanonicalSchedulePlacement =
  | Readonly<{
      kind: 'date-span';
      startDate: PlainDate;
      endDateExclusive: PlainDate;
    }>
  | Readonly<{
      kind: 'floating-local';
      startsLocalAt: PlainDateTime;
      endsLocalAt: PlainDateTime;
    }>
  | Readonly<{
      kind: 'named-zone-local';
      startsLocalAt: PlainDateTime;
      endsLocalAt: PlainDateTime;
      zoneId: string;
      resolvedStartAt: Instant;
      resolvedEndAt: Instant;
    }>
  | Readonly<{
      kind: 'absolute';
      startsAt: Instant;
      endsAt: Instant;
    }>
  | Readonly<{
      kind: 'coarse-local-period';
      localDate: PlainDate;
      period: 'morning' | 'afternoon' | 'evening';
    }>;

export type TimelineCanonicalScheduledActivityBasis = Readonly<{
  kind: 'scheduled-activity';
  activityRef: string;
  eventRef?: never;
  scheduleRef: string;
  placementMaterialStateRef: string;
  placement: TimelineCanonicalSchedulePlacement;
}>;

export type TimelineCanonicalScheduledEventBasis = Readonly<{
  kind: 'scheduled-event';
  eventRef: string;
  activityRef?: never;
  scheduleRef: string;
  placementMaterialStateRef: string;
  placement: TimelineCanonicalSchedulePlacement;
}>;

export type TimelineCanonicalScheduledOccurrenceBasis = Readonly<{
  kind: 'scheduled-occurrence';
  occurrenceRef: string;
  sourceKind: 'routine' | 'event';
  sourceNativeRef: string;
  activityRef?: never;
  eventRef?: never;
  scheduleRef: string;
  placementMaterialStateRef: string;
  placement: TimelineCanonicalSchedulePlacement;
}>;

export type TimelineCanonicalScheduleBasis =
  | TimelineCanonicalScheduledActivityBasis
  | TimelineCanonicalScheduledEventBasis
  | TimelineCanonicalScheduledOccurrenceBasis;

export type TimelineEvent = Readonly<{
  id: TimelineEventId;
  startMinute: number;
  endMinute: number;
  title: string;
  groupId: TimelineGroupId;
  /** Presentation-only override; grouping and filters continue to use groupId. */
  appearanceTone?: TimelineSemanticTone;
  /**
   * Exact canonical basis retained by a real Timeline projection. It is not a
   * second owner and does not turn this ViewModel into canonical truth.
   */
  canonicalBasis?: TimelineCanonicalScheduleBasis;
  origin?: 'create';
  meta?: string;
  subitems?: readonly string[];
}>;

export type TimelineDateLaneKind =
  'all-day' | 'coarse' | 'expectation' | 'flexible';
export type TimelineCoarsePeriod = 'morning' | 'afternoon' | 'evening';

export type TimelineAllDayItem = Readonly<{
  id: string;
  startDateKey: string;
  endDateExclusiveKey: string;
  title: string;
  groupId: TimelineGroupId;
  /** Presentation-only override; grouping and filters continue to use groupId. */
  appearanceTone?: TimelineSemanticTone;
  /** Canonical Schedule identity retained without inventing a clock interval. */
  canonicalBasis?: TimelineCanonicalScheduleBasis;
  /** Defaults to all-day for legacy/local materialized items. */
  laneKind?: TimelineDateLaneKind;
  /** Present only for accepted coarse-local-period placement. */
  coarsePeriod?: TimelineCoarsePeriod;
  origin?: 'create';
  meta?: string;
}>;

export type TimelineDay = Readonly<{
  date: PlainDate;
  events: readonly TimelineEvent[];
}>;

export type TimelineDensityMetrics = Readonly<{
  count: number;
  shortCount: number;
  maxConcurrent: number;
  overlapRatio: number;
  burst: number;
}>;

export type TimelineTimeMapper = Readonly<{
  height: number;
  pxPerMinute: number;
  map: (minute: number) => number;
  inv: (pixel: number) => number;
}>;

export type TimelineOverlapSlot = Readonly<{
  lane: number;
  laneCount: number;
}>;

export type TimelineEventLayout = Readonly<{
  event: TimelineEvent;
  top: number;
  height: number;
  compactLane: number;
  compactLaneCount: number;
  compactLeftPercent: number;
  compactWidthPercent: number;
  groupIndex: number;
  groupLane: number;
  groupLaneCount: number;
}>;

export type TimelineGap = Readonly<{
  fromMinute: number;
  toMinute: number;
  durationMinutes: number;
}>;
