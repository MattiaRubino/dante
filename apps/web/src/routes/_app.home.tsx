import { createFileRoute } from '@tanstack/react-router';

import { HomePage, type HomeWorldOpenIntent } from '../features/home';
import {
  HOME_PROTOTYPE_IDENTITY_FIXTURE,
  normalizeHomeDateSearch,
} from '../features/home/route-contract';
import {
  getWorldFocusWorld,
  normalizeWorldFocusId,
  primeWorldFocusEntry,
  resolveWorldFocusWorldByLabel,
  WorldFocusPage,
  type WorldFocusCloseRequest,
  type WorldFocusId,
} from '../features/world-focus';

type HomeSearch = Readonly<{
  date?: string;
  focus?: WorldFocusId;
}>;

function createHomeSearch(
  date: string | undefined,
  focus: WorldFocusId | undefined,
): HomeSearch {
  return {
    ...(date === undefined ? {} : { date }),
    ...(focus === undefined ? {} : { focus }),
  };
}

export const Route = createFileRoute('/_app/home')({
  validateSearch: (search: Record<string, unknown>): HomeSearch => {
    const date = normalizeHomeDateSearch(search.date);
    const focus = normalizeWorldFocusId(search.focus);
    return createHomeSearch(date, focus);
  },
  component: HomeRoute,
});

function HomeRoute() {
  const search = Route.useSearch();
  const navigate = Route.useNavigate();
  const focusedWorld =
    search.focus === undefined ? undefined : getWorldFocusWorld(search.focus);

  const onViewedDateChange = (isoDate: string | undefined) => {
    void navigate({
      search: createHomeSearch(isoDate, search.focus),
      resetScroll: false,
    });
  };

  const onOpenWorldFocus = (intent: HomeWorldOpenIntent) => {
    const world = resolveWorldFocusWorldByLabel(intent.label);
    if (world === undefined) {
      return;
    }

    primeWorldFocusEntry({
      worldId: world.id,
      source: 'home',
      origin: intent.origin,
    });

    void navigate({
      search: createHomeSearch(search.date, world.id),
      resetScroll: false,
    });
  };

  const closeWorldFocus = ({ preferHistory }: WorldFocusCloseRequest) => {
    if (preferHistory && typeof window !== 'undefined') {
      window.history.back();
      return;
    }

    void navigate({
      search: createHomeSearch(search.date, undefined),
      replace: true,
      resetScroll: false,
    });
  };

  return (
    <>
      <div
        data-world-focus-underlay="home"
        inert={focusedWorld === undefined ? undefined : true}
        aria-hidden={focusedWorld === undefined ? undefined : true}
      >
        <HomePage
          viewedDateIso={search.date}
          preferredName={HOME_PROTOTYPE_IDENTITY_FIXTURE.preferredName}
          onViewedDateChange={onViewedDateChange}
          onOpenWorldFocus={onOpenWorldFocus}
        />
      </div>

      {focusedWorld === undefined ? null : (
        <WorldFocusPage
          world={focusedWorld}
          source="home"
          onClose={closeWorldFocus}
        />
      )}
    </>
  );
}
