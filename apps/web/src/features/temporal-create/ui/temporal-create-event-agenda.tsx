import { useRef, type KeyboardEvent } from 'react';
import { useTranslation } from 'react-i18next';

import './temporal-create-event-agenda.css';

type TemporalCreateEventAgendaProps = Readonly<{
  parts: readonly string[];
  onChange: (parts: readonly string[]) => void;
}>;

type ScalettaRowProps = Readonly<{
  part: string;
  index: number;
  total: number;
  onChange: (index: number, value: string) => void;
  onMove: (index: number, direction: -1 | 1) => void;
  onRemove: (index: number) => void;
}>;

function ScalettaRow({
  part,
  index,
  total,
  onChange,
  onMove,
  onRemove,
}: ScalettaRowProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');

  const onKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.altKey && event.key === 'ArrowUp' && index > 0) {
      event.preventDefault();
      onMove(index, -1);
      return;
    }
    if (event.altKey && event.key === 'ArrowDown' && index < total - 1) {
      event.preventDefault();
      onMove(index, 1);
    }
  };

  return (
    <div
      className="temporal-create-event-agenda__part"
      data-temporal-create-agenda-part
      role="listitem"
    >
      <span className="temporal-create-event-agenda__position" aria-hidden="true">
        {index + 1}
      </span>
      <span
        className="temporal-create-event-agenda__divider"
        aria-hidden="true"
      />
      <input
        data-temporal-create-agenda-input
        data-agenda-index={index}
        type="text"
        value={part}
        maxLength={300}
        onChange={(event) => onChange(index, event.currentTarget.value)}
        onKeyDown={onKeyDown}
        aria-label={
          italian
            ? `Punto scaletta ${index + 1}`
            : `Run of show item ${index + 1}`
        }
        placeholder={italian ? 'Punto della scaletta' : 'Run of show item'}
        autoComplete="off"
      />
      <div className="temporal-create-event-agenda__actions">
        <button
          type="button"
          disabled={index === 0}
          onClick={() => onMove(index, -1)}
          aria-label={italian ? 'Sposta su' : 'Move up'}
        >
          ↑
        </button>
        <button
          type="button"
          disabled={index === total - 1}
          onClick={() => onMove(index, 1)}
          aria-label={italian ? 'Sposta giù' : 'Move down'}
        >
          ↓
        </button>
        <button
          type="button"
          className="is-remove"
          onClick={() => onRemove(index)}
          aria-label={italian ? 'Rimuovi punto' : 'Remove item'}
        >
          ×
        </button>
      </div>
    </div>
  );
}

export function TemporalCreateEventAgenda({
  parts,
  onChange,
}: TemporalCreateEventAgendaProps) {
  const { i18n } = useTranslation('common');
  const italian = i18n.language.toLowerCase().startsWith('it');
  const rootRef = useRef<HTMLElement>(null);

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

  const updatePart = (index: number, value: string) => {
    const next = [...parts];
    next[index] = value;
    publish(next);
  };

  const movePart = (index: number, direction: -1 | 1) => {
    const target = index + direction;
    if (target < 0 || target >= parts.length) return;
    const next = [...parts];
    [next[index], next[target]] = [next[target] ?? '', next[index] ?? ''];
    publish(next);
    focusPart(target);
  };

  const removePart = (index: number) => {
    publish(parts.filter((_, candidateIndex) => candidateIndex !== index));
    requestAnimationFrame(() => {
      const nextIndex = Math.min(index, parts.length - 2);
      if (nextIndex >= 0) focusPart(nextIndex);
    });
  };

  const addPart = () => {
    const nextIndex = parts.length;
    publish([...parts, '']);
    focusPart(nextIndex);
  };

  return (
    <section
      ref={rootRef}
      className="temporal-create-event-agenda"
      data-temporal-create-agenda
      aria-label={italian ? 'Scaletta evento' : 'Event run of show'}
    >
      {parts.length > 0 ? (
        <div className="temporal-create-event-agenda__list" role="list">
          <div className="temporal-create-event-agenda__group-label">
            {italian ? 'Scaletta' : 'Run of show'}
          </div>
          {parts.map((part, index) => (
            <ScalettaRow
              key={index}
              part={part}
              index={index}
              total={parts.length}
              onChange={updatePart}
              onMove={movePart}
              onRemove={removePart}
            />
          ))}
        </div>
      ) : null}

      <div className="temporal-create-event-agenda__root-actions">
        <button
          className="temporal-create-event-agenda__add"
          type="button"
          onClick={addPart}
          aria-label={italian ? 'Aggiungi punto alla scaletta' : 'Add run of show item'}
        >
          <span aria-hidden="true">＋</span>
          {italian ? 'Scaletta' : 'Run of show'}
        </button>
      </div>
    </section>
  );
}
