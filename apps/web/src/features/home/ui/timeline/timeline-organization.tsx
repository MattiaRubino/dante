import { useCallback, useEffect, useMemo, useState } from 'react';

import {
  createRemoteTemporalOrganizationDataSource,
  type OrganizationKind,
  type OrganizationSnapshot,
} from '../../../temporal/remote-organization';
import { subscribeTemporalTimelineInvalidation } from '../../../temporal/timeline-invalidation';
import type { TimelineGroup } from './model/timeline-types';

export const LEGACY_UNASSIGNED_GROUP = 'legacy-unassigned';

export function canonicalOrganizationGroups(
  snapshot: OrganizationSnapshot,
): readonly TimelineGroup[] {
  const areas = [...snapshot.areas].sort((a, b) => a.sortOrder - b.sortOrder);
  const groups: TimelineGroup[] = areas.map((item) => ({
    id: item.ref,
    label: item.name,
    tone: 'personal',
    organizationRevision: item.revision,
    colorCode: item.colorCode,
    hidden: item.hidden,
    archived: item.archived,
  }));
  // U2 makes unassigned a legitimate actor-local organization state. The
  // group itself remains neutral; accepted item colors stay presentation-only.
  if (snapshot.unassigned.length || snapshot.assignments.length === 0) {
    const itemColorCodes = Object.freeze(
      Object.fromEntries(
        snapshot.unassigned.flatMap((item) =>
          item.colorCode === null
            ? []
            : [[`${item.kind}:${item.itemRef}`, item.colorCode]],
        ),
      ),
    );
    groups.push({
      id: LEGACY_UNASSIGNED_GROUP,
      label: 'Senza Life Area',
      tone: 'personal',
      itemColorCodes,
    });
  }
  return Object.freeze(groups);
}

export function useTimelineOrganization(enabled: boolean) {
  const [snapshot, setSnapshot] = useState<OrganizationSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [revision, setRevision] = useState(0);
  const source = useMemo(() => createRemoteTemporalOrganizationDataSource(), []);
  const refresh = useCallback(() => setRevision((value) => value + 1), []);

  useEffect(() => {
    if (!enabled) return;
    return subscribeTemporalTimelineInvalidation(refresh);
  }, [enabled, refresh]);

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    void source.load().then(
      (result) => {
        if (cancelled) return;
        setSnapshot(result);
        setError(null);
      },
      (reason: unknown) => {
        if (cancelled) return;
        setError(
          reason instanceof Error
            ? reason.message
            : 'Organizzazione non disponibile.',
        );
      },
    );
    return () => {
      cancelled = true;
    };
  }, [enabled, revision, source]);

  return { snapshot, error, source, refresh } as const;
}

type Item = Readonly<{ kind: OrganizationKind; itemRef: string }>;
type Source = ReturnType<typeof createRemoteTemporalOrganizationDataSource>;

/**
 * U3 retires the old inline Life Area/Tag editor from Timeline. Quick Create
 * owns day-to-day Life Area authoring; richer organization management can
 * return later as a dedicated surface without duplicating controls here.
 *
 * The export is retained temporarily so TimelineSurface does not need a broad
 * structural rewrite in the same visual step.
 */
export function TimelineOrganizationPanel(
  _props: Readonly<{
    snapshot: OrganizationSnapshot | null;
    error: string | null;
    source: Source;
    onRefresh: () => void;
    selectedItem: Item | null;
  }>,
) {
  return null;
}
