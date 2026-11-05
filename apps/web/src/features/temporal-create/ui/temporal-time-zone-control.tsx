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
}: Readonly<{
  zoneId: string | null;
  onChange: (zoneId: string | null) => void;
  disabled?: boolean;
  italian?: boolean;
  allowFloating?: boolean;
}>) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const label = zoneId ?? (italian ? 'Ora locale' : 'Local time');

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
        title={label}
        onClick={() => setOpen((current) => !current)}
      >
        <GlobeIcon />
        <span className="temporal-create-timezone-divider" aria-hidden="true" />
        <span className="temporal-create-timezone-label">
          {italian ? 'Fuso orario' : 'Time zone'} · {label}
        </span>
        <span className="temporal-create-timezone-chevron" aria-hidden="true">
          {open ? '⌃' : '⌄'}
        </span>
      </button>
      {open ? (
        <div className="temporal-create-timezone-panel">
          <div className="temporal-create-timezone-current">
            <GlobeIcon />
            <span>{label}</span>
          </div>
          <div className="temporal-create-timezone-list">
            {allowFloating ? (
              <button
                type="button"
                className={zoneId === null ? 'is-selected' : ''}
                onClick={() => {
                  onChange(null);
                  setOpen(false);
                }}
              >
                Ora locale
              </button>
            ) : null}
            {TIME_ZONES.map((zone) => (
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
          </div>
        </div>
      ) : null}
    </div>
  );
}
