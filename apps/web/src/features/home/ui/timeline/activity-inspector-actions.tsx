import { useState } from 'react';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
} from '../../../temporal/remote-activity-inspector';

export function ActivityInspectorActions({
  activityRef,
  onEdit,
  onDeleted,
}: Readonly<{
  activityRef: string;
  onEdit: (profile: ActivityProfile) => void;
  onDeleted: () => void;
}>) {
  const [source] = useState(createRemoteActivityInspector);
  const [confirming, setConfirming] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');

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
      </div>
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
