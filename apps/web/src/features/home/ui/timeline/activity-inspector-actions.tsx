import { useEffect, useState } from 'react';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
} from '../../../temporal/remote-activity-inspector';
import { createRemoteActivityEditSettings } from '../../../temporal/remote-activity-edit-settings';
import {
  buildActivityDuplicateSeed,
  type ActivityDuplicateSeed,
} from '../../../temporal-create/application/activity-duplicate-seed';

export function ActivityInspectorActions({
  activityRef,
  onEdit,
  onDeleted,
  onDuplicate,
}: Readonly<{
  activityRef: string;
  onEdit: (profile: ActivityProfile) => void;
  onDeleted: () => void;
  onDuplicate: (seed: ActivityDuplicateSeed) => void;
}>) {
  const [source] = useState(createRemoteActivityInspector);
  const [settingsSource] = useState(createRemoteActivityEditSettings);
  const [profile, setProfile] = useState<ActivityProfile | null>(null);
  const [confirming, setConfirming] = useState(false);
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

  return (
    <>
      <div className="timeline-activity-inspector__toolbar">
        <button
          type="button"
          disabled={pending}
          onClick={() =>
            void action(async () => {
              onEdit(await source.get(activityRef));
            })
          }
        >
          Modifica
        </button>
        <button
          type="button"
          disabled={pending}
          onClick={() => setConfirming(true)}
        >
          Elimina
        </button>
        <button
          type="button"
          disabled={pending}
          onClick={() =>
            void action(async () => {
              const [savedProfile, settings] = await Promise.all([
                source.get(activityRef),
                settingsSource.load(activityRef),
              ]);
              onDuplicate(buildActivityDuplicateSeed(savedProfile, settings));
            })
          }
        >
          Duplica
        </button>
      </div>
      {profile?.description || profile?.location ? (
        <div className="timeline-activity-inspector__details">
          {profile.description ? <p>{profile.description}</p> : null}
          {profile.location ? <p>Località: {profile.location}</p> : null}
        </div>
      ) : null}
      {error ? <p role="alert">{error}</p> : null}
      {confirming ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            Eliminare questa attività? Le sessioni già registrate restano nello
            storico.
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
