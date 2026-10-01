import { useEffect, useMemo, useRef, useState } from 'react';
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

const DEFAULT_COLOR = TEMPORAL_CREATE_DEFAULT_COLOR;
const COLOR_PRESETS = Object.freeze([
  '#D50000',
  '#E67C73',
  '#AD1457',
  '#F4511E',
  DEFAULT_COLOR,
  '#EF6C00',
  '#F6BF26',
  '#FFD600',
  '#C0CA33',
  '#7CB342',
  '#33B679',
  '#0B8043',
  '#009688',
  '#26A69A',
  '#039BE5',
  '#4285F4',
  '#3F51B5',
  '#7986CB',
  '#673AB7',
  '#8E24AA',
  '#B39DDB',
  '#795548',
  '#616161',
  '#E0E0E0',
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
  const [query, setQuery] = useState(() => selectedLabel(draft));
  const [availableContexts, setAvailableContexts] = useState(contexts);
  const [recentColors] = useState<readonly string[]>(() =>
    typeof window === 'undefined'
      ? Object.freeze([])
      : readTemporalCreateRecentUsedColors(),
  );
  const rootRef = useRef<HTMLDivElement | null>(null);
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
    if (!areaOpen && !colorOpen) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setAreaOpen(false);
        setColorOpen(false);
        setCustomColorOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [areaOpen, colorOpen]);

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
            setCustomColorOpen(false);
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
                onClick={() => setCustomColorOpen((current) => !current)}
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
                  onClick={() => changeColor(color)}
                >
                  <span aria-hidden="true" style={{ background: color }} />
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
                      onClick={() => changeColor(color)}
                    >
                      <span aria-hidden="true" style={{ background: color }} />
                    </button>
                  ))}
                </div>
              </div>
            ) : null}

            {customColorOpen ? (
              <div className="temporal-create-life-area-field__custom-picker">
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
