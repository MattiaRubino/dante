import { forwardRef, useImperativeHandle, useState } from 'react';
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
import type { RecurringAuthoringCalendarRecurrence } from '../../../temporal-create/application/remote-recurring-authoring';
import { TemporalCreateCalendarRecurrenceFields } from '../../../temporal-create/ui/temporal-create-calendar-recurrence-fields';
import {
  TemporalCreateQuickRecurrenceSelect,
  type QuickRecurrence,
} from '../../../temporal-create/ui/temporal-create-quick-recurrence-select';
import { TemporalRecurrencePanel } from '../../../temporal-create/ui/temporal-recurrence-panel';

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

/** Recurrence is part of the owning editor's Save draft.
 * It must never expose an independent mutation button in the form.
 */
export type ExistingRecurrenceControlHandle = Readonly<{
  getRule: () => RecurringAuthoringCalendarRecurrence | null;
}>;

export const ExistingRecurrenceControl = forwardRef<
  ExistingRecurrenceControlHandle,
  Readonly<{
    kind: 'activity' | 'event';
    date: string;
    startTime: string;
    allDay: boolean;
    zoneId: string;
    disambiguation: 'earlier' | 'later';
    onSelectionChange: (selected: boolean) => void;
  }>
>(function ExistingRecurrenceControl(
  {
    kind,
    date,
    startTime,
    allDay,
    zoneId,
    disambiguation,
    onSelectionChange,
  },
  ref,
) {
  const [intent, setIntent] = useState<RecurrenceIntent | null>(null);
  const [customChoice, setCustomChoice] = useState(false);
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
  const changeRecurrence = (choice: QuickRecurrence) => {
    if (choice === 'none') {
      setIntent(null);
      setCustomChoice(false);
      onSelectionChange(false);
      return;
    }
    const previous = intent ?? base.eventRecurrence;
    const fallbackFrequency = intent?.calendarFrequency ?? 'weekly';
    const frequency: RecurrenceIntent['calendarFrequency'] =
      choice === 'custom' ? fallbackFrequency : choice;
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
    onSelectionChange(true);
  };

  useImperativeHandle(ref, () => ({
    getRule: () => {
      if (intent === null) return null;
      const rule =
        kind === 'activity'
          ? buildTemporalCreateActivityRecurrence(fields)
          : buildTemporalCreateEventRecurrence(fields);
      if (rule.family_code !== 'calendar_wall_clock') {
        throw new Error('Scegli una ripetizione a calendario.');
      }
      return rule;
    },
  }));

  return (
    <TemporalRecurrencePanel
      kind={kind}
      className="timeline-existing-recurrence"
      expanded={intent !== null}
      choice={
        <div
          className="temporal-create-u2-repeat"
          data-create-path="eventRecurrence"
        >
          <TemporalCreateQuickRecurrenceSelect
            value={selection}
            onChange={changeRecurrence}
          />
        </div>
      }
    >
      <TemporalCreateCalendarRecurrenceFields
        fields={fields}
        onPatch={(patch) => {
          if (patch.eventRecurrence) {
            setIntent(patch.eventRecurrence);
            onSelectionChange(true);
          }
        }}
        renderError={() => null}
        embedded
      />
    </TemporalRecurrencePanel>
  );
});
