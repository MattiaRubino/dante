import type { TimelineCanonicalScheduleBasis } from './model/timeline-types';

/**
 * Successful owner-local Vault moves are hard deletes. Hide the old native
 * subject from presentation immediately after the server commit, including
 * during an in-flight or stale authoritative Timeline/Area refresh.
 *
 * This Set is UI-only; it is not canonical deletion state.
 */
export function movedVaultSubjectKey(
  kind: 'activity' | 'event',
  nativeRef: string,
): string {
  return `${kind}:${nativeRef}`;
}

export function wasMovedToVault(
  basis: TimelineCanonicalScheduleBasis | undefined,
  movedSubjects: ReadonlySet<string>,
): boolean {
  if (!basis) return false;
  if (basis.kind === 'scheduled-activity') {
    return movedSubjects.has(movedVaultSubjectKey('activity', basis.activityRef));
  }
  if (basis.kind === 'scheduled-event') {
    return movedSubjects.has(movedVaultSubjectKey('event', basis.eventRef));
  }
  // A standalone Move never targets series/occurrence subjects.
  return false;
}
