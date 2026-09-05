import { Link } from '@tanstack/react-router';
import { useEffect, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import danteSymbolUrl from '../../../../../assets/brand/logo/master/dante-symbol-master-v0.svg?url';
import danteWordmarkRaw from '../../../../../assets/brand/wordmark/master/dante-wordmark-master-v0.svg?raw';
import { PRIMARY_DESTINATIONS } from '../model/navigation';
import { AccountMenuContent } from './account-menu';
import { CreateMenuContent } from './create-menu';
import {
  HomeIcon,
  ReviewIcon,
  SearchIcon,
  TodayIcon,
  UserIcon,
  WorldsIcon,
} from './icons';
import { LauncherMenuContent } from './launcher-menu';
import { MenuPopover } from './primitives/menu-popover';
import { TopbarSearchSurface } from './topbar-search-surface';

const DESTINATION_ICONS = {
  home: HomeIcon,
  worlds: WorldsIcon,
  today: TodayIcon,
} as const;

type OpenMenu = 'create' | 'launcher' | 'account' | null;

function isEditableShortcutTarget(target: EventTarget | null) {
  if (!(target instanceof HTMLElement)) {
    return false;
  }

  return (
    target.isContentEditable ||
    target.tagName === 'INPUT' ||
    target.tagName === 'TEXTAREA' ||
    target.tagName === 'SELECT'
  );
}

export function GlobalTopbar() {
  const { t } = useTranslation('common');
  const [searchOpen, setSearchOpen] = useState(false);
  const [openMenu, setOpenMenu] = useState<OpenMenu>(null);
  const searchTriggerRef = useRef<HTMLButtonElement>(null);
  const createTriggerRef = useRef<HTMLButtonElement>(null);
  const launcherTriggerRef = useRef<HTMLButtonElement>(null);
  const accountTriggerRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    const handleShortcut = (event: KeyboardEvent) => {
      if (event.repeat) {
        return;
      }

      const key = event.key.toLocaleLowerCase();
      const commandShortcut =
        key === 'k' && (event.metaKey || event.ctrlKey) && !event.altKey;
      const slashShortcut =
        event.key === '/' &&
        !event.metaKey &&
        !event.ctrlKey &&
        !event.altKey &&
        !event.shiftKey &&
        !isEditableShortcutTarget(event.target);

      if (!commandShortcut && !slashShortcut) {
        return;
      }

      event.preventDefault();
      setOpenMenu(null);
      setSearchOpen(true);
    };

    document.addEventListener('keydown', handleShortcut);
    return () => document.removeEventListener('keydown', handleShortcut);
  }, []);

  const closeSearch = (restoreFocus = true) => {
    setSearchOpen(false);
    if (restoreFocus) {
      queueMicrotask(() => searchTriggerRef.current?.focus());
    }
  };

  const toggleSearch = () => {
    setOpenMenu(null);
    if (searchOpen) {
      closeSearch(true);
    } else {
      setSearchOpen(true);
    }
  };

  const toggleMenu = (menu: Exclude<OpenMenu, null>) => {
    setSearchOpen(false);
    setOpenMenu((current) => (current === menu ? null : menu));
  };

  return (
    <header
      className={`app-topbar${searchOpen ? ' is-searching' : ''}`}
      data-app-region="topbar"
      data-search-state={searchOpen ? 'open' : 'closed'}
    >
      <div className="app-topbar-left">
        <Link
          to="/home"
          className="app-topbar-brand"
          aria-label={t(($) => $.common.shell.topbar.brandHomeLabel)}
          onClick={() => setSearchOpen(false)}
        >
          <img
            className="app-topbar-brand-symbol"
            src={danteSymbolUrl}
            alt=""
          />
          <span
            className="app-topbar-brand-wordmark"
            aria-hidden="true"
            dangerouslySetInnerHTML={{ __html: danteWordmarkRaw }}
          />
        </Link>
      </div>

      {searchOpen ? (
        <TopbarSearchSurface onClose={closeSearch} />
      ) : (
        <nav
          className="app-topbar-nav"
          aria-label={t(($) => $.common.shell.topbar.navigationLabel)}
        >
          {PRIMARY_DESTINATIONS.map((destination) => {
            const Icon = DESTINATION_ICONS[destination.id];
            const label = t(
              ($) => $.common.shell.destinations[destination.id].label,
            );

            return (
              <Link
                key={destination.id}
                to={destination.to}
                className="app-topbar-nav-link"
                activeProps={{
                  className: 'app-topbar-nav-link is-active',
                  'aria-current': 'page',
                }}
                onClick={() => setOpenMenu(null)}
              >
                <Icon />
                <span>{label}</span>
              </Link>
            );
          })}
        </nav>
      )}

      <div className="app-topbar-utilities">
        <button
          ref={searchTriggerRef}
          className={`app-topbar-search-trigger${searchOpen ? ' is-active' : ''}`}
          type="button"
          aria-expanded={searchOpen}
          aria-controls={searchOpen ? 'app-search-surface' : undefined}
          aria-label={t(($) => $.common.shell.topbar.searchLabel)}
          onClick={toggleSearch}
        >
          <SearchIcon />
        </button>

        <div className="app-popover-anchor">
          <button
            ref={createTriggerRef}
            className="app-topbar-create"
            type="button"
            aria-haspopup="menu"
            aria-expanded={openMenu === 'create'}
            aria-controls="app-create-menu"
            onClick={() => toggleMenu('create')}
          >
            <span className="app-topbar-plus" aria-hidden="true">
              +
            </span>
            <span className="app-topbar-create-label">
              {t(($) => $.common.shell.topbar.create)}
            </span>
          </button>
          <MenuPopover
            id="app-create-menu"
            label={t(($) => $.common.shell.create.menuLabel)}
            open={openMenu === 'create'}
            onOpenChange={(open) => setOpenMenu(open ? 'create' : null)}
            triggerRef={createTriggerRef}
            className="app-create-menu"
          >
            <CreateMenuContent />
          </MenuPopover>
        </div>

        <button
          className="app-topbar-review"
          type="button"
          disabled
          title={t(($) => $.common.shell.review.legacyHint)}
          aria-label={t(($) => $.common.shell.topbar.review)}
        >
          <ReviewIcon />
          <span className="app-topbar-review-label">
            {t(($) => $.common.shell.topbar.review)}
          </span>
          <span className="app-topbar-review-badge" aria-hidden="true">
            3
          </span>
        </button>

        <div className="app-popover-anchor">
          <button
            ref={launcherTriggerRef}
            className="app-topbar-icon-button"
            type="button"
            aria-haspopup="menu"
            aria-expanded={openMenu === 'launcher'}
            aria-controls="app-launcher-menu"
            aria-label={t(($) => $.common.shell.topbar.launcher)}
            onClick={() => toggleMenu('launcher')}
          >
            <span className="app-topbar-launcher-glyph" aria-hidden="true">
              {Array.from({ length: 9 }, (_, index) => (
                <span key={index} />
              ))}
            </span>
          </button>
          <MenuPopover
            id="app-launcher-menu"
            label={t(($) => $.common.shell.launcher.menuLabel)}
            open={openMenu === 'launcher'}
            onOpenChange={(open) => setOpenMenu(open ? 'launcher' : null)}
            triggerRef={launcherTriggerRef}
            className="app-launcher-menu"
          >
            <LauncherMenuContent onSelect={() => setOpenMenu(null)} />
          </MenuPopover>
        </div>

        <div className="app-popover-anchor">
          <button
            ref={accountTriggerRef}
            className="app-topbar-account"
            type="button"
            aria-haspopup="menu"
            aria-expanded={openMenu === 'account'}
            aria-controls="app-account-menu"
            aria-label={t(($) => $.common.shell.topbar.account)}
            onClick={() => toggleMenu('account')}
          >
            <span className="app-topbar-avatar" aria-hidden="true">
              <UserIcon />
            </span>
          </button>
          <MenuPopover
            id="app-account-menu"
            label={t(($) => $.common.shell.account.menuLabel)}
            open={openMenu === 'account'}
            onOpenChange={(open) => setOpenMenu(open ? 'account' : null)}
            triggerRef={accountTriggerRef}
            className="app-account-menu"
          >
            <AccountMenuContent onSelect={() => setOpenMenu(null)} />
          </MenuPopover>
        </div>
      </div>
    </header>
  );
}
