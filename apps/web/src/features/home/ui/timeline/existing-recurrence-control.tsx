import { useState } from 'react';
import { Temporal } from '@dante/time';
import {
  createTemporalCreateFields,
  type TemporalCreateFields,
  type TemporalCreateWeekday,
} from '../../../temporal-create/model/temporal-create-session';
import { TemporalCreateCalendarRecurrenceFields } from '../../../temporal-create/ui/temporal-create-calendar-recurrence-fields';
import {
  buildTemporalCreateActivityRecurrence,
  buildTemporalCreateEventRecurrence,
} from '../../../temporal-create/application/temporal-create-b14-runtime';
import type { RecurringAuthoringCalendarRecurrence } from '../../../temporal-create/application/remote-recurring-authoring';

export function ExistingRecurrenceControl({
  kind,
  date,
  startTime,
  allDay,
  zoneId,
  disambiguation,
  disabled,
  onStart,
}: Readonly<{
  kind: 'activity' | 'event';
  date: string;
  startTime: string;
  allDay: boolean;
  zoneId: string;
  disambiguation: 'earlier' | 'later';
  disabled: boolean;
  onStart: (rule: RecurringAuthoringCalendarRecurrence) => Promise<void>;
}>) {
  const [open, setOpen] = useState(false);
  const [intent, setIntent] = useState<
    TemporalCreateFields['eventRecurrence'] | null
  >(null);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const base = createTemporalCreateFields({
    kind,
    date,
    startTime,
    timeSemantics: allDay ? 'all-day' : 'timed',
    timeMode: 'zoned',
    timeZoneId: zoneId,
    timeDisambiguation: disambiguation,
  });
  const fields: TemporalCreateFields = {
    ...base,
    eventRecurrence: intent ?? {
      ...base.eventRecurrence,
      owner: kind === 'event' ? 'event' : 'routine',
      patternKind: 'calendar-wall-clock',
      calendarFrequency: 'daily',
    },
  };
  const weekday = (['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'] as const)[
    Temporal.PlainDate.from(date).dayOfWeek - 1
  ] as TemporalCreateWeekday;

  return (
    <section className="timeline-activity-editor__repeat" aria-label="Ripeti">
      <button type="button" onClick={() => setOpen(!open)}>
        Ripeti · {open ? 'Configura' : 'Mai'}
      </button>
      {open ? (
        <>
          <label className="temporal-create-repeat__row">
            <span className="temporal-create-repeat__row-label">Frequenza</span>
            <select
              aria-label="Frequenza ripetizione"
              value={fields.eventRecurrence.calendarFrequency}
              onChange={(event) => {
                const frequency = event.currentTarget
                  .value as TemporalCreateFields['eventRecurrence']['calendarFrequency'];
                setIntent({
                  ...fields.eventRecurrence,
                  calendarFrequency: frequency,
                  weekdays:
                    frequency === 'weekly'
                      ? [weekday]
                      : fields.eventRecurrence.weekdays,
                  calendarOrdinalWeekday: weekday,
                  calendarOrdinal: Math.ceil(
                    Temporal.PlainDate.from(date).day / 7,
                  ),
                });
                setError('');
              }}
            >
              <option value="daily">Ogni giorno</option>
              <option value="weekly">Ogni settimana</option>
              <option value="monthly">Ogni mese</option>
              <option value="monthly-ordinal">Ogni mese per posizione</option>
              <option value="yearly">Ogni anno</option>
            </select>
          </label>
          <TemporalCreateCalendarRecurrenceFields
            fields={fields}
            onPatch={(patch) => {
              if (patch.eventRecurrence) setIntent(patch.eventRecurrence);
              setError('');
            }}
            renderError={() => null}
          />
          {error ? <p role="alert">{error}</p> : null}
          <button
            type="button"
            disabled={pending || disabled}
            onClick={() => {
              setPending(true);
              setError('');
              try {
                const rule =
                  kind === 'activity'
                    ? buildTemporalCreateActivityRecurrence(fields)
                    : buildTemporalCreateEventRecurrence(fields);
                if (rule.family_code !== 'calendar_wall_clock') {
                  throw new Error('Scegli una ripetizione a calendario.');
                }
                void onStart(rule)
                  .catch((reason: unknown) =>
                    setError(
                      reason instanceof Error
                        ? reason.message
                        : 'Ripetizione non riuscita.',
                    ),
                  )
                  .finally(() => setPending(false));
              } catch (reason) {
                setError(
                  reason instanceof Error
                    ? reason.message
                    : 'Ripetizione non valida.',
                );
                setPending(false);
              }
            }}
          >
            {pending
              ? 'Avvio…'
              : `Avvia ripetizione da ${kind === 'event' ? 'questo Evento' : 'questa Attività'}`}
          </button>
          {disabled ? (
            <p>Salva le modifiche correnti prima di avviare la ripetizione.</p>
          ) : null}
        </>
      ) : null}
    </section>
  );
}
