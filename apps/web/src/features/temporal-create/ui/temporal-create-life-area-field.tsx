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
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState(() => selectedLabel(draft));
  const [availableContexts, setAvailableContexts] = useState(contexts);
  const rootRef = useRef<HTMLDivElement | null>(null);
  const sourceRef = useRef<ReturnType<typeof createRemoteTemporalOrganizationDataSource> | null>(null);

  useEffect(() => {
    setQuery(selectedLabel(draft));
  }, [draft.lifeArea]);

  useEffect(() => {
    setAvailableContexts(contexts);
  }, [contexts]);

  useEffect(() => {
    if (!open || import.meta.env.MODE === 'test') return;
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
  }, [contexts, open]);

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
    setOpen(false);
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
      setOpen(true);
      return;
    }
    const previousColor =
      draft.lifeArea.kind === 'new' ? draft.lifeArea.colorCode : null;
    onLifeAreaChange(
      Object.freeze({ kind: 'new' as const, name, colorCode: previousColor }),
    );
    onItemColorChange(null);
    onLegacyContextChange('');
    setOpen(true);
  };

  const changeColor = (colorCode: string) => {
    const canonical = colorCode.toUpperCase();
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

  return (
    <div ref={rootRef} className="temporal-create-life-area-field">
      <div className="temporal-create-life-area-field__input-row">
        <input
          type="text"
          value={query}
          placeholder="Life Area (opzionale)"
          aria-label="Life Area (opzionale)"
          autoComplete="off"
          onFocus={() => setOpen(true)}
          onChange={(event) => stageTypedName(event.currentTarget.value)}
        />
        <label
          className="temporal-create-life-area-field__color"
          title={
            draft.lifeArea.kind === 'none'
              ? 'Colore attività/evento'
              : 'Colore Life Area'
          }
        >
          <span
            aria-hidden="true"
            style={{ background: selectedColor(draft) }}
          />
          <input
            type="color"
            value={selectedColor(draft)}
            aria-label={
              draft.lifeArea.kind === 'none'
                ? 'Colore attività o evento'
                : 'Colore Life Area'
            }
            onChange={(event) => changeColor(event.currentTarget.value)}
          />
        </label>
        {query ? (
          <button type="button" aria-label="Rimuovi Life Area" onClick={clear}>
            ×
          </button>
        ) : null}
      </div>

      {open ? (
        <div className="temporal-create-life-area-field__options" role="listbox">
          <button
            type="button"
            role="option"
            aria-selected={draft.lifeArea.kind === 'none'}
            onClick={() => {
              clear();
              setOpen(false);
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
  );
}
