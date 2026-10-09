import { useEffect, useRef, useState } from 'react';

import { createRemoteTemporalOrganizationDataSource } from '../../temporal/remote-organization';
import type {
  TemporalCreateU2AuthoringDraft,
  TemporalCreateU2LifeAreaDraft,
} from '../model/temporal-create-u2-authoring';
import { TemporalColorControl, TEMPORAL_DEFAULT_COLOR } from './temporal-color-control';
import { TemporalLifeAreaSelect, type TemporalLifeAreaOption } from './temporal-life-area-select';
import type { TemporalCreateContextOption } from './temporal-create-ui-types';

import './temporal-create-life-area-field.css';

type TemporalCreateLifeAreaFieldProps = Readonly<{
  contexts: readonly TemporalCreateContextOption[];
  draft: TemporalCreateU2AuthoringDraft;
  onLifeAreaChange: (value: TemporalCreateU2LifeAreaDraft) => void;
  onItemColorChange: (value: string | null) => void;
  onLegacyContextChange: (contextId: string) => void;
}>;

const DEFAULT_COLOR = TEMPORAL_DEFAULT_COLOR;
const UNASSIGNED_PRESENTATION_CONTEXT_ID = 'legacy-unassigned';

function authorableContexts(
  contexts: readonly TemporalCreateContextOption[],
): readonly TemporalCreateContextOption[] {
  return Object.freeze(
    contexts.filter((context) => context.id !== UNASSIGNED_PRESENTATION_CONTEXT_ID),
  );
}
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
  const byRef = new Map(
    authorableContexts(contexts).map((context) => [context.id, context]),
  );
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
  const [query, setQuery] = useState(() => selectedLabel(draft));
  const [availableContexts, setAvailableContexts] = useState(() =>
    authorableContexts(contexts),
  );
  const sourceRef = useRef<
    ReturnType<typeof createRemoteTemporalOrganizationDataSource> | null
  >(null);

  useEffect(() => {
    setQuery(selectedLabel(draft));
  }, [draft.lifeArea]);

  useEffect(() => {
    setAvailableContexts(authorableContexts(contexts));
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

  const choose = (choice: TemporalLifeAreaOption) => {
    const context = availableContexts.find((candidate) => candidate.id === choice.id);
    if (!context) return;
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
      return;
    }
    const previousColor = selectedColor(draft);
    onLifeAreaChange(
      Object.freeze({ kind: 'new' as const, name, colorCode: previousColor }),
    );
    onItemColorChange(null);
    onLegacyContextChange('');
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
    <>
      <div className="temporal-create-life-area-field" data-create-path="contextId">
        <TemporalColorControl value={selectedColor(draft)} label={colorLabel}
          onChange={changeColor} />

        <TemporalLifeAreaSelect query={query} options={availableContexts}
          selectedId={draft.lifeArea.kind === 'existing' ? draft.lifeArea.lifeAreaRef : null}
          onQueryChange={stageTypedName} onChoose={choose} onClear={clear} />
      </div>
    </>
  );
}
