import { useTranslation } from 'react-i18next';

import type { AccessCondition } from '../model/access-flow';

export function AccessConditionNotice({
  condition,
}: Readonly<{ condition: AccessCondition }>) {
  const { t } = useTranslation('common');

  if (condition.kind === 'idle') {
    return null;
  }

  const title =
    condition.kind === 'offline'
      ? t(($) => $.common.access.network.offlineTitle)
      : condition.kind === 'rate-limited'
        ? t(($) => $.common.access.network.rateLimitedTitle)
        : condition.kind === 'server-unavailable'
          ? t(($) => $.common.access.network.serverUnavailableTitle)
          : t(($) => $.common.access.integration.title);

  const body =
    condition.kind === 'offline'
      ? t(($) => $.common.access.network.offlineBody)
      : condition.kind === 'rate-limited'
        ? t(($) => $.common.access.network.rateLimitedBody)
        : condition.kind === 'server-unavailable'
          ? t(($) => $.common.access.network.serverUnavailableBody)
          : t(($) => $.common.access.integration.body);

  return (
    <div className="access-condition-notice" role="status" aria-live="polite">
      <strong>{title}</strong>
      <span>{body}</span>
    </div>
  );
}
