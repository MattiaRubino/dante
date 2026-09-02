import type { PlainDate } from '@dante/time';

export type TimelineEventId = string;
export type TimelineGroupId = string;

export type TimelineSemanticTone =
  | 'focus'
  | 'meeting'
  | 'health'
  | 'creative'
  | 'personal'
  | 'urgent';

export type TimelineGroup = Readonly<{
  id: TimelineGroupId;
  label: string;
  tone: TimelineSemanticTone;
}>;

export type TimelineEvent = Readonly<{
  id: TimelineEventId;
  startMinute: number;
  endMinute: number;
  title: string;
  groupId: TimelineGroupId;
  origin?: 'create';
  meta?: string;
  subitems?: readonly string[];
}>;

export type TimelineAllDayItem = Readonly<{
  id: string;
  startDateKey: string;
  endDateExclusiveKey: string;
  title: string;
  groupId: TimelineGroupId;
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
