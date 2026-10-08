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
  type ActivityReplanChange,
  type ActivityNewPlanned,
  type ActivityReplanTime,
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
  const [reminderLeadMinutes, setReminderLeadMinutes] = useState<number | null>(null);
  const [planDraft, setPlanDraft] = useState<Record<string, ActivityReplanTime>>({});
  const [newPlanned, setNewPlanned] = useState<ActivityNewPlanned[]>([]);
  const [removedPlanned, setRemovedPlanned] = useState<string[]>([]);
  const [planPreview, setPlanPreview] = useState<readonly ActivityReplanChange[] | null>(null);
  const [planOperation, setPlanOperation] = useState<string | null>(null);
  const [planPending, setPlanPending] = useState(false);
  const [planError, setPlanError] = useState('');
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
  const editablePlan = settings?.schedules.filter((schedule) =>
    schedule.role === 'interval' || schedule.role === 'planned') ?? [];
  const coreDirty =
    draft.title !== profile.title ||
    draft.description !== (profile.description ?? '') ||
    draft.location !== (profile.location ?? '') ||
    draft.colorCode !== (profile.colorCode ?? '') ||
    (settings !== null &&
      (captureMode !== settings.capture.mode ||
        realityMode !== settings.reality.mode ||
        reminderLeadMinutes !== settings.reminderLeadMinutes));
  const canReplan = !!settings &&
    settings.schedules.some((schedule) => schedule.role === 'interval') &&
    editablePlan.every((schedule) =>
      ['floating_local', 'named_zone_local'].includes(schedule.temporalForm) &&
      !!schedule.start && !!schedule.end);
  const planDirty = canReplan && (removedPlanned.length > 0 || newPlanned.length > 0 ||
    editablePlan.some((schedule) => !removedPlanned.includes(schedule.scheduleRef) && (
      planDraft[schedule.scheduleRef]?.start !== schedule.start ||
      planDraft[schedule.scheduleRef]?.end !== schedule.end)));
  const replanDraft = { times: planDraft, removedPlanned, newPlanned };
  const dirty = coreDirty || planDirty;

  const loadSettings = useCallback(() => {
    return settingsSource
      .load(profile.activityRef)
      .then((loaded) => {
        setSettings(loaded);
        setCaptureMode(loaded.capture.mode);
        setRealityMode(loaded.reality.mode);
        setReminderLeadMinutes(loaded.reminderLeadMinutes);
        setPlanDraft(Object.fromEntries(loaded.schedules.map((schedule) => [
          schedule.scheduleRef, { start: schedule.start ?? '', end: schedule.end ?? '' },
        ])));
        setNewPlanned([]);
        setRemovedPlanned([]);
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
    if (pending || planPending) return;
    if (confirmingDiscard) {
      setConfirmingDiscard(false);
    } else if (dirty) {
      setConfirmingDiscard(true);
    } else {
      onCancel();
    }
  }, [confirmingDiscard, dirty, onCancel, pending, planPending]);

  const changePlan = (ref: string, field: keyof ActivityReplanTime, value: string) => {
    setPlanDraft((current) => ({ ...current,
      [ref]: { start: current[ref]?.start ?? '', end: current[ref]?.end ?? '', [field]: value },
    }));
    setPlanPreview(null);
    setPlanOperation(null);
    setPlanError('');
  };

  const changeNewPlanned = (ref: string, field: 'start' | 'end' | 'name', value: string) => {
    setNewPlanned((current) => current.map((item) => item.clientRef === ref
      ? { ...item, [field]: value } : item));
    setPlanPreview(null);
    setPlanOperation(null);
  };

  const previewPlan = () => {
    if (!settings || !canReplan || !planDirty || coreDirty || planPending) return;
    const operationId = crypto.randomUUID();
    setPlanPending(true);
    setPlanError('');
    void settingsSource.previewReplan(profile.activityRef, settings, replanDraft, operationId)
      .then((changes) => {
        setPlanOperation(operationId);
        setPlanPreview(changes);
      })
      .catch((reason: unknown) => setPlanError(reason instanceof Error
        ? reason.message : 'Anteprima non disponibile.'))
      .finally(() => setPlanPending(false));
  };

  const applyPlan = () => {
    if (!settings || !planPreview || !planOperation || planPending || coreDirty) return;
    setPlanPending(true);
    setPlanError('');
    void settingsSource.applyReplan(profile.activityRef, settings, replanDraft, planOperation)
      .then((saved) => {
        setSettings(saved);
        setPlanDraft(Object.fromEntries(saved.schedules.map((schedule) => [
          schedule.scheduleRef, { start: schedule.start ?? '', end: schedule.end ?? '' },
        ])));
        setNewPlanned([]);
        setRemovedPlanned([]);
        setPlanPreview(null);
        setPlanOperation(null);
        onSaved(profile);
      })
      .catch((reason: unknown) => setPlanError(reason instanceof Error
        ? reason.message : 'Riprogrammazione non riuscita.'))
      .finally(() => setPlanPending(false));
  };

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
          pending || planPending ||
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
          const reminderChanged = reminderLeadMinutes !== settings.reminderLeadMinutes;
          if (!metadataChanged && !captureChanged && !realityChanged && !reminderChanged) {
            onSaved(profile);
            return;
          }
          const saved = await settingsSource.saveCore(profile, settings, {
            ...(metadataChanged ? { profile: changed } : {}),
            ...(captureChanged ? { capture: captureMode } : {}),
            ...(realityChanged ? { reality: realityMode } : {}),
            ...(reminderChanged ? { reminderLeadMinutes } : {}),
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
            {settings.reminderScheduleRef ? (
              <fieldset>
                <legend>Promemoria</legend>
                <label className="timeline-activity-editor__checkbox">
                  <input
                    type="checkbox"
                    checked={reminderLeadMinutes !== null}
                    onChange={(event) => {
                      operation.current = undefined;
                      setReminderLeadMinutes(event.target.checked ? 15 : null);
                    }}
                  />
                  Attiva promemoria
                </label>
                {reminderLeadMinutes !== null ? (
                  <label>
                    Minuti prima dell’inizio
                    <input
                      type="number"
                      min={0}
                      max={10080}
                      required
                      value={reminderLeadMinutes}
                      onChange={(event) => {
                        operation.current = undefined;
                        setReminderLeadMinutes(Number(event.target.value));
                      }}
                    />
                  </label>
                ) : null}
              </fieldset>
            ) : null}
            <section
              className="timeline-activity-editor__readback"
              aria-label="Programmazione attuale"
            >
              <h3>Programmazione attuale</h3>
              {planError ? <p role="alert">{planError}</p> : null}
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
                      {canReplan && (schedule.role === 'interval' || schedule.role === 'planned') &&
                        !removedPlanned.includes(schedule.scheduleRef) ? (
                        <div className="timeline-activity-editor__fields">
                          <label>
                            Inizio
                            <input type="datetime-local" required disabled={planPending}
                              value={planDraft[schedule.scheduleRef]?.start.slice(0, 16) ?? ''}
                              onChange={(event) => changePlan(schedule.scheduleRef, 'start', event.target.value)} />
                          </label>
                          <label>
                            Fine
                            <input type="datetime-local" required disabled={planPending}
                              value={planDraft[schedule.scheduleRef]?.end.slice(0, 16) ?? ''}
                              onChange={(event) => changePlan(schedule.scheduleRef, 'end', event.target.value)} />
                          </label>
                        </div>
                      ) : null}
                      {canReplan && schedule.role === 'planned' ? (
                        <button type="button" disabled={planPending} onClick={() => {
                          setRemovedPlanned((current) => current.includes(schedule.scheduleRef)
                            ? current.filter((ref) => ref !== schedule.scheduleRef)
                            : [...current, schedule.scheduleRef]);
                          setPlanPreview(null);
                          setPlanOperation(null);
                        }}>
                          {removedPlanned.includes(schedule.scheduleRef) ? 'Mantieni sessione' : 'Rimuovi sessione'}
                        </button>
                      ) : null}
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Nessun intervallo programmato.</p>
              )}
              {canReplan ? (
                <div>
                  {newPlanned.map((item) => (
                    <div key={item.clientRef} className="timeline-activity-editor__fields">
                      <label>Nome sessione
                        <input maxLength={300} disabled={planPending} value={item.name}
                          onChange={(event) => changeNewPlanned(item.clientRef, 'name', event.target.value)} />
                      </label>
                      <label>Inizio
                        <input type="datetime-local" required disabled={planPending} value={item.start.slice(0, 16)}
                          onChange={(event) => changeNewPlanned(item.clientRef, 'start', event.target.value)} />
                      </label>
                      <label>Fine
                        <input type="datetime-local" required disabled={planPending} value={item.end.slice(0, 16)}
                          onChange={(event) => changeNewPlanned(item.clientRef, 'end', event.target.value)} />
                      </label>
                      <button type="button" disabled={planPending} onClick={() => {
                        setNewPlanned((current) => current.filter((row) => row.clientRef !== item.clientRef));
                        setPlanPreview(null);
                        setPlanOperation(null);
                      }}>Rimuovi nuova sessione</button>
                    </div>
                  ))}
                  <button type="button" disabled={planPending ||
                    editablePlan.filter((row) => row.role === 'planned').length - removedPlanned.length +
                      newPlanned.length >= 100} onClick={() => {
                    setNewPlanned((current) => [...current, {
                      clientRef: crypto.randomUUID(), name: '', start: '', end: '',
                    }]);
                    setPlanPreview(null);
                    setPlanOperation(null);
                  }}>Aggiungi sessione pianificata</button>
                </div>
              ) : null}
              {planDirty ? (
                <div>
                  {coreDirty ? <p>Salva le altre impostazioni separatamente prima di spostare l’attività.</p> : null}
                  <button type="button" disabled={planPending || pending || coreDirty}
                    onClick={previewPlan}>
                    {planPending ? 'Verifica…' : 'Verifica spostamento'}
                  </button>
                  <button type="button" disabled={planPending} onClick={() => {
                    setPlanDraft(Object.fromEntries(settings.schedules.map((schedule) => [
                      schedule.scheduleRef,
                      { start: schedule.start ?? '', end: schedule.end ?? '' },
                    ])));
                    setNewPlanned([]);
                    setRemovedPlanned([]);
                    setPlanPreview(null);
                    setPlanOperation(null);
                  }}>Ripristina orari</button>
                </div>
              ) : null}
              {planPreview ? (
                <div role="group" aria-label="Anteprima spostamento">
                  <h4>Modifiche proposte</h4>
                  <ul>{planPreview.map((change) => (
                    <li key={change.scheduleRef ?? change.clientRef}>
                      {change.role === 'planned_added' ? 'Nuova sessione' :
                        change.role === 'planned_removed' ? 'Sessione rimossa' :
                        change.role === 'planned' ? 'Sessione pianificata' :
                        change.role === 'envelope' ? 'Intervallo complessivo' : 'Intervallo'}:
                      {' '}{change.previousStart && change.previousEnd ?
                        `${change.previousStart} – ${change.previousEnd}` : ''}
                      {' → '}{change.proposedStart && change.proposedEnd ?
                        `${change.proposedStart} – ${change.proposedEnd}` : 'rimossa'}
                    </li>
                  ))}</ul>
                  <button type="button" disabled={planPending || pending || coreDirty} onClick={applyPlan}>
                    Applica programmazione
                  </button>
                  <button type="button" disabled={planPending} onClick={() => {
                    setPlanPreview(null);
                    setPlanOperation(null);
                  }}>Annulla proposta</button>
                </div>
              ) : null}
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
        <button type="button" disabled={pending || planPending} onClick={requestClose}>
          Annulla
        </button>
        <button
          type="submit"
          disabled={
            pending || planPending || planDirty ||
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
