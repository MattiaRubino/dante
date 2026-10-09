import { Temporal, type PlainDate, type PlainDateTime } from '@dante/time';
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import { openPlanForActivity } from '../../../temporal/plan-work-intent';
import type {
  TemporalPlanningTrayDataSource,
  TemporalPlanningTrayItem,
} from '../../../temporal/planning-tray-data-source';
import { createRemoteTemporalPlanningTrayDataSource } from '../../../temporal/remote-planning-tray-data-source';
import { SessionSubjectControls } from '../../../temporal/session-subject-controls';
import {
  subscribeTemporalPlanningInvalidation,
  subscribeTemporalTimelineInvalidation,
} from '../../../temporal/timeline-invalidation';
import type { TemporalCreateRuntime } from '../../../temporal-create';
import type { TimelinePlanningTrayItem } from './timeline-planning-tray';

import './timeline-planning-tray.css';

type TimelineB01PlanningTrayProps = Readonly<{
  items?: readonly TimelinePlanningTrayItem[];
  runtime: TemporalCreateRuntime;
  defaultDate: PlainDate;
  onBeforeOpen?: (() => void) | undefined;
  source?: TemporalPlanningTrayDataSource | undefined;
  hiddenTrigger?: boolean;
  openRequest?: number;
}>;

type ReadState = 'loading' | 'ready' | 'error';

const PANEL_ID = 'timeline-planning-tray-b01';
const PANEL_GAP_PX = 8;
const PANEL_VIEWPORT_PADDING_PX = 12;
const PANEL_DESKTOP_WIDTH_PX = 390;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function copyFor(language: string) {
  const english = language.toLowerCase().startsWith('en');
  return english
    ? Object.freeze({
        title: 'Existing unplaced items',
        trigger: 'Open existing unplaced items',
        close: 'Close existing unplaced items',
        description: 'Already-created Activities and Events without accepted Timeline placement. They are not drafts.',
        loading: 'Loading items…',
        failed: 'Items to place are unavailable.',
        retry: 'Retry',
        search: 'Search items to place',
        searchPlaceholder: 'Search…',
        emptyTitle: 'Nothing to place',
        emptyBody: 'Activities and events without a placement will appear here.',
        activity: 'Activity',
        event: 'Event',
        postponed: 'Postponed',
        place: 'Place',
        placementTitle: 'Accepted Schedule',
        date: 'Date',
        time: 'Start',
        duration: 'Duration (minutes)',
        timeReference: 'Time reference',
        localTime: 'Local time',
        namedZoneTime: 'Specific time zone',
        timeZone: 'Time zone',
        cancel: 'Cancel',
        confirm: 'Place on Timeline',
        placing: 'Placing…',
        invalidPlacement: 'Choose a valid same-day interval.',
        placementFailed: 'The Schedule was not accepted. The item is still here.',
      })
    : Object.freeze({
        title: 'Elementi già creati',
        trigger: 'Apri elementi già creati',
        close: 'Chiudi elementi già creati',
        description: 'Attività ed Eventi già creati senza collocazione: non sono Bozze.',
        loading: 'Caricamento elementi…',
        failed: 'Gli elementi esistenti non sono disponibili.',
        retry: 'Riprova',
        search: 'Cerca tra gli elementi già creati',
        searchPlaceholder: 'Cerca…',
        emptyTitle: 'Niente da collocare',
        emptyBody: 'Attività ed eventi senza collocazione compariranno qui.',
        activity: 'Attività',
        event: 'Evento',
        postponed: 'Posticipato',
        place: 'Colloca',
        placementTitle: 'Schedule accettato',
        date: 'Data',
        time: 'Inizio',
        duration: 'Durata (minuti)',
        timeReference: 'Riferimento orario',
        localTime: 'Ora locale',
        namedZoneTime: 'Fuso specifico',
        timeZone: 'Fuso orario',
        cancel: 'Annulla',
        confirm: 'Colloca in Timeline',
        placing: 'Collocazione…',
        invalidPlacement: 'Scegli un intervallo valido nella stessa giornata.',
        placementFailed: 'Lo Schedule non è stato accettato. L’elemento resta qui.',
      });
}

function itemKey(item: TemporalPlanningTrayItem): string {
  return `${item.kind}:${item.subjectRef}`;
}

function operationId(item: TemporalPlanningTrayItem): string {
  const random = globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random()}`;
  return `planning-tray:${item.kind}:${item.subjectRef}:${random}`;
}

export function TimelinePlanningTrayB01({
  items: _items,
  runtime: _runtime,
  defaultDate,
  onBeforeOpen,
  source: injectedSource,
  hiddenTrigger = false,
  openRequest = 0,
}: TimelineB01PlanningTrayProps) {
  const { i18n } = useTranslation('common');
  const language = i18n.resolvedLanguage ?? i18n.language;
  const copy = copyFor(language);
  const source = useMemo(
    () => injectedSource ?? createRemoteTemporalPlanningTrayDataSource(),
    [injectedSource],
  );
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const panelRef = useRef<HTMLElement | null>(null);
  const searchRef = useRef<HTMLInputElement | null>(null);
  const readGenerationRef = useRef(0);
  const [actionsHost, setActionsHost] = useState<HTMLElement | null>(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [readState, setReadState] = useState<ReadState>('loading');
  const [remoteItems, setRemoteItems] = useState<readonly TemporalPlanningTrayItem[]>([]);
  const [placingKey, setPlacingKey] = useState<string | null>(null);
  const [placementDate, setPlacementDate] = useState(defaultDate.toString());
  const [placementTime, setPlacementTime] = useState('09:00');
  const [durationMinutes, setDurationMinutes] = useState(30);
  const [placementTimeMode, setPlacementTimeMode] = useState<'floating' | 'zoned'>('floating');
  const [placementTimeZone, setPlacementTimeZone] = useState(
    () => Intl.DateTimeFormat().resolvedOptions().timeZone || 'Europe/Rome',
  );
  const [placementPending, setPlacementPending] = useState(false);
  const [placementError, setPlacementError] = useState<string | null>(null);
  const [panelStyle, setPanelStyle] = useState<CSSProperties | undefined>();

  const lastExternalOpenRequest = useRef(openRequest);
  useEffect(() => {
    if (openRequest === lastExternalOpenRequest.current) return;
    lastExternalOpenRequest.current = openRequest;
    setOpen(true);
    setPlacingKey(null);
    setPlacementError(null);
  }, [openRequest]);

  const filteredItems = useMemo(() => {
    const normalized = query.trim().toLocaleLowerCase();
    if (!normalized) return remoteItems;
    return remoteItems.filter((item) =>
      item.title.toLocaleLowerCase().includes(normalized),
    );
  }, [query, remoteItems]);

  const refresh = useCallback(async () => {
    const generation = ++readGenerationRef.current;
    setReadState('loading');
    try {
      const items = await source.listItems();
      if (readGenerationRef.current !== generation) return;
      setRemoteItems(items);
      setReadState('ready');
    } catch {
      if (readGenerationRef.current === generation) setReadState('error');
    }
  }, [source]);

  useEffect(() => {
    void refresh();
    return () => {
      readGenerationRef.current += 1;
    };
  }, [refresh]);

  useEffect(() => {
    const reload = () => void refresh();
    const unsubscribePlanning = subscribeTemporalPlanningInvalidation(reload);
    const unsubscribeTimeline = subscribeTemporalTimelineInvalidation(reload);
    return () => {
      unsubscribePlanning();
      unsubscribeTimeline();
    };
  }, [refresh]);

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      setActionsHost(document.querySelector<HTMLElement>('.dante-timeline-actions'));
    });
    return () => cancelAnimationFrame(frame);
  }, []);

  const positionPanel = useCallback(() => {
    const trigger = triggerRef.current;
    if (!trigger || window.innerWidth <= 900) {
      setPanelStyle(undefined);
      return;
    }
    const rect = trigger.getBoundingClientRect();
    const width = Math.min(
      PANEL_DESKTOP_WIDTH_PX,
      window.innerWidth - PANEL_VIEWPORT_PADDING_PX * 2,
    );
    const left = clamp(
      rect.right - width,
      PANEL_VIEWPORT_PADDING_PX,
      window.innerWidth - width - PANEL_VIEWPORT_PADDING_PX,
    );
    const top = Math.max(PANEL_VIEWPORT_PADDING_PX, rect.bottom + PANEL_GAP_PX);
    setPanelStyle({
      top,
      left,
      right: 'auto',
      width,
      maxHeight: `calc(100dvh - ${top + PANEL_VIEWPORT_PADDING_PX}px)`,
    });
  }, []);

  useEffect(() => {
    if (!open) return;
    const frame = requestAnimationFrame(() => {
      positionPanel();
      searchRef.current?.focus();
    });
    const reposition = () => positionPanel();
    window.addEventListener('resize', reposition);
    document.addEventListener('scroll', reposition, true);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener('resize', reposition);
      document.removeEventListener('scroll', reposition, true);
    };
  }, [open, positionPanel]);

  useEffect(() => {
    if (!open) return;
    const closeOutside = (event: globalThis.PointerEvent) => {
      if (!(event.target instanceof Node)) return;
      if (panelRef.current?.contains(event.target) || triggerRef.current?.contains(event.target)) {
        return;
      }
      setOpen(false);
      setQuery('');
    };
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return;
      setOpen(false);
      setQuery('');
      requestAnimationFrame(() => triggerRef.current?.focus());
      event.preventDefault();
    };
    document.addEventListener('pointerdown', closeOutside, true);
    document.addEventListener('keydown', closeOnEscape, true);
    return () => {
      document.removeEventListener('pointerdown', closeOutside, true);
      document.removeEventListener('keydown', closeOnEscape, true);
    };
  }, [open]);

  const submitPlacement = useCallback(
    async (item: TemporalPlanningTrayItem) => {
      setPlacementError(null);
      let start: PlainDateTime;
      let end: PlainDateTime;
      try {
        start = Temporal.PlainDateTime.from(`${placementDate}T${placementTime}`);
        end = start.add({ minutes: durationMinutes });
        if (
          !Number.isInteger(durationMinutes) ||
          durationMinutes <= 0 ||
          !start.toPlainDate().equals(end.toPlainDate())
        ) {
          throw new RangeError('cross-day-or-empty');
        }
        if (placementTimeMode === 'zoned') {
          start.toZonedDateTime(placementTimeZone.trim(), { disambiguation: 'reject' });
          end.toZonedDateTime(placementTimeZone.trim(), { disambiguation: 'reject' });
        }
      } catch {
        setPlacementError(copy.invalidPlacement);
        return;
      }

      const placement =
        placementTimeMode === 'zoned'
          ? Object.freeze({
              kind: 'named-zone-local-interval' as const,
              startsLocalAt: start,
              endsLocalAt: end,
              zoneId: placementTimeZone.trim(),
              disambiguation: 'reject' as const,
            })
          : Object.freeze({
              kind: 'floating-local-interval' as const,
              startsLocalAt: start,
              endsLocalAt: end,
            });

      setPlacementPending(true);
      try {
        await source.placeItem({
          kind: item.kind,
          subjectRef: item.subjectRef,
          operationId: operationId(item),
          placement,
        });
        await refresh();
        setPlacingKey(null);
      } catch {
        setPlacementError(copy.placementFailed);
      } finally {
        setPlacementPending(false);
      }
    },
    [
      copy.invalidPlacement,
      copy.placementFailed,
      durationMinutes,
      placementDate,
      placementTime,
      placementTimeMode,
      placementTimeZone,
      refresh,
      source,
    ],
  );

  const trigger = (
    <button
      ref={triggerRef}
      className={`timeline-planning-trigger${open ? ' is-active' : ''}`}
      type="button"
      aria-label={copy.trigger}
      aria-controls={PANEL_ID}
      aria-expanded={open}
      onClick={() => {
        const next = !open;
        if (next) {
          onBeforeOpen?.();
          void refresh();
        }
        setOpen(next);
        if (!next) setQuery('');
      }}
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 6.5h16v11H4z" />
        <path d="M8 10h8M8 14h5" />
        <path d="M16.5 3.5v5M14 6h5" />
      </svg>
      {remoteItems.length > 0 ? (
        <span className="timeline-planning-trigger__badge" aria-hidden="true">
          {remoteItems.length > 99 ? '99+' : remoteItems.length}
        </span>
      ) : null}
    </button>
  );

  const panel = open ? (
    <aside
      ref={panelRef}
      id={PANEL_ID}
      className="timeline-planning-tray"
      aria-label={copy.title}
      data-timeline-planning-tray="true"
      data-timeline-planning-read-state={readState}
      style={panelStyle}
    >
      <header className="timeline-planning-tray__header">
        <div>
          <span className="timeline-planning-tray__kicker">DANTE · Timeline</span>
          <h2>{copy.title}</h2>
          <p>{copy.description}</p>
        </div>
        <button
          className="timeline-planning-tray__close"
          type="button"
          aria-label={copy.close}
          onClick={() => {
            setOpen(false);
            setQuery('');
            requestAnimationFrame(() => triggerRef.current?.focus());
          }}
        >
          ×
        </button>
      </header>

      {remoteItems.length > 0 ? (
        <label className="timeline-planning-tray__search">
          <span className="home-visually-hidden">{copy.search}</span>
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="6" />
            <path d="m16 16 4 4" />
          </svg>
          <input
            ref={searchRef}
            type="search"
            value={query}
            placeholder={copy.searchPlaceholder}
            onChange={(event) => setQuery(event.target.value)}
          />
          <span>{filteredItems.length}</span>
        </label>
      ) : null}

      <div className="timeline-planning-tray__body">
        {readState === 'error' ? (
          <div className="timeline-planning-empty is-search" role="alert">
            <strong>{copy.failed}</strong>
            <button type="button" onClick={() => void refresh()}>{copy.retry}</button>
          </div>
        ) : readState === 'loading' && remoteItems.length === 0 ? (
          <div className="timeline-planning-empty"><strong>{copy.loading}</strong></div>
        ) : remoteItems.length === 0 ? (
          <div className="timeline-planning-empty">
            <span aria-hidden="true">✓</span>
            <strong>{copy.emptyTitle}</strong>
            <p>{copy.emptyBody}</p>
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="timeline-planning-empty is-search"><strong>{copy.emptyTitle}</strong></div>
        ) : (
          filteredItems.map((item) => {
            const key = itemKey(item);
            const placing = placingKey === key;
            const typeLabel = item.kind === 'activity' ? copy.activity : copy.event;
            const stateLabel = item.state === 'postponed' ? copy.postponed : typeLabel;
            return (
              <article
                key={key}
                className="timeline-planning-card timeline-planning-card--session"
                data-timeline-planning-item={key}
                data-temporal-subject-kind={item.kind}
                data-temporal-subject-ref={item.subjectRef}
                data-temporal-planning-state={item.state}
                data-timeline-tone="personal"
              >
                <div className="timeline-planning-card__main">
                  {item.kind === 'activity' ? (
                    <button
                      className="timeline-planning-card__copy"
                      type="button"
                      aria-label={`Apri Plan per ${item.title}`}
                      onClick={() => {
                        setOpen(false);
                        setQuery('');
                        openPlanForActivity({
                          activityRef: item.subjectRef,
                          title: item.title,
                        });
                      }}
                    >
                      <strong>{item.title}</strong>
                      <span className="timeline-planning-card__policy">{stateLabel}</span>
                    </button>
                  ) : (
                    <div className="timeline-planning-card__copy">
                      <strong>{item.title}</strong>
                      <span className="timeline-planning-card__policy">{stateLabel}</span>
                    </div>
                  )}
                  <span className="timeline-planning-card__actions">
                    <button
                      type="button"
                      aria-label={`${copy.place}: ${item.title}`}
                      aria-expanded={placing}
                      onClick={() => {
                        setPlacingKey(placing ? null : key);
                        setPlacementError(null);
                      }}
                    >
                      {copy.place}
                    </button>
                  </span>
                </div>

                {item.kind === 'activity' ? (
                  <SessionSubjectControls
                    kind="activity"
                    subjectRef={item.subjectRef}
                    label={item.title}
                  />
                ) : null}

                {placing ? (
                  <form
                    className="timeline-planning-quick-place"
                    onSubmit={(event) => {
                      event.preventDefault();
                      void submitPlacement(item);
                    }}
                  >
                    <div className="timeline-planning-quick-place__heading">
                      <strong>{copy.placementTitle}</strong>
                      <span>{stateLabel}</span>
                    </div>
                    <label>
                      <span>{copy.date}</span>
                      <input
                        type="date"
                        value={placementDate}
                        disabled={placementPending}
                        onChange={(event) => setPlacementDate(event.target.value)}
                      />
                    </label>
                    <label>
                      <span>{copy.time}</span>
                      <input
                        type="time"
                        value={placementTime}
                        disabled={placementPending}
                        onChange={(event) => setPlacementTime(event.target.value)}
                      />
                    </label>
                    <label>
                      <span>{copy.duration}</span>
                      <input
                        type="number"
                        min={1}
                        max={1440}
                        step={1}
                        value={durationMinutes}
                        disabled={placementPending}
                        onChange={(event) => setDurationMinutes(Number(event.target.value))}
                      />
                    </label>
                    <label>
                      <span>{copy.timeReference}</span>
                      <select
                        value={placementTimeMode}
                        disabled={placementPending}
                        onChange={(event) =>
                          setPlacementTimeMode(event.target.value as 'floating' | 'zoned')
                        }
                      >
                        <option value="floating">{copy.localTime}</option>
                        <option value="zoned">{copy.namedZoneTime}</option>
                      </select>
                    </label>
                    {placementTimeMode === 'zoned' ? (
                      <label>
                        <span>{copy.timeZone}</span>
                        <input
                          type="text"
                          value={placementTimeZone}
                          disabled={placementPending}
                          onChange={(event) => setPlacementTimeZone(event.target.value)}
                          placeholder="Europe/Rome"
                        />
                      </label>
                    ) : null}
                    {placementError ? <p role="alert">{placementError}</p> : null}
                    <div className="timeline-planning-quick-place__actions">
                      <button
                        type="button"
                        disabled={placementPending}
                        onClick={() => {
                          setPlacingKey(null);
                          setPlacementError(null);
                        }}
                      >
                        {copy.cancel}
                      </button>
                      <button type="submit" disabled={placementPending}>
                        {placementPending ? copy.placing : copy.confirm}
                      </button>
                    </div>
                  </form>
                ) : null}
              </article>
            );
          })
        )}
      </div>
    </aside>
  ) : null;

  return (
    <>
      {!hiddenTrigger && actionsHost ? createPortal(trigger, actionsHost) : null}
      {typeof document !== 'undefined' && panel
        ? createPortal(panel, document.body)
        : null}
    </>
  );
}
