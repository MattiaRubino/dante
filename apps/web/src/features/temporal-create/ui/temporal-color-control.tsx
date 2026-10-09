import { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { HexColorInput, HexColorPicker } from 'react-colorful';

import {
  readTemporalCreateRecentUsedColors,
  rememberTemporalCreateUsedColor,
  TEMPORAL_CREATE_DEFAULT_COLOR,
} from './temporal-create-recent-colors';

import './temporal-create-life-area-field.css';

export const TEMPORAL_DEFAULT_COLOR = TEMPORAL_CREATE_DEFAULT_COLOR;

const PRESETS = [
  ['#D50000', 'Rosso'], ['#E67C73', 'Salmone'],
  ['#AD1457', 'Lampone'], ['#F4511E', 'Rosso arancio'],
  [TEMPORAL_DEFAULT_COLOR, 'Arancione DANTE'], ['#EF6C00', 'Arancione scuro'],
  ['#F6BF26', 'Ambra'], ['#FFD600', 'Giallo'],
  ['#C0CA33', 'Lime'], ['#7CB342', 'Verde mela'],
  ['#33B679', 'Verde menta'], ['#0B8043', 'Verde bosco'],
  ['#009688', 'Turchese'], ['#26A69A', 'Acquamarina'],
  ['#039BE5', 'Azzurro'], ['#4285F4', 'Blu'],
  ['#3F51B5', 'Indaco'], ['#7986CB', 'Pervinca'],
  ['#673AB7', 'Viola'], ['#8E24AA', 'Prugna'],
  ['#B39DDB', 'Lavanda'], ['#795548', 'Marrone'],
  ['#616161', 'Grigio'], ['#E0E0E0', 'Bianco fumo'],
] as const;

export function TemporalColorControl({ value, label, onChange }: Readonly<{
  value: string;
  label: string;
  onChange: (color: string) => void;
}>) {
  const [open, setOpen] = useState(false);
  const [customOpen, setCustomOpen] = useState(false);
  const [position, setPosition] = useState<{ left: number; top: number } | null>(null);
  const [recentColors] = useState<readonly string[]>(() =>
    typeof window === 'undefined' ? [] : readTemporalCreateRecentUsedColors());
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const panelRef = useRef<HTMLDivElement | null>(null);
  const color = /^#[0-9A-F]{6}$/i.test(value) ? value.toUpperCase() : TEMPORAL_DEFAULT_COLOR;

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (event.target instanceof Node &&
          !triggerRef.current?.contains(event.target) &&
          !panelRef.current?.contains(event.target)) {
        setOpen(false);
        setCustomOpen(false);
      }
    };
    const close = () => { setOpen(false); setCustomOpen(false); };
    document.addEventListener('pointerdown', dismiss, true);
    window.addEventListener('resize', close);
    return () => {
      document.removeEventListener('pointerdown', dismiss, true);
      window.removeEventListener('resize', close);
    };
  }, [open]);

  useEffect(() => {
    const form = triggerRef.current?.closest('form');
    if (!form) return;
    const remember = () => rememberTemporalCreateUsedColor(color);
    form.addEventListener('submit', remember);
    return () => form.removeEventListener('submit', remember);
  }, [color]);

  const change = (next: string) => {
    const canonical = next.toUpperCase();
    if (/^#[0-9A-F]{6}$/.test(canonical)) onChange(canonical);
  };

  const toggle = () => {
    if (open) { setOpen(false); setCustomOpen(false); return; }
    const rect = triggerRef.current?.getBoundingClientRect();
    if (!rect) return;
    const width = 270;
    const gap = 12;
    const padding = 12;
    const left = rect.left - width - gap < padding
      ? Math.min(window.innerWidth - width - padding, rect.right + gap)
      : rect.left - width - gap;
    setPosition({
      left: Math.max(padding, left),
      top: Math.max(padding, Math.min(rect.top - 118, window.innerHeight - 430)),
    });
    setOpen(true);
  };

  return <>
    <div className="temporal-create-life-area-field__color-cell">
      <button ref={triggerRef} className="temporal-create-life-area-field__color-trigger"
        type="button" aria-label={label} title={label}
        aria-expanded={open} onClick={toggle}>
        <span aria-hidden="true" style={{ background: color }} />
      </button>
    </div>
    {open && position && typeof document !== 'undefined' ? createPortal(
      <div ref={panelRef} className="temporal-create-life-area-field__color-popover is-floating"
        data-temporal-create-portal="color" role="dialog" aria-label="Scegli colore"
        style={position}>
        <div className="temporal-create-life-area-field__palette">
          <button className="temporal-create-life-area-field__custom-trigger"
            type="button" aria-label="Colore personalizzato" title="Colore personalizzato"
            aria-expanded={customOpen} onClick={() => setCustomOpen((current) => !current)}>
            <span aria-hidden="true" />
          </button>
          {PRESETS.map(([preset, name]) => <button key={preset}
            className="temporal-create-life-area-field__color-swatch"
            type="button" aria-label={name} title={name}
            aria-pressed={color === preset} onClick={() => change(preset)}>
            <span aria-hidden="true" style={{ background: preset }} />
          </button>)}
        </div>
        {recentColors.length > 0 ? <div className="temporal-create-life-area-field__recent"
          aria-label="Ultimi colori usati">
          <small>Usati di recente</small>
          <div>{recentColors.map((recent) => <button key={recent} type="button"
            aria-label={`Colore usato ${recent}`} title={`Usato di recente · ${recent}`}
            onClick={() => change(recent)}>
            <span aria-hidden="true" style={{ background: recent }} />
          </button>)}</div>
        </div> : null}
        {customOpen ? <div className="temporal-create-life-area-field__custom-picker is-embedded">
          <HexColorPicker color={color} onChange={change}
            aria-label="Selettore colore personalizzato" />
          <label><span>HEX</span><HexColorInput color={color} onChange={change}
            prefixed aria-label="Codice colore HEX" /></label>
        </div> : null}
      </div>, document.body) : null}
  </>;
}
