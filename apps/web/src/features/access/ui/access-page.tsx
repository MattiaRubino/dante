import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';
import { AccessBrandStage } from './access-brand-stage';
import { AccessLocaleSwitcher } from './access-locale-switcher';
import { AccessSignInPanel } from './access-sign-in-panel';
import '../access.css';
import '../access-composition.css';

export function AccessPage() {
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

        <AccessLocaleSwitcher />
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
