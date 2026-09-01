import {
  useId,
  useLayoutEffect,
  useRef,
  type CSSProperties,
  type KeyboardEvent,
  type PointerEvent,
} from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalCreateSession } from '../model/temporal-create-session';

export type TemporalCreateComposerPosition = Readonly<{
  top: number;
  left: number;
}>;

type TemporalCreateComposerProps = Readonly<{
  position: TemporalCreateComposerPosition;
  session: TemporalCreateSession;
  onTitleChange: (title: string) => void;
  onRequestClose: () => void;
  onContinueEditing: () => void;
  onDiscard: () => void;
}>;

function focusableElements(root: HTMLElement): HTMLElement[] {
  return Array.from(
    root.querySelectorAll<HTMLElement>(
      'button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])',
    ),
  ).filter((element) => !element.hasAttribute('hidden'));
}

export function TemporalCreateComposer({
  position,
  session,
  onTitleChange,
  onRequestClose,
  onContinueEditing,
  onDiscard,
}: TemporalCreateComposerProps) {
  const { t } = useTranslation('common');
  const titleId = useId();
  const dialogTitleId = useId();
  const discardDescriptionId = useId();
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const titleRef = useRef<HTMLInputElement | null>(null);
  const continueRef = useRef<HTMLButtonElement | null>(null);

  useLayoutEffect(() => {
    titleRef.current?.focus();
  }, []);

  useLayoutEffect(() => {
    if (session.closeDecision === 'confirm-discard') {
      continueRef.current?.focus();
    }
  }, [session.closeDecision]);

  const continueEditing = () => {
    onContinueEditing();
    requestAnimationFrame(() => titleRef.current?.focus());
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      if (session.closeDecision === 'confirm-discard') {
        continueEditing();
      } else {
        onRequestClose();
      }
      return;
    }

    if (event.key !== 'Tab') {
      return;
    }

    const root = dialogRef.current;
    if (!root) {
      return;
    }

    const focusables = focusableElements(root);
    if (focusables.length === 0) {
      event.preventDefault();
      return;
    }

    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    const active = document.activeElement;

    if (event.shiftKey && active === first) {
      event.preventDefault();
      last?.focus();
    } else if (!event.shiftKey && active === last) {
      event.preventDefault();
      first?.focus();
    }
  };

  const handleBackdropPointerDown = (event: PointerEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget) {
      event.preventDefault();
      onRequestClose();
    }
  };

  const style = {
    top: `${position.top}px`,
    left: `${position.left}px`,
  } as CSSProperties;

  return (
    <div
      className="temporal-create-backdrop"
      data-temporal-create="backdrop"
      onPointerDown={handleBackdropPointerDown}
    >
      <div
        ref={dialogRef}
        className="temporal-create-composer"
        data-temporal-create="composer"
        role="dialog"
        aria-modal="true"
        aria-labelledby={dialogTitleId}
        onKeyDown={handleKeyDown}
        style={style}
      >
        <div className="temporal-create-composer__header">
          <div>
            <span className="temporal-create-composer__eyebrow">
              {t(($) => $.common.home.timeline.create.draft)}
            </span>
            <h2 id={dialogTitleId}>
              {t(($) => $.common.home.timeline.create.title)}
            </h2>
          </div>
          <button
            className="temporal-create-composer__close"
            type="button"
            onClick={onRequestClose}
            aria-label={t(($) => $.common.home.timeline.create.close)}
          >
            ×
          </button>
        </div>

        <div className="temporal-create-composer__body">
          <label htmlFor={titleId}>
            {t(($) => $.common.home.timeline.create.titleLabel)}
          </label>
          <input
            ref={titleRef}
            id={titleId}
            name="temporal-create-title"
            type="text"
            value={session.draft.current.title}
            onChange={(event) => onTitleChange(event.currentTarget.value)}
            placeholder={t(($) => $.common.home.timeline.create.titlePlaceholder)}
            autoComplete="off"
            spellCheck="true"
          />
        </div>

        {session.closeDecision === 'confirm-discard' ? (
          <div
            className="temporal-create-discard"
            role="alert"
            aria-describedby={discardDescriptionId}
          >
            <div>
              <strong>
                {t(($) => $.common.home.timeline.create.discardTitle)}
              </strong>
              <p id={discardDescriptionId}>
                {t(($) => $.common.home.timeline.create.discardBody)}
              </p>
            </div>
            <div className="temporal-create-discard__actions">
              <button
                ref={continueRef}
                type="button"
                onClick={continueEditing}
              >
                {t(($) => $.common.home.timeline.create.continueEditing)}
              </button>
              <button
                className="temporal-create-discard__destructive"
                type="button"
                onClick={onDiscard}
              >
                {t(($) => $.common.home.timeline.create.discard)}
              </button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
