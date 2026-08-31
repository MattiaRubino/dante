import { createFileRoute } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { AppPlaceholderPage } from '../app-shell';
import {
  getWorldFocusWorld,
  normalizeWorldFocusId,
  WorldFocusPage,
  type WorldFocusCloseRequest,
  type WorldFocusId,
} from '../features/world-focus';

type WorldsSearch = Readonly<{
  focus?: WorldFocusId;
}>;

export const Route = createFileRoute('/_app/worlds')({
  validateSearch: (search: Record<string, unknown>): WorldsSearch => {
    const focus = normalizeWorldFocusId(search.focus);
    return focus === undefined ? {} : { focus };
  },
  component: WorldsPage,
});

function WorldsPage() {
  const { t } = useTranslation('common');
  const search = Route.useSearch();
  const navigate = Route.useNavigate();
  const focusedWorld =
    search.focus === undefined ? undefined : getWorldFocusWorld(search.focus);

  const closeWorldFocus = ({ preferHistory }: WorldFocusCloseRequest) => {
    if (preferHistory && typeof window !== 'undefined') {
      window.history.back();
      return;
    }

    void navigate({
      search: {},
      replace: true,
      resetScroll: false,
    });
  };

  return (
    <>
      <div
        data-world-focus-underlay="worlds"
        inert={focusedWorld === undefined ? undefined : true}
        aria-hidden={focusedWorld === undefined ? undefined : true}
      >
        <AppPlaceholderPage
          eyebrow={t(($) => $.common.shell.placeholder.eyebrow)}
          title={t(($) => $.common.shell.destinations.worlds.label)}
          description={t(($) => $.common.shell.placeholder.worlds)}
          status={t(($) => $.common.shell.placeholder.status)}
        />
      </div>

      {focusedWorld === undefined ? null : (
        <WorldFocusPage
          world={focusedWorld}
          source="worlds"
          onClose={closeWorldFocus}
        />
      )}
    </>
  );
}
