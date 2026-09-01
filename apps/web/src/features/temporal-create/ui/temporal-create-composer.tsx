import {
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  type CSSProperties,
  type KeyboardEvent,
  type PointerEvent,
} from 'react';
import { useTranslation } from 'react-i18next';

import type { TemporalValidationIssue } from '../../temporal';
import type { TemporalCreateSession } from '../model/temporal-create-session';

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
  onToggleDetails: () => void;
  onRequestClose: () => void;
  onContinueEditing: () => void;
  onDiscard: () => void;
  onSubmit: () => void;
}>;

function focusableElements(root: HTMLElement): HTMLElement[] {
  return Array.from(
    root.querySelectorAll<HTMLElement>(
      'button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
    ),
  ).filter((element) => !element.hasAttribute('hidden'));
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
  onToggleDetails,
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
    requestAnimationFrame(() => {
      dialogRef.current
        ?.querySelector<HTMLElement>(`[data-create-path="${firstPath}"]`)
        ?.focus();
    });
  }, [issues, session.closeDecision]);

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

  const fieldError = (path: string) => {
    const issue = issueFor(issues, path);
    if (!issue) {
      return null;
    }
    const key = issue.code as keyof typeof t;
    void key;
    return (
      <span className="temporal-create-field-error" role="alert">
        {issue.code === 'temporal.projection.title.required'
          ? t(($) => $.common.home.timeline.create.validation.title)
          : issue.code === 'temporal.create.date.invalid'
            ? t(($) => $.common.home.timeline.create.validation.date)
            : issue.code === 'temporal.create.start_time.invalid'
              ? t(($) => $.common.home.timeline.create.validation.time)
              : issue.code === 'temporal.create.duration.invalid'
                ? t(($) => $.common.home.timeline.create.validation.duration)
                : issue.code === 'temporal.create.timezone.invalid'
                  ? t(($) => $.common.home.timeline.create.validation.timeZone)
                  : issue.code === 'temporal.create.event.requires_placement'
                    ? t(($) => $.common.home.timeline.create.validation.eventPlacement)
                    : t(($) => $.common.home.timeline.create.validation.generic)}
      </span>
    );
  };

  const style = {
    top: `${position.top}px`,
    left: `${position.left}px`,
  } satisfies CSSProperties;

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
        aria-busy={pending || undefined}
        onKeyDown={handleKeyDown}
        style={style}
      >
        <div className="temporal-create-composer__header">
          <div>
            <span className="temporal-create-composer__eyebrow">
              {t(($) => $.common.home.timeline.create.draft)}
            </span>
            <h2 id={dialogTitleId}>{t(($) => $.common.home.timeline.create.title)}</h2>
          </div>
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

        <div className="temporal-create-composer__body">
          <label htmlFor={titleId}>{t(($) => $.common.home.timeline.create.titleLabel)}</label>
          <input
            ref={titleRef}
            id={titleId}
            data-create-path="title"
            name="temporal-create-title"
            type="text"
            value={fields.title}
            onChange={(event) => onPatch({ title: event.currentTarget.value })}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                onSubmit();
              }
            }}
            placeholder={t(($) => $.common.home.timeline.create.titlePlaceholder)}
            autoComplete="off"
            spellCheck="true"
          />
          {fieldError('title')}

          <div className="temporal-create-segmented" role="radiogroup" aria-label={t(($) => $.common.home.timeline.create.kind.label)}>
            {(['activity', 'event'] as const).map((kind) => (
              <button
                key={kind}
                type="button"
                role="radio"
                aria-checked={fields.kind === kind}
                className={fields.kind === kind ? 'is-active' : ''}
                onClick={() =>
                  onPatch({
                    kind,
                    ...(kind === 'event' && fields.timeSemantics === 'unscheduled'
                      ? { timeSemantics: 'timed' as const }
                      : {}),
                  })
                }
              >
                {kind === 'activity'
                  ? t(($) => $.common.home.timeline.create.kind.activity)
                  : t(($) => $.common.home.timeline.create.kind.event)}
              </button>
            ))}
          </div>

          <div className="temporal-create-segmented is-secondary" role="radiogroup" aria-label={t(($) => $.common.home.timeline.create.timeSemantics.label)} data-create-path="timeSemantics">
            {(['timed', 'all-day', 'unscheduled'] as const).map((semantics) => (
              <button
                key={semantics}
                type="button"
                role="radio"
                aria-checked={fields.timeSemantics === semantics}
                disabled={fields.kind === 'event' && semantics === 'unscheduled'}
                className={fields.timeSemantics === semantics ? 'is-active' : ''}
                onClick={() => onPatch({ timeSemantics: semantics })}
              >
                {semantics === 'timed'
                  ? t(($) => $.common.home.timeline.create.timeSemantics.timed)
                  : semantics === 'all-day'
                    ? t(($) => $.common.home.timeline.create.timeSemantics.allDay)
                    : t(($) => $.common.home.timeline.create.timeSemantics.unscheduled)}
              </button>
            ))}
          </div>
          {fieldError('timeSemantics')}

          <div className="temporal-create-temporal-row">
            <label className="temporal-create-control">
              <span>{t(($) => $.common.home.timeline.create.date)}</span>
              <input data-create-path="date" type="date" value={fields.date} onChange={(event) => onPatch({ date: event.currentTarget.value })} />
              {fieldError('date')}
            </label>
            {fields.timeSemantics === 'timed' ? (
              <>
                <label className="temporal-create-control">
                  <span>{t(($) => $.common.home.timeline.create.start)}</span>
                  <input data-create-path="startTime" type="time" step="300" value={fields.startTime} onChange={(event) => onPatch({ startTime: event.currentTarget.value })} />
                  {fieldError('startTime')}
                </label>
                <label className="temporal-create-control">
                  <span>{t(($) => $.common.home.timeline.create.duration)}</span>
                  <select data-create-path="durationMinutes" value={fields.durationMinutes} onChange={(event) => onPatch({ durationMinutes: Number(event.currentTarget.value) })}>
                    {[15, 30, 45, 60, 90, 120, 180].map((minutes) => (
                      <option key={minutes} value={minutes}>{minutes < 60 ? `${minutes} min` : minutes % 60 === 0 ? `${minutes / 60} h` : `${Math.floor(minutes / 60)} h ${minutes % 60} min`}</option>
                    ))}
                  </select>
                  {fieldError('durationMinutes')}
                </label>
              </>
            ) : null}
          </div>

          <label className="temporal-create-control">
            <span>{t(($) => $.common.home.timeline.create.context)}</span>
            <select data-create-path="contextId" value={fields.contextId} onChange={(event) => onPatch({ contextId: event.currentTarget.value })}>
              {contexts.map((context) => <option key={context.id} value={context.id}>{context.label}</option>)}
            </select>
          </label>

          <button className="temporal-create-details-toggle" type="button" aria-expanded={session.detailsOpen} onClick={onToggleDetails}>
            {session.detailsOpen
              ? t(($) => $.common.home.timeline.create.details.hide)
              : t(($) => $.common.home.timeline.create.details.show)}
          </button>

          {session.detailsOpen ? (
            <div className="temporal-create-details">
              {fields.timeSemantics === 'timed' ? (
                <>
                  <div className="temporal-create-segmented is-secondary" role="radiogroup" aria-label={t(($) => $.common.home.timeline.create.timeMode.label)}>
                    {(['floating', 'zoned'] as const).map((mode) => (
                      <button key={mode} type="button" role="radio" aria-checked={fields.timeMode === mode} className={fields.timeMode === mode ? 'is-active' : ''} onClick={() => onPatch({ timeMode: mode })}>
                        {mode === 'floating'
                          ? t(($) => $.common.home.timeline.create.timeMode.floating)
                          : t(($) => $.common.home.timeline.create.timeMode.zoned)}
                      </button>
                    ))}
                  </div>
                  {fields.timeMode === 'zoned' ? (
                    <label className="temporal-create-control">
                      <span>{t(($) => $.common.home.timeline.create.timeZone)}</span>
                      <input data-create-path="timeZoneId" type="text" value={fields.timeZoneId} onChange={(event) => onPatch({ timeZoneId: event.currentTarget.value })} autoComplete="off" />
                      {fieldError('timeZoneId')}
                    </label>
                  ) : null}
                </>
              ) : null}
              <label className="temporal-create-control">
                <span>{t(($) => $.common.home.timeline.create.notes)}</span>
                <textarea value={fields.notes} rows={3} onChange={(event) => onPatch({ notes: event.currentTarget.value })} placeholder={t(($) => $.common.home.timeline.create.notesPlaceholder)} />
              </label>
            </div>
          ) : null}

          <div className="temporal-create-preview-summary" aria-live="polite">
            <span>{fields.kind === 'activity' ? t(($) => $.common.home.timeline.create.kind.activity) : t(($) => $.common.home.timeline.create.kind.event)}</span>
            <b>·</b>
            <span>{fields.timeSemantics === 'unscheduled' ? t(($) => $.common.home.timeline.create.preview.unscheduled) : fields.timeSemantics === 'all-day' ? `${fields.date} · ${t(($) => $.common.home.timeline.create.timeSemantics.allDay)}` : `${fields.date} · ${fields.startTime} · ${fields.durationMinutes} min`}</span>
          </div>

          {failureMessage ? <div className="temporal-create-operation-error" role="alert">{failureMessage}</div> : null}

          <div className="temporal-create-actions">
            <button type="button" disabled={pending} onClick={onRequestClose}>{t(($) => $.common.home.timeline.create.cancel)}</button>
            <button className="is-primary" type="button" disabled={pending} onClick={onSubmit}>{pending ? t(($) => $.common.home.timeline.create.creating) : t(($) => $.common.home.timeline.create.submit)}</button>
          </div>
        </div>

        {session.closeDecision === 'confirm-discard' ? (
          <div className="temporal-create-discard" role="alert" aria-describedby={discardDescriptionId}>
            <div>
              <strong>{t(($) => $.common.home.timeline.create.discardTitle)}</strong>
              <p id={discardDescriptionId}>{t(($) => $.common.home.timeline.create.discardBody)}</p>
            </div>
            <div className="temporal-create-discard__actions">
              <button ref={continueRef} type="button" onClick={continueEditing}>{t(($) => $.common.home.timeline.create.continueEditing)}</button>
              <button className="temporal-create-discard__destructive" type="button" onClick={onDiscard}>{t(($) => $.common.home.timeline.create.discard)}</button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
