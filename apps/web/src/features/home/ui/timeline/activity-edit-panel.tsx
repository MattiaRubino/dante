import {
  useCallback,
  useEffect,
  useRef,
  useState,
  type RefObject,
} from 'react';
import { Temporal, detectDeviceTimeZone } from '@dante/time';

import {
  createRemoteActivityInspector,
  type ActivityProfile,
  type ActivitySessionImpact,
} from '../../../temporal/remote-activity-inspector';
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
  type ActivityObjectiveBatch,
  type ObjectiveAssessment,
  type ObjectiveView,
  type RealityMode,
} from '../../../temporal/remote-reality-objective-data-source';
import type { SessionCaptureMode } from '../../../temporal/remote-session-capability-data-source';
import {
  createRemoteTemporalSessionDataSource,
  type TemporalSessionView,
} from '../../../temporal/remote-session-data-source';
import { TemporalColorControl } from '../../../temporal-create/ui/temporal-color-control';
import { TimeControl } from '../../../temporal-create/ui/temporal-create-core-u2';
import { TemporalCreateDatePicker } from '../../../temporal-create/ui/temporal-create-date-picker';
import { TemporalAuthoringTitleRow } from '../../../temporal-create/ui/temporal-authoring-title-row';
import { TemporalCreatePlacementLockButton } from '../../../temporal-create/ui/temporal-create-placement-lock-button';
import { createRemoteExistingRecurrence } from '../../../temporal/remote-existing-recurrence';
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
import '../../../temporal-create/ui/temporal-create-activity-polish.css';
import '../../../temporal-create/ui/temporal-create-advanced-activity-structure.css';
import '../../../temporal-create/ui/temporal-create-session-time-polish.css';
import './activity-edit-panel.css';
import '../../../temporal-create/ui/temporal-editor-section-typography.css';
import {
  ExistingRecurrenceControl,
  type ExistingRecurrenceControlHandle,
} from './existing-recurrence-control';
import { SessionAttemptDeleteDialog } from './session-attempt-delete-dialog';
import { ObjectiveRecordingDeleteDialog } from './objective-recording-delete-dialog';
import { UnsavedChangesDialog } from './unsaved-changes-dialog';
import {
  createRemoteRecurringProfileEdit,
  type RecurringProfileContext,
  type RecurringProfileEditScope,
  type RecurringProfileEditPreview,
} from '../../../temporal/remote-recurring-profile-edit';

function planValidation(
  settings: ActivityEditSettings,
  draft: ActivityReplanDraft,
) {
  const errors: Record<string, string> = {};
  if (draft.dateSpan) {
    const { startDate, endDateExclusive } = draft.dateSpan;
    if (!startDate || !endDateExclusive || endDateExclusive <= startDate) {
      errors.dateSpan = 'La fine deve seguire l’inizio.';
    }
    return errors;
  }
  const spans: { ref: string; start: string; end: string }[] = [];
  const check = (ref: string, start: string, end: string) => {
    start = start.slice(0, 16);
    end = end.slice(0, 16);
    if (!start || !end) errors[ref] = 'Completa l’orario.';
    else if (end <= start) errors[ref] = 'La fine deve seguire l’inizio.';
    else spans.push({ ref, start, end });
  };
  const intervals = settings.schedules.filter(
    (row) =>
      row.role === 'interval' &&
      !draft.removedIntervals.includes(row.scheduleRef),
  );
  const root = settings.schedules.find((row) => row.role === 'envelope');
  const bounds = settings.schedules.some((row) => row.role === 'interval')
    ? intervals
        .map((row) => ({
          ref: row.scheduleRef,
          start: (draft.times[row.scheduleRef]?.start ?? '').slice(0, 16),
          end: (draft.times[row.scheduleRef]?.end ?? '').slice(0, 16),
        }))
        .concat(
          draft.newIntervals.map((row) => ({
            ref: row.clientRef,
            start: row.start.slice(0, 16),
            end: row.end.slice(0, 16),
          })),
        )
    : root
      ? [
          {
            ref: root.scheduleRef,
            start: (draft.times[root.scheduleRef]?.start ?? '').slice(0, 16),
            end: (draft.times[root.scheduleRef]?.end ?? '').slice(0, 16),
          },
        ].concat(
          draft.newIntervals.map((row) => ({
            ref: row.clientRef,
            start: row.start.slice(0, 16),
            end: row.end.slice(0, 16),
          })),
        )
      : [];
  bounds.forEach(({ ref, start, end }) => check(ref, start, end));
  const orderedBounds = bounds
    .filter((row) => !errors[row.ref])
    .sort((a, b) => a.start.localeCompare(b.start));
  for (let i = 1; i < orderedBounds.length; i++) {
    if (orderedBounds[i - 1]!.end > orderedBounds[i]!.start) {
      errors[orderedBounds[i]!.ref] = 'Intervalli sovrapposti.';
    }
  }
  return errors;
}

function recordedClock(value: string, zone?: string): string {
  return new Intl.DateTimeFormat('it-IT', {
    hour: '2-digit',
    minute: '2-digit',
    ...(zone ? { timeZone: zone } : {}),
  }).format(new Date(value));
}

function recordedDuration(seconds: number): string {
  const whole = Math.max(0, Math.floor(seconds));
  return [Math.floor(whole / 3600), Math.floor((whole % 3600) / 60), whole % 60]
    .map((part) => String(part).padStart(2, '0'))
    .join(':');
}

function shiftedDate(value: string, days: number): string {
  if (!value) return '';
  try {
    return Temporal.PlainDate.from(value).add({ days }).toString();
  } catch {
    return '';
  }
}

function nextIntervalAfter(value: string): ActivityReplanTime {
  const start = Temporal.PlainDateTime.from(value.slice(0, 16)).add({
    minutes: 30,
  });
  return {
    start: start.toString({ smallestUnit: 'minute' }),
    end: start.add({ hours: 1 }).toString({ smallestUnit: 'minute' }),
  };
}

function ActivityIntervalFields({
  value,
  onChange,
  onRemove,
  removeLabel,
  error,
  disabled,
}: Readonly<{
  value: ActivityReplanTime;
  onChange: (field: keyof ActivityReplanTime, value: string) => void;
  onRemove?: () => void;
  removeLabel?: string;
  error?: string | undefined;
  disabled: boolean;
}>) {
  return (
    <div
      className="temporal-create-activity-interval__fields timeline-activity-editor__interval-fields"
      data-edit-invalid={!!error}
      inert={disabled || undefined}
    >
      <TemporalCreateDatePicker
        label="Data inizio"
        locale="it"
        value={value.start.slice(0, 10)}
        onChange={(date) =>
          onChange('start', `${date}T${value.start.slice(11, 16)}`)
        }
      />
      <TimeControl
        label="Inizio"
        value={value.start.slice(11, 16)}
        dataPath="editInterval.startTime"
        onChange={(time) =>
          onChange('start', `${value.start.slice(0, 10)}T${time}`)
        }
      />
      <span
        className="temporal-create-activity-interval__arrow"
        aria-hidden="true"
      >
        →
      </span>
      <TimeControl
        label="Fine"
        value={value.end.slice(11, 16)}
        dataPath="editInterval.endTime"
        onChange={(time) =>
          onChange('end', `${value.end.slice(0, 10)}T${time}`)
        }
      />
      <TemporalCreateDatePicker
        label="Data fine"
        align="end"
        locale="it"
        value={value.end.slice(0, 10)}
        onChange={(date) =>
          onChange('end', `${date}T${value.end.slice(11, 16)}`)
        }
      />
      {onRemove ? (
        <button
          type="button"
          className="temporal-create-activity-interval__remove"
          aria-label={removeLabel}
          title={removeLabel}
          onClick={onRemove}
        >
          ×
        </button>
      ) : null}
      {error ? (
        <small className="temporal-create-field-error" role="alert">
          {error}
        </small>
      ) : null}
    </div>
  );
}

export function ActivityEditPanel({
  profile,
  initialScope = 'only_this',
  timeZone,
  onSaved,
  onCancel,
  closeRequestRef,
}: Readonly<{
  profile: ActivityProfile;
  initialScope?: RecurringProfileEditScope;
  timeZone?: string;
  onSaved: (profile: ActivityProfile) => void;
  onCancel: () => void;
  closeRequestRef: RefObject<(() => void) | null>;
}>) {
  const [settingsSource] = useState(createRemoteActivityEditSettings);
  const [sessionSource] = useState(createRemoteTemporalSessionDataSource);
  const [sessionImpactSource] = useState(createRemoteActivityInspector);
  const [deletingAttempt, setDeletingAttempt] = useState<{
    attempt: TemporalSessionView;
    impact: ActivitySessionImpact;
  } | null>(null);
  const [attemptDeletePending, setAttemptDeletePending] = useState(false);
  const [attemptDeleteError, setAttemptDeleteError] = useState('');
  const [clockNow, setClockNow] = useState(() => Date.now());
  const [sessionAttempts, setSessionAttempts] = useState<
    readonly TemporalSessionView[] | null
  >(null);
  const [sessionAttemptsError, setSessionAttemptsError] = useState('');
  useEffect(() => {
    let active = true;
    const refresh = () => {
      void sessionSource
        .list('activity', profile.activityRef)
        .then((attempts) => {
          if (!active) return;
          setSessionAttempts(attempts);
          setSessionAttemptsError('');
        })
        .catch((reason: unknown) => {
          if (!active) return;
          setSessionAttempts(null);
          setSessionAttemptsError(
            reason instanceof Error
              ? reason.message
              : 'Impossibile leggere le Sessioni registrate.',
          );
        });
    };
    refresh();
    window.addEventListener('dante:session-changed', refresh);
    return () => {
      active = false;
      window.removeEventListener('dante:session-changed', refresh);
    };
  }, [profile.activityRef, sessionSource]);

  useEffect(() => {
    if (!sessionAttempts?.some((attempt) => attempt.open && !attempt.paused))
      return;
    const tick = window.setInterval(() => setClockNow(Date.now()), 1000);
    return () => window.clearInterval(tick);
  }, [sessionAttempts]);

  const attemptStatus = (attempt: TemporalSessionView) =>
    !attempt.open ? 'conclusa' : attempt.paused ? 'in pausa' : 'in corso';

  const requestAttemptDeletion = (attempt: TemporalSessionView) => {
    setAttemptDeletePending(true);
    setAttemptDeleteError('');
    void sessionImpactSource
      .sessionImpact(profile.activityRef)
      .then((impact) => {
        if (
          !impact.attempts.some((row) => row.sessionRef === attempt.sessionRef)
        ) {
          throw new Error('La registrazione è cambiata. Ricarica Modifica.');
        }
        setDeletingAttempt({ attempt, impact });
      })
      .catch((reason: unknown) =>
        setAttemptDeleteError(
          reason instanceof Error
            ? reason.message
            : 'Impossibile verificare la registrazione.',
        ),
      )
      .finally(() => setAttemptDeletePending(false));
  };

  const confirmAttemptDeletion = () => {
    if (!deletingAttempt) return;
    setAttemptDeletePending(true);
    setAttemptDeleteError('');
    void sessionImpactSource
      .deleteSessionAttempt(
        profile.activityRef,
        deletingAttempt.attempt.sessionRef,
        deletingAttempt.impact.fingerprint,
      )
      .then(() => sessionSource.list('activity', profile.activityRef))
      .then((attempts) => {
        setSessionAttempts(attempts);
        setDeletingAttempt(null);
      })
      .catch((reason: unknown) => {
        setDeletingAttempt(null);
        setAttemptDeleteError(
          reason instanceof Error
            ? reason.message
            : 'Impossibile eliminare la registrazione.',
        );
        void sessionSource
          .list('activity', profile.activityRef)
          .then(setSessionAttempts)
          .catch(() => setSessionAttempts(null));
      })
      .finally(() => setAttemptDeletePending(false));
  };

  const attemptLine = (attempt: TemporalSessionView) => {
    const activeSeconds =
      attempt.activeSeconds +
      (attempt.open && !attempt.paused
        ? Math.max(0, (clockNow - Date.parse(attempt.evaluatedAt)) / 1000)
        : 0);
    const period = attempt.endedAt
      ? `${recordedClock(attempt.startedAt, timeZone)}–${recordedClock(attempt.endedAt, timeZone)}`
      : `Avviata alle ${recordedClock(attempt.startedAt, timeZone)}`;
    return `${period} · ${attempt.open ? (attempt.paused ? 'In pausa' : 'In corso') : 'Totale attivo'} ${recordedDuration(activeSeconds)}`;
  };

  const attemptRecord = (attempt: TemporalSessionView) => (
    <div className="timeline-activity-editor__record" key={attempt.sessionRef}>
      <div className="timeline-activity-editor__record-content">
        <span className="timeline-activity-editor__record-state">
          {attemptStatus(attempt)}
        </span>
        <span>{attemptLine(attempt)}</span>
      </div>
      <button
        type="button"
        className="timeline-activity-editor__delete-trigger"
        disabled={pending || planPending || attemptDeletePending}
        aria-label={`Elimina registrazione ${attempt.sessionRef}`}
        onClick={() => requestAttemptDeletion(attempt)}
      >
        Elimina registrazione
      </button>
    </div>
  );

  const [objectiveSource] = useState(createRemoteRealityObjectiveDataSource);
  const [recurringSource] = useState(createRemoteRecurringProfileEdit);
  const [existingRecurrence] = useState(createRemoteExistingRecurrence);
  const recurrenceControl = useRef<ExistingRecurrenceControlHandle>(null);
  const recurrenceOperation = useRef<string | null>(null);
  const recurrenceResume = useRef<{
    profile: ActivityProfile;
    settings: ActivityEditSettings;
  } | null>(null);
  const [recurrenceSelected, setRecurrenceSelected] = useState(false);
  const [recurringContext, setRecurringContext] =
    useState<RecurringProfileContext | null>(null);
  const [recurringLoading, setRecurringLoading] = useState(true);
  const [recurringError, setRecurringError] = useState('');
  const [editScope, setEditScope] =
    useState<RecurringProfileEditScope>(initialScope);
  const [seriesPreview, setSeriesPreview] =
    useState<RecurringProfileEditPreview | null>(null);
  const [seriesPreviewError, setSeriesPreviewError] = useState('');
  const [settings, setSettings] = useState<ActivityEditSettings | null>(null);
  const [loadingSettings, setLoadingSettings] = useState(true);
  const [settingsError, setSettingsError] = useState('');
  const [captureMode, setCaptureMode] = useState<SessionCaptureMode | null>(
    null,
  );
  const [realityMode, setRealityMode] = useState<RealityMode | null>(null);
  const [reminderLeadMinutes, setReminderLeadMinutes] = useState<number | null>(
    null,
  );
  const [placementProtected, setPlacementProtected] = useState<boolean | null>(
    null,
  );
  const [lockError, setLockError] = useState('');
  const [areaChoice, setAreaChoice] = useState<ActivityLifeAreaChoice | null>(
    null,
  );
  const [selectedArea, setSelectedArea] = useState('');
  const [areaQuery, setAreaQuery] = useState('');
  const [plannedNames, setPlannedNames] = useState<Record<string, string>>({});
  const [nameError, setNameError] = useState('');
  const [areaError, setAreaError] = useState('');
  const [planDraft, setPlanDraft] = useState<
    Record<string, ActivityReplanTime>
  >({});
  const [allDay, setAllDay] = useState(false);
  const [dateSpanDraft, setDateSpanDraft] = useState({ start: '', end: '' });
  const [newPlanned, setNewPlanned] = useState<ActivityNewPlanned[]>([]);
  const [deletedPlanned, setDeletedPlanned] = useState<string[]>([]);
  const [newIntervals, setNewIntervals] = useState<ActivityNewInterval[]>([]);
  const [removedIntervals, setRemovedIntervals] = useState<string[]>([]);
  const [objectiveRows, setObjectiveRows] = useState<ActivityObjectiveDraft[]>(
    [],
  );
  const [removedObjectives, setRemovedObjectives] = useState<string[]>([]);
  const [objectivePending, setObjectivePending] = useState(false);
  const [objectiveError, setObjectiveError] = useState('');
  const [deletingObjective, setDeletingObjective] = useState<ObjectiveView | null>(null);
  const [objectiveDeletePending, setObjectiveDeletePending] = useState(false);
  const [correctingObjective, setCorrectingObjective] =
    useState<ObjectiveView | null>(null);
  const [correctedValue, setCorrectedValue] = useState('');
  const [correctedBoolean, setCorrectedBoolean] = useState('true');
  const [correctedAssessment, setCorrectedAssessment] =
    useState<ObjectiveAssessment>('unknown');
  const correctionOperation = useRef<string | null>(null);
  const loadedObjectiveOrigins = useRef(new Set<string>());
  const [areaColorOverride, setAreaColorOverride] = useState<string | null>(
    null,
  );
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
  const hasIntervals =
    settings?.schedules.some((schedule) => schedule.role === 'interval') ??
    false;
  const editablePlan =
    settings?.schedules.filter(
      (schedule) =>
        schedule.role === 'interval' ||
        (schedule.role === 'envelope' && !hasIntervals),
    ) ?? [];
  const envelope = settings?.schedules.find((row) => row.role === 'envelope');
  const originalAllDay = envelope?.temporalForm === 'date_span';
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
  const canReplan =
    !!settings &&
    !!envelope &&
    editablePlan.every(
      (schedule) =>
        ['floating_local', 'named_zone_local', 'date_span'].includes(
          schedule.temporalForm ?? '',
        ) &&
        !!schedule.start &&
        !!schedule.end,
    );
  // Completed named attempts are factual history, not a lock on future planning.
  // The generic capture setting still requires deleting every real attempt.
  const captureLocked = sessionAttempts === null || sessionAttempts.length > 0;
  const planningLocked =
    sessionAttempts === null ||
    sessionAttempts.some(
      (attempt) => !attempt.plannedScheduleRef || attempt.open,
    );
  const temporalDirty =
    canReplan &&
    (allDay !== originalAllDay ||
      (allDay &&
        (dateSpanDraft.start !== envelope?.start ||
          shiftedDate(dateSpanDraft.end, 1) !== envelope?.end)) ||
      removedIntervals.length > 0 ||
      newIntervals.length > 0 ||
      editablePlan.some(
        (schedule) =>
          !removedIntervals.includes(schedule.scheduleRef) &&
          (planDraft[schedule.scheduleRef]?.start !== schedule.start ||
            planDraft[schedule.scheduleRef]?.end !== schedule.end),
      ));
  const planDirty =
    canReplan &&
    (temporalDirty || newPlanned.length > 0 || deletedPlanned.length > 0);
  const replanDraft = {
    times: planDraft,
    ...(allDay
      ? {
          dateSpan: {
            startDate: dateSpanDraft.start,
            endDateExclusive: shiftedDate(dateSpanDraft.end, 1),
          },
        }
      : originalAllDay
        ? { targetZoneId: timeZone ?? detectDeviceTimeZone() }
        : {}),
    splitEnvelope: !hasIntervals && newIntervals.length > 0,
    removedIntervals,
    newIntervals,
    removedPlanned: [],
    deletedPlanned,
    newPlanned,
  };
  const planErrors =
    settings && canReplan && planDirty
      ? planValidation(settings, replanDraft)
      : {};
  const lockDirty =
    settings !== null &&
    settings.placementLockScheduleRef !== null &&
    placementProtected !== null &&
    placementProtected !== settings.placementProtected;
  const newAreaName = areaQuery.trim().replace(/\s+/g, ' ');
  const selectedAreaOption = areaChoice?.options.find(
    (area) => area.ref === selectedArea,
  );
  const selectedAreaColor =
    areaColorOverride ??
    (selectedArea
      ? (selectedAreaOption?.colorCode ?? '#616161')
      : draft.colorCode || '#EA5C12');
  const creatingArea =
    !!newAreaName &&
    !selectedArea &&
    !areaChoice?.options.some(
      (area) =>
        area.name.toLocaleLowerCase() === newAreaName.toLocaleLowerCase(),
    );
  const areaDirty =
    areaChoice !== null &&
    (creatingArea ||
      (selectedArea || null) !== areaChoice.currentRef ||
      (selectedArea !== '' &&
        areaColorOverride !== null &&
        areaColorOverride !== selectedAreaOption?.colorCode));
  const areaQueryValid =
    !areaQuery ||
    !!areaChoice?.options.some(
      (area) =>
        area.ref === selectedArea &&
        area.name.toLocaleLowerCase() === newAreaName.toLocaleLowerCase(),
    ) ||
    creatingArea;
  const scopedDomainUnsupported =
    !!recurringContext && editScope !== 'only_this';
  const nameDirty =
    !!settings &&
    settings.schedules.some(
      (schedule) =>
        schedule.role === 'planned' &&
        (plannedNames[schedule.scheduleRef] ?? '') !== (schedule.name ?? ''),
    );
  const objectiveDirty =
    removedObjectives.length > 0 ||
    objectiveRows.some(
      (row) => !removedObjectives.includes(row.id) && objectiveChanged(row),
    );
  const dirty =
    coreDirty ||
    planDirty ||
    lockDirty ||
    areaDirty ||
    objectiveDirty ||
    nameDirty ||
    recurrenceSelected;

  const loadSettings = useCallback(() => {
    return settingsSource
      .load(profile.activityRef)
      .then((loaded) => {
        setSettings(loaded);
        setObjectiveRows(loaded.objectives.map(existingObjectiveDraft));
        setRemovedObjectives([]);
        loadedObjectiveOrigins.current.clear();
        setObjectiveError('');
        setCaptureMode(loaded.capture.mode);
        setRealityMode(loaded.reality.mode);
        setReminderLeadMinutes(loaded.reminderLeadMinutes);
        setPlacementProtected(loaded.placementProtected);
        setLockError('');
        setPlanDraft(
          Object.fromEntries(
            loaded.schedules.map((schedule) => [
              schedule.scheduleRef,
              { start: schedule.start ?? '', end: schedule.end ?? '' },
            ]),
          ),
        );
        const root = loaded.schedules.find((row) => row.role === 'envelope');
        setAllDay(root?.temporalForm === 'date_span');
        setDateSpanDraft({
          start: root?.start?.slice(0, 10) ?? '',
          end: shiftedDate(
            root?.end?.slice(0, 10) ?? '',
            root?.temporalForm === 'date_span' ? -1 : 0,
          ),
        });
        setNewPlanned([]);
        setPlannedNames(
          Object.fromEntries(
            loaded.schedules
              .filter((row) => row.role === 'planned')
              .map((row) => [row.scheduleRef, row.name ?? '']),
          ),
        );
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
  }, [
    profile.activityRef,
    settingsSource,
    setSettings,
    setObjectiveRows,
    setRemovedObjectives,
    loadedObjectiveOrigins,
    setObjectiveError,
    setCaptureMode,
    setRealityMode,
    setReminderLeadMinutes,
    setPlacementProtected,
    setLockError,
    setPlanDraft,
    setAllDay,
    setDateSpanDraft,
    setNewPlanned,
    setPlannedNames,
    setDeletedPlanned,
    setNewIntervals,
    setRemovedIntervals,
    setSettingsError,
    setLoadingSettings,
  ]);

  useEffect(() => {
    void loadSettings();
  }, [loadSettings]);

  useEffect(() => {
    let active = true;
    queueMicrotask(() => {
      if (!active) return;
      setRecurringContext(null);
      setEditScope(initialScope);
      setRecurringLoading(true);
      setRecurringError('');
    });
    void recurringSource
      .loadActivityContext(profile.activityRef)
      .then((loaded) => {
        if (active) setRecurringContext(loaded);
      })
      .catch((reason: unknown) => {
        if (active)
          setRecurringError(
            reason instanceof Error
              ? reason.message
              : 'Origine della ricorrenza non disponibile.',
          );
      })
      .finally(() => {
        if (active) setRecurringLoading(false);
      });
    return () => {
      active = false;
    };
  }, [profile.activityRef, recurringSource, initialScope]);

  useEffect(() => {
    if (!recurringContext || editScope === 'only_this') return;
    let active = true;
    queueMicrotask(() => {
      if (active) {
        setSeriesPreview(null);
        setSeriesPreviewError('');
      }
    });
    void recurringSource
      .loadPreview(recurringContext, editScope)
      .then((preview) => {
        if (active) setSeriesPreview(preview);
      })
      .catch((reason: unknown) => {
        if (active)
          setSeriesPreviewError(
            reason instanceof Error
              ? reason.message
              : 'Anteprima non disponibile.',
          );
      });
    return () => {
      active = false;
    };
  }, [recurringContext, editScope, recurringSource]);

  useEffect(() => {
    let active = true;
    void settingsSource
      .loadLifeAreaChoice(profile.activityRef)
      .then((loaded) => {
        if (!active) return;
        setAreaColorOverride(null);
        setAreaChoice(loaded);
        setSelectedArea(loaded.currentRef ?? '');
        setAreaQuery(
          loaded.options.find((area) => area.ref === loaded.currentRef)?.name ??
            '',
        );
        setAreaError('');
      })
      .catch((reason: unknown) => {
        if (active)
          setAreaError(
            reason instanceof Error
              ? reason.message
              : 'Life Area non disponibile.',
          );
      });
    return () => {
      active = false;
    };
  }, [profile.activityRef, settingsSource]);

  const requestClose = () => {
    if (pending || planPending || objectivePending) return;
    if (confirmingDiscard) {
      setConfirmingDiscard(false);
    } else if (dirty) {
      setConfirmingDiscard(true);
    } else {
      onCancel();
    }
  };

  const patchObjective = (
    id: string,
    patch: Partial<ActivityObjectiveDraft>,
  ) => {
    setObjectiveRows((rows) =>
      rows.map((row) =>
        row.id === id
          ? {
              ...row,
              ...patch,
              operationId: crypto.randomUUID(),
              revisionBasis: null,
            }
          : row,
      ),
    );
    setObjectiveError('');
  };

  const moveObjective = (id: string, direction: -1 | 1) => {
    setObjectiveRows((rows) => {
      const visible = rows.filter((row) => !removedObjectives.includes(row.id));
      const index = visible.findIndex((row) => row.id === id);
      const target = index + direction;
      if (index < 0 || target < 0 || target >= visible.length) return rows;
      const reordered = [...visible];
      [reordered[index], reordered[target]] = [
        reordered[target]!,
        reordered[index]!,
      ];
      const ordered = new Map<string, ActivityObjectiveDraft>(
        reordered.map((row, order): [string, ActivityObjectiveDraft] => [
          row.id,
          order === row.presentationOrder
            ? row
            : {
                ...row,
                presentationOrder: order,
                operationId: crypto.randomUUID(),
                revisionBasis: null,
              },
        ]),
      );
      return rows
        .map((row) => ordered.get(row.id) ?? row)
        .sort((a, b) => a.presentationOrder - b.presentationOrder);
    });
    setObjectiveError('');
  };

  const inspectObjective = (row: ActivityObjectiveDraft) => {
    if (
      !row.objectiveRef ||
      loadedObjectiveOrigins.current.has(row.objectiveRef)
    )
      return;
    loadedObjectiveOrigins.current.add(row.objectiveRef);
    void objectiveSource
      .getSeriesState(row.objectiveRef)
      .then((series) => {
        setObjectiveRows((rows) =>
          rows.map((item) =>
            item.id === row.id ? { ...item, seriesState: series } : item,
          ),
        );
      })
      .catch((reason: unknown) => {
        loadedObjectiveOrigins.current.delete(row.objectiveRef!);
        setObjectiveError(
          reason instanceof Error
            ? reason.message
            : 'Impossibile verificare la ricorrenza dell’obiettivo.',
        );
      });
  };

  const startResultCorrection = (objective: ObjectiveView) => {
    if (
      objectivePending ||
      !objective.observationRef ||
      !objective.evaluationStateRef
    )
      return;
    setCorrectingObjective(objective);
    setCorrectedValue(
      objective.resultKind === 'qualitative'
        ? (objective.qualitativeCode ?? '')
        : (objective.observedNumeric?.toString() ?? ''),
    );
    setCorrectedBoolean(objective.observedBoolean === false ? 'false' : 'true');
    setCorrectedAssessment(objective.assessmentCode ?? 'unknown');
    correctionOperation.current = null;
    setObjectiveError('');
  };

  const applyResultCorrection = () => {
    if (!correctingObjective || !settings || objectivePending) return;
    const objective = correctingObjective;
    if (!objective.evaluationStateRef) {
      setObjectiveError(
        'Manca la valutazione corrente: aggiorna la scheda prima di rettificare.',
      );
      return;
    }
    const numeric =
      objective.resultKind === 'quantity' || objective.resultKind === 'range'
        ? Number(correctedValue)
        : null;
    if (
      (numeric !== null &&
        (!correctedValue.trim() || !Number.isFinite(numeric))) ||
      (objective.resultKind === 'qualitative' && !correctedValue.trim())
    ) {
      setObjectiveError('Inserisci il risultato corretto.');
      return;
    }
    setObjectivePending(true);
    setObjectiveError('');
    void objectiveSource
      .correctResult(objective.objectiveRef, {
        operationId: (correctionOperation.current ??= crypto.randomUUID()),
        expectedEvaluationStateRef: objective.evaluationStateRef,
        observedBoolean:
          objective.resultKind === 'boolean'
            ? correctedBoolean === 'true'
            : null,
        observedNumeric: numeric,
        qualitativeCode:
          objective.resultKind === 'qualitative' ? correctedValue.trim() : null,
        assessmentCode:
          objective.resultKind === 'qualitative' ? correctedAssessment : null,
      })
      .then(() =>
        settingsSource.refreshObjectives(profile.activityRef, settings),
      )
      .then((saved) => {
        setSettings(saved);
        setCorrectingObjective(null);
        correctionOperation.current = null;
      })
      .catch((reason: unknown) => {
        setObjectiveError(
          reason instanceof Error
            ? reason.message
            : 'Rettifica del risultato non riuscita.',
        );
      })
      .finally(() => setObjectivePending(false));
  };

  const requestRecordedObjectiveDeletion = (objective: ObjectiveView) => {
    if (
      pending || planPending || objectivePending || objectiveDeletePending ||
      !objective.observationRef || !objective.evaluationStateRef
    ) return;
    // Removing one accepted result is independent of unfinished
    // Objective drafts or other pending edits to this form.
    setObjectiveError('');
    setDeletingObjective(objective);
  };

  const confirmRecordedObjectiveDeletion = () => {
    if (
      !deletingObjective?.evaluationStateRef || !settings ||
      objectiveDeletePending
    ) return;
    const objective = deletingObjective;
    setObjectiveDeletePending(true);
    setObjectiveError('');
    void objectiveSource
      .deleteRecordedResult(
        objective.objectiveRef, objective.evaluationStateRef!,
      )
      .then(() => settingsSource.refreshObjectives(profile.activityRef, settings))
      .then((fresh) => {
        const restored = fresh.objectives.find(
          (item) => item.objectiveRef === objective.objectiveRef,
        );
        if (!restored || restored.observationRef || restored.evaluationStateRef) {
          throw new Error('Registrazione eliminata, ma rilettura non coerente. Riapri Modifica.');
        }
        setSettings(fresh);
        // Only refresh the affected accepted Objective. Preserve other
        // unsaved new/edited/removal drafts and their operation identities.
        setObjectiveRows((rows) => rows.map((row) =>
          row.objectiveRef === objective.objectiveRef
            ? existingObjectiveDraft(restored)
            : row,
        ));
        setCorrectingObjective(null);
        setDeletingObjective(null);
        correctionOperation.current = null;
        operation.current = undefined;
      })
      .catch((reason: unknown) => {
        setDeletingObjective(null);
        setObjectiveError(
          reason instanceof Error
            ? reason.message
            : 'Eliminazione registrazione non riuscita. Riapri Modifica.',
        );
      })
      .finally(() => setObjectiveDeletePending(false));
  };

  const prepareObjectiveRows = async (): Promise<ActivityObjectiveBatch> => {
    const retained = objectiveRows.filter(
      (row) => !removedObjectives.includes(row.id),
    );
    for (const row of retained) {
      const error = objectiveDraftError(row);
      if (error)
        throw new Error(`${row.label.trim() || 'Nuovo obiettivo'}: ${error}`);
    }
    const updated = retained.filter(
      (row) => row.objectiveRef && objectiveChanged(row),
    );
    const retired = objectiveRows.filter(
      (row) => row.objectiveRef && removedObjectives.includes(row.id),
    );
    const changed = [...updated, ...retired];
    const definitions = await Promise.all(
      changed.map(async (row) => {
        if (row.revisionBasis !== null) {
          return {
            definitionRevision: row.revisionBasis,
            verificationRevision: row.original?.verificationRevision ?? 0,
          };
        }
        const current = await objectiveSource.getDefinition(row.objectiveRef!);
        const original = row.original!;
        if (
          current.label !== original.label ||
          current.resultKind !== original.resultKind ||
          current.comparatorCode !== original.comparatorCode ||
          current.targetValue !== original.targetValue ||
          current.targetMin !== original.targetMin ||
          current.targetMax !== original.targetMax ||
          current.unitCode !== original.unitCode ||
          current.presentationOrder !== original.presentationOrder ||
          (current.verificationMode ?? 'none') !==
            (original.verificationMode ?? 'none') ||
          (current.verificationRevision ?? 0) !==
            (original.verificationRevision ?? 0)
        ) {
          throw new Error(
            'Un obiettivo è cambiato: riapri Modifica prima di salvare.',
          );
        }
        return current;
      }),
    );
    setObjectiveRows((rows) =>
      rows.map((row) => {
        const index = changed.findIndex((item) => item.id === row.id);
        return index >= 0 && row.operationId === changed[index]!.operationId
          ? { ...row, revisionBasis: definitions[index]!.definitionRevision }
          : row;
      }),
    );
    const revisions = definitions.slice(0, updated.length);
    const retireRevisions = definitions.slice(updated.length);
    return {
      add: retained
        .filter((row) => !row.objectiveRef)
        .map((row) => ({
          ...objectiveData(row),
          operationId: row.operationId,
        })),
      revise: updated.map((row, index) => ({
        objectiveRef: row.objectiveRef!,
        change: {
          ...objectiveData(row),
          operationId: row.operationId,
          expectedRevision: revisions[index]!.definitionRevision,
          expectedVerificationRevision:
            revisions[index]!.verificationRevision ??
            row.original?.verificationRevision ??
            0,
          scopeCode: row.scope,
          seriesState: row.seriesState,
        },
      })),
      retire: retired.map((row, index) => ({
        objectiveRef: row.objectiveRef!,
        operationId: row.operationId,
        expectedRevision: retireRevisions[index]!.definitionRevision,
      })),
    };
  };

  const changePlan = (
    ref: string,
    field: keyof ActivityReplanTime,
    value: string,
  ) => {
    setPlanDraft((current) => ({
      ...current,
      [ref]: {
        start: current[ref]?.start ?? '',
        end: current[ref]?.end ?? '',
        [field]: value,
      },
    }));
    setPlanOperation(null);
    setPlanError('');
  };

  const changeNewInterval = (
    ref: string,
    field: keyof ActivityReplanTime,
    value: string,
  ) => {
    setNewIntervals((current) =>
      current.map((item) =>
        item.clientRef === ref ? { ...item, [field]: value } : item,
      ),
    );
    setPlanOperation(null);
    setPlanError('');
  };

  const changeNewPlanned = (ref: string, field: 'name', value: string) => {
    setNewPlanned((current) =>
      current.map((item) =>
        item.clientRef === ref ? { ...item, [field]: value } : item,
      ),
    );
    setPlanOperation(null);
    setPlanError('');
  };

  useEffect(() => {
    closeRequestRef.current = requestClose;
    return () => {
      closeRequestRef.current = null;
    };
  });

  return (
    <form
      className="timeline-activity-editor"
      onSubmit={(event) => {
        event.preventDefault();
        if (
          pending ||
          planPending ||
          objectivePending ||
          objectiveDeletePending ||
          !settings ||
          loadingSettings ||
          recurringLoading ||
          !!recurringError ||
          settingsError ||
          !captureMode ||
          !realityMode ||
          !draft.title.trim() ||
          sessionAttempts === null ||
          !!sessionAttemptsError
        )
          return;
        if (planDirty && Object.keys(planErrors).length) return;
        let proposedRecurrence: ReturnType<
          ExistingRecurrenceControlHandle['getRule']
        >;
        try {
          proposedRecurrence = recurrenceControl.current?.getRule() ?? null;
        } catch (reason) {
          setError(
            reason instanceof Error
              ? reason.message
              : 'Ripetizione non valida.',
          );
          return;
        }
        if (recurrenceResume.current && !proposedRecurrence) {
          const accepted = recurrenceResume.current;
          recurrenceResume.current = null;
          onSaved(accepted.profile);
          return;
        }
        if (
          proposedRecurrence &&
          !allDay &&
          envelope?.temporalForm === 'floating_local'
        ) {
          setError('Per ripetere questa Attività serve un orario con fuso.');
          return;
        }
        if (recurringContext && editScope !== 'only_this') {
          if (!seriesPreview || seriesPreviewError) {
            setError(
              'Carica e controlla l’anteprima delle istanze interessate.',
            );
            return;
          }
          if (
            planDirty ||
            lockDirty ||
            areaDirty ||
            (objectiveDirty &&
              (editScope !== 'this_and_following' || metadataDirty)) ||
            nameDirty ||
            captureMode !== settings.capture.mode ||
            realityMode !== settings.reality.mode ||
            reminderLeadMinutes !== settings.reminderLeadMinutes
          ) {
            setError(
              'La modifica della serie per orari, intervalli, Sessioni, obiettivi, Life Area o promemoria non è ancora disponibile. Scegli «Solo questa istanza» per queste modifiche.',
            );
            return;
          }
          if (!metadataDirty && !objectiveDirty) {
            setError(
              'Modifica un dato generale o un obiettivo per aggiornare la serie.',
            );
            return;
          }
        }
        if (areaDirty && (!areaQueryValid || scopedDomainUnsupported)) {
          setAreaError('Scegli una Life Area valida per questa attività.');
          return;
        }
        if (nameDirty && scopedDomainUnsupported) {
          setNameError('Per rinominare una Sessione scegli «Solo questa».');
          return;
        }
        const invalidObjective = objectiveRows.find(
          (row) =>
            !removedObjectives.includes(row.id) && objectiveDraftError(row),
        );
        if (invalidObjective) {
          setObjectiveError(
            `${invalidObjective.label.trim() || 'Nuovo obiettivo'}: ${objectiveDraftError(invalidObjective)}`,
          );
          const field = event.currentTarget.querySelector<HTMLInputElement>(
            `.timeline-activity-editor__objective-row[data-objective-id="${invalidObjective.id}"] input[type="number"]`,
          );
          field?.focus();
          return;
        }
        if (planningLocked && temporalDirty) {
          setError(
            'Elimina le registrazioni attive o della Sessione dell’attività prima di cambiare orari o intervalli.',
          );
          return;
        }
        if (captureLocked && captureMode !== settings.capture.mode) {
          setError(
            'Elimina tutte le registrazioni prima di cambiare Sessione dell’attività.',
          );
          return;
        }
        // Saving an unchanged Activity is an editor close, never an empty
        // atomic-edit command. PostgreSQL rejects empty writes, and sending
        // one would invent a mutation instead of preserving accepted state.
        if (
          (!recurringContext || editScope === 'only_this') &&
          !proposedRecurrence &&
          !coreDirty &&
          !planDirty &&
          !lockDirty &&
          !areaDirty &&
          !objectiveDirty &&
          !nameDirty
        ) {
          onSaved(profile);
          return;
        }
        setObjectiveError('');
        setPending(true);
        setPlanPending(true);
        setError('');
        void (async () => {
          if (!recurringContext || editScope === 'only_this') {
            // Do not replay an accepted atomic edit with stale CAS if the
            // separate recurrence activation previously failed.
            if (proposedRecurrence && recurrenceResume.current) {
              const accepted = recurrenceResume.current;
              const currentEnvelope = accepted.settings.schedules.find(
                (row) => row.role === 'envelope',
              );
              if (!currentEnvelope?.placementStateRef) {
                throw new Error('Programmazione Attività non disponibile.');
              }
              await existingRecurrence.startActivity(
                {
                  activityRef: accepted.profile.activityRef,
                  expectedProfileRevision: accepted.profile.revision,
                  envelopeScheduleRef: currentEnvelope.scheduleRef,
                  expectedPlacementStateRef: currentEnvelope.placementStateRef,
                },
                proposedRecurrence,
                (recurrenceOperation.current ??= crypto.randomUUID()),
              );
              recurrenceResume.current = null;
              onSaved(accepted.profile);
              return;
            }
            if (
              proposedRecurrence &&
              !(
                coreDirty ||
                planDirty ||
                lockDirty ||
                areaDirty ||
                objectiveDirty ||
                nameDirty
              )
            ) {
              if (!envelope?.placementStateRef) {
                throw new Error('Programmazione Attività non disponibile.');
              }
              await existingRecurrence.startActivity(
                {
                  activityRef: profile.activityRef,
                  expectedProfileRevision: profile.revision,
                  envelopeScheduleRef: envelope.scheduleRef,
                  expectedPlacementStateRef: envelope.placementStateRef,
                },
                proposedRecurrence,
                (recurrenceOperation.current ??= crypto.randomUUID()),
              );
              onSaved(profile);
              return;
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
            const captureChanged = captureMode !== settings.capture.mode;
            const realityChanged = realityMode !== settings.reality.mode;
            const reminderChanged =
              reminderLeadMinutes !== settings.reminderLeadMinutes;
            const coreChanged =
              (!recurringContext && metadataChanged) ||
              captureChanged ||
              realityChanged ||
              reminderChanged;
            const renamed = settings.schedules
              .filter(
                (row) =>
                  row.role === 'planned' &&
                  !deletedPlanned.includes(row.scheduleRef) &&
                  (plannedNames[row.scheduleRef] ?? row.name ?? '') !==
                    (row.name ?? ''),
              )
              .map((row) => ({
                scheduleRef: row.scheduleRef,
                expectedName: row.name,
                name: plannedNames[row.scheduleRef]?.trim() || null,
              }));
            const targetArea = selectedArea || null;
            const selectedOption = areaChoice?.options.find(
              (option) => option.ref === targetArea,
            );
            const color =
              areaColorOverride ??
              (creatingArea ? draft.colorCode || '#EA5C12' : null);
            const colorChanged =
              !!selectedOption &&
              !!color &&
              color.toUpperCase() !== selectedOption.colorCode?.toUpperCase();
            const assignmentChanged =
              creatingArea || targetArea !== areaChoice?.currentRef;
            const atomicOperation = planOperation ?? crypto.randomUUID();
            setPlanOperation(atomicOperation);
            const occurrencePatch =
              recurringContext && metadataChanged
                ? Object.fromEntries(
                    Object.entries(changed).filter(
                      ([key, value]) =>
                        value !== profile[key as keyof typeof changed],
                    ),
                  )
                : null;
            const saved = await settingsSource.applyAtomicEdit(
              profile,
              settings,
              {
                ...(planDirty ? { draft: replanDraft } : {}),
                ...(objectiveDirty
                  ? { objectives: await prepareObjectiveRows() }
                  : {}),
                ...(coreChanged
                  ? {
                      changes: {
                        ...(metadataChanged && !recurringContext
                          ? { profile: changed }
                          : {}),
                        ...(captureChanged ? { capture: captureMode } : {}),
                        ...(realityChanged ? { reality: realityMode } : {}),
                        ...(reminderChanged ? { reminderLeadMinutes } : {}),
                      },
                    }
                  : {}),
                ...(recurringContext && occurrencePatch
                  ? {
                      occurrenceProfile: {
                        occurrenceRef: recurringContext.occurrenceRef,
                        expectedRevision: recurringContext.editRevision,
                        expectedRecurrenceStateRef:
                          recurringContext.recurrenceStateRef,
                        patch: occurrencePatch,
                      },
                    }
                  : {}),
                ...(lockDirty && settings.placementLockScheduleRef
                  ? {
                      placementLock: {
                        scheduleRef: settings.placementLockScheduleRef,
                        expectedRevision: settings.placementLockRevision,
                        locked: placementProtected === true,
                      },
                    }
                  : {}),
                ...(renamed.length ? { plannedNames: renamed } : {}),
                ...(areaDirty && areaChoice
                  ? {
                      lifeArea: {
                        expectedAssignmentRevision: areaChoice.currentRevision,
                        lifeAreaRef: targetArea,
                        assign: assignmentChanged,
                        ...(creatingArea
                          ? {
                              newArea: {
                                name: newAreaName,
                                colorCode: color?.toUpperCase() ?? null,
                              },
                            }
                          : {}),
                        ...(colorChanged && selectedOption && color
                          ? {
                              expectedAreaRevision: selectedOption.revision,
                              colorCode: color.toUpperCase(),
                              iconCode: selectedOption.iconCode,
                            }
                          : {}),
                      },
                    }
                  : {}),
              },
              atomicOperation,
            );
            setSettings(saved.settings);
            setObjectiveRows(
              saved.settings.objectives.map(existingObjectiveDraft),
            );
            setRemovedObjectives([]);
            setPlanOperation(null);
            if (proposedRecurrence && !recurringContext) {
              const currentEnvelope = saved.settings.schedules.find(
                (row) => row.role === 'envelope',
              );
              if (!currentEnvelope?.placementStateRef) {
                throw new Error('Programmazione Attività non disponibile.');
              }
              recurrenceResume.current = {
                profile: saved.profile,
                settings: saved.settings,
              };
              await existingRecurrence.startActivity(
                {
                  activityRef: saved.profile.activityRef,
                  expectedProfileRevision: saved.profile.revision,
                  envelopeScheduleRef: currentEnvelope.scheduleRef,
                  expectedPlacementStateRef: currentEnvelope.placementStateRef,
                },
                proposedRecurrence,
                (recurrenceOperation.current ??= crypto.randomUUID()),
              );
              recurrenceResume.current = null;
            }
            onSaved(saved.profile);
            return;
          }
          if (
            recurringContext &&
            editScope === 'this_and_following' &&
            objectiveDirty
          ) {
            if (
              removedObjectives.length > 0 ||
              objectiveRows.some((row) => !row.objectiveRef)
            ) {
              throw new Error(
                'Per aggiungere o rimuovere obiettivi della serie usa Modifica ricorrenza.',
              );
            }
            const batch = await prepareObjectiveRows();
            const revisions = await Promise.all(
              batch.revise.map(async (revision) => {
                const seriesState =
                  revision.change.seriesState ??
                  (await objectiveSource.getSeriesState(revision.objectiveRef));
                if (!seriesState) {
                  throw new Error(
                    'Obiettivo senza origine ricorrente: riapri la modifica della serie.',
                  );
                }
                return {
                  objectiveRef: revision.objectiveRef,
                  change: {
                    ...revision.change,
                    scopeCode: 'this_and_following' as const,
                    seriesState,
                  },
                };
              }),
            );
            const atomicOperation = planOperation ?? crypto.randomUUID();
            setPlanOperation(atomicOperation);
            const saved = await settingsSource.applyAtomicEdit(
              profile,
              settings,
              {
                objectives: {
                  add: [],
                  revise: revisions,
                  retire: [],
                },
              },
              atomicOperation,
            );
            setSettings(saved.settings);
            setObjectiveRows(
              saved.settings.objectives.map(existingObjectiveDraft),
            );
            setRemovedObjectives([]);
            setPlanOperation(null);
            onSaved(saved.profile);
            return;
          }
          // Structure-wide Objective addition/removal is handled by the
          // Recurrence editor, which also updates future materialization.
          // The profile-only fallback keeps the existing preview contract.
          if (!recurringContext || !metadataDirty) {
            throw new Error(
              'Modifica i dati generali della serie prima di salvare.',
            );
          }
          const changed = {
            title: draft.title.trim(),
            description: draft.description.trim() || null,
            location: draft.location.trim() || null,
            colorCode: draft.colorCode || null,
          };
          const changedKeys = Object.fromEntries(
            Object.entries(changed).filter(
              ([key, value]) => value !== profile[key as keyof typeof changed],
            ),
          );
          const nextProfile = await recurringSource.saveActivityProfile(
            profile.activityRef,
            recurringContext,
            editScope,
            changedKeys,
            (operation.current ??= crypto.randomUUID()),
            seriesPreview ?? undefined,
          );
          operation.current = undefined;
          onSaved(nextProfile);
        })()
          .catch((reason: unknown) => {
            const message =
              reason instanceof Error
                ? reason.message
                : 'Operazione non riuscita.';
            setError(
              recurrenceResume.current
                ? `Modifiche salvate, ma ripetizione non avviata: ${message}. Premi di nuovo Salva per riprovare.`
                : message,
            );
          })
          .finally(() => {
            setPending(false);
            setPlanPending(false);
          });
      }}
    >
      <div
        className="timeline-activity-editor__body"
        inert={confirmingDiscard || objectiveDeletePending || undefined}
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
        <TemporalAuthoringTitleRow
          kind="activity"
          className="timeline-activity-editor__title-row"
        >
          <label className="timeline-activity-editor__title">
            <span className="timeline-activity-editor__visually-hidden">
              Titolo
            </span>
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
                <TemporalCreatePlacementLockButton
                  kind="activity"
                  locked={placementProtected ?? settings.placementProtected}
                  invalid={!!lockError}
                  disabled={pending || planPending}
                  onToggle={() => {
                    setPlacementProtected(
                      !(placementProtected ?? settings.placementProtected),
                    );
                    setLockError('');
                  }}
                />
              ) : null}
              <label className="temporal-create-structure-session-toggle timeline-activity-editor__capture">
                <input
                  type="checkbox"
                  disabled={captureLocked || pending || planPending}
                  checked={
                    (captureMode ?? settings.capture.mode) !== 'disabled'
                  }
                  onChange={(event) => {
                    operation.current = undefined;
                    setCaptureMode(event.target.checked ? 'live' : 'disabled');
                  }}
                />
                Sessione
              </label>
            </div>
          ) : null}
        </TemporalAuthoringTitleRow>
        {lockError ? <p role="alert">{lockError}</p> : null}
        {sessionAttemptsError ? (
          <p role="alert">{sessionAttemptsError}</p>
        ) : null}
        {settings &&
        (settings.schedules.some((row) => row.role === 'planned') ||
          newPlanned.length > 0 ||
          canReplan) ? (
          <section
            className="temporal-create-activity-tree timeline-activity-editor__sessions"
            aria-label="Sessioni attività"
          >
            <div
              className="temporal-create-activity-tree__spine"
              aria-hidden="true"
            />
            {settings.schedules.some(
              (row) =>
                row.role === 'planned' &&
                !deletedPlanned.includes(row.scheduleRef),
            ) || newPlanned.length > 0 ? (
              <div className="temporal-create-activity-tree__root-sessions">
                <div className="temporal-create-activity-tree__group-label temporal-editor-section-heading">
                  Sessioni attività
                </div>
                {settings.schedules
                  .filter(
                    (row) =>
                      row.role === 'planned' &&
                      !deletedPlanned.includes(row.scheduleRef),
                  )
                  .map((row) => {
                    return (
                      <div
                        className="temporal-create-tree-item is-session is-root"
                        key={row.scheduleRef}
                        data-edit-planned-session={row.scheduleRef}
                      >
                        <div className="temporal-create-tree-row">
                          <span
                            className="temporal-create-tree-row__icon"
                            aria-hidden="true"
                          >
                            ▶
                          </span>
                          <span
                            className="temporal-create-tree-row__divider"
                            aria-hidden="true"
                          />
                          <input
                            className="temporal-create-tree-row__title"
                            maxLength={300}
                            aria-label="Nome Sessione"
                            placeholder="Nome Sessione"
                            disabled={pending || planPending}
                            value={plannedNames[row.scheduleRef] ?? ''}
                            onChange={(event) => {
                              const value = event.currentTarget.value;
                              setPlannedNames((current) => ({
                                ...current,
                                [row.scheduleRef]: value,
                              }));
                              setNameError('');
                            }}
                          />
                          <div className="temporal-create-tree-row__actions">
                            {!sessionAttempts?.some(
                              (attempt) =>
                                attempt.plannedScheduleRef === row.scheduleRef,
                            ) ? (
                              <button
                                type="button"
                                className="is-remove"
                                aria-label="Rimuovi Sessione"
                                disabled={
                                  !canReplan ||
                                  sessionAttempts === null ||
                                  pending ||
                                  planPending
                                }
                                onClick={() => {
                                  setDeletedPlanned((current) => [
                                    ...current,
                                    row.scheduleRef,
                                  ]);
                                  setPlanOperation(null);
                                  setPlanError('');
                                }}
                              >
                                ×
                              </button>
                            ) : null}
                          </div>
                        </div>
                        {sessionAttempts
                          ?.filter(
                            (attempt) =>
                              attempt.plannedScheduleRef === row.scheduleRef,
                          )
                          .map(attemptRecord)}
                      </div>
                    );
                  })}
                {newPlanned.map((item) => (
                  <div
                    className="temporal-create-tree-item is-session is-root"
                    key={item.clientRef}
                    data-edit-new-session={item.clientRef}
                  >
                    <div className="temporal-create-tree-row">
                      <span
                        className="temporal-create-tree-row__icon"
                        aria-hidden="true"
                      >
                        ▶
                      </span>
                      <span
                        className="temporal-create-tree-row__divider"
                        aria-hidden="true"
                      />
                      <input
                        className="temporal-create-tree-row__title"
                        maxLength={300}
                        aria-label="Nome Sessione"
                        placeholder="Nome Sessione"
                        disabled={planPending}
                        value={item.name}
                        onChange={(event) =>
                          changeNewPlanned(
                            item.clientRef,
                            'name',
                            event.target.value,
                          )
                        }
                      />
                      <div className="temporal-create-tree-row__actions">
                        <button
                          type="button"
                          className="is-remove"
                          aria-label="Rimuovi Sessione"
                          disabled={planPending}
                          onClick={() => {
                            setNewPlanned((current) =>
                              current.filter(
                                (row) => row.clientRef !== item.clientRef,
                              ),
                            );
                            setPlanOperation(null);
                          }}
                        >
                          ×
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : null}
            {canReplan ? (
              <div className="temporal-create-activity-tree__root-actions">
                <button
                  type="button"
                  className="temporal-create-tree-add"
                  disabled={
                    planPending ||
                    settings.schedules.filter(
                      (row) =>
                        row.role === 'planned' &&
                        !deletedPlanned.includes(row.scheduleRef),
                    ).length +
                      newPlanned.length >=
                      100
                  }
                  onClick={() => {
                    setNewPlanned((current) => [
                      ...current,
                      { clientRef: crypto.randomUUID(), name: '' },
                    ]);
                    setPlanOperation(null);
                  }}
                >
                  <span aria-hidden="true">＋</span>Sessione
                </button>
              </div>
            ) : null}
          </section>
        ) : null}
        {sessionAttempts?.some((attempt) => !attempt.plannedScheduleRef) ? (
          <section
            className="timeline-activity-editor__main-record"
            aria-label="Registrazioni Sessione attività"
          >
            <h3>Sessione attività</h3>
            {sessionAttempts
              .filter((attempt) => !attempt.plannedScheduleRef)
              .map(attemptRecord)}
          </section>
        ) : null}
        {attemptDeleteError ? <p role="alert">{attemptDeleteError}</p> : null}
        {sessionAttempts?.length ? (
          <p className="timeline-activity-editor__record-hint">
            {planningLocked
              ? 'Orari e intervalli restano bloccati finché esistono registrazioni attive o della Sessione dell’attività. Per cambiare Sessione dell’attività elimina tutte le registrazioni.'
              : 'Le registrazioni concluse restano svolte ai loro orari reali. Puoi riprogrammare l’attività; per cambiare Sessione dell’attività elimina tutte le registrazioni.'}
          </p>
        ) : null}
        {settings ? (
          <>
            <section
              className="timeline-activity-editor__readback"
              aria-label="Programmazione attuale"
            >
              <div
                className="timeline-activity-editor__placement"
                role="group"
                aria-label="Collocazione attuale"
              >
                <button
                  type="button"
                  className={!allDay ? 'is-selected' : ''}
                  aria-pressed={!allDay}
                  disabled={!canReplan || planningLocked || planPending}
                  onClick={() => {
                    if (originalAllDay && envelope) {
                      setPlanDraft((current) => ({
                        ...current,
                        [envelope.scheduleRef]: {
                          start: `${dateSpanDraft.start}T09:00`,
                          end: `${dateSpanDraft.start}T10:00`,
                        },
                      }));
                    }
                    setAllDay(false);
                    setPlanOperation(null);
                    setPlanError('');
                  }}
                >
                  Orario
                </button>
                <button
                  type="button"
                  className={allDay ? 'is-selected' : ''}
                  aria-pressed={allDay}
                  disabled={
                    !canReplan || planningLocked || hasIntervals || planPending
                  }
                  onClick={() => {
                    if (envelope) {
                      setDateSpanDraft({
                        start: (
                          planDraft[envelope.scheduleRef]?.start ??
                          envelope.start ??
                          ''
                        ).slice(0, 10),
                        end: (
                          planDraft[envelope.scheduleRef]?.end ??
                          envelope.end ??
                          ''
                        ).slice(0, 10),
                      });
                    }
                    setNewIntervals([]);
                    setAllDay(true);
                    setPlanOperation(null);
                    setPlanError('');
                  }}
                >
                  Tutto il giorno
                </button>
              </div>
              {hasIntervals ? (
                <p className="timeline-activity-editor__planning-hint">
                  Tutto il giorno è disponibile per le attività con un solo
                  periodo, senza intervalli separati.
                </p>
              ) : null}
              <h3 className="timeline-activity-editor__visually-hidden">
                Programmazione attuale
              </h3>
              {!allDay &&
              (settings.schedules.find((schedule) => schedule.zoneId)?.zoneId ||
                originalAllDay) ? (
                <p className="timeline-activity-editor__timezone">
                  <span aria-hidden="true">◎</span> Fuso orario ·{' '}
                  {originalAllDay
                    ? (timeZone ?? detectDeviceTimeZone())
                    : settings.schedules.find((schedule) => schedule.zoneId)
                        ?.zoneId}
                </p>
              ) : null}
              {planError ? <p role="alert">{planError}</p> : null}
              {nameError ? <p role="alert">{nameError}</p> : null}
              {scopedDomainUnsupported && nameDirty ? (
                <p role="status">
                  La rinomina di Session pianificate per tutta la serie non è
                  ancora supportata. Seleziona «Solo questa».
                </p>
              ) : null}
              {allDay && canReplan ? (
                <div
                  className="timeline-activity-editor__all-day"
                  data-edit-invalid={!!planErrors.dateSpan}
                  inert={planningLocked || undefined}
                >
                  <TemporalCreateDatePicker
                    label="Data inizio"
                    locale="it"
                    value={dateSpanDraft.start}
                    onChange={(start) => {
                      setDateSpanDraft((current) => ({ ...current, start }));
                      setPlanOperation(null);
                      setPlanError('');
                    }}
                  />
                  <span aria-hidden="true">→</span>
                  <TemporalCreateDatePicker
                    label="Data fine"
                    align="end"
                    locale="it"
                    value={dateSpanDraft.end}
                    onChange={(end) => {
                      setDateSpanDraft((current) => ({ ...current, end }));
                      setPlanOperation(null);
                      setPlanError('');
                    }}
                  />
                  {planErrors.dateSpan ? (
                    <small className="temporal-create-field-error" role="alert">
                      {planErrors.dateSpan}
                    </small>
                  ) : null}
                </div>
              ) : settings.schedules.length ? (
                <ul>
                  {settings.schedules
                    .filter(
                      (schedule) =>
                        schedule.role !== 'planned' &&
                        (schedule.role !== 'envelope' || !hasIntervals),
                    )
                    .map((schedule, index) => (
                      <li
                        key={schedule.scheduleRef}
                        className="temporal-create-activity-interval"
                      >
                        {hasIntervals || newIntervals.length > 0 ? (
                          <span className="temporal-create-activity-interval__label">
                            Intervallo {index + 1}
                          </span>
                        ) : null}
                        {schedule.start && schedule.end && !canReplan ? (
                          <div
                            className="timeline-activity-editor__schedule-time"
                            role="group"
                            aria-label="Orario programmato"
                          >
                            <span>
                              {(
                                planDraft[schedule.scheduleRef]?.start ||
                                schedule.start
                              ).slice(0, 10)}
                            </span>
                            <span>
                              {(
                                planDraft[schedule.scheduleRef]?.start ||
                                schedule.start
                              ).slice(11, 16)}
                            </span>
                            <span aria-hidden="true">→</span>
                            <span>
                              {(
                                planDraft[schedule.scheduleRef]?.end ||
                                schedule.end
                              ).slice(11, 16)}
                            </span>
                            <span>
                              {(
                                planDraft[schedule.scheduleRef]?.end ||
                                schedule.end
                              ).slice(0, 10)}
                            </span>
                          </div>
                        ) : null}
                        {canReplan &&
                        !removedIntervals.includes(schedule.scheduleRef) ? (
                          <ActivityIntervalFields
                            value={
                              planDraft[schedule.scheduleRef] ?? {
                                start: schedule.start ?? '',
                                end: schedule.end ?? '',
                              }
                            }
                            onChange={(field, value) =>
                              changePlan(schedule.scheduleRef, field, value)
                            }
                            error={planErrors[schedule.scheduleRef]}
                            disabled={planningLocked || planPending}
                            {...(schedule.role === 'interval'
                              ? {
                                  removeLabel: `Rimuovi intervallo ${index + 1}`,
                                  onRemove: () => {
                                    setRemovedIntervals((current) => [
                                      ...current,
                                      schedule.scheduleRef,
                                    ]);
                                    setPlanOperation(null);
                                    setPlanError('');
                                  },
                                }
                              : {})}
                          />
                        ) : null}
                        {canReplan &&
                        removedIntervals.includes(schedule.scheduleRef) ? (
                          <button
                            type="button"
                            disabled={planningLocked || planPending}
                            onClick={() => {
                              setRemovedIntervals((current) =>
                                current.filter(
                                  (ref) => ref !== schedule.scheduleRef,
                                ),
                              );
                              setPlanOperation(null);
                              setPlanError('');
                            }}
                          >
                            Mantieni intervallo {index + 1}
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
                    La modifica degli orari richiede pianificazioni locali con
                    inizio e fine. Le altre forme temporali restano inalterate:
                    DANTE non le converte automaticamente. Puoi comunque
                    correggere separatamente il nome delle Session pianificate,
                    senza modificare lo Schedule.
                  </p>
                </details>
              ) : null}
              {canReplan && !allDay ? (
                <div className="temporal-create-activity-intervals timeline-activity-editor__intervals">
                  {newIntervals.map((item, index) => (
                    <div
                      key={item.clientRef}
                      className="temporal-create-activity-interval"
                    >
                      <span className="temporal-create-activity-interval__label">
                        Intervallo{' '}
                        {editablePlan.filter((row) => row.role === 'interval')
                          .length -
                          removedIntervals.length +
                          (hasIntervals ? 0 : 1) +
                          index +
                          1}
                      </span>
                      <ActivityIntervalFields
                        value={item}
                        onChange={(field, value) =>
                          changeNewInterval(item.clientRef, field, value)
                        }
                        error={planErrors[item.clientRef]}
                        disabled={planningLocked || planPending}
                        removeLabel={`Rimuovi intervallo ${
                          editablePlan.filter((row) => row.role === 'interval')
                            .length -
                          removedIntervals.length +
                          (hasIntervals ? 0 : 1) +
                          index +
                          1
                        }`}
                        onRemove={() => {
                          setNewIntervals((current) =>
                            current.filter(
                              (row) => row.clientRef !== item.clientRef,
                            ),
                          );
                          setPlanOperation(null);
                          setPlanError('');
                        }}
                      />
                    </div>
                  ))}
                  {!originalAllDay ? (
                    <button
                      type="button"
                      className="temporal-create-activity-intervals__add"
                      disabled={
                        planningLocked ||
                        planPending ||
                        (hasIntervals
                          ? editablePlan.filter(
                              (row) => row.role === 'interval',
                            ).length
                          : 1) -
                          removedIntervals.length +
                          newIntervals.length >=
                          100
                      }
                      onClick={() => {
                        setNewIntervals((current) => {
                          const lastEnd =
                            current.at(-1)?.end ??
                            editablePlan
                              .filter(
                                (row) =>
                                  !removedIntervals.includes(row.scheduleRef),
                              )
                              .map(
                                (row) =>
                                  planDraft[row.scheduleRef]?.end ??
                                  row.end ??
                                  '',
                              )
                              .sort()
                              .at(-1) ??
                            envelope?.end ??
                            envelope?.start ??
                            '';
                          return [
                            ...current,
                            {
                              clientRef: crypto.randomUUID(),
                              ...nextIntervalAfter(lastEnd),
                            },
                          ];
                        });
                        setPlanOperation(null);
                        setPlanError('');
                      }}
                    >
                      <span aria-hidden="true">＋</span> Aggiungi intervallo
                    </button>
                  ) : null}
                </div>
              ) : null}
              {planDirty ? (
                <div>
                  <button
                    type="button"
                    disabled={planPending}
                    onClick={() => {
                      setPlanDraft(
                        Object.fromEntries(
                          settings.schedules.map((schedule) => [
                            schedule.scheduleRef,
                            {
                              start: schedule.start ?? '',
                              end: schedule.end ?? '',
                            },
                          ]),
                        ),
                      );
                      setNewPlanned([]);
                      setDeletedPlanned([]);
                      setNewIntervals([]);
                      setRemovedIntervals([]);
                      setAllDay(originalAllDay);
                      setDateSpanDraft({
                        start: envelope?.start?.slice(0, 10) ?? '',
                        end: shiftedDate(
                          envelope?.end?.slice(0, 10) ?? '',
                          originalAllDay ? -1 : 0,
                        ),
                      });
                      setPlanOperation(null);
                    }}
                  >
                    Ripristina orari
                  </button>
                </div>
              ) : null}
            </section>
            {recurringContext ? null : envelope?.start &&
              envelope.placementStateRef ? (
              <ExistingRecurrenceControl
                ref={recurrenceControl}
                kind="activity"
                date={
                  allDay
                    ? dateSpanDraft.start
                    : (
                        planDraft[envelope.scheduleRef]?.start ?? envelope.start
                      ).slice(0, 10)
                }
                startTime={
                  allDay
                    ? '00:00'
                    : (
                        planDraft[envelope.scheduleRef]?.start ?? envelope.start
                      ).slice(11, 16) || '09:00'
                }
                allDay={allDay}
                zoneId={envelope.zoneId ?? timeZone ?? detectDeviceTimeZone()}
                disambiguation="earlier"
                onSelectionChange={(selected) => {
                  setRecurrenceSelected(selected);
                  recurrenceOperation.current = null;
                }}
              />
            ) : (
              <div
                className="timeline-activity-editor__repeat"
                role="group"
                aria-label="Ripeti"
              >
                Ripeti · Mai
              </div>
            )}
            <div className="timeline-activity-editor__area-color">
              <div className="temporal-create-life-area-field">
                <TemporalColorControl
                  value={selectedAreaColor}
                  label={
                    selectedArea || creatingArea
                      ? 'Colore Life Area'
                      : 'Colore attività o evento'
                  }
                  onChange={(colorCode) => {
                    if (selectedArea || creatingArea) {
                      setAreaColorOverride(colorCode);
                    } else {
                      operation.current = undefined;
                      setDraft((current) => ({ ...current, colorCode }));
                    }
                  }}
                />
                <div
                  className="timeline-activity-editor__area-choice"
                  data-edit-invalid={!!areaError}
                >
                  {areaError ? (
                    <small className="temporal-create-field-error" role="alert">
                      {areaError}
                    </small>
                  ) : null}
                  {!areaChoice && !areaError ? (
                    <p role="status">Caricamento Life Area…</p>
                  ) : null}
                  {areaChoice ? (
                    <>
                      {scopedDomainUnsupported && areaDirty ? (
                        <p role="status">
                          Per modificare la Life Area scegli «Solo questa»: non
                          propaghiamo modifiche parziali alla serie.
                        </p>
                      ) : null}
                      <TemporalLifeAreaSelect
                        query={areaQuery}
                        label="Area assegnata"
                        options={areaChoice.options.map((area) => ({
                          id: area.ref,
                          label: area.name,
                          colorCode: area.colorCode ?? null,
                        }))}
                        selectedId={selectedArea || null}
                        disabled={pending || planPending}
                        onQueryChange={(query) => {
                          setAreaQuery(query);
                          setAreaColorOverride(null);
                          setSelectedArea(
                            areaChoice.options.find(
                              (area) =>
                                area.name.toLocaleLowerCase() ===
                                query.trim().toLocaleLowerCase(),
                            )?.ref ?? '',
                          );
                          setAreaError('');
                        }}
                        onChoose={(area) => {
                          setSelectedArea(area.id);
                          setAreaQuery(area.label);
                          setAreaColorOverride(null);
                          setAreaError('');
                        }}
                        onClear={() => {
                          setSelectedArea('');
                          setAreaQuery('');
                          setAreaError('');
                          setAreaColorOverride(null);
                        }}
                      />
                      {creatingArea ? (
                        <small>
                          La nuova Life Area verrà creata quando salvi.
                        </small>
                      ) : null}
                      {!areaQueryValid ? (
                        <small>Scegli una Life Area dall’elenco.</small>
                      ) : null}
                    </>
                  ) : null}
                </div>
              </div>
            </div>
            <section
              className="temporal-create-reality-objectives timeline-activity-editor__outcome"
              aria-label="Configurazione obiettivi"
            >
              <section
                className="temporal-create-reality-objectives__block is-objectives timeline-activity-editor__readback"
                aria-label="Obiettivi attuali"
              >
                <div className="temporal-create-reality-objectives__block-copy">
                  <strong className="temporal-editor-section-heading">
                    Obiettivi
                  </strong>
                </div>
                <div
                  className="timeline-activity-editor__objectives"
                  data-edit-invalid={!!objectiveError}
                >
                  {objectiveRows
                    .filter((row) => !removedObjectives.includes(row.id))
                    .map((row, index, visible) => (
                      <ActivityObjectiveRow
                        key={row.id}
                        row={row}
                        index={index}
                        total={visible.length}
                        disabled={pending || planPending || objectivePending || objectiveDeletePending}
                        onInspect={() => inspectObjective(row)}
                        onCorrectRecorded={() => {
                          if (row.original) startResultCorrection(row.original);
                        }}
                        onDeleteRecorded={() => {
                          if (row.original) requestRecordedObjectiveDeletion(row.original);
                        }}
                        onChange={(patch) => patchObjective(row.id, patch)}
                        onMove={(direction) => moveObjective(row.id, direction)}
                        onRemove={() => {
                          if (row.objectiveRef) {
                            setRemovedObjectives((current) => [
                              ...current,
                              row.id,
                            ]);
                          } else {
                            setObjectiveRows((current) =>
                              current.filter((item) => item.id !== row.id),
                            );
                          }
                          setObjectiveError('');
                        }}
                      />
                    ))}
                  {removedObjectives.length > 0 ? (
                    <button
                      type="button"
                      onClick={() => {
                        setRemovedObjectives([]);
                        setObjectiveError('');
                      }}
                      disabled={pending || planPending}
                    >
                      Ripristina obiettivi rimossi
                    </button>
                  ) : null}
                  <div className="temporal-create-objectives__root-actions">
                    <button
                      type="button"
                      className="temporal-create-objectives__add"
                      disabled={pending || planPending || objectivePending}
                      onClick={() => {
                        const next = newObjectiveDraft(
                          Math.max(
                            -1,
                            ...objectiveRows.map(
                              (row) => row.presentationOrder,
                            ),
                          ) + 1,
                        );
                        setObjectiveRows((rows) => [...rows, next]);
                        setObjectiveError('');
                      }}
                    >
                      + Obiettivo
                    </button>
                  </div>
                  {objectiveError ? (
                    <small className="temporal-create-field-error" role="alert">
                      {objectiveError}
                    </small>
                  ) : null}
                </div>
                {correctingObjective ? (
                  <fieldset disabled={objectivePending}>
                    <legend>
                      Rettifica risultato — {correctingObjective.label}
                    </legend>
                    {correctingObjective.resultKind === 'boolean' ? (
                      <label>
                        Risultato corretto
                        <select
                          value={correctedBoolean}
                          onChange={(event) => {
                            setCorrectedBoolean(event.target.value);
                            correctionOperation.current = null;
                          }}
                        >
                          <option value="true">Sì</option>
                          <option value="false">No</option>
                        </select>
                      </label>
                    ) : (
                      <label>
                        Risultato corretto
                        <input
                          type={
                            correctingObjective.resultKind === 'qualitative'
                              ? 'text'
                              : 'number'
                          }
                          step="any"
                          value={correctedValue}
                          onChange={(event) => {
                            setCorrectedValue(event.target.value);
                            correctionOperation.current = null;
                          }}
                        />
                      </label>
                    )}
                    {correctingObjective.resultKind === 'qualitative' ? (
                      <label>
                        Valutazione corretta
                        <select
                          value={correctedAssessment}
                          onChange={(event) => {
                            setCorrectedAssessment(
                              event.target.value as ObjectiveAssessment,
                            );
                            correctionOperation.current = null;
                          }}
                        >
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
                    <button
                      type="button"
                      onClick={() => {
                        setCorrectingObjective(null);
                        correctionOperation.current = null;
                      }}
                    >
                      Annulla rettifica
                    </button>
                    <p>
                      La rettifica aggiorna il valore corrente senza cancellare
                      l’osservazione e la valutazione precedenti.
                    </p>
                  </fieldset>
                ) : null}
              </section>
            </section>
            <div className="timeline-activity-editor__location">
              <input
                className="temporal-create-u2-location"
                aria-label="Località"
                placeholder="Località"
                value={draft.location}
                onChange={(event) => {
                  operation.current = undefined;
                  setDraft({ ...draft, location: event.target.value });
                }}
              />
            </div>
            {settings.reminderScheduleRef ? (
              <TemporalReminderControl
                value={reminderLeadMinutes}
                onChange={(value) => {
                  operation.current = undefined;
                  setReminderLeadMinutes(value);
                }}
              />
            ) : null}
          </>
        ) : null}
        <section
          className="timeline-activity-editor__description temporal-create-section is-wide temporal-create-description-section"
          aria-label="Descrizione"
        >
          <h3>Descrizione</h3>
          <textarea
            className="temporal-create-u2-description temporal-create-advanced-description"
            aria-label="Descrizione"
            rows={5}
            value={draft.description}
            onChange={(event) => {
              operation.current = undefined;
              setDraft({ ...draft, description: event.target.value });
            }}
          />
        </section>
        {recurringContext && editScope !== 'only_this' ? (
          <fieldset className="timeline-activity-editor__fields">
            <legend>Ambito della modifica</legend>
            <p>
              {editScope === 'from_next'
                ? 'Dalla prossima istanza'
                : 'Questa e le successive'}
            </p>
            {seriesPreviewError ? (
              <p role="alert">{seriesPreviewError}</p>
            ) : null}
            {!seriesPreview && !seriesPreviewError ? (
              <p role="status">Verifica delle istanze…</p>
            ) : null}
            {seriesPreview ? (
              <div role="status">
                <p>
                  {seriesPreview.targetOccurrenceRefs.length} istanze già create
                  interessate; le future saranno governate dalla nuova modifica
                  ai dati generali.
                </p>
                {seriesPreview.protectedOccurrences.length > 0 ? (
                  <>
                    <p>
                      {seriesPreview.protectedOccurrences.length} eccezioni
                      future conservate:
                    </p>
                    <ul>
                      {seriesPreview.protectedOccurrences
                        .slice(0, 10)
                        .map((item) => (
                          <li key={item.occurrenceRef}>
                            {new Intl.DateTimeFormat('it-IT', {
                              dateStyle: 'medium',
                              timeStyle: 'short',
                            }).format(new Date(item.expectedAt))}{' '}
                            ·{' '}
                            {item.reason === 'registration'
                              ? 'registrazione'
                              : item.reason === 'skipped'
                                ? 'saltata'
                                : item.reason === 'legacy_unknown'
                                  ? 'origine del nome da verificare'
                                  : 'modifica individuale'}
                          </li>
                        ))}
                    </ul>
                  </>
                ) : null}
              </div>
            ) : null}
          </fieldset>
        ) : null}
      </div>
      <div
        className="timeline-activity-editor__actions dante-temporal-panel-actions"
        inert={confirmingDiscard || objectiveDeletePending || undefined}
      >
        <button
          type="button"
          disabled={pending || planPending || objectivePending || objectiveDeletePending}
          onClick={requestClose}
        >
          Annulla
        </button>
        <button
          type="submit"
          className="is-primary"
          disabled={
            pending ||
            planPending ||
            objectivePending ||
            objectiveDeletePending ||
            !settings ||
            loadingSettings ||
            recurringLoading ||
            !!recurringError ||
            !!settingsError ||
            sessionAttempts === null ||
            !!sessionAttemptsError ||
            !captureMode ||
            !realityMode ||
            !draft.title.trim()
          }
        >
          {pending ? 'Salvataggio…' : 'Salva modifiche'}
        </button>
      </div>
      {deletingObjective ? (
        <ObjectiveRecordingDeleteDialog
          objectiveLabel={deletingObjective.label}
          busy={objectiveDeletePending}
          onConfirm={confirmRecordedObjectiveDeletion}
          onCancel={() => setDeletingObjective(null)}
        />
      ) : null}
      {deletingAttempt ? (
        <SessionAttemptDeleteDialog
          sessionType={
            deletingAttempt.attempt.plannedScheduleRef == null
              ? 'main'
              : 'named'
          }
          inProgress={deletingAttempt.attempt.open}
          busy={attemptDeletePending}
          onConfirm={confirmAttemptDeletion}
          onCancel={() => setDeletingAttempt(null)}
        />
      ) : null}
      {confirmingDiscard ? (
        <UnsavedChangesDialog
          onDiscard={onCancel}
          onContinue={() => setConfirmingDiscard(false)}
        />
      ) : null}
    </form>
  );
}
