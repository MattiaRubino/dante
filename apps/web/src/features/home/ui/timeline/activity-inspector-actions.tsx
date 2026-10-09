import { useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
} from '../../../temporal/remote-activity-inspector';
import { createRemoteActivityEditSettings } from '../../../temporal/remote-activity-edit-settings';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import {
  createRemoteDraftVault, notifyDraftVaultUpdated,
} from '../../../temporal-create/application/remote-draft-vault';
import {
  draftVaultSnapshotFromDuplicate,
} from '../../../temporal-create/application/draft-vault-from-duplicate';
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
  const [draftVault] = useState(createRemoteDraftVault);
  const [profile, setProfile] = useState<ActivityProfile | null>(null);
  const [confirming, setConfirming] = useState(false);
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
              const [savedProfile, settings, childCount, recurring] = await Promise.all([
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
        <button type="button" aria-label="Sposta in Bozze" title="Sposta in Bozze"
          disabled={pending} onClick={() => setConfirmingVault(true)}>
          {toolbarTarget ? <TimelineInspectorIcon name="copy" /> : 'Sposta in Bozze'}
        </button>
        <button
          type="button"
          aria-label="Elimina"
          title="Elimina"
          disabled={pending}
          onClick={() => setConfirming(true)}
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
      {confirmingVault ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>L'Attività verrà conservata come bozza non operativa e ritirata
            dalla Timeline. Le esecuzioni o i risultati registrati impediscono
            il ritiro: in quel caso l'originale rimane intatto.</p>
          <button type="button" disabled={pending}
            onClick={() => void action(async () => {
              if (subitemsCount > 0) {
                throw new Error('Sposta prima o completa le sotto-attività.');
              }
              const [savedProfile, settings, childCount, recurring, choice] = await Promise.all([
                source.get(activityRef),
                settingsSource.load(activityRef),
                settingsSource.loadChildCount(activityRef),
                recurringSource.loadActivityContext(activityRef),
                settingsSource.loadLifeAreaChoice(activityRef),
              ]);
              if (recurring !== null || childCount !== 0) {
                throw new Error('Questa attività contiene una serie o sotto-attività: ' +
                  'non possiamo ritirarle fingendo che siano una singola bozza.');
              }
              const selected = settings.lifeAreaRef === null ? undefined
                : choice.options.find((area) => area.ref === settings.lifeAreaRef);
              if (settings.lifeAreaRef !== null && !selected) {
                throw new Error('Life Area non più disponibile: ricarica la scheda.');
              }
              const areaDraft = selected ? {
                kind: 'existing' as const, lifeAreaRef: selected.ref,
                label: selected.name, expectedRevision: selected.revision ?? 1,
                colorCode: selected.colorCode ?? null, colorChanged: false,
              } : undefined;
              const draft = await draftVault.save(
                draftVaultSnapshotFromDuplicate(
                  buildActivityDuplicateSeed(savedProfile, settings), areaDraft,
                ),
                { draftRef: crypto.randomUUID(), revision: null,
                  operationId: crypto.randomUUID() },
              );
              try {
                await source.retire(activityRef);
              } catch (reason) {
                try {
                  await draftVault.remove(draft);
                } catch {
                  notifyDraftVaultUpdated();
                  throw new Error('Attività originale non ritirata. È stata conservata ' +
                    'anche una bozza: controlla Bozze prima di riprovare.');
                }
                throw reason;
              }
              notifyDraftVaultUpdated();
              onDeleted();
            })}>Conferma spostamento in Bozze</button>
          <button type="button" disabled={pending}
            onClick={() => setConfirmingVault(false)}>Annulla</button>
        </div>
      ) : null}
      {confirming ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            Eliminare questa attività? Se ci sono sessioni o risultati registrati,
            il sistema ne impedisce la cancellazione: puoi correggere i dati storici.
          </p>
          <button
            type="button"
            disabled={pending}
            onClick={() =>
              void action(async () => {
                await source.retire(activityRef);
                onDeleted();
              })
            }
          >
            Conferma eliminazione
          </button>
          <button
            type="button"
            disabled={pending}
            onClick={() => setConfirming(false)}
          >
            Annulla
          </button>
        </div>
      ) : null}
    </>
  );
}
