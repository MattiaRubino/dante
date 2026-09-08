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

import type { TemporalCreateRuntime } from '../../../temporal-create';
import { timelinePlanningCopy } from './timeline-planning-copy';
import type { TimelinePlanningTrayItem } from './timeline-planning-tray';

import './timeline-planning-tray.css';

type TimelineB01PlanningTrayProps = Readonly<{
  items: readonly TimelinePlanningTrayItem[];
  runtime: TemporalCreateRuntime;
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
        description: 'Activities that exist but do not have an accepted Schedule.',
        loading: 'Loading activities…',
        failed: 'Activities to place are unavailable.',
        retry: 'Retry',
        activity: 'Activity',
      })
    : Object.freeze({
        description: 'Attività già esistenti, ma senza uno Schedule accettato.',
        loading: 'Caricamento attività…',
        failed: 'Le attività da collocare non sono disponibili.',
        retry: 'Riprova',
        activity: 'Activity',
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
  items,
  runtime,
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
  const [remoteItems, setRemoteItems] = useState<
    readonly CanonicalPlanningActivity[]
  >([]);
  const [panelStyle, setPanelStyle] = useState<CSSProperties | undefined>();

  const mergedItems = useMemo(() => {
    const byProjectionId = new Map<string, CanonicalPlanningActivity>();
    for (const item of remoteItems) {
      byProjectionId.set(item.projectionId, item);
    }
    for (const item of items) {
      if (!byProjectionId.has(item.id)) {
        byProjectionId.set(
          item.id,
          Object.freeze({
            projectionId: item.id,
            activityRef: item.id,
            title: item.title,
          }),
        );
      }
    }
    return Object.freeze([...byProjectionId.values()]);
  }, [items, remoteItems]);

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
          filteredItems.map((item) => (
            <article
              key={item.projectionId}
              className="timeline-planning-card"
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
              </div>
            </article>
          ))
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
