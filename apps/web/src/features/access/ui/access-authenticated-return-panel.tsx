import { Link } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import type { AccessCondition } from '../model/access-flow';
import { AccessConditionNotice } from './access-condition-notice';
import { AccessPanelFrame } from './access-panel-frame';

type AccessAuthenticatedReturnPanelProps = Readonly<{
  condition: AccessCondition;
  onLogOut: () => void;
  pending?: boolean;
}>;

export function AccessAuthenticatedReturnPanel({
  condition,
  onLogOut,
  pending = false,
}: AccessAuthenticatedReturnPanelProps) {
  const { t } = useTranslation('common');

  return (
    <AccessPanelFrame
      titleId="access-authenticated-return-title"
      kicker={t(($) => $.common.access.kicker.access)}
      title={t(($) => $.common.access.authenticated.title)}
      body={t(($) => $.common.access.authenticated.body)}
    >
      <div className="access-completion-mark" aria-hidden="true">
        ✓
      </div>
      <Link
        className="access-primary-button access-security-link"
        to="/security"
      >
        {t(($) => $.common.access.security.title)}
      </Link>
      <button
        className="access-secondary-button"
        type="button"
        onClick={onLogOut}
        disabled={pending}
        aria-busy={pending}
      >
        {t(($) => $.common.access.action.logout)}
      </button>
      <AccessConditionNotice condition={condition} />
    </AccessPanelFrame>
  );
}
