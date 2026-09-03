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
import { temporalCreateProductCopy } from './temporal-create-product-copy';
import type {
  TemporalCreateComposerPosition,
  TemporalCreateContextOption,
} from './temporal-create-ui-types';

export type {
  TemporalCreateComposerPosition,
  TemporalCreateContextOption,
} from './temporal-create-ui-types';

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
  const { t, i18n } = useTranslation('common');
  const copy = temporalCreateProductCopy(i18n.resolvedLanguage ?? i18n.language);
  const titleId = useId();
  const dialogTitleId = useId();
  const discardTitleId = useId();
  const discardDescriptionId = useId();
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const discardRef = useRef<HTMLDivElement | null>(null);
  const titleRef = useRef<HTMLInputElement | null>(null);
  const continueRef = useRef<HTMLButtonElement | null>(null);
  const closeAttemptFocusRef = useRef<HTMLElement | null>(null);
  const fields = session.draft.current;
  const pending = lifecycle === 'pending';
  const discardPending = session.closeDecision === 'confirm-discard';
  const advanced = session.surface !== 'quick';

  useLayoutEffect(() => {
    titleRef.current?.focus();
  }, []);

  useLayoutEffect(() => {
    if (discardPending) {
      continueRef.current?.focus();
    }
  }, [discardPending]);

  useEffect(() => {
    if (issues.length === 0 || discardPending) {
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
  }, [discardPending, issues, session.surface]);

  const rememberCloseAttemptFocus = () => {
    const active = document.activeElement;
    closeAttemptFocusRef.current =
      active instanceof HTMLElement && dialogRef.current?.contains(active)
        ? active
        : titleRef.current;
  };

  const requestCloseFromCurrentFocus = () => {
    rememberCloseAttemptFocus();
    onRequestClose();
  };

  const continueEditing = () => {
    const returnTarget = closeAttemptFocusRef.current;
    onContinueEditing();
    requestAnimationFrame(() => {
      if (returnTarget?.isConnected) {
        returnTarget.focus({ preventScroll: true });
      } else {
        titleRef.current?.focus({ preventScroll: true });
      }
    });
  };

  const handleKeyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      if (discardPending) {
        continueEditing();
      } else if (!pending) {
        requestCloseFromCurrentFocus();
      }
      return;
    }

    if (event.key !== 'Tab') {
      return;
    }
    const root = discardPending ? discardRef.current : dialogRef.current;
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
      requestCloseFromCurrentFocus();
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
      case 'temporal.create.event_buffer.invalid':
        return t(($) => $.common.home.timeline.create.validation.eventBuffer);
      case 'temporal.create.recurrence.interval_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceInterval);
      case 'temporal.create.recurrence.weekdays_required':
        return t(($) => $.common.home.timeline.create.validation.recurrenceWeekdays);
      case 'temporal.create.recurrence.ordinal_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceOrdinal);
      case 'temporal.create.recurrence.elapsed_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceElapsed);
      case 'temporal.create.recurrence.quota_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceQuota);
      case 'temporal.create.recurrence.quota_timezone_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceQuotaTimeZone,
        );
      case 'temporal.create.recurrence.cycle_invalid':
        return t(($) => $.common.home.timeline.create.validation.recurrenceCycle);
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
              ? copy.activity.toPlace
              : null;

  const submitForm = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit();
  };

  const showAdvanced = () => onSurfaceChange('full');

  return (
    <div
      className="temporal-create-backdrop"
      data-temporal-create="backdrop"
      onPointerDown={handleBackdropPointerDown}
    >
      <div
        ref={dialogRef}
        className={`temporal-create-composer${advanced ? ' is-advanced' : ''}`}
        data-temporal-create="composer"
        data-temporal-create-surface={advanced ? 'advanced' : 'base'}
        role="dialog"
        aria-modal="true"
        aria-labelledby={dialogTitleId}
        aria-busy={pending || undefined}
        onKeyDown={handleKeyDown}
        style={style}
      >
        <div
          className="temporal-create-composer__header"
          inert={discardPending || undefined}
        >
          <div className="temporal-create-composer__heading-copy">
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
            disabled={pending}
            onClick={requestCloseFromCurrentFocus}
            aria-label={t(($) => $.common.home.timeline.create.close)}
          >
            ×
          </button>
        </div>

        <form
          className="temporal-create-composer__body"
          inert={discardPending || undefined}
          onSubmit={submitForm}
        >
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
            onRequestAdvanced={showAdvanced}
            renderError={renderError}
          />

          <button
            type="button"
            className={`temporal-create-advanced-toggle${advanced ? ' is-open' : ''}`}
            aria-expanded={advanced}
            onClick={() => onSurfaceChange(advanced ? 'quick' : 'full')}
          >
            <span>{advanced ? copy.hideAdvanced : copy.advanced}</span>
            <span aria-hidden="true">{advanced ? '⌃' : '⌄'}</span>
          </button>

          <TemporalCreateAdvancedFields
            fields={fields}
            contexts={contexts}
            depth={advanced ? 'full' : 'quick'}
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
            {fields.kind === 'event' &&
            fields.eventRecurrence.patternKind !== 'none' ? (
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
            <button
              type="button"
              disabled={pending}
              onClick={requestCloseFromCurrentFocus}
            >
              {t(($) => $.common.home.timeline.create.cancel)}
            </button>
            <button className="is-primary" type="submit" disabled={pending}>
              {pending
                ? t(($) => $.common.home.timeline.create.creating)
                : t(($) => $.common.home.timeline.create.submit)}
            </button>
          </div>
        </form>

        {discardPending ? (
          <div
            ref={discardRef}
            className="temporal-create-discard"
            role="alertdialog"
            aria-modal="true"
            aria-labelledby={discardTitleId}
            aria-describedby={discardDescriptionId}
          >
            <div>
              <strong id={discardTitleId}>
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
