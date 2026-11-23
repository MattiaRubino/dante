import { describe, expect, it } from 'vitest';

import type { TimelineCanonicalScheduleBasis } from './model/timeline-types';
import { movedVaultSubjectKey, wasMovedToVault } from './timeline-vault-move-visibility';

describe('Vault move Timeline tombstones', () => {
  const activity = {
    kind: 'scheduled-activity',
    activityRef: 'activity-1',
  } as TimelineCanonicalScheduleBasis;
  const event = {
    kind: 'scheduled-event',
    eventRef: 'event-1',
  } as TimelineCanonicalScheduleBasis;
  const unrelated = {
    kind: 'scheduled-activity',
    activityRef: 'activity-2',
  } as TimelineCanonicalScheduleBasis;
  const occurrence = {
    kind: 'scheduled-occurrence',
    occurrenceRef: 'occ-1',
    sourceKind: 'event',
    sourceNativeRef: 'event-1',
  } as TimelineCanonicalScheduleBasis;

  it('keeps a confirmed Activity invisible across stale timed or all-day projections', () => {
    const removed = new Set([movedVaultSubjectKey('activity', 'activity-1')]);
    expect(wasMovedToVault(activity, removed)).toBe(true);
    expect(wasMovedToVault(unrelated, removed)).toBe(false);
    expect(wasMovedToVault(event, removed)).toBe(false);
    expect(wasMovedToVault(undefined, removed)).toBe(false);
  });

  it('hides an Event by native identity even if a stale Schedule projection arrives', () => {
    const removed = new Set([movedVaultSubjectKey('event', 'event-1')]);
    expect(wasMovedToVault(event, removed)).toBe(true);
    expect(wasMovedToVault(activity, removed)).toBe(false);
    // Move is forbidden for series/instances; their separate identity remains
    // governed by the recurrence machinery.
    expect(wasMovedToVault(occurrence, removed)).toBe(false);
  });
});
