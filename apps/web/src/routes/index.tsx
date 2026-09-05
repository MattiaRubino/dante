import { createFileRoute } from '@tanstack/react-router';

import { AccessPage, authSessionQueryOptions } from '../features/access';

export const Route = createFileRoute('/')({
  loader: ({ context }) =>
    context.queryClient.prefetchQuery(authSessionQueryOptions()),
  component: AccessRoute,
});

function AccessRoute() {
  const { recoveryProofStore } = Route.useRouteContext();
  return <AccessPage recoveryProofStore={recoveryProofStore} />;
}
