import { useState } from 'react';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
} from '../../../temporal/remote-activity-inspector';

export function ActivityEditPanel({
  profile,
  onSaved,
  onCancel,
}: Readonly<{
  profile: ActivityProfile;
  onSaved: (profile: ActivityProfile) => void;
  onCancel: () => void;
}>) {
  const [source] = useState(createRemoteActivityInspector);
  const [draft, setDraft] = useState(() => ({
    title: profile.title,
    description: profile.description ?? '',
    location: profile.location ?? '',
    colorCode: profile.colorCode ?? '',
  }));
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');

  return (
    <form
      className="timeline-activity-editor"
      onSubmit={(event) => {
        event.preventDefault();
        if (pending || !draft.title.trim()) return;
        setPending(true);
        setError('');
        void source
          .revise(profile, {
            title: draft.title.trim(),
            description: draft.description.trim() || null,
            location: draft.location.trim() || null,
            colorCode: draft.colorCode || null,
          })
          .then(onSaved)
          .catch((reason: unknown) => {
            setError(
              reason instanceof Error
                ? reason.message
                : 'Operazione non riuscita.',
            );
          })
          .finally(() => setPending(false));
      }}
    >
      <div className="timeline-activity-editor__body">
        {error ? <p role="alert">{error}</p> : null}
        <label className="timeline-activity-editor__title">
          Titolo
          <input
            required
            maxLength={300}
            value={draft.title}
            onChange={(event) =>
              setDraft({ ...draft, title: event.target.value })
            }
          />
        </label>
        <div className="timeline-activity-editor__fields">
          <label>
            Descrizione
            <textarea
              value={draft.description}
              onChange={(event) =>
                setDraft({ ...draft, description: event.target.value })
              }
            />
          </label>
          <label>
            Località
            <input
              value={draft.location}
              onChange={(event) =>
                setDraft({ ...draft, location: event.target.value })
              }
            />
          </label>
          <fieldset>
            <legend>Colore</legend>
            <label className="timeline-activity-editor__checkbox">
              <input
                type="checkbox"
                checked={!!draft.colorCode}
                onChange={(event) =>
                  setDraft({
                    ...draft,
                    colorCode: event.target.checked ? '#EA5C12' : '',
                  })
                }
              />
              Colore personalizzato
            </label>
            {draft.colorCode ? (
              <input
                aria-label="Scegli colore"
                type="color"
                value={draft.colorCode}
                onChange={(event) =>
                  setDraft({
                    ...draft,
                    colorCode: event.target.value.toUpperCase(),
                  })
                }
              />
            ) : null}
          </fieldset>
        </div>
      </div>
      <div className="timeline-activity-editor__actions">
        <button type="button" disabled={pending} onClick={onCancel}>
          Annulla
        </button>
        <button type="submit" disabled={pending || !draft.title.trim()}>
          {pending ? 'Salvataggio…' : 'Salva modifiche'}
        </button>
      </div>
    </form>
  );
}
