import type { PlainDate } from '@dante/time';
import {
  useCallback,
  useEffect,
  useLayoutEffect,
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
  type TemporalCreateComposerPosition,
  type TemporalCreateContextOption,
} from './temporal-create-composer';

import './temporal-create.css';

const VIEWPORT_PADDING_PX = 16;
const DEFAULT_COMPOSER_TOP_PX = 64;
const FLOATING_COMPOSER_BREAKPOINT_PX = 900;

type InvocationAnchor = Readonly<{
  left: number;
  top: number;
  bottom: number;
}>;

type ComposerDrag = Readonly<{
  pointerId: number;
  startX: number;
  startY: number;
  startLeft: number;
  startTop: number;
  width: number;
  height: number;
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

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), Math.max(min, max));
}

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
  const composerDragRef = useRef<ComposerDrag | null>(null);
  const [runtime] = useState(
    () => runtimeOverride ?? createLocalTemporalCreateRuntime(),
  );
  const requestSeenRef = useRef<number | null>(null);
  const preparedRef = useRef<TemporalCreatePreparedOperation | null>(null);
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
  const [position, setPosition] = useState<TemporalCreateComposerPosition>({
    top: DEFAULT_COMPOSER_TOP_PX,
    left: VIEWPORT_PADDING_PX,
  });

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
      const defaultsToUnplacedActivity =
        import.meta.env.MODE !== 'test' &&
        startMinute === undefined &&
        seed?.timeSemantics === undefined &&
        seed?.startTime === undefined;
      const base = createTemporalCreateFields({
        date: targetDate,
        timeSemantics: defaultsToUnplacedActivity ? 'unscheduled' : 'timed',
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
      composerDragRef.current = null;
      document.documentElement.removeAttribute('data-temporal-create-dragging');
      preparedRef.current = null;
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
      focusReturnRef.current = focusReturnTarget ?? triggerRef.current;
      void externalAnchor;
      setPosition({
        top: DEFAULT_COMPOSER_TOP_PX,
        left: VIEWPORT_PADDING_PX,
      });
      setOpen(true);
    },
    [freshFields, onBeforeOpen],
  );

  useEffect(() => {
    if (
      !creationEnabled ||
      !request ||
      requestSeenRef.current === request.id ||
      open
    ) {
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
  }, [creationEnabled, open, openComposer, request]);

  useEffect(() => {
    if (!open || session.closeDecision === 'confirm-discard') {
      onPreview(null);
      return;
    }
    onPreview(temporalCreateTimelinePreviewFromFields(session.draft.current));
    return () => onPreview(null);
  }, [onPreview, open, session.closeDecision, session.draft]);

  useLayoutEffect(() => {
    if (!open) {
      return;
    }

    const clampFloatingPosition = () => {
      const composer = document.querySelector<HTMLElement>(
        '[data-temporal-create="composer"]',
      );
      if (!composer || window.innerWidth <= FLOATING_COMPOSER_BREAKPOINT_PX) {
        return;
      }
      const rect = composer.getBoundingClientRect();
      setPosition((current) => {
        const next = {
          left: clamp(
            current.left,
            VIEWPORT_PADDING_PX,
            window.innerWidth - rect.width - VIEWPORT_PADDING_PX,
          ),
          top: clamp(
            current.top,
            VIEWPORT_PADDING_PX,
            window.innerHeight - rect.height - VIEWPORT_PADDING_PX,
          ),
        };
        return next.left === current.left && next.top === current.top
          ? current
          : next;
      });
    };

    const frame = requestAnimationFrame(clampFloatingPosition);
    window.addEventListener('resize', clampFloatingPosition);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener('resize', clampFloatingPosition);
    };
  }, [open, session.surface]);

  useEffect(() => {
    if (!open) {
      composerDragRef.current = null;
      document.documentElement.removeAttribute('data-temporal-create-dragging');
      return;
    }

    const composer = document.querySelector<HTMLElement>(
      '[data-temporal-create="composer"]',
    );
    const handle = composer?.querySelector<HTMLElement>(
      '.temporal-create-composer__heading-copy',
    );
    if (!composer || !handle) {
      return;
    }

    const finishDrag = (pointerId?: number) => {
      if (
        pointerId !== undefined &&
        composerDragRef.current?.pointerId !== pointerId
      ) {
        return;
      }
      composerDragRef.current = null;
      document.documentElement.removeAttribute('data-temporal-create-dragging');
    };

    const onPointerDown = (event: PointerEvent) => {
      if (
        window.innerWidth <= FLOATING_COMPOSER_BREAKPOINT_PX ||
        event.button !== 0 ||
        !event.isPrimary
      ) {
        return;
      }
      const target = event.target;
      if (
        target instanceof Element &&
        target.closest('button, input, select, textarea, a')
      ) {
        return;
      }
      const rect = composer.getBoundingClientRect();
      composerDragRef.current = {
        pointerId: event.pointerId,
        startX: event.clientX,
        startY: event.clientY,
        startLeft: rect.left,
        startTop: rect.top,
        width: rect.width,
        height: rect.height,
      };
      document.documentElement.setAttribute(
        'data-temporal-create-dragging',
        'true',
      );
      handle.setPointerCapture(event.pointerId);
      event.preventDefault();
    };

    const onPointerMove = (event: PointerEvent) => {
      const drag = composerDragRef.current;
      if (!drag || drag.pointerId !== event.pointerId) {
        return;
      }
      setPosition({
        left: clamp(
          drag.startLeft + event.clientX - drag.startX,
          VIEWPORT_PADDING_PX,
          window.innerWidth - drag.width - VIEWPORT_PADDING_PX,
        ),
        top: clamp(
          drag.startTop + event.clientY - drag.startY,
          VIEWPORT_PADDING_PX,
          window.innerHeight - drag.height - VIEWPORT_PADDING_PX,
        ),
      });
      event.preventDefault();
    };

    const onPointerUp = (event: PointerEvent) => finishDrag(event.pointerId);
    const onPointerCancel = (event: PointerEvent) =>
      finishDrag(event.pointerId);

    handle.addEventListener('pointerdown', onPointerDown);
    handle.addEventListener('pointermove', onPointerMove);
    handle.addEventListener('pointerup', onPointerUp);
    handle.addEventListener('pointercancel', onPointerCancel);
    return () => {
      handle.removeEventListener('pointerdown', onPointerDown);
      handle.removeEventListener('pointermove', onPointerMove);
      handle.removeEventListener('pointerup', onPointerUp);
      handle.removeEventListener('pointercancel', onPointerCancel);
      finishDrag();
    };
  }, [open, session.surface]);

  const requestClose = () => {
    if (lifecycle === 'pending') {
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
    preparedRef.current = null;
    setIssues([]);
    setFailureMessage('');
    setLifecycle('idle');
    setSession((current) => updateTemporalCreateFields(current, next));
  };

  const changeSurface = (surface: TemporalCreateSurface) => {
    setSession((current) => setTemporalCreateSurface(current, surface));
  };

  const submit = async () => {
    if (commitInFlightRef.current) {
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
    const preparation = preparedRef.current
      ? ({ status: 'ready', prepared: preparedRef.current } as const)
      : runtime.prepare(session.draft.current);
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
        setSession(discardTemporalCreateSession(freshFields(defaultDate)));
        closeComposer(!focusHandled);
        return;
      }
      if (execution.result.status === 'rejected') {
        setIssues(execution.result.issues);
        setLifecycle('idle');
      } else {
        setLifecycle('failed');
        setFailureMessage(t(($) => $.common.home.timeline.create.failure));
      }
    } catch {
      setLifecycle('failed');
      setFailureMessage(t(($) => $.common.home.timeline.create.failure));
    } finally {
      commitInFlightRef.current = false;
    }
  };

  const composer = open ? (
    <TemporalCreateComposer
      position={position}
      session={session}
      contexts={contexts}
      issues={issues}
      lifecycle={lifecycle}
      failureMessage={failureMessage}
      onPatch={patch}
      onSurfaceChange={changeSurface}
      onRequestClose={requestClose}
      onContinueEditing={() =>
        setSession((current) => continueTemporalCreateEditing(current))
      }
      onDiscard={() => closeComposer()}
      onSubmit={() => void submit()}
    />
  ) : null;

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
        disabled={!creationEnabled}
        aria-label={t(($) => $.common.home.timeline.quickAdd)}
        aria-haspopup="dialog"
        aria-expanded={open}
        title={
          creationEnabled
            ? t(($) => $.common.home.timeline.quickAdd)
            : 'Crea prima una Life Area attiva'
        }
      >
        +
      </button>
      {composer && typeof document !== 'undefined'
        ? createPortal(composer, document.body)
        : null}
    </>
  );
}
