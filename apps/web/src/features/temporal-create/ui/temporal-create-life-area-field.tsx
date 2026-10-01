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
  '#D50000',
  '#E67C73',
  '#F4511E',
  '#F6BF26',
  '#FFD600',
  '#33B679',
  '#0B8043',
  '#039BE5',
  '#4285F4',
  '#3F51B5',
  '#7986CB',
  '#8E24AA',
  '#B39DDB',
  '#AD1457',
  '#616161',
  '#A79B8E',
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

function readRecentColors(): readonly string[] {
  try {
    const raw = window.localStorage.getItem(RECENT_COLORS_KEY);
    if (!raw) return Object.freeze([]);
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return Object.freeze([]);
    return Object.freeze(
      parsed
        .filter(
          (value): value is string =>
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
  const [query, setQuery] = useState(() => selectedLabel(draft));
  const [availableContexts, setAvailableContexts] = useState(contexts);
  const [recentColors, setRecentColors] = useState<readonly string[]>(() =>
    typeof window === 'undefined' ? Object.freeze([]) : readRecentColors(),
  );
  const rootRef = useRef<HTMLDivElement | null>(null);
  const sourceRef = useRef<
    ReturnType<typeof createRemoteTemporalOrganizationDataSource> | null
  >(null);
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

  const rememberColor = (colorCode: string) => {
    const canonical = colorCode.toUpperCase();
    const next = Object.freeze(
      [
        canonical,
        ...recentColors.filter((color) => color !== canonical),
      ].slice(0, 3),
    );
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
            {COLOR_PRESETS.map((color) => (
              <button
                key={color}
                className="temporal-create-life-area-field__color-swatch"
                type="button"
                aria-label={`Colore ${color}`}
                aria-pressed={currentColor === color}
                onClick={() => changeColor(color)}
              >
                <span aria-hidden="true" style={{ background: color }} />
              </button>
            ))}
            {recentColors.length > 0 ? (
              <div
                className="temporal-create-life-area-field__recent"
                aria-label="Colori recenti"
              >
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
  );
}
