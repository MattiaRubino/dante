import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
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

type EditorBounds = Readonly<{
  top: number;
  left: number;
  width: number;
  height: number;
  borderRadius: string;
}>;

function editorForZonePicker(trigger: HTMLElement | null): HTMLElement | null {
  // Prefer the actual surrounding modal over a nested series form.
  return trigger?.closest<HTMLElement>(
    '.temporal-create-composer, .timeline-event-modal--edit',
  ) ?? trigger?.closest<HTMLElement>('.timeline-recurring-series-editor') ?? null;
}

function timezoneFocusable(panel: HTMLElement): HTMLElement[] {
  return Array.from(
    panel.querySelectorAll<HTMLElement>(
      'button:not([disabled]), input:not([disabled]), select:not([disabled]), ' +
      'textarea:not([disabled]), [tabindex]:not([tabindex="-1"])',
    ),
  ).filter((element) => !element.hasAttribute('hidden') &&
    element.getAttribute('aria-hidden') !== 'true');
}

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
    <svg
      className="temporal-create-timezone-globe"
      viewBox="0 0 24 24"
      fill="none"
      aria-hidden="true"
      focusable="false"
    >
      <circle className="temporal-create-timezone-globe__sphere" cx="12" cy="12" r="9" />
      <path className="temporal-create-timezone-globe__grid"
        d="M3 12h18M12 3c-2.7 2.5-4 5.5-4 9s1.3 6.5 4 9M12 3c2.7 2.5 4 5.5 4 9s-1.3 6.5-4 9" />
      <path className="temporal-create-timezone-globe__grid"
        d="M5.6 6.7c3.7 1.7 9.1 1.7 12.8 0M5.6 17.3c3.7-1.7 9.1-1.7 12.8 0" />
      <circle className="temporal-create-timezone-globe__accent" cx="17.4" cy="7.2" r="1.7" />
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
  const choiceRef = useRef<HTMLButtonElement>(null);
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
        ref={choiceRef}
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
                  choiceRef.current?.focus({ preventScroll: true });
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
                  choiceRef.current?.focus({ preventScroll: true });
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
  endZoneId?: string | null | undefined;
  onZonesChange?: (startZone: string | null, endZone: string | null) => void;
  allowDistinctZones?: boolean;
  date?: string;
  disabled?: boolean;
  disabledReason?: string | undefined;
  italian?: boolean;
  allowFloating?: boolean;
  displayLabel?: string | undefined;
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
  const triggerRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const restoreFocusRef = useRef(false);
  const [position, setPosition] = useState<DialogPlacement | null>(null);
  const [editorBounds, setEditorBounds] = useState<EditorBounds | null>(null);
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
    const editor = editorForZonePicker(rootRef.current);
    if (!editor) {
      setEditorBounds(null);
      return;
    }
    const rect = editor.getBoundingClientRect();
    const nextBounds: EditorBounds = {
      top: rect.top,
      left: rect.left,
      width: rect.width,
      height: rect.height,
      borderRadius: window.getComputedStyle(editor).borderRadius,
    };
    setEditorBounds((old) =>
      old?.top === nextBounds.top && old.left === nextBounds.left &&
      old.width === nextBounds.width && old.height === nextBounds.height &&
      old.borderRadius === nextBounds.borderRadius ? old : nextBounds,
    );
  }, []);
  const closeDialog = useCallback(() => {
    restoreFocusRef.current = true;
    setOpen(false);
  }, []);
  const openDialog = () => {
    if (disabled) return;
    // The shield keeps the anchor inaccessible while this dialog is open.
    if (open) return;
    setDraftStart(zoneId ?? local);
    setDraftEnd(endZoneId ?? zoneId ?? local);
    setDistinct(isDistinct && allowDistinctZones);
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
    closeDialog();
  };

  // One modal contract for Quick/Advanced and every Activity/Event/series Edit.
  // The editor is inert while this body-portaled panel owns interaction.
  useLayoutEffect(() => {
    if (!open) {
      if (restoreFocusRef.current) {
        restoreFocusRef.current = false;
        triggerRef.current?.focus({ preventScroll: true });
      }
      return;
    }
    const panel = panelRef.current;
    if (!panel) return;
    const editor = editorForZonePicker(rootRef.current);
    const wasInert = editor?.inert ?? false;
    if (editor) editor.inert = true;

    const firstControl = () => timezoneFocusable(panel)[0] ?? panel;
    const initialFocus = panel.querySelector<HTMLElement>(
      '.temporal-zone-dialog__choice',
    ) ?? firstControl();
    initialFocus.focus({ preventScroll: true });

    const keepFocusInside = (event: FocusEvent) => {
      if (event.target instanceof Node && !panel.contains(event.target)) {
        firstControl().focus({ preventScroll: true });
      }
    };
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        event.preventDefault();
        event.stopPropagation();
        closeDialog();
        return;
      }
      if (event.key !== 'Tab') return;
      const focusables = timezoneFocusable(panel);
      const first = focusables[0];
      const last = focusables.at(-1);
      if (!first || !last) {
        event.preventDefault();
        panel.focus({ preventScroll: true });
        return;
      }
      if (event.shiftKey && (document.activeElement === first ||
          !panel.contains(document.activeElement))) {
        event.preventDefault();
        last.focus({ preventScroll: true });
      } else if (!event.shiftKey && (document.activeElement === last ||
          !panel.contains(document.activeElement))) {
        event.preventDefault();
        first.focus({ preventScroll: true });
      }
    };
    const blockOutsidePointer = (event: MouseEvent | PointerEvent) => {
      if (event.target instanceof Node && panel.contains(event.target)) return;
      event.preventDefault();
      event.stopPropagation();
    };
    const blockOutsideScroll = (event: WheelEvent | TouchEvent) => {
      if (event.target instanceof Node && panel.contains(event.target)) return;
      event.preventDefault();
      event.stopPropagation();
    };

    document.addEventListener('focusin', keepFocusInside, true);
    document.addEventListener('keydown', onKeyDown, true);
    document.addEventListener('pointerdown', blockOutsidePointer, true);
    document.addEventListener('mousedown', blockOutsidePointer, true);
    document.addEventListener('click', blockOutsidePointer, true);
    document.addEventListener('wheel', blockOutsideScroll, { capture: true, passive: false });
    document.addEventListener('touchmove', blockOutsideScroll, { capture: true, passive: false });

    return () => {
      document.removeEventListener('focusin', keepFocusInside, true);
      document.removeEventListener('keydown', onKeyDown, true);
      document.removeEventListener('pointerdown', blockOutsidePointer, true);
      document.removeEventListener('mousedown', blockOutsidePointer, true);
      document.removeEventListener('click', blockOutsidePointer, true);
      document.removeEventListener('wheel', blockOutsideScroll, true);
      document.removeEventListener('touchmove', blockOutsideScroll, true);
      if (editor) editor.inert = wasInert;
    };
  }, [open, closeDialog]);

  useEffect(() => {
    if (!open) return;
    const reposition = () => updatePosition();
    window.addEventListener('resize', reposition);
    window.addEventListener('scroll', reposition, true);
    return () => {
      window.removeEventListener('resize', reposition);
      window.removeEventListener('scroll', reposition, true);
    };
  }, [open, updatePosition]);

  const panel = open ? (
    <div
      ref={panelRef}
      role="dialog"
      aria-modal="true"
      tabIndex={-1}
      aria-label={italian ? 'Imposta fuso orario' : 'Set time zone'}
      className="temporal-create-timezone-panel is-config-dialog"
      data-temporal-create-portal=""
      style={position ?? undefined}
      onKeyDown={(event) => event.stopPropagation()}
    >
      <h3>{italian ? 'Fuso orario' : 'Time zone'}</h3>
      {allowDistinctZones ? (
        <label className="temporal-zone-dialog__toggle">
          <input
            type="checkbox"
            checked={distinct}
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
        <button type="button" onClick={closeDialog}>
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
        ref={triggerRef}
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
        ? createPortal(
            <>
              <div className="temporal-create-timezone-interaction-shield"
                aria-hidden="true" />
              <div className="temporal-create-timezone-editor-dimmer"
                aria-hidden="true" style={editorBounds ?? undefined} />
              {panel}
            </>,
            document.body,
          )
        : panel}
    </div>
  );
}
