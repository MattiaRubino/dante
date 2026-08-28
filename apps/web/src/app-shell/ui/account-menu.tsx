import { Link } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { SettingsIcon, UserIcon } from './icons';

type AccountMenuContentProps = {
  onSelect: () => void;
};

export function AccountMenuContent({ onSelect }: AccountMenuContentProps) {
  const { t } = useTranslation('common');

  return (
    <div className="app-menu-content app-account-menu-content">
      <header className="app-account-card">
        <span className="app-account-avatar" aria-hidden="true">MR</span>
        <span>
          <strong>{t(($) => $.common.shell.account.title)}</strong>
          <small>{t(($) => $.common.shell.account.identityUnavailable)}</small>
        </span>
      </header>

      <div className="app-menu-list" role="none">
        <Link
          to="/profile"
          role="menuitem"
          className="app-menu-item"
          onClick={onSelect}
        >
          <UserIcon />
          <span>{t(($) => $.common.shell.account.profile)}</span>
        </Link>
        <Link
          to="/settings"
          role="menuitem"
          className="app-menu-item"
          onClick={onSelect}
        >
          <SettingsIcon />
          <span>{t(($) => $.common.shell.account.settings)}</span>
        </Link>
      </div>

      <div className="app-account-meta" role="none">
        <span>
          <small>{t(($) => $.common.shell.account.language)}</small>
          <strong>{t(($) => $.common.shell.account.languageValue)}</strong>
        </span>
      </div>

      <div className="app-menu-separator" role="separator" />

      <button
        type="button"
        role="menuitem"
        className="app-menu-item app-account-logout is-unavailable"
        aria-disabled="true"
        aria-describedby="app-account-logout-reason"
        onClick={(event) => event.preventDefault()}
      >
        <span>{t(($) => $.common.shell.account.logout)}</span>
        <small id="app-account-logout-reason">
          {t(($) => $.common.shell.account.logoutUnavailable)}
        </small>
      </button>
    </div>
  );
}
