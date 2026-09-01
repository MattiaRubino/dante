import { useState, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';

import type { ProviderContinuation } from '../application/auth-provider';
import { isValidAccessEmail } from '../model/access-flow';
import { AccessPanelFrame, AccessPasswordToggle } from './access-panel-frame';

type ProviderContinuationValue = Exclude<
  ProviderContinuation,
  Readonly<{ kind: 'none' }>
>;

type AccessProviderFlowPanelProps = Readonly<{
  continuation: ProviderContinuationValue;
  authenticated: boolean;
  errorMessage: string | null;
  pending: boolean;
  onSetEnrollmentEmail: (email: string) => void;
  onVerifyEnrollment: (code: string) => void;
  onResendEnrollment: () => void;
  onAuthenticateExistingAccount: (email: string, password: string) => void;
  onAuthenticateExistingPasskey: () => void;
  onConfirmLink: () => void;
}>;

function continuationStateKey(continuation: ProviderContinuationValue): string {
  if (continuation.kind === 'link') {
    return `link:${continuation.link.external_link_challenge_ref}`;
  }
  return `enrollment:${continuation.enrollment.email_address ?? ''}:${continuation.enrollment.verification_expires_at ?? ''}`;
}

export function AccessProviderFlowPanel(props: AccessProviderFlowPanelProps) {
  return (
    <AccessProviderFlowPanelState
      key={continuationStateKey(props.continuation)}
      {...props}
    />
  );
}

function AccessProviderFlowPanelState({
  continuation,
  authenticated,
  errorMessage,
  pending,
  onSetEnrollmentEmail,
  onVerifyEnrollment,
  onResendEnrollment,
  onAuthenticateExistingAccount,
  onAuthenticateExistingPasskey,
  onConfirmLink,
}: AccessProviderFlowPanelProps) {
  const { t } = useTranslation('common');
  const enrollment =
    continuation.kind === 'enrollment' ? continuation.enrollment : null;
  const [editingEmail, setEditingEmail] = useState(
    enrollment?.verification_expires_at == null,
  );
  const [email, setEmail] = useState(enrollment?.email_address ?? '');
  const [code, setCode] = useState('');
  const [fieldError, setFieldError] = useState<string | null>(null);
  const [linkEmail, setLinkEmail] = useState('');
  const [linkPassword, setLinkPassword] = useState('');
  const [showLinkPassword, setShowLinkPassword] = useState(false);

  function submitLinkCredentials(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmedEmail = linkEmail.trim();
    if (!isValidAccessEmail(trimmedEmail)) {
      setFieldError(t(($) => $.common.access.validation.email));
      return;
    }
    if (linkPassword.length === 0) {
      setFieldError(t(($) => $.common.access.validation.passwordRequired));
      return;
    }
    setFieldError(null);
    onAuthenticateExistingAccount(trimmedEmail, linkPassword);
  }

  if (continuation.kind === 'link') {
    const provider = continuation.link.provider_code;
    const passwordLabel = t(($) => $.common.access.field.password);
    return (
      <AccessPanelFrame
        titleId="access-provider-link-title"
        kicker={t(($) => $.common.access.kicker.access)}
        title={t(($) => $.common.access.link.title)}
        body={t(($) => $.common.access.link.body)}
      >
        <p className="access-provider-label">
          {provider === 'google'
            ? t(($) => $.common.access.provider.googleName)
            : provider === 'apple'
              ? t(($) => $.common.access.provider.appleName)
              : provider}
        </p>
        {authenticated ? (
          <>
            <p className="access-security-note">
              {t(($) => $.common.access.link.authenticatedReady)}
            </p>
            <button
              className="access-primary-button"
              type="button"
              disabled={pending}
              aria-busy={pending}
              onClick={onConfirmLink}
            >
              {t(($) => $.common.access.link.confirm)}
            </button>
          </>
        ) : (
          <>
            <p className="access-security-note">
              {t(($) => $.common.access.link.authenticateFirst)}
            </p>
            <form
              className="access-flow-form"
              onSubmit={submitLinkCredentials}
              noValidate
            >
              <div className="access-field">
                <label htmlFor="access-link-email">
                  {t(($) => $.common.access.field.email)}
                </label>
                <input
                  id="access-link-email"
                  type="email"
                  autoComplete="email"
                  value={linkEmail}
                  disabled={pending}
                  onChange={(event) => {
                    setLinkEmail(event.target.value);
                    setFieldError(null);
                  }}
                />
              </div>
              <div className="access-field">
                <label htmlFor="access-link-password">{passwordLabel}</label>
                <div className="access-input-wrap">
                  <input
                    id="access-link-password"
                    type={showLinkPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    value={linkPassword}
                    disabled={pending}
                    onChange={(event) => {
                      setLinkPassword(event.target.value);
                      setFieldError(null);
                    }}
                  />
                  <AccessPasswordToggle
                    showPassword={showLinkPassword}
                    controls="access-link-password"
                    fieldLabel={passwordLabel}
                    onToggle={() => setShowLinkPassword((value) => !value)}
                  />
                </div>
              </div>
              <button
                className="access-primary-button"
                type="submit"
                disabled={pending}
                aria-busy={pending}
              >
                {t(($) => $.common.access.link.authenticate)}
              </button>
            </form>
            <div className="access-divider" aria-hidden="true">
              <span />
              <p>{t(($) => $.common.access.common.or)}</p>
              <span />
            </div>
            <button
              className="access-secondary-button"
              type="button"
              disabled={pending}
              onClick={onAuthenticateExistingPasskey}
            >
              {t(($) => $.common.access.link.authenticatePasskey)}
            </button>
          </>
        )}
        {fieldError || errorMessage ? (
          <p className="access-field-error" role="alert">
            {fieldError ?? errorMessage}
          </p>
        ) : null}
      </AccessPanelFrame>
    );
  }

  const verificationIssued =
    enrollment?.verification_expires_at !== null &&
    enrollment?.verification_expires_at !== undefined &&
    !editingEmail;

  function submitEmail(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = email.trim();
    if (!isValidAccessEmail(trimmed)) {
      setFieldError(t(($) => $.common.access.validation.email));
      return;
    }
    setFieldError(null);
    onSetEnrollmentEmail(trimmed);
  }

  function submitCode(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!/^\d{6}$/.test(code)) {
      setFieldError(t(($) => $.common.access.validation.verificationCode));
      return;
    }
    setFieldError(null);
    onVerifyEnrollment(code);
  }

  return (
    <AccessPanelFrame
      titleId="access-provider-enrollment-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.providerEnrollment.title)}
      body={t(($) => $.common.access.providerEnrollment.body)}
    >
      {verificationIssued ? (
        <>
          <p className="access-email-context">{enrollment?.email_address}</p>
          <form className="access-flow-form" onSubmit={submitCode} noValidate>
            <div className="access-field">
              <label htmlFor="access-provider-enrollment-code">
                {t(($) => $.common.access.field.verificationCode)}
              </label>
              <input
                id="access-provider-enrollment-code"
                className="access-code-input"
                inputMode="numeric"
                autoComplete="one-time-code"
                maxLength={6}
                value={code}
                disabled={pending}
                aria-invalid={Boolean(fieldError || errorMessage)}
                onChange={(event) => {
                  setCode(event.target.value.replace(/\D/g, '').slice(0, 6));
                  setFieldError(null);
                }}
              />
            </div>
            <button
              className="access-primary-button"
              type="submit"
              disabled={pending}
              aria-busy={pending}
            >
              {t(($) => $.common.access.providerEnrollment.verify)}
            </button>
          </form>
          <div className="access-secondary-actions">
            <button
              className="access-inline-action"
              type="button"
              disabled={pending}
              onClick={onResendEnrollment}
            >
              {t(($) => $.common.access.verify.resend)}
            </button>
            <button
              className="access-inline-action"
              type="button"
              disabled={pending}
              onClick={() => setEditingEmail(true)}
            >
              {t(($) => $.common.access.action.changeEmail)}
            </button>
          </div>
        </>
      ) : (
        <form className="access-flow-form" onSubmit={submitEmail} noValidate>
          <div className="access-field">
            <label htmlFor="access-provider-enrollment-email">
              {t(($) => $.common.access.field.email)}
            </label>
            <input
              id="access-provider-enrollment-email"
              type="email"
              inputMode="email"
              autoComplete="email"
              value={email}
              disabled={pending}
              aria-invalid={Boolean(fieldError || errorMessage)}
              onChange={(event) => {
                setEmail(event.target.value);
                setFieldError(null);
              }}
            />
          </div>
          <button
            className="access-primary-button"
            type="submit"
            disabled={pending}
            aria-busy={pending}
          >
            {t(($) => $.common.access.providerEnrollment.sendCode)}
          </button>
        </form>
      )}
      {fieldError || errorMessage ? (
        <p className="access-field-error" role="alert">
          {fieldError ?? errorMessage}
        </p>
      ) : null}
      <p className="access-security-note">
        {t(($) => $.common.access.providerEnrollment.privacy)}
      </p>
    </AccessPanelFrame>
  );
}
