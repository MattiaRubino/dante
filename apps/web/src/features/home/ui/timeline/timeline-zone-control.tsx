import { useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import { timeZoneGmtOffset } from '../../../temporal-create/ui/temporal-time-zone-control';
import { sameTimelineTimeZone } from '../../../temporal/timeline-view-zone';

import './timeline-zone-control.css';

type Props = Readonly<{
  effectiveZoneId: string;
  selectedZoneId: string | null;
  date: string;
  secondaryZoneIds: readonly string[];
  onSelect: (zoneId: string | null) => void;
  onAddSecondaryZone: (zoneId: string) => void;
  onRemoveSecondaryZone: (zoneId: string) => void;
  onReorderSecondaryZones: () => void;
}>;

const COMMON_ZONES = ['UTC', 'Europe/Rome', 'Europe/London',
  'America/New_York', 'America/Los_Angeles', 'Asia/Tokyo', 'Asia/Kolkata'];
const ALL_ZONES: readonly string[] = (() => {
  try {
    const intl = Intl as typeof Intl & {
      supportedValuesOf?: (key: string) => string[];
    };
    const zones = intl.supportedValuesOf?.('timeZone') ?? [];
    return [...new Set([...COMMON_ZONES, ...zones])].sort();
  } catch {
    return COMMON_ZONES;
  }
})();

function compactOffset(offset: string): string {
  return offset.replace(/^GMT([+-])0?(\d{1,2}):00$/, 'GMT$1$2')
    .replace(/^GMT([+-])0?(\d):([0-9]{2})$/, 'GMT$1$2:$3');
}

export function TimelineZoneControl({
  effectiveZoneId, selectedZoneId, date, secondaryZoneIds,
  onSelect, onAddSecondaryZone, onRemoveSecondaryZone,
  onReorderSecondaryZones,
}: Props) {
  const rootRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLDivElement>(null);
  const [position, setPosition] = useState<Readonly<{
    top: number; left: number; width: number;
  }> | null>(null);
  const searchRef = useRef<HTMLInputElement>(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const offset = compactOffset(timeZoneGmtOffset(effectiveZoneId, date));
  const choices = useMemo(() => {
    const needle = query.trim().toLowerCase();
    const ordered = [selectedZoneId, ...secondaryZoneIds, ...COMMON_ZONES, ...ALL_ZONES]
      .filter((zone): zone is string => zone !== null);
    const matching = [...new Set(ordered)].filter((zone) => {
      if (!needle) return true;
      const offset = timeZoneGmtOffset(zone, date).toLowerCase();
      return zone.toLowerCase().includes(needle) ||
        zone.toLowerCase().replaceAll('_', ' ').includes(needle) ||
        offset.includes(needle) || compactOffset(offset).toLowerCase().includes(needle);
    });
    return matching.slice(0, 80);
  }, [date, query, selectedZoneId, secondaryZoneIds]);

  useLayoutEffect(() => {
    if (!open) return;
    const reposition = () => {
      const rect = triggerRef.current?.getBoundingClientRect();
      if (!rect) return;
      const gutter = 12;
      const width = Math.min(340, window.innerWidth - gutter * 2);
      const left = Math.max(gutter,
        Math.min(rect.left, window.innerWidth - width - gutter));
      const maxHeight = Math.min(410, window.innerHeight - gutter * 2);
      const top = rect.bottom + maxHeight + 7 <= window.innerHeight - gutter
        ? rect.bottom + 7 : Math.max(gutter, rect.top - maxHeight - 7);
      setPosition({ top, left, width });
    };
    reposition();
    window.addEventListener('resize', reposition);
    window.addEventListener('scroll', reposition, true);
    return () => {
      window.removeEventListener('resize', reposition);
      window.removeEventListener('scroll', reposition, true);
    };
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (!(event.target instanceof Node) ||
          rootRef.current?.contains(event.target) ||
          panelRef.current?.contains(event.target)) return;
      setOpen(false);
      setQuery('');
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      event.preventDefault();
      event.stopPropagation();
      setOpen(false);
      setQuery('');
      triggerRef.current?.focus({ preventScroll: true });
    };
    document.addEventListener('pointerdown', dismiss, true);
    document.addEventListener('keydown', escape, true);
    searchRef.current?.focus({ preventScroll: true });
    return () => {
      document.removeEventListener('pointerdown', dismiss, true);
      document.removeEventListener('keydown', escape, true);
    };
  }, [open]);

  const select = (zoneId: string | null) => {
    onSelect(zoneId);
    setOpen(false);
    setQuery('');
    triggerRef.current?.focus({ preventScroll: true });
  };

  const atCapacity = secondaryZoneIds.length >= 2;
  const shortZone = (zone: string) => zone.split('/').at(-1)?.replaceAll('_', ' ') ?? zone;

  return (
    <div className="dante-timeline-zone" ref={rootRef}>
      {secondaryZoneIds.map((zone) => (
        <span
          className="dante-timeline-zone__secondary-rail"
          key={zone}
          title={'Fuso secondario: ' + zone}
          aria-label={'Fuso secondario: ' + zone}
        >
          <span>{shortZone(zone)}</span>
          <small>{compactOffset(timeZoneGmtOffset(zone, date))}</small>
        </span>
      ))}
      <button
        ref={triggerRef}
        type="button"
        className="dante-timeline-zone__trigger"
        aria-haspopup="dialog"
        aria-expanded={open}
        aria-label={`Fuso orario della Timeline: ${effectiveZoneId}`}
        title={`Fuso di visualizzazione: ${effectiveZoneId}`}
        onClick={() => {
          setQuery('');
          setOpen((prev) => !prev);
        }}
      >
        <span className="dante-timeline-zone__trigger-offset">{offset}</span>
        <span className="dante-timeline-zone__trigger-chevron" aria-hidden="true">⌄</span>
      </button>
      {open && typeof document !== 'undefined' ? createPortal(
        <div ref={panelRef} className="dante-timeline-zone__panel" role="dialog"
          aria-label="Fuso orario della Timeline"
          style={position ?? { opacity: 0, pointerEvents: 'none' }}>
          <div className="dante-timeline-zone__heading">
            <strong>Fuso orario della Timeline</strong>
            <span aria-live="polite">{secondaryZoneIds.length + 1} di 3 fusi</span>
          </div>
          <input ref={searchRef} type="search"
            aria-label="Cerca fuso o GMT"
            placeholder="Cerca città, fuso o GMT…"
            value={query} onChange={(event) => setQuery(event.currentTarget.value)} />
          <div className="dante-timeline-zone__options" role="listbox"
            aria-label="Fusi orari disponibili">
            <button type="button" role="option"
              aria-selected={selectedZoneId === null}
              onClick={() => select(null)}>
              <span>Automatico · dispositivo</span>
              {selectedZoneId === null ? <span aria-hidden="true">✓</span> : null}
            </button>
            {choices.map((zone) => {
              const isPrimary = sameTimelineTimeZone(zone, effectiveZoneId);
              const secondary = secondaryZoneIds.find(
                (stored) => sameTimelineTimeZone(stored, zone),
              );
              const isSecondary = secondary !== undefined;
              return (
                <div className="dante-timeline-zone__option-row" key={zone}>
                  <button type="button" role="option"
                    className="dante-timeline-zone__option-name"
                    aria-selected={isPrimary}
                    title={isSecondary ? 'Rendi principale: ' + zone : undefined}
                    onClick={() => select(zone)}>
                    <span>{timeZoneGmtOffset(zone, date)} · {zone.replaceAll('_', ' ')}</span>
                    {isPrimary ? <span aria-hidden="true">✓</span> : null}
                  </button>
                  {isSecondary ? (
                    <>
                      {secondaryZoneIds.length === 2 ? (
                        <button type="button" className="dante-timeline-zone__option-action"
                          aria-label={'Inverti ordine dei fusi secondari: ' + zone}
                          title="Inverti ordine dei fusi secondari"
                          onClick={onReorderSecondaryZones}>⇄</button>
                      ) : null}
                      <button type="button" className="dante-timeline-zone__option-action"
                        aria-label={'Rimuovi fuso secondario: ' + zone}
                        title={'Rimuovi fuso secondario: ' + zone}
                        onClick={() => onRemoveSecondaryZone(secondary ?? zone)}>×</button>
                    </>
                  ) : !isPrimary && !atCapacity ? (
                    <button type="button" className="dante-timeline-zone__option-action"
                      aria-label={'Aggiungi fuso secondario: ' + zone}
                      title={'Aggiungi fuso secondario: ' + zone}
                      onClick={() => onAddSecondaryZone(zone)}>+</button>
                  ) : null}
                </div>
              );
            })}
            {choices.length === 0 ? <p>Nessun fuso trovato</p> : null}
          </div>
          {atCapacity ? <p className="dante-timeline-zone__limit">
            Massimo 3 fusi. Rimuovine uno per aggiungerne un altro.
          </p> : null}
        </div>, document.body,
      ) : null}
    </div>
  );
}
