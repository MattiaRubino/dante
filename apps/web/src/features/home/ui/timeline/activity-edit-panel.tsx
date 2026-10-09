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
import { TemporalColorControl } from '../../../temporal-create/ui/temporal-color-control';
import { TimeControl } from '../../../temporal-create/ui/temporal-create-core-u2';
import { TemporalCreateDatePicker } from '../../../temporal-create/ui/temporal-create-date-picker';
import { TemporalLifeAreaSelect } from '../../../temporal-create/ui/temporal-life-area-select';
import { TemporalReminderControl } from '../../../temporal-create/ui/temporal-create-quick-reminder';
import '../../../temporal-create/ui/temporal-create-u1.css';
import '../../../temporal-create/ui/temporal-create-product-flow.css';
import '../../../temporal-create/ui/temporal-create-advanced-shell.css';
import '../../../temporal-create/ui/temporal-panel-controls.css';
import '../../../temporal-create/ui/temporal-create-reality-objectives-section.css';
import '../../../temporal-create/ui/temporal-create-core-u2.css';
import '../../../temporal-create/ui/temporal-create-advanced-activity-structure.css';
import '../../../temporal-create/ui/temporal-create-session-time-polish.css';
import './activity-edit-panel.css';
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
  const [areaQuery, setAreaQuery] = useState('');
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
  const [objectiveComposerOpen, setObjectiveComposerOpen] = useState(false);
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
  const hasIntervals = settings?.schedules.some((schedule) => schedule.role === 'interval') ?? false;
  const editablePlan = settings?.schedules.filter((schedule) =>
    schedule.role === 'interval' || schedule.role === 'planned' ||
    (schedule.role === 'envelope' && !hasIntervals)) ?? [];
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
    settings.schedules.some((schedule) => schedule.role === 'envelope') &&
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
  const areaQueryValid = !areaQuery || !!areaChoice?.options.some((area) =>
    area.ref === selectedArea && area.name === areaQuery);
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
      setAreaQuery(loaded.options.find((area) => area.ref === loaded.currentRef)?.name ?? '');
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
    if (!areaChoice || !areaDirty || !areaQueryValid || !settings || pending || planPending ||
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
      setObjectiveComposerOpen(true);
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
      setObjectiveComposerOpen(false);
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
        <div className="temporal-create-type-grid is-four timeline-activity-editor__kind"
          role="group" aria-label="Tipo: Attività">
          <button type="button" className="is-active" aria-current="true"><strong>Attività</strong></button>
          <button type="button" disabled title="Il tipo non può essere cambiato dopo la creazione"><strong>Evento</strong></button>
          <button type="button" className="is-deferred" disabled><strong>Timer</strong><small>Prossimamente</small></button>
          <button type="button" className="is-deferred" disabled><strong>Sveglia</strong><small>Prossimamente</small></button>
        </div>
        <div className="temporal-create-title-row has-tools timeline-activity-editor__title-row">
        <label className="timeline-activity-editor__title">
          <span className="timeline-activity-editor__visually-hidden">Titolo</span>
          <input
            className="temporal-create-title-input"
            required
            maxLength={300}
            placeholder="Titolo"
            value={draft.title}
            onChange={(event) => {
              operation.current = undefined;
              setDraft({ ...draft, title: event.target.value });
            }}
          />
        </label>
        {settings ? (
          <div className="temporal-create-title-row__tools timeline-activity-editor__title-tools">
            {settings.placementLockScheduleRef ? (
              <button type="button" className="temporal-create-placement-lock"
                aria-label={placementProtected ? 'Sblocca spostamenti' : 'Blocca spostamenti'}
                aria-pressed={placementProtected ?? settings.placementProtected}
                title={placementProtected ? 'Sblocca spostamenti' : 'Blocca spostamenti'}
                disabled={pending || planPending || lockPending}
                onClick={() => {
                  setPlacementProtected(!(placementProtected ?? settings.placementProtected));
                  setLockError('');
                }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor"
                  strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <rect x="5" y="10" width="14" height="11" rx="2" />
                  {(placementProtected ?? settings.placementProtected)
                    ? <path d="M8 10V7a4 4 0 0 1 8 0v3" />
                    : <path d="M8 10V7a4 4 0 0 1 7.5-1.9" />}
                </svg>
                <span>{placementProtected ? 'Sblocca spostamenti' : 'Blocca spostamenti'}</span>
              </button>
            ) : null}
            <label className="temporal-create-structure-session-toggle timeline-activity-editor__capture">
              <input type="checkbox" checked={(captureMode ?? settings.capture.mode) !== 'disabled'}
                onChange={(event) => {
                  operation.current = undefined;
                  setCaptureMode(event.target.checked ? 'live' : 'disabled');
                }} />
              Sessione
            </label>
          </div>
        ) : null}
        </div>
        {lockError ? <p role="alert">{lockError}</p> : null}
        {settings && (settings.schedules.some((row) => row.role === 'planned') || newPlanned.length > 0) ? (
          <section className="temporal-create-activity-tree timeline-activity-editor__sessions"
            aria-label="Sessioni pianificate">
            <div className="temporal-create-activity-tree__spine" aria-hidden="true" />
            <div className="temporal-create-activity-tree__root-sessions">
              <div className="temporal-create-activity-tree__group-label">Sessioni attività</div>
              {settings.schedules.filter((row) => row.role === 'planned').map((row) => {
                const removed = removedPlanned.includes(row.scheduleRef);
                const currentStart = planDraft[row.scheduleRef]?.start ?? row.start ?? '';
                const currentEnd = planDraft[row.scheduleRef]?.end ?? row.end ?? '';
                return (
                  <div className="temporal-create-tree-item is-session is-root"
                    key={row.scheduleRef} data-edit-planned-session={row.scheduleRef}>
                    <div className="temporal-create-tree-row">
                      <span className="temporal-create-tree-row__icon" aria-hidden="true">▶</span>
                      <span className="temporal-create-tree-row__divider" aria-hidden="true" />
                      <input className="temporal-create-tree-row__title" maxLength={300}
                        aria-label="Nome Sessione" placeholder="Nome Sessione"
                        disabled={removed || !!namePending || pending || planPending}
                        value={plannedNames[row.scheduleRef] ?? ''}
                        onChange={(event) => {
                          setPlannedNames((current) => ({
                            ...current, [row.scheduleRef]: event.target.value,
                          }));
                          setNameError('');
                        }} />
                      <div className="temporal-create-tree-row__actions">
                        <button type="button" className="is-active"
                          aria-expanded="true" aria-controls={`edit-session:${row.scheduleRef}:time`}
                          title="La rimozione dell’orario di una Session già pianificata non è ancora disponibile"
                          disabled>Orario</button>
                        {canReplan ? <button type="button" className="is-remove" disabled={planPending}
                          aria-label={removed ? 'Mantieni Sessione' : 'Rimuovi Sessione'}
                          onClick={() => {
                            setRemovedPlanned((current) => current.includes(row.scheduleRef)
                              ? current.filter((ref) => ref !== row.scheduleRef)
                              : [...current, row.scheduleRef]);
                            setPlanPreview(null);
                            setPlanOperation(null);
                          }}>{removed ? '↶' : '×'}</button> : null}
                      </div>
                    </div>
                    {!removed ? (
                      <div id={`edit-session:${row.scheduleRef}:time`}
                        className="temporal-create-tree-time-editor" inert={planPending || undefined}>
                        {canReplan ? <>
                          <TemporalCreateDatePicker label="Data Sessione" locale="it"
                            value={currentStart.slice(0, 10)}
                            onChange={(date) => changePlan(row.scheduleRef, 'start',
                              `${date}${currentStart.slice(10, 16)}`)} />
                          <TimeControl label="Inizio Sessione" dataPath={`startTime-${row.scheduleRef}`}
                            value={currentStart.slice(11, 16)}
                            onChange={(time) => changePlan(row.scheduleRef, 'start',
                              `${currentStart.slice(0, 10)}T${time}`)} />
                          <TimeControl label="Fine Sessione" dataPath={`endTime-${row.scheduleRef}`}
                            value={currentEnd.slice(11, 16)}
                            onChange={(time) => changePlan(row.scheduleRef, 'end',
                              `${currentEnd.slice(0, 10)}T${time}`)} />
                        </> : <span>{currentStart} – {currentEnd}</span>}
                      </div>
                    ) : null}
                    {(plannedNames[row.scheduleRef] ?? '') !== (row.name ?? '') ? (
                      <button type="button" disabled={!!namePending || pending || planPending ||
                        planDirty || areaDirty || coreDirty || lockDirty || scopedDomainUnsupported}
                        onClick={() => {
                          const next = plannedNames[row.scheduleRef]?.trim() || null;
                          setNamePending(row.scheduleRef);
                          setNameError('');
                          void settingsSource.revisePlannedName(profile.activityRef,
                            row.scheduleRef, row.name, next).then((saved) => {
                            setSettings((current) => current && ({ ...current,
                              schedules: current.schedules.map((schedule) => schedule.scheduleRef === row.scheduleRef
                                ? { ...schedule, name: saved } : schedule),
                            }));
                            setPlannedNames((current) => ({ ...current, [row.scheduleRef]: saved ?? '' }));
                          }).catch((reason: unknown) => {
                            setNameError(reason instanceof Error ? reason.message : 'Rinomina non riuscita.');
                          }).finally(() => setNamePending(null));
                        }}>Salva nome sessione</button>
                    ) : null}
                  </div>
                );
              })}
              {newPlanned.map((item) => (
                <div className="temporal-create-tree-item is-session is-root" key={item.clientRef}
                  data-edit-new-session={item.clientRef}>
                  <div className="temporal-create-tree-row">
                    <span className="temporal-create-tree-row__icon" aria-hidden="true">▶</span>
                    <span className="temporal-create-tree-row__divider" aria-hidden="true" />
                    <input className="temporal-create-tree-row__title" maxLength={300}
                      aria-label="Nome Sessione" placeholder="Nome Sessione" disabled={planPending}
                      value={item.name} onChange={(event) => changeNewPlanned(item.clientRef,
                        'name', event.target.value)} />
                    <div className="temporal-create-tree-row__actions">
                      <button type="button" className="is-active" aria-expanded="true"
                        aria-controls={`edit-session:${item.clientRef}:time`}
                        title="Le nuove Session pianificate richiedono ancora un orario" disabled>Orario</button>
                      <button type="button" className="is-remove" aria-label="Rimuovi Sessione"
                        disabled={planPending} onClick={() => {
                          setNewPlanned((current) => current.filter((row) => row.clientRef !== item.clientRef));
                          setPlanPreview(null);
                          setPlanOperation(null);
                        }}>×</button>
                    </div>
                  </div>
                  <div id={`edit-session:${item.clientRef}:time`} className="temporal-create-tree-time-editor">
                    <TemporalCreateDatePicker label="Data Sessione" locale="it" value={item.start.slice(0, 10)}
                      onChange={(date) => changeNewPlanned(item.clientRef, 'start',
                        `${date}${item.start.slice(10, 16)}`)} />
                    <TimeControl label="Inizio Sessione" dataPath={`newStart-${item.clientRef}`}
                      value={item.start.slice(11, 16)} onChange={(time) => changeNewPlanned(item.clientRef,
                        'start', `${item.start.slice(0, 10)}T${time}`)} />
                    <TimeControl label="Fine Sessione" dataPath={`newEnd-${item.clientRef}`}
                      value={item.end.slice(11, 16)} onChange={(time) => changeNewPlanned(item.clientRef,
                        'end', `${item.end.slice(0, 10)}T${time}`)} />
                  </div>
                </div>
              ))}
            </div>
          </section>
        ) : null}
        {canReplan ? (
          <button type="button" className="temporal-create-structure-add timeline-activity-editor__add-session"
            disabled={planPending || editablePlan.filter((row) => row.role === 'planned').length -
              removedPlanned.length + newPlanned.length >= 100}
            onClick={() => {
              const root = settings?.schedules.find((row) => row.role === 'envelope');
              setNewPlanned((current) => [...current, {
                clientRef: crypto.randomUUID(), name: '',
                start: root?.start?.slice(0, 16) ?? '',
                end: root?.end?.slice(0, 16) ?? '',
              }]);
              setPlanPreview(null);
              setPlanOperation(null);
            }}>＋ Sessione</button>
        ) : null}
        {lockDirty ? (
          <button type="button" className="timeline-activity-editor__apply-lock"
            disabled={pending || planPending || lockPending} onClick={applyPlacementLock}>
            {lockPending ? 'Salvataggio…' : 'Applica blocco spostamenti'}
          </button>
        ) : null}
        {settings ? (
          <>
            <section
              className="timeline-activity-editor__readback"
              aria-label="Programmazione attuale"
            >
              <div className="timeline-activity-editor__placement" role="group" aria-label="Collocazione attuale">
                <span className={settings.schedules.length > 0 &&
                    settings.schedules[0]?.temporalForm !== 'date_span' ? 'is-selected' : ''}>Orario</span>
                <span className={settings.schedules[0]?.temporalForm === 'date_span' ? 'is-selected' : ''}>Tutto il giorno</span>
                <span className={settings.schedules.length === 0 ? 'is-selected' : ''}>Da collocare</span>
              </div>
              <h3 className="timeline-activity-editor__visually-hidden">Programmazione attuale</h3>
              {settings.schedules.find((schedule) => schedule.zoneId)?.zoneId ? (
                <p className="timeline-activity-editor__timezone">
                  <span aria-hidden="true">◎</span> Fuso orario · {settings.schedules.find((schedule) => schedule.zoneId)?.zoneId}
                </p>
              ) : null}
              {planError ? <p role="alert">{planError}</p> : null}
              {nameError ? <p role="alert">{nameError}</p> : null}
              {scopedDomainUnsupported && nameDirty ? (
                <p role="status">La rinomina di Session pianificate per tutta la serie non è ancora supportata. Seleziona «Solo questa».</p>
              ) : null}
              {settings.schedules.length ? (
                <ul>
                  {settings.schedules.filter((schedule) => schedule.role !== 'planned').map((schedule) => (
                    <li key={schedule.scheduleRef}>
                      <div className="timeline-activity-editor__schedule-label">
                      {schedule.name ||
                        (schedule.role === 'planned'
                          ? 'Sessione programmata'
                          : schedule.role === 'envelope'
                            ? 'Intervallo complessivo'
                            : 'Intervallo')}
                      </div>
                      {schedule.start && schedule.end && !canReplan ? (
                        <div className="timeline-activity-editor__schedule-time" role="group" aria-label="Orario programmato">
                          <span>{(planDraft[schedule.scheduleRef]?.start || schedule.start).slice(0, 10)}</span>
                          <span>{(planDraft[schedule.scheduleRef]?.start || schedule.start).slice(11, 16)}</span>
                          <span aria-hidden="true">→</span>
                          <span>{(planDraft[schedule.scheduleRef]?.end || schedule.end).slice(11, 16)}</span>
                          <span>{(planDraft[schedule.scheduleRef]?.end || schedule.end).slice(0, 10)}</span>
                        </div>
                      ) : null}
                      {canReplan && (schedule.role === 'interval' ||
                        (schedule.role === 'envelope' && !hasIntervals)) &&
                        !removedPlanned.includes(schedule.scheduleRef) &&
                         !removedIntervals.includes(schedule.scheduleRef) ? (
                        <div className="temporal-create-u2-when timeline-activity-editor__when"
                          inert={planPending || undefined}>
                          <TemporalCreateDatePicker label="Data inizio" locale="it"
                            value={(planDraft[schedule.scheduleRef]?.start ?? schedule.start ?? '').slice(0, 10)}
                            onChange={(date) => changePlan(schedule.scheduleRef, 'start',
                              `${date}${(planDraft[schedule.scheduleRef]?.start ?? schedule.start ?? '').slice(10, 16)}`)} />
                          <TimeControl label="Inizio" dataPath={`startTime-${schedule.scheduleRef}`}
                            value={(planDraft[schedule.scheduleRef]?.start ?? schedule.start ?? '').slice(11, 16)}
                            onChange={(time) => changePlan(schedule.scheduleRef, 'start',
                              `${(planDraft[schedule.scheduleRef]?.start ?? schedule.start ?? '').slice(0, 10)}T${time}`)} />
                          <span className="timeline-activity-editor__when-arrow" aria-hidden="true">→</span>
                          <TimeControl label="Fine" dataPath={`endTime-${schedule.scheduleRef}`}
                            value={(planDraft[schedule.scheduleRef]?.end ?? schedule.end ?? '').slice(11, 16)}
                            onChange={(time) => changePlan(schedule.scheduleRef, 'end',
                              `${(planDraft[schedule.scheduleRef]?.end ?? schedule.end ?? '').slice(0, 10)}T${time}`)} />
                          <TemporalCreateDatePicker label="Data fine" locale="it"
                            value={(planDraft[schedule.scheduleRef]?.end ?? schedule.end ?? '').slice(0, 10)}
                            onChange={(date) => changePlan(schedule.scheduleRef, 'end',
                              `${date}${(planDraft[schedule.scheduleRef]?.end ?? schedule.end ?? '').slice(10, 16)}`)} />
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
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Nessun intervallo programmato.</p>
              )}
              {!canReplan && settings.schedules.length > 0 ? (
                <details className="timeline-activity-editor__planning-help">
                  <summary>Questo orario non è modificabile qui</summary>
                  <p>
                  La modifica degli orari richiede
                  pianificazioni locali con inizio e fine. Le altre forme temporali
                  restano inalterate: DANTE non le converte automaticamente.
                  Puoi comunque correggere separatamente il nome delle Session
                  pianificate, senza modificare lo Schedule.
                  </p>
                </details>
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
                  {hasIntervals ? <button type="button" disabled={planPending ||
                    editablePlan.filter((row) => row.role === 'interval').length -
                      removedIntervals.length + newIntervals.length >= 100}
                    onClick={() => {
                      setNewIntervals((current) => [...current, {
                        clientRef: crypto.randomUUID(), start: '', end: '',
                      }]);
                      setPlanPreview(null);
                      setPlanOperation(null);
                      setPlanError('');
                    }}>Aggiungi intervallo</button> : null}
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
            <div className="timeline-activity-editor__repeat" role="group" aria-label="Ripeti">
              Ripeti · {recurringContext ? 'Serie attiva' : 'Mai'}
            </div>
            <div className="timeline-activity-editor__area-color">
              <div className="temporal-create-life-area-field">
              <TemporalColorControl value={draft.colorCode || '#EA5C12'}
                label="Colore attività o evento" onChange={(colorCode) => {
                  operation.current = undefined;
                  setDraft((current) => ({ ...current, colorCode }));
                }} />
              <div className="timeline-activity-editor__area-choice">
              {areaError ? <p role="alert">{areaError}</p> : null}
              {!areaChoice && !areaError ? <p role="status">Caricamento Life Area…</p> : null}
              {areaChoice ? (
                <>
                  {scopedDomainUnsupported && areaDirty ? (
                    <p role="status">Per modificare la Life Area scegli «Solo questa»: non propaghiamo modifiche parziali alla serie.</p>
                  ) : null}
                  <TemporalLifeAreaSelect query={areaQuery}
                    label="Area assegnata"
                    options={areaChoice.options.map((area) => ({ id: area.ref, label: area.name }))}
                    selectedId={selectedArea || null}
                    disabled={pending || planPending || lockPending || areaPending}
                    onQueryChange={(query) => {
                      setAreaQuery(query);
                      setSelectedArea(areaChoice.options.find((area) => area.name === query)?.ref ?? '');
                      areaOperation.current = null;
                      setAreaError('');
                    }}
                    onChoose={(area) => {
                      setSelectedArea(area.id);
                      setAreaQuery(area.label);
                      areaOperation.current = null;
                      setAreaError('');
                    }}
                    onClear={() => { setSelectedArea(''); setAreaQuery(''); setAreaError(''); }} />
                  {!areaQueryValid ? <small>Scegli una Life Area dall’elenco.</small> : null}
                  {areaDirty ? (
                    <button type="button" disabled={!areaQueryValid || pending || planPending || lockPending || areaPending || scopedDomainUnsupported}
                      onClick={applyLifeArea}>
                      {areaPending ? 'Salvataggio…' : 'Applica Life Area'}
                    </button>
                  ) : null}
                </>
              ) : null}
              </div>
              </div>
            </div>
            <section className="temporal-create-reality-objectives timeline-activity-editor__outcome"
              aria-label="Svolgimento e obiettivi">
              <div className="temporal-create-reality-objectives__heading timeline-activity-editor__section-heading">
                <h3>Svolgimento e obiettivi</h3>
              </div>
            <div className="temporal-create-reality-objectives__block is-reality">
              <div className="temporal-create-reality-objectives__block-copy">
                <strong>Svolgimento dell’attività</strong>
              </div>
              <div className="temporal-create-reality-mode" role="radiogroup"
                aria-label="Verifica dello svolgimento">
                {([
                  ['manual', 'Nessuna verifica'],
                  ['review_on_end', 'Chiedi al termine'],
                  ['auto_confirm_outcome', 'Conferma automatica'],
                ] as const).map(([mode, label]) => (
                  <button key={mode} type="button" role="radio"
                    aria-checked={(realityMode ?? settings.reality.mode) === mode}
                    className={(realityMode ?? settings.reality.mode) === mode ? 'is-active' : ''}
                    onClick={() => { operation.current = undefined; setRealityMode(mode); }}>
                    {label}
                  </button>
                ))}
              </div>
            </div>
            <div className="temporal-create-reality-objectives__divider" />
            <section
              className="temporal-create-reality-objectives__block is-objectives timeline-activity-editor__readback"
              aria-label="Obiettivi attuali"
            >
              <div className="temporal-create-reality-objectives__block-copy"><strong>Obiettivi</strong></div>
              <div className="timeline-activity-editor__objectives">
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
              ) : null}
              {!objectiveComposerOpen ? (
                <button type="button" className="timeline-activity-editor__add-objective"
                  aria-label="Apri nuovo obiettivo"
                  onClick={() => setObjectiveComposerOpen(true)}>＋ Aggiungi obiettivo</button>
              ) : (
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
                    setObjectiveComposerOpen(false);
                    setObjectiveDraft({
                      label: '', resultKind: 'boolean', comparatorCode: null,
                      targetValue: '', targetMin: '', targetMax: '', unitCode: '',
                    });
                    objectiveOperation.current = null;
                  }}>Annulla modifica obiettivo</button>
                ) : (
                  <button type="button" onClick={() => {
                    setObjectiveComposerOpen(false);
                    setObjectiveDraft({ label: '', resultKind: 'boolean', comparatorCode: null,
                      targetValue: '', targetMin: '', targetMax: '', unitCode: '' });
                  }}>Annulla</button>
                )}
              </fieldset>
              )}
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
              </div>
            </section>
            </section>
            <div className="timeline-activity-editor__location">
            <input className="temporal-create-u2-location" aria-label="Località"
              placeholder="Località"
              value={draft.location}
              onChange={(event) => {
                operation.current = undefined;
                setDraft({ ...draft, location: event.target.value });
              }}
            />
            </div>
             {settings.reminderScheduleRef ? (
              <TemporalReminderControl value={reminderLeadMinutes}
                onChange={(value) => {
                  operation.current = undefined;
                  setReminderLeadMinutes(value);
                }} />
            ) : null}
          </>
        ) : null}
        <section className="timeline-activity-editor__description temporal-create-section is-wide temporal-create-description-section" aria-label="Descrizione">
          <h3>Descrizione</h3>
            <textarea className="temporal-create-u2-description temporal-create-advanced-description"
              aria-label="Descrizione" placeholder="Descrizione" rows={5}
              value={draft.description}
              onChange={(event) => {
                operation.current = undefined;
                setDraft({ ...draft, description: event.target.value });
              }}
            />
        </section>
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
        className="timeline-activity-editor__actions dante-temporal-panel-actions"
        inert={confirmingDiscard || undefined}
      >
        <button type="button" disabled={pending || planPending || lockPending ||
          areaPending || objectivePending || !!namePending} onClick={requestClose}>
          Annulla
        </button>
        <button
          type="submit"
          className="is-primary"
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
