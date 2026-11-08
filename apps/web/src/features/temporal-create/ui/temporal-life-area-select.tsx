import { useEffect, useMemo, useRef, useState } from 'react';

import { TEMPORAL_DEFAULT_COLOR } from './temporal-color-control';

import './temporal-create-life-area-field.css';

export type TemporalLifeAreaOption = Readonly<{
  id: string;
  label: string;
  colorCode?: string | null;
  tone?: string;
}>;

/** Read-only color provenance for an assigned Life Area.
 * Its hue belongs to the Life Area, not an editable item-color override.
 */
export function TemporalAssignedLifeAreaSwatch({
  colorCode,
}: Readonly<{ colorCode: string | null | undefined }>) {
  const color =
    typeof colorCode === 'string' && /^#[0-9A-F]{6}$/i.test(colorCode)
      ? colorCode.toUpperCase()
      : TEMPORAL_DEFAULT_COLOR;
  return (
    <div className="temporal-create-life-area-field__color-cell">
      <span
        className="temporal-create-life-area-field__color-trigger"
        role="img"
        aria-label={`Colore della Life Area: ${color}`}
      >
        <span aria-hidden="true" style={{ background: color }} />
      </span>
    </div>
  );
}

function normalized(value: string): string {
  return value.trim().replace(/\s+/g, ' ');
}

export function TemporalLifeAreaSelect({
  query,
  options,
  selectedId,
  onQueryChange,
  onChoose,
  onClear,
  disabled = false,
  label = 'Life Area (opzionale)',
  placeholder = 'Life Area (opzionale)',
}: Readonly<{
  query: string;
  options: readonly TemporalLifeAreaOption[];
  selectedId: string | null;
  onQueryChange: (query: string) => void;
  onChoose: (option: TemporalLifeAreaOption) => void;
  onClear: () => void;
  disabled?: boolean;
  label?: string;
  placeholder?: string;
}>) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const filtered = useMemo(() => {
    const needle = normalized(query).toLocaleLowerCase();
    return needle
      ? options.filter((option) =>
          option.label.toLocaleLowerCase().includes(needle),
        )
      : options;
  }, [options, query]);

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [open]);

  return (
    <div ref={rootRef} className="temporal-create-life-area-field__area-cell">
      <input
        type="text"
        value={query}
        placeholder={placeholder}
        aria-label={label}
        maxLength={100}
        disabled={disabled}
        autoComplete="off"
        onFocus={() => setOpen(true)}
        onChange={(event) => {
          onQueryChange(event.currentTarget.value);
          setOpen(true);
        }}
      />
      {query ? (
        <button
          type="button"
          aria-label="Rimuovi Life Area"
          disabled={disabled}
          onClick={() => {
            onClear();
            setOpen(false);
          }}
        >
          ×
        </button>
      ) : null}
      {open && filtered.length > 0 ? (
        <div
          className="temporal-create-life-area-field__options"
          role="listbox"
        >
          {filtered.map((option) => (
            <button
              key={option.id}
              type="button"
              role="option"
              aria-selected={selectedId === option.id}
              onClick={() => {
                onChoose(option);
                setOpen(false);
              }}
            >
              <span
                className="temporal-create-life-area-field__swatch"
                style={
                  option.colorCode
                    ? { background: option.colorCode }
                    : undefined
                }
                data-context-tone={option.tone}
                aria-hidden="true"
              />
              <span>{option.label}</span>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
