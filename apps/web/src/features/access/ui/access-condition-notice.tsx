import { useTranslation } from 'react-i18next';

import type { AccessCondition } from '../model/access-flow';

export function AccessConditionNotice({
  condition,
}: Readonly<{ condition: AccessCondition }>) {
  const { t } = useTranslation('common');

  if (condition.kind === 'idle' || condition.kind === 'backend-required') {
    return null;
  }

  let title: string;
  let body: string;

  switch (condition.kind) {
    case 'offline':
      title = t(($) => $.common.access.network.offlineTitle);
      body = t(($) => $.common.access.network.offlineBody);
      break;
    case 'rate-limited':
      title = t(($) => $.common.access.network.rateLimitedTitle);
      body = t(($) => $.common.access.network.rateLimitedBody);
      break;
    case 'server-unavailable':
      title = t(($) => $.common.access.network.serverUnavailableTitle);
      body = t(($) => $.common.access.network.serverUnavailableBody);
      break;
    case 'invalid-credentials':
      title = t(($) => $.common.access.failure.invalidCredentialsTitle);
      body = t(($) => $.common.access.failure.invalidCredentialsBody);
      break;
    case 'account-unavailable':
      title = t(($) => $.common.access.failure.accountUnavailableTitle);
      body = t(($) => $.common.access.failure.accountUnavailableBody);
      break;
    case 'password-compromised':
      title = t(($) => $.common.access.failure.passwordCompromisedTitle);
      body = t(($) => $.common.access.failure.passwordCompromisedBody);
      break;
    case 'request-invalid':
      title = t(($) => $.common.access.failure.requestInvalidTitle);
      body = t(($) => $.common.access.failure.requestInvalidBody);
      break;
    case 'unexpected':
      title = t(($) => $.common.access.failure.unexpectedTitle);
      body = t(($) => $.common.access.failure.unexpectedBody);
      break;
  }

  return (
    <div className="access-condition-notice" role="status" aria-live="polite">
      <strong>{title}</strong>
      <span>{body}</span>
    </div>
  );
}
