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
} from '../application/temporal-create-runtime';
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
const COMPOSER_GAP_PX = 10;
const QUICK_WIDTH_PX = 560;
const EXPANDED_WIDTH_PX = 760;
const QUICK_ESTIMATED_HEIGHT_PX = 650;
const EXPANDED_ESTIMATED_HEIGHT_PX = 760;

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
  anchor?: InvocationAnchor;
}>;

export type TemporalCreateEntryProps = Readonly<{
  defaultDate: PlainDate;
  contexts: readonly TemporalCreateContextOption[];
  request?: TemporalCreateInvocation | null;
  onPreview: (projection: TemporalCreateTimelineProjection | null) => void;
  onApplied: (effect: TemporalCreateAppliedEffect) => boolean;
  onBeforeOpen?: (() => void) | undefined;
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
  onPreview,
  onApplied,
  onBeforeOpen,
}: TemporalCreateEntryProps) {
  const { t } = useTranslation('common');
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const runtimeRef = useRef(createLocalTemporalCreateRuntime());
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
  const [anchor, setAnchor] = useState<InvocationAnchor | null>(null);
  const [position, setPosition] = useState<TemporalCreateComposerPosition>({
    top: 72,
    left: VIEWPORT_PADDING_PX,
  });

  const freshFields = useCallback(
    (date: PlainDate, startMinute?: number, durationMinutes?: number) => {
      const runtime = runtimeRef.current;
      const zone = runtime.clock.timeZoneId();
      let minute = startMinute;
      if (minute === undefined) {
        if (date.equals(runtime.clock.today(zone))) {
          const now = runtime.clock.now().toZonedDateTimeISO(zone);
          minute = Math.ceil((now.hour * 60 + now.minute) / 15) * 15;
        } else {
          minute = 9 * 60;
        }
      }
      return createTemporalCreateFields({
        date: date.toString(),
        startTime: minuteToInput(minute),
        durationMinutes: durationMinutes ?? 30,
        timeZoneId: zone,
        contextId:
          contexts.find((context) => context.id === 'personale')?.id ??
          contexts[0]?.id ??
          'personale',
      });
    },
    [contexts],
  );

  const restoreTriggerFocus = useCallback(() => {
    requestAnimationFrame(() => triggerRef.current?.focus());
  }, []);

  const closeComposer = useCallback(
    (restoreFocus = true) => {
      setOpen(false);
      setIssues([]);
      setFailureMessage('');
      setLifecycle('idle');
      setAnchor(null);
      preparedRef.current = null;
      commitInFlightRef.current = false;
      onPreview(null);
      if (restoreFocus) {
        restoreTriggerFocus();
      }
    },
    [onPreview, restoreTriggerFocus],
  );

  const openComposer = useCallback(
    (
      date: PlainDate,
      startMinute?: number,
      durationMinutes?: number,
      externalAnchor?: InvocationAnchor,
    ) => {
      onBeforeOpen?.();
      const fields = freshFields(date, startMinute, durationMinutes);
      setSession(createTemporalCreateSession(fields));
      setIssues([]);
      setFailureMessage('');
      setLifecycle('idle');
      preparedRef.current = null;
      const triggerRect = triggerRef.current?.getBoundingClientRect();
      setAnchor(
        externalAnchor ??
          (triggerRect
            ? {
                left: triggerRect.left,
                top: triggerRect.top,
                bottom: triggerRect.bottom,
              }
            : null),
      );
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
        request.anchor,
      );
    });
    return () => cancelAnimationFrame(frame);
  }, [open, openComposer, request]);

  useEffect(() => {
    if (!open) {
      return;
    }
    const previous = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = previous;
    };
  }, [open]);

  useEffect(() => {
    if (!open || session.closeDecision === 'confirm-discard') {
      onPreview(null);
      return;
    }
    onPreview(
      temporalCreateTimelinePreviewFromFields(session.draft.current),
    );
    return () => onPreview(null);
  }, [onPreview, open, session.closeDecision, session.draft]);

  useLayoutEffect(() => {
    if (!open || !anchor || session.surface === 'full') {
      return;
    }
    const updatePosition = () => {
      const desiredWidth =
        session.surface === 'expanded' ? EXPANDED_WIDTH_PX : QUICK_WIDTH_PX;
      const width = Math.min(
        desiredWidth,
        Math.max(0, window.innerWidth - VIEWPORT_PADDING_PX * 2),
      );
      const left = clamp(
        anchor.left,
        VIEWPORT_PADDING_PX,
        window.innerWidth - width - VIEWPORT_PADDING_PX,
      );
      const below = anchor.bottom + COMPOSER_GAP_PX;
      const estimatedHeight = Math.min(
        session.surface === 'expanded'
          ? EXPANDED_ESTIMATED_HEIGHT_PX
          : QUICK_ESTIMATED_HEIGHT_PX,
        window.innerHeight - VIEWPORT_PADDING_PX * 2,
      );
      const above = anchor.top - COMPOSER_GAP_PX - estimatedHeight;
      const top =
        below + estimatedHeight <= window.innerHeight - VIEWPORT_PADDING_PX
          ? below
          : clamp(
              above,
              VIEWPORT_PADDING_PX,
              window.innerHeight - estimatedHeight - VIEWPORT_PADDING_PX,
            );
      setPosition({ top, left });
    };
    updatePosition();
    window.addEventListener('resize', updatePosition);
    return () => window.removeEventListener('resize', updatePosition);
  }, [anchor, open, session.surface]);

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

  const patch = (
    next: Partial<TemporalCreateSession['draft']['current']>,
  ) => {
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
    const runtime = runtimeRef.current;
    const preparation = preparedRef.current
      ? ({ status: 'ready', prepared: preparedRef.current } as const)
      : runtime.prepare(session.draft.current);
    if (preparation.status === 'invalid') {
      setIssues(preparation.issues);
      if (session.surface === 'quick' && preparation.issues.some((issue) => issue.path[0].includes('.'))) {
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
        const focusHandled = onApplied(execution.effect);
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
        onClick={() => openComposer(defaultDate)}
        aria-label={t(($) => $.common.home.timeline.quickAdd)}
        aria-haspopup="dialog"
        aria-expanded={open}
        title={t(($) => $.common.home.timeline.quickAdd)}
      >
        +
      </button>
      {composer && typeof document !== 'undefined'
        ? createPortal(composer, document.body)
        : null}
    </>
  );
}
