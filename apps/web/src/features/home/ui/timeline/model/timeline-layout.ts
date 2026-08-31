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

function timelineEventsOverlap(
  left: TimelineEvent,
  right: TimelineEvent,
): boolean {
  return left.startMinute < right.endMinute && right.startMinute < left.endMinute;
}

export function computeTimelineOverlapLayout(
  events: readonly TimelineEvent[],
  groups: readonly TimelineGroup[] = [],
): ReadonlyMap<TimelineEventId, TimelineOverlapSlot> {
  const chronological = [...events].sort((left, right) => {
    return (
      left.startMinute - right.startMinute ||
      left.endMinute - right.endMinute ||
      groupOrderIndex(left.groupId, groups) -
        groupOrderIndex(right.groupId, groups) ||
      left.id.localeCompare(right.id)
    );
  });

  const clusters: TimelineEvent[][] = [];
  let current: { events: TimelineEvent[]; endMinute: number } | undefined;

  for (const event of chronological) {
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
    /*
     * Compact mode is not a rigid grouped grid, but overlapping cards still
     * need a truthful left-to-right relationship with the visible group row.
     * Assigning lanes only by event start time made reordered group chips and
     * their cards drift apart. Within each temporal collision cluster we keep
     * the minimum number of practical lanes while guaranteeing this invariant:
     * when two cards overlap, a card from an earlier visible group can never be
     * placed to the right of a card from a later visible group.
     */
    const semanticOrder = [...cluster].sort((left, right) => {
      return (
        groupOrderIndex(left.groupId, groups) -
          groupOrderIndex(right.groupId, groups) ||
        left.startMinute - right.startMinute ||
        left.endMinute - right.endMinute ||
        left.id.localeCompare(right.id)
      );
    });
    const laneByEvent = new Map<TimelineEventId, number>();
    const assigned: TimelineEvent[] = [];
    let maxLane = 0;

    for (const event of semanticOrder) {
      const eventGroupIndex = groupOrderIndex(event.groupId, groups);
      let lane = 0;

      for (const previous of assigned) {
        if (
          timelineEventsOverlap(previous, event) &&
          groupOrderIndex(previous.groupId, groups) < eventGroupIndex
        ) {
          lane = Math.max(lane, (laneByEvent.get(previous.id) ?? 0) + 1);
        }
      }

      while (
        assigned.some(
          (previous) =>
            laneByEvent.get(previous.id) === lane &&
            timelineEventsOverlap(previous, event),
        )
      ) {
        lane += 1;
      }

      laneByEvent.set(event.id, lane);
      assigned.push(event);
      maxLane = Math.max(maxLane, lane);
    }

    const laneCount = Math.max(1, maxLane + 1);
    for (const event of cluster) {
      result.set(event.id, {
        lane: laneByEvent.get(event.id) ?? 0,
        laneCount,
      });
    }
  }

  return result;
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

    let compactLeftPercent: number;
    let compactWidthPercent: number;
    if (compact.laneCount === 1) {
      /*
       * Zero is an explicit intrinsic-sizing sentinel. Isolated cards have no
       * horizontal collision constraint, so their width belongs to the DOM
       * runtime where the real rendered content/font/locale can be measured.
       * The layout engine only owns their temporal position and shared axis.
       */
      compactLeftPercent = layoutPolicy.compactLeftInsetPercent;
      compactWidthPercent = 0;
    } else {
      const laneSpan =
        layoutPolicy.compactLaneRegionPercent / compact.laneCount;
      compactLeftPercent =
        layoutPolicy.compactLeftInsetPercent + compact.lane * laneSpan;
      compactWidthPercent = Math.max(
        layoutPolicy.compactAbsoluteMinLaneWidthPercent,
        laneSpan - layoutPolicy.compactMultiLaneGapPercent,
      );
      compactWidthPercent = Math.min(
        compactWidthPercent,
        layoutPolicy.compactMaxRightPercent - compactLeftPercent,
      );
    }

    compactLeftPercent = Math.max(
      layoutPolicy.compactLeftInsetPercent,
      Math.min(layoutPolicy.compactMaxLeftPercent, compactLeftPercent),
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
