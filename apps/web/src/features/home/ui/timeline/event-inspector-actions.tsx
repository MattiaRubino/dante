import { useState } from 'react';

import { createRemoteEventLifeAreaSettings, type EventLifeAreaChoice } from '../../../temporal/remote-event-life-area-settings';
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
  const [areaSource] = useState(createRemoteEventLifeAreaSettings);
  const [areaChoice, setAreaChoice] = useState<EventLifeAreaChoice | null>(null);
  const [areaSelection, setAreaSelection] = useState('');
  const [editingArea, setEditingArea] = useState(false);
  const [areaNotice, setAreaNotice] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const openAreaEditor = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const loaded = await areaSource.load(eventRef);
      setAreaChoice(loaded);
      setAreaSelection(loaded.currentRef ?? '');
      setEditingArea(true);
      setAreaNotice('');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Life Area Event non disponibile.');
    } finally {
      setBusy(false);
    }
  };

  const saveArea = async () => {
    if (!areaChoice || busy) return;
    setBusy(true);
    setError('');
    try {
      const saved = await areaSource.assign(
        eventRef, areaChoice, areaSelection || null, crypto.randomUUID(),
      );
      setAreaChoice(saved);
      setAreaSelection(saved.currentRef ?? '');
      setAreaNotice('Life Area Event aggiornata.');
      setEditingArea(false);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Salvataggio Life Area Event rifiutato.');
    } finally {
      setBusy(false);
    }
  };

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
      <button type="button" disabled={busy}
        onClick={() => editingArea ? setEditingArea(false) : void openAreaEditor()}>
        {editingArea ? 'Chiudi Life Area' : 'Modifica Life Area'}
      </button>
      {editingArea && areaChoice ? (
        <div className="timeline-activity-editor__fields">
          <label>
            Life Area Event
            <select disabled={busy} value={areaSelection}
              onChange={(event) => { setAreaSelection(event.target.value); setAreaNotice(''); }}>
              <option value="">Nessuna Life Area</option>
              {areaChoice.options.map((item) => (
                <option key={item.ref} value={item.ref}>{item.name}</option>
              ))}
            </select>
          </label>
          <button type="button" disabled={busy || (areaSelection || null) === areaChoice.currentRef}
            onClick={() => void saveArea()}>
            Salva Life Area Event
          </button>
        </div>
      ) : null}
      {areaNotice ? <p role="status">{areaNotice}</p> : null}
      {error ? <p role="alert">{error}</p> : null}
    </div>
  );
}
