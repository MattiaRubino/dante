import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';

export function GlobalTopbar() {
  const { t } = useTranslation('common');

  return (
    <header className="home-topbar" data-home-region="topbar">
      <div className="home-topbar-left">
        <div
          className="home-topbar-brand"
          aria-label={t(($) => $.common.home.topbar.brandLabel)}
        >
          <img src={danteSymbolUrl} alt="" aria-hidden="true" />
          <span>DANTE</span>
        </div>

        <button
          className="home-topbar-search"
          type="button"
          disabled
          aria-label={t(($) => $.common.home.topbar.search)}
          data-home-control="search"
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="6.5" />
            <path d="m16 16 4 4" />
          </svg>
          <span>{t(($) => $.common.home.topbar.search)}</span>
          <kbd>⌘ K</kbd>
        </button>
      </div>

      <nav aria-label={t(($) => $.common.home.topbar.navigationLabel)}>
        <span aria-current="page">
          {t(($) => $.common.home.topbar.home)}
        </span>
        <span>{t(($) => $.common.home.topbar.worlds)}</span>
        <span>{t(($) => $.common.home.topbar.today)}</span>
      </nav>

      <div className="home-topbar-utilities">
        <button
          className="home-topbar-create"
          type="button"
          disabled
          data-home-control="create"
        >
          <span aria-hidden="true">＋</span>
          <span className="home-topbar-create-label">
            {t(($) => $.common.home.topbar.create)}
          </span>
        </button>

        <button
          className="home-topbar-review"
          type="button"
          disabled
          data-home-control="review"
        >
          {t(($) => $.common.home.topbar.review)}
        </button>

        <button
          className="home-topbar-icon-button"
          type="button"
          disabled
          aria-label={t(($) => $.common.home.topbar.launcher)}
          data-home-control="launcher"
        >
          <span className="home-topbar-launcher-glyph" aria-hidden="true">
            {Array.from({ length: 9 }, (_, index) => (
              <span key={index} />
            ))}
          </span>
        </button>

        <button
          className="home-topbar-account"
          type="button"
          disabled
          aria-label={t(($) => $.common.home.topbar.account)}
          data-home-control="account"
        >
          <span aria-hidden="true" />
        </button>
      </div>
    </header>
  );
}
