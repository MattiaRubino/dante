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

export function TemporalCreateQuickReminder({ fields, onPatch }: Props) {
  if (fields.timeSemantics !== 'timed') return null;

  const eligible =
    fields.timeMode === 'zoned' &&
    fields.eventRecurrence.patternKind === 'none';
  const value = fields.confirmation.reminderLeadMinutes;

  return (
    <label
      className={`temporal-create-quick-reminder${eligible ? '' : ' is-disabled'}`}
      title={
        eligible
          ? 'Promemoria relativo all’inizio dello Schedule.'
          : 'Il promemoria richiede un orario con fuso specifico e senza ricorrenza.'
      }
    >
      <span className="temporal-create-quick-reminder__icon" aria-hidden="true">
        <BellIcon />
      </span>
      <span className="temporal-create-quick-reminder__divider" aria-hidden="true" />
      <select
        aria-label="Ricorda"
        disabled={!eligible}
        value={value === null ? '' : String(value)}
        onChange={(event) => {
          const raw = event.currentTarget.value;
          onPatch({
            confirmation: {
              ...fields.confirmation,
              reminderLeadMinutes: raw === '' ? null : Number(raw),
            },
          });
        }}
      >
        {TEMPORAL_CREATE_REMINDER_OPTIONS.map((option) => (
          <option key={option ?? 'none'} value={option ?? ''}>
            {reminderLabel(option)}
          </option>
        ))}
      </select>
    </label>
  );
}
