import { createFileRoute } from '@tanstack/react-router';

import { authSessionQueryOptions } from '../features/access/application/auth-session';
import { AccessPage } from '../features/access';

export const Route = createFileRoute('/')({
  loader: ({ context }) =>
    context.queryClient.prefetchQuery(authSessionQueryOptions()),
  component: AccessPage,
});
