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
  type ActivityNewInterval,
  type ActivityNewPlanned,
  type ActivityReplanTime,
  type ActivityEditSettings,
  type ActivityLifeAreaChoice,
} from '../../../temporal/remote-activity-edit-settings';
import {
  createRemoteRealityObjectiveDataSource,
  type ObjectiveAssessment,
  type ObjectiveComparator,
  type ObjectiveKind,
  type ObjectiveView,
  type ObjectiveSeriesEditState,
  type RealityMode,
} from '../../../temporal/remote-reality-objective-data-source';
import type { SessionCaptureMode } from '../../../temporal/remote-session-capability-data-source';
import {
  createRemoteRecurringProfileEdit,
  type RecurringProfileContext,
  type RecurringProfileEditScope,
} from '../../../temporal/remote-recurring-profile-edit';

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
  const [objectiveSource] = useState(createRemoteRealityObjectiveDataSource);
  const [recurringSource] = useState(createRemoteRecurringProfileEdit);
  const [recurringContext, setRecurringContext] = useState<RecurringProfileContext | null>(null);
  const [recurringLoading, setRecurringLoading] = useState(true);
  const [recurringError, setRecurringError] = useState('');
  const [editScope, setEditScope] = useState<RecurringProfileEditScope>('only_this');
  const [settings, setSettings] = useState<ActivityEditSettings | null>(null);
  const [loadingSettings, setLoadingSettings] = useState(true);
  const [settingsError, setSettingsError] = useState('');
  const [captureMode, setCaptureMode] = useState<SessionCaptureMode | null>(
    null,
  );
  const [realityMode, setRealityMode] = useState<RealityMode | null>(null);
  const [reminderLeadMinutes, setReminderLeadMinutes] = useState<number | null>(null);
  const [placementProtected, setPlacementProtected] = useState<boolean | null>(null);
  const [lockPending, setLockPending] = useState(false);
  const [lockError, setLockError] = useState('');
  const [areaChoice, setAreaChoice] = useState<ActivityLifeAreaChoice | null>(null);
  const [selectedArea, setSelectedArea] = useState('');
  const [plannedNames, setPlannedNames] = useState<Record<string, string>>({});
  const [namePending, setNamePending] = useState<string | null>(null);
  const [nameError, setNameError] = useState('');
  const [areaPending, setAreaPending] = useState(false);
  const [areaError, setAreaError] = useState('');
  const areaOperation = useRef<string | null>(null);
  const [planDraft, setPlanDraft] = useState<Record<string, ActivityReplanTime>>({});
  const [newPlanned, setNewPlanned] = useState<ActivityNewPlanned[]>([]);
  const [removedPlanned, setRemovedPlanned] = useState<string[]>([]);
  const [newIntervals, setNewIntervals] = useState<ActivityNewInterval[]>([]);
  const [removedIntervals, setRemovedIntervals] = useState<string[]>([]);
  const [objectiveDraft, setObjectiveDraft] = useState({
    label: '', resultKind: 'boolean' as ObjectiveKind,
    comparatorCode: null as ObjectiveComparator | null,
    targetValue: '', targetMin: '', targetMax: '', unitCode: '',
  });
  const [objectivePending, setObjectivePending] = useState(false);
  const [objectiveError, setObjectiveError] = useState('');
  const objectiveOperation = useRef<string | null>(null);
  const [editingObjective, setEditingObjective] = useState<{
    objectiveRef: string;
    definitionRevision: number;
    presentationOrder: number;
    seriesState: ObjectiveSeriesEditState | null;
  } | null>(null);
  const [objectiveScope, setObjectiveScope] = useState<'only_this' | 'this_and_following'>(
    'only_this',
  );
  const [correctingObjective, setCorrectingObjective] = useState<ObjectiveView | null>(null);
  const [correctedValue, setCorrectedValue] = useState('');
  const [correctedBoolean, setCorrectedBoolean] = useState('true');
  const [correctedAssessment, setCorrectedAssessment] = useState<ObjectiveAssessment>('unknown');
  const correctionOperation = useRef<string | null>(null);
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
  const metadataDirty =
    draft.title !== profile.title ||
    draft.description !== (profile.description ?? '') ||
    draft.location !== (profile.location ?? '') ||
    draft.colorCode !== (profile.colorCode ?? '');
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
  const planDirty = canReplan && (
    removedIntervals.length > 0 || newIntervals.length > 0 ||
    removedPlanned.length > 0 || newPlanned.length > 0 ||
    editablePlan.some((schedule) =>
      !removedPlanned.includes(schedule.scheduleRef) &&
      !removedIntervals.includes(schedule.scheduleRef) && (
        planDraft[schedule.scheduleRef]?.start !== schedule.start ||
        planDraft[schedule.scheduleRef]?.end !== schedule.end
      ))
  );
  const replanDraft = {
    times: planDraft, removedIntervals, newIntervals, removedPlanned, newPlanned,
  };
  const lockDirty = settings !== null && settings.placementLockScheduleRef !== null &&
    placementProtected !== null && placementProtected !== settings.placementProtected;
  const areaDirty = areaChoice !== null &&
    (selectedArea || null) !== areaChoice.currentRef;
  const scopedDomainUnsupported = !!recurringContext && editScope === 'this_and_following';
  const nameDirty = !!settings && settings.schedules.some((schedule) =>
    schedule.role === 'planned' && (plannedNames[schedule.scheduleRef] ?? '') !== (schedule.name ?? ''));
  const objectiveDirty = !!objectiveDraft.label || objectiveDraft.resultKind !== 'boolean' ||
    !!objectiveDraft.targetValue || !!objectiveDraft.targetMin ||
    !!objectiveDraft.targetMax || !!objectiveDraft.unitCode;
  const dirty = coreDirty || planDirty || lockDirty || areaDirty || objectiveDirty || nameDirty;

  const loadSettings = useCallback(() => {
    return settingsSource
      .load(profile.activityRef)
      .then((loaded) => {
        setSettings(loaded);
        setCaptureMode(loaded.capture.mode);
        setRealityMode(loaded.reality.mode);
        setReminderLeadMinutes(loaded.reminderLeadMinutes);
        setPlacementProtected(loaded.placementProtected);
        setLockError('');
        setPlanDraft(Object.fromEntries(loaded.schedules.map((schedule) => [
          schedule.scheduleRef, { start: schedule.start ?? '', end: schedule.end ?? '' },
        ])));
        setNewPlanned([]);
        setPlannedNames(Object.fromEntries(loaded.schedules.filter((row) => row.role === 'planned')
          .map((row) => [row.scheduleRef, row.name ?? ''])));
        setRemovedPlanned([]);
        setNewIntervals([]);
        setRemovedIntervals([]);
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

  useEffect(() => {
    let active = true;
    setRecurringContext(null);
    setEditScope('only_this');
    setRecurringLoading(true);
    setRecurringError('');
    void recurringSource.loadActivityContext(profile.activityRef).then((loaded) => {
      if (active) setRecurringContext(loaded);
    }).catch((reason: unknown) => {
      if (active) setRecurringError(reason instanceof Error
        ? reason.message : 'Origine della ricorrenza non disponibile.');
    }).finally(() => {
      if (active) setRecurringLoading(false);
    });
    return () => { active = false; };
  }, [profile.activityRef, recurringSource]);

  useEffect(() => {
    let active = true;
    void settingsSource.loadLifeAreaChoice(profile.activityRef).then((loaded) => {
      if (!active) return;
      setAreaChoice(loaded);
      setSelectedArea(loaded.currentRef ?? '');
      setAreaError('');
    }).catch((reason: unknown) => {
      if (active) setAreaError(reason instanceof Error
        ? reason.message : 'Life Area non disponibile.');
    });
    return () => { active = false; };
  }, [profile.activityRef, settingsSource]);

  const requestClose = useCallback(() => {
    if (pending || planPending || lockPending || areaPending || objectivePending || namePending) return;
    if (confirmingDiscard) {
      setConfirmingDiscard(false);
    } else if (dirty) {
      setConfirmingDiscard(true);
    } else {
      onCancel();
    }
  }, [areaPending, confirmingDiscard, dirty, lockPending, onCancel,
    objectivePending, pending, planPending, namePending]);

  const applyLifeArea = () => {
    if (!areaChoice || !areaDirty || !settings || pending || planPending ||
        lockPending || areaPending) return;
    if (scopedDomainUnsupported) {
      setAreaError('La Life Area si può modificare solo con «Solo questa»; la propagazione alla serie non è disponibile.');
      return;
    }
    if (areaChoice.currentRef !== settings.lifeAreaRef) {
      setAreaError('Assegnazione cambiata. Chiudi Modifica e riapri.');
      return;
    }
    setAreaPending(true);
    setAreaError('');
    const operationId = areaOperation.current ??= crypto.randomUUID();
    void settingsSource.assignLifeArea(
      profile.activityRef, areaChoice, selectedArea || null, operationId,
    ).then((saved) => {
      areaOperation.current = null;
      setAreaChoice(saved);
      setSettings((current) => current && ({ ...current, lifeAreaRef: saved.currentRef }));
    }).catch((reason: unknown) => {
      setAreaError(reason instanceof Error ? reason.message : 'Cambio Life Area non riuscito.');
    }).finally(() => setAreaPending(false));
  };

  const updateObjectiveDraft = (patch: Partial<typeof objectiveDraft>) => {
    setObjectiveDraft((current) => ({ ...current, ...patch }));
    objectiveOperation.current = null;
    setObjectiveError('');
  };

  const startObjectiveEdit = (objective: ObjectiveView) => {
    if (objectivePending || !settings) return;
    setObjectivePending(true);
    setObjectiveError('');
    void Promise.all([
      objectiveSource.getDefinition(objective.objectiveRef),
      objectiveSource.getSeriesState(objective.objectiveRef),
    ]).then(([definition, seriesState]) => {
      setEditingObjective({
        objectiveRef: definition.objectiveRef,
        definitionRevision: definition.definitionRevision,
        presentationOrder: definition.presentationOrder,
        seriesState,
      });
      setObjectiveScope('only_this');
      setObjectiveDraft({
        label: definition.label,
        resultKind: definition.resultKind,
        comparatorCode: definition.comparatorCode,
        targetValue: definition.targetValue?.toString() ?? '',
        targetMin: definition.targetMin?.toString() ?? '',
        targetMax: definition.targetMax?.toString() ?? '',
        unitCode: definition.unitCode ?? '',
      });
      objectiveOperation.current = null;
    }).catch((reason: unknown) => {
      setObjectiveError(reason instanceof Error
        ? reason.message : 'Definizione dell’obiettivo non disponibile.');
    }).finally(() => setObjectivePending(false));
  };

  const startResultCorrection = (objective: ObjectiveView) => {
    if (objectivePending || !objective.observationRef || !objective.evaluationStateRef) return;
    setCorrectingObjective(objective);
    setCorrectedValue(objective.resultKind === 'qualitative'
      ? objective.qualitativeCode ?? ''
      : objective.observedNumeric?.toString() ?? '');
    setCorrectedBoolean(objective.observedBoolean === false ? 'false' : 'true');
    setCorrectedAssessment(objective.assessmentCode ?? 'unknown');
    correctionOperation.current = null;
    setObjectiveError('');
  };

  const applyResultCorrection = () => {
    if (!correctingObjective || !settings || objectivePending) return;
    const objective = correctingObjective;
    if (!objective.evaluationStateRef) {
      setObjectiveError('Manca la valutazione corrente: aggiorna la scheda prima di rettificare.');
      return;
    }
    const numeric = objective.resultKind === 'quantity' || objective.resultKind === 'range'
      ? Number(correctedValue) : null;
    if ((numeric !== null && (!correctedValue.trim() || !Number.isFinite(numeric))) ||
        (objective.resultKind === 'qualitative' && !correctedValue.trim())) {
      setObjectiveError('Inserisci il risultato corretto.');
      return;
    }
    setObjectivePending(true);
    setObjectiveError('');
    void objectiveSource.correctResult(objective.objectiveRef, {
      operationId: correctionOperation.current ??= crypto.randomUUID(),
      expectedEvaluationStateRef: objective.evaluationStateRef,
      observedBoolean: objective.resultKind === 'boolean'
        ? correctedBoolean === 'true' : null,
      observedNumeric: numeric,
      qualitativeCode: objective.resultKind === 'qualitative'
        ? correctedValue.trim() : null,
      assessmentCode: objective.resultKind === 'qualitative'
        ? correctedAssessment : null,
    }).then(() => settingsSource.refreshObjectives(profile.activityRef, settings))
      .then((saved) => {
        setSettings(saved);
        setCorrectingObjective(null);
        correctionOperation.current = null;
      }).catch((reason: unknown) => {
        setObjectiveError(reason instanceof Error
          ? reason.message : 'Rettifica del risultato non riuscita.');
      }).finally(() => setObjectivePending(false));
  };

  const addObjective = () => {
    if (!settings || objectivePending || pending || planPending || lockPending || areaPending ||
        !objectiveDraft.label.trim()) return;
    const kind = objectiveDraft.resultKind;
    const numeric = (value: string) => value.trim() && Number.isFinite(Number(value))
      ? Number(value) : null;
    const target = numeric(objectiveDraft.targetValue);
    const min = numeric(objectiveDraft.targetMin);
    const max = numeric(objectiveDraft.targetMax);
    if ((kind === 'quantity' && (target === null || !objectiveDraft.comparatorCode)) ||
        (kind === 'range' && (min === null || max === null || min > max))) {
      setObjectiveError('Controlla i valori numerici dell’obiettivo.');
      return;
    }
    const operationId = objectiveOperation.current ??= crypto.randomUUID();
    setObjectivePending(true);
    setObjectiveError('');
    const definition = {
      label: objectiveDraft.label.trim(),
      resultKind: kind,
      comparatorCode: kind === 'quantity'
        ? objectiveDraft.comparatorCode : kind === 'range' ? 'between' : null,
      targetValue: kind === 'quantity' ? target : null,
      targetMin: kind === 'range' ? min : null,
      targetMax: kind === 'range' ? max : null,
      unitCode: kind === 'quantity' || kind === 'range'
        ? objectiveDraft.unitCode.trim() || null : null,
    };
    const save = editingObjective
      ? objectiveSource.reviseDefinition(editingObjective.objectiveRef, {
          ...definition,
          presentationOrder: editingObjective.presentationOrder,
          expectedRevision: editingObjective.definitionRevision,
          scopeCode: objectiveScope,
          seriesState: editingObjective.seriesState,
          operationId,
        }).then(() => settingsSource.refreshObjectives(profile.activityRef, settings))
      : settingsSource.addObjective(
          profile.activityRef, settings, definition, operationId,
        );
    void save.then((saved) => {
      setSettings(saved);
      setEditingObjective(null);
      setObjectiveDraft({
        label: '', resultKind: 'boolean', comparatorCode: null,
        targetValue: '', targetMin: '', targetMax: '', unitCode: '',
      });
      objectiveOperation.current = null;
    }).catch((reason: unknown) => {
      setObjectiveError(reason instanceof Error
        ? reason.message : 'Impossibile aggiungere l’obiettivo.');
    }).finally(() => setObjectivePending(false));
  };

  const applyPlacementLock = () => {
    if (!settings || placementProtected === null || !lockDirty ||
        pending || planPending || lockPending) return;
    setLockPending(true);
    setLockError('');
    void settingsSource.setPlacementProtected(
      settings, placementProtected,
    ).then((saved) => {
      setSettings(saved);
    }).catch((reason: unknown) => {
      setLockError(reason instanceof Error
        ? reason.message : 'Impossibile aggiornare la protezione.');
    }).finally(() => setLockPending(false));
  };

  const changePlan = (ref: string, field: keyof ActivityReplanTime, value: string) => {
    setPlanDraft((current) => ({ ...current,
      [ref]: { start: current[ref]?.start ?? '', end: current[ref]?.end ?? '', [field]: value },
    }));
    setPlanPreview(null);
    setPlanOperation(null);
    setPlanError('');
  };

  const changeNewInterval = (
    ref: string, field: keyof ActivityReplanTime, value: string,
  ) => {
    setNewIntervals((current) => current.map((item) =>
      item.clientRef === ref ? { ...item, [field]: value } : item));
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
    if (!settings || !canReplan || !planDirty || coreDirty || lockDirty || areaDirty ||
        nameDirty || namePending || planPending || lockPending || areaPending) return;
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
    if (!settings || !planPreview || !planOperation || planPending || coreDirty ||
        lockDirty || areaDirty || nameDirty || namePending || lockPending || areaPending) return;
    setPlanPending(true);
    setPlanError('');
    void settingsSource.applyReplan(profile.activityRef, settings, replanDraft, planOperation)
      .then((saved) => {
        setSettings(saved);
        setPlannedNames(Object.fromEntries(saved.schedules.filter((row) => row.role === 'planned')
          .map((row) => [row.scheduleRef, row.name ?? ''])));
        setPlanDraft(Object.fromEntries(saved.schedules.map((schedule) => [
          schedule.scheduleRef, { start: schedule.start ?? '', end: schedule.end ?? '' },
        ])));
        setNewPlanned([]);
        setRemovedPlanned([]);
        setNewIntervals([]);
        setRemovedIntervals([]);
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
          pending || planPending || lockPending || areaPending || objectivePending || namePending ||
          areaDirty || lockDirty || planDirty || objectiveDirty || nameDirty ||
          !settings ||
          loadingSettings ||
          recurringLoading ||
          !!recurringError ||
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
          if (recurringContext && metadataChanged) {
            // The recurring metadata edit is one atomic owner/CAS command.
            // Do not split it into two independent partial saves.
            if (captureChanged || realityChanged || reminderChanged) {
              throw new Error(
                'Per mantenere il salvataggio atomico, modifica i dati generali ' +
                'separatamente da Sessioni, Reality e Promemoria.',
              );
            }
            const changedKeys = Object.fromEntries(
              Object.entries(changed).filter(
                ([key, value]) => value !== profile[key as keyof typeof changed],
              ),
            );
            const nextProfile = await recurringSource.saveActivityProfile(
              profile.activityRef, recurringContext, editScope,
              changedKeys, operation.current ??= crypto.randomUUID(),
            );
            operation.current = undefined;
            onSaved(nextProfile);
            return;
          }
          if (recurringContext && editScope === 'this_and_following') {
            throw new Error(
              'Questa e le prossime richiede una modifica ai dati generali.',
            );
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
        {recurringError ? <p role="alert">{recurringError}</p> : null}
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
            <fieldset aria-label="Life Area">
              <legend>Life Area</legend>
              {areaError ? <p role="alert">{areaError}</p> : null}
              {!areaChoice && !areaError ? <p role="status">Caricamento Life Area…</p> : null}
              {areaChoice ? (
                <>
                  {scopedDomainUnsupported && areaDirty ? (
                    <p role="status">Per modificare la Life Area scegli «Solo questa»: non propaghiamo modifiche parziali alla serie.</p>
                  ) : null}
                  <label>
                    Area assegnata
                    <select
                      value={selectedArea}
                      disabled={pending || planPending || lockPending || areaPending}
                      onChange={(event) => {
                        setSelectedArea(event.target.value);
                        areaOperation.current = null;
                        setAreaError('');
                      }}
                    >
                      <option value="">
                        Nessuna Life Area
                      </option>
                      {areaChoice.currentRef &&
                        !areaChoice.options.some((area) => area.ref === areaChoice.currentRef) ? (
                          <option value={areaChoice.currentRef} disabled>
                            Area precedente non più disponibile
                          </option>
                        ) : null}
                      {areaChoice.options.map((area) => (
                        <option key={area.ref} value={area.ref}>{area.name}</option>
                      ))}
                    </select>
                  </label>
                  {areaDirty ? (
                    <button type="button" disabled={pending || planPending || lockPending || areaPending || scopedDomainUnsupported}
                      onClick={applyLifeArea}>
                      {areaPending ? 'Salvataggio…' : 'Applica Life Area'}
                    </button>
                  ) : null}
                </>
              ) : null}
            </fieldset>
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
            {settings.placementLockScheduleRef ? (
               <fieldset aria-label="Protezione collocazione">
                 <legend>Protezione collocazione</legend>
                 {lockError ? <p role="alert">{lockError}</p> : null}
                 <label className="timeline-activity-editor__checkbox">
                   <input
                     type="checkbox"
                     checked={placementProtected ?? settings.placementProtected}
                     disabled={pending || planPending || lockPending}
                     onChange={(event) => {
                       setPlacementProtected(event.target.checked);
                       setLockError('');
                     }}
                   />
                   Non spostare automaticamente questa attività
                 </label>
                 {lockDirty ? (
                   <button
                     type="button"
                     disabled={pending || planPending || lockPending}
                     onClick={applyPlacementLock}
                   >
                     {lockPending ? 'Salvataggio…' : 'Applica protezione'}
                   </button>
                 ) : null}
               </fieldset>
             ) : null}
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
              {nameError ? <p role="alert">{nameError}</p> : null}
              {scopedDomainUnsupported && nameDirty ? (
                <p role="status">La rinomina di Session pianificate per tutta la serie non è ancora supportata. Seleziona «Solo questa».</p>
              ) : null}
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
                      {schedule.role === 'planned' ? (
                        <div className="timeline-activity-editor__fields">
                          <label>
                            Nome sessione pianificata
                            <input maxLength={300} disabled={!!namePending || pending || planPending}
                              value={plannedNames[schedule.scheduleRef] ?? ''}
                              onChange={(event) => {
                                setPlannedNames((current) => ({
                                  ...current, [schedule.scheduleRef]: event.target.value,
                                }));
                                setNameError('');
                              }} />
                          </label>
                          {(plannedNames[schedule.scheduleRef] ?? '') !== (schedule.name ?? '') ? (
                            <button type="button" disabled={!!namePending || pending || planPending ||
                              planDirty || areaDirty || coreDirty || lockDirty || scopedDomainUnsupported}
                              onClick={() => {
                                const next = plannedNames[schedule.scheduleRef]?.trim() || null;
                                setNamePending(schedule.scheduleRef);
                                setNameError('');
                                void settingsSource.revisePlannedName(
                                  profile.activityRef, schedule.scheduleRef, schedule.name, next,
                                ).then((saved) => {
                                  setSettings((current) => current && ({
                                    ...current,
                                    schedules: current.schedules.map((row) =>
                                      row.scheduleRef === schedule.scheduleRef
                                        ? { ...row, name: saved } : row),
                                  }));
                                  setPlannedNames((current) => ({
                                    ...current, [schedule.scheduleRef]: saved ?? '',
                                  }));
                                }).catch((reason: unknown) => {
                                  setNameError(reason instanceof Error
                                    ? reason.message : 'Rinomina della sessione non riuscita.');
                                }).finally(() => setNamePending(null));
                              }}>
                              {namePending === schedule.scheduleRef ? 'Salvataggio…' : 'Salva nome sessione'}
                            </button>
                          ) : null}
                        </div>
                      ) : null}
                      {canReplan && (schedule.role === 'interval' || schedule.role === 'planned') &&
                        !removedPlanned.includes(schedule.scheduleRef) &&
                         !removedIntervals.includes(schedule.scheduleRef) ? (
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
                      {canReplan && schedule.role === 'interval' ? (
                        <button type="button" disabled={planPending} onClick={() => {
                          setRemovedIntervals((current) =>
                            current.includes(schedule.scheduleRef)
                              ? current.filter((ref) => ref !== schedule.scheduleRef)
                              : [...current, schedule.scheduleRef]);
                          setPlanPreview(null);
                          setPlanOperation(null);
                          setPlanError('');
                        }}>
                          {removedIntervals.includes(schedule.scheduleRef)
                            ? 'Mantieni intervallo' : 'Rimuovi intervallo'}
                        </button>
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
              {!canReplan && settings.schedules.length > 0 ? (
                <p role="status">
                  La modifica degli orari qui richiede almeno un intervallo e
                  pianificazioni locali con inizio e fine. Le altre forme temporali
                  restano inalterate: DANTE non le converte automaticamente.
                  Puoi comunque correggere separatamente il nome delle Session
                  pianificate, senza modificare lo Schedule.
                </p>
              ) : null}
              {canReplan ? (
                <div>
                  {newIntervals.map((item) => (
                    <div key={item.clientRef} className="timeline-activity-editor__fields">
                      <label>Inizio nuovo intervallo
                        <input type="datetime-local" required disabled={planPending}
                          value={item.start.slice(0, 16)}
                          onChange={(event) => changeNewInterval(
                            item.clientRef, 'start', event.target.value)} />
                      </label>
                      <label>Fine nuovo intervallo
                        <input type="datetime-local" required disabled={planPending}
                          value={item.end.slice(0, 16)}
                          onChange={(event) => changeNewInterval(
                            item.clientRef, 'end', event.target.value)} />
                      </label>
                      <button type="button" disabled={planPending} onClick={() => {
                        setNewIntervals((current) =>
                          current.filter((row) => row.clientRef !== item.clientRef));
                        setPlanPreview(null);
                        setPlanOperation(null);
                        setPlanError('');
                      }}>Rimuovi nuovo intervallo</button>
                    </div>
                  ))}
                  <button type="button" disabled={planPending ||
                    editablePlan.filter((row) => row.role === 'interval').length -
                      removedIntervals.length + newIntervals.length >= 100}
                    onClick={() => {
                      setNewIntervals((current) => [...current, {
                        clientRef: crypto.randomUUID(), start: '', end: '',
                      }]);
                      setPlanPreview(null);
                      setPlanOperation(null);
                      setPlanError('');
                    }}>Aggiungi intervallo</button>
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
                  {coreDirty || lockDirty || areaDirty || nameDirty ? (
                    <p>Salva prima i nomi delle Session e le altre impostazioni; la programmazione si applica separatamente.</p>
                  ) : null}
                  <button type="button" disabled={planPending || pending || lockPending || areaPending ||
                      !!namePending || coreDirty || lockDirty || areaDirty || nameDirty}
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
                    setNewIntervals([]);
                    setRemovedIntervals([]);
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
                      {change.role === 'interval_added' ? 'Nuovo intervallo' :
                        change.role === 'interval_removed' ? 'Intervallo rimosso' :
                        change.role === 'planned_added' ? 'Nuova sessione' :
                        change.role === 'planned_removed' ? 'Sessione rimossa' :
                        change.role === 'planned' ? 'Sessione pianificata' :
                        change.role === 'envelope' ? 'Intervallo complessivo' : 'Intervallo'}:
                      {' '}{change.previousStart && change.previousEnd ?
                        `${change.previousStart} – ${change.previousEnd}` : ''}
                      {' → '}{change.proposedStart && change.proposedEnd ?
                        `${change.proposedStart} – ${change.proposedEnd}` : 'rimossa'}
                    </li>
                  ))}</ul>
                  <button type="button" disabled={planPending || pending || lockPending || areaPending ||
                      !!namePending || coreDirty || lockDirty || areaDirty || nameDirty} onClick={applyPlan}>
                    Applica programmazione
                  </button>
                  <button type="button" disabled={planPending} onClick={() => {
                    setPlanPreview(null);
                    setPlanOperation(null);
                  }}>Annulla proposta</button>
                </div>
              ) : null}
            </section>
            <section
              className="timeline-activity-editor__readback"
              aria-label="Obiettivi attuali"
            >
              <h3>Obiettivi attuali</h3>
              {settings.objectives.length ? (
                <ul>
                  {settings.objectives.map((objective) => (
                    <li key={objective.objectiveRef}>
                      {objective.label}
                      {objective.assessmentCode ? ` · ${objective.assessmentCode}` : ''}
                      <button type="button" disabled={objectivePending}
                        onClick={() => startObjectiveEdit(objective)}>
                        Modifica obiettivo
                      </button>
                      {objective.observationRef ? (
                        <button type="button" disabled={objectivePending}
                          onClick={() => startResultCorrection(objective)}>
                          Correggi risultato
                        </button>
                      ) : null}
                    </li>
                  ))}
                </ul>
              ) : <p>Nessun obiettivo configurato.</p>}
              <fieldset disabled={objectivePending}>
                <legend>{editingObjective ? 'Modifica obiettivo' : 'Nuovo obiettivo'}</legend>
                <label>Nome obiettivo
                  <input maxLength={300} value={objectiveDraft.label}
                    onChange={(event) => updateObjectiveDraft({ label: event.target.value })} />
                </label>
                <label>Tipo obiettivo
                  <select value={objectiveDraft.resultKind} onChange={(event) => {
                    const kind = event.target.value as ObjectiveKind;
                    updateObjectiveDraft({
                      resultKind: kind,
                      comparatorCode: kind === 'quantity' ? 'gte' :
                        kind === 'range' ? 'between' : null,
                      targetValue: '', targetMin: '', targetMax: '', unitCode: '',
                    });
                  }}>
                    <option value="boolean">Sì / No</option>
                    <option value="quantity">Quantità</option>
                    <option value="qualitative">Qualitativo</option>
                    <option value="range">Intervallo numerico</option>
                  </select>
                </label>
                {objectiveDraft.resultKind === 'quantity' ? (
                  <div className="timeline-activity-editor__fields">
                    <label>Confronto obiettivo
                      <select value={objectiveDraft.comparatorCode ?? 'gte'}
                        onChange={(event) => updateObjectiveDraft({
                          comparatorCode: event.target.value as ObjectiveComparator,
                        })}>
                        <option value="eq">Uguale a</option>
                        <option value="gte">Almeno</option>
                        <option value="lte">Al massimo</option>
                      </select>
                    </label>
                    <label>Valore obiettivo
                      <input type="number" required step="any"
                        value={objectiveDraft.targetValue}
                        onChange={(event) => updateObjectiveDraft({
                          targetValue: event.target.value,
                        })} />
                    </label>
                  </div>
                ) : null}
                {objectiveDraft.resultKind === 'range' ? (
                  <div className="timeline-activity-editor__fields">
                    <label>Minimo obiettivo
                      <input type="number" required step="any" value={objectiveDraft.targetMin}
                        onChange={(event) => updateObjectiveDraft({
                          targetMin: event.target.value,
                        })} />
                    </label>
                    <label>Massimo obiettivo
                      <input type="number" required step="any" value={objectiveDraft.targetMax}
                        onChange={(event) => updateObjectiveDraft({
                          targetMax: event.target.value,
                        })} />
                    </label>
                  </div>
                ) : null}
                {['quantity', 'range'].includes(objectiveDraft.resultKind) ? (
                  <label>Unità di misura
                    <input maxLength={40} value={objectiveDraft.unitCode}
                      onChange={(event) => updateObjectiveDraft({
                        unitCode: event.target.value,
                      })} />
                  </label>
                ) : null}
                {editingObjective && recurringContext &&
                  !editingObjective.seriesState ? (
                    <p>Questo obiettivo è stato aggiunto individualmente:
                      non esiste ancora una provenienza comune verificabile
                      per modificarlo anche nelle istanze future.
                      La correzione riguarda solo questa istanza.</p>
                  ) : null}
                {editingObjective?.seriesState ? (
                  <fieldset>
                    <legend>Ambito della modifica dell’obiettivo</legend>
                    <label>
                      <input type="radio" name="objective-edit-scope"
                        checked={objectiveScope === 'only_this'}
                        onChange={() => setObjectiveScope('only_this')} />
                      Solo questa
                    </label>
                    <label>
                      <input type="radio" name="objective-edit-scope"
                        checked={objectiveScope === 'this_and_following'}
                        onChange={() => setObjectiveScope('this_and_following')} />
                      Questa e le prossime
                    </label>
                    <p>La definizione comprende sempre l’istanza selezionata.
                      Le altre già passate restano invariate.</p>
                  </fieldset>
                ) : null}
                {objectiveError ? <p role="alert">{objectiveError}</p> : null}
                <button type="button" onClick={addObjective}
                  disabled={objectivePending || pending || planPending ||
                    lockPending || areaPending || !objectiveDraft.label.trim()}>
                  {objectivePending ? 'Salvataggio…' :
                    editingObjective ? 'Salva obiettivo' : 'Aggiungi obiettivo'}
                </button>
                {editingObjective ? (
                  <button type="button" onClick={() => {
                    setEditingObjective(null);
                    setObjectiveDraft({
                      label: '', resultKind: 'boolean', comparatorCode: null,
                      targetValue: '', targetMin: '', targetMax: '', unitCode: '',
                    });
                    objectiveOperation.current = null;
                  }}>Annulla modifica obiettivo</button>
                ) : null}
              </fieldset>
              {correctingObjective ? (
                <fieldset disabled={objectivePending}>
                  <legend>Rettifica risultato — {correctingObjective.label}</legend>
                  {correctingObjective.resultKind === 'boolean' ? (
                    <label>Risultato corretto
                      <select value={correctedBoolean}
                        onChange={(event) => {
                          setCorrectedBoolean(event.target.value);
                          correctionOperation.current = null;
                        }}>
                        <option value="true">Sì</option>
                        <option value="false">No</option>
                      </select>
                    </label>
                  ) : (
                    <label>Risultato corretto
                      <input
                        type={correctingObjective.resultKind === 'qualitative' ? 'text' : 'number'}
                        step="any" value={correctedValue}
                        onChange={(event) => {
                          setCorrectedValue(event.target.value);
                          correctionOperation.current = null;
                        }} />
                    </label>
                  )}
                  {correctingObjective.resultKind === 'qualitative' ? (
                    <label>Valutazione corretta
                      <select value={correctedAssessment}
                        onChange={(event) => {
                          setCorrectedAssessment(event.target.value as ObjectiveAssessment);
                          correctionOperation.current = null;
                        }}>
                        <option value="satisfied">Raggiunto</option>
                        <option value="partial">Parziale</option>
                        <option value="not_satisfied">Non raggiunto</option>
                        <option value="unknown">Sconosciuto</option>
                        <option value="indeterminate">Indeterminato</option>
                      </select>
                    </label>
                  ) : null}
                  <button type="button" onClick={applyResultCorrection}>
                    Salva rettifica
                  </button>
                  <button type="button" onClick={() => {
                    setCorrectingObjective(null);
                    correctionOperation.current = null;
                  }}>Annulla rettifica</button>
                  <p>La rettifica aggiorna il valore corrente senza cancellare
                    l’osservazione e la valutazione precedenti.</p>
                </fieldset>
              ) : null}
            </section>
          </>
        ) : null}
      </div>
      {recurringContext && (metadataDirty || areaDirty || nameDirty) ? (
        <fieldset className="timeline-activity-editor__fields">
          <legend>Ambito della modifica</legend>
          <label>
            <input type="radio" name="recurring-edit-scope"
              checked={editScope === 'only_this'}
              onChange={() => setEditScope('only_this')} />
            Solo questa
          </label>
          <label>
            <input type="radio" name="recurring-edit-scope"
              checked={editScope === 'this_and_following'}
              disabled={!metadataDirty && (areaDirty || nameDirty)}
              onChange={() => setEditScope('this_and_following')} />
            Questa e le prossime
          </label>
          {(areaDirty || nameDirty) ? (
            <p role="status">
              Life Area e nomi delle Session pianificate si salvano soltanto
              per questa istanza. Per applicare i dati generali alle successive,
              salva prima queste modifiche individuali.
            </p>
          ) : null}
          <p>
            L’istanza selezionata è sempre compresa. Le altre istanze
            già passate restano invariate; le modifiche future possono
            essere rifiutate se esistono eccezioni o dati già registrati.
          </p>
        </fieldset>
      ) : null}
      <div
        className="timeline-activity-editor__actions"
        inert={confirmingDiscard || undefined}
      >
        <button type="button" disabled={pending || planPending || lockPending ||
          areaPending || objectivePending || !!namePending} onClick={requestClose}>
          Annulla
        </button>
        <button
          type="submit"
          disabled={
            pending || planPending || lockPending || areaPending || objectivePending || !!namePending ||
            areaDirty || lockDirty || planDirty || objectiveDirty || nameDirty ||
            !settings ||
            loadingSettings ||
            recurringLoading ||
            !!recurringError ||
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
