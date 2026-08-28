import { createFileRoute } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { AppPlaceholderPage } from '../app-shell';

export const Route = createFileRoute('/_app/worlds')({
  component: WorldsPage,
});

function WorldsPage() {
  const { t } = useTranslation('common');

  return (
    <AppPlaceholderPage
      eyebrow={t(($) => $.common.shell.placeholder.eyebrow)}
      title={t(($) => $.common.shell.destinations.worlds.label)}
      description={t(($) => $.common.shell.placeholder.worlds)}
      status={t(($) => $.common.shell.placeholder.status)}
    />
  );
}
