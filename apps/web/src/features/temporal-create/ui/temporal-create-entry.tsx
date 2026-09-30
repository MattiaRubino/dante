import type { PlainDate } from '@dante/time';
import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import type { TemporalValidationIssue } from '../../temporal';
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
  TemporalCreateComposer,
  type TemporalCreateContextOption,
} from './temporal-create-composer';

import './temporal-create.css';

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
  anchor?: InvocationAnchor;
}>;

export type TemporalCreateEntryProps = Readonly<{
  defaultDate: PlainDate;
  contexts: readonly TemporalCreateContextOption[];
  request?: TemporalCreateInvocation | null;
  runtime?: TemporalCreateRuntime;
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
  const requestSeenRef = useRef<number | null>(null);
  const preparedRef = useRef<TemporalCreatePreparedOperation | null>(null);
  const partialReminderRef = useRef<(() => Promise<void>) | null>(null);
  const [reminderRetry, setReminderRetry] = useState(false);
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
        timeZoneId: seed?.timeZoneId ?? zone,
        contextId: seed?.contextId ?? contexts[0]?.id ?? '',
      });
      return seed ? applyTemporalCreateFieldSeed(base, seed) : base;
    },
    [contexts, runtime],
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
      partialReminderRef.current = null;
      setReminderRetry(false);
      commitInFlightRef.current = false;
      onPreview(null);
      if (restoreFocus) {
        restoreComposerFocus();
      }
    },
    [onPreview, restoreComposerFocus],
  );

  const openComposer = useCallback(
    (
      date: PlainDate,
      startMinute?: number,
      durationMinutes?: number,
      seed?: TemporalCreateFieldSeed,
      externalAnchor?: InvocationAnchor,
      focusReturnTarget?: HTMLElement | null,
    ) => {
      onBeforeOpen?.();
      const fields = freshFields(date, startMinute, durationMinutes, seed);
      setSession(createTemporalCreateSession(fields));
      setIssues([]);
      setFailureMessage('');
      setLifecycle('idle');
      preparedRef.current = null;
      partialReminderRef.current = null;
      setReminderRetry(false);
      focusReturnRef.current = focusReturnTarget ?? triggerRef.current;
      // The fixed Create panel uses an invocation's time/date as content seed,
      // never as a second positional model. The Timeline remains its own surface.
      void externalAnchor;
      setOpen(true);
    },
    [freshFields, onBeforeOpen],
  );

  useEffect(() => {
    if (!request || requestSeenRef.current === request.id || open) {
      return;
    }
    requestSeenRef.current = request.id;
    const frame = requestAnimationFrame(() => {
      openComposer(
        request.date,
        request.startMinute,
        request.durationMinutes,
        request.seed,
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
    if (lifecycle === 'pending') {
      return;
    }
    // U1 product contract: time/date/type edits are provisional positioning only.
    // Until the user gives the draft a title, outside/Escape/close dismisses it
    // immediately instead of asking to preserve or discard an unnamed draft.
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
    if (partialReminderRef.current !== null) return;
    const merged = { ...session.draft.current, ...next };
    const eligibleReminder = merged.kind === 'activity' &&
      merged.timeSemantics === 'timed' && merged.timeMode === 'zoned' &&
      merged.eventRecurrence.patternKind === 'none';
    const boundedNext = eligibleReminder ? next : {
      ...next,
      confirmation: { ...merged.confirmation, reminderLeadMinutes: null },
    };
    preparedRef.current = null;
    setIssues([]);
    setFailureMessage('');
    setLifecycle('idle');
    setSession((current) => updateTemporalCreateFields(current, boundedNext));
  };

  const changeSurface = (surface: TemporalCreateSurface) => {
    setSession((current) => setTemporalCreateSurface(current, surface));
  };

  const continueEditing = () => {
    setSession((current) => continueTemporalCreateEditing(current));
  };

  const submit = async (
    fieldsOverride?: Partial<TemporalCreateSession['draft']['current']>,
  ) => {
    if (commitInFlightRef.current) {
      return;
    }
    if (partialReminderRef.current !== null) {
      commitInFlightRef.current = true;
      setLifecycle('pending');
      try {
        await partialReminderRef.current();
        setSession(discardTemporalCreateSession(freshFields(defaultDate)));
        closeComposer();
      } catch {
        setLifecycle('failed');
        setFailureMessage(t(($) => $.common.home.timeline.create.reminderPartial));
      } finally {
        commitInFlightRef.current = false;
      }
      return;
    }
    if (
      import.meta.env.MODE !== 'test' &&
      !contexts.some(
        (context) =>
          context.id === session.draft.current.contextId &&
          /^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(
            context.id,
          ),
      )
    ) {
      setLifecycle('failed');
      setFailureMessage('Seleziona una Life Area attiva prima di creare.');
      return;
    }
    const fields = fieldsOverride
      ? { ...session.draft.current, ...fieldsOverride }
      : session.draft.current;
    const preparation = preparedRef.current && !fieldsOverride
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
          partialReminderRef.current = execution.reminderRetry;
          setReminderRetry(true);
          setLifecycle('failed');
          setFailureMessage(t(($) => $.common.home.timeline.create.reminderPartial));
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
            : null) ??
            t(($) => $.common.home.timeline.create.failure),
        );
      }
    } catch {
      setLifecycle('failed');
      setFailureMessage(t(($) => $.common.home.timeline.create.failure));
    } finally {
      commitInFlightRef.current = false;
    }
  };

  const discardPending = open && session.closeDecision === 'confirm-discard';
  // The discard confirmation has a single owner: the viewport portal below.
  // Keep the rail composer mounted for context, but present it without its legacy
  // inline confirmation so we never expose two alertdialogs for the same decision.
  const composerSession = discardPending
    ? continueTemporalCreateEditing(session)
    : session;
  const composer = open ? (
    <TemporalCreateComposer
      session={composerSession}
      contexts={contexts}
      issues={issues}
      lifecycle={lifecycle}
      failureMessage={failureMessage}
      reminderRetry={reminderRetry}
      onPatch={patch}
      onSurfaceChange={changeSurface}
      onRequestClose={requestClose}
      onContinueEditing={continueEditing}
      onDiscard={() => closeComposer()}
      onMoveToUnplaced={() =>
        void submit({ timeSemantics: 'unscheduled' })
      }
      onSubmit={() => void submit()}
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
                {session.draft.current.kind === 'activity' ? (
                  <button
                    type="button"
                    disabled={
                      lifecycle === 'pending' ||
                      session.draft.current.title.trim().length === 0
                    }
                    onClick={() =>
                      void submit({ timeSemantics: 'unscheduled' })
                    }
                  >
                    Sposta in Da collocare
                  </button>
                ) : null}
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
            triggerRef.current,
          )
        }
        aria-label={t(($) => $.common.home.timeline.quickAdd)}
        aria-haspopup="dialog"
        aria-expanded={open}
        data-create-ready={creationEnabled ? 'true' : 'false'}
        title={
          creationEnabled
            ? t(($) => $.common.home.timeline.quickAdd)
            : `${t(($) => $.common.home.timeline.quickAdd)} · seleziona una Life Area attiva per salvare`
        }
      >
        +
      </button>
      {composer && typeof document !== 'undefined'
        ? createPortal(composer, createHost ?? document.body)
        : null}
      {discardModal}
    </>
  );
}
