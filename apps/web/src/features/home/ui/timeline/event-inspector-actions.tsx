import { useState } from 'react';

import {
  createRemoteEventProfileDataSource,
  type EventProfileDraft,
} from '../../../temporal/remote-event-profile-data-source';
import type { TemporalEventDetailRecord } from '../../../temporal/event-data-source';
import { createRemoteEventLifeAreaSettings, type EventLifeAreaChoice } from '../../../temporal/remote-event-life-area-settings';
import { createRemoteEventProfileDataSource, type EventProfileDraft } from '../../../temporal/remote-event-profile-data-source';
import type { TemporalEventDetailRecord } from '../../../temporal/event-data-source';
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
  const [profileSource] = useState(createRemoteEventProfileDataSource);
  const [profile, setProfile] = useState<TemporalEventDetailRecord | null>(null);
  const [profileDraft, setProfileDraft] = useState<EventProfileDraft | null>(null);
  const [editingProfile, setEditingProfile] = useState(false);
  const [profileNotice, setProfileNotice] = useState('');
  const [profileSource] = useState(createRemoteEventProfileDataSource);
  const [profile, setProfile] = useState<TemporalEventDetailRecord | null>(null);
  const [profileDraft, setProfileDraft] = useState<EventProfileDraft | null>(null);
  const [editingProfile, setEditingProfile] = useState(false);
  const [areaChoice, setAreaChoice] = useState<EventLifeAreaChoice | null>(null);
  const [areaSelection, setAreaSelection] = useState('');
  const [editingArea, setEditingArea] = useState(false);
  const [areaNotice, setAreaNotice] = useState('');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const openProfileEditor = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const saved = await profileSource.load(eventRef);
      if (saved.profileRevision === undefined) {
        throw new Error('Revisione del profilo Event non disponibile.');
      }
      setProfile(saved);
      setProfileDraft({
        title: saved.title,
        description: saved.description ?? null,
        location: saved.location ?? null,
        colorCode: saved.colorCode ?? null,
      });
      setEditingProfile(true);
      setProfileNotice('');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Dettagli Event non disponibili.');
    } finally {
      setBusy(false);
    }
  };

  const saveProfile = async () => {
    if (busy || !profile || !profileDraft) return;
    setBusy(true);
    setError('');
    try {
      const normalized: EventProfileDraft = {
        title: profileDraft.title.trim(),
        description: profileDraft.description?.trim() || null,
        location: profileDraft.location?.trim() || null,
        colorCode: profileDraft.colorCode?.trim().toUpperCase() || null,
      };
      const accepted = await profileSource.revise(
        eventRef, profile, normalized, crypto.randomUUID(),
      );
      setProfile(accepted);
      setProfileDraft(null);
      setEditingProfile(false);
      setProfileNotice('Metadati Event aggiornati.');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Modifica Event rifiutata.');
    } finally {
      setBusy(false);
    }
  };

  const cancelProfile = () => {
    if (profile && profileDraft) {
      const changed = profileDraft.title !== profile.title ||
        (profileDraft.description ?? '') !== (profile.description ?? '') ||
        (profileDraft.location ?? '') !== (profile.location ?? '') ||
        (profileDraft.colorCode ?? '') !== (profile.colorCode ?? '');
      if (changed && !window.confirm('Scartare le modifiche Event non salvate?')) return;
    }
    setProfileDraft(null);
    setEditingProfile(false);
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

  const openProfileEditor = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const loaded = await profileSource.load(eventRef);
      setProfile(loaded);
      setProfileDraft({
        title: loaded.title,
        description: loaded.description ?? null,
        location: loaded.location ?? null,
        colorCode: loaded.colorCode ?? null,
      });
      setEditingProfile(true);
      setAreaNotice('');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Profilo Event non disponibile.');
    } finally {
      setBusy(false);
    }
  };

  const saveProfile = async () => {
    if (!profile || !profileDraft || busy) return;
    setBusy(true);
    setError('');
    try {
      const saved = await profileSource.revise(
        eventRef, profile, profileDraft, crypto.randomUUID(),
      );
      setProfile(saved);
      setEditingProfile(false);
      setAreaNotice('Profilo Event aggiornato.');
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Modifica Event rifiutata.');
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
        onClick={() => editingProfile ? setEditingProfile(false) : void openProfileEditor()}>
        {editingProfile ? 'Chiudi dettagli Event' : 'Modifica dettagli'}
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
        <div className="timeline-activity-editor__fields">
          <label>
            Titolo Event
            <input value={profileDraft.title} maxLength={300} disabled={busy}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, title: event.target.value })} />
          </label>
          <label>
            Descrizione Event
            <textarea value={profileDraft.description ?? ''} disabled={busy}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, description: event.target.value.trim() || null })} />
          </label>
          <label>
            Località Event
            <input value={profileDraft.location ?? ''} disabled={busy}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, location: event.target.value.trim() || null })} />
          </label>
          <label>
            Colore Event
            <input value={profileDraft.colorCode ?? ''} disabled={busy}
              placeholder="#AABBCC" maxLength={7}
              onChange={(event) => setProfileDraft((draft) =>
                draft && { ...draft, colorCode: event.target.value.toUpperCase() || null })} />
          </label>
          <button type="button" disabled={busy || !profileDraft.title.trim() ||
            (profileDraft.title === profile.title &&
             profileDraft.description === (profile.description ?? null) &&
             profileDraft.location === (profile.location ?? null) &&
             profileDraft.colorCode === (profile.colorCode ?? null))}
            onClick={() => void saveProfile()}>
            Salva dettagli Event
          </button>
        </div>
      ) : null}
      {editingProfile && profileDraft ? (
        <div className="timeline-activity-editor__fields" aria-label="Modifica profilo Event">
          <label>
            Titolo Event
            <input disabled={busy} value={profileDraft.title}
              onChange={(e) => setProfileDraft((previous) =>
                previous ? { ...previous, title: e.target.value } : previous)} />
          </label>
          <label>
            Descrizione Event
            <textarea disabled={busy} value={profileDraft.description ?? ''}
              onChange={(e) => setProfileDraft((previous) =>
                previous ? { ...previous, description: e.target.value } : previous)} />
          </label>
          <label>
            Località Event
            <input disabled={busy} value={profileDraft.location ?? ''}
              onChange={(e) => setProfileDraft((previous) =>
                previous ? { ...previous, location: e.target.value } : previous)} />
          </label>
          <label>
            Colore Event (#RRGGBB)
            <input disabled={busy} value={profileDraft.colorCode ?? ''}
              onChange={(e) => setProfileDraft((previous) =>
                previous ? { ...previous, colorCode: e.target.value } : previous)} />
          </label>
          <button type="button" disabled={busy} onClick={() => void saveProfile()}>
            Salva metadati Event
          </button>
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
      {profileNotice ? <p role="status">{profileNotice}</p> : null}
      {areaNotice ? <p role="status">{areaNotice}</p> : null}
      {error ? <p role="alert">{error}</p> : null}
    </div>
  );
}
