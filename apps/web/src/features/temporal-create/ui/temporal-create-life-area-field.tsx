import { useEffect, useMemo, useRef, useState } from 'react';

import { createRemoteTemporalOrganizationDataSource } from '../../temporal/remote-organization';
import type {
  TemporalCreateU2AuthoringDraft,
  TemporalCreateU2LifeAreaDraft,
} from '../model/temporal-create-u2-authoring';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

import './temporal-create-life-area-field.css';

type TemporalCreateLifeAreaFieldProps = Readonly<{
  contexts: readonly TemporalCreateContextOption[];
  draft: TemporalCreateU2AuthoringDraft;
  onLifeAreaChange: (value: TemporalCreateU2LifeAreaDraft) => void;
  onItemColorChange: (value: string | null) => void;
  onLegacyContextChange: (contextId: string) => void;
}>;

const DEFAULT_COLOR = '#EA5C12';
const COLOR_PRESETS = Object.freeze([
  DEFAULT_COLOR,
  '#FF3B30',
  '#FFD60A',
  '#0A84FF',
  '#30D158',
  '#64D2FF',
  '#5E5CE6',
  '#BF5AF2',
  '#FF375F',
  '#AC8E68',
  '#8E8E93',
  '#F2F2F7',
]);
const RECENT_COLORS_KEY = 'dante.temporal-create.recent-colors';

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
  areas: Awaited<ReturnType<ReturnType<typeof createRemoteTemporalOrganizationDataSource>['load']>>['areas'],
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

function colorFromPointer(
  element: HTMLElement,
  clientX: number,
  clientY: number,
): string {
  const rect = element.getBoundingClientRect();
  const x = clientX - rect.left - rect.width / 2;
  const y = clientY - rect.top - rect.height / 2;
  const radius = Math.min(rect.width, rect.height) / 2;
  const saturation = Math.max(0, Math.min(1, Math.hypot(x, y) / radius));
  const hue = (Math.atan2(y, x) * 180) / Math.PI + 90;
  const normalizedHue = (hue + 360) % 360;
  return hslToHex(normalizedHue, saturation * 100, 52);
}

function hslToHex(h: number, s: number, l: number): string {
  const saturation = s / 100;
  const lightness = l / 100;
  const chroma = (1 - Math.abs(2 * lightness - 1)) * saturation;
  const x = chroma * (1 - Math.abs(((h / 60) % 2) - 1));
  const m = lightness - chroma / 2;
  const [r1, g1, b1] =
    h < 60
      ? [chroma, x, 0]
      : h < 120
        ? [x, chroma, 0]
        : h < 180
          ? [0, chroma, x]
          : h < 240
            ? [0, x, chroma]
            : h < 300
              ? [x, 0, chroma]
              : [chroma, 0, x];
  const toHex = (channel: number) =>
    Math.round((channel + m) * 255)
      .toString(16)
      .padStart(2, '0')
      .toUpperCase();
  return `#${toHex(r1)}${toHex(g1)}${toHex(b1)}`;
}

function readRecentColors(): readonly string[] {
  try {
    const raw = window.localStorage.getItem(RECENT_COLORS_KEY);
    if (!raw) return Object.freeze([]);
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return Object.freeze([]);
    return Object.freeze(
      parsed
        .filter((value): value is string =>
          typeof value === 'string' && /^#[0-9A-F]{6}$/i.test(value),
        )
        .slice(0, 3)
        .map((value) => value.toUpperCase()),
    );
  } catch {
    return Object.freeze([]);
  }
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
  const [customOpen, setCustomOpen] = useState(false);
  const [query, setQuery] = useState(() => selectedLabel(draft));
  const [availableContexts, setAvailableContexts] = useState(contexts);
  const [recentColors, setRecentColors] = useState<readonly string[]>(() =>
    typeof window === 'undefined' ? Object.freeze([]) : readRecentColors(),
  );
  const rootRef = useRef<HTMLDivElement | null>(null);
  const wheelRef = useRef<HTMLButtonElement | null>(null);
  const sourceRef = useRef<ReturnType<typeof createRemoteTemporalOrganizationDataSource> | null>(null);
  const currentColor = selectedColor(draft);

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
    if (!areaOpen && !colorOpen && !customOpen) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setAreaOpen(false);
        setColorOpen(false);
        setCustomOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [areaOpen, colorOpen, customOpen]);

  const filtered = useMemo(() => {
    const needle = normalized(query).toLocaleLowerCase();
    return needle
      ? availableContexts.filter((context) =>
          context.label.toLocaleLowerCase().includes(needle),
        )
      : availableContexts;
  }, [availableContexts, query]);

  const rememberColor = (colorCode: string) => {
    const canonical = colorCode.toUpperCase();
    const next = Object.freeze([
      canonical,
      ...recentColors.filter((color) => color !== canonical),
    ].slice(0, 3));
    setRecentColors(next);
    try {
      window.localStorage.setItem(RECENT_COLORS_KEY, JSON.stringify(next));
    } catch {
      // Recent colors are a local UI convenience only.
    }
  };

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
      (context) => context.label.toLocaleLowerCase() === name.toLocaleLowerCase(),
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
    rememberColor(canonical);
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

  const chooseCustomAt = (clientX: number, clientY: number) => {
    const wheel = wheelRef.current;
    if (!wheel) return;
    changeColor(colorFromPointer(wheel, clientX, clientY));
  };

  const colorLabel =
    draft.lifeArea.kind === 'none'
      ? 'Colore attività o evento'
      : 'Colore Life Area';

  return (
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
            setCustomOpen(false);
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
            <button
              className="temporal-create-life-area-field__color-swatch is-custom"
              type="button"
              aria-label="Colore personalizzato"
              aria-expanded={customOpen}
              title="Colore personalizzato"
              onClick={() => setCustomOpen((current) => !current)}
            >
              <span aria-hidden="true" />
            </button>
            {COLOR_PRESETS.map((color) => (
              <button
                key={color}
                className="temporal-create-life-area-field__color-swatch"
                type="button"
                aria-label={`Colore ${color}`}
                aria-pressed={currentColor === color}
                onClick={() => {
                  changeColor(color);
                  setCustomOpen(false);
                }}
              >
                <span aria-hidden="true" style={{ background: color }} />
              </button>
            ))}
            {recentColors.length > 0 ? (
              <div className="temporal-create-life-area-field__recent" aria-label="Colori recenti">
                {recentColors.map((color) => (
                  <button
                    key={color}
                    type="button"
                    aria-label={`Colore recente ${color}`}
                    onClick={() => changeColor(color)}
                  >
                    <span aria-hidden="true" style={{ background: color }} />
                  </button>
                ))}
              </div>
            ) : null}
            {customOpen ? (
              <div
                className="temporal-create-life-area-field__custom-popover"
                role="dialog"
                aria-label="Colore personalizzato"
              >
                <button
                  ref={wheelRef}
                  className="temporal-create-life-area-field__color-wheel"
                  type="button"
                  aria-label="Scegli un colore dal cerchio"
                  onPointerDown={(event) => {
                    event.currentTarget.setPointerCapture(event.pointerId);
                    chooseCustomAt(event.clientX, event.clientY);
                  }}
                  onPointerMove={(event) => {
                    if (event.currentTarget.hasPointerCapture(event.pointerId)) {
                      chooseCustomAt(event.clientX, event.clientY);
                    }
                  }}
                  onPointerUp={(event) => {
                    if (event.currentTarget.hasPointerCapture(event.pointerId)) {
                      event.currentTarget.releasePointerCapture(event.pointerId);
                    }
                  }}
                >
                  <span
                    className="temporal-create-life-area-field__color-wheel-marker"
                    aria-hidden="true"
                    style={{ background: currentColor }}
                  />
                </button>
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
            setCustomOpen(false);
          }}
          onChange={(event) => stageTypedName(event.currentTarget.value)}
        />
        {query ? (
          <button type="button" aria-label="Rimuovi Life Area" onClick={clear}>
            ×
          </button>
        ) : null}

        {areaOpen ? (
          <div className="temporal-create-life-area-field__options" role="listbox">
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
  );
}
