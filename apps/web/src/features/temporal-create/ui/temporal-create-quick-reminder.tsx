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

export function TemporalReminderControl({ value, onChange, disabled = false,
  unavailableReason = 'Il promemoria richiede un orario preciso.' }: Readonly<{
  value: number | null;
  onChange: (value: number | null) => void;
  disabled?: boolean;
  unavailableReason?: string;
}>) {
  return (
    <label
      className={`temporal-create-quick-reminder${disabled ? ' is-disabled' : ''}`}
      title={disabled ? unavailableReason : 'Promemoria relativo all’inizio dello Schedule.'}
    >
      <span className="temporal-create-quick-reminder__icon" aria-hidden="true">
        <BellIcon />
      </span>
      <span className="temporal-create-quick-reminder__divider" aria-hidden="true" />
      <select
        aria-label="Ricorda"
        disabled={disabled}
        value={value === null ? '' : String(value)}
        onChange={(event) => {
          const raw = event.currentTarget.value;
          onChange(raw === '' ? null : Number(raw));
        }}
      >
        {disabled ? <option value="">Ricorda · Non disponibile</option> : null}
        {!disabled && value !== null && !TEMPORAL_CREATE_REMINDER_OPTIONS.includes(value) ?
          <option value={value}>{reminderLabel(value)}</option> : null}
        {!disabled ? TEMPORAL_CREATE_REMINDER_OPTIONS.map((option) => (
          <option key={option ?? 'none'} value={option ?? ''}>
            {reminderLabel(option)}
          </option>
        )) : null}
      </select>
    </label>
  );
}

export function TemporalCreateQuickReminder({ fields, onPatch }: Props) {
  const eligible = fields.timeSemantics === 'timed' && fields.timeMode === 'zoned';
  return <TemporalReminderControl
    value={eligible ? fields.confirmation.reminderLeadMinutes : null}
    disabled={!eligible}
    unavailableReason={fields.timeSemantics !== 'timed'
      ? 'Il promemoria richiede un orario preciso.'
      : 'Il promemoria richiede un fuso orario specifico.'}
    onChange={(reminderLeadMinutes) => onPatch({
      confirmation: { ...fields.confirmation, reminderLeadMinutes },
    })}
  />;
}
