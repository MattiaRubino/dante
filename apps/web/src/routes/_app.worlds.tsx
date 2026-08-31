import { Outlet, createFileRoute, useRouterState } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { AppPlaceholderPage } from '../app-shell';

export const Route = createFileRoute('/_app/worlds')({
  component: WorldsRoute,
});

function WorldsRoute() {
  const { t } = useTranslation('common');
  const hasWorldFocusChild = useRouterState({
    select: (state) =>
      state.matches.some(
        (match) => match.routeId === '/_app/worlds/$worldId',
      ),
  });

  if (hasWorldFocusChild) {
    return <Outlet />;
  }

  return (
    <AppPlaceholderPage
      eyebrow={t(($) => $.common.shell.placeholder.eyebrow)}
      title={t(($) => $.common.shell.destinations.worlds.label)}
      description={t(($) => $.common.shell.placeholder.worlds)}
      status={t(($) => $.common.shell.placeholder.status)}
    />
  );
}
