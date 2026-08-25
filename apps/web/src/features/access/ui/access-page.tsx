import { useEffect, useReducer } from 'react';

import danteSymbolUrl from '../../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkUrl from '../../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?url';
import {
  accessFlowReducer,
  initialAccessFlowState,
} from '../model/access-flow';
import { AccessBrandStage } from './access-brand-stage';
import { AccessFlowPanel } from './access-flow-panel';
import { AccessLocaleSwitcher } from './access-locale-switcher';
import '../access.css';
import '../access-composition.css';
import '../access-flow.css';

export function AccessPage() {
  const [flow, dispatch] = useReducer(
    accessFlowReducer,
    initialAccessFlowState,
  );

  useEffect(() => {
    const goOffline = () => dispatch({ type: 'NETWORK_OFFLINE' });
    const goOnline = () => dispatch({ type: 'NETWORK_ONLINE' });

    if (!window.navigator.onLine) {
      goOffline();
    }

    window.addEventListener('offline', goOffline);
    window.addEventListener('online', goOnline);

    return () => {
      window.removeEventListener('offline', goOffline);
      window.removeEventListener('online', goOnline);
    };
  }, []);

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
          <AccessFlowPanel flow={flow} dispatch={dispatch} />
        </div>
      </main>
    </div>
  );
}
