import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
  type ActivitySessionImpact,
} from '../../../temporal/remote-activity-inspector';
import { createRemoteActivityEditSettings } from '../../../temporal/remote-activity-edit-settings';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import type { RecurringProfileEditScope } from '../../../temporal/remote-recurring-profile-edit';
import {
  createRemoteTemporalHardDeletion,
  type TemporalHardDeletionPreview,
} from '../../../temporal/remote-temporal-hard-deletion';
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
  onEdit: (profile: ActivityProfile, scope: RecurringProfileEditScope) => void;
  onDeleted: () => void;
  onDuplicate: (seed: ActivityDuplicateSeed) => void;
  toolbarTarget?: HTMLElement | null;
}>) {
  const [source] = useState(createRemoteActivityInspector);
  const [settingsSource] = useState(createRemoteActivityEditSettings);
  const [recurringSource] = useState(createRemoteRecurringProfileEdit);
  const [hardDelete] = useState(createRemoteTemporalHardDeletion);
  const [draftVault] = useState(createRemoteDraftVault);
  const [profile, setProfile] = useState<ActivityProfile | null>(null);
  const [editChoice, setEditChoice] = useState<{
    profile: ActivityProfile;
    selectedHasFacts: boolean;
  } | null>(null);
  const [confirming, setConfirming] = useState(false);
  const [deleteImpact, setDeleteImpact] =
    useState<ActivitySessionImpact | null>(null);
  const [recurringDeletePreview, setRecurringDeletePreview] = useState<
    readonly [TemporalHardDeletionPreview, TemporalHardDeletionPreview] | null
  >(null);
  const [confirmingVault, setConfirmingVault] = useState(false);
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
            const [loaded, recurring] = await Promise.all([
              source.get(activityRef),
              recurringSource.loadActivityContext(activityRef),
            ]);
            if (!recurring) {
              onEdit(loaded, 'only_this');
              return;
            }
            const preview = await recurringSource.loadPreview(
              recurring,
              'only_this',
            );
            setEditChoice({
              profile: loaded,
              selectedHasFacts: preview.selectedProtection === 'registration',
            });
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
          <TimelineInspectorIcon name="vault" />
        ) : (
          'Sposta in Bozze'
        )}
      </button>
      <button
        type="button"
        aria-label="Elimina"
        title="Elimina"
        disabled={pending}
        onClick={() =>
          void action(async () => {
            const current = await source.sessionImpact(activityRef);
            const origin =
              await recurringSource.loadActivityContext(activityRef);
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
      {editChoice ? (
        <div
          className="timeline-activity-inspector__confirmation"
          role="group"
          aria-label="Ambito modifica ricorrenza"
        >
          <p>
            Questa attività fa parte di una ricorrenza. Quali istanze vuoi
            modificare?
          </p>
          <button
            type="button"
            disabled={pending}
            onClick={() => {
              onEdit(editChoice.profile, 'only_this');
              setEditChoice(null);
            }}
          >
            Solo questa istanza
          </button>
          <button
            type="button"
            disabled={pending}
            onClick={() => {
              onEdit(
                editChoice.profile,
                editChoice.selectedHasFacts
                  ? 'from_next'
                  : 'this_and_following',
              );
              setEditChoice(null);
            }}
          >
            {editChoice.selectedHasFacts
              ? 'Dalla prossima istanza'
              : 'Questa e le successive'}
          </button>
          {editChoice.selectedHasFacts ? (
            <p>La registrazione di questa istanza rimane invariata.</p>
          ) : null}
          <button
            type="button"
            disabled={pending}
            onClick={() => setEditChoice(null)}
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
              Verranno eliminate anche {deleteImpact.attempts.length} Sessioni
              registrate (
              {deleteImpact.attempts
                .map((attempt) => attempt.status)
                .join(', ')}
              ).
            </p>
          ) : null}
          {recurringDeletePreview ? (
            <>
              <p>
                Questa Activity appartiene a una Routine ricorrente. «Solo
                questa istanza» rimuove unicamente l’Activity selezionata e
                tutte le sue Sessioni e i suoi dati. «Tutta la serie» elimina
                definitivamente anche la Routine, tutte le altre istanze e i
                relativi dati, presenti e futuri.
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
                  await source.deleteHard(
                    activityRef,
                    deleteImpact.fingerprint,
                  );
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
