import { useState } from 'react';

import { createRemoteTemporalEventAgendaDataSource } from '../../../temporal/remote-event-agenda-data-source';
import { createRemoteTemporalResponsibilityDataSource } from '../../../temporal/remote-responsibility-data-source';
import { buildEventDuplicateSeed } from '../../../temporal-create/application/event-duplicate-seed';
import type { ActivityDuplicateSeed } from '../../../temporal-create/application/activity-duplicate-seed';
import type { TimelineCanonicalSchedulePlacement } from './model/timeline-types';

export function EventInspectorActions({
  eventRef,
  placement,
  onDuplicate,
}: Readonly<{
  eventRef: string;
  placement: TimelineCanonicalSchedulePlacement;
  onDuplicate: (seed: ActivityDuplicateSeed) => void;
}>) {
  const [eventSource] = useState(createRemoteTemporalEventAgendaDataSource);
  const [participationSource] = useState(createRemoteTemporalResponsibilityDataSource);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const duplicate = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const [event, participants, referents] = await Promise.all([
        eventSource.loadEvent(eventRef),
        participationSource.listExpectedParticipation(eventRef),
        participationSource.listPersonReferents(),
      ]);
      const labels = new Map(referents.map((ref) => [ref.personRef, ref.displayLabel]));
      const expectedParticipants = participants
        .filter((entry) => entry.requirementCode !== null)
        .map((entry) => {
          const label = entry.participantIsSelf
            ? 'Io'
            : labels.get(entry.participantPersonRef);
          if (!label || entry.requirementCode === null) {
            throw new Error(
              'Impossibile duplicare: un partecipante non è più disponibile.',
            );
          }
          return {
            personRef: entry.participantPersonRef,
            displayLabel: label,
            requirementCode: entry.requirementCode,
          };
        });
      // Do not assign a new Event identity until Create is explicitly accepted.
      onDuplicate(buildEventDuplicateSeed(event, placement, expectedParticipants));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message
        : 'Impossibile preparare una duplicazione fedele dell’evento.');
    } finally {
      setBusy(false);
    }
  };
  return (
    <div className="timeline-activity-inspector__actions">
      <button type="button" disabled={busy} onClick={() => void duplicate()}>
        {busy ? 'Preparazione…' : 'Duplica'}
      </button>
      {error ? <p role="alert">{error}</p> : null}
    </div>
  );
}
