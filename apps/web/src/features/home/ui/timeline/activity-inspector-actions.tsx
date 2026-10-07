import { useEffect, useState } from 'react';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
} from '../../../temporal/remote-activity-inspector';

export function ActivityInspectorActions({
  activityRef,
  onSaved,
  onDeleted,
}: Readonly<{
  activityRef: string;
  onSaved: (profile: ActivityProfile) => void;
  onDeleted: () => void;
}>) {
  const [source] = useState(createRemoteActivityInspector);
  const [profile, setProfile] = useState<ActivityProfile | null>(null);
  const [editing, setEditing] = useState(false);
  const [confirming, setConfirming] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const [draft, setDraft] = useState({ title: '', description: '', location: '', colorCode: '' });

  useEffect(() => {
    setProfile(null);
    setEditing(false);
    setConfirming(false);
    setError('');
  }, [activityRef]);

  async function action(task: () => Promise<void>) {
    setPending(true);
    setError('');
    try {
      await task();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Operazione non riuscita.');
    } finally {
      setPending(false);
    }
  }

  return (
    <>
      <div className="timeline-activity-inspector__toolbar">
        <button type="button" disabled={pending} onClick={() => void action(async () => {
          const current = await source.get(activityRef);
          setProfile(current);
          setDraft({
            title: current.title,
            description: current.description ?? '',
            location: current.location ?? '',
            colorCode: current.colorCode ?? '',
          });
          setEditing(true);
        })}>Modifica</button>
        <button type="button" disabled={pending} onClick={() => setConfirming(true)}>Elimina</button>
      </div>
      {error ? <p role="alert">{error}</p> : null}
      {confirming ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>Eliminare questa attività? Le sessioni già registrate restano nello storico.</p>
          <button type="button" disabled={pending} onClick={() => void action(async () => {
            await source.retire(activityRef);
            onDeleted();
          })}>Conferma eliminazione</button>
          <button type="button" disabled={pending} onClick={() => setConfirming(false)}>Annulla</button>
        </div>
      ) : null}
      {editing ? (
        <form className="timeline-activity-inspector__editor" onSubmit={(event) => {
          event.preventDefault();
          if (!profile) return;
          void action(async () => {
            const saved = await source.revise(profile, {
              title: draft.title.trim(),
              description: draft.description.trim() || null,
              location: draft.location.trim() || null,
              colorCode: draft.colorCode || null,
            });
            setProfile(saved);
            setEditing(false);
            onSaved(saved);
          });
        }}>
          <h4>Modifica attività</h4>
          <label>Titolo<input required maxLength={300} value={draft.title} onChange={(event) => setDraft({ ...draft, title: event.target.value })} /></label>
          <label>Descrizione<textarea value={draft.description} onChange={(event) => setDraft({ ...draft, description: event.target.value })} /></label>
          <label>Località<input value={draft.location} onChange={(event) => setDraft({ ...draft, location: event.target.value })} /></label>
          <label>Colore<input type="color" value={draft.colorCode || '#EA5C12'} disabled={!draft.colorCode} onChange={(event) => setDraft({ ...draft, colorCode: event.target.value.toUpperCase() })} /></label>
          <label><input type="checkbox" checked={!!draft.colorCode} onChange={(event) => setDraft({ ...draft, colorCode: event.target.checked ? '#EA5C12' : '' })} /> Colore personalizzato</label>
          <div><button type="submit" disabled={pending || !draft.title.trim()}>Salva</button> <button type="button" onClick={() => setEditing(false)}>Annulla</button></div>
        </form>
      ) : null}
    </>
  );
}
