import { useEffect, useMemo, useState } from 'react';

import { createWebFetch } from '../../../../platform/api/web-fetch';
import { createRemoteActivityEditSettings } from '../../../temporal/remote-activity-edit-settings';
import { createRemoteRealityObjectiveDataSource } from '../../../temporal/remote-reality-objective-data-source';
import {
  subscribeTemporalPlanningInvalidation,
  subscribeTemporalTimelineInvalidation,
} from '../../../temporal/timeline-invalidation';
import type { TimelineAllDayItem } from './model/timeline-types';

type Details = Readonly<{
  objectives: number;
  sessions: number;
  lifeAreaRef: string | null;
}>;
const reads = new Map<string, Promise<Details>>();

function readDetails(key: string): Promise<Details> {
  const cached = reads.get(key);
  if (cached) return cached;
  const [kind, ref] = key.split(':') as [string, string];
  const read = (async () => {
    if (kind === 'activity') {
      const [settings, children] = await Promise.all([
        createRemoteActivityEditSettings().load(ref),
        createWebFetch(globalThis.fetch)(
          `/api/v1/temporal/activities/${encodeURIComponent(ref)}/children`,
        )
          .then(async (response) =>
            response.ok ? (response.json() as Promise<unknown>) : null,
          )
          .catch(() => null),
      ]);
      const schedules =
        children && typeof children === 'object' && 'schedules' in children
          ? children.schedules
          : null;
      return {
        objectives: settings.objectives.length,
        sessions: Array.isArray(schedules)
          ? schedules.filter(
              (row: unknown) =>
                row &&
                typeof row === 'object' &&
                'role_code' in row &&
                row.role_code === 'planned',
            ).length
          : 0,
        lifeAreaRef: settings.lifeAreaRef,
      };
    }
    const objectives =
      await createRemoteRealityObjectiveDataSource().listObjectives(
        'event',
        ref,
      );
    return { objectives: objectives.length, sessions: 0, lifeAreaRef: null };
  })().catch((error: unknown) => {
    reads.delete(key);
    throw error;
  });
  reads.set(key, read);
  return read;
}

/** One planning read per subject, even when its bar spans many visible days. */
export function useTimelineDateLaneDetails(
  items: readonly TimelineAllDayItem[],
): ReadonlyMap<string, Details> {
  const keys = useMemo(
    () =>
      [
        ...new Set(
          items.flatMap((item) => {
            const basis = item.canonicalBasis;
            if (basis?.kind === 'scheduled-activity')
              return [`activity:${basis.activityRef}`];
            if (basis?.kind === 'scheduled-event')
              return [`event:${basis.eventRef}`];
            return [];
          }),
        ),
      ].sort(),
    [items],
  );
  const joined = keys.join('|');
  const [revision, setRevision] = useState(0);
  const [loaded, setLoaded] = useState<Readonly<{
    key: string;
    values: ReadonlyMap<string, Details>;
  }> | null>(null);

  useEffect(() => {
    const invalidate = () => {
      reads.clear();
      setRevision((value) => value + 1);
    };
    const stopPlanning = subscribeTemporalPlanningInvalidation(invalidate);
    const stopTimeline = subscribeTemporalTimelineInvalidation(invalidate);
    return () => {
      stopPlanning();
      stopTimeline();
    };
  }, []);

  useEffect(() => {
    let cancelled = false;
    void Promise.all(
      keys.map(async (key) => {
        try {
          return [key, await readDetails(key)] as const;
        } catch {
          return null;
        }
      }),
    ).then((results) => {
      if (!cancelled)
        setLoaded({
          key: joined,
          values: new Map(results.filter((value) => value !== null)),
        });
    });
    return () => {
      cancelled = true;
    };
  }, [joined, keys, revision]);
  return loaded?.key === joined ? loaded.values : new Map();
}
