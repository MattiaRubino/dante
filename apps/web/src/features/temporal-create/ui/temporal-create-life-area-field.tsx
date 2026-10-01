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

const COLOR_PRESETS = Object.freeze([
  '#FF8A3D',
  '#FF5D73',
  '#F4C95D',
  '#FFE66D',
  '#62D394',
  '#2A9D8F',
  '#45C4D9',
  '#5D8CFF',
  '#6574CD',
  '#8B73FF',
  '#C875E6',
  '#8D99AE',
]);
const RECENT_COLORS_KEY = 'dante.temporal-create.recent-colors.v1';
const MAX_RECENT_COLORS = 3;
const COLOR_CODE = /^#[0-9A-F]{6}$/;

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
      return draft.lifeArea.colorCode ?? '#FF8A3D';
    case 'none':
      return draft.itemColorCode ?? '#FF8A3D';
  }
}

function readRecentColors(): readonly string[] {
  if (typeof window === 'undefined') return Object.freeze([]);
  try {
    const parsed: unknown = JSON.parse(window.localStorage.getItem(RECENT_COLORS_KEY) ?? '[]');
    if (!Array.isArray(parsed)) return Object.freeze([]);
    return Object.freeze(
      parsed
        .filter((value): value is string =>
          typeof value === 'string' && COLOR_CODE.test(value.toUpperCase()),
        )
        .map((value) => value.toUpperCase())
        .filter((value, index, all) => all.indexOf(value) === index)
        .slice(0, MAX_RECENT_COLORS),
    );
  } catch {
    return Object.freeze([]);
  }
}

function writeRecentColors(colors: readonly string[]): void {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(RECENT_COLORS_KEY, JSON.stringify(colors));
  } catch {
    // Recent swatches are presentation convenience only.
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

export function TemporalCreateLifeAreaField({
  contexts,
  draft,
  onLifeAreaChange,
  onItemColorChange,
  onLegacyContextChange,
}: TemporalCreateLifeAreaFieldProps) {
  const [areaOpen, setAreaOpen] = useState(false);
  const [colorOpen, setColorOpen] = useState(false);
  const [query, setQuery] = useState(() => selectedLabel(draft));
  const [availableContexts, setAvailableContexts] = useState(contexts);
  const [catalogLoading, setCatalogLoading] = useState(
    () => import.meta.env.MODE !== 'test',
  );
  const [recentColors, setRecentColors] = useState<readonly string[]>(readRecentColors);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const customColorRef = useRef<HTMLInputElement | null>(null);
  const sourceRef = useRef<ReturnType<typeof createRemoteTemporalOrganizationDataSource> | null>(null);
  const currentColor = selectedColor(draft);

  useEffect(() => {
    setQuery(selectedLabel(draft));
  }, [draft.lifeArea]);

  useEffect(() => {
    setAvailableContexts(contexts);
  }, [contexts]);

  useEffect(() => {
    if (import.meta.env.MODE === 'test') {
      setCatalogLoading(false);
      return;
    }
    sourceRef.current ??= createRemoteTemporalOrganizationDataSource();
    let cancelled = false;
    setCatalogLoading(true);
    void sourceRef.current.load().then(
      (snapshot) => {
        if (!cancelled) {
          setAvailableContexts(canonicalOptions(contexts, snapshot.areas));
          setCatalogLoading(false);
        }
      },
      () => {
        if (!cancelled) setCatalogLoading(false);
      },
    );
    return () => {
      cancelled = true;
    };
  }, [contexts]);

  useEffect(() => {
    if (!areaOpen && !colorOpen) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setAreaOpen(false);
        setColorOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [areaOpen, colorOpen]);

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
        colorCode: context.colorCode ?? null,
        colorChanged: false,
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
      draft.lifeArea.kind === 'new' ? draft.lifeArea.colorCode : null;
    onLifeAreaChange(
      Object.freeze({ kind: 'new' as const, name, colorCode: previousColor }),
    );
    onItemColorChange(null);
    onLegacyContextChange('');
    setAreaOpen(true);
  };

  const rememberColor = (colorCode: string) => {
    const canonical = colorCode.toUpperCase();
    const next = Object.freeze(
      [canonical, ...recentColors.filter((value) => value !== canonical)].slice(
        0,
        MAX_RECENT_COLORS,
      ),
    );
    setRecentColors(next);
    writeRecentColors(next);
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
              title="Colore personalizzato"
              onClick={() => customColorRef.current?.click()}
            >
              <span aria-hidden="true" />
            </button>
            {recentColors.map((color, index) => (
              <button
                key={`recent-${color}`}
                className="temporal-create-life-area-field__color-swatch is-recent"
                type="button"
                aria-label={`Colore recente ${index + 1}: ${color}`}
                aria-pressed={currentColor === color}
                title="Colore recente"
                onClick={() => {
                  changeColor(color);
                  setColorOpen(false);
                }}
              >
                <span aria-hidden="true" style={{ background: color }} />
              </button>
            ))}
            {COLOR_PRESETS.map((color) => (
              <button
                key={color}
                className="temporal-create-life-area-field__color-swatch"
                type="button"
                aria-label={`Colore ${color}`}
                aria-pressed={currentColor === color}
                onClick={() => {
                  changeColor(color);
                  setColorOpen(false);
                }}
              >
                <span aria-hidden="true" style={{ background: color }} />
              </button>
            ))}
            <input
              ref={customColorRef}
              className="temporal-create-life-area-field__native-color"
              type="color"
              value={currentColor}
              aria-label="Scegli colore personalizzato"
              onChange={(event) => {
                changeColor(event.currentTarget.value);
                setColorOpen(false);
              }}
            />
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
            {catalogLoading ? (
              <div className="temporal-create-life-area-field__loading" role="status">
                Aggiornamento Life Area…
              </div>
            ) : (
              filtered.map((context) => (
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
              ))
            )}
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