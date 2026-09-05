import { useEffect } from 'react';

import { observeResolvedRoute } from './bridge';

type RouteObserverProps = Readonly<{
  routeId: string;
}>;

export function RouteObserver({ routeId }: RouteObserverProps) {
  useEffect(() => {
    observeResolvedRoute(routeId);
  }, [routeId]);

  return null;
}
