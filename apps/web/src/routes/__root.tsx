import type { QueryClient } from '@tanstack/react-query';
import { Outlet, createRootRouteWithContext } from '@tanstack/react-router';

type WebRouterContext = Readonly<{
  queryClient: QueryClient;
}>;

export const Route = createRootRouteWithContext<WebRouterContext>()({
  component: RootLayout,
});

function RootLayout() {
  return <Outlet />;
}
