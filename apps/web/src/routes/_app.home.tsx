import { createFileRoute } from '@tanstack/react-router';

import { HomePage } from '../features/home';
import { normalizeHomeDateSearch } from '../features/home/model/day-context';

type HomeSearch = Readonly<{
  date?: string;
}>;

export const Route = createFileRoute('/_app/home')({
  validateSearch: (search: Record<string, unknown>): HomeSearch => {
    const date = normalizeHomeDateSearch(search.date);
    return date === undefined ? {} : { date };
  },
  component: HomeRoute,
});

function HomeRoute() {
  const search = Route.useSearch();
  const navigate = Route.useNavigate();

  const onViewedDateChange = (isoDate: string | undefined) => {
    void navigate({
      search: isoDate === undefined ? {} : { date: isoDate },
    });
  };

  return (
    <HomePage
      viewedDateIso={search.date}
      onViewedDateChange={onViewedDateChange}
    />
  );
}
