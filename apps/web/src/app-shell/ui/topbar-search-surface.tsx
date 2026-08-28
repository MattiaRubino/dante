import { useNavigate } from '@tanstack/react-router';
import {
  useEffect,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent,
} from 'react';
import { useTranslation } from 'react-i18next';

import { APP_DESTINATIONS, type AppDestination } from '../model/navigation';
import { ArrowRightIcon, CloseIcon, SearchIcon } from './icons';

type TopbarSearchSurfaceProps = {
  onClose: (restoreFocus?: boolean) => void;
};

function normalize(value: string) {
  return value.trim().toLocaleLowerCase();
}

export function TopbarSearchSurface({ onClose }: TopbarSearchSurfaceProps) {
  const { t } = useTranslation('common');
  const navigate = useNavigate();
  const inputRef = useRef<HTMLInputElement>(null);
  const [query, setQuery] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const destinationCopy = useMemo(
    () => ({
      home: {
        label: t(($) => $.common.shell.destinations.home.label),
        description: t(($) => $.common.shell.destinations.home.description),
      },
      worlds: {
        label: t(($) => $.common.shell.destinations.worlds.label),
        description: t(($) => $.common.shell.destinations.worlds.description),
      },
      today: {
        label: t(($) => $.common.shell.destinations.today.label),
        description: t(($) => $.common.shell.destinations.today.description),
      },
      profile: {
        label: t(($) => $.common.shell.destinations.profile.label),
        description: t(($) => $.common.shell.destinations.profile.description),
      },
      settings: {
        label: t(($) => $.common.shell.destinations.settings.label),
        description: t(($) => $.common.shell.destinations.settings.description),
      },
    }),
    [t],
  );

  const filteredDestinations = useMemo(() => {
    const normalizedQuery = normalize(query);

    if (!normalizedQuery) {
      return APP_DESTINATIONS;
    }

    return APP_DESTINATIONS.filter((destination) => {
      const copy = destinationCopy[destination.id];
      return normalize(`${copy.label} ${copy.description}`).includes(
        normalizedQuery,
      );
    });
  }, [destinationCopy, query]);

  const selectDestination = async (destination: AppDestination) => {
    onClose(false);
    await navigate({ to: destination.to });
  };

  const handleInputKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      onClose(true);
      return;
    }

    if (event.key === 'ArrowDown') {
      event.preventDefault();
      setActiveIndex((current) =>
        filteredDestinations.length === 0
          ? 0
          : (current + 1) % filteredDestinations.length,
      );
      return;
    }

    if (event.key === 'ArrowUp') {
      event.preventDefault();
      setActiveIndex((current) =>
        filteredDestinations.length === 0
          ? 0
          : (current - 1 + filteredDestinations.length) %
            filteredDestinations.length,
      );
      return;
    }

    if (event.key === 'Enter') {
      const destination = filteredDestinations[activeIndex];
      if (destination) {
        event.preventDefault();
        void selectDestination(destination);
      }
    }
  };

  return (
    <div
      id="app-search-surface"
      className="app-topbar-search-surface"
      role="search"
      aria-label={t(($) => $.common.shell.search.title)}
    >
      <div className="app-topbar-search-field">
        <SearchIcon />
        <input
          ref={inputRef}
          type="search"
          role="combobox"
          value={query}
          placeholder={t(($) => $.common.shell.search.placeholder)}
          aria-label={t(($) => $.common.shell.topbar.searchLabel)}
          aria-expanded="true"
          aria-autocomplete="list"
          aria-controls="app-search-results"
          aria-activedescendant={
            filteredDestinations[activeIndex]
              ? `app-search-result-${filteredDestinations[activeIndex].id}`
              : undefined
          }
          onChange={(event) => {
            setQuery(event.target.value);
            setActiveIndex(0);
          }}
          onKeyDown={handleInputKeyDown}
        />
        <kbd>{t(($) => $.common.shell.topbar.searchShortcut)}</kbd>
        <button
          type="button"
          className="app-topbar-search-close"
          aria-label={t(($) => $.common.shell.actions.close)}
          onClick={() => onClose(true)}
        >
          <CloseIcon />
        </button>
      </div>

      <div className="app-topbar-search-panel">
        <div className="app-search-section-head">
          <span>{t(($) => $.common.shell.search.navigationSection)}</span>
          <small>{filteredDestinations.length}</small>
        </div>

        <div
          id="app-search-results"
          className="app-search-results"
          role="listbox"
          aria-label={t(($) => $.common.shell.search.navigationSection)}
        >
          {filteredDestinations.length > 0 ? (
            filteredDestinations.map((destination, index) => {
              const copy = destinationCopy[destination.id];
              return (
                <button
                  key={destination.id}
                  id={`app-search-result-${destination.id}`}
                  type="button"
                  role="option"
                  aria-selected={index === activeIndex}
                  className={index === activeIndex ? 'is-active' : undefined}
                  onPointerMove={() => setActiveIndex(index)}
                  onClick={() => void selectDestination(destination)}
                >
                  <span>
                    <strong>{copy.label}</strong>
                    <small>{copy.description}</small>
                  </span>
                  <ArrowRightIcon />
                </button>
              );
            })
          ) : (
            <p className="app-search-empty">
              {t(($) => $.common.shell.search.noResults)}
            </p>
          )}
        </div>

        <footer className="app-search-footer">
          <span>{t(($) => $.common.shell.search.remoteUnavailable)}</span>
          <span aria-hidden="true">↑ ↓ · Enter · Esc</span>
        </footer>
      </div>
    </div>
  );
}
