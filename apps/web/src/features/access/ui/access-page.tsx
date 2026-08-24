import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';
import { AccessBrandStage } from './access-brand-stage';
import { AccessSignInPanel } from './access-sign-in-panel';
import '../access.css';
import '../access-composition.css';

export function AccessPage() {
  const { i18n } = useTranslation();
  const localeName = i18n.resolvedLanguage?.toLowerCase().startsWith('en')
    ? 'English'
    : 'Italiano';

  return (
    <div className="access-shell">
      <header className="access-topbar">
        <div className="access-brand-lockup">
          <img
            className="access-brand-symbol"
            src={danteSymbolUrl}
            alt=""
            aria-hidden="true"
          />
          <img
            className="access-brand-wordmark"
            src={danteWordmarkUrl}
            alt="DANTE"
          />
        </div>

        <button
          className="access-locale-button"
          type="button"
          aria-label={`Lingua: ${localeName}`}
        >
          <svg
            className="access-locale-globe"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            focusable="false"
            aria-hidden="true"
          >
            <circle cx="12" cy="12" r="9" />
            <path d="M3.5 9h17M3.5 15h17M12 3c2.2 2.6 3.3 5.6 3.3 9S14.2 18.4 12 21M12 3C9.8 5.6 8.7 8.6 8.7 12S9.8 18.4 12 21" />
          </svg>
          <span className="access-locale-name">{localeName}</span>
          <svg
            className="access-locale-chevron"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            focusable="false"
            aria-hidden="true"
          >
            <path d="m7 10 5 5 5-5" />
          </svg>
        </button>
      </header>

      <main className="access-main">
        <div className="access-frame">
          <AccessBrandStage />
          <AccessSignInPanel />
        </div>
      </main>
    </div>
  );
}
