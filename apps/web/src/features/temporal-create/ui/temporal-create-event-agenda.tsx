import { useRef, useState, type KeyboardEvent } from 'react';
import { useTranslation } from 'react-i18next';

import './temporal-create-event-agenda.css';

type TemporalCreateEventAgendaProps = Readonly<{
  parts: readonly string[];
  onChange: (parts: readonly string[]) => void;
}>;

type AgendaPartEditorProps = Readonly<{
  part: string;
  index: number;
  total: number;
  onCommit: (index: number, value: string) => void;
  onMove: (index: number, direction: -1 | 1, value: string) => void;
  onRemove: (index: number) => void;
}>;

function AgendaPartEditor({
  part,
  index,
  total,
  onCommit,
  onMove,
  onRemove,
}: AgendaPartEditorProps) {
  const { t } = useTranslation('common');
  const [draft, setDraft] = useState(part);
  const commit = () => onCommit(index, draft);

  const onKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.altKey && event.key === 'ArrowUp' && index > 0) {
      event.preventDefault();
      onMove(index, -1, draft);
      return;
    }
    if (event.altKey && event.key === 'ArrowDown' && index < total - 1) {
      event.preventDefault();
      onMove(index, 1, draft);
      return;
    }
    if (event.key === 'Enter') {
      event.preventDefault();
      event.currentTarget.blur();
      return;
    }
    if (event.key === 'Escape' && draft !== part) {
      event.preventDefault();
      event.stopPropagation();
      setDraft(part);
    }
  };

  return (
    <div
      className="temporal-create-event-agenda__part"
      data-temporal-create-agenda-part
      role="listitem"
    >
      <span
        className="temporal-create-event-agenda__position"
        aria-hidden="true"
      >
        {index + 1}
      </span>
      <input
        data-temporal-create-agenda-input
        data-agenda-index={index}
        type="text"
        value={draft}
        onChange={(event) => setDraft(event.currentTarget.value)}
        onBlur={commit}
        onKeyDown={onKeyDown}
        aria-label={t(
          ($) => $.common.home.timeline.create.eventDetails.agendaEdit,
          { position: index + 1 },
        )}
        aria-keyshortcuts="Alt+ArrowUp Alt+ArrowDown"
        autoComplete="off"
      />
      <div className="temporal-create-event-agenda__actions">
        <button
          type="button"
          disabled={index === 0}
          onClick={() => onMove(index, -1, draft)}
          aria-label={t(
            ($) => $.common.home.timeline.create.eventDetails.agendaMoveUp,
            { position: index + 1 },
          )}
        >
          <span aria-hidden="true">↑</span>
        </button>
        <button
          type="button"
          disabled={index === total - 1}
          onClick={() => onMove(index, 1, draft)}
          aria-label={t(
            ($) => $.common.home.timeline.create.eventDetails.agendaMoveDown,
            { position: index + 1 },
          )}
        >
          <span aria-hidden="true">↓</span>
        </button>
        <button
          type="button"
          onClick={() => onRemove(index)}
          aria-label={t(
            ($) => $.common.home.timeline.create.eventDetails.agendaRemove,
            { position: index + 1 },
          )}
        >
          <span aria-hidden="true">×</span>
        </button>
      </div>
    </div>
  );
}

export function TemporalCreateEventAgenda({
  parts,
  onChange,
}: TemporalCreateEventAgendaProps) {
  const { t } = useTranslation('common');
  const [newPart, setNewPart] = useState('');
  const rootRef = useRef<HTMLFieldSetElement>(null);
  const newPartRef = useRef<HTMLInputElement>(null);

  const publish = (next: readonly string[]) => {
    onChange(Object.freeze([...next]));
  };

  const focusPart = (index: number) => {
    requestAnimationFrame(() => {
      rootRef.current
        ?.querySelector<HTMLInputElement>(
          `[data-temporal-create-agenda-input][data-agenda-index="${index}"]`,
        )
        ?.focus();
    });
  };

  const focusAfterRemoval = (index: number, nextLength: number) => {
    requestAnimationFrame(() => {
      if (nextLength === 0) {
        newPartRef.current?.focus();
        return;
      }
      const target = Math.min(index, nextLength - 1);
      rootRef.current
        ?.querySelector<HTMLInputElement>(
          `[data-temporal-create-agenda-input][data-agenda-index="${target}"]`,
        )
        ?.focus();
    });
  };

  const commitPart = (index: number, value: string) => {
    const normalized = value.trim();
    if (normalized.length === 0) {
      const next = parts.filter(
        (_, candidateIndex) => candidateIndex !== index,
      );
      if (next.length !== parts.length) {
        publish(next);
        focusAfterRemoval(index, next.length);
      }
      return;
    }
    if (parts[index] === normalized) {
      return;
    }
    const next = [...parts];
    next[index] = normalized;
    publish(next);
  };

  const movePart = (index: number, direction: -1 | 1, value: string) => {
    const target = index + direction;
    if (target < 0 || target >= parts.length) {
      return;
    }
    const normalized = value.trim();
    if (normalized.length === 0) {
      const next = parts.filter(
        (_, candidateIndex) => candidateIndex !== index,
      );
      publish(next);
      focusAfterRemoval(index, next.length);
      return;
    }
    const next = [...parts];
    next[index] = normalized;
    [next[index], next[target]] = [next[target] ?? '', next[index] ?? ''];
    publish(next);
    focusPart(target);
  };

  const removePart = (index: number) => {
    const next = parts.filter((_, candidateIndex) => candidateIndex !== index);
    publish(next);
    focusAfterRemoval(index, next.length);
  };

  const addPart = () => {
    const normalized = newPart.trim();
    if (normalized.length === 0) {
      return;
    }
    publish([...parts, normalized]);
    setNewPart('');
    requestAnimationFrame(() => newPartRef.current?.focus());
  };

  return (
    <fieldset
      ref={rootRef}
      className="temporal-create-event-agenda"
      data-temporal-create-agenda
    >
      <legend>
        {t(($) => $.common.home.timeline.create.eventDetails.agenda)}
      </legend>
      <p className="temporal-create-event-agenda__description">
        {t(($) => $.common.home.timeline.create.eventDetails.agendaDescription)}
      </p>

      {parts.length > 0 ? (
        <div className="temporal-create-event-agenda__list" role="list">
          {parts.map((part, index) => (
            <AgendaPartEditor
              key={`${index}:${part}`}
              part={part}
              index={index}
              total={parts.length}
              onCommit={commitPart}
              onMove={movePart}
              onRemove={removePart}
            />
          ))}
        </div>
      ) : (
        <p className="temporal-create-event-agenda__empty">
          {t(($) => $.common.home.timeline.create.eventDetails.agendaEmpty)}
        </p>
      )}

      <div className="temporal-create-event-agenda__add">
        <label className="temporal-create-control">
          <span>
            {t(($) => $.common.home.timeline.create.eventDetails.agendaNewItem)}
          </span>
          <input
            ref={newPartRef}
            type="text"
            value={newPart}
            onChange={(event) => setNewPart(event.currentTarget.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                event.preventDefault();
                addPart();
                return;
              }
              if (event.key === 'Escape' && newPart.length > 0) {
                event.preventDefault();
                event.stopPropagation();
                setNewPart('');
              }
            }}
            placeholder={t(
              ($) =>
                $.common.home.timeline.create.eventDetails
                  .agendaNewItemPlaceholder,
            )}
            autoComplete="off"
          />
        </label>
        <button
          className="temporal-create-event-agenda__add-button"
          type="button"
          onClick={addPart}
          disabled={newPart.trim().length === 0}
        >
          {t(($) => $.common.home.timeline.create.eventDetails.agendaAdd)}
        </button>
      </div>

      <p className="temporal-create-event-agenda__hint">
        {t(
          ($) => $.common.home.timeline.create.eventDetails.agendaKeyboardHint,
        )}
      </p>
    </fieldset>
  );
}
