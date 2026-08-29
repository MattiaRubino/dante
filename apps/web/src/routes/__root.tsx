import type { QueryClient } from '@tanstack/react-query';
import { Outlet, createRootRouteWithContext } from '@tanstack/react-router';

import type { RecoveryProofStore } from '../platform/auth/recovery-proof';

type WebRouterContext = Readonly<{
  queryClient: QueryClient;
  recoveryProofStore: RecoveryProofStore;
}>;

export const Route = createRootRouteWithContext<WebRouterContext>()({
  component: RootLayout,
});

function RootLayout() {
  return <Outlet />;
}
