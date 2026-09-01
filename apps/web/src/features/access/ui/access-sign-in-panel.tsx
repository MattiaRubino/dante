import { useState, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';

import type { ProviderBrowserUnavailableError } from '../../../platform/auth/web-auth-provider';
import { usePasskeySignInMutation } from '../application/auth-passkey';
import { isValidAccessEmail, type AccessCondition } from '../model/access-flow';
import { AccessConditionNotice } from './access-condition-notice';
import { GoogleIdentityButton, ProviderButton } from './provider-button';

export type GoogleButtonState = Readonly<{
  clientId: string | null;
  nonce: string | null;
  pending: boolean;
  errorMessage?: string | null;
  onCredential: (credential: string) => void;
  onError: (error: ProviderBrowserUnavailableError) => void;
}>;

type AccessSignInPanelProps = Readonly<{
  condition: AccessCondition;
  onCreateAccount: () => void;
  onForgotPassword: () => void;
  onCredentialSubmit: (email: string, password: string) => void;
  google: GoogleButtonState;
  onApple: () => void;
  pending?: boolean;
}>;

type SignInErrors = {
  email?: string;
  password?: string;
};

function withoutEmailError(current: SignInErrors): SignInErrors {
  const next: SignInErrors = {};
  if (current.password !== undefined) {
    next.password = current.password;
  }
  return next;
}

function withoutPasswordError(current: SignInErrors): SignInErrors {
  const next: SignInErrors = {};
  if (current.email !== undefined) {
    next.email = current.email;
  }
  return next;
}

export function AccessSignInPanel({
  condition,
  onCreateAccount,
  onForgotPassword,
  onCredentialSubmit,
  google,
  onApple,
  pending = false,
}: AccessSignInPanelProps) {
  const { t } = useTranslation('common');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<SignInErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const [passkeyError, setPasskeyError] = useState<string | null>(null);
  const passkeyMutation = usePasskeySignInMutation();
  const interactionPending =
    pending || passkeyMutation.isPending || google.pending;
  const passwordControlLabel = showPassword
    ? t(($) => $.common.access.action.hidePassword)
    : t(($) => $.common.access.action.showPassword);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (interactionPending) {
      return;
    }

    const nextErrors: SignInErrors = {};
    const trimmedEmail = email.trim();

    if (!isValidAccessEmail(trimmedEmail)) {
      nextErrors.email = t(($) => $.common.access.validation.email);
    }
    if (!password) {
      nextErrors.password = t(
        ($) => $.common.access.validation.passwordRequired,
      );
    }

    setErrors(nextErrors);
    if (nextErrors.email || nextErrors.password) {
      return;
    }

    onCredentialSubmit(trimmedEmail, password);
  }

  function signInWithPasskey() {
    if (interactionPending) {
      return;
    }
    setPasskeyError(null);
    passkeyMutation.mutate(undefined, {
      onError: () =>
        setPasskeyError(t(($) => $.common.access.failure.passkeyBody)),
    });
  }

  return (
    <section className="access-panel" aria-labelledby="access-signin-title">
      <form className="access-panel-inner" onSubmit={handleSubmit} noValidate>
        <p className="access-kicker">
          {t(($) => $.common.access.kicker.access)}
        </p>

        <h1 id="access-signin-title">
          {t(($) => $.common.access.signin.title)}
        </h1>
        <p className="access-signin-copy">
          {t(($) => $.common.access.signin.body)}
        </p>

        <div className="access-provider-stack">
          <GoogleIdentityButton
            label={t(($) => $.common.access.provider.google)}
            clientId={google.clientId}
            nonce={google.nonce}
            onCredential={google.onCredential}
            onError={google.onError}
            disabled={interactionPending}
          />
          <ProviderButton
            provider="apple"
            label={t(($) => $.common.access.provider.apple)}
            onClick={onApple}
            disabled={interactionPending}
          />
          <button
            className="access-provider-button"
            type="button"
            disabled={interactionPending}
            aria-busy={passkeyMutation.isPending}
            onClick={signInWithPasskey}
          >
            <span className="access-provider-icon" aria-hidden="true">
              ◇
            </span>
            <span>{t(($) => $.common.access.provider.passkey)}</span>
          </button>
        </div>

        {google.errorMessage ? (
          <p className="access-field-error" role="alert">
            {google.errorMessage}
          </p>
        ) : null}
        {passkeyError ? (
          <p className="access-field-error" role="alert">
            {passkeyError}
          </p>
        ) : null}

        <div className="access-divider" aria-hidden="true">
          <span />
          <p>{t(($) => $.common.access.common.or)}</p>
          <span />
        </div>

        <div className="access-field-stack">
          <div className="access-field">
            <label htmlFor="access-email">
              {t(($) => $.common.access.field.email)}
            </label>
            <input
              id="access-email"
              name="email"
              type="email"
              autoComplete="email"
              inputMode="email"
              placeholder={t(($) => $.common.access.field.emailPlaceholder)}
              value={email}
              disabled={interactionPending}
              aria-invalid={Boolean(errors.email)}
              aria-describedby={errors.email ? 'access-email-error' : undefined}
              onChange={(event) => {
                setEmail(event.target.value);
                if (errors.email) {
                  setErrors(withoutEmailError);
                }
              }}
            />
            {errors.email ? (
              <span id="access-email-error" className="access-field-error">
                {errors.email}
              </span>
            ) : null}
          </div>

          <div className="access-field">
            <div className="access-field-heading">
              <label htmlFor="access-password">
                {t(($) => $.common.access.field.password)}
              </label>
              <button
                className="access-inline-action"
                type="button"
                onClick={onForgotPassword}
                disabled={interactionPending}
              >
                {t(($) => $.common.access.signin.forgot)}
              </button>
            </div>
            <div className="access-input-wrap">
              <input
                id="access-password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
                value={password}
                disabled={interactionPending}
                aria-invalid={Boolean(errors.password)}
                aria-describedby={
                  errors.password ? 'access-password-error' : undefined
                }
                onChange={(event) => {
                  setPassword(event.target.value);
                  if (errors.password) {
                    setErrors(withoutPasswordError);
                  }
                }}
              />
              <button
                className="access-password-toggle"
                type="button"
                aria-label={passwordControlLabel}
                aria-pressed={showPassword}
                disabled={interactionPending}
                onClick={() => setShowPassword((value) => !value)}
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
            </div>
            {errors.password ? (
              <span id="access-password-error" className="access-field-error">
                {errors.password}
              </span>
            ) : null}
          </div>
        </div>

        <button
          className="access-primary-button"
          type="submit"
          disabled={interactionPending}
          aria-busy={pending}
        >
          {t(($) => $.common.access.action.continue)}
        </button>

        <AccessConditionNotice condition={condition} />

        <div className="access-new-account">
          <span>{t(($) => $.common.access.signin.new)}</span>
          <button
            className="access-inline-action access-create-account"
            type="button"
            onClick={onCreateAccount}
            disabled={interactionPending}
          >
            {t(($) => $.common.access.action.createAccount)}
          </button>
        </div>
      </form>
    </section>
  );
}
