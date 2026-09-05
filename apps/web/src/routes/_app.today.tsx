import { createFileRoute } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { AppPlaceholderPage } from '../app-shell';

export const Route = createFileRoute('/_app/today')({
  component: TodayPage,
});

function TodayPage() {
  const { t } = useTranslation('common');

  return (
    <AppPlaceholderPage
      eyebrow={t(($) => $.common.shell.placeholder.eyebrow)}
      title={t(($) => $.common.shell.destinations.today.label)}
      description={t(($) => $.common.shell.placeholder.today)}
      status={t(($) => $.common.shell.placeholder.status)}
    />
  );
}
