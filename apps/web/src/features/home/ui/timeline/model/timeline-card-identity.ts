import type { TimelineCanonicalScheduleBasis } from './timeline-types';

/** Presentation markers derive from canonical ownership, never Life Area color. */
export function timelineCardIdentity(
  basis: TimelineCanonicalScheduleBasis | undefined,
  expectedSourceKind?: 'routine' | 'event',
): Readonly<{ kind: 'activity' | 'event'; recurringInstance: boolean }> {
  return {
    kind:
      basis?.kind === 'scheduled-activity' ||
      (basis?.kind === 'scheduled-occurrence' &&
        basis.sourceKind === 'routine') ||
      (basis === undefined && expectedSourceKind === 'routine')
        ? 'activity'
        : 'event',
    recurringInstance:
      basis?.kind === 'scheduled-occurrence' ||
      expectedSourceKind !== undefined,
  };
}
