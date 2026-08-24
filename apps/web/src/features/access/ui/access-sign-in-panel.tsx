import { useState } from 'react';
import { useTranslation } from 'react-i18next';

import { ProviderButton } from './provider-button';

export function AccessSignInPanel() {
  const { t } = useTranslation('common');
  const [showPassword, setShowPassword] = useState(false);
  const passwordControlLabel = showPassword
    ? t(($) => $.common.access.action.hidePassword)
    : t(($) => $.common.access.action.showPassword);

  return (
    <section className="access-panel" aria-labelledby="access-signin-title">
      <div className="access-panel-inner">
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
          />
          <ProviderButton
            provider="apple"
            label={t(($) => $.common.access.provider.apple)}
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
            />
          </div>

          <div className="access-field">
            <div className="access-field-heading">
              <label htmlFor="access-password">
                {t(($) => $.common.access.field.password)}
              </label>
              <button className="access-inline-action" type="button">
                {t(($) => $.common.access.signin.forgot)}
              </button>
            </div>
            <div className="access-input-wrap">
              <input
                id="access-password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="current-password"
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
          </div>
        </div>

        <button className="access-primary-button" type="button">
          {t(($) => $.common.access.action.signin)}
        </button>

        <div className="access-new-account">
          <span>{t(($) => $.common.access.signin.new)}</span>
          <button
            className="access-inline-action access-create-account"
            type="button"
          >
            {t(($) => $.common.access.action.createAccount)}
          </button>
        </div>

        <p className="access-legal">
          {t(($) => $.common.access.legal.prefix)}{' '}
          <button type="button">{t(($) => $.common.access.legal.terms)}</button>
          {' · '}
          <button type="button">
            {t(($) => $.common.access.legal.privacy)}
          </button>
        </p>
      </div>
    </section>
  );
}
