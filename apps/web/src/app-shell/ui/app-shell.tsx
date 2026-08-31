import { Outlet, useRouterState } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import './app-shell.css';
import './app-shell-theme.css';
import './app-shell-p1-polish.css';
import './app-shell-world-focus.css';
import { GlobalTopbar } from './global-topbar';

function hasWorldFocusMatch(
  matches: readonly Readonly<{
    routeId: string;
    search: unknown;
  }>[],
) {
  return matches.some((match) => {
    if (match.routeId !== '/_app/home' && match.routeId !== '/_app/worlds') {
      return false;
    }

    const search =
      typeof match.search === 'object' && match.search !== null
        ? (match.search as Record<string, unknown>)
        : undefined;

    return typeof search?.focus === 'string';
  });
}

export function AppShell() {
  const { t } = useTranslation('common');
  const isWorldFocus = useRouterState({
    select: (state) => hasWorldFocusMatch(state.matches),
  });

  return (
    <div
      className="app-shell"
      data-app-region="shell"
      data-app-surface={isWorldFocus ? 'world-focus' : 'standard'}
    >
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
