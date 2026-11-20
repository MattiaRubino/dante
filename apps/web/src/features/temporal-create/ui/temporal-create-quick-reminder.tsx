import {
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
  type CSSProperties,
} from 'react';
import { createPortal } from 'react-dom';

import type { TemporalCreateFields } from '../model/temporal-create-session';
import {
  TEMPORAL_CREATE_REMINDER_OPTIONS,
  temporalCreateDurationLabel,
} from './temporal-create-field-shared';

import './temporal-create-quick-reminder.css';

type Props = Readonly<{
  fields: TemporalCreateFields;
  onPatch: (patch: Partial<TemporalCreateFields>) => void;
}>;

function BellIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M6.5 9a5.5 5.5 0 0 1 11 0v3.4l1.5 2.1H5l1.5-2.1V9Z" />
      <path d="M9.5 17.5a2.7 2.7 0 0 0 5 0" />
    </svg>
  );
}

function reminderLabel(value: number | null): string {
  if (value === null) return 'Ricorda · Nessuno';
  if (value === 0) return 'Ricorda · All’orario';
  if (value === 1440) return 'Ricorda · 1 giorno prima';
  return `Ricorda · ${temporalCreateDurationLabel(value)} prima`;
}

export function TemporalReminderControl({
  value,
  onChange,
  disabled = false,
  unavailableReason = 'Il promemoria richiede un orario preciso.',
}: Readonly<{
  value: number | null;
  onChange: (value: number | null) => void;
  disabled?: boolean;
  unavailableReason?: string;
}>) {
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(0);
  const [popupPosition, setPopupPosition] = useState<CSSProperties>({});
  const rootRef = useRef<HTMLDivElement>(null);
  const popupRef = useRef<HTMLDivElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  const listId = useId();
  const options = TEMPORAL_CREATE_REMINDER_OPTIONS.includes(value)
    ? TEMPORAL_CREATE_REMINDER_OPTIONS
    : [value, ...TEMPORAL_CREATE_REMINDER_OPTIONS];
  const selectedIndex = options.indexOf(value);

  useEffect(() => {
    if (disabled) setOpen(false);
  }, [disabled]);

  useLayoutEffect(() => {
    if (!open) return;
    const position = () => {
      const rect = rootRef.current?.getBoundingClientRect();
      if (!rect) return;
      const desiredHeight = Math.min(
        320,
        popupRef.current?.scrollHeight || 320,
      );
      const roomBelow = window.innerHeight - rect.bottom - 8;
      const roomAbove = rect.top - 8;
      const above = roomBelow < desiredHeight && roomAbove > roomBelow;
      const menuHeight = Math.min(
        desiredHeight,
        Math.max(40, above ? roomAbove : roomBelow),
      );
      setPopupPosition({
        top: above ? rect.top - menuHeight - 2 : rect.bottom + 2,
        left: rect.left + 7,
        width: Math.max(0, rect.width - 14),
        maxHeight: menuHeight,
      });
    };
    position();
    window.addEventListener('resize', position);
    window.addEventListener('scroll', position, true);
    return () => {
      window.removeEventListener('resize', position);
      window.removeEventListener('scroll', position, true);
    };
  }, [open]);

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !rootRef.current?.contains(event.target) &&
        !popupRef.current?.contains(event.target)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [open]);

  const choose = (next: number | null) => {
    onChange(next);
    setOpen(false);
    triggerRef.current?.focus();
  };

  return (
    <div
      ref={rootRef}
      className={`temporal-create-quick-reminder${disabled ? ' is-disabled' : ''}`}
      title={
        disabled
          ? unavailableReason
          : 'Promemoria relativo all’inizio dello Schedule.'
      }
    >
      <span className="temporal-create-quick-reminder__icon" aria-hidden="true">
        <BellIcon />
      </span>
      <span
        className="temporal-create-quick-reminder__divider"
        aria-hidden="true"
      />
      <button
        ref={triggerRef}
        type="button"
        role="combobox"
        aria-label="Ricorda"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-controls={open ? listId : undefined}
        aria-activedescendant={open ? `${listId}-${activeIndex}` : undefined}
        disabled={disabled}
        onClick={() => {
          setActiveIndex(selectedIndex);
          setOpen((current) => !current);
        }}
        onKeyDown={(event) => {
          if (event.key === 'Escape' && open) {
            event.preventDefault();
            event.stopPropagation();
            setOpen(false);
            return;
          }
          if (event.key === 'Tab') {
            setOpen(false);
            return;
          }
          if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
            event.preventDefault();
            const direction = event.key === 'ArrowDown' ? 1 : -1;
            setActiveIndex((index) =>
              open
                ? (index + direction + options.length) % options.length
                : (selectedIndex + direction + options.length) % options.length,
            );
            setOpen(true);
            return;
          }
          if (event.key === 'Home' || event.key === 'End') {
            event.preventDefault();
            setActiveIndex(event.key === 'Home' ? 0 : options.length - 1);
            setOpen(true);
            return;
          }
          if ((event.key === 'Enter' || event.key === ' ') && open) {
            event.preventDefault();
            choose(options[activeIndex] ?? null);
          }
        }}
      >
        <span>
          {disabled ? 'Ricorda · Non disponibile' : reminderLabel(value)}
        </span>
        <span className="temporal-create-quick-reminder__chevron" aria-hidden="true">
          ⌄
        </span>
      </button>
      {open && !disabled
        ? createPortal(
            <div
              ref={popupRef}
              id={listId}
              className="temporal-create-quick-reminder__options"
              role="listbox"
              aria-label="Ricorda"
              style={popupPosition}
            >
              {options.map((option, index) => (
                <button
                  key={option ?? 'none'}
                  id={`${listId}-${index}`}
                  type="button"
                  role="option"
                  aria-selected={option === value}
                  data-active={index === activeIndex}
                  onPointerEnter={() => setActiveIndex(index)}
                  onPointerDown={(event) => event.preventDefault()}
                  onClick={() => choose(option)}
                >
                  {reminderLabel(option)}
                </button>
              ))}
            </div>,
            document.body,
          )
        : null}
    </div>
  );
}

export function TemporalCreateQuickReminder({ fields, onPatch }: Props) {
  const eligible =
    fields.timeSemantics === 'timed' && fields.timeMode === 'zoned';
  return (
    <TemporalReminderControl
      value={eligible ? fields.confirmation.reminderLeadMinutes : null}
      disabled={!eligible}
      unavailableReason={
        fields.timeSemantics !== 'timed'
          ? 'Il promemoria richiede un orario preciso.'
          : 'Il promemoria richiede un fuso orario specifico.'
      }
      onChange={(reminderLeadMinutes) =>
        onPatch({
          confirmation: { ...fields.confirmation, reminderLeadMinutes },
        })
      }
    />
  );
}
