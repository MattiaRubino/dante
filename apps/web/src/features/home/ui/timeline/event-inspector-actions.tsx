import { useState } from 'react';
import { createPortal } from 'react-dom';

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
import {
  createRemoteTemporalHardDeletion,
  type TemporalHardDeletionPreview,
  type EventDeletionOccurrenceChoice,
} from '../../../temporal/remote-temporal-hard-deletion';
import { createRemoteTemporalOrganizationDataSource } from '../../../temporal/remote-organization';
import {
  createRemoteDraftVault,
  notifyDraftVaultUpdated,
} from '../../../temporal-create/application/remote-draft-vault';
import { draftVaultSnapshotFromDuplicate } from '../../../temporal-create/application/draft-vault-from-duplicate';
import { createRemoteTemporalEventAgendaDataSource } from '../../../temporal/remote-event-agenda-data-source';
import { createRemoteTemporalResponsibilityDataSource } from '../../../temporal/remote-responsibility-data-source';
import { systemTemporalIdFactory } from '../../../temporal/model';
import type { ActivityDuplicateSeed } from '../../../temporal-create/application/activity-duplicate-seed';
import { buildEventDuplicateSeed } from '../../../temporal-create/application/event-duplicate-seed';
import type { TimelineCanonicalSchedulePlacement } from './model/timeline-types';
import { TimelineInspectorIcon } from './timeline-inspector-icon';

export function EventInspectorActions({
  eventRef,
  placement,
  occurrenceRef = null,
  onDeleted,
  onDuplicate,
  toolbarTarget = null,
}: Readonly<{
  eventRef: string;
  placement: TimelineCanonicalSchedulePlacement;
  occurrenceRef?: string | null;
  onDeleted?: () => void;
  onDuplicate: (seed: ActivityDuplicateSeed) => void;
  toolbarTarget?: HTMLElement | null;
}>) {
  const [eventSource] = useState(createRemoteTemporalEventAgendaDataSource);
  const [participationSource] = useState(
    createRemoteTemporalResponsibilityDataSource,
  );
  const [recurrenceGuard] = useState(createRemoteEventRecurrenceGuard);
  const [hardDelete] = useState(createRemoteTemporalHardDeletion);
  const [deletePreviews, setDeletePreviews] = useState<
    readonly TemporalHardDeletionPreview[] | null
  >(null);
  const [deletionChoices, setDeletionChoices] = useState<
    readonly EventDeletionOccurrenceChoice[]
  >([]);
  const [selectedDeletionOccurrence, setSelectedDeletionOccurrence] = useState('');
  const [profileSource] = useState(createRemoteEventProfileDataSource);
  const [areaSource] = useState(createRemoteEventLifeAreaSettings);
  const [organizationSource] = useState(
    createRemoteTemporalOrganizationDataSource,
  );
  const [draftVault] = useState(createRemoteDraftVault);
  const [profile, setProfile] = useState<TemporalEventDetailRecord | null>(
    null,
  );
  const [profileDraft, setProfileDraft] = useState<EventProfileDraft | null>(
    null,
  );
  const [areaChoice, setAreaChoice] = useState<EventLifeAreaChoice | null>(
    null,
  );
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
      setError(
        reason instanceof Error
          ? reason.message
          : 'Dettagli Event non disponibili.',
      );
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
      if (
        changed &&
        !window.confirm('Scartare le modifiche Event non salvate?')
      )
        return;
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
        eventRef,
        profile,
        normalized,
        systemTemporalIdFactory.operationId(),
      );
      setProfile(saved);
      setProfileDraft(null);
      setEditingProfile(false);
      setProfileNotice('Metadati Event aggiornati.');
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Modifica Event rifiutata.',
      );
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
      setError(
        reason instanceof Error
          ? reason.message
          : 'Life Area Event non disponibile.',
      );
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
        eventRef,
        areaChoice,
        areaSelection || null,
        systemTemporalIdFactory.operationId(),
      );
      setAreaChoice(saved);
      setAreaSelection(saved.currentRef ?? '');
      setEditingArea(false);
      setAreaNotice('Life Area Event aggiornata.');
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Salvataggio Life Area Event rifiutato.',
      );
    } finally {
      setBusy(false);
    }
  };

  const duplicate = async (intoVault = false) => {
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
      const labels = new Map(
        referents.map((row) => [row.personRef, row.displayLabel]),
      );
      const expectedParticipants = participants
        .filter((row) => row.requirementCode !== null)
        .map((row) => {
          const label = row.participantIsSelf
            ? 'Io'
            : labels.get(row.participantPersonRef);
          if (!label || row.requirementCode === null) {
            throw new Error(
              'Impossibile duplicare: un partecipante non è più disponibile.',
            );
          }
          return {
            personRef: row.participantPersonRef,
            displayLabel: label,
            requirementCode: row.requirementCode,
          };
        });
      const seed = buildEventDuplicateSeed(
        event,
        placement,
        expectedParticipants,
      );
      if (!intoVault) {
        onDuplicate(seed);
      } else {
        const organization = await organizationSource.load();
        const area =
          event.lifeAreaRef === null || event.lifeAreaRef === undefined
            ? undefined
            : organization.areas.find((row) => row.ref === event.lifeAreaRef);
        if (event.lifeAreaRef && !area) {
          throw new Error(
            'Life Area Event non disponibile: la bozza non è stata salvata.',
          );
        }
        const selected = area
          ? {
              kind: 'existing' as const,
              lifeAreaRef: area.ref,
              label: area.name,
              expectedRevision: area.revision,
              colorCode: area.colorCode,
              colorChanged: false,
            }
          : undefined;
        await draftVault.save(draftVaultSnapshotFromDuplicate(seed, selected), {
          draftRef: crypto.randomUUID(),
          revision: null,
          operationId: crypto.randomUUID(),
        });
        notifyDraftVaultUpdated();
        setProfileNotice(
          'Copia salvata nelle Bozze. L’Evento originale rimane attivo.',
        );
      }
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Impossibile preparare una duplicazione fedele dell’evento.',
      );
    } finally {
      setBusy(false);
    }
  };


  const confirmDeletion = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const recurring = await recurrenceGuard.isRecurring(eventRef);
      if (!recurring) {
        setDeletionChoices([]);
        setSelectedDeletionOccurrence('');
        setDeletePreviews([await hardDelete.preview(eventRef, 'event_once')]);
      } else {
        const [series, choices] = await Promise.all([
          hardDelete.preview(eventRef, 'event_series'),
          hardDelete.eventOccurrences(eventRef),
        ]);
        const selected = occurrenceRef !== null &&
          choices.some((choice) => choice.occurrenceRef === occurrenceRef)
          ? occurrenceRef
          : '';
        setDeletionChoices(choices);
        setSelectedDeletionOccurrence(selected);
        const instance =
          selected === ''
            ? null
            : await hardDelete.preview(selected, 'event_instance');
        setDeletePreviews(instance === null ? [series] : [instance, series]);
      }
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Impossibile verificare l’evento da eliminare.',
      );
    } finally {
      setBusy(false);
    }
  };

  const acceptDeletion = async (preview: TemporalHardDeletionPreview) => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      await hardDelete.deleteConfirmed(preview);
      if (onDeleted) onDeleted();
      else window.location.reload();
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Eliminazione Event rifiutata.',
      );
    } finally {
      setBusy(false);
    }
  };

  const toolbar = (
    <div className="timeline-activity-inspector__toolbar">
      <button
        type="button"
        disabled={busy}
        aria-label="Modifica"
        title="Modifica"
        onClick={() =>
          editingProfile ? cancelProfile() : void openProfileEditor()
        }
      >
        {toolbarTarget ? (
          <TimelineInspectorIcon name="edit" />
        ) : editingProfile ? (
          'Chiudi modifica Event'
        ) : (
          'Modifica'
        )}
      </button>
      <button
        type="button"
        disabled={busy}
        aria-label="Duplica"
        title="Duplica"
        onClick={() => void duplicate()}
      >
        {toolbarTarget ? (
          <TimelineInspectorIcon name="copy" />
        ) : busy ? (
          'Preparazione…'
        ) : (
          'Duplica'
        )}
      </button>
      <button
        type="button"
        disabled={busy}
        aria-label="Copia in Bozze"
        title="Copia in Bozze"
        onClick={() => void duplicate(true)}
      >
        {toolbarTarget ? (
          <TimelineInspectorIcon name="copy" />
        ) : (
          'Copia in Bozze'
        )}
      </button>
      <button
        type="button"
        disabled={busy}
        aria-label="Elimina Event"
        title="Elimina Event"
        onClick={() => void confirmDeletion()}
      >
        {toolbarTarget ? (
          <TimelineInspectorIcon name="trash" />
        ) : (
          'Elimina'
        )}
      </button>
    </div>
  );

  return (
    <div className="timeline-activity-inspector__actions">
      {toolbarTarget ? createPortal(toolbar, toolbarTarget) : toolbar}
      {!toolbarTarget || editingProfile || editingArea ? (
        <button
          type="button"
          disabled={busy}
          onClick={() =>
            editingArea ? setEditingArea(false) : void openAreaEditor()
          }
        >
          {editingArea ? 'Chiudi Life Area' : 'Modifica Life Area'}
        </button>
      ) : null}

      {editingProfile && profileDraft && profile ? (
        <div
          className="timeline-activity-editor__fields"
          aria-label="Modifica profilo Event"
        >
          <label>
            Titolo Event
            <input
              disabled={busy}
              maxLength={300}
              value={profileDraft.title}
              onChange={(event) => {
                const title = event.currentTarget.value;
                setProfileDraft((draft) => draft && { ...draft, title });
              }}
            />
          </label>
          <label>
            Descrizione Event
            <textarea
              disabled={busy}
              value={profileDraft.description ?? ''}
              onChange={(event) => {
                const description = event.currentTarget.value || null;
                setProfileDraft((draft) => draft && { ...draft, description });
              }}
            />
          </label>
          <label>
            Località Event
            <input
              disabled={busy}
              value={profileDraft.location ?? ''}
              onChange={(event) => {
                const location = event.currentTarget.value || null;
                setProfileDraft((draft) => draft && { ...draft, location });
              }}
            />
          </label>
          <label>
            Colore Event (#RRGGBB)
            <input
              disabled={busy}
              maxLength={7}
              value={profileDraft.colorCode ?? ''}
              onChange={(event) => {
                const colorCode = event.currentTarget.value || null;
                setProfileDraft((draft) => draft && { ...draft, colorCode });
              }}
            />
          </label>
          <button
            type="button"
            disabled={busy || !profileDraft.title.trim()}
            onClick={() => void saveProfile()}
          >
            Salva metadati Event
          </button>
          <button type="button" disabled={busy} onClick={cancelProfile}>
            Annulla
          </button>
        </div>
      ) : null}
      {editingArea && areaChoice ? (
        <div className="timeline-activity-editor__fields">
          <label>
            Life Area Event
            <select
              disabled={busy}
              value={areaSelection}
              onChange={(event) => {
                setAreaSelection(event.target.value);
                setAreaNotice('');
              }}
            >
              <option value="">Nessuna Life Area</option>
              {areaChoice.options.map((row) => (
                <option key={row.ref} value={row.ref}>
                  {row.name}
                </option>
              ))}
            </select>
          </label>
          <button
            type="button"
            disabled={busy || (areaSelection || null) === areaChoice.currentRef}
            onClick={() => void saveArea()}
          >
            Salva Life Area Event
          </button>
        </div>
      ) : null}
      {profileNotice ? <p role="status">{profileNotice}</p> : null}
      {areaNotice ? <p role="status">{areaNotice}</p> : null}
      {deletePreviews ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            L’eliminazione è definitiva e comprende Schedule, promemoria,
            Objective e dati storici collegati all’Evento o all’istanza.
            La rimozione dalla Timeline è un’operazione diversa.
          </p>
          {deletionChoices.length > 0 ? (
            <label>
              Istanza Event da eliminare
              <select
                value={selectedDeletionOccurrence}
                disabled={busy}
                onChange={(event) => {
                  const selected = event.currentTarget.value;
                  void (async () => {
                    setBusy(true);
                    setError('');
                    try {
                      const series = deletePreviews.find(
                        (preview) => preview.scope === 'event_series',
                      );
                      if (!series) {
                        throw new Error('Anteprima della serie non disponibile.');
                      }
                      const instance = selected
                        ? await hardDelete.preview(selected, 'event_instance')
                        : null;
                      setSelectedDeletionOccurrence(selected);
                      setDeletePreviews(instance ? [instance, series] : [series]);
                    } catch (reason) {
                      setError(
                        reason instanceof Error
                          ? reason.message
                          : 'Impossibile selezionare l’istanza.',
                      );
                    } finally {
                      setBusy(false);
                    }
                  })();
                }}
              >
                <option value="">Seleziona una Occurrence specifica</option>
                {deletionChoices.map((choice) => (
                  <option key={choice.occurrenceRef} value={choice.occurrenceRef}>
                    {choice.displayLabel}
                  </option>
                ))}
              </select>
            </label>
          ) : null}
          {deletePreviews.map((preview) => (
            <button
              type="button"
              key={preview.scope}
              disabled={busy}
              onClick={() => void acceptDeletion(preview)}
            >
              {preview.scope === 'event_once'
                ? 'Conferma eliminazione definitiva'
                : preview.scope === 'event_instance'
                  ? 'Solo questa istanza'
                  : 'Tutta la serie'}
            </button>
          ))}
          {deletionChoices.length !== 0 && selectedDeletionOccurrence === '' ? (
            <p>
              Per «Solo questa istanza» seleziona la data dell’Occurrence.
              «Tutta la serie» elimina anche tutte le altre istanze.
            </p>
          ) : null}
          <button
            type="button"
            disabled={busy}
            onClick={() => {
              setDeletePreviews(null);
              setDeletionChoices([]);
              setSelectedDeletionOccurrence('');
            }}
          >
            Annulla
          </button>
        </div>
      ) : null}
      {error ? <p role="alert">{error}</p> : null}
    </div>
  );
}
