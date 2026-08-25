import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

type AccessPanelFrameProps = Readonly<{
  titleId: string;
  kicker: string;
  title: string;
  body?: string;
  onBack?: () => void;
  children: ReactNode;
  footer?: ReactNode;
}>;

export function AccessPanelFrame({
  titleId,
  kicker,
  title,
  body,
  onBack,
  children,
  footer,
}: AccessPanelFrameProps) {
  const { t } = useTranslation('common');

  return (
    <section className="access-panel" aria-labelledby={titleId}>
      <div className="access-panel-inner">
        <div className="access-panel-heading-row">
          <p className="access-kicker">{kicker}</p>
          {onBack ? (
            <button
              className="access-inline-action access-back-action"
              type="button"
              onClick={onBack}
            >
              ← {t(($) => $.common.access.action.back)}
            </button>
          ) : null}
        </div>
        <h1 id={titleId}>{title}</h1>
        {body ? <p className="access-signin-copy">{body}</p> : null}
        <div className="access-flow-content">{children}</div>
        {footer ? <div className="access-flow-footer">{footer}</div> : null}
      </div>
    </section>
  );
}

type AccessPasswordToggleProps = Readonly<{
  showPassword: boolean;
  onToggle: () => void;
  controls: string;
  fieldLabel?: string;
}>;

export function AccessPasswordToggle({
  showPassword,
  onToggle,
  controls,
  fieldLabel,
}: AccessPasswordToggleProps) {
  const { t } = useTranslation('common');
  const action = showPassword
    ? t(($) => $.common.access.action.hidePassword)
    : t(($) => $.common.access.action.showPassword);
  const label = fieldLabel ? `${action}: ${fieldLabel}` : action;

  return (
    <button
      className="access-password-toggle"
      type="button"
      aria-label={label}
      aria-controls={controls}
      aria-pressed={showPassword}
      onClick={onToggle}
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.8"
        focusable="false"
        aria-hidden="true"
      >
        <path d="M2.5 12s3.4-6 9.5-6 9.5 6 9.5 6-3.4 6-9.5 6-9.5-6-9.5-6Z" />
        <circle cx="12" cy="12" r="2.7" />
        {showPassword ? <path d="m4 4 16 16" /> : null}
      </svg>
    </button>
  );
}
