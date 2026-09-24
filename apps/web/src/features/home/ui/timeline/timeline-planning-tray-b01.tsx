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

import { SessionSubjectControls } from '../../../temporal/session-subject-controls';
import {
  subscribeTemporalPlanningInvalidation,
  subscribeTemporalTimelineInvalidation,
} from '../../../temporal/timeline-invalidation';
import type { TemporalCreateRuntime } from '../../../temporal-create';
import { timelinePlanningCopy } from './timeline-planning-copy';

import './timeline-planning-tray.css';

type TimelineB01PlanningTrayProps = Readonly<{
  runtime: TemporalCreateRuntime;
  defaultDate: PlainDate;
  onBeforeOpen?: (() => void) | undefined;
}>;

type CanonicalPlanningActivity = Readonly<{
  projectionId: string;
  activityRef: string;
  title: string;
}>;

type ReadState = 'loading' | 'ready' | 'error';

const PANEL_ID = 'timeline-planning-tray-b01';
const PANEL_GAP_PX = 8;
const PANEL_VIEWPORT_PADDING_PX = 12;
const PANEL_DESKTOP_WIDTH_PX = 370;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function readCopy(language: string) {
  const english = language.toLowerCase().startsWith('en');
  return english
    ? Object.freeze({
        description:
          'Activities that exist but do not have an accepted Schedule.',
        loading: 'Loading activities…',
        failed: 'Activities to place are unavailable.',
        retry: 'Retry',
        activity: 'Activity',
        place: 'Place',
        placementTitle: 'Accepted Schedule',
        date: 'Date',
        time: 'Start',
        duration: 'Duration (minutes)',
        cancel: 'Cancel',
        confirm: 'Place in Timeline',
        placing: 'Placing…',
        invalidPlacement: 'Choose a valid same-day interval.',
        placementFailed:
          'The Schedule was not accepted. The Activity is still here.',
      })
    : Object.freeze({
        description: 'Attività già esistenti, ma senza uno Schedule accettato.',
        loading: 'Caricamento attività…',
        failed: 'Le attività da collocare non sono disponibili.',
        retry: 'Riprova',
        activity: 'Activity',
        place: 'Colloca',
        placementTitle: 'Schedule accettato',
        date: 'Data',
        time: 'Inizio',
        duration: 'Durata (minuti)',
        cancel: 'Annulla',
        confirm: 'Colloca in Timeline',
        placing: 'Collocazione…',
        invalidPlacement: 'Scegli un intervallo valido nella stessa giornata.',
        placementFailed:
          'Lo Schedule non è stato accettato. L’Activity resta qui.',
      });
}

function canonicalActivities(
  projections: Awaited<ReturnType<TemporalCreateRuntime['list']>>,
): readonly CanonicalPlanningActivity[] {
  const byProjectionId = new Map<string, CanonicalPlanningActivity>();
  for (const projection of projections) {
    if (
      projection.subject.source !== 'native' ||
      projection.subject.kind !== 'activity' ||
      projection.placement !== null
    ) {
      continue;
    }
    byProjectionId.set(
      projection.id,
      Object.freeze({
        projectionId: projection.id,
        activityRef: projection.subject.id,
        title: projection.title,
      }),
    );
  }
  return Object.freeze([...byProjectionId.values()]);
}

export function TimelinePlanningTrayB01({
  items: _items,
  runtime,
  defaultDate,
  onBeforeOpen,
}: TimelineB01PlanningTrayProps) {
  const { i18n } = useTranslation('common');
  const language = i18n.resolvedLanguage ?? i18n.language;
  const copy = timelinePlanningCopy(language);
  const b01Copy = readCopy(language);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const panelRef = useRef<HTMLElement | null>(null);
  const searchRef = useRef<HTMLInputElement | null>(null);
  const readGenerationRef = useRef(0);
  const [actionsHost, setActionsHost] = useState<HTMLElement | null>(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [readState, setReadState] = useState<ReadState>('loading');
  const [placingActivityRef, setPlacingActivityRef] = useState<string | null>(
    null,
  );
  const [placementDate, setPlacementDate] = useState(defaultDate.toString());
  const [placementTime, setPlacementTime] = useState('09:00');
  const [durationMinutes, setDurationMinutes] = useState(30);
  const [placementPending, setPlacementPending] = useState(false);
  const [placementError, setPlacementError] = useState<string | null>(null);
  const [remoteItems, setRemoteItems] = useState<
    readonly CanonicalPlanningActivity[]
  >([]);
  const [panelStyle, setPanelStyle] = useState<CSSProperties | undefined>();

  const mergedItems = remoteItems;

  const filteredItems = useMemo(() => {
    const normalized = query.trim().toLocaleLowerCase();
    if (!normalized) {
      return mergedItems;
    }
    return mergedItems.filter((item) =>
      item.title.toLocaleLowerCase().includes(normalized),
    );
  }, [mergedItems, query]);

  const commitRead = useCallback(
    (
      generation: number,
      projections: Awaited<ReturnType<TemporalCreateRuntime['list']>>,
    ) => {
      if (readGenerationRef.current !== generation) {
        return;
      }
      setRemoteItems(canonicalActivities(projections));
      setReadState('ready');
    },
    [],
  );

  const failRead = useCallback((generation: number) => {
    if (readGenerationRef.current === generation) {
      setReadState('error');
    }
  }, []);

  const refresh = useCallback(async () => {
    const generation = ++readGenerationRef.current;
    setReadState('loading');
    try {
      commitRead(generation, await runtime.list());
    } catch {
      failRead(generation);
    }
  }, [commitRead, failRead, runtime]);

  useEffect(() => {
    const generation = ++readGenerationRef.current;
    void runtime
      .list()
      .then((projections) => commitRead(generation, projections))
      .catch(() => failRead(generation));
    return () => {
      if (readGenerationRef.current === generation) {
        readGenerationRef.current += 1;
      }
    };
  }, [commitRead, failRead, runtime]);

  useEffect(() => {
    const reload = () => {
      void refresh();
    };
    const unsubscribePlanning = subscribeTemporalPlanningInvalidation(reload);
    // A Schedule withdrawal changes both Timeline and the derived Activity tray.
    // Listen to the canonical Timeline read invalidation as well, so every governed
    // unschedule path refreshes the same remote Activity projection immediately.
    const unsubscribeTimeline = subscribeTemporalTimelineInvalidation(reload);
    return () => {
      unsubscribePlanning();
      unsubscribeTimeline();
    };
  }, [refresh]);

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      setActionsHost(
        document.querySelector<HTMLElement>('.dante-timeline-actions'),
      );
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
    if (!open) {
      return;
    }
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
    if (!open) {
      return;
    }
    const closeOutside = (event: globalThis.PointerEvent) => {
      if (!(event.target instanceof Node)) {
        return;
      }
      if (
        panelRef.current?.contains(event.target) ||
        triggerRef.current?.contains(event.target)
      ) {
        return;
      }
      setOpen(false);
      setQuery('');
    };
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') {
        return;
      }
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
    async (activityRef: string) => {
      setPlacementError(null);
      let start: PlainDateTime;
      let end: PlainDateTime;
      try {
        start = Temporal.PlainDateTime.from(
          `${placementDate}T${placementTime}`,
        );
        end = start.add({ minutes: durationMinutes });
        if (
          durationMinutes <= 0 ||
          !start.toPlainDate().equals(end.toPlainDate())
        ) {
          throw new RangeError('cross-day-or-empty');
        }
      } catch {
        setPlacementError(b01Copy.invalidPlacement);
        return;
      }

      setPlacementPending(true);
      try {
        const result = await runtime.placeExistingActivity(
          activityRef,
          Object.freeze({
            kind: 'floating-local' as const,
            start,
            end,
          }),
        );
        if (result.status !== 'applied') {
          setPlacementError(b01Copy.placementFailed);
          return;
        }
        await refresh();
        setPlacingActivityRef(null);
      } catch {
        setPlacementError(b01Copy.placementFailed);
      } finally {
        setPlacementPending(false);
      }
    },
    [
      b01Copy.invalidPlacement,
      b01Copy.placementFailed,
      durationMinutes,
      placementDate,
      placementTime,
      refresh,
      runtime,
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
        if (!next) {
          setQuery('');
        }
      }}
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 6.5h16v11H4z" />
        <path d="M8 10h8M8 14h5" />
        <path d="M16.5 3.5v5M14 6h5" />
      </svg>
      {mergedItems.length > 0 ? (
        <span className="timeline-planning-trigger__badge" aria-hidden="true">
          {mergedItems.length > 99 ? '99+' : mergedItems.length}
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
          <span className="timeline-planning-tray__kicker">
            DANTE · Timeline
          </span>
          <h2>{copy.title}</h2>
          <p>{b01Copy.description}</p>
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

      {mergedItems.length > 0 ? (
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
            <strong>{b01Copy.failed}</strong>
            <button type="button" onClick={() => void refresh()}>
              {b01Copy.retry}
            </button>
          </div>
        ) : readState === 'loading' && mergedItems.length === 0 ? (
          <div className="timeline-planning-empty">
            <strong>{b01Copy.loading}</strong>
          </div>
        ) : mergedItems.length === 0 ? (
          <div className="timeline-planning-empty">
            <span aria-hidden="true">✓</span>
            <strong>{copy.emptyTitle}</strong>
            <p>{copy.emptyBody}</p>
          </div>
        ) : filteredItems.length === 0 ? (
          <div className="timeline-planning-empty is-search">
            <strong>{copy.emptyTitle}</strong>
          </div>
        ) : (
          filteredItems.map((item) => {
            const placing = placingActivityRef === item.activityRef;
            return (
              <article
                key={item.projectionId}
                className="timeline-planning-card timeline-planning-card--session"
                data-timeline-planning-item={item.projectionId}
                data-temporal-activity-ref={item.activityRef}
                data-timeline-tone="personal"
              >
                <div className="timeline-planning-card__main">
                  <span className="timeline-planning-card__copy">
                    <strong>{item.title}</strong>
                    <span className="timeline-planning-card__policy">
                      {b01Copy.activity}
                    </span>
                  </span>
                  <span className="timeline-planning-card__actions">
                    <button
                      type="button"
                      aria-label={`${b01Copy.place}: ${item.title}`}
                      aria-expanded={placing}
                      onClick={() => {
                        setPlacingActivityRef(
                          placing ? null : item.activityRef,
                        );
                        setPlacementError(null);
                      }}
                    >
                      {b01Copy.place}
                    </button>
                  </span>
                </div>

                <SessionSubjectControls
                  kind="activity"
                  subjectRef={item.activityRef}
                  label={item.title}
                />

                {placing ? (
                  <form
                    className="timeline-planning-quick-place"
                    onSubmit={(event) => {
                      event.preventDefault();
                      void submitPlacement(item.activityRef);
                    }}
                  >
                    <div className="timeline-planning-quick-place__heading">
                      <strong>{b01Copy.placementTitle}</strong>
                      <span>{b01Copy.activity}</span>
                    </div>
                    <label>
                      <span>{b01Copy.date}</span>
                      <input
                        type="date"
                        value={placementDate}
                        disabled={placementPending}
                        onChange={(event) =>
                          setPlacementDate(event.target.value)
                        }
                      />
                    </label>
                    <label>
                      <span>{b01Copy.time}</span>
                      <input
                        type="time"
                        value={placementTime}
                        disabled={placementPending}
                        onChange={(event) =>
                          setPlacementTime(event.target.value)
                        }
                      />
                    </label>
                    <label>
                      <span>{b01Copy.duration}</span>
                      <input
                        type="number"
                        min={1}
                        max={1440}
                        step={1}
                        value={durationMinutes}
                        disabled={placementPending}
                        onChange={(event) =>
                          setDurationMinutes(Number(event.target.value))
                        }
                      />
                    </label>
                    {placementError ? (
                      <p role="alert">{placementError}</p>
                    ) : null}
                    <div className="timeline-planning-quick-place__actions">
                      <button
                        type="button"
                        disabled={placementPending}
                        onClick={() => {
                          setPlacingActivityRef(null);
                          setPlacementError(null);
                        }}
                      >
                        {b01Copy.cancel}
                      </button>
                      <button type="submit" disabled={placementPending}>
                        {placementPending ? b01Copy.placing : b01Copy.confirm}
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
      {actionsHost ? createPortal(trigger, actionsHost) : null}
      {typeof document !== 'undefined' && panel
        ? createPortal(panel, document.body)
        : null}
    </>
  );
}
