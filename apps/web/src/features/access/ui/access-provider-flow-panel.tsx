import { useEffect, useState, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';

import type { ProviderContinuation } from '../application/auth-provider';
import { isValidAccessEmail } from '../model/access-flow';
import { AccessPanelFrame } from './access-panel-frame';

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
  onAuthenticateExistingAccount: () => void;
  onConfirmLink: () => void;
}>;

export function AccessProviderFlowPanel({
  continuation,
  authenticated,
  errorMessage,
  pending,
  onSetEnrollmentEmail,
  onVerifyEnrollment,
  onResendEnrollment,
  onAuthenticateExistingAccount,
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

  useEffect(() => {
    if (enrollment === null) {
      return;
    }
    setEmail(enrollment.email_address ?? '');
    setEditingEmail(enrollment.verification_expires_at == null);
    setCode('');
    setFieldError(null);
  }, [enrollment]);

  if (continuation.kind === 'link') {
    const provider = continuation.link.provider_code;
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
        <p className="access-security-note">
          {authenticated
            ? t(($) => $.common.access.link.authenticatedReady)
            : t(($) => $.common.access.link.authenticateFirst)}
        </p>
        <button
          className="access-primary-button"
          type="button"
          disabled={pending}
          aria-busy={pending}
          onClick={
            authenticated ? onConfirmLink : onAuthenticateExistingAccount
          }
        >
          {authenticated
            ? t(($) => $.common.access.link.confirm)
            : t(($) => $.common.access.link.action)}
        </button>
        {errorMessage ? (
          <p className="access-field-error" role="alert">
            {errorMessage}
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
