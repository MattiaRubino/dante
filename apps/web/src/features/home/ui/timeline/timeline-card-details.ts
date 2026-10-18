import { useEffect, useState } from 'react';

import { createRemoteActivityEditSettings } from '../../../temporal/remote-activity-edit-settings';
import { createRemoteTemporalEventAgendaDataSource } from '../../../temporal/remote-event-agenda-data-source';
import { createRemoteRealityObjectiveDataSource } from '../../../temporal/remote-reality-objective-data-source';
import { subscribeTemporalTimelineInvalidation } from '../../../temporal/timeline-invalidation';
import type { TimelineEvent } from './model/timeline-types';

type CardDetails = Readonly<{
  lifeAreaRef: string | null;
  objectiveCount: number;
  agendaCount: number;
}>;
type LoadedCardDetails = Readonly<{ key: string; details: CardDetails }>;

/** Presentation data only; the Timeline Schedule remains the placement authority. */
export function useTimelineCardDetails(
  event: TimelineEvent,
): CardDetails | null {
  const basis = event.canonicalBasis;
  const kind = basis?.kind;
  const subjectRef =
    basis?.kind === 'scheduled-activity'
      ? basis.activityRef
      : basis?.kind === 'scheduled-event'
        ? basis.eventRef
        : basis?.kind === 'scheduled-occurrence' && basis.sourceKind === 'event'
          ? basis.sourceNativeRef
          : null;
  const key = subjectRef === null ? null : `${kind}:${subjectRef}`;
  const [loaded, setLoaded] = useState<LoadedCardDetails | null>(null);
  const [revision, setRevision] = useState(0);

  useEffect(
    () =>
      subscribeTemporalTimelineInvalidation(() => setRevision((n) => n + 1)),
    [],
  );

  useEffect(() => {
    if (!subjectRef || !key) return;
    let cancelled = false;
    const controller = new AbortController();
    const load = async (): Promise<CardDetails> => {
      if (kind === 'scheduled-activity') {
        const snapshot =
          await createRemoteActivityEditSettings().load(subjectRef);
        return {
          lifeAreaRef: snapshot.lifeAreaRef,
          objectiveCount: snapshot.objectives.length,
          agendaCount: 0,
        };
      }
      const [profile, objectives] = await Promise.all([
        createRemoteTemporalEventAgendaDataSource().loadEvent(
          subjectRef,
          controller.signal,
        ),
        createRemoteRealityObjectiveDataSource()
          .listObjectives('event', subjectRef)
          .catch(() => []),
      ]);
      return {
        lifeAreaRef: profile.lifeAreaRef ?? null,
        objectiveCount: objectives.length,
        agendaCount: profile.agendaParts.length,
      };
    };
    void load().then(
      (details) => {
        if (!cancelled) setLoaded({ key, details });
      },
      () => {
        if (!cancelled) setLoaded(null);
      },
    );
    return () => {
      cancelled = true;
      controller.abort();
    };
  }, [key, kind, subjectRef, revision]);

  return loaded?.key === key ? loaded.details : null;
}
