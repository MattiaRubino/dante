import { Link } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

import { LAUNCHER_DESTINATIONS } from '../model/navigation';
import { HomeIcon, TodayIcon, WorldsIcon } from './icons';

const DESTINATION_ICONS = {
  home: HomeIcon,
  worlds: WorldsIcon,
  today: TodayIcon,
} as const;

type LauncherMenuContentProps = {
  onSelect: () => void;
};

export function LauncherMenuContent({ onSelect }: LauncherMenuContentProps) {
  const { t } = useTranslation('common');

  return (
    <div className="app-menu-content app-launcher-menu-content">
      <header className="app-menu-heading">
        <span className="app-dialog-kicker">
          {t(($) => $.common.shell.launcher.kicker)}
        </span>
        <strong>{t(($) => $.common.shell.launcher.title)}</strong>
        <small>{t(($) => $.common.shell.launcher.description)}</small>
      </header>

      <div className="app-launcher-grid" role="none">
        {LAUNCHER_DESTINATIONS.map((destination) => {
          const Icon = DESTINATION_ICONS[destination.id];
          const label = t(
            ($) => $.common.shell.destinations[destination.id].label,
          );

          return (
            <Link
              key={destination.id}
              to={destination.to}
              role="menuitem"
              className="app-launcher-item"
              onClick={onSelect}
            >
              <Icon />
              <span>{label}</span>
            </Link>
          );
        })}
      </div>
    </div>
  );
}
