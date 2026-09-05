import { createFileRoute } from '@tanstack/react-router';

import { HomePage, type HomeWorldOpenIntent } from '../features/home';
import {
  HOME_PROTOTYPE_IDENTITY_FIXTURE,
  normalizeHomeDateSearch,
} from '../features/home/route-contract';
import {
  primeWorldFocusEntry,
  resolveWorldFocusWorldByLabel,
} from '../features/world-focus';

type HomeSearch = Readonly<{
  date?: string;
}>;

function createHomeSearch(date: string | undefined): HomeSearch {
  return date === undefined ? {} : { date };
}

export const Route = createFileRoute('/_app/home')({
  validateSearch: (search: Record<string, unknown>): HomeSearch =>
    createHomeSearch(normalizeHomeDateSearch(search.date)),
  component: HomeRoute,
});

function HomeRoute() {
  const search = Route.useSearch();
  const navigate = Route.useNavigate();

  const onViewedDateChange = (isoDate: string | undefined) => {
    void navigate({
      search: createHomeSearch(isoDate),
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
      to: '/worlds/$worldId',
      params: { worldId: world.id },
      resetScroll: false,
    });
  };

  return (
    <HomePage
      viewedDateIso={search.date}
      preferredName={HOME_PROTOTYPE_IDENTITY_FIXTURE.preferredName}
      onViewedDateChange={onViewedDateChange}
      onOpenWorldFocus={onOpenWorldFocus}
    />
  );
}
