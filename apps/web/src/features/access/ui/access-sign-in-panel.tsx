import { useTranslation } from 'react-i18next';

import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';
import { ProviderButton } from './provider-button';

export function AccessSignInPanel() {
  const { t } = useTranslation('common');

  return (
    <section className="access-panel" aria-labelledby="access-signin-title">
      <div className="access-panel-inner">
        <img
          className="access-panel-wordmark"
          src={danteWordmarkUrl}
          alt="DANTE"
        />

        <p className="access-kicker">
          {t(($) => $.common.access.kicker.access)}
        </p>
        <h2 id="access-signin-title">
          {t(($) => $.common.access.signin.title)}
        </h2>
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
            <input
              id="access-password"
              name="password"
              type="password"
              autoComplete="current-password"
            />
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
