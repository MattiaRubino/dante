import { createFileRoute } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { AppPlaceholderPage } from '../app-shell';

export const Route = createFileRoute('/_app/settings')({
  component: SettingsPage,
});

function SettingsPage() {
  const { t } = useTranslation('common');

  return (
    <AppPlaceholderPage
      eyebrow={t(($) => $.common.shell.placeholder.eyebrow)}
      title={t(($) => $.common.shell.destinations.settings.label)}
      description={t(($) => $.common.shell.placeholder.settings)}
      status={t(($) => $.common.shell.placeholder.status)}
    />
  );
}
