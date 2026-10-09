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
  type ActivityNewInterval,
  type ActivityNewPlanned,
  type ActivityReplanDraft,
  type ActivityReplanTime,
  type ActivityEditSettings,
  type ActivityLifeAreaChoice,
} from '../../../temporal/remote-activity-edit-settings';
import {
  createRemoteRealityObjectiveDataSource,
  type ObjectiveAssessment,
  type ObjectiveView,
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
import {
  ActivityObjectiveRow,
  existingObjectiveDraft,
  newObjectiveDraft,
  objectiveChanged,
  objectiveData,
  objectiveDraftError,
  type ActivityObjectiveDraft,
} from './activity-objective-row';

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

function planValidation(settings: ActivityEditSettings, draft: ActivityReplanDraft) {
  const errors: Record<string, string> = {};
  const spans: { ref: string; start: string; end: string }[] = [];
  const check = (ref: string, start: string, end: string) => {
    start = start.slice(0, 16);
    end = end.slice(0, 16);
    if (!start || !end) errors[ref] = 'Completa l’orario.';
    else if (end <= start) errors[ref] = 'La fine deve seguire l’inizio.';
    else spans.push({ ref, start, end });
  };
  const intervals = settings.schedules.filter((row) => row.role === 'interval' &&
    !draft.removedIntervals.includes(row.scheduleRef));
  const root = settings.schedules.find((row) => row.role === 'envelope');
  const bounds = settings.schedules.some((row) => row.role === 'interval')
    ? intervals.map((row) => ({ ref: row.scheduleRef,
        start: (draft.times[row.scheduleRef]?.start ?? '').slice(0, 16),
        end: (draft.times[row.scheduleRef]?.end ?? '').slice(0, 16) }))
      .concat(draft.newIntervals.map((row) => ({ ref: row.clientRef,
        start: row.start.slice(0, 16), end: row.end.slice(0, 16) })))
    : root ? [{ ref: root.scheduleRef,
        start: (draft.times[root.scheduleRef]?.start ?? '').slice(0, 16),
        end: (draft.times[root.scheduleRef]?.end ?? '').slice(0, 16) }] : [];
  bounds.forEach(({ ref, start, end }) => check(ref, start, end));
  const orderedBounds = bounds.filter((row) => !errors[row.ref]).sort((a, b) =>
    a.start.localeCompare(b.start));
  for (let i = 1; i < orderedBounds.length; i++) {
    if (orderedBounds[i - 1]!.end > orderedBounds[i]!.start) {
      errors[orderedBounds[i]!.ref] = 'Intervalli sovrapposti.';
    }
  }
  const planned = settings.schedules.filter((row) => row.role === 'planned' &&
    !draft.removedPlanned.includes(row.scheduleRef) &&
    !draft.deletedPlanned?.includes(row.scheduleRef) &&
    (row.placementStateRef !== null || !!draft.times[row.scheduleRef]?.start))
    .map((row) => ({ ref: row.scheduleRef,
      start: (draft.times[row.scheduleRef]?.start ?? '').slice(0, 16),
      end: (draft.times[row.scheduleRef]?.end ?? '').slice(0, 16) }))
    .concat(draft.newPlanned.filter((row) => !!row.start || !!row.end)
      .map((row) => ({ ref: row.clientRef,
        start: row.start.slice(0, 16), end: row.end.slice(0, 16) })));
  planned.forEach(({ ref, start, end }) => check(ref, start, end));
  if (orderedBounds.length && bounds.length === orderedBounds.length) {
    const min = orderedBounds[0]!.start;
    const max = orderedBounds[orderedBounds.length - 1]!.end;
    for (const row of planned) {
      if (!errors[row.ref] && (row.start < min || row.end > max)) {
        errors[row.ref] = 'Fuori dall’orario dell’attività.';
      }
    }
  }
  const orderedPlanned = spans.filter((row) => planned.some((item) => item.ref === row.ref))
    .sort((a, b) => a.start.localeCompare(b.start));
  for (let i = 1; i < orderedPlanned.length; i++) {
    if (orderedPlanned[i - 1]!.end > orderedPlanned[i]!.start) {
      errors[orderedPlanned[i]!.ref] = 'Sessioni sovrapposte.';
    }
  }
  return errors;
}

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
  const [lockError, setLockError] = useState('');
  const [areaChoice, setAreaChoice] = useState<ActivityLifeAreaChoice | null>(null);
  const [selectedArea, setSelectedArea] = useState('');
  const [areaQuery, setAreaQuery] = useState('');
  const [plannedNames, setPlannedNames] = useState<Record<string, string>>({});
  const [nameError, setNameError] = useState('');
  const [areaError, setAreaError] = useState('');
  const areaOperation = useRef<string | null>(null);
  const areaCreateOperation = useRef<string | null>(null);
  const [planDraft, setPlanDraft] = useState<Record<string, ActivityReplanTime>>({});
  const [newPlanned, setNewPlanned] = useState<ActivityNewPlanned[]>([]);
  const [removedPlanned, setRemovedPlanned] = useState<string[]>([]);
  const [deletedPlanned, setDeletedPlanned] = useState<string[]>([]);
  const [newIntervals, setNewIntervals] = useState<ActivityNewInterval[]>([]);
  const [removedIntervals, setRemovedIntervals] = useState<string[]>([]);
  const [objectiveRows, setObjectiveRows] = useState<ActivityObjectiveDraft[]>([]);
  const [removedObjectives, setRemovedObjectives] = useState<string[]>([]);
  const [expandedObjective, setExpandedObjective] = useState<string | null>(null);
  const [objectivePending, setObjectivePending] = useState(false);
  const [objectiveError, setObjectiveError] = useState('');
  const [correctingObjective, setCorrectingObjective] = useState<ObjectiveView | null>(null);
  const [correctedValue, setCorrectedValue] = useState('');
  const [correctedBoolean, setCorrectedBoolean] = useState('true');
  const [correctedAssessment, setCorrectedAssessment] = useState<ObjectiveAssessment>('unknown');
  const correctionOperation = useRef<string | null>(null);
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
    schedule.role === 'interval' || (schedule.role === 'planned' && !!schedule.start && !!schedule.end) ||
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
      ['floating_local', 'named_zone_local'].includes(schedule.temporalForm ?? '') &&
      !!schedule.start && !!schedule.end);
  const planDirty = canReplan && (
    removedIntervals.length > 0 || newIntervals.length > 0 ||
    removedPlanned.length > 0 || newPlanned.length > 0 ||
    deletedPlanned.length > 0 ||
    (settings?.schedules.some((schedule) => schedule.role === 'planned' &&
      schedule.placementStateRef === null && !deletedPlanned.includes(schedule.scheduleRef) &&
      !!planDraft[schedule.scheduleRef]?.start) ?? false) ||
    editablePlan.some((schedule) =>
      !removedPlanned.includes(schedule.scheduleRef) &&
      !deletedPlanned.includes(schedule.scheduleRef) &&
      !removedIntervals.includes(schedule.scheduleRef) && (
        planDraft[schedule.scheduleRef]?.start !== schedule.start ||
        planDraft[schedule.scheduleRef]?.end !== schedule.end
      ))
  );
  const replanDraft = {
    times: planDraft, removedIntervals, newIntervals, removedPlanned,
    deletedPlanned, newPlanned,
  };
  const planErrors = settings && canReplan && planDirty
    ? planValidation(settings, replanDraft) : {};
  const lockDirty = settings !== null && settings.placementLockScheduleRef !== null &&
    placementProtected !== null && placementProtected !== settings.placementProtected;
  const newAreaName = areaQuery.trim().replace(/\s+/g, ' ');
  const creatingArea = !!newAreaName && !selectedArea &&
    !areaChoice?.options.some((area) => area.name.toLocaleLowerCase() ===
      newAreaName.toLocaleLowerCase());
  const areaDirty = areaChoice !== null &&
    (creatingArea || (selectedArea || null) !== areaChoice.currentRef);
  const areaQueryValid = !areaQuery || !!areaChoice?.options.some((area) =>
    area.ref === selectedArea && area.name.toLocaleLowerCase() ===
      newAreaName.toLocaleLowerCase()) || creatingArea;
  const scopedDomainUnsupported = !!recurringContext && editScope === 'this_and_following';
  const nameDirty = !!settings && settings.schedules.some((schedule) =>
    schedule.role === 'planned' && (plannedNames[schedule.scheduleRef] ?? '') !== (schedule.name ?? ''));
  const objectiveDirty = removedObjectives.length > 0 ||
    objectiveRows.some((row) => !removedObjectives.includes(row.id) && objectiveChanged(row));
  const dirty = coreDirty || planDirty || lockDirty || areaDirty || objectiveDirty || nameDirty;

  const loadSettings = useCallback(() => {
    return settingsSource
      .load(profile.activityRef)
      .then((loaded) => {
        setSettings(loaded);
        setObjectiveRows(loaded.objectives.map(existingObjectiveDraft));
        setRemovedObjectives([]);
        setExpandedObjective(null);
        setObjectiveError('');
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
        setDeletedPlanned([]);
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
    if (pending || planPending || objectivePending) return;
    if (confirmingDiscard) {
      setConfirmingDiscard(false);
    } else if (dirty) {
      setConfirmingDiscard(true);
    } else {
      onCancel();
    }
  }, [confirmingDiscard, dirty, onCancel, objectivePending, pending, planPending]);

  const patchObjective = (id: string, patch: Partial<ActivityObjectiveDraft>) => {
    setObjectiveRows((rows) => rows.map((row) => row.id === id
      ? { ...row, ...patch, operationId: crypto.randomUUID(), revisionBasis: null } : row));
    setObjectiveError('');
  };

  const toggleObjective = (row: ActivityObjectiveDraft) => {
    setExpandedObjective((current) => current === row.id ? null : row.id);
    if (row.objectiveRef && !row.seriesState) {
      void objectiveSource.getSeriesState(row.objectiveRef).then((series) => {
        setObjectiveRows((rows) => rows.map((item) => item.id === row.id
          ? { ...item, seriesState: series } : item));
      }).catch((reason: unknown) => {
        setObjectiveError(reason instanceof Error
          ? reason.message : 'Impossibile verificare la ricorrenza dell’obiettivo.');
      });
    }
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

  const saveObjectiveRows = async (currentSettings: ActivityEditSettings) => {
    if (!objectiveDirty) return currentSettings;
    const retained = objectiveRows.filter((row) => !removedObjectives.includes(row.id));
    for (const row of retained) {
      const error = objectiveDraftError(row);
      if (error) throw new Error(`${row.label.trim() || 'Nuovo obiettivo'}: ${error}`);
    }
    const updated = retained.filter((row) => row.objectiveRef && objectiveChanged(row));
    const retired = objectiveRows.filter((row) =>
      row.objectiveRef && removedObjectives.includes(row.id));
    const changed = [...updated, ...retired];
    const definitions = await Promise.all(changed.map(async (row) => {
      if (row.revisionBasis !== null) {
        return { definitionRevision: row.revisionBasis };
      }
      const current = await objectiveSource.getDefinition(row.objectiveRef!);
      const original = row.original!;
      if (current.label !== original.label ||
          current.resultKind !== original.resultKind ||
          current.comparatorCode !== original.comparatorCode ||
          current.targetValue !== original.targetValue ||
          current.targetMin !== original.targetMin ||
          current.targetMax !== original.targetMax ||
          current.unitCode !== original.unitCode ||
          current.presentationOrder !== original.presentationOrder) {
        throw new Error('Un obiettivo è cambiato: riapri Modifica prima di salvare.');
      }
      return current;
    }));
    setObjectiveRows((rows) => rows.map((row) => {
      const index = changed.findIndex((item) => item.id === row.id);
      return index >= 0 && row.operationId === changed[index]!.operationId
        ? { ...row, revisionBasis: definitions[index]!.definitionRevision } : row;
    }));
    const revisions = definitions.slice(0, updated.length);
    const retireRevisions = definitions.slice(updated.length);
    const saved = await objectiveSource.applyActivityEdits(profile.activityRef, {
      add: retained.filter((row) => !row.objectiveRef).map((row) => ({
        ...objectiveData(row), operationId: row.operationId,
      })),
      revise: updated.map((row, index) => ({
        objectiveRef: row.objectiveRef!,
        change: {
          ...objectiveData(row), operationId: row.operationId,
          expectedRevision: revisions[index]!.definitionRevision,
          scopeCode: row.scope, seriesState: row.seriesState,
        },
      })),
      retire: retired.map((row, index) => ({
        objectiveRef: row.objectiveRef!,
        operationId: row.operationId,
        expectedRevision: retireRevisions[index]!.definitionRevision,
      })),
    });
    const next = { ...currentSettings, objectives: saved };
    setSettings(next);
    setObjectiveRows(saved.map(existingObjectiveDraft));
    setRemovedObjectives([]);
    setExpandedObjective(null);
    return next;
  };

  const changePlan = (ref: string, field: keyof ActivityReplanTime, value: string) => {
    setPlanDraft((current) => ({ ...current,
      [ref]: { start: current[ref]?.start ?? '', end: current[ref]?.end ?? '', [field]: value },
    }));
    setPlanOperation(null);
                    setPlanError('');
    setPlanError('');
  };

  const changeNewInterval = (
    ref: string, field: keyof ActivityReplanTime, value: string,
  ) => {
    setNewIntervals((current) => current.map((item) =>
      item.clientRef === ref ? { ...item, [field]: value } : item));
    setPlanOperation(null);
    setPlanError('');
  };

  const changeNewPlanned = (ref: string, field: 'start' | 'end' | 'name', value: string) => {
    setNewPlanned((current) => current.map((item) => item.clientRef === ref
      ? { ...item, [field]: value } : item));
    setPlanOperation(null);
    setPlanError('');
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
          pending || planPending || objectivePending ||
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
        if (planDirty && Object.keys(planErrors).length) return;
        if (areaDirty && (!areaQueryValid || scopedDomainUnsupported)) {
          setAreaError('Scegli una Life Area valida per questa attività.');
          return;
        }
        if (nameDirty && scopedDomainUnsupported) {
          setNameError('Per rinominare una Sessione scegli «Solo questa».');
          return;
        }
        setPending(true);
        setPlanPending(true);
        setError('');
        let errorHandled = false;
        void (async () => {
          let currentSettings = settings;
          if (lockDirty && placementProtected === false) {
            currentSettings = await settingsSource.setPlacementProtected(currentSettings, false)
              .catch((reason: unknown) => {
                errorHandled = true;
                setLockError(reason instanceof Error ? reason.message : 'Impossibile sbloccare.');
                throw reason;
              });
            setSettings(currentSettings);
          }
          if (planDirty) {
            setPlanError('');
            const operationId = planOperation ?? crypto.randomUUID();
            setPlanOperation(operationId);
            currentSettings = await settingsSource.applyReplan(profile.activityRef,
              currentSettings, replanDraft, operationId)
              .catch((reason: unknown) => {
                errorHandled = true;
                setPlanError(reason instanceof Error ? reason.message : 'Orario non salvato.');
                throw reason;
              });
            setSettings(currentSettings);
            setPlanDraft(Object.fromEntries(currentSettings.schedules.map((row) => [
              row.scheduleRef, { start: row.start ?? '', end: row.end ?? '' },
            ])));
            setNewPlanned([]);
            setRemovedPlanned([]);
            setDeletedPlanned([]);
            setNewIntervals([]);
            setRemovedIntervals([]);
            setPlanOperation(null);
          }
          for (const row of currentSettings.schedules.filter((item) => item.role === 'planned' &&
            (plannedNames[item.scheduleRef] ?? item.name ?? '') !== (item.name ?? ''))) {
            const next = plannedNames[row.scheduleRef]?.trim() || null;
            const saved = await settingsSource.revisePlannedName(profile.activityRef,
              row.scheduleRef, row.name, next).catch((reason: unknown) => {
                errorHandled = true;
                setNameError(reason instanceof Error ? reason.message : 'Nome non salvato.');
                throw reason;
              });
            currentSettings = { ...currentSettings, schedules: currentSettings.schedules.map(
              (item) => item.scheduleRef === row.scheduleRef ? { ...item, name: saved } : item) };
            setSettings(currentSettings);
            setPlannedNames((current) => ({ ...current, [row.scheduleRef]: saved ?? '' }));
          }
          if (areaDirty && areaChoice) {
            if (areaChoice.currentRef !== currentSettings.lifeAreaRef) {
              errorHandled = true;
              setAreaError('Life Area cambiata. Riapri Modifica.');
              throw new Error('Life Area cambiata. Riapri Modifica.');
            }
            let choice = areaChoice;
            let targetArea = selectedArea || null;
            if (creatingArea) {
              const created = await settingsSource.createLifeArea(
                newAreaName, areaCreateOperation.current ??= crypto.randomUUID(),
              ).catch((reason: unknown) => {
                errorHandled = true;
                setAreaError(reason instanceof Error ? reason.message : 'Life Area non creata.');
                throw reason;
              });
              targetArea = created.ref;
              choice = { ...choice, options: [...choice.options, created] };
              setAreaChoice(choice);
              setSelectedArea(created.ref);
              setAreaQuery(created.name);
              areaCreateOperation.current = null;
            }
            const saved = await settingsSource.assignLifeArea(profile.activityRef,
              choice, targetArea, areaOperation.current ??= crypto.randomUUID())
              .catch((reason: unknown) => {
                errorHandled = true;
                setAreaError(reason instanceof Error ? reason.message : 'Life Area non salvata.');
                throw reason;
              });
            areaOperation.current = null;
            setAreaChoice(saved);
            currentSettings = { ...currentSettings, lifeAreaRef: saved.currentRef };
            setSettings(currentSettings);
          }
          if (lockDirty && placementProtected === true) {
            currentSettings = await settingsSource.setPlacementProtected(currentSettings, true)
              .catch((reason: unknown) => {
                errorHandled = true;
                setLockError(reason instanceof Error ? reason.message : 'Blocco non salvato.');
                throw reason;
              });
            setSettings(currentSettings);
          }
          if (objectiveDirty) {
            currentSettings = await saveObjectiveRows(currentSettings).catch(
              (reason: unknown) => {
                errorHandled = true;
                setObjectiveError(reason instanceof Error
                  ? reason.message : 'Impossibile salvare gli obiettivi.');
                throw reason;
              },
            );
          }
          const changed = {
            title: draft.title.trim(),
            description: draft.description.trim() || null,
            location: draft.location.trim() || null,
            colorCode: draft.colorCode || null,
          };
          const metadataChanged = Object.entries(changed).some(
            ([key, value]) => value !== profile[key as keyof typeof changed],
          );
          const captureChanged = captureMode !== currentSettings.capture.mode;
          const realityChanged = realityMode !== currentSettings.reality.mode;
          const reminderChanged = reminderLeadMinutes !== currentSettings.reminderLeadMinutes;
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
          const saved = await settingsSource.saveCore(profile, currentSettings, {
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
            if (!errorHandled) setError(message);
          })
          .finally(() => {
            setPending(false);
            setPlanPending(false);
          });
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
                disabled={pending || planPending}
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
              {settings.schedules.filter((row) => row.role === 'planned' &&
                !deletedPlanned.includes(row.scheduleRef)).map((row) => {
                const removed = removedPlanned.includes(row.scheduleRef);
                const currentStart = planDraft[row.scheduleRef]?.start ?? row.start ?? '';
                const currentEnd = planDraft[row.scheduleRef]?.end ?? row.end ?? '';
                const hasTime = !removed && (row.placementStateRef !== null || !!currentStart);
                return (
                  <div className="temporal-create-tree-item is-session is-root"
                    key={row.scheduleRef} data-edit-planned-session={row.scheduleRef}>
                    <div className="temporal-create-tree-row">
                      <span className="temporal-create-tree-row__icon" aria-hidden="true">▶</span>
                      <span className="temporal-create-tree-row__divider" aria-hidden="true" />
                      <input className="temporal-create-tree-row__title" maxLength={300}
                        aria-label="Nome Sessione" placeholder="Nome Sessione"
                        disabled={removed || pending || planPending}
                        value={plannedNames[row.scheduleRef] ?? ''}
                        onChange={(event) => {
                          const value = event.currentTarget.value;
                          setPlannedNames((current) => ({
                            ...current, [row.scheduleRef]: value,
                          }));
                          setNameError('');
                        }} />
                      <div className="temporal-create-tree-row__actions">
                        <button type="button" className={hasTime ? 'is-active' : undefined}
                          aria-expanded={hasTime} aria-controls={`edit-session:${row.scheduleRef}:time`}
                          disabled={!canReplan || planPending}
                          onClick={() => {
                            if (row.placementStateRef !== null) {
                              setRemovedPlanned((current) => current.includes(row.scheduleRef)
                                ? current.filter((ref) => ref !== row.scheduleRef)
                                : [...current, row.scheduleRef]);
                            } else {
                              const root = settings.schedules.find((schedule) => schedule.role === 'envelope');
                              setPlanDraft((current) => ({ ...current, [row.scheduleRef]: hasTime
                                ? { start: '', end: '' }
                                : { start: root?.start?.slice(0, 16) ?? '',
                                    end: root?.end?.slice(0, 16) ?? '' },
                              }));
                            }
                              setPlanOperation(null);
                            setPlanError('');
                          }}>Orario</button>
                        <button type="button" className="is-remove" aria-label="Rimuovi Sessione"
                          disabled={!canReplan || pending || planPending}
                          onClick={() => {
                            setDeletedPlanned((current) => [...current, row.scheduleRef]);
                            setRemovedPlanned((current) => current.filter((ref) => ref !== row.scheduleRef));
                            setPlanOperation(null);
                            setPlanError('');
                          }}>×</button>
                      </div>
                    </div>
                    {hasTime ? (
                      <div id={`edit-session:${row.scheduleRef}:time`}
                        className="temporal-create-tree-time-editor" inert={planPending || undefined}
                        data-edit-invalid={!!planErrors[row.scheduleRef]}>
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
                        {planErrors[row.scheduleRef] ? <small className="temporal-create-field-error" role="alert">
                          {planErrors[row.scheduleRef]}</small> : null}
                      </div>
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
                      <button type="button" className={item.start ? 'is-active' : undefined}
                        aria-expanded={!!item.start}
                        aria-controls={`edit-session:${item.clientRef}:time`}
                        disabled={planPending}
                        onClick={() => {
                          const root = settings.schedules.find((row) => row.role === 'envelope');
                          setNewPlanned((current) => current.map((row) => row.clientRef === item.clientRef
                            ? { ...row, start: row.start ? '' : root?.start?.slice(0, 16) ?? '',
                                end: row.start ? '' : root?.end?.slice(0, 16) ?? '' } : row));
                          setPlanOperation(null);
                        }}>Orario</button>
                      <button type="button" className="is-remove" aria-label="Rimuovi Sessione"
                        disabled={planPending} onClick={() => {
                          setNewPlanned((current) => current.filter((row) => row.clientRef !== item.clientRef));
                          setPlanOperation(null);
                        }}>×</button>
                    </div>
                  </div>
                  {item.start ? <div id={`edit-session:${item.clientRef}:time`}
                    className="temporal-create-tree-time-editor" data-edit-invalid={!!planErrors[item.clientRef]}>
                    <TemporalCreateDatePicker label="Data Sessione" locale="it" value={item.start.slice(0, 10)}
                      onChange={(date) => changeNewPlanned(item.clientRef, 'start',
                        `${date}${item.start.slice(10, 16)}`)} />
                    <TimeControl label="Inizio Sessione" dataPath={`newStart-${item.clientRef}`}
                      value={item.start.slice(11, 16)} onChange={(time) => changeNewPlanned(item.clientRef,
                        'start', `${item.start.slice(0, 10)}T${time}`)} />
                    <TimeControl label="Fine Sessione" dataPath={`newEnd-${item.clientRef}`}
                      value={item.end.slice(11, 16)} onChange={(time) => changeNewPlanned(item.clientRef,
                        'end', `${item.end.slice(0, 10)}T${time}`)} />
                    {planErrors[item.clientRef] ? <small className="temporal-create-field-error" role="alert">
                      {planErrors[item.clientRef]}</small> : null}
                  </div> : null}
                </div>
              ))}
            </div>
          </section>
        ) : null}
        {canReplan ? (
          <button type="button" className="temporal-create-structure-add timeline-activity-editor__add-session"
            disabled={planPending || settings.schedules.filter((row) => row.role === 'planned' &&
              !deletedPlanned.includes(row.scheduleRef)).length +
              newPlanned.length >= 100}
            onClick={() => {
              setNewPlanned((current) => [...current, {
                clientRef: crypto.randomUUID(), name: '',
                start: '', end: '',
              }]);
              setPlanOperation(null);
            }}>＋ Sessione</button>
        ) : null}
        {settings ? (
          <>
            <section
              className="timeline-activity-editor__readback"
              aria-label="Programmazione attuale"
            >
              <div className="timeline-activity-editor__placement" role="group" aria-label="Collocazione attuale">
                <span className={settings.schedules.some((row) => row.role === 'envelope' &&
                    row.temporalForm !== null && row.temporalForm !== 'date_span') ? 'is-selected' : ''}>Orario</span>
                <span className={settings.schedules.some((row) => row.role === 'envelope' &&
                    row.temporalForm === 'date_span') ? 'is-selected' : ''}>Tutto il giorno</span>
                <span className={!settings.schedules.some((row) => row.role === 'envelope' &&
                    row.placementStateRef !== null) ? 'is-selected' : ''}>Da collocare</span>
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
                          inert={planPending || undefined}
                          data-edit-invalid={!!planErrors[schedule.scheduleRef]}>
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
                          {planErrors[schedule.scheduleRef] ? <small className="temporal-create-field-error" role="alert">
                            {planErrors[schedule.scheduleRef]}</small> : null}
                        </div>
                      ) : null}
                      {canReplan && schedule.role === 'interval' ? (
                        <button type="button" disabled={planPending} onClick={() => {
                          setRemovedIntervals((current) =>
                            current.includes(schedule.scheduleRef)
                              ? current.filter((ref) => ref !== schedule.scheduleRef)
                              : [...current, schedule.scheduleRef]);
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
                    <div key={item.clientRef} className="timeline-activity-editor__fields"
                      data-edit-invalid={!!planErrors[item.clientRef]}>
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
                        setPlanOperation(null);
                        setPlanError('');
                      }}>Rimuovi nuovo intervallo</button>
                      {planErrors[item.clientRef] ? <small role="alert" className="temporal-create-field-error">
                        {planErrors[item.clientRef]}</small> : null}
                    </div>
                  ))}
                  {hasIntervals ? <button type="button" disabled={planPending ||
                    editablePlan.filter((row) => row.role === 'interval').length -
                      removedIntervals.length + newIntervals.length >= 100}
                    onClick={() => {
                      setNewIntervals((current) => [...current, {
                        clientRef: crypto.randomUUID(), start: '', end: '',
                      }]);
                              setPlanOperation(null);
                      setPlanError('');
                    }}>Aggiungi intervallo</button> : null}
                </div>
              ) : null}
              {planDirty ? (
                <div>
                  <button type="button" disabled={planPending} onClick={() => {
                    setPlanDraft(Object.fromEntries(settings.schedules.map((schedule) => [
                      schedule.scheduleRef,
                      { start: schedule.start ?? '', end: schedule.end ?? '' },
                    ])));
                    setNewPlanned([]);
                    setRemovedPlanned([]);
                    setDeletedPlanned([]);
                    setNewIntervals([]);
                    setRemovedIntervals([]);
                          setPlanOperation(null);
                  }}>Ripristina orari</button>
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
                    disabled={pending || planPending}
                    onQueryChange={(query) => {
                      setAreaQuery(query);
                      setSelectedArea(areaChoice.options.find((area) =>
                        area.name.toLocaleLowerCase() === query.trim().toLocaleLowerCase())?.ref ?? '');
                      areaOperation.current = null;
                      areaCreateOperation.current = null;
                      setAreaError('');
                    }}
                    onChoose={(area) => {
                      setSelectedArea(area.id);
                      setAreaQuery(area.label);
                      areaOperation.current = null;
                      setAreaError('');
                    }}
                    onClear={() => {
                      setSelectedArea(''); setAreaQuery(''); setAreaError('');
                      areaCreateOperation.current = null;
                    }} />
                  {creatingArea ? <small>La nuova Life Area verrà creata quando salvi.</small> : null}
                  {!areaQueryValid ? <small>Scegli una Life Area dall’elenco.</small> : null}
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
                {objectiveRows.filter((row) => !removedObjectives.includes(row.id))
                  .map((row) => (
                    <ActivityObjectiveRow key={row.id} row={row}
                      expanded={expandedObjective === row.id}
                      disabled={pending || planPending || objectivePending}
                      onToggle={() => toggleObjective(row)}
                      onChange={(patch) => patchObjective(row.id, patch)}
                      onRemove={() => {
                        if (row.objectiveRef) {
                          setRemovedObjectives((current) => [...current, row.id]);
                        } else {
                          setObjectiveRows((current) =>
                            current.filter((item) => item.id !== row.id));
                        }
                        setObjectiveError('');
                      }} />
                  ))}
                {removedObjectives.length > 0 ? (
                  <button type="button" onClick={() => {
                    setRemovedObjectives([]);
                    setObjectiveError('');
                  }} disabled={pending || planPending}>
                    Ripristina obiettivi rimossi
                  </button>
                ) : null}
                <button type="button" className="timeline-activity-editor__add-objective"
                  disabled={pending || planPending || objectivePending}
                  onClick={() => {
                    const next = newObjectiveDraft(
                      Math.max(-1, ...objectiveRows.map((row) => row.presentationOrder)) + 1,
                    );
                    setObjectiveRows((rows) => [...rows, next]);
                    setExpandedObjective(next.id);
                    setObjectiveError('');
                  }}>
                  ＋ Aggiungi obiettivo
                </button>
                {objectiveError ? <p role="alert">{objectiveError}</p> : null}
                {settings.objectives.filter((row) => row.observationRef).map((row) => (
                  <div key={row.objectiveRef}>
                    <span>{row.label} · risultato registrato</span>
                    <button type="button" disabled={objectivePending || pending}
                      onClick={() => startResultCorrection(row)}>Correggi risultato</button>
                  </div>
                ))}
              </div>
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
              aria-label="Descrizione" rows={5}
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
        <button type="button" disabled={pending || planPending || objectivePending} onClick={requestClose}>
          Annulla
        </button>
        <button
          type="submit"
          className="is-primary"
          disabled={
            pending || planPending || objectivePending ||
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
