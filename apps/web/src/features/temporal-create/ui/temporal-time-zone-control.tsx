import { useEffect, useRef, useState } from 'react';

const FALLBACK_TIME_ZONES = Object.freeze([
  'Europe/Rome',
  'Europe/London',
  'Europe/Paris',
  'Europe/Berlin',
  'Europe/Madrid',
  'Europe/Athens',
  'America/New_York',
  'America/Chicago',
  'America/Denver',
  'America/Los_Angeles',
  'America/Sao_Paulo',
  'Asia/Dubai',
  'Asia/Kolkata',
  'Asia/Singapore',
  'Asia/Tokyo',
  'Australia/Sydney',
  'Pacific/Auckland',
  'UTC',
]);

function supportedTimeZones(): readonly string[] {
  const intl = Intl as typeof Intl & {
    supportedValuesOf?: (key: string) => string[];
  };
  try {
    const values = intl.supportedValuesOf?.('timeZone') ?? [];
    if (values.length > 0)
      return Object.freeze(
        Array.from(new Set(['UTC', ...values])).sort((a, b) =>
          a.localeCompare(b),
        ),
      );
  } catch {
    // The same deterministic choices remain available without Intl.supportedValuesOf.
  }
  return FALLBACK_TIME_ZONES;
}

const TIME_ZONES = supportedTimeZones();

function GlobeIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="8" />
      <path d="M4 12h16M12 4c2.2 2.1 3.3 4.8 3.3 8S14.2 17.9 12 20M12 4c-2.2 2.1-3.3 4.8-3.3 8S9.8 17.9 12 20" />
    </svg>
  );
}

export function TemporalTimeZoneControl({
  zoneId,
  onChange,
  disabled = false,
  italian = true,
  allowFloating = true,
  displayLabel,
}: Readonly<{
  zoneId: string | null;
  onChange: (zoneId: string | null) => void;
  disabled?: boolean;
  italian?: boolean;
  allowFloating?: boolean;
  displayLabel?: string;
}>) {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const rootRef = useRef<HTMLDivElement>(null);
  const searchRef = useRef<HTMLInputElement>(null);
  const localLabel = italian ? 'Ora locale' : 'Local time';
  const label = displayLabel ?? zoneId ?? localLabel;
  const search = query.trim().toLocaleLowerCase();
  const visibleZones = TIME_ZONES.filter(
    (zone) =>
      zone.toLocaleLowerCase().includes(search) ||
      zone.replaceAll('_', ' ').toLocaleLowerCase().includes(search),
  );
  const showLocal =
    allowFloating &&
    (search === '' || localLabel.toLocaleLowerCase().includes(search));

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      )
        setOpen(false);
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [open]);

  useEffect(() => {
    if (open) searchRef.current?.focus();
  }, [open]);

  return (
    <div
      ref={rootRef}
      className="temporal-create-timezone-control"
      data-create-path="timeZoneId"
    >
      <button
        className={`temporal-create-timezone-trigger${open ? ' is-open' : ''}`}
        type="button"
        disabled={disabled}
        aria-label={`Fuso orario: ${label}`}
        aria-expanded={open}
        onClick={() => {
          setQuery('');
          setOpen((current) => !current);
        }}
      >
        <GlobeIcon />
        <span className="temporal-create-timezone-label">{label}</span>
        <span className="temporal-create-timezone-chevron" aria-hidden="true">
          {open ? '⌃' : '⌄'}
        </span>
      </button>
      {open ? (
        <div
          className="temporal-create-timezone-panel"
          role="dialog"
          aria-label={italian ? 'Scegli fuso orario' : 'Choose time zone'}
          onKeyDown={(event) => {
            if (event.key === 'Escape') {
              event.stopPropagation();
              setOpen(false);
              rootRef.current?.querySelector('button')?.focus();
            }
          }}
        >
          <input
            ref={searchRef}
            className="temporal-create-timezone-search"
            type="search"
            value={query}
            onChange={(event) => setQuery(event.currentTarget.value)}
            aria-label={italian ? 'Cerca fuso orario' : 'Search time zone'}
            placeholder={italian ? 'Cerca fuso orario' : 'Search time zone'}
          />
          <div className="temporal-create-timezone-list">
            {showLocal ? (
              <button
                type="button"
                className={zoneId === null ? 'is-selected' : ''}
                onClick={() => {
                  onChange(null);
                  setOpen(false);
                }}
              >
                {localLabel}
              </button>
            ) : null}
            {visibleZones.map((zone) => (
              <button
                key={zone}
                type="button"
                className={zoneId === zone ? 'is-selected' : ''}
                onClick={() => {
                  onChange(zone);
                  setOpen(false);
                }}
              >
                {zone.replaceAll('_', ' ')}
              </button>
            ))}
            {visibleZones.length === 0 && !showLocal ? (
              <p className="temporal-create-timezone-empty">
                {italian ? 'Nessun fuso trovato' : 'No time zone found'}
              </p>
            ) : null}
          </div>
        </div>
      ) : null}
    </div>
  );
}
