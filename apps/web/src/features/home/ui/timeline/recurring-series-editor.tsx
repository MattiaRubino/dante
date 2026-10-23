import { useEffect, useRef, useState, type RefObject } from 'react';
import { Temporal } from '@dante/time';
import { createWebFetch } from '../../../../platform/api/web-fetch';

import {
  createRemoteRecurringSeriesEdit,
  type RecurringSeriesReview,
  type RecurringSeriesSource,
  type SeriesScope,
} from '../../../temporal/remote-recurring-series-edit';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import { TimeControl } from '../../../temporal-create/ui/temporal-create-core-u2';
import { TemporalColorControl } from '../../../temporal-create/ui/temporal-color-control';
import { TemporalCreateDatePicker } from '../../../temporal-create/ui/temporal-create-date-picker';
import { TemporalLifeAreaSelect } from '../../../temporal-create/ui/temporal-life-area-select';
import { TemporalReminderControl } from '../../../temporal-create/ui/temporal-create-quick-reminder';
import '../../../temporal-create/ui/temporal-create-calendar-recurrence-fields.css';
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

function SeriesIntervalFields({
  selectedDate,
  wallTime,
  row,
  index,
  onChange,
  onRemove,
}: Readonly<{
  selectedDate: string;
  wallTime: string;
  row: Entry;
  index: number;
  onChange: (row: Entry) => void;
  onRemove?: (() => void) | undefined;
}>) {
  const anchor = Temporal.PlainDateTime.from(
    `${selectedDate}T${wallTime.slice(0, 5) || '09:00'}`,
  );
  const start = anchor.add({ minutes: asNumber(row.start_offset_minutes) });
  const end = start.add({ minutes: asNumber(row.duration_minutes) });
  const changeStart = (day: string, time: string) => {
    const next = Temporal.PlainDateTime.from(`${day}T${time}`);
    onChange({
      ...row,
      start_offset_minutes: anchor.until(next).total({ unit: 'minutes' }),
      duration_minutes: next.until(end).total({ unit: 'minutes' }),
    });
  };
  const changeEnd = (day: string, time: string) => {
    const next = Temporal.PlainDateTime.from(`${day}T${time}`);
    onChange({
      ...row,
      duration_minutes: start.until(next).total({ unit: 'minutes' }),
    });
  };
  return (
    <div className="temporal-create-activity-interval">
      <span className="temporal-create-activity-interval__label">
        Intervallo {index + 1}
      </span>
      <div className="temporal-create-activity-interval__fields timeline-activity-editor__interval-fields">
        <TemporalCreateDatePicker
          label="Data inizio"
          locale="it"
          value={start.toPlainDate().toString()}
          onChange={(day) =>
            changeStart(
              day,
              start.toPlainTime().toString({ smallestUnit: 'minute' }),
            )
          }
        />
        <TimeControl
          label="Inizio"
          value={start.toPlainTime().toString({ smallestUnit: 'minute' })}
          dataPath={`series.interval.${index}.start`}
          onChange={(value) =>
            changeStart(start.toPlainDate().toString(), value)
          }
        />
        <span
          className="temporal-create-activity-interval__arrow"
          aria-hidden="true"
        >
          →
        </span>
        <TimeControl
          label="Fine"
          value={end.toPlainTime().toString({ smallestUnit: 'minute' })}
          dataPath={`series.interval.${index}.end`}
          onChange={(value) => changeEnd(end.toPlainDate().toString(), value)}
        />
        <TemporalCreateDatePicker
          label="Data fine"
          locale="it"
          value={end.toPlainDate().toString()}
          onChange={(day) =>
            changeEnd(
              day,
              end.toPlainTime().toString({ smallestUnit: 'minute' }),
            )
          }
        />
        {onRemove ? (
          <button
            type="button"
            className="temporal-create-activity-interval__remove"
            aria-label={`Rimuovi intervallo ${index + 1}`}
            onClick={onRemove}
          >
            ×
          </button>
        ) : null}
      </div>
    </div>
  );
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
  const [request] = useState(() => createWebFetch(globalThis.fetch));
  const [source, setSource] = useState<RecurringSeriesSource | null>(null);
  const [structure, setStructure] = useState<Entry>({});
  const [recurrence, setRecurrence] = useState<Entry>({});
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [color, setColor] = useState('');
  const [areas, setAreas] = useState<
    readonly { ref: string; name: string; colorCode: string | null }[]
  >([]);
  const [areaQuery, setAreaQuery] = useState('');
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
      request('/api/v1/temporal/life-areas').then(async (response) => {
        if (!response.ok) throw new Error('Life Area non disponibili.');
        return response.json() as Promise<unknown>;
      }),
    ])
      .then(([loaded, catalog]) => {
        if (!active) return;
        if (loaded.owner !== owner || !Array.isArray(catalog)) {
          throw new Error('La serie selezionata non corrisponde all’editor.');
        }
        const areaOptions = catalog
          .map(asEntry)
          .filter((area) => area.archived === false)
          .map((area) => ({
            ref: asText(area.life_area_ref),
            name: asText(area.name),
            colorCode: asText(area.color_code) || null,
          }));
        setAreas(areaOptions);
        setSource(loaded);
        setStructure(loaded.structure);
        setRecurrence(initialRecurrence(loaded, scope));
        setTitle(loaded.title);
        const template =
          owner === 'routine'
            ? asEntry(loaded.structure.activity_template)
            : {};
        const assignedArea = asText(
          owner === 'routine'
            ? template.life_area_ref
            : loaded.structure.life_area_ref,
        );
        setAreaQuery(
          areaOptions.find((area) => area.ref === assignedArea)?.name ?? '',
        );
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
  }, [occurrenceRef, owner, remote, request, scope]);

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
  const root = {
    start_offset_minutes: 0,
    duration_minutes: asNumber(structure.duration_minutes) || 30,
    ...asEntry(template.root_window),
  };
  const intervals = asRows(template.activity_intervals);
  const editIntervals = (rows: Entry[]) => {
    if (rows.length === 0) {
      editRows('activity_intervals', rows);
      return;
    }
    const first = Math.min(
      ...rows.map((row) => asNumber(row.start_offset_minutes)),
    );
    const last = Math.max(
      ...rows.map(
        (row) =>
          asNumber(row.start_offset_minutes) + asNumber(row.duration_minutes),
      ),
    );
    changeStructure({
      ...structure,
      duration_minutes: last - first,
      activity_template: {
        ...template,
        root_window: {
          start_offset_minutes: first,
          duration_minutes: last - first,
        },
        activity_intervals: rows,
      },
    });
  };
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
    if (
      areaQuery.trim() !==
      (areas.find((area) => area.ref === activeArea)?.name ?? '')
    ) {
      setError('Scegli una Life Area dall’elenco.');
      return;
    }
    if (
      owner === 'routine' &&
      [
        root,
        ...intervals,
        ...sessions.filter((row) => row.time_enabled !== false),
      ].some((row) => asNumber(row.duration_minutes) <= 0)
    ) {
      setError('La fine di ogni intervallo deve seguire l’inizio.');
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
        <h3 className="timeline-recurring-series-editor__scope">
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
            <div className="timeline-activity-editor__kind" aria-label="Tipo">
              <span className={owner === 'routine' ? 'is-selected' : ''}>
                Attività
              </span>
              <span className={owner === 'event' ? 'is-selected' : ''}>
                Evento
              </span>
              <span>Timer</span>
              <span>Sveglia</span>
            </div>
            <div className="temporal-create-title-row has-tools timeline-activity-editor__title-row">
              <label className="timeline-activity-editor__title">
                <span className="timeline-activity-editor__visually-hidden">
                  Titolo
                </span>
                <input
                  className="temporal-create-title-input"
                  aria-label="Titolo"
                  value={title}
                  maxLength={300}
                  onChange={(e) => updateMetadata(setTitle, e.target.value)}
                />
              </label>
              {owner === 'routine' ? (
                <div className="timeline-activity-editor__title-tools">
                  <button
                    type="button"
                    className="temporal-create-placement-lock"
                    aria-pressed={template.placement_protected === true}
                    onClick={() =>
                      updateTemplate({
                        placement_protected:
                          template.placement_protected !== true,
                      })
                    }
                  >
                    {template.placement_protected === true
                      ? 'Sblocca'
                      : 'Blocca'}{' '}
                    spostamenti
                  </button>
                  <label className="temporal-create-structure-session-toggle">
                    <input
                      type="checkbox"
                      checked={template.session_capture_mode !== 'disabled'}
                      onChange={(e) =>
                        updateTemplate({
                          session_capture_mode: e.target.checked
                            ? 'live'
                            : 'disabled',
                        })
                      }
                    />
                    Sessione
                  </label>
                </div>
              ) : null}
            </div>
            <section
              className="timeline-recurring-series-editor__timing"
              aria-label="Orario della serie"
            >
              <h3>Orario</h3>
              <div className="timeline-activity-editor__timezone">
                <span aria-hidden="true">◉</span>
                Fuso orario · {asText(recurrence.zone_id) || 'della serie'}
              </div>
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
              {owner === 'event' && structure.placement_kind === 'timed' ? (
                <TimeControl
                  label="Inizio"
                  value={time.slice(0, 5)}
                  dataPath="series.start"
                  onChange={changeTime}
                />
              ) : null}
              {owner === 'event' ? (
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
                      changeStructure({
                        ...structure,
                        [structure.placement_kind === 'all_day'
                          ? 'duration_days'
                          : 'duration_minutes']: length,
                      });
                    }}
                  />
                </label>
              ) : null}
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
                <section
                  className="temporal-create-activity-tree timeline-activity-editor__sessions"
                  aria-label="Sessioni pianificate"
                >
                  <div
                    className="temporal-create-activity-tree__spine"
                    aria-hidden="true"
                  />
                  <div className="temporal-create-activity-tree__group-label">
                    Sessioni attività
                  </div>
                  {sessions.map((row, index) => (
                    <div
                      key={index}
                      className="temporal-create-tree-item is-session is-root"
                    >
                      <div className="temporal-create-tree-row">
                        <span
                          className="temporal-create-tree-row__icon"
                          aria-hidden="true"
                        >
                          ▶
                        </span>
                        <span
                          className="temporal-create-tree-row__divider"
                          aria-hidden="true"
                        />
                        <input
                          className="temporal-create-tree-row__title"
                          aria-label={`Nome Sessione ${index + 1}`}
                          placeholder="Nome Sessione"
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
                        <div className="temporal-create-tree-row__actions">
                          <button
                            type="button"
                            className="is-remove"
                            aria-label={`Rimuovi Sessione ${index + 1}`}
                            onClick={() =>
                              editRows(
                                'planned_slices',
                                sessions.filter((_, i) => i !== index),
                              )
                            }
                          >
                            ×
                          </button>
                        </div>
                      </div>
                      {row.time_enabled !== false ? (
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
                      ) : null}
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
                    </div>
                  ))}
                  <div className="temporal-create-activity-tree__root-actions">
                    <button
                      type="button"
                      className="temporal-create-tree-add"
                      onClick={() =>
                        editRows('planned_slices', [
                          ...sessions,
                          { name: '', time_enabled: false },
                        ])
                      }
                    >
                      + Sessione
                    </button>
                  </div>
                  <details className="timeline-recurring-series-editor__advanced">
                    <summary>Opzioni Sessione e struttura</summary>
                    <label>
                      Sessione dell’attività{' '}
                      <select
                        value={asText(template.session_capture_mode)}
                        onChange={(e) =>
                          updateTemplate({
                            session_capture_mode: e.target.value,
                          })
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
                  </details>
                </section>
                <section
                  className="temporal-create-activity-intervals timeline-activity-editor__intervals"
                  aria-label="Intervalli"
                >
                  {(intervals.length ? intervals : [root]).map((row, index) => (
                    <SeriesIntervalFields
                      key={index}
                      selectedDate={source.selectedDate}
                      wallTime={time}
                      row={row}
                      index={index}
                      onChange={(next) => {
                        if (intervals.length) {
                          editIntervals(
                            intervals.map((item, i) =>
                              i === index ? next : item,
                            ),
                          );
                        } else {
                          changeStructure({
                            ...structure,
                            duration_minutes: next.duration_minutes,
                            activity_template: {
                              ...template,
                              root_window: next,
                            },
                          });
                        }
                      }}
                      onRemove={
                        intervals.length > 1
                          ? () =>
                              editIntervals(
                                intervals.filter((_, i) => i !== index),
                              )
                          : undefined
                      }
                    />
                  ))}
                  <button
                    type="button"
                    className="temporal-create-activity-intervals__add"
                    onClick={() => {
                      const existing = intervals.length ? intervals : [root];
                      const last = existing[existing.length - 1] ?? root;
                      editIntervals([
                        ...existing,
                        {
                          start_offset_minutes:
                            asNumber(last.start_offset_minutes) +
                            asNumber(last.duration_minutes) +
                            15,
                          duration_minutes: 30,
                        },
                      ]);
                    }}
                  >
                    + Aggiungi intervallo
                  </button>
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
                    className="temporal-create-tree-add"
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
            <section
              className="temporal-create-section is-wide temporal-create-repeat timeline-recurring-series-editor__recurrence timeline-activity-editor__repeat"
              aria-label="Ricorrenza"
            >
              <div className="temporal-create-section__heading temporal-create-repeat__heading">
                <h3>Ripetizione</h3>
              </div>
              {owner === 'routine' ? (
                <details className="timeline-recurring-series-editor__advanced">
                  <summary>Ora di riferimento della ricorrenza</summary>
                  <TimeControl
                    label="Ora di riferimento"
                    value={time.slice(0, 5)}
                    dataPath="series.anchorTime"
                    onChange={changeTime}
                  />
                </details>
              ) : null}
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
              <div className="temporal-create-repeat__row">
                <span className="temporal-create-repeat__row-label">
                  Ripeti ogni
                </span>
                <input
                  className="temporal-create-repeat__interval"
                  aria-label="Intervallo di ripetizione"
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
                />
                <span className="temporal-create-repeat__unit-label">
                  {recurrence.pattern_code === 'weekly_weekdays'
                    ? 'settimana'
                    : recurrence.pattern_code === 'monthly_month_days' ||
                        recurrence.pattern_code === 'monthly_ordinal_weekdays'
                      ? 'mese'
                      : recurrence.pattern_code === 'yearly_month_days'
                        ? 'anno'
                        : 'giorno'}
                </span>
              </div>
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
              <div className="temporal-create-repeat__end-row">
                <span className="temporal-create-repeat__row-label">
                  Termina
                </span>
                <div
                  className="temporal-create-repeat__end-choices"
                  role="radiogroup"
                  aria-label="Fine ripetizione"
                >
                  {(
                    [
                      ['open', 'Mai'],
                      ['until_boundary', 'Data'],
                      ['expected_count', 'Dopo'],
                    ] as const
                  ).map(([mode, label]) => (
                    <div
                      key={mode}
                      className={`temporal-create-repeat__end-option${recurrence.range_kind === mode ? ' is-active' : ''}`}
                    >
                      <button
                        type="button"
                        role="radio"
                        aria-checked={recurrence.range_kind === mode}
                        className={`temporal-create-repeat__end-choice${recurrence.range_kind === mode ? ' is-active' : ''}`}
                        onClick={() =>
                          changeRecurrence({
                            ...recurrence,
                            range_kind: mode,
                            effective_until:
                              mode === 'until_boundary'
                                ? asText(recurrence.effective_until) ||
                                  dayAfter(source.selectedDate)
                                : null,
                            expected_occurrence_count:
                              mode === 'expected_count'
                                ? asNumber(
                                    recurrence.expected_occurrence_count,
                                  ) || 1
                                : null,
                          })
                        }
                      >
                        <span
                          className="temporal-create-repeat__radio-dot"
                          aria-hidden="true"
                        />
                        <span>{label}</span>
                      </button>
                      {mode === 'until_boundary' ? (
                        <div className="temporal-create-repeat__end-date">
                          <TemporalCreateDatePicker
                            label="Ultimo giorno"
                            locale="it"
                            value={
                              asText(recurrence.effective_until)
                                ? dayBefore(asText(recurrence.effective_until))
                                : source.selectedDate
                            }
                            onChange={(day) =>
                              changeRecurrence({
                                ...recurrence,
                                range_kind: 'until_boundary',
                                effective_until: dayAfter(day),
                                expected_occurrence_count: null,
                              })
                            }
                          />
                        </div>
                      ) : null}
                      {mode === 'expected_count' ? (
                        <label className="temporal-create-repeat__count">
                          <input
                            type="number"
                            min={1}
                            aria-label="Numero di occorrenze"
                            value={
                              asNumber(recurrence.expected_occurrence_count) ||
                              1
                            }
                            onFocus={() =>
                              changeRecurrence({
                                ...recurrence,
                                range_kind: 'expected_count',
                                effective_until: null,
                                expected_occurrence_count:
                                  asNumber(
                                    recurrence.expected_occurrence_count,
                                  ) || 1,
                              })
                            }
                            onChange={(e) =>
                              changeRecurrence({
                                ...recurrence,
                                range_kind: 'expected_count',
                                effective_until: null,
                                expected_occurrence_count: Number(
                                  e.target.value,
                                ),
                              })
                            }
                          />
                          <span>occorrenze</span>
                        </label>
                      ) : null}
                    </div>
                  ))}
                </div>
              </div>
            </section>
            <section
              className="temporal-create-reality-objectives timeline-activity-editor__outcome"
              aria-label="Svolgimento e obiettivi"
            >
              <div className="temporal-create-reality-objectives__heading timeline-activity-editor__section-heading">
                <h3>Svolgimento e obiettivi</h3>
                <p>
                  Decidi se verificare lo svolgimento e quali risultati vuoi
                  misurare.
                </p>
              </div>
              <div className="temporal-create-reality-objectives__block is-reality">
                <div className="temporal-create-reality-objectives__block-copy">
                  <strong>Svolgimento dell’attività</strong>
                </div>
                <div
                  className="temporal-create-reality-mode"
                  role="radiogroup"
                  aria-label="Verifica dello svolgimento"
                >
                  {(
                    [
                      ['manual', 'Nessuna verifica'],
                      ['review_on_end', 'Chiedi al termine'],
                      ['auto_confirm_outcome', 'Conferma automatica'],
                    ] as const
                  ).map(([mode, label]) => (
                    <button
                      key={mode}
                      type="button"
                      role="radio"
                      aria-checked={
                        (owner === 'routine'
                          ? template.reality_mode
                          : structure.reality_mode) === mode
                      }
                      className={
                        (owner === 'routine'
                          ? template.reality_mode
                          : structure.reality_mode) === mode
                          ? 'is-active'
                          : ''
                      }
                      onClick={() =>
                        owner === 'routine'
                          ? updateTemplate({ reality_mode: mode })
                          : changeStructure({
                              ...structure,
                              reality_mode: mode,
                            })
                      }
                    >
                      {label}
                    </button>
                  ))}
                </div>
              </div>
              <div className="temporal-create-reality-objectives__divider" />
              <div className="temporal-create-reality-objectives__block is-objectives timeline-activity-editor__readback">
                <div className="temporal-create-reality-objectives__block-copy">
                  <strong>Obiettivi</strong>
                </div>
                <div className="timeline-activity-editor__objectives">
                  {objectives.map((row, index) => (
                    <div
                      key={index}
                      className="timeline-recurring-series-editor__objective"
                    >
                      <span>{index + 1}</span>
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
                        onChange={(e) =>
                          changeObjectiveKind(index, e.target.value)
                        }
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
                        aria-label={`Rimuovi obiettivo ${index + 1}`}
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
                        ×
                      </button>
                    </div>
                  ))}
                  <button
                    type="button"
                    className="timeline-activity-editor__add-objective"
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
                    + Aggiungi obiettivo
                  </button>
                </div>
              </div>
            </section>
            <section
              className="timeline-activity-editor__area-color"
              aria-label="Life Area"
            >
              {!activeArea ? (
                <TemporalColorControl
                  value={color}
                  label="Colore attività o evento"
                  onChange={(value) => updateMetadata(setColor, value)}
                />
              ) : null}
              <TemporalLifeAreaSelect
                query={areaQuery}
                label="Area assegnata"
                options={areas.map((area) => ({
                  id: area.ref,
                  label: area.name,
                  colorCode: area.colorCode,
                }))}
                selectedId={activeArea || null}
                onQueryChange={(value) => {
                  setAreaQuery(value);
                  setReview(null);
                }}
                onChoose={(area) => {
                  setAreaQuery(area.label);
                  updateMetadata(setColor, '');
                  if (owner === 'routine')
                    updateTemplate({ life_area_ref: area.id });
                  else
                    changeStructure({ ...structure, life_area_ref: area.id });
                }}
                onClear={() => {
                  setAreaQuery('');
                  if (owner === 'routine')
                    updateTemplate({ life_area_ref: null });
                  else changeStructure({ ...structure, life_area_ref: null });
                }}
              />
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
