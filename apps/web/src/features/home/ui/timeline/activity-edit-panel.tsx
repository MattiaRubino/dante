import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type RefObject,
} from 'react';

import type { ActivityProfile } from '../../../temporal/remote-activity-inspector';
import {
  createRemoteActivityEditSettings,
  type ActivityEditSettings,
} from '../../../temporal/remote-activity-edit-settings';
import type { RealityMode } from '../../../temporal/remote-reality-objective-data-source';
import type { SessionCaptureMode } from '../../../temporal/remote-session-capability-data-source';

export function ActivityEditPanel({
  profile,
  onSaved,
  onCancel,
  closeRequestRef,
}: Readonly<{
  profile: ActivityProfile;
  onSaved: (profile: ActivityProfile) => void;
  onCancel: () => void;
  closeRequestRef: RefObject<(() => void) | null>;
}>) {
  const [settingsSource] = useState(createRemoteActivityEditSettings);
  const [settings, setSettings] = useState<ActivityEditSettings | null>(null);
  const [loadingSettings, setLoadingSettings] = useState(true);
  const [settingsError, setSettingsError] = useState('');
  const [captureMode, setCaptureMode] = useState<SessionCaptureMode | null>(
    null,
  );
  const [realityMode, setRealityMode] = useState<RealityMode | null>(null);
  const operation = useRef<string | undefined>(undefined);
  const [draft, setDraft] = useState(() => ({
    title: profile.title,
    description: profile.description ?? '',
    location: profile.location ?? '',
    colorCode: profile.colorCode ?? '',
  }));
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const [confirmingDiscard, setConfirmingDiscard] = useState(false);
  const discardButtonRef = useRef<HTMLButtonElement | null>(null);
  const dirty =
    draft.title !== profile.title ||
    draft.description !== (profile.description ?? '') ||
    draft.location !== (profile.location ?? '') ||
    draft.colorCode !== (profile.colorCode ?? '') ||
    (settings !== null &&
      (captureMode !== settings.capture.mode ||
        realityMode !== settings.reality.mode));

  const loadSettings = useCallback(() => {
    return settingsSource
      .load(profile.activityRef)
      .then((loaded) => {
        setSettings(loaded);
        setCaptureMode(loaded.capture.mode);
        setRealityMode(loaded.reality.mode);
      })
      .catch((reason: unknown) => {
        setSettingsError(
          reason instanceof Error
            ? reason.message
            : 'Impostazioni non disponibili.',
        );
      })
      .finally(() => setLoadingSettings(false));
  }, [profile.activityRef, settingsSource]);

  useEffect(() => {
    void loadSettings();
  }, [loadSettings]);

  const requestClose = useCallback(() => {
    if (pending) return;
    if (confirmingDiscard) {
      setConfirmingDiscard(false);
    } else if (dirty) {
      setConfirmingDiscard(true);
    } else {
      onCancel();
    }
  }, [confirmingDiscard, dirty, onCancel, pending]);

  useEffect(() => {
    closeRequestRef.current = requestClose;
    return () => {
      closeRequestRef.current = null;
    };
  }, [closeRequestRef, requestClose]);

  useEffect(() => {
    if (confirmingDiscard) discardButtonRef.current?.focus();
  }, [confirmingDiscard]);

  return (
    <form
      className="timeline-activity-editor"
      onSubmit={(event) => {
        event.preventDefault();
        if (
          pending ||
          !settings ||
          loadingSettings ||
          settingsError ||
          !captureMode ||
          !realityMode ||
          !draft.title.trim()
        )
          return;
        setPending(true);
        setError('');
        void (async () => {
          const changed = {
            title: draft.title.trim(),
            description: draft.description.trim() || null,
            location: draft.location.trim() || null,
            colorCode: draft.colorCode || null,
          };
          const metadataChanged = Object.entries(changed).some(
            ([key, value]) => value !== profile[key as keyof typeof changed],
          );
          const captureChanged = captureMode !== settings.capture.mode;
          const realityChanged = realityMode !== settings.reality.mode;
          if (!metadataChanged && !captureChanged && !realityChanged) {
            onSaved(profile);
            return;
          }
          const saved = await settingsSource.saveCore(profile, settings, {
            ...(metadataChanged ? { profile: changed } : {}),
            ...(captureChanged ? { capture: captureMode } : {}),
            ...(realityChanged ? { reality: realityMode } : {}),
          }, operation.current ??= crypto.randomUUID());
          operation.current = undefined;
          setSettings(saved.settings);
          onSaved(saved.profile);
        })()
          .catch((reason: unknown) => {
            const message =
              reason instanceof Error
                ? reason.message
                : 'Operazione non riuscita.';
            setError(message);
          })
          .finally(() => setPending(false));
      }}
    >
      <div
        className="timeline-activity-editor__body"
        inert={confirmingDiscard || undefined}
      >
        {error ? <p role="alert">{error}</p> : null}
        {loadingSettings ? (
          <p role="status">Caricamento impostazioni…</p>
        ) : null}
        {settingsError ? (
          <div role="alert">
            {settingsError}
            <button
              type="button"
              onClick={() => {
                setLoadingSettings(true);
                setSettingsError('');
                void loadSettings();
              }}
            >
              Riprova
            </button>
          </div>
        ) : null}
        <label className="timeline-activity-editor__title">
          Titolo
          <input
            required
            maxLength={300}
            value={draft.title}
            onChange={(event) => {
              operation.current = undefined;
              setDraft({ ...draft, title: event.target.value });
            }}
          />
        </label>
        <div className="timeline-activity-editor__fields">
          <label>
            Descrizione
            <textarea
              value={draft.description}
              onChange={(event) => {
                operation.current = undefined;
                setDraft({ ...draft, description: event.target.value });
              }}
            />
          </label>
          <label>
            Località
            <input
              value={draft.location}
              onChange={(event) => {
                operation.current = undefined;
                setDraft({ ...draft, location: event.target.value });
              }}
            />
          </label>
          <fieldset>
            <legend>Colore</legend>
            <label className="timeline-activity-editor__checkbox">
              <input
                type="checkbox"
                checked={!!draft.colorCode}
              onChange={(event) => {
                operation.current = undefined;
                setDraft({
                    ...draft,
                    colorCode: event.target.checked ? '#EA5C12' : '',
                });
              }}
              />
              Colore personalizzato
            </label>
            {draft.colorCode ? (
              <input
                aria-label="Scegli colore"
                type="color"
                value={draft.colorCode}
                onChange={(event) => {
                  operation.current = undefined;
                  setDraft({
                    ...draft,
                    colorCode: event.target.value.toUpperCase(),
                  });
                }}
              />
            ) : null}
          </fieldset>
        </div>
        {settings ? (
          <>
            <div className="timeline-activity-editor__fields">
              <label>
                Registrazione sessioni
                <select
                  value={captureMode ?? settings.capture.mode}
                  onChange={(event) => {
                    operation.current = undefined;
                    setCaptureMode(event.target.value as SessionCaptureMode);
                  }}
                >
                  <option value="disabled">Disattivata</option>
                  <option value="record">Registrazione</option>
                  <option value="live">Sessione in diretta</option>
                  <option value="record_and_live">
                    Registrazione e diretta
                  </option>
                </select>
              </label>
              <label>
                Verifica dello svolgimento
                <select
                  value={realityMode ?? settings.reality.mode}
                  onChange={(event) => {
                    operation.current = undefined;
                    setRealityMode(event.target.value as RealityMode);
                  }}
                >
                  <option value="manual">Manuale</option>
                  <option value="review_on_end">Chiedi al termine</option>
                  <option value="auto_confirm_outcome">
                    Conferma automaticamente
                  </option>
                </select>
              </label>
            </div>
            <section
              className="timeline-activity-editor__readback"
              aria-label="Programmazione attuale"
            >
              <h3>Programmazione attuale</h3>
              {settings.schedules.length ? (
                <ul>
                  {settings.schedules.map((schedule) => (
                    <li key={schedule.scheduleRef}>
                      {schedule.name ||
                        (schedule.role === 'planned'
                          ? 'Sessione programmata'
                          : schedule.role === 'envelope'
                            ? 'Intervallo complessivo'
                            : 'Intervallo')}
                      {schedule.start ? ` · ${schedule.start}` : ''}
                      {schedule.end ? ` – ${schedule.end}` : ''}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Nessun intervallo programmato.</p>
              )}
            </section>
            {settings.objectives.length ? (
              <section
                className="timeline-activity-editor__readback"
                aria-label="Obiettivi attuali"
              >
                <h3>Obiettivi attuali</h3>
                <ul>
                  {settings.objectives.map((objective) => (
                    <li key={objective.objectiveRef}>{objective.label}</li>
                  ))}
                </ul>
              </section>
            ) : null}
          </>
        ) : null}
      </div>
      <div
        className="timeline-activity-editor__actions"
        inert={confirmingDiscard || undefined}
      >
        <button type="button" disabled={pending} onClick={requestClose}>
          Annulla
        </button>
        <button
          type="submit"
          disabled={
            pending ||
            !settings ||
            loadingSettings ||
            !!settingsError ||
            !draft.title.trim()
          }
        >
          {pending ? 'Salvataggio…' : 'Salva modifiche'}
        </button>
      </div>
      {confirmingDiscard ? (
        <div className="timeline-activity-editor__discard" role="alert">
          <p>Scartare le modifiche non salvate?</p>
          <button ref={discardButtonRef} type="button" onClick={onCancel}>
            Scarta modifiche
          </button>
          <button type="button" onClick={() => setConfirmingDiscard(false)}>
            Continua a modificare
          </button>
        </div>
      ) : null}
    </form>
  );
}
