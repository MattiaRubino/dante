import type { QueryClient } from '@tanstack/react-query';
import {
  Outlet,
  createRootRouteWithContext,
  useMatches,
} from '@tanstack/react-router';

import { RouteObserver } from '../platform/observability';

type WebRouterContext = Readonly<{
  queryClient: QueryClient;
}>;

export const Route = createRootRouteWithContext<WebRouterContext>()({
  component: RootLayout,
});

function RootLayout() {
  const matches = useMatches();
  const routeId = matches.at(-1)?.routeId ?? 'unknown';

  return (
    <>
      <RouteObserver routeId={routeId} />
      <Outlet />
    </>
  );
}
