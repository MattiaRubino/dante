import { useEffect, useState } from 'react';

import { createRemoteTemporalResponsibilityDataSource } from '../../../temporal/remote-responsibility-data-source';
import { subscribeTemporalTimelineInvalidation } from '../../../temporal/timeline-invalidation';

type Participant = Readonly<{
  personRef: string;
  label: string;
  requirement: 'required' | 'optional';
}>;

export function TimelineEventParticipation({
  eventRef,
}: Readonly<{ eventRef: string }>) {
  const [snapshot, setSnapshot] = useState<Readonly<{
    key: string;
    participants: readonly Participant[];
  }> | null>(null);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let active = true;
    const source = createRemoteTemporalResponsibilityDataSource(
      globalThis.fetch,
    );
    const read = () => {
      void Promise.all([
        source.listExpectedParticipation(eventRef),
        source.listPersonReferents(),
      ])
        .then(([participation, people]) => {
          if (!active) return;
          const labels = new Map(
            people.map((person) => [person.personRef, person.displayLabel]),
          );
          setSnapshot({
            key: eventRef,
            participants: participation.flatMap((row) => {
              if (row.requirementCode === null) return [];
              return [
                {
                  personRef: row.participantPersonRef,
                  label: row.participantIsSelf
                    ? 'Io'
                    : (labels.get(row.participantPersonRef) ??
                      'Persona non disponibile'),
                  requirement: row.requirementCode,
                },
              ];
            }),
          });
          setFailed(false);
        })
        .catch(() => {
          if (active) setFailed(true);
        });
    };
    read();
    const unsubscribe = subscribeTemporalTimelineInvalidation(read);
    return () => {
      active = false;
      unsubscribe();
    };
  }, [eventRef]);

  const participants = snapshot?.key === eventRef ? snapshot.participants : [];
  if (!failed && participants.length === 0) return null;
  return (
    <section
      className="timeline-event-modal__participation"
      aria-label="Partecipanti"
    >
      <h4>Partecipanti</h4>
      {failed ? <p role="alert">Partecipanti non disponibili.</p> : null}
      {participants.map((row) => (
        <div key={row.personRef} className="timeline-event-modal__participant">
          <span>{row.label}</span>
          <span>
            {row.requirement === 'required' ? 'Richiesto' : 'Opzionale'}
          </span>
        </div>
      ))}
    </section>
  );
}
