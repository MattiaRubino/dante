import { useEffect } from 'react';
import { Navigate, createFileRoute } from '@tanstack/react-router';

import {
  getWorldFocusWorld,
  normalizeWorldFocusId,
  normalizeWorldFocusTimePreset,
  readWorldFocusEntry,
  resolveWorldFocusTimePreset,
  WorldFocusPage,
  WorldFocusRouteError,
  type WorldFocusCloseRequest,
  type WorldFocusEntrySource,
  type WorldFocusTimePreset,
} from '../features/world-focus';

type WorldFocusRouteSearch = Readonly<{
  time?: WorldFocusTimePreset;
}>;

export const Route = createFileRoute('/_app/worlds/$worldId')({
  validateSearch: (search: Record<string, unknown>): WorldFocusRouteSearch => {
    const time = normalizeWorldFocusTimePreset(search.time);
    return time === undefined ? {} : { time };
  },
  component: WorldFocusRoute,
  errorComponent: WorldFocusRouteError,
});

function WorldFocusRoute() {
  const { worldId } = Route.useParams();
  const { time: requestedTimePreset } = Route.useSearch();
  const navigate = Route.useNavigate();
  const normalizedWorldId = normalizeWorldFocusId(worldId);
  const world =
    normalizedWorldId === undefined
      ? undefined
      : getWorldFocusWorld(normalizedWorldId);
  const effectiveTimePreset = resolveWorldFocusTimePreset(
    world?.lens?.time,
    requestedTimePreset,
  );

  useEffect(() => {
    if (
      world === undefined ||
      requestedTimePreset === undefined ||
      effectiveTimePreset === requestedTimePreset
    ) {
      return;
    }

    void navigate({
      search: {},
      replace: true,
      resetScroll: false,
    });
  }, [effectiveTimePreset, navigate, requestedTimePreset, world]);

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

  const changeTimePreset = (preset: WorldFocusTimePreset) => {
    const capability = world.lens?.time;
    const currentPreset = resolveWorldFocusTimePreset(
      capability,
      requestedTimePreset,
    );

    if (
      capability === undefined ||
      !capability.presets.includes(preset) ||
      preset === currentPreset
    ) {
      return;
    }

    void navigate({
      search: preset === capability.defaultPreset ? {} : { time: preset },
      replace: false,
      resetScroll: false,
    });
  };

  return (
    <WorldFocusPage
      world={world}
      source={source}
      {...(requestedTimePreset === undefined ? {} : { requestedTimePreset })}
      onTimePresetChange={changeTimePreset}
      onClose={closeWorldFocus}
    />
  );
}
