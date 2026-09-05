import {
  useEffect,
  useId,
  useMemo,
  useRef,
  useState,
  type KeyboardEvent,
} from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalCreateContextInput,
  TemporalCreateContextOption,
  TemporalCreateContextTone,
} from './temporal-create-ui-types';

import './temporal-create-context-picker.css';

const CONTEXT_TONES: readonly TemporalCreateContextTone[] = Object.freeze([
  'focus',
  'meeting',
  'health',
  'creative',
  'personal',
  'urgent',
]);

type TemporalCreateContextPickerProps = Readonly<{
  value: string;
  contexts: readonly TemporalCreateContextOption[];
  onChange: (contextId: string) => void;
  onCreateContext:
    ((input: TemporalCreateContextInput) => TemporalCreateContextOption) | null;
}>;

function normalizedQuery(value: string): string {
  return value.trim().toLocaleLowerCase();
}

export function TemporalCreateContextPicker({
  value,
  contexts,
  onChange,
  onCreateContext,
}: TemporalCreateContextPickerProps) {
  const { t } = useTranslation('common');
  const popupId = useId();
  const rootRef = useRef<HTMLDivElement | null>(null);
  const searchRef = useRef<HTMLInputElement | null>(null);
  const nameRef = useRef<HTMLInputElement | null>(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [creating, setCreating] = useState(false);
  const [newLabel, setNewLabel] = useState('');
  const [newTone, setNewTone] = useState<TemporalCreateContextTone>('focus');

  const selected =
    contexts.find((context) => context.id === value) ?? contexts[0] ?? null;
  const normalized = normalizedQuery(query);
  const filtered = useMemo(
    () =>
      normalized.length === 0
        ? contexts
        : contexts.filter((context) =>
            context.label.toLocaleLowerCase().includes(normalized),
          ),
    [contexts, normalized],
  );

  const resetTransientState = () => {
    setQuery('');
    setCreating(false);
    setNewLabel('');
    setNewTone('focus');
  };

  useEffect(() => {
    if (!open) {
      return;
    }

    const frame = requestAnimationFrame(() => searchRef.current?.focus());
    const closeOutside = (event: globalThis.PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target)
      ) {
        setOpen(false);
        setQuery('');
        setCreating(false);
        setNewLabel('');
        setNewTone('focus');
      }
    };
    document.addEventListener('pointerdown', closeOutside, true);
    return () => {
      cancelAnimationFrame(frame);
      document.removeEventListener('pointerdown', closeOutside, true);
    };
  }, [open]);

  const close = () => {
    setOpen(false);
    resetTransientState();
    requestAnimationFrame(() =>
      rootRef.current
        ?.querySelector<HTMLButtonElement>('.temporal-create-context-trigger')
        ?.focus(),
    );
  };

  const toggle = () => {
    if (open) {
      setOpen(false);
      resetTransientState();
      return;
    }
    resetTransientState();
    setOpen(true);
  };

  const chooseContext = (contextId: string) => {
    onChange(contextId);
    setOpen(false);
    resetTransientState();
  };

  const keyDown = (event: KeyboardEvent<HTMLDivElement>) => {
    if (event.key === 'Escape') {
      event.preventDefault();
      event.stopPropagation();
      close();
    }
  };

  const beginCreate = () => {
    setCreating(true);
    setNewLabel(query.trim());
    requestAnimationFrame(() => nameRef.current?.focus());
  };

  const cancelCreate = () => {
    setCreating(false);
    setNewLabel('');
    setNewTone('focus');
    requestAnimationFrame(() => searchRef.current?.focus());
  };

  const submitNewContext = () => {
    const label = newLabel.trim().replace(/\s+/g, ' ');
    if (!label || onCreateContext === null) {
      nameRef.current?.focus();
      return;
    }
    const created = onCreateContext({ label, tone: newTone });
    onChange(created.id);
    setOpen(false);
    resetTransientState();
  };

  const createLabel = `${t(($) => $.common.home.topbar.create)} ${t(
    ($) => $.common.home.timeline.create.context,
  ).toLocaleLowerCase()}`;
  const searchLabel = `${t(($) => $.common.home.topbar.search)} ${t(
    ($) => $.common.home.timeline.create.context,
  ).toLocaleLowerCase()}`;

  return (
    <div
      ref={rootRef}
      className="temporal-create-context-picker"
      data-create-path="contextId"
      onKeyDown={keyDown}
    >
      <span className="temporal-create-context-picker__label">
        {t(($) => $.common.home.timeline.create.context)}
      </span>
      <button
        className="temporal-create-context-trigger"
        type="button"
        aria-haspopup="dialog"
        aria-expanded={open}
        aria-controls={open ? popupId : undefined}
        onClick={toggle}
      >
        <span
          className="temporal-create-context-swatch"
          data-context-tone={selected?.tone ?? 'personal'}
          aria-hidden="true"
        />
        <span className="temporal-create-context-trigger__label">
          {selected?.label ?? t(($) => $.common.home.timeline.create.context)}
        </span>
        <span
          className="temporal-create-context-trigger__chevron"
          aria-hidden="true"
        >
          ▾
        </span>
      </button>

      {open ? (
        <div
          id={popupId}
          className="temporal-create-context-popover"
          role="dialog"
          aria-label={t(($) => $.common.home.timeline.create.context)}
        >
          {!creating ? (
            <>
              <div className="temporal-create-context-search">
                <span aria-hidden="true">⌕</span>
                <input
                  ref={searchRef}
                  type="search"
                  value={query}
                  onChange={(event) => setQuery(event.currentTarget.value)}
                  aria-label={searchLabel}
                  placeholder={searchLabel}
                  autoComplete="off"
                />
              </div>

              <div
                className="temporal-create-context-options"
                role="listbox"
                aria-label={t(($) => $.common.home.timeline.create.context)}
              >
                {filtered.map((context) => (
                  <button
                    key={context.id}
                    type="button"
                    role="option"
                    aria-selected={context.id === value}
                    className={context.id === value ? 'is-selected' : ''}
                    data-context-tone={context.tone}
                    onClick={() => chooseContext(context.id)}
                  >
                    <span
                      className="temporal-create-context-swatch"
                      data-context-tone={context.tone}
                      aria-hidden="true"
                    />
                    <span>{context.label}</span>
                    {context.local ? (
                      <small>
                        {t(($) => $.common.home.timeline.create.draft)}
                      </small>
                    ) : null}
                    <i aria-hidden="true">✓</i>
                  </button>
                ))}
              </div>

              {onCreateContext ? (
                <button
                  className="temporal-create-context-new"
                  type="button"
                  onClick={beginCreate}
                >
                  <span aria-hidden="true">＋</span>
                  <span>{createLabel}</span>
                </button>
              ) : null}
            </>
          ) : (
            <div className="temporal-create-context-create">
              <label>
                <span>{t(($) => $.common.home.timeline.create.context)}</span>
                <input
                  ref={nameRef}
                  type="text"
                  value={newLabel}
                  onChange={(event) => setNewLabel(event.currentTarget.value)}
                  autoComplete="off"
                />
              </label>

              <div
                className="temporal-create-context-tone-grid"
                role="radiogroup"
                aria-label={t(($) => $.common.home.timeline.create.context)}
              >
                {CONTEXT_TONES.map((tone) => {
                  const reference =
                    contexts.find((context) => context.tone === tone)?.label ??
                    tone;
                  return (
                    <button
                      key={tone}
                      type="button"
                      role="radio"
                      aria-checked={newTone === tone}
                      aria-label={`${t(($) => $.common.home.timeline.create.context)} · ${reference}`}
                      className={newTone === tone ? 'is-selected' : ''}
                      data-context-tone={tone}
                      onClick={() => setNewTone(tone)}
                    >
                      <span aria-hidden="true" />
                    </button>
                  );
                })}
              </div>

              <div className="temporal-create-context-create__actions">
                <button type="button" onClick={cancelCreate}>
                  {t(($) => $.common.home.timeline.create.cancel)}
                </button>
                <button
                  type="button"
                  className="is-primary"
                  disabled={newLabel.trim().length === 0}
                  onClick={submitNewContext}
                >
                  {createLabel}
                </button>
              </div>
            </div>
          )}
        </div>
      ) : null}
    </div>
  );
}
