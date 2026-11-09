import { type RefObject, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { detectDeviceTimeZone } from '@dante/time';

import type { TemporalEventDetailRecord } from '../../../temporal/event-data-source';
import {
  createRemoteRealityObjectiveDataSource,
  type ActivityObjectiveBatch,
  type ObjectiveAssessment,
  type ObjectiveView,
  type RealityMode,
} from '../../../temporal/remote-reality-objective-data-source';
import {
  createRemoteEventLifeAreaSettings,
  type EventLifeAreaChoice,
} from '../../../temporal/remote-event-life-area-settings';
import {
  createRemoteEventProfileDataSource,
  type EventProfileDraft,
} from '../../../temporal/remote-event-profile-data-source';
import { createRemoteEventRecurrenceGuard } from '../../../temporal/remote-event-recurrence-guard';
import { createRemoteExistingRecurrence } from '../../../temporal/remote-existing-recurrence';
import {
  createRemoteRecurringProfileEdit,
  type RecurringProfileContext,
  type RecurringProfileEditPreview,
  type RecurringProfileEditScope,
} from '../../../temporal/remote-recurring-profile-edit';
import {
  createRemoteTemporalHardDeletion,
  type TemporalHardDeletionPreview,
} from '../../../temporal/remote-temporal-hard-deletion';
import { createRemoteTemporalOrganizationDataSource } from '../../../temporal/remote-organization';
import {
  createRemoteDraftVault,
  notifyDraftVaultUpdated,
} from '../../../temporal-create/application/remote-draft-vault';
import { draftVaultSnapshotFromDuplicate } from '../../../temporal-create/application/draft-vault-from-duplicate';
import { createRemoteTemporalEventAgendaDataSource } from '../../../temporal/remote-event-agenda-data-source';
import { createRemoteTemporalResponsibilityDataSource } from '../../../temporal/remote-responsibility-data-source';
import { systemTemporalIdFactory } from '../../../temporal/model';
import type { ActivityDuplicateSeed } from '../../../temporal-create/application/activity-duplicate-seed';
import { TemporalCreateEventAgenda } from '../../../temporal-create/ui/temporal-create-event-agenda';
import '../../../temporal-create/ui/temporal-editor-section-typography.css';
import { TemporalEventParticipantsFields } from '../../../temporal-create/ui/temporal-create-event-participants';
import type { TemporalCreateEventParticipantDraft } from '../../../temporal-create/model/temporal-create-u2-authoring';
import { TemporalReminderControl } from '../../../temporal-create/ui/temporal-create-quick-reminder';
import {
  TemporalColorControl,
  TEMPORAL_DEFAULT_COLOR,
} from '../../../temporal-create/ui/temporal-color-control';
import {
  TemporalAssignedLifeAreaSwatch,
  TemporalLifeAreaSelect,
} from '../../../temporal-create/ui/temporal-life-area-select';
import {
  createRemoteScheduleReminderDataSource,
  type ScheduleReminderView,
} from '../../../temporal/remote-schedule-reminder-data-source';
import { buildEventDuplicateSeed } from '../../../temporal-create/application/event-duplicate-seed';
import {
  createRemotePlacementLockDataSource,
  type PlacementLockState,
} from '../../../temporal/remote-placement-lock-data-source';
import { TemporalCreatePlacementLockButton } from '../../../temporal-create/ui/temporal-create-placement-lock-button';
import type { ExistingRecurrenceControlHandle } from './existing-recurrence-control';
import { TemporalAuthoringTitleRow } from '../../../temporal-create/ui/temporal-authoring-title-row';
import type { TimelineCanonicalSchedulePlacement } from './model/timeline-types';
import { TimelineInspectorIcon } from './timeline-inspector-icon';
import { RecurringEditScopeDialog } from './recurring-edit-scope-dialog';
import { RecurringSeriesEditor } from './recurring-series-editor';
import { ExistingRecurrenceControl } from './existing-recurrence-control';
import { UnsavedChangesDialog } from './unsaved-changes-dialog';
import { TemporalDeleteDialog } from './temporal-delete-dialog';
import { ObjectiveRecordingDeleteDialog } from './objective-recording-delete-dialog';
import {
  EventScheduleEditor,
  eventScheduleDraftFromPlacement,
  eventSchedulePlacementFromDraft,
  type EventScheduleDraft,
} from './event-schedule-editor';
import {
  ActivityObjectiveRow,
  existingObjectiveDraft,
  newObjectiveDraft,
  objectiveChanged,
  objectiveData,
  objectiveDraftError,
  type ActivityObjectiveDraft,
} from './activity-objective-row';

export function EventInspectorActions({
  eventRef,
  placement,
  itemTitle,
  scheduleLabel,
  occurrenceRef = null,
  scheduleRef = null,
  placementMaterialStateRef = null,
  onDeleted,
  onDuplicate,
  onCancelScope,
  onEditorStateChange,
  closeRequestRef,
  toolbarTarget = null,
}: Readonly<{
  eventRef: string;
  placement: TimelineCanonicalSchedulePlacement;
  itemTitle?: string;
  scheduleLabel?: string;
  occurrenceRef?: string | null;
  scheduleRef?: string | null;
  placementMaterialStateRef?: string | null;
  onDeleted?: () => void;
  onDuplicate: (seed: ActivityDuplicateSeed) => void;
  onCancelScope?: () => void;
  onEditorStateChange?: (mode: 'profile' | 'series' | null) => void;
  closeRequestRef?: RefObject<(() => void) | null>;
  toolbarTarget?: HTMLElement | null;
}>) {
  const [eventSource] = useState(createRemoteTemporalEventAgendaDataSource);
  const [participationSource] = useState(
    createRemoteTemporalResponsibilityDataSource,
  );
  const [recurrenceGuard] = useState(createRemoteEventRecurrenceGuard);
  const [existingRecurrence] = useState(createRemoteExistingRecurrence);
  const recurrenceControl = useRef<ExistingRecurrenceControlHandle>(null);
  const recurrenceOperation = useRef<string | null>(null);
  const recurrenceResume = useRef<{
    eventRef: string;
    expectedProfileRevision: number;
    scheduleRef: string;
    expectedPlacementStateRef: string;
  } | null>(null);
  const [recurrenceSelected, setRecurrenceSelected] = useState(false);
  const [existingSeed, setExistingSeed] = useState<string | null>(null);
  const [recurringSource] = useState(createRemoteRecurringProfileEdit);
  const [hardDelete] = useState(createRemoteTemporalHardDeletion);
  const [deletePreviews, setDeletePreviews] = useState<
    readonly TemporalHardDeletionPreview[] | null
  >(null);

  const [profileSource] = useState(createRemoteEventProfileDataSource);
  const [placementLockSource] = useState(createRemotePlacementLockDataSource);
  const [placementLockInitial, setPlacementLockInitial] =
    useState<PlacementLockState | null>(null);
  const [placementLockDraft, setPlacementLockDraft] = useState(false);
  const [areaSource] = useState(createRemoteEventLifeAreaSettings);
  const [objectiveSource] = useState(createRemoteRealityObjectiveDataSource);
  const [reminderSource] = useState(createRemoteScheduleReminderDataSource);
  const [organizationSource] = useState(
    createRemoteTemporalOrganizationDataSource,
  );
  const [draftVault] = useState(createRemoteDraftVault);
  const [profile, setProfile] = useState<TemporalEventDetailRecord | null>(
    null,
  );
  const [profileDraft, setProfileDraft] = useState<EventProfileDraft | null>(
    null,
  );
  const [agendaDraft, setAgendaDraft] = useState<readonly string[]>([]);
  const [scheduleDraft, setScheduleDraft] = useState<EventScheduleDraft | null>(
    null,
  );
  const [scheduleInitial, setScheduleInitial] =
    useState<EventScheduleDraft | null>(null);
  const [scheduleError, setScheduleError] = useState('');
  const [reminderCurrent, setReminderCurrent] =
    useState<ScheduleReminderView | null>(null);
  const [reminderLead, setReminderLead] = useState<number | null>(null);
  const [reminderInitial, setReminderInitial] = useState<number | null>(null);
  const [participantsInitial, setParticipantsInitial] = useState<
    readonly TemporalCreateEventParticipantDraft[]
  >([]);
  const [participantsDraft, setParticipantsDraft] = useState<
    readonly TemporalCreateEventParticipantDraft[]
  >([]);
  const [objectiveRows, setObjectiveRows] = useState<ActivityObjectiveDraft[]>(
    [],
  );
  const [correctingObjective, setCorrectingObjective] =
    useState<ObjectiveView | null>(null);
  const [deletingObjective, setDeletingObjective] = useState<ObjectiveView | null>(null);
  const [objectiveDeletePending, setObjectiveDeletePending] = useState(false);
  const [correctedValue, setCorrectedValue] = useState('');
  const [correctedBoolean, setCorrectedBoolean] = useState('true');
  const [correctedAssessment, setCorrectedAssessment] =
    useState<ObjectiveAssessment>('unknown');
  const correctionOperation = useRef<string | null>(null);
  const [realityPolicy, setRealityPolicy] = useState<Readonly<{
    mode: RealityMode;
    stateRef: string | null;
  }> | null>(null);
  const [realityMode, setRealityMode] = useState<RealityMode>('manual');
  const [removedObjectives, setRemovedObjectives] = useState<string[]>([]);
  const [objectiveError, setObjectiveError] = useState('');
  const [areaChoice, setAreaChoice] = useState<EventLifeAreaChoice | null>(
    null,
  );
  const [areaSelection, setAreaSelection] = useState('');
  const [areaQuery, setAreaQuery] = useState('');
  const [areaError, setAreaError] = useState('');
  const [newAreaColor, setNewAreaColor] = useState(TEMPORAL_DEFAULT_COLOR);
  const [editingProfile, setEditingProfile] = useState(false);
  const [confirmingDiscard, setConfirmingDiscard] = useState(false);
  const [editChoice, setEditChoice] = useState<{
    context: RecurringProfileContext;
    selectedProtection: RecurringProfileEditPreview['selectedProtection'];
    firstExistingEvent?: boolean;
  } | null>(null);
  const [editScope, setEditScope] =
    useState<RecurringProfileEditScope>('only_this');
  const [verifiedSource, setVerifiedSource] = useState<{
    eventRef: string;
    recurring: boolean;
  } | null>(null);
  const vaultEligible =
    occurrenceRef === null &&
    verifiedSource?.eventRef === eventRef &&
    !verifiedSource.recurring;
  useEffect(() => {
    if (occurrenceRef !== null) return;
    let active = true;
    void recurrenceGuard
      .isRecurring(eventRef)
      .then((recurring) => {
        if (active) setVerifiedSource({ eventRef, recurring });
      })
      .catch(() => {
        // A failed owner lookup cannot enable a destructive Vault action.
        if (active) setVerifiedSource({ eventRef, recurring: true });
      });
    return () => {
      active = false;
    };
  }, [eventRef, occurrenceRef, recurrenceGuard]);

  const [recurringContext, setRecurringContext] =
    useState<RecurringProfileContext | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const [profileNotice, setProfileNotice] = useState('');

  useEffect(() => {
    onEditorStateChange?.(
      editingProfile
        ? recurringContext && editScope !== 'only_this'
          ? 'series'
          : 'profile'
        : null,
    );
  }, [editScope, editingProfile, onEditorStateChange, recurringContext]);

  const openProfileEditor = async (
    selectedScope: RecurringProfileEditScope = 'only_this',
    context: RecurringProfileContext | null = null,
  ) => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const [
        loaded,
        area,
        objectives,
        reality,
        reminder,
        participants,
        referents,
        seed,
        placementLock,
      ] = await Promise.all([
        context && occurrenceRef && eventSource.loadOccurrenceEvent
          ? eventSource.loadOccurrenceEvent(occurrenceRef)
          : profileSource.load(eventRef),
        areaSource.load(eventRef),
        objectiveSource.listObjectives(
          context ? 'occurrence' : 'event',
          context ? context.occurrenceRef : eventRef,
        ),
        objectiveSource.getRealityPolicy(
          context ? 'occurrence' : 'event',
          context ? context.occurrenceRef : eventRef,
        ),
        !scheduleRef ||
        (placement.kind !== 'named-zone-local' && placement.kind !== 'absolute')
          ? Promise.resolve(null)
          : reminderSource.get(scheduleRef),
        context
          ? participationSource.listOccurrenceExpectedParticipation(
              context.occurrenceRef,
            )
          : participationSource.listExpectedParticipation(eventRef),
        participationSource.listPersonReferents(),
        context
          ? Promise.resolve(null)
          : existingRecurrence.eventSeed(eventRef),
        scheduleRef
          ? placementLockSource.get(scheduleRef)
          : Promise.resolve(null),
      ]);
      if (
        scheduleRef !== null &&
        placementLock?.scheduleRef !== scheduleRef.toLowerCase()
      ) {
        throw new Error('Blocco spostamenti Event non disponibile.');
      }
      setPlacementLockInitial(placementLock);
      setPlacementLockDraft(placementLock?.locked ?? false);
      setExistingSeed(seed);
      if (loaded.profileRevision === undefined) {
        throw new Error('Revisione del profilo Event non disponibile.');
      }
      const patch = context
        ? await recurringSource.loadOccurrencePatch(context)
        : {};
      const effective = { ...loaded, ...patch };
      setProfile(effective);
      setAgendaDraft(effective.agendaParts ?? []);
      const initialSchedule = eventScheduleDraftFromPlacement(placement);
      setScheduleDraft(initialSchedule);
      setScheduleInitial(initialSchedule);
      setScheduleError('');
      setReminderCurrent(reminder);
      setReminderLead(reminder?.enabled ? reminder.leadMinutes : null);
      setReminderInitial(reminder?.enabled ? reminder.leadMinutes : null);
      const labels = new Map(
        referents.map((person) => [person.personRef, person.displayLabel]),
      );
      const expectedParticipants = participants
        .filter((participant) => participant.requirementCode !== null)
        .map((participant) => ({
          personRef: participant.participantIsSelf
            ? 'self'
            : participant.participantPersonRef,
          displayLabel: participant.participantIsSelf
            ? 'Io'
            : (labels.get(participant.participantPersonRef) ??
              'Persona non disponibile'),
          requirementCode: participant.requirementCode!,
        }));
      setParticipantsInitial(expectedParticipants);
      setParticipantsDraft(expectedParticipants);
      setObjectiveRows(objectives.map(existingObjectiveDraft));
      setCorrectingObjective(null);
      correctionOperation.current = null;
      setRealityPolicy(reality);
      setRealityMode(reality?.mode ?? 'manual');
      setRemovedObjectives([]);
      setObjectiveError('');
      setAreaChoice(area);
      setAreaSelection(
        context ? (effective.lifeAreaRef ?? '') : (area?.currentRef ?? ''),
      );
      setAreaQuery(
        area?.options.find(
          (option) =>
            option.ref === (context ? effective.lifeAreaRef : area.currentRef),
        )?.name ?? '',
      );
      setAreaError('');
      setNewAreaColor(TEMPORAL_DEFAULT_COLOR);
      setRecurrenceSelected(false);
      recurrenceOperation.current = null;
      recurrenceResume.current = null;
      setProfileDraft({
        title: effective.title,
        description: effective.description ?? null,
        location: effective.location ?? null,
        colorCode: effective.colorCode ?? null,
      });
      setRecurringContext(context);
      setEditScope(selectedScope);
      setEditingProfile(true);
      setProfileNotice('');
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Dettagli Event non disponibili.',
      );
    } finally {
      setBusy(false);
    }
  };

  const chooseProfileEditor = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const recurring = await recurrenceGuard.isRecurring(eventRef);
      if (!recurring) {
        // The physical Event is standalone, but its saved schedule can also
        // be the canonical first generated Occurrence of a second source.
        const first = await existingRecurrence.eventFirstOccurrence(eventRef);
        if (first !== null) {
          const context = await recurringSource.loadOccurrenceContext(first);
          const preview = await recurringSource.loadPreview(
            context,
            'only_this',
          );
          setEditChoice({
            context,
            selectedProtection: preview.selectedProtection,
            firstExistingEvent: true,
          });
          return;
        }
        await openProfileEditor();
        return;
      }
      if (!occurrenceRef) {
        throw new Error(
          'Apri un’istanza della ricorrenza per scegliere l’ambito della modifica.',
        );
      }
      const context =
        await recurringSource.loadOccurrenceContext(occurrenceRef);
      if (context.sourceRef !== eventRef) {
        throw new Error(
          'Questa istanza non appartiene all’Evento selezionato.',
        );
      }
      const preview = await recurringSource.loadPreview(context, 'only_this');
      setEditChoice({
        context,
        selectedProtection: preview.selectedProtection,
      });
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Ricorrenza non disponibile.',
      );
    } finally {
      setBusy(false);
    }
  };

  const cancelProfile = () => {
    if (confirmingDiscard) {
      setConfirmingDiscard(false);
      return;
    }
    if (profile && profileDraft) {
      const changed =
        profileDraft.title !== profile.title ||
        (profileDraft.description ?? '') !== (profile.description ?? '') ||
        (profileDraft.location ?? '') !== (profile.location ?? '') ||
        (profileDraft.colorCode ?? '') !== (profile.colorCode ?? '') ||
        agendaDraft.some(
          (part, index) => part !== profile.agendaParts?.[index],
        ) ||
        agendaDraft.length !== (profile.agendaParts?.length ?? 0) ||
        objectiveRows.some((row) => objectiveChanged(row)) ||
        removedObjectives.length > 0 ||
        JSON.stringify(scheduleDraft) !== JSON.stringify(scheduleInitial) ||
        reminderLead !== reminderInitial ||
        (placementLockInitial !== null &&
          placementLockDraft !== placementLockInitial.locked) ||
        JSON.stringify(participantsDraft) !==
          JSON.stringify(participantsInitial) ||
        (realityPolicy !== null && realityMode !== realityPolicy.mode) ||
        (areaChoice !== null &&
          (areaSelection || null) !==
            (recurringContext
              ? (profile.lifeAreaRef ?? null)
              : areaChoice.currentRef)) ||
        recurrenceSelected;
      if (changed) {
        setConfirmingDiscard(true);
        return;
      }
    }
    setProfileDraft(null);
    setRecurrenceSelected(false);
    recurrenceOperation.current = null;
    recurrenceResume.current = null;
    setPlacementLockInitial(null);
    setCorrectingObjective(null);
    correctionOperation.current = null;
    setEditingProfile(false);
  };

  useEffect(() => {
    if (
      !closeRequestRef ||
      (editingProfile && recurringContext && editScope !== 'only_this')
    ) {
      return;
    }
    closeRequestRef.current = editingProfile ? cancelProfile : null;
    return () => {
      closeRequestRef.current = null;
    };
  });

  const beginResultCorrection = (objective: ObjectiveView) => {
    if (busy || !objective.observationRef || !objective.evaluationStateRef) {
      setObjectiveError(
        'Rettifica non disponibile senza una valutazione corrente.',
      );
      return;
    }
    if (
      removedObjectives.length > 0 ||
      objectiveRows.some((row) => objectiveChanged(row))
    ) {
      setObjectiveError(
        'Salva prima le modifiche agli obiettivi, poi rettifica il risultato.',
      );
      return;
    }
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
    if (!correctingObjective || busy) return;
    const objective = correctingObjective;
    if (!objective.evaluationStateRef) {
      setObjectiveError('Aggiorna la scheda: manca la valutazione corrente.');
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
    setBusy(true);
    setObjectiveError('');
    const kind = recurringContext ? 'occurrence' : 'event';
    const subjectRef = recurringContext?.occurrenceRef ?? eventRef;
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
      .then(() => objectiveSource.listObjectives(kind, subjectRef))
      .then((fresh) => {
        setObjectiveRows(fresh.map(existingObjectiveDraft));
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
      .finally(() => setBusy(false));
  };

  const requestRecordedObjectiveDeletion = (objective: ObjectiveView) => {
    if (busy || objectiveDeletePending || !objective.evaluationStateRef ||
        !objective.observationRef) return;
    // Recorded-result removal must not destroy or block unrelated
    // unfinished Objective drafts in this Edit form.
    setObjectiveError('');
    setDeletingObjective(objective);
  };

  const confirmRecordedObjectiveDeletion = () => {
    if (!deletingObjective?.evaluationStateRef || objectiveDeletePending) return;
    const objective = deletingObjective;
    const kind = recurringContext ? 'occurrence' : 'event';
    const subjectRef = recurringContext?.occurrenceRef ?? eventRef;
    setObjectiveDeletePending(true);
    setBusy(true);
    setObjectiveError('');
    void objectiveSource
      .deleteRecordedResult(
        objective.objectiveRef, objective.evaluationStateRef!,
      )
      .then(() => objectiveSource.listObjectives(kind, subjectRef))
      .then((fresh) => {
        const restored = fresh.find(
          (item) => item.objectiveRef === objective.objectiveRef,
        );
        if (!restored || restored.observationRef || restored.evaluationStateRef) {
          throw new Error('Registrazione eliminata, ma rilettura non coerente. Riapri Modifica.');
        }
        // Merge the accepted readback into the single affected row only.
        // Existing draft edits, unfinished new Objectives and removals survive.
        setObjectiveRows((rows) => rows.map((row) =>
          row.objectiveRef === objective.objectiveRef
            ? existingObjectiveDraft(restored)
            : row,
        ));
        setCorrectingObjective(null);
        setDeletingObjective(null);
        correctionOperation.current = null;
      })
      .catch((reason: unknown) => {
        setDeletingObjective(null);
        setObjectiveError(
          reason instanceof Error
            ? reason.message
            : 'Impossibile eliminare la registrazione. Riapri Modifica.',
        );
      })
      .finally(() => {
        setBusy(false);
        setObjectiveDeletePending(false);
      });
  };

  const prepareObjectives =
    async (): Promise<ActivityObjectiveBatch | null> => {
      const retained = objectiveRows.filter(
        (row) => !removedObjectives.includes(row.id),
      );
      for (const row of retained) {
        const problem = objectiveDraftError(row);
        if (problem) {
          setObjectiveError(`${row.label.trim() || 'Obiettivo'}: ${problem}`);
          throw new Error(`${row.label.trim() || 'Obiettivo'}: ${problem}`);
        }
      }
      const added = retained.filter((row) => !row.objectiveRef);
      const revised = retained.filter(
        (row) => row.objectiveRef && objectiveChanged(row),
      );
      const retired = objectiveRows.filter(
        (row) => row.objectiveRef && removedObjectives.includes(row.id),
      );
      if (added.length + revised.length + retired.length === 0) return null;
      const definitions = await Promise.all(
        [...revised, ...retired].map(async (row) => {
          const current = await objectiveSource.getDefinition(
            row.objectiveRef!,
          );
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
              'Un obiettivo è cambiato: riapri Modifica e riprova.',
            );
          }
          return current;
        }),
      );
      return {
        add: added.map((row) => ({
          ...objectiveData(row),
          operationId: row.operationId,
        })),
        revise: revised.map((row, index) => ({
          objectiveRef: row.objectiveRef!,
          change: {
            ...objectiveData(row),
            operationId: row.operationId,
            expectedRevision: definitions[index]!.definitionRevision,
            expectedVerificationRevision:
              definitions[index]!.verificationRevision ??
              row.original?.verificationRevision ??
              0,
            scopeCode: 'only_this' as const,
            seriesState: null,
          },
        })),
        retire: retired.map((row, index) => ({
          objectiveRef: row.objectiveRef!,
          operationId: row.operationId,
          expectedRevision:
            definitions[revised.length + index]!.definitionRevision,
        })),
      };
    };

  const saveProfile = async () => {
    if (!profile || !profileDraft || busy) return;
    setBusy(true);
    setError('');
    try {
      const proposedRecurrence = recurrenceControl.current?.getRule() ?? null;
      if (recurrenceResume.current && !proposedRecurrence) {
        recurrenceResume.current = null;
        setProfile(null);
        setProfileDraft(null);
        setRecurrenceSelected(false);
        setEditingProfile(false);
        setProfileNotice('Modifiche salvate; ripetizione non avviata.');
        return;
      }
      if (
        proposedRecurrence &&
        scheduleDraft?.kind === 'timed' &&
        !scheduleDraft.zoneId
      ) {
        throw new Error('Per ripetere questo Evento serve un orario con fuso.');
      }
      if (
        proposedRecurrence &&
        (!scheduleRef ||
          !placementMaterialStateRef ||
          profile.profileRevision === undefined)
      ) {
        throw new Error(
          'Programmazione Event non disponibile per la ripetizione.',
        );
      }
      if (proposedRecurrence && recurrenceResume.current) {
        const createdSourceRef = await existingRecurrence.startEvent(
          recurrenceResume.current,
          proposedRecurrence,
          (recurrenceOperation.current ??=
            systemTemporalIdFactory.operationId()),
        );
        recurrenceResume.current = null;
        setExistingSeed(createdSourceRef);
        setProfile(null);
        setProfileDraft(null);
        setRecurrenceSelected(false);
        setEditingProfile(false);
        setProfileNotice('Ripetizione avviata da questo Evento.');
        return;
      }
      let acceptedProfile = profile;
      let acceptedStateRef = placementMaterialStateRef;
      let acceptedEdit = false;
      const areaName = areaQuery.trim().replace(/\s+/g, ' ');
      const selectedArea = areaChoice?.options.find(
        (option) => option.ref === areaSelection,
      );
      const creatingLocalArea = areaName !== '' && !selectedArea;
      if (
        (selectedArea &&
          selectedArea.name.toLocaleLowerCase() !==
            areaName.toLocaleLowerCase()) ||
        (creatingLocalArea && (areaName.length > 100 || !areaChoice))
      ) {
        const message = 'Nome Life Area non valido.';
        setAreaError(message);
        throw new Error(message);
      }
      const normalized: EventProfileDraft = {
        title: profileDraft.title.trim(),
        description: profileDraft.description?.trim() || null,
        location: profileDraft.location?.trim() || null,
        colorCode: profileDraft.colorCode?.trim().toUpperCase() || null,
      };
      const placementLockChanged =
        placementLockInitial !== null &&
        placementLockDraft !== placementLockInitial.locked;
      if (recurringContext) {
        const changed = Object.fromEntries(
          (Object.keys(normalized) as (keyof EventProfileDraft)[])
            .filter((key) => normalized[key] !== (profile[key] ?? null))
            .map((key) => [key, normalized[key]]),
        );
        const objectives = await prepareObjectives();
        const scheduleChanged =
          JSON.stringify(scheduleDraft) !== JSON.stringify(scheduleInitial);
        const reminderChanged = reminderLead !== reminderInitial;
        const structureChanged =
          JSON.stringify(agendaDraft) !==
            JSON.stringify(profile.agendaParts ?? []) ||
          (areaSelection || null) !== (profile.lifeAreaRef ?? null) ||
          creatingLocalArea ||
          JSON.stringify(
            participantsDraft.map(({ personRef, requirementCode }) => ({
              personRef,
              requirementCode,
            })),
          ) !==
            JSON.stringify(
              participantsInitial.map(({ personRef, requirementCode }) => ({
                personRef,
                requirementCode,
              })),
            );
        if (
          reminderLead !== null &&
          scheduleDraft &&
          (scheduleDraft.kind !== 'timed' || !scheduleDraft.zoneId)
        ) {
          throw new Error('Il promemoria richiede un orario con fuso.');
        }
        if (
          scheduleChanged &&
          (!scheduleDraft || !scheduleRef || !placementMaterialStateRef)
        ) {
          throw new Error('Programmazione dell’istanza non disponibile.');
        }
        if (reminderChanged && !scheduleRef) {
          throw new Error('Schedule del promemoria non disponibile.');
        }
        if (
          Object.keys(changed).length === 0 &&
          !structureChanged &&
          !objectives &&
          !scheduleChanged &&
          !reminderChanged &&
          !placementLockChanged &&
          realityMode === realityPolicy?.mode
        ) {
          setProfileDraft(null);
          setEditingProfile(false);
          return;
        }
        let selectedSchedule: ReturnType<
          typeof eventSchedulePlacementFromDraft
        > | null = null;
        if (scheduleChanged && scheduleDraft) {
          try {
            selectedSchedule = eventSchedulePlacementFromDraft(scheduleDraft);
          } catch (reason) {
            const message =
              reason instanceof Error
                ? reason.message
                : 'Orario Evento non valido.';
            setScheduleError(message);
            throw new Error(message, { cause: reason });
          }
        }
        await recurringSource.saveEventLocal(
          recurringContext,
          changed,
          {
            agendaParts: agendaDraft,
            lifeAreaRef: areaSelection || null,
            participants: participantsDraft,
            ...(creatingLocalArea
              ? { newArea: { name: areaName, colorCode: newAreaColor } }
              : {}),
          },
          {
            placementLock:
              placementLockChanged && placementLockInitial
                ? {
                    scheduleRef: placementLockInitial.scheduleRef,
                    locked: placementLockDraft,
                    expectedRevision: placementLockInitial.revision,
                  }
                : null,
            schedule:
              scheduleChanged &&
              selectedSchedule &&
              scheduleRef &&
              placementMaterialStateRef
                ? {
                    scheduleRef,
                    materialStateRef: placementMaterialStateRef,
                    placement: selectedSchedule,
                  }
                : null,
            reminder:
              reminderChanged && scheduleRef
                ? {
                    scheduleRef,
                    stateRef: reminderCurrent?.materialStateRef ?? null,
                    leadMinutes: reminderLead,
                  }
                : null,
            reality:
              realityMode !== realityPolicy?.mode
                ? {
                    mode: realityMode,
                    stateRef: realityPolicy?.stateRef ?? null,
                  }
                : null,
            objectives,
          },
          systemTemporalIdFactory.operationId(),
        );
      } else {
        const objectives = await prepareObjectives();
        const initialParticipants = new Map(
          participantsInitial.map((item) => [
            item.personRef,
            item.requirementCode,
          ]),
        );
        const currentParticipants = new Map(
          participantsDraft.map((item) => [
            item.personRef,
            item.requirementCode,
          ]),
        );
        const participantChanges = [
          ...new Set([
            ...initialParticipants.keys(),
            ...currentParticipants.keys(),
          ]),
        ]
          .filter(
            (ref) =>
              initialParticipants.get(ref) !== currentParticipants.get(ref),
          )
          .map((participantRef) => ({
            participantRef,
            requirementCode: currentParticipants.get(participantRef) ?? null,
            expectedRequirementCode:
              initialParticipants.get(participantRef) ?? null,
          }));
        const scheduleChanged =
          JSON.stringify(scheduleDraft) !== JSON.stringify(scheduleInitial);
        const reminderChanged = reminderLead !== reminderInitial;
        if (
          reminderLead !== null &&
          scheduleDraft &&
          (scheduleDraft.kind !== 'timed' || !scheduleDraft.zoneId)
        ) {
          throw new Error('Il promemoria richiede un orario con fuso.');
        }
        if (reminderChanged && !scheduleRef) {
          throw new Error('Schedule del promemoria non disponibile.');
        }
        let schedule: ReturnType<
          typeof eventSchedulePlacementFromDraft
        > | null = null;
        if (scheduleChanged) {
          if (!scheduleDraft || !scheduleRef || !placementMaterialStateRef) {
            throw new Error(
              'Programmazione Evento non disponibile: riapri la modifica.',
            );
          }
          try {
            schedule = eventSchedulePlacementFromDraft(scheduleDraft);
          } catch (reason) {
            const message =
              reason instanceof Error
                ? reason.message
                : 'Orario Evento non valido.';
            setScheduleError(message);
            throw new Error(message, { cause: reason });
          }
        }
        const profileChanged =
          normalized.title !== profile.title ||
          normalized.description !== (profile.description ?? null) ||
          normalized.location !== (profile.location ?? null) ||
          normalized.colorCode !== (profile.colorCode ?? null);
        const agendaChanged =
          agendaDraft.length !== (profile.agendaParts?.length ?? 0) ||
          agendaDraft.some(
            (part, index) => part !== profile.agendaParts?.[index],
          );
        const areaChanged =
          areaChoice !== null &&
          ((areaSelection || null) !== areaChoice.currentRef ||
            creatingLocalArea);
        const realityChanged =
          realityPolicy !== null && realityMode !== realityPolicy.mode;
        if (
          !profileChanged &&
          !agendaChanged &&
          !areaChanged &&
          !objectives &&
          !realityChanged &&
          !schedule &&
          !reminderChanged &&
          !placementLockChanged &&
          participantChanges.length === 0 &&
          !proposedRecurrence
        ) {
          setProfileDraft(null);
          setEditingProfile(false);
          return;
        }
        if (
          agendaChanged ||
          areaChanged ||
          objectives ||
          realityChanged ||
          schedule ||
          reminderChanged ||
          placementLockChanged ||
          participantChanges.length > 0
        ) {
          const saved = await profileSource.reviseAtomic(
            eventRef,
            profile,
            {
              ...(profileChanged ? { profile: normalized } : {}),
              ...(agendaChanged ? { agendaParts: agendaDraft } : {}),
              ...(areaChanged && areaChoice
                ? {
                    lifeArea: {
                      ref: areaSelection || null,
                      expectedRevision: areaChoice.currentRevision,
                      ...(creatingLocalArea
                        ? {
                            newArea: {
                              name: areaName,
                              colorCode: newAreaColor,
                            },
                          }
                        : {}),
                    },
                  }
                : {}),
              ...(objectives ? { objectives } : {}),
              ...(placementLockChanged && placementLockInitial
                ? {
                    placementLock: {
                      scheduleRef: placementLockInitial.scheduleRef,
                      locked: placementLockDraft,
                      expectedRevision: placementLockInitial.revision,
                    },
                  }
                : {}),
              ...(schedule && scheduleRef && placementMaterialStateRef
                ? {
                    schedule: {
                      scheduleRef,
                      expectedMaterialStateRef: placementMaterialStateRef,
                      placement: schedule,
                    },
                  }
                : {}),
              ...(reminderChanged && scheduleRef
                ? {
                    reminder: {
                      scheduleRef,
                      expectedStateRef:
                        reminderCurrent?.materialStateRef ?? null,
                      enabled: reminderLead !== null,
                      leadMinutes:
                        reminderLead ?? reminderCurrent?.leadMinutes ?? 15,
                    },
                  }
                : {}),
              ...(participantChanges.length > 0
                ? { participants: participantChanges }
                : {}),
              ...(realityChanged && realityPolicy
                ? {
                    reality: {
                      mode: realityMode,
                      expectedStateRef: realityPolicy.stateRef,
                    },
                  }
                : {}),
            },
            systemTemporalIdFactory.operationId(),
          );
          acceptedProfile = saved ?? profile;
          acceptedStateRef =
            saved?.updatedPlacementStateRef ?? placementMaterialStateRef;
          acceptedEdit = true;
        } else if (profileChanged) {
          acceptedProfile = await profileSource.revise(
            eventRef,
            profile,
            normalized,
            systemTemporalIdFactory.operationId(),
          );
          acceptedEdit = true;
        }
      }
      if (proposedRecurrence && scheduleRef && acceptedStateRef) {
        if (acceptedProfile.profileRevision === undefined) {
          throw new Error('Revisione Event non disponibile.');
        }
        const basis = {
          eventRef,
          expectedProfileRevision: acceptedProfile.profileRevision,
          scheduleRef,
          expectedPlacementStateRef: acceptedStateRef,
        };
        if (acceptedEdit) recurrenceResume.current = basis;
        const createdSourceRef = await existingRecurrence.startEvent(
          basis,
          proposedRecurrence,
          (recurrenceOperation.current ??=
            systemTemporalIdFactory.operationId()),
        );
        recurrenceResume.current = null;
        setExistingSeed(createdSourceRef);
      }
      setProfile(null);
      setProfileDraft(null);
      setRecurrenceSelected(false);
      setEditingProfile(false);
      setProfileNotice(
        proposedRecurrence
          ? 'Ripetizione avviata da questo Evento.'
          : 'Evento aggiornato.',
      );
    } catch (reason) {
      const message =
        reason instanceof Error ? reason.message : 'Modifica Event rifiutata.';
      setError(
        recurrenceResume.current
          ? `Modifiche salvate, ripetizione non avviata: ${message}. Premi Salva per riprovare.`
          : message,
      );
    } finally {
      setBusy(false);
    }
  };

  const duplicate = async (intoVault = false) => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const recurring = await recurrenceGuard.isRecurring(eventRef);
      if (recurring && (intoVault || !occurrenceRef)) {
        throw new Error(
          'Apri un’istanza della ricorrenza per precompilarla in Create avanzato.',
        );
      }
      if (recurring && !eventSource.loadOccurrenceEvent) {
        throw new Error('Dettagli della singola istanza non disponibili.');
      }
      // Read the selected Occurrence (including local exceptions), not the
      // Event source. Read-only: no new Event, Schedule or factual record.
      const context =
        recurring && occurrenceRef
          ? await recurringSource.loadOccurrenceContext(occurrenceRef)
          : null;
      if (context && context.sourceRef !== eventRef) {
        throw new Error('L’istanza non appartiene alla serie selezionata.');
      }
      const subjectRef = context?.occurrenceRef ?? eventRef;
      const subjectKind = context ? 'occurrence' : 'event';
      const [event, participants, referents, reality, objectives, reminder] =
        await Promise.all([
          context && eventSource.loadOccurrenceEvent
            ? eventSource.loadOccurrenceEvent(context.occurrenceRef)
            : eventSource.loadEvent(eventRef),
          context
            ? participationSource.listOccurrenceExpectedParticipation(
                context.occurrenceRef,
              )
            : participationSource.listExpectedParticipation(eventRef),
          participationSource.listPersonReferents(),
          objectiveSource.getRealityPolicy(subjectKind, subjectRef),
          objectiveSource.listObjectives(subjectKind, subjectRef),
          scheduleRef &&
          ['named-zone-local', 'absolute'].includes(placement.kind)
            ? reminderSource.get(scheduleRef)
            : Promise.resolve(null),
        ]);
      const effectiveEvent = context
        ? { ...event, ...(await recurringSource.loadOccurrencePatch(context)) }
        : event;
      const labels = new Map(
        referents.map((row) => [row.personRef, row.displayLabel]),
      );
      const expectedParticipants = participants
        .filter((row) => row.requirementCode !== null)
        .map((row) => {
          const label = row.participantIsSelf
            ? 'Io'
            : labels.get(row.participantPersonRef);
          if (!label || row.requirementCode === null) {
            throw new Error(
              'Impossibile duplicare: un partecipante non è più disponibile.',
            );
          }
          return {
            personRef: row.participantPersonRef,
            displayLabel: label,
            requirementCode: row.requirementCode,
          };
        });
      const seed = buildEventDuplicateSeed(
        effectiveEvent,
        placement,
        expectedParticipants,
        reality.mode,
        objectives,
        reminder?.enabled ? reminder.leadMinutes : null,
      );
      if (!intoVault) {
        onDuplicate(seed);
      } else {
        const organization = await organizationSource.load();
        const area =
          event.lifeAreaRef === null || event.lifeAreaRef === undefined
            ? undefined
            : organization.areas.find((row) => row.ref === event.lifeAreaRef);
        if (event.lifeAreaRef && !area) {
          throw new Error(
            'Life Area Event non disponibile: la bozza non è stata salvata.',
          );
        }
        const selected = area
          ? {
              kind: 'existing' as const,
              lifeAreaRef: area.ref,
              label: area.name,
              expectedRevision: area.revision,
              colorCode: area.colorCode,
              colorChanged: false,
            }
          : undefined;
        await draftVault.save(draftVaultSnapshotFromDuplicate(seed, selected), {
          draftRef: crypto.randomUUID(),
          revision: null,
          operationId: crypto.randomUUID(),
        });
        notifyDraftVaultUpdated();
        setProfileNotice(
          'Copia salvata nelle Bozze. L’Evento originale rimane attivo.',
        );
      }
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Impossibile preparare una duplicazione fedele dell’evento.',
      );
    } finally {
      setBusy(false);
    }
  };

  const confirmDeletion = async () => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      const recurring = await recurrenceGuard.isRecurring(eventRef);
      if (!recurring) {
        const seededSource = await existingRecurrence.eventSeed(eventRef);
        if (seededSource === null) {
          setDeletePreviews([await hardDelete.preview(eventRef, 'event_once')]);
        } else {
          // Preserve the source Event's physical first-instance identity.
          const [instance, series] = await Promise.all([
            hardDelete.preview(eventRef, 'event_once'),
            hardDelete.preview(eventRef, 'event_series'),
          ]);
          setDeletePreviews([instance, series]);
        }
      } else {
        const series = await hardDelete.preview(eventRef, 'event_series');
        // A single instance may only be removed when its identity is certain.
        // No free-form instance picker in a destructive confirmation.
        let selected: string | null = null;
        if (occurrenceRef) {
          const choices = await hardDelete.eventOccurrences(eventRef);
          if (
            choices.some((choice) => choice.occurrenceRef === occurrenceRef)
          ) {
            selected = occurrenceRef;
          }
        } else if (scheduleRef) {
          const choices = await hardDelete.eventOccurrences(eventRef);
          const matches = choices.filter(
            (choice) => choice.scheduleRef === scheduleRef,
          );
          if (matches.length === 1) selected = matches[0]!.occurrenceRef;
        }
        const instance = selected
          ? await hardDelete.preview(selected, 'event_instance')
          : null;
        setDeletePreviews(instance ? [instance, series] : [series]);
      }
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Impossibile verificare l’evento da eliminare.',
      );
    } finally {
      setBusy(false);
    }
  };

  const acceptDeletion = async (preview: TemporalHardDeletionPreview) => {
    if (busy) return;
    setBusy(true);
    setError('');
    try {
      await hardDelete.deleteConfirmed(preview);
      if (onDeleted) onDeleted();
      else window.location.reload();
    } catch (reason) {
      setError(
        reason instanceof Error
          ? reason.message
          : 'Eliminazione Event rifiutata.',
      );
    } finally {
      setBusy(false);
    }
  };

  const toolbar = (
    <div className="timeline-activity-inspector__toolbar">
      <button
        type="button"
        disabled={busy}
        aria-label="Modifica"
        title="Modifica"
        onClick={() =>
          editingProfile ? cancelProfile() : void chooseProfileEditor()
        }
      >
        {toolbarTarget ? (
          <TimelineInspectorIcon name="edit" />
        ) : editingProfile ? (
          'Chiudi modifica Event'
        ) : (
          'Modifica'
        )}
      </button>
      <button
        type="button"
        disabled={busy}
        aria-label="Duplica"
        title="Duplica"
        onClick={() => void duplicate()}
      >
        {toolbarTarget ? (
          <TimelineInspectorIcon name="copy" />
        ) : busy ? (
          'Preparazione…'
        ) : (
          'Duplica'
        )}
      </button>
      {vaultEligible ? (
        <button
          type="button"
          disabled={busy}
          aria-label="Copia in Bozze"
          title="Copia in Bozze"
          onClick={() => void duplicate(true)}
        >
          {toolbarTarget ? (
            <TimelineInspectorIcon name="vault" />
          ) : (
            'Copia in Bozze'
          )}
        </button>
      ) : null}
      <button
        type="button"
        disabled={busy}
        aria-label="Elimina Event"
        title="Elimina Event"
        onClick={() => void confirmDeletion()}
      >
        {toolbarTarget ? <TimelineInspectorIcon name="trash" /> : 'Elimina'}
      </button>
    </div>
  );

  return (
    <div className="timeline-activity-inspector__actions">
      {editingProfile
        ? null
        : toolbarTarget
          ? createPortal(toolbar, toolbarTarget)
          : toolbar}
      {editChoice ? (
        <RecurringEditScopeDialog
          subjectLabel="Evento"
          selectedProtection={editChoice.selectedProtection}
          busy={busy}
          onOnlyThis={() => {
            const choice = editChoice;
            setEditChoice(null);
            void (choice.firstExistingEvent
              ? openProfileEditor()
              : openProfileEditor('only_this', choice.context));
          }}
          onFollowing={() => {
            const choice = editChoice;
            setEditChoice(null);
            if (choice.firstExistingEvent) {
              // The shared series editor reads the generated Occurrence.
              // Do not fetch a second synthetic Event for the physical first.
              setEditScope(
                choice.selectedProtection ? 'from_next' : 'this_and_following',
              );
              setRecurringContext(choice.context);
              setEditingProfile(true);
              setProfileNotice('');
              return;
            }
            void openProfileEditor(
              choice.selectedProtection ? 'from_next' : 'this_and_following',
              choice.context,
            );
          }}
          onCancel={() => {
            setEditChoice(null);
            onCancelScope?.();
          }}
        />
      ) : null}
      {editingProfile && recurringContext && editScope !== 'only_this' ? (
        <RecurringSeriesEditor
          occurrenceRef={recurringContext.occurrenceRef}
          scope={editScope}
          owner="event"
          {...(closeRequestRef ? { closeRequestRef } : {})}
          onSaved={() => {
            setEditingProfile(false);
            setProfileNotice('Serie aggiornata.');
          }}
          onCancel={() => setEditingProfile(false)}
        />
      ) : editingProfile && profileDraft && profile ? (
        <div
          className="timeline-event-profile-editor"
          aria-label="Modifica profilo Event"
        >
          <div
            className="timeline-event-profile-editor__body"
            inert={confirmingDiscard || undefined}
          >
            <TemporalAuthoringTitleRow
              kind="event"
              className="timeline-activity-editor__title-row timeline-event-profile-editor__title-row"
            >
              <label className="timeline-activity-editor__title">
                <span className="timeline-activity-editor__visually-hidden">
                  Titolo Event
                </span>
                <input
                  className="temporal-create-title-input"
                  disabled={busy}
                  maxLength={300}
                  placeholder="Titolo"
                  value={profileDraft.title}
                  onChange={(event) => {
                    const title = event.currentTarget.value;
                    setProfileDraft((draft) => draft && { ...draft, title });
                  }}
                />
              </label>
              <div className="temporal-create-title-row__tools">
                <TemporalCreatePlacementLockButton
                  kind="event"
                  locked={placementLockDraft}
                  disabled={
                    busy ||
                    !scheduleRef ||
                    placementLockInitial?.scheduleRef !==
                      scheduleRef.toLowerCase()
                  }
                  onToggle={() => setPlacementLockDraft((locked) => !locked)}
                />
              </div>
            </TemporalAuthoringTitleRow>
            <>
              <TemporalCreateEventAgenda
                parts={agendaDraft}
                maxPartLength={1000}
                onChange={setAgendaDraft}
                editStyle
              />
              {scheduleDraft ? (
                <EventScheduleEditor
                  draft={scheduleDraft}
                  disabled={busy}
                  error={scheduleError}
                  onChange={(next) => {
                    setScheduleDraft(next);
                    setScheduleError('');
                  }}
                />
              ) : (
                <p role="status">
                  Questa forma di programmazione si modifica dall’Inspector
                  della Schedule.
                </p>
              )}
              {!recurringContext && occurrenceRef === null && scheduleDraft ? (
                existingSeed ? (
                  <div
                    className="timeline-activity-editor__repeat"
                    role="group"
                    aria-label="Ripeti"
                  >
                    Ripeti · Serie attiva
                  </div>
                ) : scheduleRef && placementMaterialStateRef ? (
                  <ExistingRecurrenceControl
                    ref={recurrenceControl}
                    kind="event"
                    date={scheduleDraft.startDate}
                    startTime={scheduleDraft.startTime}
                    allDay={scheduleDraft.kind === 'all-day'}
                    zoneId={scheduleDraft.zoneId ?? detectDeviceTimeZone()}
                    disambiguation={
                      scheduleDraft.disambiguation === 'later'
                        ? 'later'
                        : 'earlier'
                    }
                    onSelectionChange={(selected) => {
                      setRecurrenceSelected(selected);
                      recurrenceOperation.current = null;
                    }}
                  />
                ) : null
              ) : null}
              <div className="timeline-activity-editor__area-color">
                <div className="temporal-create-life-area-field">
                  {areaSelection ? (
                    <TemporalAssignedLifeAreaSwatch
                      colorCode={
                        areaChoice?.options.find(
                          (option) => option.ref === areaSelection,
                        )?.colorCode
                      }
                    />
                  ) : (
                    <TemporalColorControl
                      value={
                        areaQuery.trim() && !areaSelection
                          ? newAreaColor
                          : (profileDraft.colorCode ?? TEMPORAL_DEFAULT_COLOR)
                      }
                      label={
                        areaQuery.trim() && !areaSelection
                          ? 'Colore nuova Life Area'
                          : 'Colore attività o evento'
                      }
                      onChange={(colorCode) => {
                        if (areaQuery.trim() && !areaSelection) {
                          setNewAreaColor(colorCode);
                        } else {
                          setProfileDraft(
                            (draft) => draft && { ...draft, colorCode },
                          );
                        }
                      }}
                    />
                  )}
                  {areaChoice ? (
                    <div
                      className="timeline-activity-editor__area-choice"
                      data-edit-invalid={!!areaError}
                    >
                      <TemporalLifeAreaSelect
                        query={areaQuery}
                        label="Life Area (opzionale)"
                        options={areaChoice.options.map((option) => ({
                          id: option.ref,
                          label: option.name,
                          colorCode: option.colorCode,
                        }))}
                        selectedId={areaSelection || null}
                        disabled={busy}
                        onQueryChange={(query) => {
                          setAreaQuery(query);
                          const matched = areaChoice.options.find(
                            (option) =>
                              option.name.toLocaleLowerCase() ===
                              query.trim().toLocaleLowerCase(),
                          );
                          setAreaSelection(matched?.ref ?? '');
                          if (query.trim() && !matched) {
                            // A Life Area owns its appearance: do not retain
                            // the standalone Event item color when creating one.
                            setProfileDraft(
                              (draft) => draft && { ...draft, colorCode: null },
                            );
                          }
                          setAreaError('');
                        }}
                        onChoose={(option) => {
                          setAreaSelection(option.id);
                          setAreaQuery(option.label);
                          // A Life Area's color owns its Events. Drop a stale
                          // standalone color override on explicit assignment.
                          setProfileDraft(
                            (draft) => draft && { ...draft, colorCode: null },
                          );
                          setAreaError('');
                        }}
                        onClear={() => {
                          setAreaSelection('');
                          setAreaQuery('');
                          setAreaError('');
                        }}
                      />
                      {areaQuery.trim() && !areaSelection ? (
                        <small role="status">
                          La nuova Life Area sarà creata insieme al salvataggio
                          dell’Evento.
                        </small>
                      ) : null}
                      {areaError ? (
                        <small
                          className="temporal-create-field-error"
                          role="alert"
                        >
                          {areaError}
                        </small>
                      ) : null}
                    </div>
                  ) : null}
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
                          disabled={busy || objectiveDeletePending}
                          onCorrectRecorded={() => {
                            if (row.original) beginResultCorrection(row.original);
                          }}
                          onDeleteRecorded={() => {
                            if (row.original) requestRecordedObjectiveDeletion(row.original);
                          }}
                          onChange={(patch) => {
                            setObjectiveRows((rows) =>
                              rows.map((item) =>
                                item.id === row.id
                                  ? { ...item, ...patch }
                                  : item,
                              ),
                            );
                            setObjectiveError('');
                          }}
                          onMove={(direction) => {
                            const target = index + direction;
                            if (target < 0 || target >= visible.length) return;
                            setObjectiveRows((rows) => {
                              const next = [...rows];
                              const other = visible[target]!;
                              const first = next.findIndex(
                                (item) => item.id === row.id,
                              );
                              const second = next.findIndex(
                                (item) => item.id === other.id,
                              );
                              if (first < 0 || second < 0) return rows;
                              next[first] = {
                                ...next[first]!,
                                presentationOrder: other.presentationOrder,
                              };
                              next[second] = {
                                ...next[second]!,
                                presentationOrder: row.presentationOrder,
                              };
                              return next.sort(
                                (a, b) =>
                                  a.presentationOrder - b.presentationOrder,
                              );
                            });
                          }}
                          onRemove={() => {
                            if (row.original?.observationRef) {
                              setObjectiveError(
                                'Questo obiettivo ha risultati registrati e non può essere eliminato.',
                              );
                              return;
                            }
                            if (row.objectiveRef) {
                              setRemovedObjectives((ids) => [...ids, row.id]);
                            } else {
                              setObjectiveRows((rows) =>
                                rows.filter((item) => item.id !== row.id),
                              );
                            }
                          }}
                        />
                      ))}
                    <div className="temporal-create-objectives__root-actions">
                      <button
                        type="button"
                        className="temporal-create-objectives__add"
                        disabled={busy}
                        onClick={() =>
                          setObjectiveRows((rows) => [
                            ...rows,
                            newObjectiveDraft(
                              Math.max(
                                -1,
                                ...rows.map((item) => item.presentationOrder),
                              ) + 1,
                            ),
                          ])
                        }
                      >
                        + Obiettivo
                      </button>
                    </div>
                    {correctingObjective ? (
                      <fieldset disabled={busy}>
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
                              <option value="not_satisfied">
                                Non raggiunto
                              </option>
                              <option value="unknown">Sconosciuto</option>
                              <option value="indeterminate">
                                Indeterminato
                              </option>
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
                          La rettifica non elimina osservazioni o valutazioni
                          precedenti.
                        </p>
                      </fieldset>
                    ) : null}
                    {objectiveError ? (
                      <small
                        className="temporal-create-field-error"
                        role="alert"
                      >
                        {objectiveError}
                      </small>
                    ) : null}
                  </div>
                </section>
              </section>
            </>
            <div className="timeline-activity-editor__location">
              <input
                className="temporal-create-u2-location"
                aria-label="Località"
                disabled={busy}
                placeholder="Località"
                value={profileDraft.location ?? ''}
                onChange={(event) => {
                  const location = event.currentTarget.value || null;
                  setProfileDraft((draft) => draft && { ...draft, location });
                }}
              />
            </div>
            {scheduleRef &&
            (placement.kind === 'named-zone-local' ||
              placement.kind === 'absolute') ? (
              <TemporalReminderControl
                value={reminderLead}
                disabled={
                  busy ||
                  (reminderLead === null &&
                    placement.kind !== 'absolute' &&
                    (scheduleDraft?.kind !== 'timed' || !scheduleDraft.zoneId))
                }
                onChange={setReminderLead}
              />
            ) : null}
            <TemporalEventParticipantsFields
              participants={participantsDraft}
              onChange={setParticipantsDraft}
              disabled={busy}
            />
            <section
              className="timeline-activity-editor__description temporal-create-section is-wide temporal-create-description-section"
              aria-label="Descrizione"
            >
              <h3>Descrizione</h3>
              <textarea
                className="temporal-create-u2-description temporal-create-advanced-description"
                aria-label="Descrizione"
                rows={5}
                disabled={busy}
                value={profileDraft.description ?? ''}
                onChange={(event) => {
                  const description = event.currentTarget.value || null;
                  setProfileDraft(
                    (draft) => draft && { ...draft, description },
                  );
                }}
              />
            </section>
          </div>
          <div
            className="timeline-event-profile-editor__actions dante-temporal-panel-actions"
            inert={confirmingDiscard || undefined}
          >
            <button type="button" disabled={busy} onClick={cancelProfile}>
              Annulla
            </button>
            <button
              type="button"
              className="is-primary"
              disabled={busy || !profileDraft.title.trim()}
              onClick={() => void saveProfile()}
            >
              Salva modifiche
            </button>
          </div>
          {confirmingDiscard ? (
            <UnsavedChangesDialog
              onDiscard={() => {
                setConfirmingDiscard(false);
                setProfileDraft(null);
                setRecurrenceSelected(false);
                recurrenceOperation.current = null;
                recurrenceResume.current = null;
                setEditingProfile(false);
              }}
              onContinue={() => setConfirmingDiscard(false)}
            />
          ) : null}
        </div>
      ) : null}
      {profileNotice ? <p role="status">{profileNotice}</p> : null}
      {deletePreviews ? (
        <TemporalDeleteDialog
          subject="evento"
          itemTitle={itemTitle ?? profile?.title ?? 'Evento'}
          scheduleLabel={scheduleLabel}
          busy={busy}
          error={error}
          note={
            deletePreviews.some(
              (preview) => preview.scope === 'event_series',
            ) &&
            !deletePreviews.some(
              (preview) =>
                preview.scope === 'event_instance' ||
                preview.scope === 'event_once',
            )
              ? 'Per eliminare una singola istanza, aprila dalla Timeline.'
              : undefined
          }
          choices={deletePreviews.map((preview) => ({
            key: preview.scope,
            label:
              preview.scope === 'event_once'
                ? deletePreviews.length > 1
                  ? 'Solo questa istanza'
                  : 'Elimina definitivamente'
                : preview.scope === 'event_instance'
                  ? 'Solo questa istanza'
                  : 'Tutta la serie',
            onConfirm: () => void acceptDeletion(preview),
          }))}
          onCancel={() => {
            setDeletePreviews(null);
            setError('');
          }}
        />
      ) : null}
      {deletingObjective ? (
        <ObjectiveRecordingDeleteDialog
          objectiveLabel={deletingObjective.label}
          busy={objectiveDeletePending}
          onConfirm={confirmRecordedObjectiveDeletion}
          onCancel={() => setDeletingObjective(null)}
        />
      ) : null}
      {error && !deletePreviews ? <p role="alert">{error}</p> : null}
    </div>
  );
}
