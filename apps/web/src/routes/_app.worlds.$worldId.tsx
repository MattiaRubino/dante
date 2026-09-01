import { Navigate, createFileRoute } from '@tanstack/react-router';

import {
  getWorldFocusWorld,
  normalizeWorldFocusId,
  readWorldFocusEntry,
  WorldFocusPage,
  WorldFocusRouteError,
  type WorldFocusCloseRequest,
  type WorldFocusEntrySource,
} from '../features/world-focus';

export const Route = createFileRoute('/_app/worlds/$worldId')({
  component: WorldFocusRoute,
  errorComponent: WorldFocusRouteError,
});

function WorldFocusRoute() {
  const { worldId } = Route.useParams();
  const navigate = Route.useNavigate();
  const normalizedWorldId = normalizeWorldFocusId(worldId);
  const world =
    normalizedWorldId === undefined
      ? undefined
      : getWorldFocusWorld(normalizedWorldId);

  if (world === undefined) {
    return <Navigate to="/worlds" replace />;
  }

  const source: WorldFocusEntrySource =
    readWorldFocusEntry(world.id, 'home') !== null
      ? 'home'
      : readWorldFocusEntry(world.id, 'worlds') !== null
        ? 'worlds'
        : 'worlds';

  const closeWorldFocus = ({ preferHistory }: WorldFocusCloseRequest) => {
    if (preferHistory && typeof window !== 'undefined') {
      window.history.back();
      return;
    }

    void navigate({
      to: '/worlds',
      replace: true,
      resetScroll: false,
    });
  };

  return <WorldFocusPage world={world} source={source} onClose={closeWorldFocus} />;
}
