import { useEffect, useRef, useState, type RefObject } from 'react';
import { Temporal } from '@dante/time';

import {
  createRemoteRecurringSeriesEdit,
  type RecurringSeriesReview,
  type RecurringSeriesSource,
  type SeriesScope,
} from '../../../temporal/remote-recurring-series-edit';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import { TimeControl } from '../../../temporal-create/ui/temporal-create-core-u2';
import { TemporalCreateDatePicker } from '../../../temporal-create/ui/temporal-create-date-picker';
import { TemporalReminderControl } from '../../../temporal-create/ui/temporal-create-quick-reminder';
import './activity-edit-panel.css';

type Entry = Record<string, unknown>;

const asEntry = (value: unknown): Entry =>
  value && typeof value === 'object' && !Array.isArray(value)
    ? (value as Entry)
    : {};
const asRows = (value: unknown): Entry[] =>
  Array.isArray(value) ? value.map(asEntry) : [];
const asText = (value: unknown): string =>
  typeof value === 'string' ? value : '';
const asNumber = (value: unknown): number =>
  typeof value === 'number' && Number.isFinite(value) ? value : 0;

function ordinalSelection(value: unknown): {
  weekday_number: number;
  ordinal: number;
} {
  const first = asEntry(Array.isArray(value) ? value[0] : null);
  return {
    weekday_number: asNumber(first.weekday_number) || 1,
    ordinal: asNumber(first.ordinal) || 1,
  };
}

function yearlySelection(value: unknown): {
  month_number: number;
  month_day: number;
} {
  const first = asEntry(Array.isArray(value) ? value[0] : null);
  return {
    month_number: asNumber(first.month_number) || 1,
    month_day: asNumber(first.month_day) || 1,
  };
}

function dayAfter(day: string): string {
  return Temporal.PlainDate.from(day).add({ days: 1 }).toString();
}

function dayBefore(day: string): string {
  return Temporal.PlainDate.from(day).subtract({ days: 1 }).toString();
}

function initialRecurrence(
  source: RecurringSeriesSource,
  scope: SeriesScope,
): Entry {
  return {
    ...source.recurrence,
    effective_from:
      scope === 'from_next'
        ? dayAfter(source.selectedDate)
        : source.selectedDate,
  };
}

function writeRows(
  structure: Entry,
  owner: RecurringSeriesSource['owner'],
  key: string,
  rows: Entry[],
): Entry {
  if (owner === 'event') return { ...structure, [key]: rows };
  return {
    ...structure,
    activity_template: { ...asEntry(structure.activity_template), [key]: rows },
  };
}

export function RecurringSeriesEditor({
  occurrenceRef,
  scope,
  owner,
  onSaved,
  onCancel,
  closeRequestRef,
}: Readonly<{
  occurrenceRef: string;
  scope: SeriesScope;
  owner: 'routine' | 'event';
  onSaved: () => void;
  onCancel: () => void;
  closeRequestRef?: RefObject<(() => void) | null>;
}>) {
  const [remote] = useState(createRemoteRecurringSeriesEdit);
  const [source, setSource] = useState<RecurringSeriesSource | null>(null);
  const [structure, setStructure] = useState<Entry>({});
  const [recurrence, setRecurrence] = useState<Entry>({});
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [color, setColor] = useState('');
  const [areas, setAreas] = useState<readonly { ref: string; name: string }[]>(
    [],
  );
  const [review, setReview] = useState<RecurringSeriesReview | null>(null);
  const [reviewedIntent, setReviewedIntent] = useState<
    Parameters<typeof remote.preview>[0] | null
  >(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');
  const operation = useRef(crypto.randomUUID());

  useEffect(() => {
    let active = true;
    void Promise.all([
      remote.load(occurrenceRef),
      fetch('/api/v1/temporal/life-areas', { credentials: 'include' }).then(
        async (response) => {
          if (!response.ok) throw new Error('Life Area non disponibili.');
          return response.json() as Promise<unknown>;
        },
      ),
    ])
      .then(([loaded, catalog]) => {
        if (!active) return;
        if (loaded.owner !== owner || !Array.isArray(catalog)) {
          throw new Error('La serie selezionata non corrisponde all’editor.');
        }
        setAreas(
          catalog
            .map(asEntry)
            .filter((area) => area.archived === false)
            .map((area) => ({
              ref: asText(area.life_area_ref),
              name: asText(area.name),
            })),
        );
        setSource(loaded);
        setStructure(loaded.structure);
        setRecurrence(initialRecurrence(loaded, scope));
        setTitle(loaded.title);
        const template =
          owner === 'routine'
            ? asEntry(loaded.structure.activity_template)
            : {};
        setDescription(loaded.description ?? asText(template.description));
        setLocation(loaded.location ?? asText(template.location));
        setColor(loaded.colorCode ?? asText(template.item_color_code));
      })
      .catch((reason: unknown) => {
        if (active)
          setError(
            reason instanceof Error ? reason.message : 'Serie non disponibile.',
          );
      });
    return () => {
      active = false;
    };
  }, [occurrenceRef, owner, remote, scope]);

  useEffect(() => {
    if (!closeRequestRef) return;
    closeRequestRef.current = onCancel;
    return () => {
      closeRequestRef.current = null;
    };
  }, [closeRequestRef, onCancel]);

  const changeStructure = (value: Entry) => {
    setStructure(value);
    setReview(null);
  };
  const changeRecurrence = (value: Entry) => {
    setRecurrence(value);
    setReview(null);
  };
  const template = asEntry(structure.activity_template);
  const updateTemplate = (patch: Entry) =>
    changeStructure({
      ...structure,
      activity_template: { ...template, ...patch },
    });
  const editRows = (key: string, rows: Entry[]) =>
    changeStructure(writeRows(structure, owner, key, rows));
  const objectives = asRows(
    owner === 'routine' ? template.objectives : structure.objectives,
  );
  const changeObjective = (index: number, patch: Entry) =>
    editRows(
      'objectives',
      objectives.map((part, i) => (i === index ? { ...part, ...patch } : part)),
    );
  const changeObjectiveKind = (index: number, kind: string) =>
    changeObjective(index, {
      result_kind: kind,
      comparator_code:
        kind === 'quantity' ? 'gte' : kind === 'range' ? 'between' : null,
      target_value: kind === 'quantity' ? 1 : null,
      target_min: kind === 'range' ? 0 : null,
      target_max: kind === 'range' ? 1 : null,
      unit_code: kind === 'quantity' || kind === 'range' ? '' : null,
    });
  const root = asEntry(template.root_window);
  const intervals = asRows(template.activity_intervals);
  const sessions = asRows(template.planned_slices);
  const children = asRows(template.children);
  const agenda = Array.isArray(structure.agenda_parts)
    ? structure.agenda_parts.map(asText)
    : [];
  const activeArea = asText(
    owner === 'routine' ? template.life_area_ref : structure.life_area_ref,
  );
  const time = Array.isArray(recurrence.wall_times)
    ? asText(recurrence.wall_times[0])
    : '';
  const monthDays = Array.isArray(recurrence.month_days)
    ? recurrence.month_days.map(asNumber)
    : [];
  const ordinalDays = Array.isArray(recurrence.ordinal_weekdays)
    ? recurrence.ordinal_weekdays.map(asEntry)
    : [];
  const yearDays = Array.isArray(recurrence.year_month_days)
    ? recurrence.year_month_days.map(asEntry)
    : [];
  const changeTime = (next: string) =>
    changeRecurrence({ ...recurrence, wall_times: [next] });
  const changePattern = (pattern: string) => {
    const weekday = Temporal.PlainDate.from(
      source?.selectedDate ?? '2027-01-01',
    ).dayOfWeek;
    const day = Number((source?.selectedDate ?? '').slice(8, 10)) || 1;
    const month = Number((source?.selectedDate ?? '').slice(5, 7)) || 1;
    changeRecurrence({
      ...recurrence,
      pattern_code: pattern,
      weekdays: pattern === 'weekly_weekdays' ? [weekday] : [],
      month_days: pattern === 'monthly_month_days' ? [day] : [],
      ordinal_weekdays:
        pattern === 'monthly_ordinal_weekdays'
          ? [{ weekday_number: weekday, ordinal: 1 }]
          : [],
      year_month_days:
        pattern === 'yearly_month_days'
          ? [{ month_number: month, month_day: day }]
          : [],
      step_unit_code: pattern === 'anchor_step' ? 'day' : null,
      pattern_anchor_date:
        pattern === 'anchor_step' || asNumber(recurrence.interval_count) > 1
          ? (source?.selectedDate ?? null)
          : null,
    });
  };
  const updateMetadata = (set: (value: string) => void, value: string) => {
    set(value);
    setReview(null);
  };

  const prepare = async () => {
    if (!source || busy) return;
    setError('');
    if (!title.trim()) {
      setError('Inserisci un titolo.');
      return;
    }
    setBusy(true);
    try {
      const completeStructure =
        owner === 'routine'
          ? {
              ...structure,
              activity_template: {
                ...template,
                description: description.trim() || null,
                location: location.trim() || null,
                item_color_code: color.trim() || null,
              },
            }
          : structure;
      const patch: Record<string, string | null> = {};
      if (title.trim() !== source.title) patch.title = title.trim();
      if (description.trim() !== (source.description ?? ''))
        patch.description = description.trim() || null;
      if (location.trim() !== (source.location ?? ''))
        patch.location = location.trim() || null;
      if (color.trim() !== (source.colorCode ?? ''))
        patch.color_code = color.trim() || null;
      const intent = {
        selectedRef: occurrenceRef,
        source,
        scope,
        recurrence,
        structure: completeStructure,
        profilePatch: Object.keys(patch).length ? patch : null,
        operationId: operation.current,
      };
      const result = await remote.preview(intent);
      setReviewedIntent(intent);
      setReview(result);
    } catch (reason) {
      setError(
        reason instanceof Error ? reason.message : 'Anteprima non disponibile.',
      );
    } finally {
      setBusy(false);
    }
  };

  const accept = async () => {
    if (!reviewedIntent || !review || busy) return;
    setBusy(true);
    setError('');
    try {
      await remote.accept(reviewedIntent, review);
      onSaved();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Serie non salvata.');
      setReview(null);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="timeline-activity-editor timeline-recurring-series-editor">
      <div className="timeline-activity-editor__body">
        <h3>
          {scope === 'from_next'
            ? 'Dalla prossima istanza'
            : 'Questa e le successive'}
        </h3>
        {error ? <p role="alert">{error}</p> : null}
        {!source && !error ? (
          <p role="status">Caricamento della serie…</p>
        ) : null}
        {source ? (
          <>
            <label>
              Titolo
              <input
                value={title}
                maxLength={300}
                onChange={(e) => updateMetadata(setTitle, e.target.value)}
              />
            </label>
            <section aria-label="Ricorrenza">
              <h3>Ricorrenza</h3>
              <label>
                Frequenza{' '}
                <select
                  value={asText(recurrence.pattern_code)}
                  onChange={(e) => changePattern(e.target.value)}
                >
                  <option value="daily">Ogni giorno</option>
                  <option value="weekly_weekdays">
                    Giorni della settimana
                  </option>
                  <option value="monthly_month_days">Giorni del mese</option>
                  <option value="monthly_ordinal_weekdays">
                    Settimana del mese
                  </option>
                  <option value="yearly_month_days">Giorni dell’anno</option>
                  <option value="anchor_step">Passo fisso</option>
                </select>
              </label>
              <label>
                Ripeti ogni{' '}
                <input
                  type="number"
                  min={1}
                  max={10000}
                  value={asNumber(recurrence.interval_count)}
                  onChange={(e) => {
                    const interval = Number(e.target.value);
                    changeRecurrence({
                      ...recurrence,
                      interval_count: interval,
                      pattern_anchor_date:
                        interval > 1 ||
                        recurrence.pattern_code === 'anchor_step'
                          ? source.selectedDate
                          : null,
                    });
                  }}
                />{' '}
              </label>
              {recurrence.pattern_code === 'weekly_weekdays' ? (
                <fieldset>
                  <legend>Giorni</legend>
                  {['Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab', 'Dom'].map(
                    (label, index) => {
                      const weekday = index + 1;
                      const selected =
                        Array.isArray(recurrence.weekdays) &&
                        recurrence.weekdays.includes(weekday);
                      return (
                        <label key={weekday}>
                          <input
                            type="checkbox"
                            checked={selected}
                            onChange={() =>
                              changeRecurrence({
                                ...recurrence,
                                weekdays: selected
                                  ? (recurrence.weekdays as number[]).filter(
                                      (day) => day !== weekday,
                                    )
                                  : [
                                      ...(recurrence.weekdays as number[]),
                                      weekday,
                                    ].sort((a, b) => a - b),
                              })
                            }
                          />
                          {label}
                        </label>
                      );
                    },
                  )}
                </fieldset>
              ) : null}
              {recurrence.pattern_code === 'monthly_month_days' ? (
                <fieldset>
                  <legend>Giorni del mese</legend>
                  {monthDays.map((day, index) => (
                    <div
                      key={index}
                      className="timeline-recurring-series-editor__row"
                    >
                      <label>
                        Giorno{' '}
                        <input
                          type="number"
                          min={-31}
                          max={31}
                          value={day}
                          onChange={(e) =>
                            changeRecurrence({
                              ...recurrence,
                              month_days: monthDays.map((value, i) =>
                                i === index ? Number(e.target.value) : value,
                              ),
                            })
                          }
                        />
                      </label>
                      <button
                        type="button"
                        disabled={monthDays.length === 1}
                        onClick={() =>
                          changeRecurrence({
                            ...recurrence,
                            month_days: monthDays.filter((_, i) => i !== index),
                          })
                        }
                      >
                        Rimuovi
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={() =>
                      changeRecurrence({
                        ...recurrence,
                        month_days: [...monthDays, 1],
                      })
                    }
                  >
                    Aggiungi giorno
                  </button>
                </fieldset>
              ) : null}
              {recurrence.pattern_code === 'monthly_ordinal_weekdays' ? (
                <fieldset>
                  <legend>Settimane del mese</legend>
                  {ordinalDays.map((entry, index) => (
                    <div
                      key={index}
                      className="timeline-recurring-series-editor__row"
                    >
                      <label>
                        Settimana{' '}
                        <select
                          value={asNumber(entry.ordinal)}
                          onChange={(e) =>
                            changeRecurrence({
                              ...recurrence,
                              ordinal_weekdays: ordinalDays.map((value, i) =>
                                i === index
                                  ? {
                                      ...value,
                                      ordinal: Number(e.target.value),
                                    }
                                  : value,
                              ),
                            })
                          }
                        >
                          {[1, 2, 3, 4, 5, -1, -2, -3, -4, -5].map((n) => (
                            <option key={n} value={n}>
                              {n === -1 ? 'Ultima' : n}
                            </option>
                          ))}
                        </select>
                      </label>
                      <label>
                        Giorno{' '}
                        <select
                          value={asNumber(entry.weekday_number)}
                          onChange={(e) =>
                            changeRecurrence({
                              ...recurrence,
                              ordinal_weekdays: ordinalDays.map((value, i) =>
                                i === index
                                  ? {
                                      ...value,
                                      weekday_number: Number(e.target.value),
                                    }
                                  : value,
                              ),
                            })
                          }
                        >
                          {[
                            'Lun',
                            'Mar',
                            'Mer',
                            'Gio',
                            'Ven',
                            'Sab',
                            'Dom',
                          ].map((label, i) => (
                            <option key={label} value={i + 1}>
                              {label}
                            </option>
                          ))}
                        </select>
                      </label>
                      <button
                        type="button"
                        disabled={ordinalDays.length === 1}
                        onClick={() =>
                          changeRecurrence({
                            ...recurrence,
                            ordinal_weekdays: ordinalDays.filter(
                              (_, i) => i !== index,
                            ),
                          })
                        }
                      >
                        Rimuovi
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={() =>
                      changeRecurrence({
                        ...recurrence,
                        ordinal_weekdays: [
                          ...ordinalDays,
                          ordinalSelection(null),
                        ],
                      })
                    }
                  >
                    Aggiungi settimana
                  </button>
                </fieldset>
              ) : null}
              {recurrence.pattern_code === 'yearly_month_days' ? (
                <fieldset>
                  <legend>Giorni dell’anno</legend>
                  {yearDays.map((entry, index) => (
                    <div
                      key={index}
                      className="timeline-recurring-series-editor__row"
                    >
                      <label>
                        Mese{' '}
                        <input
                          type="number"
                          min={1}
                          max={12}
                          value={asNumber(entry.month_number)}
                          onChange={(e) =>
                            changeRecurrence({
                              ...recurrence,
                              year_month_days: yearDays.map((value, i) =>
                                i === index
                                  ? {
                                      ...value,
                                      month_number: Number(e.target.value),
                                    }
                                  : value,
                              ),
                            })
                          }
                        />
                      </label>
                      <label>
                        Giorno{' '}
                        <input
                          type="number"
                          min={-31}
                          max={31}
                          value={asNumber(entry.month_day)}
                          onChange={(e) =>
                            changeRecurrence({
                              ...recurrence,
                              year_month_days: yearDays.map((value, i) =>
                                i === index
                                  ? {
                                      ...value,
                                      month_day: Number(e.target.value),
                                    }
                                  : value,
                              ),
                            })
                          }
                        />
                      </label>
                      <button
                        type="button"
                        disabled={yearDays.length === 1}
                        onClick={() =>
                          changeRecurrence({
                            ...recurrence,
                            year_month_days: yearDays.filter(
                              (_, i) => i !== index,
                            ),
                          })
                        }
                      >
                        Rimuovi
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={() =>
                      changeRecurrence({
                        ...recurrence,
                        year_month_days: [...yearDays, yearlySelection(null)],
                      })
                    }
                  >
                    Aggiungi giorno
                  </button>
                </fieldset>
              ) : null}
              {recurrence.pattern_code === 'anchor_step' ? (
                <label>
                  Unità{' '}
                  <select
                    value={asText(recurrence.step_unit_code)}
                    onChange={(e) =>
                      changeRecurrence({
                        ...recurrence,
                        step_unit_code: e.target.value,
                      })
                    }
                  >
                    <option value="day">Giorni</option>
                    <option value="week">Settimane</option>
                    <option value="month">Mesi</option>
                    <option value="year">Anni</option>
                  </select>
                </label>
              ) : null}
              <label>
                Fine{' '}
                <select
                  value={asText(recurrence.range_kind)}
                  onChange={(e) =>
                    changeRecurrence({
                      ...recurrence,
                      range_kind: e.target.value,
                      effective_until:
                        e.target.value === 'until_boundary'
                          ? dayAfter(source.selectedDate)
                          : null,
                      expected_occurrence_count:
                        e.target.value === 'expected_count' ? 1 : null,
                    })
                  }
                >
                  <option value="open">Mai</option>
                  <option value="until_boundary">Data</option>
                  <option value="expected_count">Numero di istanze</option>
                </select>
              </label>
              {recurrence.range_kind === 'until_boundary' ? (
                <TemporalCreateDatePicker
                  label="Ultimo giorno"
                  locale="it"
                  value={
                    asText(recurrence.effective_until)
                      ? dayBefore(asText(recurrence.effective_until)).slice(
                          0,
                          10,
                        )
                      : source.selectedDate
                  }
                  onChange={(day) =>
                    changeRecurrence({
                      ...recurrence,
                      effective_until: dayAfter(day),
                    })
                  }
                />
              ) : null}
              {recurrence.range_kind === 'expected_count' ? (
                <label>
                  Istanze{' '}
                  <input
                    type="number"
                    min={1}
                    value={asNumber(recurrence.expected_occurrence_count)}
                    onChange={(e) =>
                      changeRecurrence({
                        ...recurrence,
                        expected_occurrence_count: Number(e.target.value),
                      })
                    }
                  />
                </label>
              ) : null}
            </section>
            <section aria-label="Orario della serie">
              <h3>Orario</h3>
              {owner === 'event' ? (
                <label>
                  Tutto il giorno
                  <input
                    type="checkbox"
                    checked={structure.placement_kind === 'all_day'}
                    onChange={(e) => {
                      const allDay = e.target.checked;
                      changeStructure({
                        ...structure,
                        placement_kind: allDay ? 'all_day' : 'timed',
                        duration_minutes: allDay ? null : 60,
                        duration_days: allDay ? 1 : null,
                        reminder_lead_minutes: allDay
                          ? null
                          : structure.reminder_lead_minutes,
                      });
                      changeRecurrence({
                        ...recurrence,
                        wall_times: allDay ? [] : ['09:00:00'],
                      });
                    }}
                  />
                </label>
              ) : null}
              {owner === 'routine' || structure.placement_kind === 'timed' ? (
                <TimeControl
                  label="Inizio"
                  value={time.slice(0, 5)}
                  dataPath="series.start"
                  onChange={changeTime}
                />
              ) : null}
              <label>
                {structure.placement_kind === 'all_day'
                  ? 'Giorni'
                  : 'Durata in minuti'}
                <input
                  type="number"
                  min={1}
                  value={asNumber(
                    structure.placement_kind === 'all_day'
                      ? structure.duration_days
                      : structure.duration_minutes,
                  )}
                  onChange={(e) => {
                    const length = Number(e.target.value);
                    changeStructure(
                      owner === 'routine'
                        ? {
                            ...structure,
                            duration_minutes: length,
                            activity_template: {
                              ...template,
                              root_window: {
                                ...root,
                                duration_minutes: length,
                              },
                            },
                          }
                        : {
                            ...structure,
                            [structure.placement_kind === 'all_day'
                              ? 'duration_days'
                              : 'duration_minutes']: length,
                          },
                    );
                  }}
                />
              </label>
              {structure.placement_kind !== 'all_day' ? (
                <TemporalReminderControl
                  value={
                    typeof structure.reminder_lead_minutes === 'number'
                      ? structure.reminder_lead_minutes
                      : null
                  }
                  onChange={(value) =>
                    changeStructure({
                      ...structure,
                      reminder_lead_minutes: value,
                    })
                  }
                />
              ) : null}
            </section>
            {owner === 'routine' ? (
              <>
                <section aria-label="Intervalli">
                  <h3>Intervalli</h3>
                  {intervals.map((row, index) => (
                    <div key={index}>
                      <label>
                        Inizio in minuti{' '}
                        <input
                          type="number"
                          value={asNumber(row.start_offset_minutes)}
                          onChange={(e) =>
                            editRows(
                              'activity_intervals',
                              intervals.map((part, i) =>
                                i === index
                                  ? {
                                      ...part,
                                      start_offset_minutes: Number(
                                        e.target.value,
                                      ),
                                    }
                                  : part,
                              ),
                            )
                          }
                        />
                      </label>
                      <label>
                        Durata{' '}
                        <input
                          type="number"
                          min={1}
                          value={asNumber(row.duration_minutes)}
                          onChange={(e) =>
                            editRows(
                              'activity_intervals',
                              intervals.map((part, i) =>
                                i === index
                                  ? {
                                      ...part,
                                      duration_minutes: Number(e.target.value),
                                    }
                                  : part,
                              ),
                            )
                          }
                        />
                      </label>
                      <button
                        type="button"
                        onClick={() =>
                          editRows(
                            'activity_intervals',
                            intervals.filter((_, i) => i !== index),
                          )
                        }
                      >
                        Rimuovi intervallo
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={() =>
                      editRows('activity_intervals', [
                        ...intervals,
                        {
                          start_offset_minutes: asNumber(
                            root.start_offset_minutes,
                          ),
                          duration_minutes: asNumber(root.duration_minutes),
                        },
                      ])
                    }
                  >
                    Aggiungi intervallo
                  </button>
                </section>
                <section aria-label="Sessioni pianificate">
                  <h3>Sessioni</h3>
                  {sessions.map((row, index) => (
                    <div key={index}>
                      <input
                        aria-label={`Nome Sessione ${index + 1}`}
                        maxLength={300}
                        value={asText(row.name)}
                        onChange={(e) =>
                          editRows(
                            'planned_slices',
                            sessions.map((part, i) =>
                              i === index
                                ? { ...part, name: e.target.value }
                                : part,
                            ),
                          )
                        }
                      />
                      <label>
                        Con orario
                        <input
                          type="checkbox"
                          checked={row.time_enabled !== false}
                          onChange={(e) =>
                            editRows(
                              'planned_slices',
                              sessions.map((part, i) =>
                                i === index
                                  ? e.target.checked
                                    ? {
                                        name: asText(part.name),
                                        start_offset_minutes: 0,
                                        duration_minutes: 30,
                                      }
                                    : {
                                        name: asText(part.name),
                                        time_enabled: false,
                                      }
                                  : part,
                              ),
                            )
                          }
                        />
                      </label>
                      {row.time_enabled !== false ? (
                        <>
                          <label>
                            Inizio in minuti{' '}
                            <input
                              type="number"
                              value={asNumber(row.start_offset_minutes)}
                              onChange={(e) =>
                                editRows(
                                  'planned_slices',
                                  sessions.map((part, i) =>
                                    i === index
                                      ? {
                                          ...part,
                                          start_offset_minutes: Number(
                                            e.target.value,
                                          ),
                                        }
                                      : part,
                                  ),
                                )
                              }
                            />
                          </label>
                          <label>
                            Durata{' '}
                            <input
                              type="number"
                              min={1}
                              value={asNumber(row.duration_minutes)}
                              onChange={(e) =>
                                editRows(
                                  'planned_slices',
                                  sessions.map((part, i) =>
                                    i === index
                                      ? {
                                          ...part,
                                          duration_minutes: Number(
                                            e.target.value,
                                          ),
                                        }
                                      : part,
                                  ),
                                )
                              }
                            />
                          </label>
                        </>
                      ) : null}
                      <button
                        type="button"
                        onClick={() =>
                          editRows(
                            'planned_slices',
                            sessions.filter((_, i) => i !== index),
                          )
                        }
                      >
                        Rimuovi
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    onClick={() =>
                      editRows('planned_slices', [
                        ...sessions,
                        { name: '', time_enabled: false },
                      ])
                    }
                  >
                    Aggiungi Sessione
                  </button>
                  <label>
                    Sessione dell’attività{' '}
                    <select
                      value={asText(template.session_capture_mode)}
                      onChange={(e) =>
                        updateTemplate({ session_capture_mode: e.target.value })
                      }
                    >
                      <option value="disabled">Disattivata</option>
                      <option value="live">Attiva</option>
                      <option value="record">Registrazione</option>
                      <option value="record_and_live">Entrambe</option>
                    </select>
                  </label>
                  <label>
                    Durata minima della Sessione (minuti)
                    <input
                      type="number"
                      min={1}
                      value={
                        template.minimum_session_duration_microseconds == null
                          ? ''
                          : asNumber(
                              template.minimum_session_duration_microseconds,
                            ) / 60_000_000
                      }
                      onChange={(e) =>
                        updateTemplate({
                          minimum_session_duration_microseconds:
                            e.target.value === ''
                              ? null
                              : Number(e.target.value) * 60_000_000,
                        })
                      }
                    />
                  </label>
                  <label>
                    Blocco della collocazione
                    <input
                      type="checkbox"
                      checked={template.placement_protected === true}
                      onChange={(e) =>
                        updateTemplate({
                          placement_protected: e.target.checked,
                        })
                      }
                    />
                  </label>
                  <label>
                    Regola per le sottoattività
                    <select
                      value={asText(template.child_guard_mode)}
                      onChange={(e) =>
                        updateTemplate({ child_guard_mode: e.target.value })
                      }
                    >
                      <option value="none">Libere</option>
                      <option value="confirm">Conferma</option>
                      <option value="block">Bloccate</option>
                    </select>
                  </label>
                </section>
                <section aria-label="Sottoattività">
                  <h3>Sottoattività</h3>
                  {children.map((child, index) => {
                    const setChild = (patch: Entry) =>
                      editRows(
                        'children',
                        children.map((part, i) =>
                          i === index ? { ...part, ...patch } : part,
                        ),
                      );
                    const placement =
                      child.placement == null ? null : asEntry(child.placement);
                    const childSessions = asRows(child.planned_slices);
                    return (
                      <fieldset key={index}>
                        <legend>Sottoattività {index + 1}</legend>
                        <label>
                          Titolo{' '}
                          <input
                            value={asText(child.title)}
                            maxLength={300}
                            onChange={(e) =>
                              setChild({ title: e.target.value })
                            }
                          />
                        </label>
                        <label>
                          Necessità{' '}
                          <select
                            value={asText(child.requirement_code)}
                            onChange={(e) =>
                              setChild({ requirement_code: e.target.value })
                            }
                          >
                            <option value="required">Necessaria</option>
                            <option value="optional">Facoltativa</option>
                          </select>
                        </label>
                        <label>
                          Sessione{' '}
                          <select
                            value={asText(child.session_capture_mode)}
                            onChange={(e) =>
                              setChild({ session_capture_mode: e.target.value })
                            }
                          >
                            <option value="disabled">Disattivata</option>
                            <option value="record">Registrazione</option>
                            <option value="live">Attiva</option>
                            <option value="record_and_live">Entrambe</option>
                          </select>
                        </label>
                        <label>
                          Verifica{' '}
                          <select
                            value={asText(child.reality_mode)}
                            onChange={(e) =>
                              setChild({ reality_mode: e.target.value })
                            }
                          >
                            <option value="manual">Manuale</option>
                            <option value="review_on_end">Alla fine</option>
                            <option value="auto_confirm_outcome">
                              Automatica
                            </option>
                          </select>
                        </label>
                        <label>
                          Con orario{' '}
                          <input
                            type="checkbox"
                            checked={placement !== null}
                            onChange={(e) =>
                              setChild({
                                placement: e.target.checked
                                  ? {
                                      start_offset_minutes: 0,
                                      duration_minutes: 30,
                                    }
                                  : null,
                              })
                            }
                          />
                        </label>
                        {placement ? (
                          <div className="timeline-recurring-series-editor__row">
                            <label>
                              Inizio in minuti{' '}
                              <input
                                type="number"
                                value={asNumber(placement.start_offset_minutes)}
                                onChange={(e) =>
                                  setChild({
                                    placement: {
                                      ...placement,
                                      start_offset_minutes: Number(
                                        e.target.value,
                                      ),
                                    },
                                  })
                                }
                              />
                            </label>
                            <label>
                              Durata{' '}
                              <input
                                type="number"
                                min={1}
                                value={asNumber(placement.duration_minutes)}
                                onChange={(e) =>
                                  setChild({
                                    placement: {
                                      ...placement,
                                      duration_minutes: Number(e.target.value),
                                    },
                                  })
                                }
                              />
                            </label>
                          </div>
                        ) : null}
                        <strong>Sessioni della sottoattività</strong>
                        {childSessions.map((session, sessionIndex) => (
                          <div
                            key={sessionIndex}
                            className="timeline-recurring-series-editor__row"
                          >
                            <label>
                              Nome{' '}
                              <input
                                maxLength={300}
                                value={asText(session.name)}
                                onChange={(e) =>
                                  setChild({
                                    planned_slices: childSessions.map(
                                      (part, i) =>
                                        i === sessionIndex
                                          ? { ...part, name: e.target.value }
                                          : part,
                                    ),
                                  })
                                }
                              />
                            </label>
                            <label>
                              Inizio in minuti{' '}
                              <input
                                type="number"
                                value={asNumber(session.start_offset_minutes)}
                                onChange={(e) =>
                                  setChild({
                                    planned_slices: childSessions.map(
                                      (part, i) =>
                                        i === sessionIndex
                                          ? {
                                              ...part,
                                              start_offset_minutes: Number(
                                                e.target.value,
                                              ),
                                            }
                                          : part,
                                    ),
                                  })
                                }
                              />
                            </label>
                            <label>
                              Durata{' '}
                              <input
                                type="number"
                                min={1}
                                value={asNumber(session.duration_minutes)}
                                onChange={(e) =>
                                  setChild({
                                    planned_slices: childSessions.map(
                                      (part, i) =>
                                        i === sessionIndex
                                          ? {
                                              ...part,
                                              duration_minutes: Number(
                                                e.target.value,
                                              ),
                                            }
                                          : part,
                                    ),
                                  })
                                }
                              />
                            </label>
                            <button
                              type="button"
                              onClick={() =>
                                setChild({
                                  planned_slices: childSessions.filter(
                                    (_, i) => i !== sessionIndex,
                                  ),
                                })
                              }
                            >
                              Rimuovi Sessione
                            </button>
                          </div>
                        ))}
                        <button
                          type="button"
                          onClick={() =>
                            setChild({
                              planned_slices: [
                                ...childSessions,
                                {
                                  name: '',
                                  start_offset_minutes: 0,
                                  duration_minutes: 30,
                                },
                              ],
                            })
                          }
                        >
                          Aggiungi Sessione
                        </button>
                        <button
                          type="button"
                          onClick={() =>
                            editRows(
                              'children',
                              children.filter((_, i) => i !== index),
                            )
                          }
                        >
                          Rimuovi sottoattività
                        </button>
                      </fieldset>
                    );
                  })}
                  <button
                    type="button"
                    onClick={() =>
                      editRows('children', [
                        ...children,
                        {
                          title: '',
                          requirement_code: 'required',
                          session_capture_mode: 'disabled',
                          reality_mode: 'manual',
                          placement: null,
                          planned_slices: [],
                        },
                      ])
                    }
                  >
                    Aggiungi sottoattività
                  </button>
                </section>
              </>
            ) : (
              <section aria-label="Scaletta">
                <h3>Scaletta</h3>
                {agenda.map((part, index) => (
                  <div key={index}>
                    <input
                      aria-label={`Punto ${index + 1}`}
                      maxLength={1000}
                      value={part}
                      onChange={(e) =>
                        changeStructure({
                          ...structure,
                          agenda_parts: agenda.map((item, i) =>
                            i === index ? e.target.value : item,
                          ),
                        })
                      }
                    />
                    <button
                      type="button"
                      onClick={() =>
                        changeStructure({
                          ...structure,
                          agenda_parts: agenda.filter((_, i) => i !== index),
                        })
                      }
                    >
                      Rimuovi
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() =>
                    changeStructure({
                      ...structure,
                      agenda_parts: [...agenda, ''],
                    })
                  }
                >
                  Aggiungi punto
                </button>
              </section>
            )}
            <section aria-label="Svolgimento e obiettivi">
              <h3>Svolgimento e obiettivi</h3>
              <label>
                Verifica{' '}
                <select
                  value={asText(
                    owner === 'routine'
                      ? template.reality_mode
                      : structure.reality_mode,
                  )}
                  onChange={(e) =>
                    owner === 'routine'
                      ? updateTemplate({ reality_mode: e.target.value })
                      : changeStructure({
                          ...structure,
                          reality_mode: e.target.value,
                        })
                  }
                >
                  <option value="manual">Manuale</option>
                  <option value="review_on_end">Alla fine</option>
                  <option value="auto_confirm_outcome">Automatica</option>
                </select>
              </label>
              {objectives.map((row, index) => (
                <div key={index}>
                  <input
                    aria-label={`Obiettivo ${index + 1}`}
                    maxLength={300}
                    value={asText(row.label)}
                    onChange={(e) =>
                      editRows(
                        'objectives',
                        objectives.map((part, i) =>
                          i === index
                            ? { ...part, label: e.target.value }
                            : part,
                        ),
                      )
                    }
                  />
                  <select
                    aria-label={`Tipo obiettivo ${index + 1}`}
                    value={asText(row.result_kind)}
                    onChange={(e) => changeObjectiveKind(index, e.target.value)}
                  >
                    <option value="boolean">Sì o no</option>
                    <option value="quantity">Quantità</option>
                    <option value="range">Intervallo</option>
                    <option value="qualitative">Qualitativo</option>
                  </select>
                  {row.result_kind === 'quantity' ? (
                    <>
                      <select
                        aria-label={`Regola obiettivo ${index + 1}`}
                        value={asText(row.comparator_code)}
                        onChange={(e) =>
                          changeObjective(index, {
                            comparator_code: e.target.value,
                          })
                        }
                      >
                        <option value="eq">Uguale a</option>
                        <option value="gte">Almeno</option>
                        <option value="lte">Al massimo</option>
                      </select>
                      <label>
                        Valore{' '}
                        <input
                          type="number"
                          value={asNumber(row.target_value)}
                          onChange={(e) =>
                            changeObjective(index, {
                              target_value: Number(e.target.value),
                            })
                          }
                        />
                      </label>
                    </>
                  ) : null}
                  {row.result_kind === 'range' ? (
                    <>
                      <label>
                        Minimo{' '}
                        <input
                          type="number"
                          value={asNumber(row.target_min)}
                          onChange={(e) =>
                            changeObjective(index, {
                              target_min: Number(e.target.value),
                            })
                          }
                        />
                      </label>
                      <label>
                        Massimo{' '}
                        <input
                          type="number"
                          value={asNumber(row.target_max)}
                          onChange={(e) =>
                            changeObjective(index, {
                              target_max: Number(e.target.value),
                            })
                          }
                        />
                      </label>
                    </>
                  ) : null}
                  {row.result_kind === 'quantity' ||
                  row.result_kind === 'range' ? (
                    <label>
                      Unità{' '}
                      <input
                        maxLength={40}
                        value={asText(row.unit_code)}
                        onChange={(e) =>
                          changeObjective(index, {
                            unit_code: e.target.value.trim() || null,
                          })
                        }
                      />
                    </label>
                  ) : null}
                  <button
                    type="button"
                    onClick={() =>
                      editRows(
                        'objectives',
                        objectives
                          .filter((_, i) => i !== index)
                          .map((part, i) => ({
                            ...part,
                            presentation_order: i,
                          })),
                      )
                    }
                  >
                    Rimuovi
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={() =>
                  editRows('objectives', [
                    ...objectives,
                    {
                      label: '',
                      result_kind: 'boolean',
                      comparator_code: null,
                      target_value: null,
                      target_min: null,
                      target_max: null,
                      unit_code: null,
                      presentation_order: objectives.length,
                    },
                  ])
                }
              >
                Aggiungi obiettivo
              </button>
            </section>
            <section aria-label="Life Area">
              <h3>Life Area</h3>
              <select
                aria-label="Area assegnata"
                value={activeArea}
                onChange={(e) =>
                  owner === 'routine'
                    ? updateTemplate({ life_area_ref: e.target.value || null })
                    : changeStructure({
                        ...structure,
                        life_area_ref: e.target.value || null,
                      })
                }
              >
                <option value="">Nessuna</option>
                {areas.map((area) => (
                  <option key={area.ref} value={area.ref}>
                    {area.name}
                  </option>
                ))}
              </select>
            </section>
            <section aria-label="Dettagli">
              <label>
                Descrizione
                <textarea
                  value={description}
                  onChange={(e) =>
                    updateMetadata(setDescription, e.target.value)
                  }
                />
              </label>
              <label>
                Località
                <input
                  value={location}
                  onChange={(e) => updateMetadata(setLocation, e.target.value)}
                />
              </label>
              <label>
                Colore
                <input
                  type="color"
                  value={color || '#EA5C12'}
                  onChange={(e) =>
                    updateMetadata(setColor, e.target.value.toUpperCase())
                  }
                />
              </label>
            </section>
          </>
        ) : null}
      </div>
      {review ? (
        <div className="timeline-activity-editor__fields" role="status">
          <strong>Controlla prima di salvare</strong>
          <p>
            {review.targetRefs.length} istanze pianificate da sostituire,{' '}
            {review.newExpectedCount} nuove nel periodo verificato,{' '}
            {review.protected.length} eccezioni conservate.
          </p>
          {review.protected.length ? (
            <ul>
              {review.protected.slice(0, 10).map((item) => (
                <li key={item.occurrenceRef}>
                  {new Date(item.expectedAt).toLocaleString('it-IT')} ·{' '}
                  {item.reason}
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      ) : null}
      <div className="timeline-activity-editor__actions dante-temporal-panel-actions">
        <button type="button" disabled={busy} onClick={onCancel}>
          Annulla
        </button>
        <button
          type="button"
          className="is-primary"
          disabled={busy || !source}
          onClick={() => void (review ? accept() : prepare())}
        >
          {busy
            ? 'Attendi…'
            : review
              ? 'Conferma modifiche'
              : 'Verifica modifiche'}
        </button>
      </div>
    </div>
  );
}

export function RecurringActivitySeriesEditor({
  activityRef,
  scope,
  onSaved,
  onCancel,
  closeRequestRef,
}: Readonly<{
  activityRef: string;
  scope: SeriesScope;
  onSaved: () => void;
  onCancel: () => void;
  closeRequestRef: RefObject<(() => void) | null>;
}>) {
  const [remote] = useState(createRemoteRecurringProfileEdit);
  const [occurrenceRef, setOccurrenceRef] = useState<string | null>(null);
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    void remote
      .loadActivityContext(activityRef)
      .then((value) => {
        if (!active) return;
        if (!value)
          throw new Error('L’attività non appartiene più alla ricorrenza.');
        setOccurrenceRef(value.occurrenceRef);
      })
      .catch((reason: unknown) => {
        if (active)
          setError(
            reason instanceof Error
              ? reason.message
              : 'Ricorrenza non disponibile.',
          );
      });
    return () => {
      active = false;
    };
  }, [activityRef, remote]);
  if (error)
    return (
      <div className="timeline-activity-editor">
        <p role="alert">{error}</p>
        <button type="button" onClick={onCancel}>
          Chiudi
        </button>
      </div>
    );
  if (!occurrenceRef) return <p role="status">Caricamento della ricorrenza…</p>;
  return (
    <RecurringSeriesEditor
      occurrenceRef={occurrenceRef}
      owner="routine"
      scope={scope}
      onSaved={onSaved}
      onCancel={onCancel}
      closeRequestRef={closeRequestRef}
    />
  );
}
