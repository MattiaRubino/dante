import { createFileRoute } from '@tanstack/react-router';

import {
  AccessSecurityPage,
  authSessionQueryOptions,
} from '../features/access';

export const Route = createFileRoute('/security')({
  loader: ({ context }) =>
    context.queryClient.prefetchQuery(authSessionQueryOptions()),
  component: AccessSecurityPage,
});
