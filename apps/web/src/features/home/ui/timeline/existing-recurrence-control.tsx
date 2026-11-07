import { useState } from 'react';
import { Temporal } from '@dante/time';

import {
  createTemporalCreateFields,
  type TemporalCreateFields,
  type TemporalCreateWeekday,
} from '../../../temporal-create/model/temporal-create-session';
import {
  buildTemporalCreateActivityRecurrence,
  buildTemporalCreateEventRecurrence,
} from '../../../temporal-create/application/temporal-create-b14-runtime';
import type {
  RecurringAuthoringCalendarRecurrence,
} from '../../../temporal-create/application/remote-recurring-authoring';
import {
  TemporalCreateCalendarRecurrenceFields,
} from '../../../temporal-create/ui/temporal-create-calendar-recurrence-fields';
import {
  TemporalCreateQuickRecurrenceSelect,
  type QuickRecurrence,
} from '../../../temporal-create/ui/temporal-create-quick-recurrence-select';

type RecurrenceIntent = TemporalCreateFields['eventRecurrence'];

function quickChoice(
  intent: RecurrenceIntent | null,
  customChoice: boolean,
): QuickRecurrence {
  if (intent === null) return 'none';
  if (
    customChoice ||
    intent.calendarInterval !== 1 ||
    intent.calendarFrequency === 'monthly-ordinal'
  ) {
    return 'custom';
  }
  return intent.calendarFrequency;
}

/** Edit uses the same select and detailed calendar editor as Advanced Create.
 * Starting the series remains an explicit separate action on the saved item.
 */
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
  const [intent, setIntent] = useState<RecurrenceIntent | null>(null);
  const [customChoice, setCustomChoice] = useState(false);
  const [pending, setPending] = useState(false);
  const [error, setError] = useState('');
  const owner = kind === 'event' ? 'event' : 'routine';
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
    eventRecurrence: intent ?? base.eventRecurrence,
  };
  const dateValue = Temporal.PlainDate.from(date);
  const weekday = (['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU'] as const)[
    dateValue.dayOfWeek - 1
  ] as TemporalCreateWeekday;
  const selection = quickChoice(intent, customChoice);
  const startTarget = kind === 'event' ? 'questo Evento' : 'questa Attività';

  const changeRecurrence = (choice: QuickRecurrence) => {
    setError('');
    if (choice === 'none') {
      setIntent(null);
      setCustomChoice(false);
      return;
    }
    const previous = intent ?? base.eventRecurrence;
    let frequency: RecurrenceIntent['calendarFrequency'] = 'weekly';
    if (choice === 'custom') {
      frequency = intent?.calendarFrequency ?? 'weekly';
    } else {
      frequency = choice;
    }
    let weekdays: RecurrenceIntent['weekdays'] = previous.weekdays;
    if (
      frequency === 'weekly' &&
      (choice !== 'custom' || weekdays.length === 0)
    ) {
      weekdays = [weekday];
    }
    setIntent({
      ...previous,
      owner,
      patternKind: 'calendar-wall-clock',
      calendarFrequency: frequency,
      ...(choice === 'custom' ? {} : { calendarInterval: 1 }),
      weekdays,
      calendarOrdinalWeekday: weekday,
      calendarOrdinal: Math.ceil(dateValue.day / 7),
    });
    setCustomChoice(choice === 'custom');
  };

  const startRecurrence = () => {
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
        .catch((reason: unknown) => {
          setError(
            reason instanceof Error
              ? reason.message
              : 'Ripetizione non riuscita.',
          );
        })
        .finally(() => setPending(false));
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Ripetizione non valida.',
      );
      setPending(false);
    }
  };

  return (
    <section className="timeline-existing-recurrence" aria-label="Ripeti">
      <div
        className="temporal-create-u2-repeat"
        data-create-path="eventRecurrence"
      >
        <TemporalCreateQuickRecurrenceSelect
          value={selection}
          onChange={changeRecurrence}
        />
      </div>
      {intent !== null ? (
        <>
          <TemporalCreateCalendarRecurrenceFields
            fields={fields}
            onPatch={(patch) => {
              if (patch.eventRecurrence) setIntent(patch.eventRecurrence);
              setError('');
            }}
            renderError={() => null}
          />
          {error ? <p role="alert">{error}</p> : null}
          <div className="timeline-existing-recurrence__actions">
            {disabled ? (
              <p>Salva le modifiche correnti prima di avviare la ripetizione.</p>
            ) : null}
            <button
              type="button"
              disabled={pending || disabled}
              onClick={startRecurrence}
            >
              {pending
                ? 'Avvio…'
                : `Avvia ripetizione da ${startTarget}`}
            </button>
          </div>
        </>
      ) : null}
    </section>
  );
}
