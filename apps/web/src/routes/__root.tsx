import type { QueryClient } from '@tanstack/react-query';
import {
  Outlet,
  createRootRouteWithContext,
  useMatches,
} from '@tanstack/react-router';

import type { RecoveryProofStore } from '../platform/auth/recovery-proof';
import { RouteObserver } from '../platform/observability';

type WebRouterContext = Readonly<{
  queryClient: QueryClient;
  recoveryProofStore: RecoveryProofStore;
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
