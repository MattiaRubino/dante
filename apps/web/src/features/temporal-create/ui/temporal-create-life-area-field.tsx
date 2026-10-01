import { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import { HexColorInput, HexColorPicker } from 'react-colorful';

import { createRemoteTemporalOrganizationDataSource } from '../../temporal/remote-organization';
import type {
  TemporalCreateU2AuthoringDraft,
  TemporalCreateU2LifeAreaDraft,
} from '../model/temporal-create-u2-authoring';
import {
  readTemporalCreateRecentUsedColors,
  rememberTemporalCreateUsedColor,
  TEMPORAL_CREATE_DEFAULT_COLOR,
} from './temporal-create-recent-colors';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

import './temporal-create-life-area-field.css';

type TemporalCreateLifeAreaFieldProps = Readonly<{
  contexts: readonly TemporalCreateContextOption[];
  draft: TemporalCreateU2AuthoringDraft;
  onLifeAreaChange: (value: TemporalCreateU2LifeAreaDraft) => void;
  onItemColorChange: (value: string | null) => void;
  onLegacyContextChange: (contextId: string) => void;
}>;

type ColorPreset = Readonly<{
  value: string;
  label: string;
}>;

type FloatingPickerPosition = Readonly<{
  left: number;
  top: number;
}>;

const DEFAULT_COLOR = TEMPORAL_CREATE_DEFAULT_COLOR;
const COLOR_PRESETS: readonly ColorPreset[] = Object.freeze([
  Object.freeze({ value: '#D50000', label: 'Rosso' }),
  Object.freeze({ value: '#E67C73', label: 'Salmone' }),
  Object.freeze({ value: '#AD1457', label: 'Lampone' }),
  Object.freeze({ value: '#F4511E', label: 'Rosso arancio' }),
  Object.freeze({ value: DEFAULT_COLOR, label: 'Arancione DANTE' }),
  Object.freeze({ value: '#EF6C00', label: 'Arancione scuro' }),
  Object.freeze({ value: '#F6BF26', label: 'Ambra' }),
  Object.freeze({ value: '#FFD600', label: 'Giallo' }),
  Object.freeze({ value: '#C0CA33', label: 'Lime' }),
  Object.freeze({ value: '#7CB342', label: 'Verde mela' }),
  Object.freeze({ value: '#33B679', label: 'Verde menta' }),
  Object.freeze({ value: '#0B8043', label: 'Verde bosco' }),
  Object.freeze({ value: '#009688', label: 'Turchese' }),
  Object.freeze({ value: '#26A69A', label: 'Acquamarina' }),
  Object.freeze({ value: '#039BE5', label: 'Azzurro' }),
  Object.freeze({ value: '#4285F4', label: 'Blu' }),
  Object.freeze({ value: '#3F51B5', label: 'Indaco' }),
  Object.freeze({ value: '#7986CB', label: 'Pervinca' }),
  Object.freeze({ value: '#673AB7', label: 'Viola' }),
  Object.freeze({ value: '#8E24AA', label: 'Prugna' }),
  Object.freeze({ value: '#B39DDB', label: 'Lavanda' }),
  Object.freeze({ value: '#795548', label: 'Marrone' }),
  Object.freeze({ value: '#616161', label: 'Grigio' }),
  Object.freeze({ value: '#E0E0E0', label: 'Bianco fumo' }),
]);

function normalized(value: string): string {
  return value.trim().replace(/\s+/g, ' ');
}

function selectedLabel(draft: TemporalCreateU2AuthoringDraft): string {
  switch (draft.lifeArea.kind) {
    case 'none':
      return '';
    case 'existing':
      return draft.lifeArea.label;
    case 'new':
      return draft.lifeArea.name;
  }
}

function selectedColor(draft: TemporalCreateU2AuthoringDraft): string {
  switch (draft.lifeArea.kind) {
    case 'existing':
    case 'new':
      return draft.lifeArea.colorCode ?? DEFAULT_COLOR;
    case 'none':
      return draft.itemColorCode ?? DEFAULT_COLOR;
  }
}

function canonicalOptions(
  contexts: readonly TemporalCreateContextOption[],
  areas: Awaited<
    ReturnType<ReturnType<typeof createRemoteTemporalOrganizationDataSource>['load']>
  >['areas'],
): readonly TemporalCreateContextOption[] {
  const byRef = new Map(contexts.map((context) => [context.id, context]));
  return Object.freeze(
    areas
      .filter((area) => !area.archived)
      .map((area) => {
        const current = byRef.get(area.ref);
        return Object.freeze({
          id: area.ref,
          label: area.name,
          tone: current?.tone ?? ('personal' as const),
          revision: area.revision,
          colorCode: area.colorCode,
          local: false,
        });
      }),
  );
}

export function TemporalCreateLifeAreaField({
  contexts,
  draft,
  onLifeAreaChange,
  onItemColorChange,
  onLegacyContextChange,
}: TemporalCreateLifeAreaFieldProps) {
  const [areaOpen, setAreaOpen] = useState(false);
  const [colorOpen, setColorOpen] = useState(false);
  const [customColorOpen, setCustomColorOpen] = useState(false);
  const [customPickerPosition, setCustomPickerPosition] =
    useState<FloatingPickerPosition | null>(null);
  const [query, setQuery] = useState(() => selectedLabel(draft));
  const [availableContexts, setAvailableContexts] = useState(contexts);
  const [recentColors] = useState<readonly string[]>(() =>
    typeof window === 'undefined'
      ? Object.freeze([])
      : readTemporalCreateRecentUsedColors(),
  );
  const rootRef = useRef<HTMLDivElement | null>(null);
  const customPickerRef = useRef<HTMLDivElement | null>(null);
  const sourceRef = useRef<
    ReturnType<typeof createRemoteTemporalOrganizationDataSource> | null
  >(null);
  const currentColor = selectedColor(draft).toUpperCase();

  useEffect(() => {
    setQuery(selectedLabel(draft));
  }, [draft.lifeArea]);

  useEffect(() => {
    setAvailableContexts(contexts);
  }, [contexts]);

  useEffect(() => {
    if (import.meta.env.MODE === 'test') return;
    sourceRef.current ??= createRemoteTemporalOrganizationDataSource();
    let cancelled = false;
    void sourceRef.current.load().then(
      (snapshot) => {
        if (!cancelled) {
          setAvailableContexts(canonicalOptions(contexts, snapshot.areas));
        }
      },
      () => undefined,
    );
    return () => {
      cancelled = true;
    };
  }, [contexts]);

  useEffect(() => {
    if (!areaOpen && !colorOpen && !customColorOpen) return;
    const dismiss = (event: PointerEvent) => {
      if (!(event.target instanceof Node)) return;
      if (rootRef.current?.contains(event.target)) return;
      if (customPickerRef.current?.contains(event.target)) return;
      setAreaOpen(false);
      setColorOpen(false);
      setCustomColorOpen(false);
      setCustomPickerPosition(null);
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [areaOpen, colorOpen, customColorOpen]);

  useEffect(() => {
    if (!customColorOpen) return;
    const closeFloatingPicker = () => {
      setCustomColorOpen(false);
      setCustomPickerPosition(null);
    };
    window.addEventListener('resize', closeFloatingPicker);
    return () => window.removeEventListener('resize', closeFloatingPicker);
  }, [customColorOpen]);

  useEffect(() => {
    const form = rootRef.current?.closest('form');
    if (!form) return;
    const rememberUsedColor = () => rememberTemporalCreateUsedColor(currentColor);
    form.addEventListener('submit', rememberUsedColor);
    return () => form.removeEventListener('submit', rememberUsedColor);
  }, [currentColor]);

  const filtered = useMemo(() => {
    const needle = normalized(query).toLocaleLowerCase();
    return needle
      ? availableContexts.filter((context) =>
          context.label.toLocaleLowerCase().includes(needle),
        )
      : availableContexts;
  }, [availableContexts, query]);

  const choose = (context: TemporalCreateContextOption) => {
    onLifeAreaChange(
      Object.freeze({
        kind: 'existing' as const,
        lifeAreaRef: context.id,
        label: context.label,
        expectedRevision: context.revision ?? 1,
        colorCode: context.colorCode ?? DEFAULT_COLOR,
        colorChanged: context.colorCode === null,
      }),
    );
    onItemColorChange(null);
    onLegacyContextChange(context.id);
    setQuery(context.label);
    setAreaOpen(false);
  };

  const clear = () => {
    setQuery('');
    onLifeAreaChange(Object.freeze({ kind: 'none' as const }));
    onItemColorChange(DEFAULT_COLOR);
    onLegacyContextChange('');
  };

  const stageTypedName = (value: string) => {
    setQuery(value);
    const name = normalized(value);
    if (!name) {
      clear();
      return;
    }
    const exact = availableContexts.find(
      (context) =>
        context.label.toLocaleLowerCase() === name.toLocaleLowerCase(),
    );
    if (exact) {
      choose(exact);
      setAreaOpen(true);
      return;
    }
    const previousColor =
      draft.lifeArea.kind === 'new'
        ? draft.lifeArea.colorCode ?? DEFAULT_COLOR
        : DEFAULT_COLOR;
    onLifeAreaChange(
      Object.freeze({ kind: 'new' as const, name, colorCode: previousColor }),
    );
    onItemColorChange(null);
    onLegacyContextChange('');
    setAreaOpen(true);
  };

  const changeColor = (colorCode: string) => {
    const canonical = colorCode.toUpperCase();
    if (!/^#[0-9A-F]{6}$/.test(canonical)) return;
    if (draft.lifeArea.kind === 'existing') {
      onLifeAreaChange(
        Object.freeze({
          ...draft.lifeArea,
          colorCode: canonical,
          colorChanged: true,
        }),
      );
      return;
    }
    if (draft.lifeArea.kind === 'new') {
      onLifeAreaChange(
        Object.freeze({ ...draft.lifeArea, colorCode: canonical }),
      );
      return;
    }
    onItemColorChange(canonical);
  };

  const colorLabel =
    draft.lifeArea.kind === 'none'
      ? 'Colore attività o evento'
      : 'Colore Life Area';

  const openCustomPicker = (trigger: HTMLButtonElement) => {
    if (customColorOpen) {
      setCustomColorOpen(false);
      setCustomPickerPosition(null);
      return;
    }
    const rect = trigger.getBoundingClientRect();
    const panelWidth = 238;
    const panelHeight = 258;
    const gap = 12;
    let left = rect.left - panelWidth - gap;
    if (left < 12) {
      left = Math.min(window.innerWidth - panelWidth - 12, rect.right + gap);
    }
    const top = Math.max(
      12,
      Math.min(rect.top - 6, window.innerHeight - panelHeight - 12),
    );
    setCustomPickerPosition(Object.freeze({ left, top }));
    setCustomColorOpen(true);
  };

  const floatingPicker =
    customColorOpen &&
    customPickerPosition &&
    typeof document !== 'undefined'
      ? createPortal(
          <div
            ref={customPickerRef}
            className="temporal-create-life-area-field__custom-picker is-floating"
            role="dialog"
            aria-label="Colore personalizzato"
            style={{
              left: customPickerPosition.left,
              top: customPickerPosition.top,
            }}
          >
            <HexColorPicker
              color={currentColor}
              onChange={changeColor}
              aria-label="Selettore colore personalizzato"
            />
            <label>
              <span>HEX</span>
              <HexColorInput
                color={currentColor}
                onChange={changeColor}
                prefixed
                aria-label="Codice colore HEX"
              />
            </label>
          </div>,
          document.body,
        )
      : null;

  return (
    <>
      <div ref={rootRef} className="temporal-create-life-area-field">
        <div className="temporal-create-life-area-field__color-cell">
          <button
            className="temporal-create-life-area-field__color-trigger"
            type="button"
            aria-label={colorLabel}
            aria-expanded={colorOpen}
            title={colorLabel}
            onClick={() => {
              setColorOpen((current) => !current);
              setCustomColorOpen(false);
              setCustomPickerPosition(null);
              setAreaOpen(false);
            }}
          >
            <span aria-hidden="true" style={{ background: currentColor }} />
          </button>

          {colorOpen ? (
            <div
              className="temporal-create-life-area-field__color-popover"
              role="dialog"
              aria-label="Scegli colore"
            >
              <div className="temporal-create-life-area-field__palette">
                <button
                  className="temporal-create-life-area-field__custom-trigger"
                  type="button"
                  aria-label="Colore personalizzato"
                  aria-expanded={customColorOpen}
                  title="Colore personalizzato"
                  onClick={(event) => openCustomPicker(event.currentTarget)}
                >
                  <span aria-hidden="true" />
                </button>
                {COLOR_PRESETS.map((preset) => (
                  <button
                    key={preset.value}
                    className="temporal-create-life-area-field__color-swatch"
                    type="button"
                    aria-label={preset.label}
                    aria-pressed={currentColor === preset.value}
                    title={preset.label}
                    onClick={() => changeColor(preset.value)}
                  >
                    <span
                      aria-hidden="true"
                      style={{ background: preset.value }}
                    />
                  </button>
                ))}
              </div>

              {recentColors.length > 0 ? (
                <div
                  className="temporal-create-life-area-field__recent"
                  aria-label="Ultimi colori usati"
                >
                  <small>Usati di recente</small>
                  <div>
                    {recentColors.map((color) => (
                      <button
                        key={color}
                        type="button"
                        aria-label={`Colore usato ${color}`}
                        title={`Usato di recente · ${color}`}
                        onClick={() => changeColor(color)}
                      >
                        <span
                          aria-hidden="true"
                          style={{ background: color }}
                        />
                      </button>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>
          ) : null}
        </div>

        <div className="temporal-create-life-area-field__area-cell">
          <input
            type="text"
            value={query}
            placeholder="Life Area (opzionale)"
            aria-label="Life Area (opzionale)"
            autoComplete="off"
            onFocus={() => {
              setAreaOpen(true);
              setColorOpen(false);
              setCustomColorOpen(false);
              setCustomPickerPosition(null);
            }}
            onChange={(event) => stageTypedName(event.currentTarget.value)}
          />
          {query ? (
            <button type="button" aria-label="Rimuovi Life Area" onClick={clear}>
              ×
            </button>
          ) : null}

          {areaOpen ? (
            <div
              className="temporal-create-life-area-field__options"
              role="listbox"
            >
              <button
                type="button"
                role="option"
                aria-selected={draft.lifeArea.kind === 'none'}
                onClick={() => {
                  clear();
                  setAreaOpen(false);
                }}
              >
                <span className="is-empty" aria-hidden="true" />
                <span>Nessuna Life Area</span>
              </button>
              {filtered.map((context) => (
                <button
                  key={context.id}
                  type="button"
                  role="option"
                  aria-selected={
                    draft.lifeArea.kind === 'existing' &&
                    draft.lifeArea.lifeAreaRef === context.id
                  }
                  onClick={() => choose(context)}
                >
                  <span
                    className="temporal-create-life-area-field__swatch"
                    style={
                      context.colorCode
                        ? { background: context.colorCode }
                        : undefined
                    }
                    data-context-tone={context.tone}
                    aria-hidden="true"
                  />
                  <span>{context.label}</span>
                </button>
              ))}
              {draft.lifeArea.kind === 'new' ? (
                <div className="temporal-create-life-area-field__new">
                  <span aria-hidden="true">＋</span>
                  <span>
                    Crea <strong>{draft.lifeArea.name}</strong> quando premi Aggiungi
                  </span>
                </div>
              ) : null}
            </div>
          ) : null}
        </div>
      </div>
      {floatingPicker}
    </>
  );
}
