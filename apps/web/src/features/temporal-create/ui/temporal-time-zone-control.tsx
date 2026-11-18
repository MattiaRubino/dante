import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import './temporal-time-zone-dialog.css';

const FALLBACK_TIME_ZONES = Object.freeze([
  'Europe/Rome', 'Europe/London', 'Europe/Paris', 'Europe/Berlin',
  'Europe/Madrid', 'Europe/Athens', 'America/New_York', 'America/Chicago',
  'America/Denver', 'America/Los_Angeles', 'America/Sao_Paulo',
  'Asia/Dubai', 'Asia/Kolkata', 'Asia/Singapore', 'Asia/Tokyo',
  'Australia/Sydney', 'Pacific/Auckland', 'UTC',
]);

function supportedTimeZones(): readonly string[] {
  const intl = Intl as typeof Intl & {
    supportedValuesOf?: (key: string) => string[];
  };
  try {
    const available = intl.supportedValuesOf?.('timeZone') ?? [];
    if (available.length) {
      return Object.freeze(
        Array.from(new Set(['UTC', ...FALLBACK_TIME_ZONES, ...available]))
          .sort((a, b) => a.localeCompare(b)),
      );
    }
  } catch {
    // Older runtimes use the deterministic subset above.
  }
  return FALLBACK_TIME_ZONES;
}

const TIME_ZONES = supportedTimeZones();
const offsetCache = new Map<string, string>();

export function localTimeZone(): string {
  try {
    return Intl.DateTimeFormat().resolvedOptions().timeZone || 'UTC';
  } catch {
    return 'UTC';
  }
}

export function timeZoneGmtOffset(zoneId: string, day: string): string {
  // Offset is computed for the event's date, not the current system date.
  // In particular, Europe/Rome changes between GMT+01 and GMT+02.
  const validDate = /^\d{4}-\d{2}-\d{2}$/.test(day) ? day : '2026-01-01';
  const key = zoneId + '|' + validDate;
  const saved = offsetCache.get(key);
  if (saved) return saved;
  try {
    const parts = new Intl.DateTimeFormat('en-US', {
      timeZone: zoneId,
      timeZoneName: 'shortOffset',
    }).formatToParts(new Date(validDate + 'T12:00:00Z'));
    const raw = parts.find((part) => part.type === 'timeZoneName')?.value ?? '';
    if (raw === 'GMT' || raw === 'UTC') {
      offsetCache.set(key, 'GMT+00:00');
      return 'GMT+00:00';
    }
    const match = /^GMT([+-])(\d{1,2})(?::(\d{2}))?$/.exec(raw);
    if (match) {
      const formatted = 'GMT' + match[1] + String(match[2]).padStart(2, '0') +
        ':' + (match[3] ?? '00');
      offsetCache.set(key, formatted);
      return formatted;
    }
  } catch {
    // Keep a stable label even when a runtime lacks shortOffset support.
  }
  return 'GMT';
}

type DialogPlacement = Readonly<{
  top: number;
  left: number;
  width: number;
}>;

function placeDialog(anchor: DOMRect): DialogPlacement {
  const gutter = 14;
  const width = Math.min(440, Math.max(0, window.innerWidth - gutter * 2));
  const left = Math.max(
    gutter, Math.min(anchor.right - width, window.innerWidth - width - gutter),
  );
  const available = window.innerHeight - gutter * 2;
  const desired = Math.min(490, available);
  const top = anchor.bottom + 8 + desired <= window.innerHeight - gutter
    ? anchor.bottom + 8
    : Math.max(gutter, Math.min(anchor.top - desired - 8, window.innerHeight - desired - gutter));
  return { top, left, width };
}

function GlobeIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="8" />
      <path d="M4 12h16M12 4c2.2 2.1 3.3 4.8 3.3 8S14.2 17.9 12 20M12 4c-2.2 2.1-3.3 4.8-3.3 8S9.8 17.9 12 20" />
    </svg>
  );
}

type ZonePickerProps = Readonly<{
  label: string;
  zone: string;
  date: string;
  onChange: (zone: string) => void;
  italian: boolean;
  expanded: boolean;
  onExpand: () => void;
  allowLocal?: boolean;
  floating?: boolean;
  onChooseLocal?: () => void;
}>;

function ZonePicker({
  label, zone, date, onChange, italian, expanded, onExpand,
  allowLocal = false, floating = false, onChooseLocal,
}: ZonePickerProps) {
  const [query, setQuery] = useState('');
  const searchRef = useRef<HTMLInputElement>(null);
  const offset = useCallback(
    (entry: string) => timeZoneGmtOffset(entry, date),
    [date],
  );
  const showLocal = allowLocal &&
    (!query.trim() || (italian ? 'ora locale' : 'local time')
      .includes(query.trim().toLocaleLowerCase()));
  const zones = useMemo(() => {
    if (!expanded) return [];
    const search = query.trim().toLocaleLowerCase();
    const filtered = TIME_ZONES.filter((entry) =>
      !search ||
      entry.toLocaleLowerCase().includes(search) ||
      entry.replaceAll('_', ' ').toLocaleLowerCase().includes(search) ||
      offset(entry).toLocaleLowerCase().includes(search),
    );
    return filtered;
  }, [expanded, query, offset]);

  useEffect(() => {
    if (expanded) searchRef.current?.focus();
  }, [expanded]);

  return (
    <div className="temporal-zone-dialog__picker">
      <label>{label}</label>
      <button
        type="button"
        className="temporal-zone-dialog__choice"
        aria-expanded={expanded}
        onClick={() => {
          setQuery('');
          onExpand();
        }}
      >
        <span>{'(' + offset(zone) + ') ' + zone.replaceAll('_', ' ')}</span>
        <span aria-hidden="true">{expanded ? '⌃' : '⌄'}</span>
      </button>
      {expanded ? (
        <div className="temporal-zone-dialog__options">
          <input
            ref={searchRef}
            type="search"
            className="temporal-create-timezone-search"
            aria-label={italian ? 'Cerca fuso orario' : 'Search time zone'}
            placeholder={italian ? 'Cerca fuso orario o GMT' : 'Search time zone or GMT'}
            value={query}
            onChange={(event) => setQuery(event.currentTarget.value)}
          />
          <div className="temporal-create-timezone-list" role="listbox" aria-label={label}>
            {showLocal ? (
              <button
                type="button"
                role="option"
                aria-selected={floating}
                className={floating ? 'is-selected' : ''}
                onClick={() => {
                  onChooseLocal?.();
                  onExpand();
                }}
              >
                <span className="temporal-zone-dialog__offset">
                  {'(' + offset(localTimeZone()) + ')'}
                </span>
                <span>
                  {italian ? 'Ora locale' : 'Local time'}
                  {' (' + localTimeZone().replaceAll('_', ' ') + ')'}
                </span>
              </button>
            ) : null}
            {zones.map((entry) => (
              <button
                type="button"
                role="option"
                aria-selected={entry === zone && !floating}
                key={entry}
                className={entry === zone && !floating ? 'is-selected' : ''}
                onClick={() => {
                  onChange(entry);
                  onExpand();
                }}
              >
                <span className="temporal-zone-dialog__offset">{'(' + offset(entry) + ')'}</span>
                <span>{entry.replaceAll('_', ' ')}</span>
              </button>
            ))}
            {!zones.length && !showLocal ? (
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

type Props = Readonly<{
  zoneId: string | null;
  onChange: (zoneId: string | null) => void;
  endZoneId?: string | null;
  onZonesChange?: (startZone: string | null, endZone: string | null) => void;
  allowDistinctZones?: boolean;
  date?: string;
  disabled?: boolean;
  disabledReason?: string;
  italian?: boolean;
  allowFloating?: boolean;
  displayLabel?: string;
}>;

/** The one timezone UI for Quick, Advanced, Activity/Event and series edits. */
export function TemporalTimeZoneControl({
  zoneId,
  onChange,
  endZoneId = null,
  onZonesChange,
  allowDistinctZones = false,
  date,
  disabled = false,
  disabledReason,
  italian = true,
  allowFloating = true,
  displayLabel,
}: Props) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState<DialogPlacement | null>(null);
  const [draftStart, setDraftStart] = useState(localTimeZone());
  const [draftEnd, setDraftEnd] = useState(localTimeZone());
  const [distinct, setDistinct] = useState(false);
  const [draftFloating, setDraftFloating] = useState(false);
  const [expanded, setExpanded] = useState<'single' | 'start' | 'end' | null>(null);
  const local = localTimeZone();
  const activeDate = date ?? new Date().toISOString().slice(0, 10);
  const isDistinct = !!endZoneId && !!zoneId && endZoneId !== zoneId;
  const mainLabel = displayLabel ??
    (isDistinct ? (italian ? 'Personalizzato' : 'Custom') : (zoneId ?? local));
  const updatePosition = useCallback(() => {
    if (!rootRef.current) return;
    const next = placeDialog(rootRef.current.getBoundingClientRect());
    setPosition((old) =>
      old?.top === next.top && old.left === next.left && old.width === next.width
        ? old : next,
    );
  }, []);
  const openDialog = () => {
    if (disabled) return;
    if (open) {
      setOpen(false);
      return;
    }
    setDraftStart(zoneId ?? local);
    setDraftEnd(endZoneId ?? zoneId ?? local);
    setDistinct(isDistinct);
    setDraftFloating(zoneId === null);
    setExpanded(null);
    updatePosition();
    setOpen(true);
  };
  const apply = () => {
    const start = !distinct && draftFloating && allowFloating
      ? null : draftStart;
    const end = distinct && draftEnd !== draftStart ? draftEnd : null;
    if (onZonesChange) onZonesChange(start, end);
    else onChange(start);
    setOpen(false);
  };

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target) &&
        !panelRef.current?.contains(event.target)
      ) setOpen(false);
    };
    const reposition = () => updatePosition();
    document.addEventListener('pointerdown', dismiss, true);
    window.addEventListener('resize', reposition);
    window.addEventListener('scroll', reposition, true);
    return () => {
      document.removeEventListener('pointerdown', dismiss, true);
      window.removeEventListener('resize', reposition);
      window.removeEventListener('scroll', reposition, true);
    };
  }, [open, updatePosition]);

  const panel = open ? (
    <div
      ref={panelRef}
      role="dialog"
      aria-label={italian ? 'Imposta fuso orario' : 'Set time zone'}
      className="temporal-create-timezone-panel is-config-dialog"
      data-temporal-create-portal=""
      style={position ?? undefined}
      onKeyDown={(event) => {
        if (event.key === 'Escape') {
          event.stopPropagation();
          setOpen(false);
        }
      }}
    >
      <h3>{italian ? 'Fuso orario' : 'Time zone'}</h3>
      <label className="temporal-zone-dialog__toggle">
        <input
          type="checkbox"
          checked={distinct}
          disabled={!allowDistinctZones && !distinct}
          onChange={(event) => {
            setDistinct(event.currentTarget.checked);
            setDraftEnd(draftStart);
            if (event.currentTarget.checked) setDraftFloating(false);
            setExpanded(null);
          }}
        />
        <span>
          {italian
            ? 'Utilizza fusi orari diversi per inizio e fine'
            : 'Use different time zones for start and end'}
        </span>
      </label>
      {!allowDistinctZones ? (
        <small className="temporal-zone-dialog__hint">
          {italian
            ? 'Per questa programmazione è disponibile un solo fuso orario.'
            : 'Only one time zone is available for this schedule.'}
        </small>
      ) : null}
      {distinct ? (
        <>
          <ZonePicker
            label={italian ? 'Fuso orario di inizio' : 'Start time zone'}
            zone={draftStart}
            date={activeDate}
            italian={italian}
            expanded={expanded === 'start'}
            onExpand={() => setExpanded((current) => current === 'start' ? null : 'start')}
            onChange={(zone) => {
              setDraftStart(zone);
              setDraftFloating(false);
            }}
          />
          <ZonePicker
            label={italian ? 'Fuso orario di fine' : 'End time zone'}
            zone={draftEnd}
            date={activeDate}
            italian={italian}
            expanded={expanded === 'end'}
            onExpand={() => setExpanded((current) => current === 'end' ? null : 'end')}
            onChange={setDraftEnd}
          />
        </>
      ) : (
        <ZonePicker
          label={italian ? 'Fuso orario' : 'Time zone'}
          zone={draftStart}
          date={activeDate}
          italian={italian}
          expanded={expanded === 'single'}
          onExpand={() => setExpanded((current) => current === 'single' ? null : 'single')}
          onChange={(zone) => {
            setDraftStart(zone);
            setDraftFloating(false);
          }}
          allowLocal={allowFloating}
          floating={draftFloating}
          onChooseLocal={() => {
            setDraftStart(local);
            setDraftFloating(true);
          }}
        />
      )}
      <div className="temporal-zone-dialog__actions">
        <button type="button" onClick={() => setOpen(false)}>
          {italian ? 'Annulla' : 'Cancel'}
        </button>
        <button type="button" className="is-primary" onClick={apply}>
          OK
        </button>
      </div>
    </div>
  ) : null;

  return (
    <div ref={rootRef} className="temporal-create-timezone-control" data-create-path="timeZoneId"
      title={disabled ? disabledReason : undefined}>
      <button
        type="button"
        className={'temporal-create-timezone-trigger' + (open ? ' is-open' : '')}
        disabled={disabled}
        aria-expanded={open}
        aria-label={(italian ? 'Fuso orario: ' : 'Time zone: ') + mainLabel}
        onClick={openDialog}
      >
        <GlobeIcon />
        <span className="temporal-create-timezone-label">{mainLabel}</span>
        <span className="temporal-create-timezone-chevron" aria-hidden="true">
          {open ? '⌃' : '⌄'}
        </span>
      </button>
      {panel && typeof document !== 'undefined'
        ? createPortal(panel, document.body) : panel}
    </div>
  );
}
