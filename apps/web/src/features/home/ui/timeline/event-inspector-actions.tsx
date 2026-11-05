import { type RefObject, useEffect, useState } from 'react';
import { createPortal } from 'react-dom';

import type { TemporalEventDetailRecord } from '../../../temporal/event-data-source';
import {
  createRemoteRealityObjectiveDataSource,
  type ActivityObjectiveBatch,
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
import {
  createRemoteRecurringProfileEdit,
  type RecurringProfileContext,
  type RecurringProfileEditPreview,
  type RecurringProfileEditScope,
} from '../../../temporal/remote-recurring-profile-edit';
import {
  createRemoteTemporalHardDeletion,
  type TemporalHardDeletionPreview,
  type EventDeletionOccurrenceChoice,
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
import { TemporalReminderControl } from '../../../temporal-create/ui/temporal-create-quick-reminder';
import {
  createRemoteScheduleReminderDataSource,
  type ScheduleReminderView,
} from '../../../temporal/remote-schedule-reminder-data-source';
import { buildEventDuplicateSeed } from '../../../temporal-create/application/event-duplicate-seed';
import type { TimelineCanonicalSchedulePlacement } from './model/timeline-types';
import { TimelineInspectorIcon } from './timeline-inspector-icon';
import { RecurringEditScopeDialog } from './recurring-edit-scope-dialog';
import { RecurringSeriesEditor } from './recurring-series-editor';
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
  const [recurringSource] = useState(createRemoteRecurringProfileEdit);
  const [hardDelete] = useState(createRemoteTemporalHardDeletion);
  const [deletePreviews, setDeletePreviews] = useState<
    readonly TemporalHardDeletionPreview[] | null
  >(null);
  const [deletionChoices, setDeletionChoices] = useState<
    readonly EventDeletionOccurrenceChoice[]
  >([]);
  const [selectedDeletionOccurrence, setSelectedDeletionOccurrence] =
    useState('');
  const [profileSource] = useState(createRemoteEventProfileDataSource);
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
  const [objectiveRows, setObjectiveRows] = useState<ActivityObjectiveDraft[]>(
    [],
  );
  const [realityPolicy, setRealityPolicy] = useState<Readonly<{
    mode: RealityMode;
    stateRef: string | null;
  }> | null>(null);
  const [realityMode, setRealityMode] = useState<RealityMode>('manual');
  const [removedObjectives, setRemovedObjectives] = useState<string[]>([]);
  const [objectiveError, setObjectiveError] = useState('');
  const [inspectingObjective, setInspectingObjective] =
    useState<ActivityObjectiveDraft | null>(null);
  const [areaChoice, setAreaChoice] = useState<EventLifeAreaChoice | null>(
    null,
  );
  const [areaSelection, setAreaSelection] = useState('');
  const [editingProfile, setEditingProfile] = useState(false);
  const [editChoice, setEditChoice] = useState<{
    context: RecurringProfileContext;
    selectedProtection: RecurringProfileEditPreview['selectedProtection'];
  } | null>(null);
  const [editScope, setEditScope] =
    useState<RecurringProfileEditScope>('only_this');
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
      const [loaded, area, objectives, reality, reminder] = await Promise.all([
        context && occurrenceRef && eventSource.loadOccurrenceEvent
          ? eventSource.loadOccurrenceEvent(occurrenceRef)
          : profileSource.load(eventRef),
        context ? Promise.resolve(null) : areaSource.load(eventRef),
        context
          ? Promise.resolve([])
          : objectiveSource.listObjectives('event', eventRef),
        context
          ? Promise.resolve(null)
          : objectiveSource.getRealityPolicy('event', eventRef),
        context ||
        !scheduleRef ||
        (placement.kind !== 'named-zone-local' && placement.kind !== 'absolute')
          ? Promise.resolve(null)
          : reminderSource.get(scheduleRef),
      ]);
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
      setObjectiveRows(objectives.map(existingObjectiveDraft));
      setRealityPolicy(reality);
      setRealityMode(reality?.mode ?? 'manual');
      setRemovedObjectives([]);
      setObjectiveError('');
      setInspectingObjective(null);
      setAreaChoice(area);
      setAreaSelection(area?.currentRef ?? '');
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
        (!recurringContext &&
          realityPolicy !== null &&
          realityMode !== realityPolicy.mode) ||
        (!recurringContext &&
          areaChoice !== null &&
          (areaSelection || null) !== areaChoice.currentRef);
      if (
        changed &&
        !window.confirm('Scartare le modifiche Event non salvate?')
      )
        return;
    }
    setProfileDraft(null);
    setInspectingObjective(null);
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
            current.presentationOrder !== original.presentationOrder
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
      const normalized: EventProfileDraft = {
        title: profileDraft.title.trim(),
        description: profileDraft.description?.trim() || null,
        location: profileDraft.location?.trim() || null,
        colorCode: profileDraft.colorCode?.trim().toUpperCase() || null,
      };
      if (recurringContext) {
        const changed = Object.fromEntries(
          (Object.keys(normalized) as (keyof EventProfileDraft)[])
            .filter((key) => normalized[key] !== (profile[key] ?? null))
            .map((key) => [key, normalized[key]]),
        );
        if (Object.keys(changed).length === 0) {
          throw new Error('Nessuna modifica da salvare.');
        }
        await recurringSource.saveEventProfile(
          recurringContext,
          editScope,
          changed,
          systemTemporalIdFactory.operationId(),
        );
      } else {
        const objectives = await prepareObjectives();
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
            throw new Error(message);
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
          (areaSelection || null) !== areaChoice.currentRef;
        const realityChanged =
          realityPolicy !== null && realityMode !== realityPolicy.mode;
        if (
          !profileChanged &&
          !agendaChanged &&
          !areaChanged &&
          !objectives &&
          !realityChanged &&
          !schedule &&
          !reminderChanged
        ) {
          throw new Error('Nessuna modifica da salvare.');
        }
        if (
          agendaChanged ||
          areaChanged ||
          objectives ||
          realityChanged ||
          schedule ||
          reminderChanged
        ) {
          await profileSource.reviseAtomic(
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
                    },
                  }
                : {}),
              ...(objectives ? { objectives } : {}),
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
        } else {
          await profileSource.revise(
            eventRef,
            profile,
            normalized,
            systemTemporalIdFactory.operationId(),
          );
        }
      }
      setProfile(null);
      setProfileDraft(null);
      setEditingProfile(false);
      setProfileNotice('Evento aggiornato.');
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Modifica Event rifiutata.',
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
      const [event, participants, referents, recurring, reality, objectives] =
        await Promise.all([
          eventSource.loadEvent(eventRef),
          participationSource.listExpectedParticipation(eventRef),
          participationSource.listPersonReferents(),
          recurrenceGuard.isRecurring(eventRef),
          objectiveSource.getRealityPolicy('event', eventRef),
          objectiveSource.listObjectives('event', eventRef),
        ]);
      if (recurring) {
        throw new Error(
          'Questo evento è una sorgente ricorrente: Duplica non può trasformarla in un singolo evento.',
        );
      }
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
        event,
        placement,
        expectedParticipants,
        reality.mode,
        objectives,
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
        setDeletionChoices([]);
        setSelectedDeletionOccurrence('');
        setDeletePreviews([await hardDelete.preview(eventRef, 'event_once')]);
      } else {
        const [series, choices] = await Promise.all([
          hardDelete.preview(eventRef, 'event_series'),
          hardDelete.eventOccurrences(eventRef),
        ]);
        const selected =
          occurrenceRef !== null &&
          choices.some((choice) => choice.occurrenceRef === occurrenceRef)
            ? occurrenceRef
            : '';
        setDeletionChoices(choices);
        setSelectedDeletionOccurrence(selected);
        const instance =
          selected === ''
            ? null
            : await hardDelete.preview(selected, 'event_instance');
        setDeletePreviews(instance === null ? [series] : [instance, series]);
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
      {toolbarTarget ? createPortal(toolbar, toolbarTarget) : toolbar}
      {editChoice ? (
        <RecurringEditScopeDialog
          subjectLabel="Evento"
          selectedProtection={editChoice.selectedProtection}
          busy={busy}
          onOnlyThis={() => {
            const choice = editChoice;
            setEditChoice(null);
            void openProfileEditor('only_this', choice.context);
          }}
          onFollowing={() => {
            const choice = editChoice;
            setEditChoice(null);
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
          closeRequestRef={closeRequestRef}
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
          <div className="timeline-event-profile-editor__body">
            {recurringContext ? (
              <div role="status">
                <p>Ambito: solo questa istanza.</p>
              </div>
            ) : null}
            <div className="temporal-create-title-row has-tools timeline-activity-editor__title-row timeline-event-profile-editor__title-row">
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
            </div>
            {!recurringContext ? (
              <>
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
                {scheduleRef &&
                (placement.kind === 'named-zone-local' ||
                  placement.kind === 'absolute') ? (
                  <TemporalReminderControl
                    value={reminderLead}
                    disabled={
                      busy ||
                      (reminderLead === null &&
                        placement.kind !== 'absolute' &&
                        (scheduleDraft?.kind !== 'timed' ||
                          !scheduleDraft.zoneId))
                    }
                    onChange={setReminderLead}
                  />
                ) : null}
                <TemporalCreateEventAgenda
                  parts={agendaDraft}
                  maxPartLength={1000}
                  onChange={setAgendaDraft}
                />
                {areaChoice ? (
                  <label className="timeline-event-profile-editor__area">
                    Life Area (opzionale)
                    <select
                      disabled={busy}
                      value={areaSelection}
                      onChange={(event) => setAreaSelection(event.target.value)}
                    >
                      <option value="">Nessuna Life Area</option>
                      {areaChoice.options.map((row) => (
                        <option key={row.ref} value={row.ref}>
                          {row.name}
                        </option>
                      ))}
                    </select>
                  </label>
                ) : null}
                <section
                  className="temporal-create-reality-objectives timeline-activity-editor__outcome"
                  aria-label="Svolgimento e obiettivi"
                >
                  <div className="temporal-create-reality-objectives__heading timeline-activity-editor__section-heading">
                    <div>
                      <h3>Svolgimento e obiettivi</h3>
                      <p>
                        Decidi se verificare lo svolgimento e quali risultati
                        vuoi misurare.
                      </p>
                    </div>
                  </div>
                  <div className="temporal-create-reality-objectives__block is-reality">
                    <div className="temporal-create-reality-objectives__block-copy">
                      <strong>Svolgimento dell’evento</strong>
                      <span>
                        Come vuoi gestire la conferma dello svolgimento?
                      </span>
                    </div>
                    <div
                      className="temporal-create-reality-mode"
                      role="radiogroup"
                      aria-label="Verifica dello svolgimento"
                    >
                      {(
                        [
                          ['manual', 'Nessuna verifica'],
                          ['review_on_end', 'Chiedi al termine'],
                          ['auto_confirm_outcome', 'Conferma automatica'],
                        ] as const
                      ).map(([mode, label]) => (
                        <button
                          key={mode}
                          type="button"
                          role="radio"
                          aria-checked={realityMode === mode}
                          className={realityMode === mode ? 'is-active' : ''}
                          disabled={busy}
                          onClick={() => setRealityMode(mode)}
                        >
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
                    <div className="temporal-create-reality-objectives__block-copy">
                      <strong>Obiettivi</strong>
                      <span>
                        Aggiungi solo ciò che vuoi verificare o misurare
                        separatamente.
                      </span>
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
                            disabled={busy}
                            onInspect={() => setInspectingObjective(row)}
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
                              if (target < 0 || target >= visible.length)
                                return;
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
                      {inspectingObjective ? (
                        <p role="status">
                          {inspectingObjective.label}:{' '}
                          {inspectingObjective.original?.observationRef
                            ? 'risultato registrato; lo storico resta conservato.'
                            : 'nessun risultato registrato.'}
                        </p>
                      ) : null}
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
                          ＋ Aggiungi obiettivo
                        </button>
                      </div>
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
            ) : null}
            <section
              className="timeline-event-profile-editor__details"
              aria-label="Dettagli Event"
            >
              <label>
                Località Event
                <input
                  disabled={busy}
                  placeholder="Località"
                  value={profileDraft.location ?? ''}
                  onChange={(event) => {
                    const location = event.currentTarget.value || null;
                    setProfileDraft((draft) => draft && { ...draft, location });
                  }}
                />
              </label>
              <label>
                Colore Event (#RRGGBB)
                <input
                  disabled={busy}
                  maxLength={7}
                  placeholder="#RRGGBB"
                  value={profileDraft.colorCode ?? ''}
                  onChange={(event) => {
                    const colorCode = event.currentTarget.value || null;
                    setProfileDraft(
                      (draft) => draft && { ...draft, colorCode },
                    );
                  }}
                />
              </label>
            </section>
            <section className="timeline-event-profile-editor__description">
              <label>
                Descrizione Event
                <textarea
                  disabled={busy}
                  placeholder="Descrizione"
                  value={profileDraft.description ?? ''}
                  onChange={(event) => {
                    const description = event.currentTarget.value || null;
                    setProfileDraft(
                      (draft) => draft && { ...draft, description },
                    );
                  }}
                />
              </label>
            </section>
          </div>
          <div className="timeline-event-profile-editor__actions">
            <button type="button" disabled={busy} onClick={cancelProfile}>
              Annulla
            </button>
            <button
              type="button"
              disabled={busy || !profileDraft.title.trim()}
              onClick={() => void saveProfile()}
            >
              Salva modifiche
            </button>
          </div>
        </div>
      ) : null}
      {profileNotice ? <p role="status">{profileNotice}</p> : null}
      {deletePreviews ? (
        <div className="timeline-activity-inspector__confirmation">
          <p>
            L’eliminazione è definitiva e comprende Schedule, promemoria,
            Objective e dati storici collegati all’Evento o all’istanza. La
            rimozione dalla Timeline è un’operazione diversa.
          </p>
          {deletionChoices.length > 0 ? (
            <label>
              Istanza Event da eliminare
              <select
                value={selectedDeletionOccurrence}
                disabled={busy}
                onChange={(event) => {
                  const selected = event.currentTarget.value;
                  void (async () => {
                    setBusy(true);
                    setError('');
                    try {
                      const series = deletePreviews.find(
                        (preview) => preview.scope === 'event_series',
                      );
                      if (!series) {
                        throw new Error(
                          'Anteprima della serie non disponibile.',
                        );
                      }
                      const instance = selected
                        ? await hardDelete.preview(selected, 'event_instance')
                        : null;
                      setSelectedDeletionOccurrence(selected);
                      setDeletePreviews(
                        instance ? [instance, series] : [series],
                      );
                    } catch (reason) {
                      setError(
                        reason instanceof Error
                          ? reason.message
                          : 'Impossibile selezionare l’istanza.',
                      );
                    } finally {
                      setBusy(false);
                    }
                  })();
                }}
              >
                <option value="">Seleziona una Occurrence specifica</option>
                {deletionChoices.map((choice) => (
                  <option
                    key={choice.occurrenceRef}
                    value={choice.occurrenceRef}
                  >
                    {choice.displayLabel}
                  </option>
                ))}
              </select>
            </label>
          ) : null}
          {deletePreviews.map((preview) => (
            <button
              type="button"
              key={preview.scope}
              disabled={busy}
              onClick={() => void acceptDeletion(preview)}
            >
              {preview.scope === 'event_once'
                ? 'Conferma eliminazione definitiva'
                : preview.scope === 'event_instance'
                  ? 'Solo questa istanza'
                  : 'Tutta la serie'}
            </button>
          ))}
          {deletionChoices.length !== 0 && selectedDeletionOccurrence === '' ? (
            <p>
              Per «Solo questa istanza» seleziona la data dell’Occurrence.
              «Tutta la serie» elimina anche tutte le altre istanze.
            </p>
          ) : null}
          <button
            type="button"
            disabled={busy}
            onClick={() => {
              setDeletePreviews(null);
              setDeletionChoices([]);
              setSelectedDeletionOccurrence('');
            }}
          >
            Annulla
          </button>
        </div>
      ) : null}
      {error ? <p role="alert">{error}</p> : null}
    </div>
  );
}
