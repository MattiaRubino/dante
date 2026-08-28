import { useTranslation } from 'react-i18next';

import { CREATE_CAPABILITIES } from '../model/create-capabilities';
import { CalendarIcon, CaptureIcon, TaskIcon } from './icons';

const CAPABILITY_ICONS = {
  event: CalendarIcon,
  task: TaskIcon,
  capture: CaptureIcon,
} as const;

type CreateMenuContentProps = {
  onDeferredAction?: (capabilityId: string) => void;
};

export function CreateMenuContent({ onDeferredAction }: CreateMenuContentProps) {
  const { t } = useTranslation('common');

  return (
    <div className="app-menu-content app-create-menu-content">
      <header className="app-menu-heading">
        <span className="app-dialog-kicker">
          {t(($) => $.common.shell.create.kicker)}
        </span>
        <strong>{t(($) => $.common.shell.create.title)}</strong>
        <small>{t(($) => $.common.shell.create.description)}</small>
      </header>

      <div className="app-menu-list" role="none">
        {CREATE_CAPABILITIES.map((capability) => {
          const Icon = CAPABILITY_ICONS[capability.id];
          const label = t(($) => $.common.shell.create.items[capability.id].label);
          const description = t(
            ($) => $.common.shell.create.items[capability.id].description,
          );
          const reasonId = `app-create-${capability.id}-reason`;

          return (
            <button
              key={capability.id}
              type="button"
              role="menuitem"
              disabled
              aria-describedby={reasonId}
              className="app-menu-item app-menu-item-rich is-unavailable"
              onClick={() => onDeferredAction?.(capability.id)}
            >
              <span className="app-menu-item-icon" aria-hidden="true">
                <Icon />
              </span>
              <span className="app-menu-item-copy">
                <strong>{label}</strong>
                <small>{description}</small>
                <em id={reasonId}>{t(($) => $.common.shell.create.deferred)}</em>
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
