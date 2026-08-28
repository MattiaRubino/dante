import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkRaw from '../../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?raw';

const danteWordmarkWhite = danteWordmarkRaw.replaceAll('#222F37', '#FFFFFF');

function SearchIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="11" cy="11" r="6.5" />
      <path d="m16 16 4 4" />
    </svg>
  );
}

function HomeIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M3 10.8 12 3l9 7.8v9.2a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z" />
    </svg>
  );
}

function WorldsIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="8.5" />
      <path d="M3.8 9h16.4M3.8 15h16.4M12 3.5c2.1 2.3 3.2 5.1 3.2 8.5S14.1 18.2 12 20.5M12 3.5C9.9 5.8 8.8 8.6 8.8 12s1.1 6.2 3.2 8.5" />
    </svg>
  );
}

function TodayIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M7 3v3M17 3v3M4 8h16M5 5h14a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1Zm7 6v4l3 2" />
    </svg>
  );
}

export function GlobalTopbar() {
  const { t } = useTranslation('common');

  return (
    <header className="home-topbar" data-home-region="topbar">
      <div className="home-topbar-left">
        <div
          className="home-topbar-brand home-m1-brand"
          aria-label={t(($) => $.common.home.topbar.brandLabel)}
        >
          <img className="home-m1-brand-symbol" src={danteSymbolUrl} alt="" aria-hidden="true" />
          <span
            className="home-m1-brand-wordmark"
            aria-hidden="true"
            dangerouslySetInnerHTML={{ __html: danteWordmarkWhite }}
          />
        </div>

        <button
          className="home-topbar-search"
          type="button"
          disabled
          aria-label={t(($) => $.common.home.topbar.search)}
          data-home-control="search"
        >
          <SearchIcon />
          <span>{t(($) => $.common.home.topbar.search)}</span>
          <kbd>⌘K</kbd>
        </button>
      </div>

      <nav aria-label={t(($) => $.common.home.topbar.navigationLabel)}>
        <span aria-current="page">
          <HomeIcon />
          {t(($) => $.common.home.topbar.home)}
        </span>
        <span>
          <WorldsIcon />
          {t(($) => $.common.home.topbar.worlds)}
        </span>
        <span>
          <TodayIcon />
          {t(($) => $.common.home.topbar.today)}
        </span>
      </nav>

      <div className="home-topbar-utilities">
        <button
          className="home-topbar-create"
          type="button"
          disabled
          data-home-control="create"
          aria-label={t(($) => $.common.home.topbar.create)}
        >
          <span className="home-m1-plus" aria-hidden="true">+</span>
          <span className="home-topbar-create-label">
            {t(($) => $.common.home.topbar.create)}
          </span>
        </button>

        <button
          className="home-topbar-review"
          type="button"
          disabled
          data-home-control="review"
          aria-label={t(($) => $.common.home.topbar.review)}
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M5 4h14a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1Zm3 8 2.2 2.2L16 8.5" />
          </svg>
          <span className="home-m1-review-label">{t(($) => $.common.home.topbar.review)}</span>
          <span className="home-m1-review-badge" aria-hidden="true">3</span>
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
          <span className="home-m1-avatar" aria-hidden="true">MR</span>
        </button>
      </div>
    </header>
  );
}
