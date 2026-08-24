import { useTranslation } from 'react-i18next';

import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';

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

        <p className="access-kicker">{t(($) => $.access.kicker.access)}</p>
        <h2 id="access-signin-title">{t(($) => $.access.signin.title)}</h2>
        <p className="access-signin-copy">{t(($) => $.access.signin.body)}</p>

        <div className="access-provider-stack" aria-label="Provider sign-in options">
          <button className="access-provider-button" type="button">
            <span className="access-provider-mark" aria-hidden="true">
              G
            </span>
            <span>{t(($) => $.access.provider.google)}</span>
          </button>
          <button className="access-provider-button" type="button">
            <span className="access-provider-mark access-provider-mark-apple" aria-hidden="true">
              ●
            </span>
            <span>{t(($) => $.access.provider.apple)}</span>
          </button>
        </div>

        <div className="access-divider" aria-hidden="true">
          <span />
          <p>{t(($) => $.access.common.or)}</p>
          <span />
        </div>

        <div className="access-field-stack">
          <label className="access-field">
            <span>{t(($) => $.access.field.email)}</span>
            <input
              name="email"
              type="email"
              autoComplete="email"
              inputMode="email"
            />
          </label>

          <label className="access-field">
            <span className="access-field-heading">
              <span>{t(($) => $.access.field.password)}</span>
              <button className="access-inline-action" type="button">
                {t(($) => $.access.signin.forgot)}
              </button>
            </span>
            <input
              name="password"
              type="password"
              autoComplete="current-password"
            />
          </label>
        </div>

        <button className="access-primary-button" type="button">
          {t(($) => $.access.action.signin)}
        </button>

        <div className="access-new-account">
          <span>{t(($) => $.access.signin.new)}</span>
          <button className="access-inline-action access-create-account" type="button">
            {t(($) => $.access.action.createAccount)}
          </button>
        </div>

        <p className="access-legal">
          {t(($) => $.access.legal.prefix)}{' '}
          <button type="button">{t(($) => $.access.legal.terms)}</button>
          {' · '}
          <button type="button">{t(($) => $.access.legal.privacy)}</button>
        </p>
      </div>
    </section>
  );
}
