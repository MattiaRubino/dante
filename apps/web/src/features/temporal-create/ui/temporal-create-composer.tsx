import {
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
  type FormEvent,
  type KeyboardEvent,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalValidationIssue } from '../../temporal';
import type {
  TemporalCreateSession,
  TemporalCreateSurface,
} from '../model/temporal-create-session';
import type { TemporalCreateU2AuthoringDraft } from '../model/temporal-create-u2-authoring';
import {
  TemporalCreateAdvancedActivityHeaderActions,
  TemporalCreateAdvancedActivityStructure,
} from './temporal-create-advanced-activity-structure';
import { TemporalCreateEventAgenda } from './temporal-create-event-agenda';
import { TemporalCreateRealityObjectivesSection } from './temporal-create-reality-objectives-section';
import { TemporalCreateCalendarRecurrenceFields } from './temporal-create-calendar-recurrence-fields';
import {
  TemporalCreateAdvancedFields,
  TemporalCreateCoreFields,
} from './temporal-create-fields';
import { temporalCreateProductCopy } from './temporal-create-product-copy';
import { TemporalCreateU2DraftProvider } from './temporal-create-u2-draft-context';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

export type { TemporalCreateContextOption } from './temporal-create-ui-types';

type TemporalCreateComposerProps = Readonly<{
  session: TemporalCreateSession;
  contexts: readonly TemporalCreateContextOption[];
  issues: readonly TemporalValidationIssue[];
  lifecycle: 'idle' | 'pending' | 'failed';
  failureMessage: string;
  postCreateRetry: boolean;
  u2Draft: TemporalCreateU2AuthoringDraft;
  onPatch: (patch: Partial<TemporalCreateSession['draft']['current']>) => void;
  onSurfaceChange: (surface: TemporalCreateSurface) => void;
  onRequestClose: () => void;
  onContinueEditing: () => void;
  onDiscard: () => void;
  onMoveToUnplaced: () => void;
  onSubmit: () => void;
  onU2DraftChange?: (draft: TemporalCreateU2AuthoringDraft) => void;
}>;

const FOCUSABLE_SELECTOR =
  'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';
const NOOP_U2_DRAFT = () => undefined;

function focusableElements(root: HTMLElement): HTMLElement[] {
  return Array.from(
    root.querySelectorAll<HTMLElement>(FOCUSABLE_SELECTOR),
  ).filter((element) => !element.hasAttribute('hidden'));
}

function focusValidationPath(root: HTMLElement, path: string): void {
  const region = root.querySelector<HTMLElement>(
    `[data-create-path="${path}"]`,
  );
  if (!region) return;
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

function PinIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M9 4h6l-1 5 3 3v2H7v-2l3-3-1-5Z" />
      <path d="M12 14v6" />
    </svg>
  );
}

export function TemporalCreateComposer({
  session,
  contexts,
  issues,
  lifecycle,
  failureMessage,
  postCreateRetry,
  u2Draft,
  onPatch,
  onSurfaceChange,
  onRequestClose,
  onContinueEditing,
  onDiscard,
  onMoveToUnplaced,
  onSubmit,
  onU2DraftChange = NOOP_U2_DRAFT,
}: TemporalCreateComposerProps) {
  const { t, i18n } = useTranslation('common');
  const copy = temporalCreateProductCopy(
    i18n.resolvedLanguage ?? i18n.language,
  );
  const titleId = useId();
  const discardTitleId = useId();
  const discardDescriptionId = useId();
  const dialogRef = useRef<HTMLDivElement | null>(null);
  const discardRef = useRef<HTMLDivElement | null>(null);
  const titleRef = useRef<HTMLInputElement | null>(null);
  const continueRef = useRef<HTMLButtonElement | null>(null);
  const closeAttemptFocusRef = useRef<HTMLElement | null>(null);
  const advancedTargetRef = useRef<'recurrence' | null>(null);
  const [pinned, setPinned] = useState(false);
  const fields = session.draft.current;
  const pending = lifecycle === 'pending';
  const discardPending = session.closeDecision === 'confirm-discard';
  const advanced = session.surface !== 'quick';
  const italian = i18n.language.toLowerCase().startsWith('it');

  useLayoutEffect(() => {
    titleRef.current?.focus();
  }, []);

  useLayoutEffect(() => {
    if (discardPending) continueRef.current?.focus();
  }, [discardPending]);

  useEffect(() => {
    if (!advanced || advancedTargetRef.current !== 'recurrence') return;
    const frame = requestAnimationFrame(() => {
      dialogRef.current
        ?.querySelector<HTMLElement>('[data-create-recurrence-owner]')
        ?.scrollIntoView({ block: 'start' });
      advancedTargetRef.current = null;
    });
    return () => cancelAnimationFrame(frame);
  }, [advanced]);

  useEffect(() => {
    if (issues.length === 0 || discardPending) return;
    const firstPath = issues[0]?.path[0];
    if (!firstPath) return;
    const frame = requestAnimationFrame(() => {
      if (dialogRef.current) focusValidationPath(dialogRef.current, firstPath);
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

  const requestCloseFromBackdrop = () => {
    if (pinned) return;
    if (!pending && !discardPending) requestCloseFromCurrentFocus();
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
      if (discardPending) continueEditing();
      else if (!pending) requestCloseFromCurrentFocus();
      return;
    }
    if (event.key !== 'Tab' || !discardPending) return;
    const root = discardRef.current;
    if (!root) return;
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
        return t(
          ($) => $.common.home.timeline.create.validation.eventPlacement,
        );
      case 'temporal.create.all_day_range.invalid':
        return t(($) => $.common.home.timeline.create.validation.allDayRange);
      case 'temporal.create.window.invalid':
        return t(($) => $.common.home.timeline.create.validation.window);
      case 'temporal.create.deadline.invalid':
        return t(($) => $.common.home.timeline.create.validation.deadline);
      case 'temporal.create.preferred_window.invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.preferredWindow,
        );
      case 'temporal.create.minimum_session.invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.minimumSession,
        );
      case 'temporal.create.session_count.invalid':
        return t(($) => $.common.home.timeline.create.validation.sessionCount);
      case 'temporal.create.buffer.invalid':
        return t(($) => $.common.home.timeline.create.validation.buffer);
      case 'temporal.create.event_buffer.invalid':
        return t(($) => $.common.home.timeline.create.validation.eventBuffer);
      case 'temporal.create.recurrence.interval_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceInterval,
        );
      case 'temporal.create.recurrence.weekdays_required':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceWeekdays,
        );
      case 'temporal.create.recurrence.ordinal_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceOrdinal,
        );
      case 'temporal.create.recurrence.elapsed_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceElapsed,
        );
      case 'temporal.create.recurrence.quota_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceQuota,
        );
      case 'temporal.create.recurrence.quota_timezone_invalid':
        return t(
          ($) =>
            $.common.home.timeline.create.validation.recurrenceQuotaTimeZone,
        );
      case 'temporal.create.recurrence.cycle_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceCycle,
        );
      case 'temporal.create.recurrence.until_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceUntil,
        );
      case 'temporal.create.recurrence.count_invalid':
        return t(
          ($) => $.common.home.timeline.create.validation.recurrenceCount,
        );
      case 'temporal.create.recurrence.life_area_required':
        return i18n.language.toLowerCase().startsWith('en')
          ? 'Select a Life Area before creating a recurrence.'
          : 'Per creare una ricorrenza, seleziona una Life Area.';
      case 'temporal.create.reminder.invalid':
        return t(($) => $.common.home.timeline.create.validation.reminder);
      case 'temporal.create.confirmation.outcome_policy_unavailable':
        return i18n.language.toLowerCase().startsWith('en')
          ? 'This outcome policy is not available in Create. Select “Use inherited rule”.'
          : 'Questa regola per l’esito non è disponibile in Crea. Seleziona “Usa la regola ereditata”.';
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

  const submitForm = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onSubmit();
  };

  const showAdvanced = (target?: 'recurrence') => {
    advancedTargetRef.current = target ?? null;
    onSurfaceChange('full');
  };

  const toggleAdvanced = () => {
    advancedTargetRef.current = null;
    onSurfaceChange(advanced ? 'quick' : 'full');
  };

  const resetKey = `${session.draft.baseline.date}|${session.draft.baseline.startTime}|${session.draft.baseline.title}`;

  return (
    <div
      className={`temporal-create-backdrop${advanced ? ' is-advanced' : ''}${discardPending ? ' is-modal' : ''}`}
      data-temporal-create="backdrop"
      onPointerDown={(event) => {
        if (event.target === event.currentTarget) requestCloseFromBackdrop();
      }}
    >
      <div
        ref={dialogRef}
        className={`temporal-create-composer${advanced ? ' is-advanced is-full' : ''}`}
        data-temporal-create="composer"
        data-temporal-create-surface={advanced ? 'advanced' : 'base'}
        data-pinned={pinned || undefined}
        role="dialog"
        aria-modal={discardPending || undefined}
        aria-label={t(($) => $.common.home.timeline.create.title)}
        aria-busy={pending || undefined}
        onKeyDown={handleKeyDown}
      >
        <div
          className="temporal-create-composer__header is-minimal"
          inert={discardPending || undefined}
        >
          <span aria-hidden="true" />
          <div className="temporal-create-composer__header-actions">
            <button
              className="temporal-create-composer__pin"
              type="button"
              aria-pressed={pinned}
              aria-label={
                pinned
                  ? italian
                    ? 'Sblocca pannello Crea'
                    : 'Unpin Create panel'
                  : italian
                    ? 'Mantieni aperto il pannello Crea'
                    : 'Pin Create panel open'
              }
              title={pinned ? 'Pannello fissato' : 'Mantieni aperto'}
              onClick={() => setPinned((current) => !current)}
            >
              <PinIcon />
            </button>
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
        </div>

        {postCreateRetry ? (
          <div className="temporal-create-composer__body" role="status">
            <p>{failureMessage}</p>
            <div className="temporal-create-actions">
              <button
                type="button"
                disabled={pending}
                onClick={requestCloseFromCurrentFocus}
              >
                {t(($) => $.common.home.timeline.create.cancel)}
              </button>
              <button
                className="is-primary"
                type="button"
                disabled={pending}
                onClick={onSubmit}
              >
                {italian ? 'Riprova configurazione' : 'Retry configuration'}
              </button>
            </div>
          </div>
        ) : (
          <form
            className="temporal-create-composer__body"
            inert={discardPending || undefined}
            onSubmit={submitForm}
          >
            <TemporalCreateU2DraftProvider
              fields={fields}
              resetKey={resetKey}
              initialDraft={u2Draft}
              onDraftChange={onU2DraftChange}
            >
              <div
                className={
                  advanced
                    ? fields.kind === 'activity'
                      ? 'temporal-create-title-row has-tools'
                      : 'temporal-create-title-row'
                    : 'temporal-create-title-row is-quick'
                }
              >
                <div className="temporal-create-title-row__name">
                  <label
                    className="temporal-create-visually-hidden"
                    htmlFor={titleId}
                  >
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
                    onChange={(event) =>
                      onPatch({ title: event.currentTarget.value })
                    }
                    placeholder={t(
                      ($) => $.common.home.timeline.create.titleLabel,
                    )}
                    autoComplete="off"
                    spellCheck="true"
                  />
                  {renderError('title')}
                </div>
                {advanced && fields.kind === 'activity' ? (
                  <div className="temporal-create-title-row__tools">
                    <TemporalCreateAdvancedActivityHeaderActions />
                  </div>
                ) : null}
              </div>
              {advanced && fields.kind === 'activity' ? (
                <TemporalCreateAdvancedActivityStructure fields={fields} />
              ) : null}
              {advanced && fields.kind === 'event' ? (
                <TemporalCreateEventAgenda
                  parts={fields.event.agendaParts}
                  onChange={(agendaParts) =>
                    onPatch({
                      event: Object.freeze({
                        ...fields.event,
                        agendaParts,
                      }),
                    })
                  }
                />
              ) : null}
              <TemporalCreateCoreFields
                fields={fields}
                contexts={contexts}
                showCompactTimezone={!advanced}
                repeatDetails={
                  advanced &&
                  fields.eventRecurrence.patternKind === 'calendar-wall-clock' ? (
                    <TemporalCreateCalendarRecurrenceFields
                      fields={fields}
                      onPatch={onPatch}
                      renderError={renderError}
                    />
                  ) : null
                }
                realityObjectives={
                  advanced ? (
                    <TemporalCreateRealityObjectivesSection fields={fields} />
                  ) : null
                }
                onPatch={onPatch}
                onRequestAdvanced={showAdvanced}
                renderError={renderError}
              />

              <TemporalCreateAdvancedFields
                fields={fields}
                contexts={contexts}
                depth={advanced ? 'full' : 'quick'}
                onPatch={onPatch}
                renderError={renderError}
              />
            </TemporalCreateU2DraftProvider>

            {failureMessage ? (
              <div className="temporal-create-operation-error" role="alert">
                {failureMessage}
              </div>
            ) : null}

            <div className="temporal-create-actions">
              <button
                type="button"
                className="temporal-create-advanced-toggle"
                aria-expanded={advanced}
                onClick={toggleAdvanced}
              >
                <span>{advanced ? copy.hideAdvanced : copy.advanced}</span>
                <span aria-hidden="true">{advanced ? '⌃' : '⌄'}</span>
              </button>
              <button className="is-primary" type="submit" disabled={pending}>
                {pending
                  ? t(($) => $.common.home.timeline.create.creating)
                  : t(($) => $.common.home.timeline.create.submit)}
              </button>
            </div>
          </form>
        )}

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
                Annulla
              </button>
              <button
                type="button"
                disabled={pending || fields.title.trim().length === 0}
                onClick={onMoveToUnplaced}
                title={
                  fields.title.trim().length === 0
                    ? 'Inserisci prima un titolo.'
                    : undefined
                }
              >
                Sposta in Da collocare
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
