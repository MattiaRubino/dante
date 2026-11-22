import {
  useCallback,
  useEffect,
  useId,
  useRef,
  useState,
  type RefObject,
} from 'react';
import { Temporal } from '@dante/time';
import { createWebFetch } from '../../../../platform/api/web-fetch';
import { createRemoteTemporalResponsibilityDataSource } from '../../../temporal/remote-responsibility-data-source';

import {
  createRemoteRecurringSeriesEdit,
  type RecurringSeriesReview,
  type RecurringSeriesSource,
  type SeriesScope,
} from '../../../temporal/remote-recurring-series-edit';
import { createRemoteRecurringProfileEdit } from '../../../temporal/remote-recurring-profile-edit';
import type { TemporalOccurrenceInventoryReviewLease } from '../../../temporal/temporal-occurrence-inventory-fence';
import { initialRecurrenceForScope } from './recurring-series-bounds';
import { TemporalCreatePlacementLockButton } from '../../../temporal-create/ui/temporal-create-placement-lock-button';
import { TemporalAuthoringTitleRow } from '../../../temporal-create/ui/temporal-authoring-title-row';
import { useTemporalRequiredTitle } from '../../../temporal-create/ui/temporal-required-title';
import { TIME_BANDS, TimeControl, type TimeBand } from '../../../temporal-create/ui/temporal-create-core-u2';
import { TemporalColorControl } from '../../../temporal-create/ui/temporal-color-control';
import { TemporalCreateDatePicker } from '../../../temporal-create/ui/temporal-create-date-picker';
import {
  TemporalRecurrenceChoice,
  TemporalRecurrencePanel,
} from '../../../temporal-create/ui/temporal-recurrence-panel';
import { TemporalLifeAreaSelect } from '../../../temporal-create/ui/temporal-life-area-select';
import { TemporalCreateEventAgenda } from '../../../temporal-create/ui/temporal-create-event-agenda';
import { TemporalEventParticipantsFields } from '../../../temporal-create/ui/temporal-create-event-participants';
import { TemporalTimeZoneControl } from '../../../temporal-create/ui/temporal-time-zone-control';
import { TemporalObjectiveEditorRow } from '../../../temporal-create/ui/temporal-objective-editor-row';
import { capTemporalRecurrenceCount } from '../../../temporal-create/model/temporal-create-session';
import { objectiveFieldIssue, objectiveFieldIssues } from '../../../temporal-create/model/temporal-objective-validation';
import type {
  TemporalCreateObjectiveDraft,
  TemporalCreateObjectiveKind,
  TemporalCreateObjectiveComparator,
  TemporalCreateEventParticipantDraft,
} from '../../../temporal-create/model/temporal-create-u2-authoring';
import { TemporalReminderControl } from '../../../temporal-create/ui/temporal-create-quick-reminder';
import '../../../temporal-create/ui/temporal-create-calendar-recurrence-fields.css';
import './activity-edit-panel.css';
import '../../../temporal-create/ui/temporal-editor-section-typography.css';

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

const objectiveNumber = (value: unknown): string =>
  typeof value === 'number' && Number.isFinite(value) ? String(value) : '';

const protectionLabel = (reason: string): string => {
  switch (reason) {
    case 'local_change':
      return 'Modificata singolarmente: resta invariata';
    case 'registration':
      return 'Con registrazioni: resta invariata';
    case 'skipped':
      return 'Saltata: resta invariata';
    default:
      return 'Eccezione conservata: resta invariata';
  }
};

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

/** The same four time bands and side menu used by Advanced Create. */
function SeriesTimeBandPicker({
  onSelect,
}: Readonly<{ onSelect: (band: TimeBand) => void }>) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!open) return;
    const dismiss = (event: PointerEvent) => {
      if (event.target instanceof Node && !rootRef.current?.contains(event.target))
        setOpen(false);
    };
    document.addEventListener('pointerdown', dismiss, true);
    return () => document.removeEventListener('pointerdown', dismiss, true);
  }, [open]);

  const labels = {
    morning: 'Mattina',
    afternoon: 'Pomeriggio',
    evening: 'Sera',
    night: 'Notte',
  } as const;

  return (
    <div ref={rootRef} className="temporal-create-time-band-control">
      <button
        type="button"
        className="temporal-create-time-band-trigger"
        aria-label="Fasce orarie"
        aria-expanded={open}
        onClick={() => setOpen((current) => !current)}
      >
        <span aria-hidden="true">→</span>
        <small aria-hidden="true">⌄</small>
      </button>
      {open ? (
        <div className="temporal-create-time-band-panel" role="dialog" aria-label="Fasce orarie">
          {TIME_BANDS.map((band) => (
            <button
              key={band.key}
              type="button"
              onClick={() => {
                onSelect(band);
                setOpen(false);
              }}
            >
              <strong>{labels[band.key]}</strong>
              <small>{band.start}–{band.end}</small>
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}

export function SeriesIntervalFields({
  selectedDate,
  wallTime,
  row,
  index,
  onChange,
  onRemove,
  kind = 'interval',
  invalid = false,
  showLabel = true,
}: Readonly<{
  selectedDate: string;
  wallTime: string;
  row: Entry;
  index: number;
  onChange: (row: Entry) => void;
  onRemove?: (() => void) | undefined;
  kind?: 'interval' | 'session';
  invalid?: boolean;
  showLabel?: boolean;
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
      duration_minutes: asNumber(row.duration_minutes),
    });
  };
  const changeEnd = (day: string, time: string) => {
    const next = Temporal.PlainDateTime.from(`${day}T${time}`);
    onChange({
      ...row,
      duration_minutes: start.until(next).total({ unit: 'minutes' }),
    });
  };
  const changeBand = (band: TimeBand) => {
    const startAt = Temporal.PlainDateTime.from(
      `${start.toPlainDate().toString()}T${band.start}`,
    );
    const endAt = Temporal.PlainDateTime.from(
      `${start.toPlainDate().toString()}T${band.end}`,
    ).add({ days: band.end <= band.start ? 1 : 0 });
    onChange({
      ...row,
      start_offset_minutes: anchor.until(startAt).total({ unit: 'minutes' }),
      duration_minutes: startAt.until(endAt).total({ unit: 'minutes' }),
    });
  };
  return (
    <div
      className="temporal-create-activity-interval"
      data-edit-invalid={invalid || asNumber(row.duration_minutes) <= 0}
    >
      {showLabel ? (
        <span className="temporal-create-activity-interval__label">
          {kind === 'interval' ? 'Intervallo' : 'Orario Sessione'} {index + 1}
        </span>
      ) : null}
      <div className={`temporal-create-activity-interval__fields timeline-activity-editor__interval-fields temporal-schedule-time-grid${
          onRemove ? ' has-remove-track' : ''
        }`}>
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
          dataPath={`series.${kind}.${index}.start`}
          onChange={(value) =>
            changeStart(start.toPlainDate().toString(), value)
          }
        />
        <SeriesTimeBandPicker onSelect={changeBand} />
        <TimeControl
          label="Fine"
          value={end.toPlainTime().toString({ smallestUnit: 'minute' })}
          invalid={invalid || asNumber(row.duration_minutes) <= 0}
          dataPath={`series.${kind}.${index}.end`}
          onChange={(value) => changeEnd(end.toPlainDate().toString(), value)}
        />
        <TemporalCreateDatePicker
          label="Data fine"
          align="end"
          locale="it"
          value={end.toPlainDate().toString()}
          min={start.toPlainDate().toString()}
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
  const [participation] = useState(
    createRemoteTemporalResponsibilityDataSource,
  );
  const [request] = useState(() => createWebFetch(globalThis.fetch));
  const [source, setSource] = useState<RecurringSeriesSource | null>(null);
  const [structure, setStructure] = useState<Entry>({});
  const [objectiveValidationVisible, setObjectiveValidationVisible] = useState(false);
  const [recurrence, setRecurrence] = useState<Entry>({});
  const [title, setTitle] = useState('');
  const titleFeedback = useTemporalRequiredTitle(title);
  const titleRef = useRef<HTMLInputElement>(null);
  const titleErrorId = useId();
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState('');
  const [color, setColor] = useState('');
  const [areas, setAreas] = useState<
    readonly {
      ref: string;
      name: string;
      colorCode: string | null;
      revision: number;
    }[]
  >([]);
  const [areaQuery, setAreaQuery] = useState('');
  const [newAreaColor, setNewAreaColor] = useState('#EA5C12');
  const [areaColorOverride, setAreaColorOverride] = useState<string | null>(
    null,
  );
  const [areaError, setAreaError] = useState('');
  const [participantLabels, setParticipantLabels] = useState<
    Record<string, string>
  >({});
  const [review, setReview] = useState<RecurringSeriesReview | null>(null);
  const [reviewedIntent, setReviewedIntent] = useState<
    Parameters<typeof remote.preview>[0] | null
  >(null);
  const [busy, setBusy] = useState(false);
  const [lastEditedInterval, setLastEditedInterval] = useState<number | null>(null);
  const [error, setError] = useState('');
  const operation = useRef(crypto.randomUUID());
  const reviewDialogRef = useRef<HTMLDivElement>(null);
  const previewButtonRef = useRef<HTMLButtonElement>(null);
  const reviewLeaseRef = useRef<TemporalOccurrenceInventoryReviewLease | null>(
    null,
  );
  const previewEpochRef = useRef(0);
  const discardReview = useCallback(() => {
    previewEpochRef.current += 1;
    reviewLeaseRef.current?.release();
    reviewLeaseRef.current = null;
    setReview(null);
  }, []);
  const cancelEditor = useCallback(() => {
    discardReview();
    onCancel();
  }, [discardReview, onCancel]);

  // Form changes invalidate the review without reading refs in render paths.
  useEffect(() => {
    if (review === null) {
      reviewLeaseRef.current?.release();
      reviewLeaseRef.current = null;
    }
  }, [review]);

  useEffect(() => {
    return () => {
      previewEpochRef.current += 1;
      reviewLeaseRef.current?.release();
      reviewLeaseRef.current = null;
    };
  }, []);

  useEffect(() => {
    let active = true;
    void Promise.all([
      remote.load(occurrenceRef),
      request('/api/v1/temporal/life-areas').then(async (response) => {
        if (!response.ok) throw new Error('Aree non disponibili.');
        return response.json() as Promise<unknown>;
      }),
      owner === 'event'
        ? participation.listPersonReferents()
        : Promise.resolve([]),
    ])
      .then(([loaded, catalog, people]) => {
        if (!active) return;
        if (loaded.owner !== owner || !Array.isArray(catalog)) {
          throw new Error('La serie selezionata non corrisponde all’editor.');
        }
        const template =
          owner === 'routine'
            ? asEntry(loaded.structure.activity_template)
            : {};
        const assignedArea = asText(
          owner === 'routine'
            ? template.life_area_ref
            : loaded.structure.life_area_ref,
        );
        const areaOptions = catalog
          .map(asEntry)
          .filter(
            (area) =>
              area.archived === false ||
              asText(area.life_area_ref) === assignedArea,
          )
          .map((area) => ({
            ref: asText(area.life_area_ref),
            name: asText(area.name),
            colorCode: asText(area.color_code) || null,
            revision: asNumber(area.revision),
          }));
        setAreas(areaOptions);
        const labels: Record<string, string> = { self: 'Io' };
        for (const person of people) {
          labels[person.personRef] = person.displayLabel;
        }
        setParticipantLabels(labels);
        setSource(loaded);
        setStructure(loaded.structure);
        setObjectiveValidationVisible(false);
        setRecurrence(initialRecurrenceForScope(loaded, scope));
        setTitle(loaded.title);
        setAreaQuery(
          areaOptions.find((area) => area.ref === assignedArea)?.name ?? '',
        );
        setNewAreaColor('#EA5C12');
        setAreaColorOverride(null);
        setAreaError('');
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
  }, [occurrenceRef, owner, participation, remote, request, scope]);

  useEffect(() => {
    if (!closeRequestRef) return;
    closeRequestRef.current = review
      ? busy
        ? () => undefined
        : discardReview
      : cancelEditor;
    return () => {
      closeRequestRef.current = null;
    };
  }, [busy, cancelEditor, closeRequestRef, discardReview, review]);

  useEffect(() => {
    if (!review) return;
    const dialog = reviewDialogRef.current;
    const previewButton = previewButtonRef.current;
    dialog?.querySelector<HTMLButtonElement>('button')?.focus();
    const dismiss = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && !busy) {
        event.stopImmediatePropagation();
        event.preventDefault();
        discardReview();
      } else if (event.key === 'Tab' && dialog) {
        const buttons = Array.from(
          dialog.querySelectorAll<HTMLButtonElement>('button:not(:disabled)'),
        );
        const first = buttons[0];
        const last = buttons.at(-1);
        if (!first || !last) return;
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    };
    document.addEventListener('keydown', dismiss, true);
    return () => {
      document.removeEventListener('keydown', dismiss, true);
      previewButton?.focus();
    };
  }, [busy, discardReview, review]);

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
  const editRows = (key: string, rows: Entry[]) => {
    if (key === 'objectives') setObjectiveValidationVisible(false);
    changeStructure(writeRows(structure, owner, key, rows));
  };
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
  const objectiveDraft = (
    row: Entry,
    index: number,
  ): TemporalCreateObjectiveDraft => ({
    id: String(index),
    label: asText(row.label),
    resultKind: (asText(row.result_kind) ||
      'boolean') as TemporalCreateObjectiveKind,
    comparatorCode: (asText(row.comparator_code) ||
      null) as TemporalCreateObjectiveComparator | null,
    targetValue: objectiveNumber(row.target_value),
    targetMin: objectiveNumber(row.target_min),
    targetMax: objectiveNumber(row.target_max),
    unitCode: asText(row.unit_code),
    verificationMode:
      row.verification_mode === 'review_on_end' ? 'review_on_end' : 'none',
  });
  const updateObjectiveDraft = (
    index: number,
    patch: Partial<TemporalCreateObjectiveDraft>,
  ) => {
    const changes: Entry = {};
    if (patch.label !== undefined) changes.label = patch.label;
    if (patch.comparatorCode !== undefined)
      changes.comparator_code = patch.comparatorCode;
    if (patch.targetValue !== undefined)
      changes.target_value =
        patch.targetValue === '' ? null : Number(patch.targetValue);
    if (patch.targetMin !== undefined)
      changes.target_min =
        patch.targetMin === '' ? null : Number(patch.targetMin);
    if (patch.targetMax !== undefined)
      changes.target_max =
        patch.targetMax === '' ? null : Number(patch.targetMax);
    if (patch.unitCode !== undefined)
      changes.unit_code = patch.unitCode.trim() || null;
    if (patch.verificationMode !== undefined)
      changes.verification_mode = patch.verificationMode;
    changeObjective(index, changes);
  };
  const moveObjective = (index: number, direction: -1 | 1) => {
    const reordered = [...objectives];
    const [item] = reordered.splice(index, 1);
    if (!item) return;
    reordered.splice(index + direction, 0, item);
    editRows(
      'objectives',
      reordered.map((row, position) => ({
        ...row,
        presentation_order: position,
      })),
    );
  };
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
  const invalidSeriesIntervals = new Set<number>();
  const orderedSeriesIntervals = intervals.map((row, index) => {
    const start = asNumber(row.start_offset_minutes);
    const duration = asNumber(row.duration_minutes);
    if (duration <= 0) invalidSeriesIntervals.add(index);
    return { index, start, end: start + duration, duration };
  }).sort((a, b) => a.start - b.start);
  for (let index = 1; index < orderedSeriesIntervals.length; index++) {
    const previous = orderedSeriesIntervals[index - 1]!;
    const current = orderedSeriesIntervals[index]!;
    if (previous.duration > 0 && current.duration > 0 && previous.end > current.start) {
      invalidSeriesIntervals.add(
        lastEditedInterval === previous.index || lastEditedInterval === current.index
          ? lastEditedInterval : current.index,
      );
    }
  }
  const sessions = asRows(template.planned_slices);
  const agenda = Array.isArray(structure.agenda_parts)
    ? structure.agenda_parts.map(asText)
    : [];
  const eventParticipants: TemporalCreateEventParticipantDraft[] = asRows(
    structure.expected_participants,
  ).map((item) => ({
    personRef: asText(item.person_ref),
    displayLabel:
      participantLabels[asText(item.person_ref)] ?? 'Persona non disponibile',
    requirementCode: asText(item.requirement_code) as 'required' | 'optional',
  }));
  const activeArea = asText(
    owner === 'routine' ? template.life_area_ref : structure.life_area_ref,
  );
  const activeAreaOption = areas.find((area) => area.ref === activeArea);
  const normalizedAreaName = areaQuery.trim().replace(/\s+/g, ' ');
  const creatingArea =
    !!normalizedAreaName &&
    !activeArea &&
    !areas.some(
      (area) =>
        area.name.toLocaleLowerCase() ===
        normalizedAreaName.toLocaleLowerCase(),
    );
  const changingAreaColor =
    !!activeAreaOption &&
    areaColorOverride !== null &&
    areaColorOverride.toUpperCase() !==
      (activeAreaOption.colorCode ?? '').toUpperCase();
  // A recurrence's wall-clock anchor is an internal coordinate. Activity
  // intervals remain the only user-facing time controls: changing their
  // start/end updates the stored relative offsets without exposing or
  // silently rewriting the source coordinate (which also identifies occurrences).
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
  const seriesStartDate =
    asText(recurrence.effective_from) || source?.selectedDate || '';
  const seriesStartTime = time.slice(0, 5) || '09:00';
  const seriesStart = seriesStartDate
    ? Temporal.PlainDateTime.from(`${seriesStartDate}T${seriesStartTime}`)
    : null;
  const seriesEnd = seriesStart?.add({
    minutes: Math.max(1, asNumber(structure.duration_minutes) || 30),
  });
  const seriesLastDay = seriesStartDate
    ? Temporal.PlainDate.from(seriesStartDate)
        .add({ days: Math.max(1, asNumber(structure.duration_days) || 1) - 1 })
        .toString()
    : '';
  const changeSeriesEnd = (day: string, clock: string) => {
    if (!seriesStart) return;
    const next = Temporal.PlainDateTime.from(`${day}T${clock}`);
    const minutes = seriesStart.until(next).total({ unit: 'minutes' });
    if (minutes > 0)
      changeStructure({ ...structure, duration_minutes: minutes });
  };
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
    discardReview();
  };

  const prepare = async () => {
    if (!source || busy) return;
    setError('');
    setAreaError('');
    const invalidObjective = objectives.findIndex((row, index) =>
      objectiveFieldIssue(objectiveDraft(row, index)),
    );
    if (invalidObjective !== -1) {
      setObjectiveValidationVisible(true);
      requestAnimationFrame(() => {
        document.querySelector<HTMLElement>(
          `[data-objective-id="${invalidObjective}"] [aria-invalid="true"]`,
        )?.focus();
      });
      return;
    }
    if (!titleFeedback.validate()) {
      titleRef.current?.focus();
      return;
    }
    if (recurrence.range_kind === 'expected_count') {
      const count = asNumber(recurrence.expected_occurrence_count);
      if (!Number.isInteger(count) || count < 1) {
        setError(
          'Non ci sono istanze successive da modificare. Cambia esplicitamente il limite per estendere la serie.',
        );
        return;
      }
      if (count > 730) {
        setError('Inserisci da 1 a 730 occorrenze.');
        return;
      }
    }
    if (normalizedAreaName && !activeArea && !creatingArea) {
      setAreaError('Scegli l’area già esistente dall’elenco.');
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
    if (invalidSeriesIntervals.size > 0) return;
    const previewEpoch = ++previewEpochRef.current;
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
      const areaIntent = creatingArea
        ? {
            new_life_area: {
              name: normalizedAreaName,
              color_code: newAreaColor.toUpperCase(),
            },
          }
        : changingAreaColor && activeAreaOption
          ? {
              area_color_change: {
                life_area_ref: activeAreaOption.ref,
                expected_revision: activeAreaOption.revision,
                color_code: (areaColorOverride ?? '#EA5C12').toUpperCase(),
              },
            }
          : {};
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
        structure: { ...completeStructure, ...areaIntent },
        profilePatch: Object.keys(patch).length ? patch : null,
        operationId: operation.current,
      };
      const { review: result, lease } = await remote.beginReview(intent);
      if (previewEpochRef.current !== previewEpoch) {
        lease.release();
        return;
      }
      reviewLeaseRef.current?.release();
      reviewLeaseRef.current = lease;
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
    const lease = reviewLeaseRef.current;
    if (!lease) {
      setError(
        'Anteprima non più disponibile. Controlla nuovamente le modifiche.',
      );
      discardReview();
      return;
    }
    setBusy(true);
    setError('');
    try {
      await remote.accept(reviewedIntent, review, lease);
      onSaved();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : 'Serie non salvata.');
    } finally {
      discardReview();
      setBusy(false);
    }
  };

  return (
    <div className="timeline-activity-editor timeline-recurring-series-editor">
      <div className="timeline-activity-editor__body">
        {error ? <p role="alert">{error}</p> : null}
        {!source && !error ? (
          <p role="status">Caricamento della serie…</p>
        ) : null}
        {source ? (
          <>
            {scope === 'from_next' ? (
              <p className="timeline-recurring-series-editor__source-note">
                Regola della serie dalla prossima istanza. Quella selezionata
                resta invariata; le sue modifiche locali non sono copiate qui.
              </p>
            ) : null}
            <TemporalAuthoringTitleRow
              kind={owner === 'event' ? 'event' : 'activity'}
              className="timeline-activity-editor__title-row"
              invalid={titleFeedback.invalid}
              shakeAttempt={titleFeedback.shakeAttempt}
            >
              <label className="timeline-activity-editor__title">
                <span className="timeline-activity-editor__visually-hidden">
                  Titolo
                </span>
                <input
                  ref={titleRef}
                  className="temporal-create-title-input"
                  aria-label="Titolo"
                  aria-invalid={titleFeedback.invalid}
                  aria-describedby={
                    titleFeedback.invalid ? titleErrorId : undefined
                  }
                  value={title}
                  maxLength={300}
                  onChange={(e) => {
                    titleFeedback.changed(e.target.value);
                    updateMetadata(setTitle, e.target.value);
                  }}
                />
              </label>
              {owner === 'routine' ? (
                <div className="temporal-create-title-row__tools timeline-activity-editor__title-tools">
                  <TemporalCreatePlacementLockButton
                    kind="activity"
                    locked={template.placement_protected === true}
                    disabled={busy}
                    onToggle={() =>
                      updateTemplate({
                        placement_protected:
                          template.placement_protected !== true,
                      })
                    }
                  />
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
              ) : (
                <div className="temporal-create-title-row__tools timeline-activity-editor__title-tools">
                  <TemporalCreatePlacementLockButton
                    kind="event"
                    locked={structure.placement_protected === true}
                    disabled={busy}
                    onToggle={() =>
                      changeStructure({
                        ...structure,
                        placement_protected:
                          structure.placement_protected !== true,
                      })
                    }
                  />
                </div>
              )}
            </TemporalAuthoringTitleRow>
            {titleFeedback.invalid ? (
              <small
                id={titleErrorId}
                className="temporal-create-field-error"
                role="alert"
              >
                Inserisci un titolo.
              </small>
            ) : null}
            {owner === 'event' ? (
              <TemporalCreateEventAgenda
                parts={agenda}
                maxPartLength={1000}
                onChange={(parts) =>
                  changeStructure({ ...structure, agenda_parts: [...parts] })
                }
                editStyle
              />
            ) : null}
            {owner === 'routine' ? (
              <section
                className="temporal-create-activity-tree timeline-activity-editor__sessions"
                aria-label="Sessioni attività"
              >
                <div
                  className="temporal-create-activity-tree__spine"
                  aria-hidden="true"
                />
                {sessions.length > 0 ? (
                  <div className="temporal-create-activity-tree__root-sessions">
                    <div className="temporal-create-activity-tree__group-label temporal-editor-section-heading">
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
                      </div>
                    ))}
                  </div>
                ) : null}
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
                    <span aria-hidden="true">＋</span>Sessione
                  </button>
                </div>
              </section>
            ) : null}
            <div
              className={`timeline-recurring-series-editor__time-block${owner === 'routine' ? ' is-activity' : ''}`}
            >
              <section
                className="timeline-recurring-series-editor__timing"
                aria-label="Orario della serie"
              >
                <div className="temporal-time-mode-toolbar">
                  <div
                    className="timeline-activity-editor__placement"
                    role="group"
                    aria-label="Tipo di orario"
                  >
                    {owner === 'event' ? (
                      (['timed', 'all_day'] as const).map((kind) => (
                        <button
                          key={kind}
                          type="button"
                          className={
                            structure.placement_kind === kind
                              ? 'is-selected'
                              : ''
                          }
                          aria-pressed={structure.placement_kind === kind}
                          onClick={() => {
                            if (structure.placement_kind === kind) return;
                            const allDay = kind === 'all_day';
                            changeStructure({
                              ...structure,
                              placement_kind: kind,
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
                        >
                          {kind === 'timed' ? 'Orario' : 'Tutto il giorno'}
                        </button>
                      ))
                    ) : (
                      <>
                        <button
                          type="button"
                          className={
                            template.placement_kind === 'all_day'
                              ? ''
                              : 'is-selected'
                          }
                          aria-pressed={template.placement_kind !== 'all_day'}
                          onClick={() => {
                            if (template.placement_kind !== 'all_day') return;
                            changeStructure({
                              ...structure,
                              duration_minutes: 60,
                              activity_template: {
                                ...template,
                                placement_kind: undefined,
                                duration_days: undefined,
                                root_window: {
                                  start_offset_minutes: 0,
                                  duration_minutes: 60,
                                },
                              },
                            });
                            changeRecurrence({
                              ...recurrence,
                              wall_times: ['09:00:00'],
                            });
                          }}
                        >
                          Orario
                        </button>
                        <button
                          type="button"
                          className={
                            template.placement_kind === 'all_day'
                              ? 'is-selected'
                              : ''
                          }
                          aria-pressed={template.placement_kind === 'all_day'}
                          disabled={
                            intervals.length > 0 ||
                            asRows(template.children).some(
                              (child) =>
                                child.placement !== null ||
                                asRows(child.planned_slices).length > 0,
                            )
                          }
                          onClick={() => {
                            if (template.placement_kind === 'all_day') return;
                            changeStructure({
                              ...structure,
                              duration_minutes: 1440,
                              reminder_lead_minutes: null,
                              activity_template: {
                                ...template,
                                placement_kind: 'all_day',
                                duration_days: 1,
                                root_window: null,
                              },
                            });
                            changeRecurrence({ ...recurrence, wall_times: [] });
                          }}
                        >
                          Tutto il giorno
                        </button>
                      </>
                    )}
                  </div>
                  <TemporalTimeZoneControl
                    zoneId={asText(recurrence.zone_id) || null}
                    allowFloating={false}
                    allowDistinctZones={false}
                    date={seriesStartDate}
                    onChange={(zoneId) => {
                      if (zoneId)
                        changeRecurrence({ ...recurrence, zone_id: zoneId });
                    }}
                  />
                </div>
                {owner === 'event' &&
                structure.placement_kind === 'timed' &&
                seriesStart &&
                seriesEnd ? (
                  <div className="temporal-create-activity-interval__fields timeline-activity-editor__interval-fields temporal-schedule-time-grid">
                    <TemporalCreateDatePicker
                      label="Data inizio"
                      locale="it"
                      value={seriesStartDate}
                      onChange={(day) =>
                        changeRecurrence({
                          ...recurrence,
                          effective_from: day,
                          ...(recurrence.pattern_anchor_date
                            ? { pattern_anchor_date: day }
                            : {}),
                        })
                      }
                    />
                    <TimeControl
                      label="Inizio"
                      value={seriesStartTime}
                      dataPath="series.start"
                      onChange={changeTime}
                    />
                    <span
                      className="temporal-create-activity-interval__arrow"
                      aria-hidden="true"
                    >
                      →
                    </span>
                    <TimeControl
                      label="Fine"
                      value={seriesEnd
                        .toPlainTime()
                        .toString({ smallestUnit: 'minute' })}
                      dataPath="series.end"
                      onChange={(clock) =>
                        changeSeriesEnd(
                          seriesEnd.toPlainDate().toString() ===
                            seriesStartDate && clock <= seriesStartTime
                            ? dayAfter(seriesStartDate)
                            : seriesEnd.toPlainDate().toString(),
                          clock,
                        )
                      }
                    />
                    <TemporalCreateDatePicker
                      label="Data fine"
                      align="end"
                      locale="it"
                      value={seriesEnd.toPlainDate().toString()}
                      onChange={(day) =>
                        changeSeriesEnd(
                          day,
                          seriesEnd
                            .toPlainTime()
                            .toString({ smallestUnit: 'minute' }),
                        )
                      }
                    />
                  </div>
                ) : null}
                {owner === 'event' && structure.placement_kind === 'all_day' ? (
                  <div className="temporal-create-u2-all-day">
                    <TemporalCreateDatePicker
                      label="Data inizio"
                      locale="it"
                      value={seriesStartDate}
                      allDay
                      onChange={(day) =>
                        changeRecurrence({
                          ...recurrence,
                          effective_from: day,
                          ...(recurrence.pattern_anchor_date
                            ? { pattern_anchor_date: day }
                            : {}),
                        })
                      }
                    />
                    <TemporalCreateDatePicker
                      label="Data fine"
                      align="end"
                      locale="it"
                      value={seriesLastDay}
                      allDay
                      onChange={(day) => {
                        const duration =
                          Temporal.PlainDate.from(seriesStartDate)
                            .until(Temporal.PlainDate.from(day))
                            .total({ unit: 'days' }) + 1;
                        if (duration > 0)
                          changeStructure({
                            ...structure,
                            duration_days: duration,
                          });
                      }}
                    />
                  </div>
                ) : null}
              </section>
              {owner === 'routine' && template.placement_kind === 'all_day' ? (
                <label>
                  Giorni
                  <input
                    type="number"
                    min={1}
                    max={365}
                    value={asNumber(template.duration_days) || 1}
                    onChange={(event) => {
                      const days = Number(event.target.value);
                      changeStructure({
                        ...structure,
                        duration_minutes: days * 1440,
                        activity_template: { ...template, duration_days: days },
                      });
                    }}
                  />
                </label>
              ) : owner === 'routine' ? (
                <>
                  <section
                    className="temporal-create-activity-intervals timeline-activity-editor__intervals"
                    aria-label="Intervalli"
                  >
                    {(intervals.length ? intervals : [root]).map(
                      (row, index) => (
                        <SeriesIntervalFields
                          key={index}
                          selectedDate={source.selectedDate}
                          wallTime={time}
                          row={row}
                          index={index}
                          invalid={invalidSeriesIntervals.has(index)}
                          showLabel={intervals.length > 1}
                          onChange={(next) => {
                            setLastEditedInterval(index);
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
                      ),
                    )}
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
                </>
              ) : null}
            </div>
            <TemporalRecurrencePanel
              kind={owner === 'routine' ? 'activity' : 'event'}
              className="timeline-recurring-series-editor__repeat-panel"
              expanded
              choice={
                <div className="temporal-recurrence-panel__frequency">
                  <TemporalRecurrenceChoice
                    label="Ripeti"
                    value={asText(recurrence.pattern_code)}
                    onChange={changePattern}
                    options={[
                      { value: 'daily', label: 'Ogni giorno' },
                      {
                        value: 'weekly_weekdays',
                        label: 'Giorni della settimana',
                      },
                      { value: 'monthly_month_days', label: 'Giorni del mese' },
                      {
                        value: 'monthly_ordinal_weekdays',
                        label: 'Settimana del mese',
                      },
                      { value: 'yearly_month_days', label: 'Giorni dell’anno' },
                      { value: 'anchor_step', label: 'Passo fisso' },
                    ]}
                  />
                </div>
              }
            >
              <section
                className="temporal-create-section is-wide temporal-create-repeat timeline-recurring-series-editor__recurrence"
                aria-label="Dettagli ripetizione"
              >
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
                              month_days: monthDays.filter(
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
                                  ? dayBefore(
                                      asText(recurrence.effective_until),
                                    )
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
                              max={730}
                              aria-label="Numero di occorrenze"
                              value={asNumber(
                                recurrence.expected_occurrence_count,
                              )}
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
                                  expected_occurrence_count: capTemporalRecurrenceCount(
                                    Number(e.target.value),
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
            </TemporalRecurrencePanel>
            <section
              className="timeline-activity-editor__area-color temporal-editor-area-section"
              aria-label="Area"
            >
              <strong className="temporal-editor-section-heading">Area</strong>
              <TemporalColorControl
                value={
                  activeAreaOption
                    ? (areaColorOverride ??
                      activeAreaOption.colorCode ??
                      '#EA5C12')
                    : creatingArea
                      ? newAreaColor
                      : color || '#EA5C12'
                }
                label={
                  activeAreaOption
                    ? 'Colore dell’area'
                    : creatingArea
                      ? 'Colore della nuova area'
                      : 'Colore attività o evento'
                }
                onChange={(value) => {
                  if (activeAreaOption) {
                    setAreaColorOverride(value);
                    discardReview();
                  } else if (creatingArea) {
                    setNewAreaColor(value);
                    discardReview();
                  } else {
                    updateMetadata(setColor, value);
                  }
                  setAreaError('');
                }}
              />
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
                  setAreaColorOverride(null);
                  setAreaError('');
                  discardReview();
                  if (value.trim() !== activeAreaOption?.name) {
                    if (owner === 'routine')
                      updateTemplate({ life_area_ref: null });
                    else changeStructure({ ...structure, life_area_ref: null });
                  }
                }}
                onChoose={(area) => {
                  setAreaQuery(area.label);
                  setAreaColorOverride(null);
                  setAreaError('');
                  updateMetadata(setColor, '');
                  if (owner === 'routine')
                    updateTemplate({ life_area_ref: area.id });
                  else
                    changeStructure({ ...structure, life_area_ref: area.id });
                }}
                onClear={() => {
                  setAreaQuery('');
                  setAreaColorOverride(null);
                  setAreaError('');
                  if (owner === 'routine')
                    updateTemplate({ life_area_ref: null });
                  else changeStructure({ ...structure, life_area_ref: null });
                }}
              />
              {creatingArea ? (
                <small role="status">
                  La nuova area sarà creata insieme al salvataggio della serie.
                </small>
              ) : null}
              {changingAreaColor ? (
                <small role="status">
                  Modificare il colore dell’area aggiorna anche gli altri
                  elementi associati, comprese le istanze precedenti.
                </small>
              ) : null}
              {areaError ? (
                <small className="temporal-create-field-error" role="alert">
                  {areaError}
                </small>
              ) : null}
            </section>
            <section
              className="temporal-create-reality-objectives timeline-activity-editor__outcome"
              aria-label="Configurazione obiettivi"
            >
              <div className="temporal-create-reality-objectives__block is-objectives timeline-activity-editor__readback">
                <div className="temporal-create-reality-objectives__block-copy">
                  <strong className="temporal-editor-section-heading">
                    Obiettivi
                  </strong>
                </div>
                <div className="timeline-activity-editor__objectives">
                  {objectives.map((row, index) => (
                    <TemporalObjectiveEditorRow
                      key={index}
                      objective={objectiveDraft(row, index)}
                      index={index}
                      total={objectives.length}
                      variant="edit"
                      italian
                      issues={objectiveValidationVisible ? objectiveFieldIssues(objectiveDraft(row, index)) : undefined}
                      update={(_id, patch) =>
                        updateObjectiveDraft(index, patch)
                      }
                      changeKind={(_id, kind) =>
                        changeObjectiveKind(index, kind)
                      }
                      move={(_index, direction) =>
                        moveObjective(index, direction)
                      }
                      remove={() =>
                        editRows(
                          'objectives',
                          objectives
                            .filter((_, position) => position !== index)
                            .map((part, position) => ({
                              ...part,
                              presentation_order: position,
                            })),
                        )
                      }
                    />
                  ))}
                  <div className="temporal-create-objectives__root-actions">
                    <button
                      type="button"
                      className="temporal-create-objectives__add"
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
                            verification_mode: 'none',
                          },
                        ])
                      }
                    >
                      + Obiettivo
                    </button>
                  </div>
                </div>
              </div>
            </section>

            <div className="timeline-activity-editor__location">
              <input
                className="temporal-create-u2-location"
                aria-label="Località"
                placeholder="Località"
                value={location}
                onChange={(event) =>
                  updateMetadata(setLocation, event.target.value)
                }
              />
            </div>
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
            {owner === 'event' ? (
              <TemporalEventParticipantsFields
                participants={eventParticipants}
                onChange={(next) => {
                  setParticipantLabels((labels) => ({
                    ...labels,
                    ...Object.fromEntries(
                      next.map((item) => [item.personRef, item.displayLabel]),
                    ),
                  }));
                  changeStructure({
                    ...structure,
                    expected_participants: next.map((item) => ({
                      person_ref: item.personRef,
                      requirement_code: item.requirementCode,
                    })),
                  });
                }}
                disabled={busy}
              />
            ) : null}
            <section
              className="timeline-activity-editor__description temporal-create-section is-wide temporal-create-description-section"
              aria-label="Descrizione"
            >
              <h3>Descrizione</h3>
              <textarea
                className="temporal-create-u2-description temporal-create-advanced-description"
                aria-label="Descrizione"
                rows={5}
                value={description}
                onChange={(event) =>
                  updateMetadata(setDescription, event.target.value)
                }
              />
            </section>
          </>
        ) : null}
      </div>
      <div className="timeline-activity-editor__actions dante-temporal-panel-actions">
        <button type="button" disabled={busy} onClick={cancelEditor}>
          Annulla
        </button>
        <button
          type="button"
          ref={previewButtonRef}
          className="is-primary"
          disabled={
            busy || !source ||
            invalidSeriesIntervals.size > 0 ||
            (owner === 'routine' && [
              root,
              ...intervals,
              ...sessions.filter((row) => row.time_enabled !== false),
            ].some((row) => asNumber(row.duration_minutes) <= 0)) ||
            (owner === 'event' && structure.placement_kind === 'timed' &&
              asNumber(structure.duration_minutes) <= 0)
          }
          onClick={() => void prepare()}
        >
          {busy ? 'Attendi…' : 'Salva modifiche'}
        </button>
      </div>
      {review ? (
        <div className="timeline-recurring-series-review__backdrop">
          <div
            ref={reviewDialogRef}
            className="timeline-recurring-series-review__dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="timeline-recurring-series-review-title"
          >
            <h2 id="timeline-recurring-series-review-title">
              Controlla prima di salvare
            </h2>
            <p>
              {scope === 'from_next'
                ? 'Dalla prossima istanza'
                : 'Da questa istanza'}
              {recurrence.range_kind === 'open'
                ? ' · Ripetizione senza fine.'
                : '.'}
            </p>
            {review.protected.length > 0 ? (
              <div className="timeline-recurring-series-review__exceptions">
                <h3>Istanze che restano invariate</h3>
                <ul>
                  {review.protected.slice(0, 10).map((item) => (
                    <li key={item.occurrenceRef}>
                      {new Date(item.expectedAt).toLocaleString('it-IT')} ·{' '}
                      {protectionLabel(item.reason)}
                    </li>
                  ))}
                </ul>
                {review.protected.length > 10 ? (
                  <p>
                    Altre {review.protected.length - 10} istanze conservate.
                  </p>
                ) : null}
              </div>
            ) : (
              <p>Nessuna istanza già modificata resterà esclusa.</p>
            )}
            <div className="timeline-recurring-series-review__actions dante-temporal-panel-actions">
              <button
                type="button"
                disabled={busy}
                onClick={() => discardReview()}
              >
                Torna alla modifica
              </button>
              <button
                type="button"
                className="is-primary"
                disabled={busy}
                onClick={() => void accept()}
              >
                {busy ? 'Attendi…' : 'Conferma salvataggio'}
              </button>
            </div>
          </div>
        </div>
      ) : null}
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
