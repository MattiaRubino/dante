import { createFileRoute } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { AppPlaceholderPage } from '../app-shell';

export const Route = createFileRoute('/_app/profile')({
  component: ProfilePage,
});

function ProfilePage() {
  const { t } = useTranslation('common');

  return (
    <AppPlaceholderPage
      eyebrow={t(($) => $.common.shell.placeholder.eyebrow)}
      title={t(($) => $.common.shell.destinations.profile.label)}
      description={t(($) => $.common.shell.placeholder.profile)}
      status={t(($) => $.common.shell.placeholder.status)}
    />
  );
}
