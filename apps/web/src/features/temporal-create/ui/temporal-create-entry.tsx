import {
  useCallback,
  useLayoutEffect,
  useRef,
  useState,
} from 'react';
import { useTranslation } from 'react-i18next';

import {
  continueTemporalCreateEditing,
  createTemporalCreateSession,
  discardTemporalCreateSession,
  requestTemporalCreateClose,
  updateTemporalCreateTitle,
} from '../model/temporal-create-session';
import {
  TemporalCreateComposer,
  type TemporalCreateComposerPosition,
} from './temporal-create-composer';

import './temporal-create.css';

const VIEWPORT_PADDING_PX = 16;
const COMPOSER_GAP_PX = 10;
const COMPOSER_MAX_WIDTH_PX = 420;
const COMPOSER_BASE_HEIGHT_PX = 190;
const COMPOSER_DISCARD_HEIGHT_PX = 286;

function clamp(value: number, min: number, max: number): number {
  return Math.min(Math.max(value, min), Math.max(min, max));
}

export function TemporalCreateEntry() {
  const { t } = useTranslation('common');
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const [open, setOpen] = useState(false);
  const [session, setSession] = useState(createTemporalCreateSession);
  const [position, setPosition] = useState<TemporalCreateComposerPosition>({
    top: 72,
    left: VIEWPORT_PADDING_PX,
  });

  const restoreTriggerFocus = useCallback(() => {
    requestAnimationFrame(() => triggerRef.current?.focus());
  }, []);

  const closeComposer = useCallback(() => {
    setOpen(false);
    setSession(discardTemporalCreateSession());
    restoreTriggerFocus();
  }, [restoreTriggerFocus]);

  const openComposer = () => {
    setSession(createTemporalCreateSession());
    setOpen(true);
  };

  const requestClose = () => {
    const request = requestTemporalCreateClose(session);
    if (request.shouldClose) {
      closeComposer();
      return;
    }
    setSession(request.session);
  };

  useLayoutEffect(() => {
    if (!open) {
      return;
    }

    const updatePosition = () => {
      const trigger = triggerRef.current;
      if (!trigger) {
        return;
      }

      const rect = trigger.getBoundingClientRect();
      const width = Math.min(
        COMPOSER_MAX_WIDTH_PX,
        Math.max(0, window.innerWidth - VIEWPORT_PADDING_PX * 2),
      );
      const estimatedHeight =
        session.closeDecision === 'confirm-discard'
          ? COMPOSER_DISCARD_HEIGHT_PX
          : COMPOSER_BASE_HEIGHT_PX;

      const left = clamp(
        rect.left,
        VIEWPORT_PADDING_PX,
        window.innerWidth - width - VIEWPORT_PADDING_PX,
      );
      const below = rect.bottom + COMPOSER_GAP_PX;
      const above = rect.top - COMPOSER_GAP_PX - estimatedHeight;
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
    window.addEventListener('scroll', updatePosition, true);

    return () => {
      window.removeEventListener('resize', updatePosition);
      window.removeEventListener('scroll', updatePosition, true);
    };
  }, [open, session.closeDecision]);

  return (
    <>
      <button
        ref={triggerRef}
        className="dante-timeline-quick-add"
        type="button"
        onClick={openComposer}
        aria-label={t(($) => $.common.home.timeline.quickAdd)}
        aria-haspopup="dialog"
        aria-expanded={open}
        title={t(($) => $.common.home.timeline.quickAdd)}
      >
        +
      </button>

      {open ? (
        <TemporalCreateComposer
          position={position}
          session={session}
          onTitleChange={(title) =>
            setSession((current) => updateTemporalCreateTitle(current, title))
          }
          onRequestClose={requestClose}
          onContinueEditing={() =>
            setSession((current) => continueTemporalCreateEditing(current))
          }
          onDiscard={closeComposer}
        />
      ) : null}
    </>
  );
}
