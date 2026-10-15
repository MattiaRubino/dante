import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
  type ActivitySessionImpact,
} from '../../../temporal/remote-activity-inspector';
import { createRemoteActivityEditSettings } from '../../../temporal/remote-activity-edit-settings';
import {
  createRemoteActivityTimelinePlacement,
  type TimelineActivityPlacement,
  type TimelineUndoReceipt,
} from '../../../temporal/remote-activity-timeline-placement';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import { createRemoteTemporalHardDeletion, type TemporalHardDeletionPreview } from '../../../temporal/remote-temporal-hard-deletion';
import {
  createRemoteDraftVault,
  notifyDraftVaultUpdated,
} from '../../../temporal-create/application/remote-draft-vault';
import { draftVaultSnapshotFromDuplicate } from '../../../temporal-create/application/draft-vault-from-duplicate';
import {
  buildActivityDuplicateSeed,
  type ActivityDuplicateSeed,
} from '../../../temporal-create/application/activity-duplicate-seed';
import { TimelineInspectorIcon } from './timeline-inspector-icon';

export function ActivityInspectorActions({
  activityRef,
  subitemsCount = 0,
  onEdit,
  onDeleted,
  onDuplicate,
  toolbarTarget = null,
}: Readonly<{
  activityRef: string;
  subitemsCount?: number;
  onEdit: (profile: ActivityProfile) => void;
  onDeleted: () => void;
  onDuplicate: (seed: ActivityDuplicateSeed) => void;
  toolbarTarget?: HTMLElement | null;
}>) {
  const [source] = useState(createRemoteActivityInspector);
  const [settingsSource] = useState(createRemoteActivityEditSettings);
  const [recurringSource] = useState(createRemoteRecurringProfileEdit);
  const [hardDelete] = useState(createRemoteTemporalHardDeletion);
  const [timelinePlacement] = useState(createRemoteActivityTimelinePlacement);
  const [draftVault] = useState(createRemoteDraftVault);
  const [profile, setProfile] = useState<ActivityProfile | null>(null);
  const [confirming, setConfirming] = useState(false);
  const [deleteImpact, setDeleteImpact] = useState<ActivitySessionImpact | null>(null);
  const [recurringDeletePreview, setRecurringDeletePreview] = useState<
    readonly [TemporalHardDeletionPreview, TemporalHardDeletionPreview] | null
  >(null);
  const [confirmingVault, setConfirmingVault] = useState(false);
  const [removePlacement, setRemovePlacement] = useState<TimelineActivityPlacement | null>(null);
  const [removeImpact, setRemoveImpact] = useState<ActivitySessionImpact | null>(null);
  const [undoReceipt, setUndoReceipt] = useState<TimelineUndoReceipt | null>(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    void source
      .get(activityRef)
      .then((loaded) => {
        if (active) setProfile(loaded);
      })
      .catch((reason: unknown) => {
        if (active)
          setError(
            reason instanceof Error
              ? reason.message
              : 'Dettagli non disponibili.',
          );
      });
    return () => {
      active = false;
    };
  }, [activityRef, source]);

  async function action(task: () => Promise<void>) {
    setPending(true);
    setError('');
    try {
      await task();
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Operazione non riuscita.',
      );
    } finally {
      setPending(false);
    }
  }

  const toolbar = (
    <div className="timeline-activity-inspector__toolbar">
      <button
        type="button"
        aria-label="Modifica"
        title="Modifica"
        disabled={pending}
        onClick={() =>
          void action(async () => {
            onEdit(await source.get(activityRef));
          })
        }
      >
        {toolbarTarget ? <TimelineInspectorIcon name="edit" /> : 'Modifica'}
      </button>
      <button
        type="button"
        aria-label="Duplica"
        title="Duplica"
        disabled={pending}
        onClick={() =>
          void action(async () => {
            if (subitemsCount > 0) {
              throw new Error(
                'Questa attività contiene sotto-attività: la duplicazione fedele della struttura non è ancora disponibile.',
              );
            }
            const [savedProfile, settings, childCount, recurring] =
              await Promise.all([
                source.get(activityRef),
                settingsSource.load(activityRef),
                settingsSource.loadChildCount(activityRef),
                recurringSource.loadActivityContext(activityRef),
              ]);
            if (recurring !== null) {
              throw new Error(
                'La duplicazione fedele della ricorrenza richiede di copiare la sorgente: questa azione non la trasforma in una singola attività.',
              );
            }
            if (childCount !== 0) {
              throw new Error(
                'Questa attività contiene sotto-attività: la duplicazione fedele della struttura non è ancora disponibile.',
              );
            }
            onDuplicate(buildActivityDuplicateSeed(savedProfile, settings));
          })
        }
      >
        {toolbarTarget ? <TimelineInspectorIcon name="copy" /> : 'Duplica'}
      </button>
      <button
        type="button"
        aria-label="Sposta in Bozze"
        title="Sposta in Bozze"
        disabled={pending}
        onClick={() => setConfirmingVault(true)}
      >
        {toolbarTarget ? (
          <TimelineInspectorIcon name="copy" />
        ) : (
          'Sposta in Bozze'
        )}
      </button>
      <button
        type="button"
        aria-label="Rimuovi dalla Timeline"
        title="Rimuovi dalla Timeline"
        disabled={pending}
        onClick={() =>
          void action(async () => {
            const [placement, impact] = await Promise.all([
              timelinePlacement.current(activityRef),
              source.sessionImpact(activityRef),
            ]);
            setRemovePlacement(placement);
            setRemoveImpact(impact);
          })
        }
      >
        Rimuovi dalla Timeline
      </button>
      <button
        type="button"
        aria-label="Annulla rimozione Timeline"
        title="Annulla rimozione Timeline"
        disabled={pending}
        onClick={() =>
          void action(async () => {
            const receipts = await timelinePlacement.listUndo(activityRef);
            const latest = receipts[0];
            if (!latest) {
              throw new Error('Non sono presenti collocazioni ripristinabili.');
            }
            setUndoReceipt(latest);
          })
        }
      >
        Undo collocazione
      </button>
      <button
        type="button"
        aria-label="Elimina"
        title="Elimina"
        disabled={pending}
        onClick={() =>
          void action(async () => {
            const current = await source.sessionImpact(activityRef);
            const origin = await recurringSource.loadActivityContext(activityRef);
            const scopes =
              origin === null
                ? null
                : await Promise.all([
                    hardDelete.preview(activityRef, 'activity_instance'),
                    hardDelete.preview(activityRef, 'activity_series'),
                  ]);
            setRecurringDeletePreview(scopes);
            setDeleteImpact(current);
            setConfirming(true);
          })
        }
      >
        {toolbarTarget ? <TimelineInspectorIcon name="trash" /> : 'Elimina'}
      </button>
    </div>
  );

  return (
    <>
      {toolbarTarget ? createPortal(toolbar, toolbarTarget) : toolbar}
      {profile?.description || profile?.location ? (
        <div className="timeline-activity-inspector__details">
          {profile.description ? <p>{profile.description}</p> : null}
          {profile.location ? <p>Località: {profile.location}</p> : null}
        </div>
      ) : null}
      {error ? <p role="alert">{error}</p> : null}
      {removePlacement && removeImpact ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            Rimuovere questa Activity dalla Timeline senza eliminarla?
            Le Sessioni realmente registrate possono essere conservate o
            eliminate soltanto dopo una scelta esplicita.
          </p>
          {removeImpact.attempts.length !== 0 ? (
            <>
              <p>
                Sessioni registrate: {removeImpact.attempts.length}.
                «Mantieni» conserva i dati storici e i tempi reali.
              </p>
              <button
                type="button"
                disabled={pending}
                onClick={() =>
                  void action(async () => {
                    const receipt = await timelinePlacement.remove(
                      activityRef, removePlacement, 'keep',
                      removeImpact.fingerprint, removeImpact.attempts.length,
                    );
                    setUndoReceipt(receipt);
                    setRemovePlacement(null);
                    setRemoveImpact(null);
                  })
                }
              >
                Mantieni Sessioni e rimuovi dalla Timeline
              </button>
              <button
                type="button"
                disabled={pending}
                onClick={() =>
                  void action(async () => {
                    const receipt = await timelinePlacement.remove(
                      activityRef, removePlacement, 'delete',
                      removeImpact.fingerprint, removeImpact.attempts.length,
                    );
                    setUndoReceipt(receipt);
                    setRemovePlacement(null);
                    setRemoveImpact(null);
                  })
                }
              >
                Elimina Sessioni e rimuovi dalla Timeline
              </button>
            </>
          ) : (
            <button
              type="button"
              disabled={pending}
              onClick={() =>
                void action(async () => {
                  const receipt = await timelinePlacement.remove(
                    activityRef, removePlacement, null,
                    removeImpact.fingerprint, removeImpact.attempts.length,
                  );
                  setUndoReceipt(receipt);
                  setRemovePlacement(null);
                  setRemoveImpact(null);
                })
              }
            >
              Conferma rimozione dalla Timeline
            </button>
          )}
          <button
            type="button"
            disabled={pending}
            onClick={() => {
              setRemovePlacement(null);
              setRemoveImpact(null);
            }}
          >
            Annulla
          </button>
        </div>
      ) : null}
      {undoReceipt ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            Ripristinare la precedente collocazione come nuova revisione?
            La Schedule non verrà ripristinata se lo stato è cambiato.
          </p>
          <button
            type="button"
            disabled={pending}
            onClick={() =>
              void action(async () => {
                await timelinePlacement.undo(activityRef, undoReceipt);
                setUndoReceipt(null);
              })
            }
          >
            Conferma Undo della collocazione
          </button>
          <button
            type="button"
            disabled={pending}
            onClick={() => setUndoReceipt(null)}
          >
            Annulla
          </button>
        </div>
      ) : null}
      {confirmingVault ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            L'Attività verrà conservata come bozza non operativa e ritirata
            dalla Timeline. Le esecuzioni o i risultati registrati impediscono
            il ritiro: in quel caso l'originale rimane intatto.
          </p>
          <button
            type="button"
            disabled={pending}
            onClick={() =>
              void action(async () => {
                if (subitemsCount > 0) {
                  throw new Error('Sposta prima o completa le sotto-attività.');
                }
                const [savedProfile, settings, childCount, recurring, choice] =
                  await Promise.all([
                    source.get(activityRef),
                    settingsSource.load(activityRef),
                    settingsSource.loadChildCount(activityRef),
                    recurringSource.loadActivityContext(activityRef),
                    settingsSource.loadLifeAreaChoice(activityRef),
                  ]);
                if (recurring !== null || childCount !== 0) {
                  throw new Error(
                    'Questa attività contiene una serie o sotto-attività: ' +
                      'non possiamo ritirarle fingendo che siano una singola bozza.',
                  );
                }
                const selected =
                  settings.lifeAreaRef === null
                    ? undefined
                    : choice.options.find(
                        (area) => area.ref === settings.lifeAreaRef,
                      );
                if (settings.lifeAreaRef !== null && !selected) {
                  throw new Error(
                    'Life Area non più disponibile: ricarica la scheda.',
                  );
                }
                const areaDraft = selected
                  ? {
                      kind: 'existing' as const,
                      lifeAreaRef: selected.ref,
                      label: selected.name,
                      expectedRevision: selected.revision ?? 1,
                      colorCode: selected.colorCode ?? null,
                      colorChanged: false,
                    }
                  : undefined;
                const draft = await draftVault.save(
                  draftVaultSnapshotFromDuplicate(
                    buildActivityDuplicateSeed(savedProfile, settings),
                    areaDraft,
                  ),
                  {
                    draftRef: crypto.randomUUID(),
                    revision: null,
                    operationId: crypto.randomUUID(),
                  },
                );
                try {
                  await source.retire(activityRef);
                } catch (reason) {
                  try {
                    await draftVault.remove(draft);
                  } catch {
                    notifyDraftVaultUpdated();
                    throw new Error(
                      'Attività originale non ritirata. È stata conservata ' +
                        'anche una bozza: controlla Bozze prima di riprovare.',
                    );
                  }
                  throw reason;
                }
                notifyDraftVaultUpdated();
                onDeleted();
              })
            }
          >
            Conferma spostamento in Bozze
          </button>
          <button
            type="button"
            disabled={pending}
            onClick={() => setConfirmingVault(false)}
          >
            Annulla
          </button>
        </div>
      ) : null}
      {confirming && deleteImpact ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            Eliminare definitivamente questa attività, i suoi intervalli,
            promemoria, Sessioni e dati collegati? L'operazione non è
            reversibile.
          </p>
          {deleteImpact.attempts.length > 0 ? (
            <p>
              Verranno eliminate anche {deleteImpact.attempts.length}
              {' '}Sessioni registrate (
              {deleteImpact.attempts.map((attempt) => attempt.status).join(', ')}).
            </p>
          ) : null}
          {recurringDeletePreview ? (
            <>
              <p>
                Questa Activity appartiene a una Routine ricorrente.
                «Solo questa istanza» rimuove unicamente l’Activity selezionata
                e tutte le sue Sessioni e i suoi dati. «Tutta la serie»
                elimina definitivamente anche la Routine, tutte le altre
                istanze e i relativi dati, presenti e futuri.
              </p>
              <button
                type="button"
                disabled={pending}
                onClick={() =>
                  void action(async () => {
                    await hardDelete.deleteConfirmed(recurringDeletePreview[0]);
                    onDeleted();
                  })
                }
              >
                Solo questa istanza
              </button>
              <button
                type="button"
                disabled={pending}
                onClick={() =>
                  void action(async () => {
                    await hardDelete.deleteConfirmed(recurringDeletePreview[1]);
                    onDeleted();
                  })
                }
              >
                Tutta la serie
              </button>
            </>
          ) : (
            <button
              type="button"
              disabled={pending}
              onClick={() =>
                void action(async () => {
                  await source.deleteHard(activityRef, deleteImpact.fingerprint);
                  onDeleted();
                })
              }
            >
              Conferma eliminazione definitiva
            </button>
          )}
          <button
            type="button"
            disabled={pending}
            onClick={() => {
              setConfirming(false);
              setDeleteImpact(null);
              setRecurringDeletePreview(null);
            }}
          >
            Annulla
          </button>
        </div>
      ) : null}
    </>
  );
}
