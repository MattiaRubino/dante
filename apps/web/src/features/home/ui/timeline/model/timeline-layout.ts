import { timelineEventReadableHeight } from './timeline-density';
import { TIMELINE_POLICY } from './timeline-policy';
import type {
  TimelineEvent,
  TimelineEventId,
  TimelineEventLayout,
  TimelineGap,
  TimelineGroup,
  TimelineOverlapSlot,
  TimelineTimeMapper,
} from './timeline-types';

function groupOrderIndex(
  groupId: string,
  groups: readonly TimelineGroup[],
): number {
  const index = groups.findIndex((group) => group.id === groupId);
  return index < 0 ? groups.length : index;
}

export function computeTimelineOverlapLayout(
  events: readonly TimelineEvent[],
  groups: readonly TimelineGroup[] = [],
): ReadonlyMap<TimelineEventId, TimelineOverlapSlot> {
  const sorted = [...events].sort((left, right) => {
    return (
      left.startMinute - right.startMinute ||
      groupOrderIndex(left.groupId, groups) -
        groupOrderIndex(right.groupId, groups) ||
      left.endMinute - right.endMinute ||
      left.id.localeCompare(right.id)
    );
  });

  const clusters: TimelineEvent[][] = [];
  let current: { events: TimelineEvent[]; endMinute: number } | undefined;

  for (const event of sorted) {
    if (!current || event.startMinute >= current.endMinute) {
      current = { events: [event], endMinute: event.endMinute };
      clusters.push(current.events);
      continue;
    }

    current.events.push(event);
    current.endMinute = Math.max(current.endMinute, event.endMinute);
  }

  const result = new Map<TimelineEventId, TimelineOverlapSlot>();
  for (const cluster of clusters) {
    const laneEndMinutes: number[] = [];
    const laneByEvent = new Map<TimelineEventId, number>();

    for (const event of cluster) {
      let lane = laneEndMinutes.findIndex(
        (endMinute) => endMinute <= event.startMinute,
      );
      if (lane < 0) {
        lane = laneEndMinutes.length;
        laneEndMinutes.push(event.endMinute);
      } else {
        laneEndMinutes[lane] = event.endMinute;
      }
      laneByEvent.set(event.id, lane);
    }

    const laneCount = Math.max(1, laneEndMinutes.length);
    for (const event of cluster) {
      result.set(event.id, {
        lane: laneByEvent.get(event.id) ?? 0,
        laneCount,
      });
    }
  }

  return result;
}

function preferredCompactWidthPercent(
  event: TimelineEvent,
  laneCount: number,
): number {
  const layout = TIMELINE_POLICY.layout;
  if (laneCount > 1) {
    const laneWidth = layout.compactMaxRightPercent / laneCount;
    return Math.max(layout.compactMultiLaneMinWidthPercent, laneWidth - 1);
  }

  const titleWeight = Math.min(68, event.title.length);
  const metaWeight = Math.min(44, event.meta?.length ?? 0) * 0.24;
  return Math.max(
    layout.compactSingleLaneMinWidthPercent,
    Math.min(
      layout.compactSingleLaneMaxWidthPercent,
      48 + titleWeight * 0.34 + metaWeight * 0.14,
    ),
  );
}

export function computeTimelineEventLayouts(
  events: readonly TimelineEvent[],
  groups: readonly TimelineGroup[],
  mapper: TimelineTimeMapper,
): readonly TimelineEventLayout[] {
  const compactLayout = computeTimelineOverlapLayout(events, groups);
  const groupLayouts = new Map<
    TimelineEventId,
    Readonly<{ groupIndex: number; groupLane: number; groupLaneCount: number }>
  >();

  groups.forEach((group, groupIndex) => {
    const groupEvents = events.filter((event) => event.groupId === group.id);
    const overlap = computeTimelineOverlapLayout(groupEvents, groups);
    for (const event of groupEvents) {
      const slot = overlap.get(event.id) ?? { lane: 0, laneCount: 1 };
      groupLayouts.set(event.id, {
        groupIndex,
        groupLane: slot.lane,
        groupLaneCount: slot.laneCount,
      });
    }
  });

  const groupCount = Math.max(1, groups.length);
  const layoutPolicy = TIMELINE_POLICY.layout;

  return events.map((event) => {
    const compact = compactLayout.get(event.id) ?? { lane: 0, laneCount: 1 };
    const group = groupLayouts.get(event.id) ?? {
      groupIndex: 0,
      groupLane: 0,
      groupLaneCount: 1,
    };
    const top = mapper.map(event.startMinute);
    const naturalHeight = mapper.map(event.endMinute) - top;
    const height = Math.max(naturalHeight, timelineEventReadableHeight(event));
    const orderIndex = Math.max(0, groupOrderIndex(event.groupId, groups));
    const orderBias =
      groupCount > 1 ? (orderIndex / (groupCount - 1)) * 14 : 0;

    let compactLeftPercent: number;
    let compactWidthPercent: number;
    if (compact.laneCount === 1) {
      compactLeftPercent = layoutPolicy.compactLeftInsetPercent + orderBias;
      compactWidthPercent = preferredCompactWidthPercent(event, 1);
    } else {
      const laneSpan =
        layoutPolicy.compactLaneRegionPercent / compact.laneCount;
      compactLeftPercent =
        layoutPolicy.compactLeftInsetPercent + compact.lane * laneSpan;
      compactWidthPercent = Math.max(14, laneSpan - 1);
    }

    compactLeftPercent = Math.max(
      layoutPolicy.compactLeftInsetPercent,
      Math.min(layoutPolicy.compactMaxLeftPercent, compactLeftPercent),
    );
    compactWidthPercent = Math.max(
      30,
      Math.min(
        compactWidthPercent,
        layoutPolicy.compactMaxRightPercent - compactLeftPercent,
      ),
    );

    return {
      event,
      top,
      height,
      compactLane: compact.lane,
      compactLaneCount: compact.laneCount,
      compactLeftPercent,
      compactWidthPercent,
      ...group,
    };
  });
}

export function computeTimelineGaps(
  events: readonly TimelineEvent[],
): readonly TimelineGap[] {
  const sorted = [...events].sort(
    (left, right) => left.startMinute - right.startMinute,
  );
  const clusters: Array<{ startMinute: number; endMinute: number }> = [];

  for (const event of sorted) {
    const previous = clusters.at(-1);
    if (previous && event.startMinute < previous.endMinute) {
      previous.endMinute = Math.max(previous.endMinute, event.endMinute);
    } else {
      clusters.push({
        startMinute: event.startMinute,
        endMinute: event.endMinute,
      });
    }
  }

  const gaps: TimelineGap[] = [];
  for (let index = 0; index < clusters.length - 1; index += 1) {
    const cluster = clusters[index];
    const next = clusters[index + 1];
    if (!cluster || !next) {
      continue;
    }

    gaps.push({
      fromMinute: cluster.endMinute,
      toMinute: next.startMinute,
      durationMinutes: next.startMinute - cluster.endMinute,
    });
  }

  return gaps;
}
