import { useState, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';

import {
  isValidAccessEmail,
  type AccessCondition,
  type AccessProvider,
} from '../model/access-flow';
import { ProviderButton } from './provider-button';

type AccessSignInPanelProps = Readonly<{
  condition: AccessCondition;
  onCreateAccount: () => void;
  onForgotPassword: () => void;
  onCredentialSubmit: (email: string, password: string) => void;
  onProvider: (provider: AccessProvider) => void;
}>;

type SignInErrors = Readonly<{
  email?: string;
  password?: string;
}>;

function AccessConditionNotice({ condition }: { condition: AccessCondition }) {
  const { t } = useTranslation('common');

  if (condition.kind === 'idle') {
    return null;
  }

  const title =
    condition.kind === 'offline'
      ? t(($) => $.common.access.network.offlineTitle)
      : condition.kind === 'rate-limited'
        ? t(($) => $.common.access.network.rateLimitedTitle)
        : condition.kind === 'server-unavailable'
          ? t(($) => $.common.access.network.serverUnavailableTitle)
          : t(($) => $.common.access.integration.title);

  const body =
    condition.kind === 'offline'
      ? t(($) => $.common.access.network.offlineBody)
      : condition.kind === 'rate-limited'
        ? t(($) => $.common.access.network.rateLimitedBody)
        : condition.kind === 'server-unavailable'
          ? t(($) => $.common.access.network.serverUnavailableBody)
          : t(($) => $.common.access.integration.body);

  return (
    <div className="access-condition-notice" role="status" aria-live="polite">
      <strong>{title}</strong>
      <span>{body}</span>
    </div>
  );
}

export function AccessSignInPanel({
  condition,
  onCreateAccount,
  onForgotPassword,
  onCredentialSubmit,
  onProvider,
}: AccessSignInPanelProps) {
  const { t } = useTranslation('common');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<SignInErrors>({});
  const [showPassword, setShowPassword] = useState(false);
  const passwordControlLabel = showPassword
    ? t(($) => $.common.access.action.hidePassword)
    : t(($) => $.common.access.action.showPassword);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const nextErrors: SignInErrors = {};
    const trimmedEmail = email.trim();

    if (!isValidAccessEmail(trimmedEmail)) {
      nextErrors.email = t(($) => $.common.access.validation.email);
    }
    if (!password) {
      nextErrors.password = t(($) => $.common.access.validation.passwordRequired);
    }

    setErrors(nextErrors);
    if (nextErrors.email || nextErrors.password) {
      return;
    }

    onCredentialSubmit(trimmedEmail, password);
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
          <ProviderButton
            provider="google"
            label={t(($) => $.common.access.provider.google)}
            onClick={() => onProvider('google')}
          />
          <ProviderButton
            provider="apple"
            label={t(($) => $.common.access.provider.apple)}
            onClick={() => onProvider('apple')}
          />
        </div>

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
              aria-invalid={Boolean(errors.email)}
              aria-describedby={errors.email ? 'access-email-error' : undefined}
              onChange={(event) => {
                setEmail(event.target.value);
                if (errors.email) {
                  setErrors((current) => ({ ...current, email: undefined }));
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
                aria-invalid={Boolean(errors.password)}
                aria-describedby={
                  errors.password ? 'access-password-error' : undefined
                }
                onChange={(event) => {
                  setPassword(event.target.value);
                  if (errors.password) {
                    setErrors((current) => ({
                      ...current,
                      password: undefined,
                    }));
                  }
                }}
              />
              <button
                className="access-password-toggle"
                type="button"
                aria-label={passwordControlLabel}
                aria-pressed={showPassword}
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

        <button className="access-primary-button" type="submit">
          {t(($) => $.common.access.action.signin)}
        </button>

        <AccessConditionNotice condition={condition} />

        <div className="access-new-account">
          <span>{t(($) => $.common.access.signin.new)}</span>
          <button
            className="access-inline-action access-create-account"
            type="button"
            onClick={onCreateAccount}
          >
            {t(($) => $.common.access.action.createAccount)}
          </button>
        </div>

        <p className="access-legal">
          {t(($) => $.common.access.legal.prefix)}{' '}
          <span className="access-legal-placeholder">
            {t(($) => $.common.access.legal.terms)}
          </span>
          {' · '}
          <span className="access-legal-placeholder">
            {t(($) => $.common.access.legal.privacy)}
          </span>
        </p>
      </form>
    </section>
  );
}
