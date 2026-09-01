import {
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  type CSSProperties,
  type FormEvent,
  type KeyboardEvent,
  type PointerEvent,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalValidationIssue } from '../../temporal';
import type {
  TemporalCreateSession,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import {
  TemporalCreateAdvancedFields,
  TemporalCreateCoreFields,
} from './temporal-create-fields';

export type TemporalCreateComposerPosition = Readonly<{
  top: number;
  left: number;
}>;

export type TemporalCreateContextOption = Readonly<{
  id: string;
  label: string;
}>;

type TemporalCreateComposerProps = Readonly<{
  position: TemporalCreateComposerPosition;
  session: TemporalCreateSession;
  contexts: readonly TemporalCreateContextOption[];
  issues: readonly TemporalValidationIssue[];
  lifecycle: 'idle' | 'pending' | 'failed';
  failureMessage: string;
  onPatch: (patch: Partial<TemporalCreateSession['draft']['current']>) => void;
  onSurfaceChange: (surface: TemporalCreateSurface) => void;
  onRequestClose: () => void;
  onContinueEditing: () => void;
  onDiscard: () => void;
  onSubmit: () => void;
}>;

const FOCUSABLE_SELECTOR =
  'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

function focusableElements(root: HTMLElement): HTMLElement[] {
  return Array.from(root.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR)).filter(
    (element) => !element.hasAttribute('hidden'),
  );
}

function focusValidationPath(root: HTMLElement, path: string): void {
  const region = root.querySelector<HTMLElement>(`[data-create-path="${path}"]`);
  if (!region) {
    return;
  }
  if (region.matches(FOCUSABLE_SELECTOR)) {
    region.focus();
    return;
  }
  region.querySelector<HTMLElement>(FOCUSABLE_SELECTOR)?.focus();
}

function issueFor(
  issues: readonly TemporalValidationIssue[],
  path: string,
): TemporalValidationIssue | undefined {
  return issues.find((issue) => issue.path[0] === path);
}

export function TemporalCreateComposer({
  position,
  session,
  contexts,
  issues,
  lifecycle,
  failureMessage,
  onPatch,
  onSurfaceChange,
  onRequestClose,
  onContinueEditing,
  onDiscard,
  onSubmit,
}: TemporalCreateComposerProps) {
  const { t } = useTranslation('common');
  const titleId = useId();
  const dialogTitleId = useId();
  const discardDescriptionId = useId();
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const titleRef = useRef<HTMLInputElement | null>(null);
  const continueRef = useRef<HTMLButtonElement | null>(null);
  const fields = session.draft.current;
  const pending = lifecycle === 'pending';

  useLayoutEffect(() => {
    titleRef.current?.focus();
  }, []);

  useLayoutEffect(() => {
    if (session.closeDecision === 'confirm-discard') {
      continueRef.current?.focus();
    }
  }, [session.closeDecision]);

  useEffect(() => {
    if (issues.length === 0 || session.closeDecision === 'confirm-discard') {
      return;
    }
    const firstPath = issues[0]?.path[0];
    if (!firstPath) {
      return;
    }
    const frame = requestAnimationFrame(() => {
      const root = dialogRef.current;
      if (root) {
        focusValidationPath(root, firstPath);
      }
    });
    return () => cancelAnimationFrame(frame);
  }, [issues, session.closeDecision, session.surface]);

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
      } else if (!pending) {
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
    const last = focusables.at(-1);
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last?.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first?.focus();
    }
  };

  const handleBackdropPointerDown = (event: PointerEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget && !pending) {
      event.preventDefault();
      onRequestClose();
    }
  };

  const validationText = (issue: TemporalValidationIssue): string => {
    switch (issue.code) {
      case 'temporal.projection.title.required':
        return t(($) => $.common.home.timeline.create.validation.title);
      case 'temporal.create.date.invalid':
        return t(($) => $.common.home.timeline.create.validation.date);
      case 'temporal.create.start_time.invalid':
        return t(($) => $.common.home.timeline.create.validation.time);
      case 'temporal.create.duration.invalid':
        return t(($) => $.common.home.timeline.create.validation.duration);
      case 'temporal.create.timezone.invalid':
        return t(($) => $.common.home.timeline.create.validation.timeZone);
      case 'temporal.create.event.requires_placement':
        return t(($) => $.common.home.timeline.create.validation.eventPlacement);
      case 'temporal.create.all_day_range.invalid':
        return t(($) => $.common.home.timeline.create.validation.allDayRange);
      case 'temporal.create.window.invalid':
        return t(($) => $.common.home.timeline.create.validation.window);
      case 'temporal.create.deadline.invalid':
        return t(($) => $.common.home.timeline.create.validation.deadline);
      case 'temporal.create.preferred_window.invalid':
        return t(($) => $.common.home.timeline.create.validation.preferredWindow);
      case 'temporal.create.minimum_session.invalid':
        return t(($) => $.common.home.timeline.create.validation.minimumSession);
      case 'temporal.create.session_count.invalid':
        return t(($) => $.common.home.timeline.create.validation.sessionCount);
      case 'temporal.create.buffer.invalid':
        return t(($) => $.common.home.timeline.create.validation.buffer);
      case 'temporal.create.recurrence.interval_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceInterval);
      case 'temporal.create.recurrence.weekdays_required':
        return t(($) => $.common.home.timeline.create.validation.recurrenceWeekdays);
      case 'temporal.create.recurrence.until_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceUntil);
      case 'temporal.create.recurrence.count_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceCount);
      case 'temporal.create.reminder.invalid':
        return t(($) => $.common.home.timeline.create.validation.reminder);
      default:
        return t(($) => $.common.home.timeline.create.validation.generic);
    }
  };

  const renderError = (path: string): ReactNode => {
    const issue = issueFor(issues, path);
    return issue ? (
      <span className="temporal-create-field-error" role="alert">
        {validationText(issue)}
      </span>
    ) : null;
  };

  const style = {
    top: `${position.top}px`,
    left: `${position.left}px`,
  } satisfies CSSProperties;

  const surfaceTitle =
    session.surface === 'full'
      ? t(($) => $.common.home.timeline.create.surface.full)
      : session.surface === 'expanded'
        ? t(($) => $.common.home.timeline.create.surface.expanded)
        : t(($) => $.common.home.timeline.create.title);

  const constraintLabel =
    fields.scheduling.constraintKind === 'open'
      ? t(($) => $.common.home.timeline.create.planning.constraintOpen)
      : fields.scheduling.constraintKind === 'bounded-window'
        ? t(($) => $.common.home.timeline.create.planning.constraintWindow)
        : fields.scheduling.constraintKind === 'deadline'
          ? t(($) => $.common.home.timeline.create.planning.constraintDeadline)
          : fields.scheduling.constraintKind === 'preferred-window'
            ? t(($) => $.common.home.timeline.create.planning.constraintPreferred)
            : fields.timeSemantics === 'unscheduled'
              ? t(($) => $.common.home.timeline.create.timeSemantics.unscheduled)
              : null;

  const submitForm = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit();
  };

  return (
    <div
      className="temporal-create-backdrop"
      data-temporal-create="backdrop"
      onPointerDown={handleBackdropPointerDown}
    >
      <div
        ref={dialogRef}
        className={`temporal-create-composer is-${session.surface}`}
        data-temporal-create="composer"
        data-temporal-create-surface={session.surface}
        role="dialog"
        aria-modal="true"
        aria-labelledby={dialogTitleId}
        aria-busy={pending || undefined}
        onKeyDown={handleKeyDown}
        style={style}
      >
        <div className="temporal-create-composer__header">
          <div className="temporal-create-composer__heading-copy">
            <span className="temporal-create-composer__eyebrow">
              {t(($) => $.common.home.timeline.create.draft)}
            </span>
            <h2 id={dialogTitleId}>{surfaceTitle}</h2>
            {session.surface !== 'quick' ? (
              <p>{t(($) => $.common.home.timeline.create.surface.description)}</p>
            ) : null}
          </div>
          <div className="temporal-create-composer__header-actions">
            {session.surface === 'expanded' ? (
              <button
                type="button"
                className="temporal-create-surface-action"
                onClick={() => onSurfaceChange('full')}
              >
                {t(($) => $.common.home.timeline.create.surface.openFull)}
              </button>
            ) : null}
            {session.surface === 'full' ? (
              <button
                type="button"
                className="temporal-create-surface-action"
                onClick={() => onSurfaceChange('expanded')}
              >
                {t(($) => $.common.home.timeline.create.surface.backExpanded)}
              </button>
            ) : null}
            <button
              className="temporal-create-composer__close"
              type="button"
              disabled={pending}
              onClick={onRequestClose}
              aria-label={t(($) => $.common.home.timeline.create.close)}
            >
              ×
            </button>
          </div>
        </div>

        <form className="temporal-create-composer__body" onSubmit={submitForm}>
          <label className="temporal-create-title-label" htmlFor={titleId}>
            {t(($) => $.common.home.timeline.create.titleLabel)}
          </label>
          <input
            ref={titleRef}
            id={titleId}
            className="temporal-create-title-input"
            data-create-path="title"
            name="temporal-create-title"
            type="text"
            value={fields.title}
            onChange={(event) => onPatch({ title: event.currentTarget.value })}
            placeholder={t(($) => $.common.home.timeline.create.titlePlaceholder)}
            autoComplete="off"
            spellCheck="true"
          />
          {renderError('title')}

          <TemporalCreateCoreFields
            fields={fields}
            contexts={contexts}
            onPatch={onPatch}
            renderError={renderError}
          />

          {session.surface === 'quick' ? (
            <button
              className="temporal-create-details-toggle"
              type="button"
              onClick={() => onSurfaceChange('expanded')}
            >
              <span>{t(($) => $.common.home.timeline.create.details.show)}</span>
              <span aria-hidden="true">→</span>
            </button>
          ) : null}

          <TemporalCreateAdvancedFields
            fields={fields}
            contexts={contexts}
            depth={session.surface}
            onPatch={onPatch}
            renderError={renderError}
          />

          <div className="temporal-create-intent-summary" aria-live="polite">
            <span className="is-kind">
              {fields.kind === 'activity'
                ? t(($) => $.common.home.timeline.create.kind.activity)
                : t(($) => $.common.home.timeline.create.kind.event)}
            </span>
            {constraintLabel ? <span>{constraintLabel}</span> : null}
            {fields.recurrence.frequency !== 'none' ? (
              <span>
                {t(
                  ($) => $.common.home.timeline.create.recurrence.recurringBadge,
                )}
              </span>
            ) : null}
            {fields.timeSemantics === 'timed' && !constraintLabel ? (
              <span>{`${fields.date} · ${fields.startTime} · ${fields.durationMinutes} min`}</span>
            ) : fields.timeSemantics === 'all-day' ? (
              <span>{`${fields.date} · ${t(($) => $.common.home.timeline.create.timeSemantics.allDay)}`}</span>
            ) : null}
          </div>

          {failureMessage ? (
            <div className="temporal-create-operation-error" role="alert">
              {failureMessage}
            </div>
          ) : null}

          <div className="temporal-create-actions">
            {session.surface !== 'quick' ? (
              <button
                type="button"
                disabled={pending}
                onClick={() => onSurfaceChange('quick')}
              >
                {t(($) => $.common.home.timeline.create.surface.compact)}
              </button>
            ) : null}
            <button type="button" disabled={pending} onClick={onRequestClose}>
              {t(($) => $.common.home.timeline.create.cancel)}
            </button>
            <button className="is-primary" type="submit" disabled={pending}>
              {pending
                ? t(($) => $.common.home.timeline.create.creating)
                : t(($) => $.common.home.timeline.create.submit)}
            </button>
          </div>
        </form>

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
              <button ref={continueRef} type="button" onClick={continueEditing}>
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
