import { useTranslation } from 'react-i18next';

import type { AccessCondition } from '../model/access-flow';

export function AccessConditionNotice({
  condition,
}: Readonly<{ condition: AccessCondition }>) {
  const { t } = useTranslation('common');

  if (condition.kind === 'idle' || condition.kind === 'backend-required') {
    return null;
  }

  const title =
    condition.kind === 'offline'
      ? t(($) => $.common.access.network.offlineTitle)
      : condition.kind === 'rate-limited'
        ? t(($) => $.common.access.network.rateLimitedTitle)
        : t(($) => $.common.access.network.serverUnavailableTitle);

  const body =
    condition.kind === 'offline'
      ? t(($) => $.common.access.network.offlineBody)
      : condition.kind === 'rate-limited'
        ? t(($) => $.common.access.network.rateLimitedBody)
        : t(($) => $.common.access.network.serverUnavailableBody);

  return (
    <div className="access-condition-notice" role="status" aria-live="polite">
      <strong>{title}</strong>
      <span>{body}</span>
    </div>
  );
}
