import { createFileRoute } from '@tanstack/react-router';

import { AccessPage, authSessionQueryOptions } from '../features/access';

export const Route = createFileRoute('/')({
  loader: ({ context }) =>
    context.queryClient.prefetchQuery(authSessionQueryOptions()),
  component: AccessPage,
});
