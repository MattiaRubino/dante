import type { PlainDate } from '@dante/time';
import { useCallback, useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import {
  createRemoteTemporalAuthoringDataSource,
  systemTemporalIdFactory,
  type TemporalAuthoringDataSource,
  type TemporalValidationIssue,
} from '../../temporal';
import { createRemoteScheduleReminderDataSource } from '../../temporal/remote-schedule-reminder-data-source';
import { createRemoteTemporalResponsibilityDataSource } from '../../temporal/remote-responsibility-data-source';
import { invalidateTemporalTimelineRead } from '../../temporal/timeline-invalidation';
import { createRemoteRecurringAuthoringDataSource } from '../application/remote-recurring-authoring';
import {
  buildTemporalCreateActivityRecurrence,
  buildTemporalCreateEventRecurrence,
  buildTemporalCreateRecurringEventPolicy,
} from '../application/temporal-create-b14-runtime';
import {
  createLocalTemporalCreateRuntime,
  type TemporalCreateAppliedEffect,
  type TemporalCreatePreparedOperation,
  type TemporalCreateRuntime,
} from '../application/temporal-create-runtime';
import {
  applyTemporalCreateFieldSeed,
  type TemporalCreateFieldSeed,
} from '../application/temporal-create-seed';
import {
  temporalCreateTimelinePreviewFromFields,
  type TemporalCreateTimelineProjection,
} from '../application/temporal-create-projection';
import {
  createTemporalCreateEventRealityFinalizer,
  createTemporalCreateRealityFinalizer,
} from '../application/temporal-create-reality-finalizer';
import {
  buildTemporalCreateLifeAreaInput,
  buildTemporalCreateObjectiveTemplates,
  buildTemporalCreateRecurringActivityTemplate,
  buildTemporalCreateU2Request,
  temporalCreateHasU6Structure,
  temporalCreateRecurringEventSharedIntentSupported,
  temporalCreateU2QuickIntentSupported,
  validateTemporalCreateU2QuickFields,
  validateTemporalCreateU6Structure,
} from '../application/temporal-create-u2-submit';
import {
  continueTemporalCreateEditing,
  createTemporalCreateFields,
  createTemporalCreateSession,
  discardTemporalCreateSession,
  requestTemporalCreateClose,
  setTemporalCreateSurface,
  updateTemporalCreateFields,
  type TemporalCreateSession,
  type TemporalCreateSurface,
} from '../model/temporal-create-session';
import {
  createTemporalCreateU2AuthoringDraft,
  type TemporalCreateU2AuthoringDraft,
} from '../model/temporal-create-u2-authoring';
import type { ActivityDuplicateSeed } from '../application/activity-duplicate-seed';
import {
  TemporalCreateComposer,
  type TemporalCreateContextOption,
} from './temporal-create-composer';

import './temporal-create.css';
import './temporal-create-u1.css';
import './temporal-create-u1-polish.css';

type InvocationAnchor = Readonly<{
  left: number;
  top: number;
  bottom: number;
}>;

export type TemporalCreateInvocation = Readonly<{
  id: number;
  date: PlainDate;
  startMinute?: number;
  durationMinutes?: number;
  seed?: TemporalCreateFieldSeed;
  duplicate?: ActivityDuplicateSeed;
  anchor?: InvocationAnchor;
}>;

export type TemporalCreateEntryProps = Readonly<{
  defaultDate: PlainDate;
  contexts: readonly TemporalCreateContextOption[];
  request?: TemporalCreateInvocation | null;
  runtime?: TemporalCreateRuntime;
  authoringDataSource?: TemporalAuthoringDataSource;
  onPreview: (projection: TemporalCreateTimelineProjection | null) => void;
  onApplied: (effect: TemporalCreateAppliedEffect) => boolean;
  onBeforeOpen?: (() => void) | undefined;
  creationEnabled?: boolean | undefined;
}>;

function minuteToInput(minute: number): string {
  const safe = Math.max(0, Math.min(1435, Math.round(minute / 5) * 5));
  return `${String(Math.floor(safe / 60)).padStart(2, '0')}:${String(
    safe % 60,
  ).padStart(2, '0')}`;
}

export function TemporalCreateEntry({
  defaultDate,
  contexts,
  request,
  runtime: runtimeOverride,
  authoringDataSource: authoringDataSourceOverride,
  onPreview,
  onApplied,
  onBeforeOpen,
  creationEnabled = true,
}: TemporalCreateEntryProps) {
  const { t, i18n } = useTranslation('common');
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const focusReturnRef = useRef<HTMLElement | null>(null);
  const [runtime] = useState(
    () => runtimeOverride ?? createLocalTemporalCreateRuntime(),
  );
  const [authoringDataSource] = useState(
    () =>
      authoringDataSourceOverride ?? createRemoteTemporalAuthoringDataSource(),
  );
  const [reminderDataSource] = useState(() =>
    createRemoteScheduleReminderDataSource(),
  );
  const [recurringAuthoringDataSource] = useState(() =>
    createRemoteRecurringAuthoringDataSource(),
  );
  const [responsibilityDataSource] = useState(() =>
    createRemoteTemporalResponsibilityDataSource(),
  );
  const requestSeenRef = useRef<number | null>(null);
  const preparedRef = useRef<TemporalCreatePreparedOperation | null>(null);
  const partialPostCreateRef = useRef<(() => Promise<void>) | null>(null);
  const [u2Draft, setU2Draft] = useState<TemporalCreateU2AuthoringDraft>(() =>
    createTemporalCreateU2AuthoringDraft(createTemporalCreateFields()),
  );
  const u2DraftRef = useRef(u2Draft);
  const [postCreateRetry, setPostCreateRetry] = useState(false);
  const commitInFlightRef = useRef(false);
  const [open, setOpen] = useState(false);
  const [session, setSession] = useState<TemporalCreateSession>(() =>
    createTemporalCreateSession(),
  );
  const [issues, setIssues] = useState<readonly TemporalValidationIssue[]>([]);
  const [lifecycle, setLifecycle] = useState<'idle' | 'pending' | 'failed'>(
    'idle',
  );
  const [failureMessage, setFailureMessage] = useState('');
  const [failureTarget, setFailureTarget] = useState<string | null>(null);

  const freshFields = useCallback(
    (
      date: PlainDate,
      startMinute?: number,
      durationMinutes?: number,
      seed?: TemporalCreateFieldSeed,
    ) => {
      const zone = runtime.clock.timeZoneId();
      const targetDate = seed?.date ?? date.toString();
      let minute = startMinute;
      if (minute === undefined) {
        if (targetDate === runtime.clock.today(zone).toString()) {
          const now = runtime.clock.now().toZonedDateTimeISO(zone);
          minute = Math.ceil((now.hour * 60 + now.minute) / 15) * 15;
        } else {
          minute = 9 * 60;
        }
      }
      const base = createTemporalCreateFields({
        date: targetDate,
        timeSemantics: 'timed',
        startTime: seed?.startTime ?? minuteToInput(minute),
        durationMinutes: seed?.durationMinutes ?? durationMinutes ?? 30,
        timeMode: 'zoned',
        timeZoneId: seed?.timeZoneId ?? zone,
        contextId: seed?.contextId ?? '',
      });
      return seed ? applyTemporalCreateFieldSeed(base, seed) : base;
    },
    [runtime],
  );

  const restoreComposerFocus = useCallback(() => {
    const target = focusReturnRef.current ?? triggerRef.current;
    requestAnimationFrame(() => {
      if (target?.isConnected) {
        target.focus({ preventScroll: true });
      } else {
        triggerRef.current?.focus({ preventScroll: true });
      }
    });
  }, []);

  const closeComposer = useCallback(
    (restoreFocus = true) => {
      setOpen(false);
      setIssues([]);
      setFailureMessage('');
      setLifecycle('idle');
      preparedRef.current = null;
      partialPostCreateRef.current = null;
      setPostCreateRetry(false);
      commitInFlightRef.current = false;
      onPreview(null);
      if (restoreFocus) restoreComposerFocus();
    },
    [onPreview, restoreComposerFocus],
  );

  const openComposer = useCallback(
    (
      date: PlainDate,
      startMinute?: number,
      durationMinutes?: number,
      seed?: TemporalCreateFieldSeed,
      duplicate?: ActivityDuplicateSeed,
      externalAnchor?: InvocationAnchor,
      focusReturnTarget?: HTMLElement | null,
    ) => {
      onBeforeOpen?.();
      const fields = freshFields(date, startMinute, durationMinutes, seed);
      const initialDraft = createTemporalCreateU2AuthoringDraft(fields);
      const seededArea = contexts.find(
        (context) => context.id === fields.contextId,
      );
      const areaDraft = seededArea
        ? Object.freeze({
            ...initialDraft,
            lifeArea: Object.freeze({
              kind: 'existing' as const,
              lifeAreaRef: seededArea.id,
              label: seededArea.label,
              expectedRevision: seededArea.revision ?? 1,
              colorCode: seededArea.colorCode ?? null,
              colorChanged: false,
            }),
          })
        : initialDraft;
      u2DraftRef.current = duplicate
        ? Object.freeze({ ...areaDraft, ...duplicate.advanced })
        : areaDraft;
      setU2Draft(u2DraftRef.current);
      setSession(
        duplicate
          ? setTemporalCreateSurface(
              createTemporalCreateSession(fields),
              'full',
            )
          : createTemporalCreateSession(fields),
      );
      setIssues([]);
      setFailureMessage('');
      setLifecycle('idle');
      preparedRef.current = null;
      partialPostCreateRef.current = null;
      setPostCreateRetry(false);
      focusReturnRef.current = focusReturnTarget ?? triggerRef.current;
      void externalAnchor;
      setOpen(true);
    },
    [contexts, freshFields, onBeforeOpen],
  );

  useEffect(() => {
    if (!request || requestSeenRef.current === request.id || open) return;
    requestSeenRef.current = request.id;
    const frame = requestAnimationFrame(() => {
      openComposer(
        request.date,
        request.startMinute,
        request.durationMinutes,
        request.seed,
        request.duplicate,
        request.anchor,
        document.querySelector<HTMLElement>('.timeline-grid'),
      );
    });
    return () => cancelAnimationFrame(frame);
  }, [open, openComposer, request]);

  useEffect(() => {
    if (!open || session.closeDecision === 'confirm-discard') {
      onPreview(null);
      return;
    }
    onPreview(temporalCreateTimelinePreviewFromFields(session.draft.current));
    return () => onPreview(null);
  }, [onPreview, open, session.closeDecision, session.draft]);

  const requestClose = () => {
    if (lifecycle === 'pending') return;
    if (session.draft.current.title.trim().length === 0) {
      closeComposer();
      return;
    }
    const requestResult = requestTemporalCreateClose(session);
    if (requestResult.shouldClose) {
      closeComposer();
      return;
    }
    setSession(requestResult.session);
  };

  const patch = (next: Partial<TemporalCreateSession['draft']['current']>) => {
    if (partialPostCreateRef.current !== null) return;
    const merged = { ...session.draft.current, ...next };
    const eligibleReminder =
      merged.timeSemantics === 'timed' && merged.timeMode === 'zoned';
    const boundedNext = eligibleReminder
      ? next
      : {
          ...next,
          confirmation: { ...merged.confirmation, reminderLeadMinutes: null },
        };
    preparedRef.current = null;
    setIssues([]);
    setFailureMessage('');
    setFailureTarget(null);
    setLifecycle('idle');
    setSession((current) => updateTemporalCreateFields(current, boundedNext));
  };

  const changeSurface = (surface: TemporalCreateSurface) => {
    setSession((current) => setTemporalCreateSurface(current, surface));
  };

  const continueEditing = () => {
    setSession((current) => continueTemporalCreateEditing(current));
  };

  const executeU2Quick = async (
    fields: TemporalCreateSession['draft']['current'],
  ): Promise<boolean> => {
    const structureIssue = validateTemporalCreateU6Structure(
      fields,
      u2DraftRef.current,
    );
    if (structureIssue !== null) {
      setFailureTarget(
        /interval/i.test(structureIssue)
          ? 'activityIntervals'
          : /session/i.test(structureIssue)
            ? 'plannedSessions'
            : 'activityStructure',
      );
      setFailureMessage(structureIssue);
      setLifecycle('failed');
      return false;
    }
    const validation = validateTemporalCreateU2QuickFields(fields);
    if (validation.length > 0) {
      setIssues(validation);
      return false;
    }

    try {
      buildTemporalCreateObjectiveTemplates(u2DraftRef.current);
    } catch (reason) {
      setFailureTarget('objectives');
      setFailureMessage(
        reason instanceof Error ? reason.message : 'Obiettivi non validi.',
      );
      setLifecycle('failed');
      return false;
    }

    const mapped = buildTemporalCreateU2Request(
      fields,
      u2DraftRef.current,
      systemTemporalIdFactory.operationId(),
    );
    commitInFlightRef.current = true;
    setLifecycle('pending');
    setIssues([]);
    setFailureMessage('');
    try {
      const activityAuthored =
        mapped.kind === 'activity'
          ? await authoringDataSource.authorActivity(mapped.request)
          : null;
      const eventAuthored =
        mapped.kind === 'event'
          ? await authoringDataSource.authorEvent(mapped.request)
          : null;
      const authored = activityAuthored ?? eventAuthored;
      if (!authored) throw new Error('Temporal authoring returned no result.');

      const finalizeReality = activityAuthored
        ? createTemporalCreateRealityFinalizer(
            activityAuthored,
            u2DraftRef.current,
          )
        : eventAuthored
          ? createTemporalCreateEventRealityFinalizer(
              eventAuthored,
              u2DraftRef.current,
            )
          : null;
      const reminderLeadMinutes = fields.confirmation.reminderLeadMinutes;
      const scheduleRef = authored.schedule?.scheduleRef ?? null;
      const eventRef = eventAuthored?.item.subjectRef ?? null;
      const participantCommands =
        eventRef === null
          ? Object.freeze([])
          : Object.freeze(
              u2DraftRef.current.eventParticipants.map((participant) =>
                Object.freeze({
                  participant,
                  operationId: systemTemporalIdFactory.operationId(),
                }),
              ),
            );
      if (reminderLeadMinutes !== null && scheduleRef === null) {
        throw new Error(
          i18n.language.toLowerCase().startsWith('en')
            ? 'The item was created, but no Schedule is available for its reminder.'
            : 'La creazione è riuscita, ma non esiste uno Schedule a cui collegare il promemoria.',
        );
      }
      const reminderOperationId =
        reminderLeadMinutes === null
          ? null
          : systemTemporalIdFactory.operationId();
      const finalizePostCreate = async () => {
        await finalizeReality?.();
        if (
          reminderLeadMinutes !== null &&
          scheduleRef !== null &&
          reminderOperationId !== null
        ) {
          await reminderDataSource.configure(scheduleRef, {
            operationId: reminderOperationId,
            expectedMaterialStateRef: null,
            enabled: true,
            leadMinutes: reminderLeadMinutes,
          });
        }
        if (eventRef !== null) {
          for (const command of participantCommands) {
            await responsibilityDataSource.setExpectedParticipation(eventRef, {
              operationId: command.operationId,
              ...(command.participant.personRef === 'self'
                ? {}
                : { participant: command.participant.personRef }),
              requirementCode: command.participant.requirementCode,
              expectedRequirementCode: null,
            });
          }
        }
      };
      try {
        await finalizePostCreate();
      } catch {
        partialPostCreateRef.current = finalizePostCreate;
        setPostCreateRetry(true);
        setLifecycle('failed');
        setFailureMessage(
          i18n.language.toLowerCase().startsWith('en')
            ? 'The item was created, but a follow-up configuration was not saved. Retry safely without creating a duplicate.'
            : 'La creazione è riuscita, ma una configurazione successiva non è stata salvata. Riprova in sicurezza senza creare un duplicato.',
        );
        return false;
      }

      invalidateTemporalTimelineRead();
      setSession(discardTemporalCreateSession(freshFields(defaultDate)));
      closeComposer();
      return true;
    } catch (reason) {
      setLifecycle('failed');
      setFailureMessage(
        reason instanceof Error
          ? reason.message
          : t(($) => $.common.home.timeline.create.failure),
      );
      return false;
    } finally {
      commitInFlightRef.current = false;
    }
  };

  const executeRecurringActivity = async (
    fields: TemporalCreateSession['draft']['current'],
  ): Promise<boolean> => {
    const structureIssue = validateTemporalCreateU6Structure(
      fields,
      u2DraftRef.current,
    );
    if (structureIssue !== null) {
      setFailureTarget(
        /interval/i.test(structureIssue)
          ? 'activityIntervals'
          : /session/i.test(structureIssue)
            ? 'plannedSessions'
            : 'activityStructure',
      );
      setFailureMessage(structureIssue);
      setLifecycle('failed');
      return false;
    }
    const validation = validateTemporalCreateU2QuickFields(fields);
    if (validation.length > 0) {
      setIssues(validation);
      return false;
    }
    try {
      buildTemporalCreateObjectiveTemplates(u2DraftRef.current);
    } catch (reason) {
      setFailureTarget('objectives');
      setFailureMessage(
        reason instanceof Error ? reason.message : 'Obiettivi non validi.',
      );
      setLifecycle('failed');
      return false;
    }

    commitInFlightRef.current = true;
    setLifecycle('pending');
    setIssues([]);
    setFailureMessage('');
    try {
      const recurring = buildTemporalCreateRecurringActivityTemplate(
        fields,
        u2DraftRef.current,
      );
      const lifeArea = buildTemporalCreateLifeAreaInput(u2DraftRef.current);
      await recurringAuthoringDataSource.createRoutine({
        operationId: systemTemporalIdFactory.operationId(),
        title: fields.title.trim(),
        ...(lifeArea ? { lifeArea } : {}),
        tagRefs: Object.freeze([]),
        recurrence: buildTemporalCreateActivityRecurrence(fields),
        durationMinutes: recurring.durationMinutes,
        reminderLeadMinutes: fields.confirmation.reminderLeadMinutes,
        activityTemplate: recurring.template,
      });
      invalidateTemporalTimelineRead();
      setSession(discardTemporalCreateSession(freshFields(defaultDate)));
      closeComposer();
      return true;
    } catch (reason) {
      setLifecycle('failed');
      setFailureMessage(
        reason instanceof Error
          ? reason.message
          : t(($) => $.common.home.timeline.create.failure),
      );
      return false;
    } finally {
      commitInFlightRef.current = false;
    }
  };

  const executeRecurringEvent = async (
    fields: TemporalCreateSession['draft']['current'],
  ): Promise<boolean> => {
    const validation = validateTemporalCreateU2QuickFields(fields);
    if (validation.length > 0) {
      setIssues(validation);
      return false;
    }
    try {
      buildTemporalCreateObjectiveTemplates(u2DraftRef.current);
    } catch (reason) {
      setFailureTarget('objectives');
      setFailureMessage(
        reason instanceof Error ? reason.message : 'Obiettivi non validi.',
      );
      setLifecycle('failed');
      return false;
    }
    if (!temporalCreateRecurringEventSharedIntentSupported(fields)) {
      setLifecycle('failed');
      setFailureMessage(
        i18n.language.toLowerCase().startsWith('en')
          ? 'These legacy Event-specific options are no longer part of recurring Event Create. Recurrence, Life Area, color, location, description, run of show, participants and Reminder are supported.'
          : 'Queste vecchie opzioni specifiche dell’Evento non fanno più parte del Create ricorrente. Ricorrenza, Life Area, colore, località, descrizione, Scaletta, partecipanti e promemoria sono supportati.',
      );
      return false;
    }

    commitInFlightRef.current = true;
    setLifecycle('pending');
    setIssues([]);
    setFailureMessage('');
    try {
      const lifeArea = buildTemporalCreateLifeAreaInput(u2DraftRef.current);
      const policy = buildTemporalCreateRecurringEventPolicy(fields);
      const description = fields.notes.trim();
      const location = fields.event.location.trim();
      const created = await recurringAuthoringDataSource.createEvent({
        operationId: systemTemporalIdFactory.operationId(),
        title: fields.title.trim(),
        ...(lifeArea ? { lifeArea } : {}),
        ...(description ? { description } : {}),
        ...(location ? { location } : {}),
        ...(u2DraftRef.current.lifeArea.kind === 'none' &&
        u2DraftRef.current.itemColorCode
          ? { itemColorCode: u2DraftRef.current.itemColorCode }
          : {}),
        agendaParts: Object.freeze(
          fields.event.agendaParts
            .map((part) => part.trim())
            .filter((part) => part.length > 0),
        ),
        recurrence: buildTemporalCreateEventRecurrence(fields),
        placementKind: policy.placementKind,
        durationMinutes: policy.durationMinutes,
        durationDays: policy.durationDays,
        reminderLeadMinutes: fields.confirmation.reminderLeadMinutes,
        realityMode: u2DraftRef.current.realityMode,
        objectives: buildTemporalCreateObjectiveTemplates(u2DraftRef.current),
      });
      const participantCommands = Object.freeze(
        u2DraftRef.current.eventParticipants.map((participant) =>
          Object.freeze({
            participant,
            operationId: systemTemporalIdFactory.operationId(),
          }),
        ),
      );
      const finalizeParticipants = async () => {
        for (const command of participantCommands) {
          await responsibilityDataSource.setExpectedParticipation(
            created.sourceRef,
            {
              operationId: command.operationId,
              ...(command.participant.personRef === 'self'
                ? {}
                : { participant: command.participant.personRef }),
              requirementCode: command.participant.requirementCode,
              expectedRequirementCode: null,
            },
          );
        }
      };
      try {
        await finalizeParticipants();
      } catch {
        partialPostCreateRef.current = finalizeParticipants;
        setPostCreateRetry(true);
        setLifecycle('failed');
        setFailureMessage(
          i18n.language.toLowerCase().startsWith('en')
            ? 'The Event was created, but its expected participants were not fully saved. Retry safely without creating the Event again.'
            : 'L’Evento è stato creato, ma i partecipanti attesi non sono stati salvati completamente. Riprova in sicurezza senza creare di nuovo l’Evento.',
        );
        return false;
      }
      invalidateTemporalTimelineRead();
      setSession(discardTemporalCreateSession(freshFields(defaultDate)));
      closeComposer();
      return true;
    } catch (reason) {
      setLifecycle('failed');
      setFailureMessage(
        reason instanceof Error
          ? reason.message
          : t(($) => $.common.home.timeline.create.failure),
      );
      return false;
    } finally {
      commitInFlightRef.current = false;
    }
  };

  const submit = async (
    fieldsOverride?: Partial<TemporalCreateSession['draft']['current']>,
  ) => {
    if (commitInFlightRef.current) return;
    if (partialPostCreateRef.current !== null) {
      commitInFlightRef.current = true;
      setLifecycle('pending');
      try {
        await partialPostCreateRef.current();
        partialPostCreateRef.current = null;
        setPostCreateRetry(false);
        setSession(discardTemporalCreateSession(freshFields(defaultDate)));
        closeComposer();
      } catch {
        setLifecycle('failed');
        setFailureMessage(
          i18n.language.toLowerCase().startsWith('en')
            ? 'The follow-up configuration still could not be saved. Retry the configuration; the item will not be created again.'
            : 'La configurazione successiva non è ancora stata salvata. Riprova: l’elemento non verrà creato di nuovo.',
        );
      } finally {
        commitInFlightRef.current = false;
      }
      return;
    }

    const fields = fieldsOverride
      ? { ...session.draft.current, ...fieldsOverride }
      : session.draft.current;
    setFailureTarget(null);
    if (
      fields.kind === 'activity' &&
      fields.eventRecurrence.patternKind !== 'none'
    ) {
      await executeRecurringActivity(fields);
      return;
    }
    if (
      fields.kind === 'event' &&
      fields.eventRecurrence.patternKind !== 'none'
    ) {
      await executeRecurringEvent(fields);
      return;
    }

    const useU2Quick =
      (authoringDataSourceOverride !== undefined ||
        import.meta.env.MODE !== 'test') &&
      temporalCreateU2QuickIntentSupported(fields);
    if (!useU2Quick && temporalCreateHasU6Structure(u2DraftRef.current)) {
      const structure = u2DraftRef.current.activityStructure;
      setFailureTarget(
        structure.activityIntervals.length > 0
          ? 'activityIntervals'
          : structure.plannedSlices.length > 0
            ? 'plannedSessions'
            : 'activityStructure',
      );
      setLifecycle('failed');
      setFailureMessage(
        i18n.language.toLowerCase().startsWith('en')
          ? 'These advanced settings cannot yet be combined with Activity intervals or planned Sessions.'
          : 'Queste impostazioni avanzate non possono ancora essere combinate con intervalli dell’attività o Sessioni pianificate.',
      );
      return;
    }
    if (useU2Quick) {
      await executeU2Quick(fields);
      return;
    }

    const preparation =
      preparedRef.current && !fieldsOverride
        ? ({ status: 'ready', prepared: preparedRef.current } as const)
        : runtime.prepare(fields);
    if (preparation.status === 'invalid') {
      setIssues(preparation.issues);
      const hasAdvancedIssue = preparation.issues.some(
        (issue) => issue.path[0]?.includes('.') ?? false,
      );
      if (session.surface === 'quick' && hasAdvancedIssue) {
        changeSurface('expanded');
      }
      return;
    }

    preparedRef.current = preparation.prepared;
    commitInFlightRef.current = true;
    setLifecycle('pending');
    setIssues([]);
    setFailureMessage('');
    try {
      const execution = await runtime.execute(preparation.prepared);
      if (execution.result.status === 'applied' && execution.effect) {
        if (
          preparation.prepared.metadata.recurrenceOwner === null &&
          preparation.prepared.command.payload.placement !== null &&
          execution.effect.projection.placement === null
        ) {
          preparedRef.current = null;
          setSession(discardTemporalCreateSession(freshFields(defaultDate)));
          setLifecycle('failed');
          setFailureMessage(
            i18n.language.toLowerCase().startsWith('en')
              ? 'Activity created, but its Schedule was not confirmed. Check Timeline and To place.'
              : 'Attività creata, ma lo Schedule non è confermato. Controlla Timeline e Da collocare.',
          );
          return;
        }
        const focusHandled = execution.effect.undoAvailable
          ? onApplied(execution.effect)
          : false;
        if (execution.reminderRetry) {
          partialPostCreateRef.current = execution.reminderRetry;
          setPostCreateRetry(true);
          setLifecycle('failed');
          setFailureMessage(
            t(($) => $.common.home.timeline.create.reminderPartial),
          );
          return;
        }
        setSession(discardTemporalCreateSession(freshFields(defaultDate)));
        closeComposer(!focusHandled);
        return;
      }
      if (execution.result.status === 'rejected') {
        setIssues(execution.result.issues);
        setLifecycle('idle');
      } else {
        setLifecycle('failed');
        setFailureMessage(
          (execution.result.status === 'failed'
            ? execution.result.failure.message
            : null) ?? t(($) => $.common.home.timeline.create.failure),
        );
      }
    } catch (reason) {
      setLifecycle('failed');
      setFailureMessage(
        reason instanceof Error
          ? reason.message
          : t(($) => $.common.home.timeline.create.failure),
      );
    } finally {
      commitInFlightRef.current = false;
    }
  };

  const discardPending = open && session.closeDecision === 'confirm-discard';
  const composerSession = discardPending
    ? continueTemporalCreateEditing(session)
    : session;
  const advancedComposer = composerSession.surface !== 'quick';
  const composer = open ? (
    <TemporalCreateComposer
      session={composerSession}
      contexts={contexts}
      issues={issues}
      lifecycle={lifecycle}
      failureMessage={failureMessage}
      failureTarget={failureTarget}
      postCreateRetry={postCreateRetry}
      u2Draft={u2Draft}
      onPatch={patch}
      onSurfaceChange={changeSurface}
      onRequestClose={requestClose}
      onContinueEditing={continueEditing}
      onDiscard={() => closeComposer()}
      onMoveToUnplaced={() => void submit({ timeSemantics: 'unscheduled' })}
      onSubmit={() => void submit()}
      onU2DraftChange={(draft) => {
        u2DraftRef.current = draft;
        setU2Draft(draft);
        queueMicrotask(() => {
          setFailureMessage('');
          setFailureTarget(null);
        });
      }}
    />
  ) : null;
  const createHost =
    typeof document === 'undefined'
      ? null
      : document.querySelector<HTMLElement>('[data-home-context-create-host]');
  const discardModal =
    discardPending && typeof document !== 'undefined'
      ? createPortal(
          <div
            className="temporal-create-discard-viewport"
            data-temporal-create="discard-modal"
          >
            <div
              className="temporal-create-discard"
              role="alertdialog"
              aria-modal="true"
              aria-label={t(($) => $.common.home.timeline.create.discardTitle)}
            >
              <div>
                <strong>
                  {t(($) => $.common.home.timeline.create.discardTitle)}
                </strong>
                <p>{t(($) => $.common.home.timeline.create.discardBody)}</p>
              </div>
              <div className="temporal-create-discard__actions">
                <button type="button" autoFocus onClick={continueEditing}>
                  Annulla
                </button>
                <button
                  type="button"
                  disabled={
                    lifecycle === 'pending' ||
                    session.draft.current.title.trim().length === 0
                  }
                  onClick={() => void submit({ timeSemantics: 'unscheduled' })}
                >
                  Sposta in Da collocare
                </button>
                <button
                  className="temporal-create-discard__destructive"
                  type="button"
                  onClick={() => closeComposer()}
                >
                  {t(($) => $.common.home.timeline.create.discard)}
                </button>
              </div>
            </div>
          </div>,
          document.body,
        )
      : null;

  return (
    <>
      <button
        ref={triggerRef}
        className="dante-timeline-quick-add"
        type="button"
        onClick={() =>
          openComposer(
            defaultDate,
            undefined,
            undefined,
            undefined,
            undefined,
            undefined,
            triggerRef.current,
          )
        }
        aria-label={t(($) => $.common.home.timeline.quickAdd)}
        aria-haspopup="dialog"
        aria-expanded={open}
        data-create-ready={creationEnabled ? 'true' : 'false'}
        title={t(($) => $.common.home.timeline.quickAdd)}
      >
        +
      </button>
      {composer && typeof document !== 'undefined'
        ? createPortal(
            composer,
            advancedComposer ? document.body : (createHost ?? document.body),
          )
        : null}
      {discardModal}
    </>
  );
}
