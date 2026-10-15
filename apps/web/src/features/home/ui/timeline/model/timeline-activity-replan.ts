import { Temporal } from '@dante/time';

import type {
  ActivityEditSettings,
  ActivityReplanDraft,
} from '../../../../temporal/remote-activity-edit-settings';
import type { TimelineCanonicalRevision } from './timeline-canonical-revision';
import type { TimelineCanonicalScheduledActivityBasis } from './timeline-types';

/** Build a complete Activity command from one Timeline edit, without changing real attempts. */
export function activityReplanForTimelineRevision(
  settings: ActivityEditSettings,
  basis: TimelineCanonicalScheduledActivityBasis,
  revision: TimelineCanonicalRevision,
): ActivityReplanDraft | null {
  const target = settings.schedules.find(
    (row) => row.scheduleRef === basis.scheduleRef,
  );
  const envelope = settings.schedules.find((row) => row.role === 'envelope');
  const intervals = settings.schedules.filter((row) => row.role === 'interval');
  if (
    !target ||
    !envelope ||
    target.role !== (intervals.length ? 'interval' : 'envelope') ||
    !target.start ||
    !target.end ||
    !target.placementStateRef ||
    target.placementStateRef !== basis.placementMaterialStateRef ||
    target.temporalForm !== envelope.temporalForm ||
    (target.temporalForm !== 'floating_local' &&
      target.temporalForm !== 'named_zone_local') ||
    (revision.next.kind !== 'floating-local-interval' &&
      revision.next.kind !== 'named-zone-local-interval') ||
    (target.temporalForm === 'floating_local') !==
      (revision.next.kind === 'floating-local-interval')
  ) {
    return null;
  }

  const nextStart = revision.next.startsLocalAt.toString();
  const nextEnd = revision.next.endsLocalAt.toString();
  const times: Record<string, { start: string; end: string }> = {};
  for (const row of intervals.length ? intervals : [envelope]) {
    if (!row.start || !row.end || !row.placementStateRef) return null;
    times[row.scheduleRef] = { start: row.start, end: row.end };
  }
  times[target.scheduleRef] = { start: nextStart, end: nextEnd };
  const ordered = Object.values(times).sort((a, b) =>
    a.start.localeCompare(b.start),
  );
  if (
    ordered.some((span) => span.start >= span.end) ||
    ordered.some(
      (span, index) => index > 0 && ordered[index - 1]!.end > span.start,
    )
  ) {
    return null;
  }
  // A named-zone revision must retain valid local times in the source zone.
  // The canonical display conversion already resolved DST; compare the resulting
  // wall times here to avoid submitting a malformed concurrent draft.
  try {
    Temporal.PlainDateTime.from(nextStart);
    Temporal.PlainDateTime.from(nextEnd);
  } catch {
    return null;
  }
  return {
    times,
    removedIntervals: [],
    newIntervals: [],
    removedPlanned: [],
    deletedPlanned: [],
    newPlanned: [],
  };
}
