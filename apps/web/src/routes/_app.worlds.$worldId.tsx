import { Navigate, createFileRoute } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import {
  createWorldFocusIdentityDescriptor,
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
  const { t } = useTranslation('common');
  const { worldId } = Route.useParams();
  const navigate = Route.useNavigate();
  const normalizedWorldId = normalizeWorldFocusId(worldId);
  const world =
    normalizedWorldId === undefined
      ? undefined
      : getWorldFocusWorld(normalizedWorldId);

  // Opaque production identity is open-ended, but routability is not. Until a
  // real application resolver replaces the deterministic fixture catalog, an
  // arbitrary URL token does not create a World by itself.
  if (world === undefined) {
    return <Navigate to="/worlds" replace />;
  }

  const identity = createWorldFocusIdentityDescriptor({
    id: world.id,
    label: t(($) => $.common.worldFocus.worlds[world.id].label),
    description: t(($) => $.common.worldFocus.worlds[world.id].description),
  });

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

  return (
    <WorldFocusPage
      world={world}
      identity={identity}
      source={source}
      onClose={closeWorldFocus}
    />
  );
}
