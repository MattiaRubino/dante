import { Outlet } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import './app-shell.css';
import { GlobalTopbar } from './ui/global-topbar';

export function AppShell() {
  const { t } = useTranslation('common');

  return (
    <div className="app-shell" data-app-region="shell">
      <a className="app-skip-link" href="#app-route-content">
        {t(($) => $.common.shell.actions.skipToContent)}
      </a>
      <GlobalTopbar />
      <div id="app-route-content" className="app-shell-route" tabIndex={-1}>
        <Outlet />
      </div>
    </div>
  );
}
