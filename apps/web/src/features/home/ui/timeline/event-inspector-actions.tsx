import { useState } from 'react';

import type { TemporalEventDetailRecord } from '../../../temporal/event-data-source';
import {
  createRemoteEventLifeAreaSettings,
  type EventLifeAreaChoice,
} from '../../../temporal/remote-event-life-area-settings';
import {
  createRemoteEventProfileDataSource,
  type EventProfileDraft,
} from '../../../temporal/remote-event-profile-data-source';
import { createRemoteEventRecurrenceGuard } from '../../../temporal/remote-event-recurrence-guard';
import { createRemoteTemporalEventAgendaDataSource } from '../../../temporal/remote-event-agenda-data-source';
import { createRemoteTemporalResponsibilityDataSource } from '../../../temporal/remote-responsibility-data-source';
import { systemTemporalIdFactory } from '../../../temporal/model';
import type { ActivityDuplicateSeed } from '../../../temporal-create/application/activity-duplicate-seed';
import { buildEventDuplicateSeed } from '../../../temporal-create/application/event-duplicate-seed';
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
  const [recurrenceGuard] = useState(createRemoteEventRecurrenceGuard);
  const [profileSource] = useState(createRemoteEventProfileDataSource);
  const [areaSource] = useState(createRemoteEventLifeAreaSettings);
  const [profile, setProfile] = useState<TemporalEventDetailRecord | null>(null);
  const [profileDraft, setProfileDraft] = useState<EventProfileDraft | null>(null);
  const [areaChoice, setAreaChoice] = useState<EventLifeAreaChoice | null>(null);
  const [areaSelection, setAreaSelection] = useState('');
  const [editingProfile, setEditingProfile] = useState(false);
  const [editingArea, setEditingArea] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [profileNotice, setProfileNotice] = useState('');
  const [areaNotice, setAreaNotice] = useState('');

  const openProfileEditor = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const loaded = await profileSource.load(eventRef);
      if (loaded.profileRevision === undefined) {
        throw new Error('Revisione del profilo Event non disponibile.');
      }
      setProfile(loaded);
      setProfileDraft({
        title: loaded.title,
        description: loaded.description ?? null,
        location: loaded.location ?? null,
        colorCode: loaded.colorCode ?? null,
      });
      setEditingProfile(true);
      setProfileNotice('');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Dettagli Event non disponibili.');
    } finally {
      setBusy(false);
    }
  };

  const cancelProfile = () => {
    if (profile && profileDraft) {
      const changed =
        profileDraft.title !== profile.title ||
        (profileDraft.description ?? '') !== (profile.description ?? '') ||
        (profileDraft.location ?? '') !== (profile.location ?? '') ||
        (profileDraft.colorCode ?? '') !== (profile.colorCode ?? '');
      if (changed && !window.confirm('Scartare le modifiche Event non salvate?')) return;
    }
    setProfileDraft(null);
    setEditingProfile(false);
  };

  const saveProfile = async () => {
    if (!profile || !profileDraft || busy) return;
    setBusy(true);
    setError('');
    try {
      const normalized: EventProfileDraft = {
        title: profileDraft.title.trim(),
        description: profileDraft.description?.trim() || null,
        location: profileDraft.location?.trim() || null,
        colorCode: profileDraft.colorCode?.trim().toUpperCase() || null,
      };
      const saved = await profileSource.revise(
        eventRef, profile, normalized, systemTemporalIdFactory.operationId(),
      );
      setProfile(saved);
      setProfileDraft(null);
      setEditingProfile(false);
      setProfileNotice('Metadati Event aggiornati.');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Modifica Event rifiutata.');
    } finally {
      setBusy(false);
    }
  };

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
        eventRef, areaChoice, areaSelection || null, systemTemporalIdFactory.operationId(),
      );
      setAreaChoice(saved);
      setAreaSelection(saved.currentRef ?? '');
      setEditingArea(false);
      setAreaNotice('Life Area Event aggiornata.');
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
      const [event, participants, referents, recurring] = await Promise.all([
        eventSource.loadEvent(eventRef),
        participationSource.listExpectedParticipation(eventRef),
        participationSource.listPersonReferents(),
        recurrenceGuard.isRecurring(eventRef),
      ]);
      if (recurring) {
        throw new Error(
          'Questo evento è una sorgente ricorrente: Duplica non può trasformarla in un singolo evento.',
        );
      }
      const labels = new Map(referents.map((row) => [row.personRef, row.displayLabel]));
      const expectedParticipants = participants
        .filter((row) => row.requirementCode !== null)
        .map((row) => {
          const label = row.participantIsSelf ? 'Io' : labels.get(row.participantPersonRef);
          if (!label || row.requirementCode === null) {
            throw new Error('Impossibile duplicare: un partecipante non è più disponibile.');
          }
          return {
            personRef: row.participantPersonRef,
            displayLabel: label,
            requirementCode: row.requirementCode,
          };
        });
      onDuplicate(buildEventDuplicateSeed(event, placement, expectedParticipants));
    } catch (reason) {
      setError(reason instanceof Error
        ? reason.message : 'Impossibile preparare una duplicazione fedele dell’evento.');
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
        onClick={() => editingProfile ? cancelProfile() : void openProfileEditor()}>
        {editingProfile ? 'Chiudi modifica Event' : 'Modifica'}
      </button>
      <button type="button" disabled={busy}
        onClick={() => editingArea ? setEditingArea(false) : void openAreaEditor()}>
        {editingArea ? 'Chiudi Life Area' : 'Modifica Life Area'}
      </button>

      {editingProfile && profileDraft && profile ? (
        <div className="timeline-activity-editor__fields" aria-label="Modifica profilo Event">
          <label>
            Titolo Event
            <input disabled={busy} maxLength={300} value={profileDraft.title}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, title: event.target.value })} />
          </label>
          <label>
            Descrizione Event
            <textarea disabled={busy} value={profileDraft.description ?? ''}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, description: event.target.value || null })} />
          </label>
          <label>
            Località Event
            <input disabled={busy} value={profileDraft.location ?? ''}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, location: event.target.value || null })} />
          </label>
          <label>
            Colore Event (#RRGGBB)
            <input disabled={busy} maxLength={7} value={profileDraft.colorCode ?? ''}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, colorCode: event.target.value || null })} />
          </label>
          <button type="button" disabled={busy || !profileDraft.title.trim()}
            onClick={() => void saveProfile()}>Salva metadati Event</button>
          <button type="button" disabled={busy} onClick={cancelProfile}>Annulla</button>
        </div>
      ) : null}
      {editingArea && areaChoice ? (
        <div className="timeline-activity-editor__fields">
          <label>
            Life Area Event
            <select disabled={busy} value={areaSelection}
              onChange={(event) => { setAreaSelection(event.target.value); setAreaNotice(''); }}>
              <option value="">Nessuna Life Area</option>
              {areaChoice.options.map((row) => (
                <option key={row.ref} value={row.ref}>{row.name}</option>
              ))}
            </select>
          </label>
          <button type="button"
            disabled={busy || (areaSelection || null) === areaChoice.currentRef}
            onClick={() => void saveArea()}>
            Salva Life Area Event
          </button>
        </div>
      ) : null}
      {profileNotice ? <p role="status">{profileNotice}</p> : null}
      {areaNotice ? <p role="status">{areaNotice}</p> : null}
      {error ? <p role="alert">{error}</p> : null}
    </div>
  );
}
