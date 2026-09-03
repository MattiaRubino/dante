import type { PlainDate } from '@dante/time';
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
  type PointerEvent as ReactPointerEvent,
} from 'react';
import { createPortal } from 'react-dom';
import { useTranslation } from 'react-i18next';

import { TIMELINE_POLICY } from './model/timeline-policy';
import type { TimelineSemanticTone } from './model/timeline-types';
import { timelinePlanningCopy } from './timeline-planning-copy';

import './timeline-planning-tray.css';

export type TimelinePlanningConstraintKind =
  | 'none'
  | 'open'
  | 'bounded-window'
  | 'deadline'
  | 'preferred-window';

export type TimelinePlanningTrayItem = Readonly<{
  id: string;
  title: string;
  contextLabel: string;
  tone: TimelineSemanticTone;
  groupIndex: number;
  durationMinutes: number;
  constraintKind: TimelinePlanningConstraintKind;
  splittable: boolean;
  notes: string;
}>;

type TimelinePlanningTrayProps = Readonly<{
  items: readonly TimelinePlanningTrayItem[];
  defaultDate: PlainDate;
  onBeforeOpen?: (() => void) | undefined;
  onPlace: (
    itemId: string,
    dateKey: string,
    startMinute: number,
  ) => Promise<boolean>;
  onDelete: (itemId: string) => Promise<boolean>;
}>;

type DragState = Readonly<{
  pointerId: number;
  itemId: string;
  startX: number;
  startY: number;
  offsetX: number;
  offsetY: number;
  width: number;
  active: boolean;
}>;

type DragVisual = Readonly<{
  item: TimelinePlanningTrayItem;
  left: number;
  top: number;
  width: number;
}>;

type DropCandidate = Readonly<{
  itemId: string;
  dateKey: string;
  startMinute: number;
  endMinute: number;
  host: HTMLElement;
  style: CSSProperties;
  tone: TimelineSemanticTone;
}>;

const PANEL_ID = 'timeline-planning-tray';
const DRAG_THRESHOLD_PX = 7;
const EDGE_SCROLL_ZONE_PX = 72;
const EDGE_SCROLL_STEP_PX = 28;
const PANEL_GAP_PX = 8;
const PANEL_VIEWPORT_PADDING_PX = 12;
const PANEL_DESKTOP_WIDTH_PX = 370;

function clamp(value: number, min: number, max: number): number {
  return Math.max(min, Math.min(max, value));
}

function parsePixel(value: string): number {
  const parsed = Number.parseFloat(value);
  return Number.isFinite(parsed) ? parsed : 0;
}

function minuteAtClientY(section: HTMLElement, clientY: number): number {
  const rect = section.getBoundingClientRect();
  const localY = clientY - rect.top;
  const lines = Array.from(
    section.querySelectorAll<HTMLElement>('.timeline-hour-line'),
  );
  const interval = TIMELINE_POLICY.grid.minorLineIntervalMinutes;
  if (lines.length < 2) {
    return Math.max(
      0,
      Math.min(1439, (localY / Math.max(1, rect.height)) * 1440),
    );
  }

  for (let index = 0; index < lines.length - 1; index += 1) {
    const current = parsePixel(lines[index]?.style.top ?? '0');
    const next = parsePixel(lines[index + 1]?.style.top ?? String(current));
    if (localY <= next) {
      const progress =
        next <= current ? 0 : (localY - current) / (next - current);
      return Math.max(
        0,
        Math.min(
          1439,
          (index + Math.max(0, Math.min(1, progress))) * interval,
        ),
      );
    }
  }

  return 1439;
}

function createMinutePixelMapper(
  section: HTMLElement,
): (minute: number) => number {
  const interval = TIMELINE_POLICY.grid.minorLineIntervalMinutes;
  const lineTops = Array.from(
    section.querySelectorAll<HTMLElement>('.timeline-hour-line'),
    (line) => parsePixel(line.style.top),
  );

  if (lineTops.length < 2) {
    const sectionHeight = section.clientHeight;
    return (minute) =>
      (Math.max(0, Math.min(1440, minute)) / 1440) * sectionHeight;
  }

  return (minute) => {
    const normalized = Math.max(0, Math.min(1440, minute)) / interval;
    const lowerIndex = Math.min(lineTops.length - 1, Math.floor(normalized));
    const upperIndex = Math.min(lineTops.length - 1, lowerIndex + 1);
    const lower = lineTops[lowerIndex] ?? 0;
    const upper = lineTops[upperIndex] ?? lower;
    return lower + (upper - lower) * (normalized - lowerIndex);
  };
}

function snapMinute(minute: number): number {
  return Math.max(0, Math.min(1425, Math.round(minute / 15) * 15));
}

function formatMinute(minute: number): string {
  return `${String(Math.floor(minute / 60)).padStart(2, '0')}:${String(
    minute % 60,
  ).padStart(2, '0')}`;
}

function parseTimeInput(value: string): number | null {
  const match = /^(\d{2}):(\d{2})$/.exec(value);
  if (!match) {
    return null;
  }
  const hour = Number(match[1]);
  const minute = Number(match[2]);
  if (hour < 0 || hour > 23 || minute < 0 || minute > 59) {
    return null;
  }
  return hour * 60 + minute;
}

function constraintLabel(
  copy: ReturnType<typeof timelinePlanningCopy>,
  kind: TimelinePlanningConstraintKind,
): string {
  switch (kind) {
    case 'open':
      return copy.constraint.open;
    case 'bounded-window':
      return copy.constraint.boundedWindow;
    case 'deadline':
      return copy.constraint.deadline;
    case 'preferred-window':
      return copy.constraint.preferredWindow;
    case 'none':
      return copy.constraint.none;
  }
}

function suggestedStartMinute(dateKey: string): number {
  const section = document.querySelector<HTMLElement>(
    `.timeline-day-section[data-timeline-date="${CSS.escape(dateKey)}"]`,
  );
  const grid = document.querySelector<HTMLElement>('.timeline-grid');
  if (!section || !grid) {
    return 9 * 60;
  }
  const sectionRect = section.getBoundingClientRect();
  const gridRect = grid.getBoundingClientRect();
  const visibleTop = Math.max(sectionRect.top, gridRect.top);
  const visibleBottom = Math.min(sectionRect.bottom, gridRect.bottom);
  if (visibleBottom - visibleTop <= 80) {
    return 9 * 60;
  }
  return snapMinute(
    minuteAtClientY(
      section,
      visibleTop + (visibleBottom - visibleTop) * 0.38,
    ),
  );
}

function setTimelinePlanningMode(active: boolean): void {
  const root = document.querySelector<HTMLElement>(
    '.home-timeline--production',
  );
  if (active) {
    document.documentElement.setAttribute('data-timeline-planning-mode', 'true');
    root?.setAttribute('data-timeline-planning-mode', 'true');
    return;
  }
  document.documentElement.removeAttribute('data-timeline-planning-mode');
  root?.removeAttribute('data-timeline-planning-mode');
}

export function TimelinePlanningTray({
  items,
  defaultDate,
  onBeforeOpen,
  onPlace,
  onDelete,
}: TimelinePlanningTrayProps) {
  const { i18n } = useTranslation('common');
  const copy = timelinePlanningCopy(i18n.resolvedLanguage ?? i18n.language);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const panelRef = useRef<HTMLElement | null>(null);
  const searchRef = useRef<HTMLInputElement | null>(null);
  const dragRef = useRef<DragState | null>(null);
  const [actionsHost, setActionsHost] = useState<HTMLElement | null>(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [quickItemId, setQuickItemId] = useState<string | null>(null);
  const [quickDate, setQuickDate] = useState(defaultDate.toString());
  const [quickTime, setQuickTime] = useState('09:00');
  const [deleteItemId, setDeleteItemId] = useState<string | null>(null);
  const [busyItemId, setBusyItemId] = useState<string | null>(null);
  const [errorItemId, setErrorItemId] = useState<string | null>(null);
  const [candidate, setCandidate] = useState<DropCandidate | null>(null);
  const [dragVisual, setDragVisual] = useState<DragVisual | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const [panelStyle, setPanelStyle] = useState<CSSProperties | undefined>();

  const filteredItems = useMemo(() => {
    const normalized = query.trim().toLocaleLowerCase();
    if (!normalized) {
      return items;
    }
    return items.filter((item) =>
      `${item.title} ${item.contextLabel} ${item.notes}`
        .toLocaleLowerCase()
        .includes(normalized),
    );
  }, [items, query]);

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
    if (!trigger || window.matchMedia('(max-width: 900px)').matches) {
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
    const top = Math.max(
      PANEL_VIEWPORT_PADDING_PX,
      rect.bottom + PANEL_GAP_PX,
    );
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
    const refresh = () => positionPanel();
    window.addEventListener('resize', refresh);
    document.addEventListener('scroll', refresh, true);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener('resize', refresh);
      document.removeEventListener('scroll', refresh, true);
    };
  }, [open, positionPanel]);

  useEffect(() => {
    if (!open || dragActive) {
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
      setQuickItemId(null);
      setDeleteItemId(null);
      setErrorItemId(null);
    };
    document.addEventListener('pointerdown', closeOutside, true);
    return () => document.removeEventListener('pointerdown', closeOutside, true);
  }, [dragActive, open]);

  const clearDrag = useCallback(() => {
    dragRef.current = null;
    setCandidate(null);
    setDragVisual(null);
    setDragActive(false);
    setTimelinePlanningMode(false);
  }, []);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') {
        return;
      }
      if (dragRef.current?.active) {
        clearDrag();
        event.preventDefault();
        return;
      }
      if (quickItemId) {
        setQuickItemId(null);
        setErrorItemId(null);
        event.preventDefault();
        return;
      }
      if (deleteItemId) {
        setDeleteItemId(null);
        event.preventDefault();
        return;
      }
      if (open) {
        setOpen(false);
        requestAnimationFrame(() => triggerRef.current?.focus());
        event.preventDefault();
      }
    };
    document.addEventListener('keydown', onKeyDown, true);
    return () => {
      document.removeEventListener('keydown', onKeyDown, true);
      dragRef.current = null;
      setTimelinePlanningMode(false);
    };
  }, [clearDrag, deleteItemId, open, quickItemId]);

  const dropCandidateAt = (
    item: TimelinePlanningTrayItem,
    clientX: number,
    clientY: number,
  ): DropCandidate | null => {
    const target = document.elementFromPoint(clientX, clientY);
    const section = target?.closest<HTMLElement>(
      '.timeline-day-section[data-timeline-date]',
    );
    const dateKey = section?.dataset.timelineDate;
    const eventsHost = section?.querySelector<HTMLElement>(
      '.timeline-events-layer',
    );
    if (!section || !dateKey || !eventsHost) {
      return null;
    }

    const duration = Math.max(15, Math.min(1440, item.durationMinutes));
    const rawStart = snapMinute(minuteAtClientY(section, clientY));
    const startMinute = Math.max(0, Math.min(1440 - duration, rawStart));
    const endMinute = startMinute + duration;
    const pixelAtMinute = createMinutePixelMapper(section);
    const top = pixelAtMinute(startMinute);
    const bottom = pixelAtMinute(endMinute);
    const root = document.querySelector<HTMLElement>('.home-timeline--production');
    const rootStyle = root ? getComputedStyle(root) : null;
    const expansionProgress =
      Number.parseFloat(
        rootStyle?.getPropertyValue('--timeline-expansion-progress') ?? '0',
      ) || 0;
    const groupWidth =
      Number.parseFloat(
        rootStyle?.getPropertyValue('--timeline-expanded-group-width') ?? '260',
      ) || 260;
    const compactLeft = 14;
    const compactWidth = Math.min(
      300,
      Math.max(180, eventsHost.clientWidth * 0.34),
    );
    const expandedLeft = item.groupIndex * groupWidth + 6;
    const expandedWidth = Math.max(150, groupWidth - 12);

    return Object.freeze({
      itemId: item.id,
      dateKey,
      startMinute,
      endMinute,
      host: eventsHost,
      tone: item.tone,
      style: Object.freeze({
        top,
        left: compactLeft + (expandedLeft - compactLeft) * expansionProgress,
        width:
          compactWidth + (expandedWidth - compactWidth) * expansionProgress,
        height: Math.max(38, bottom - top),
      }),
    });
  };

  const autoScrollTimeline = (clientY: number) => {
    const grid = document.querySelector<HTMLElement>('.timeline-grid');
    if (!grid) {
      return;
    }
    const rect = grid.getBoundingClientRect();
    if (clientY < rect.top + EDGE_SCROLL_ZONE_PX && clientY >= rect.top) {
      grid.scrollTop = Math.max(0, grid.scrollTop - EDGE_SCROLL_STEP_PX);
    } else if (
      clientY > rect.bottom - EDGE_SCROLL_ZONE_PX &&
      clientY <= rect.bottom
    ) {
      grid.scrollTop += EDGE_SCROLL_STEP_PX;
    }
  };

  const beginPointer = (
    event: ReactPointerEvent<HTMLButtonElement>,
    item: TimelinePlanningTrayItem,
  ) => {
    if (event.button !== 0 || !event.isPrimary || busyItemId) {
      return;
    }
    const card = event.currentTarget.closest<HTMLElement>(
      '[data-timeline-planning-item]',
    );
    const rect = card?.getBoundingClientRect() ?? event.currentTarget.getBoundingClientRect();
    dragRef.current = {
      pointerId: event.pointerId,
      itemId: item.id,
      startX: event.clientX,
      startY: event.clientY,
      offsetX: event.clientX - rect.left,
      offsetY: event.clientY - rect.top,
      width: rect.width,
      active: false,
    };
    event.currentTarget.setPointerCapture(event.pointerId);
  };

  const movePointer = (
    event: ReactPointerEvent<HTMLButtonElement>,
    item: TimelinePlanningTrayItem,
  ) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== event.pointerId || drag.itemId !== item.id) {
      return;
    }
    const distance = Math.hypot(
      event.clientX - drag.startX,
      event.clientY - drag.startY,
    );
    if (!drag.active && distance >= DRAG_THRESHOLD_PX) {
      const activeDrag = { ...drag, active: true };
      dragRef.current = activeDrag;
      setDragActive(true);
      setDeleteItemId(null);
      setQuickItemId(null);
      setTimelinePlanningMode(true);
    }
    const activeDrag = dragRef.current;
    if (!activeDrag?.active) {
      return;
    }
    autoScrollTimeline(event.clientY);
    setDragVisual(
      Object.freeze({
        item,
        left: event.clientX - activeDrag.offsetX,
        top: event.clientY - activeDrag.offsetY,
        width: activeDrag.width,
      }),
    );
    setCandidate(dropCandidateAt(item, event.clientX, event.clientY));
    event.preventDefault();
  };

  const finishPointer = async (
    event: ReactPointerEvent<HTMLButtonElement>,
    item: TimelinePlanningTrayItem,
  ) => {
    const drag = dragRef.current;
    if (!drag || drag.pointerId !== event.pointerId || drag.itemId !== item.id) {
      return;
    }
    const target = candidate?.itemId === item.id ? candidate : null;
    const wasActive = drag.active;
    clearDrag();
    if (!wasActive || !target) {
      return;
    }
    setBusyItemId(item.id);
    setErrorItemId(null);
    const placed = await onPlace(item.id, target.dateKey, target.startMinute);
    setBusyItemId(null);
    if (placed) {
      setOpen(false);
      setQuery('');
    } else {
      setErrorItemId(item.id);
    }
  };

  const openQuickPlacement = (item: TimelinePlanningTrayItem) => {
    const dateKey = defaultDate.toString();
    setQuickItemId(item.id);
    setQuickDate(dateKey);
    setQuickTime(formatMinute(suggestedStartMinute(dateKey)));
    setDeleteItemId(null);
    setErrorItemId(null);
  };

  const submitQuickPlacement = async (item: TimelinePlanningTrayItem) => {
    const minute = parseTimeInput(quickTime);
    if (minute === null || !quickDate) {
      setErrorItemId(item.id);
      return;
    }
    setBusyItemId(item.id);
    setErrorItemId(null);
    const placed = await onPlace(item.id, quickDate, snapMinute(minute));
    setBusyItemId(null);
    if (placed) {
      setQuickItemId(null);
      setOpen(false);
      setQuery('');
    } else {
      setErrorItemId(item.id);
    }
  };

  const confirmDelete = async (item: TimelinePlanningTrayItem) => {
    setBusyItemId(item.id);
    setErrorItemId(null);
    const removed = await onDelete(item.id);
    setBusyItemId(null);
    if (removed) {
      setDeleteItemId(null);
      setQuickItemId(null);
    } else {
      setErrorItemId(item.id);
    }
  };

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
        }
        setOpen(next);
        setErrorItemId(null);
        if (!next) {
          setQuery('');
          setQuickItemId(null);
          setDeleteItemId(null);
        }
      }}
    >
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M4 6.5h16v11H4z" />
        <path d="M8 10h8M8 14h5" />
        <path d="M16.5 3.5v5M14 6h5" />
      </svg>
      {items.length > 0 ? (
        <span className="timeline-planning-trigger__badge" aria-hidden="true">
          {items.length > 99 ? '99+' : items.length}
        </span>
      ) : null}
    </button>
  );

  const panel = open ? (
    <aside
      ref={panelRef}
      id={PANEL_ID}
      className={`timeline-planning-tray${dragActive ? ' is-dragging' : ''}`}
      aria-label={copy.title}
      data-timeline-planning-tray="true"
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

      {items.length > 0 ? (
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
        {items.length === 0 ? (
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
            const quickOpen = quickItemId === item.id;
            const deleting = deleteItemId === item.id;
            const busy = busyItemId === item.id;
            const failed = errorItemId === item.id;
            const dragging = dragVisual?.item.id === item.id;
            return (
              <article
                key={item.id}
                className={`timeline-planning-card${busy ? ' is-busy' : ''}${
                  dragging ? ' is-drag-source' : ''
                }`}
                data-timeline-planning-item={item.id}
                data-timeline-tone={item.tone}
              >
                <button
                  className="timeline-planning-card__main"
                  type="button"
                  disabled={busy}
                  aria-label={`${item.title} · ${copy.dragHint}`}
                  onPointerDown={(event) => beginPointer(event, item)}
                  onPointerMove={(event) => movePointer(event, item)}
                  onPointerUp={(event) => void finishPointer(event, item)}
                  onPointerCancel={clearDrag}
                  onDoubleClick={() => openQuickPlacement(item)}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter') {
                      event.preventDefault();
                      openQuickPlacement(item);
                    }
                  }}
                >
                  <span className="timeline-planning-card__grip" aria-hidden="true">
                    ⠿
                  </span>
                  <span className="timeline-planning-card__copy">
                    <strong>{item.title}</strong>
                    <span className="timeline-planning-card__meta">
                      <i aria-hidden="true" />
                      {item.contextLabel}
                      <b>·</b>
                      {item.durationMinutes} min
                    </span>
                    <span className="timeline-planning-card__policy">
                      {constraintLabel(copy, item.constraintKind)}
                      {item.splittable ? ` · ${copy.splittable}` : ''}
                    </span>
                  </span>
                </button>

                <div className="timeline-planning-card__actions">
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => openQuickPlacement(item)}
                  >
                    {copy.place}
                  </button>
                  <button
                    className="timeline-planning-card__remove"
                    type="button"
                    disabled={busy}
                    onClick={() => {
                      setDeleteItemId(item.id);
                      setQuickItemId(null);
                      setErrorItemId(null);
                    }}
                    aria-label={`${copy.remove}: ${item.title}`}
                    title={copy.remove}
                  >
                    ×
                  </button>
                </div>

                {quickOpen ? (
                  <form
                    className="timeline-planning-quick-place"
                    onSubmit={(event) => {
                      event.preventDefault();
                      void submitQuickPlacement(item);
                    }}
                  >
                    <div className="timeline-planning-quick-place__heading">
                      <strong>{copy.placeTitle}</strong>
                      <span>{item.durationMinutes} min</span>
                    </div>
                    <label>
                      <span>{copy.date}</span>
                      <input
                        type="date"
                        value={quickDate}
                        onChange={(event) => setQuickDate(event.target.value)}
                      />
                    </label>
                    <label>
                      <span>{copy.time}</span>
                      <input
                        type="time"
                        step={900}
                        value={quickTime}
                        onChange={(event) => setQuickTime(event.target.value)}
                      />
                    </label>
                    <div className="timeline-planning-quick-place__actions">
                      <button type="button" onClick={() => setQuickItemId(null)}>
                        {copy.cancel}
                      </button>
                      <button type="submit" disabled={busy}>
                        {busy ? copy.placing : copy.confirmPlace}
                      </button>
                    </div>
                  </form>
                ) : null}

                {deleting ? (
                  <div className="timeline-planning-delete" role="alertdialog">
                    <strong>{copy.removeTitle}</strong>
                    <p>{copy.removeBody}</p>
                    <div>
                      <button type="button" onClick={() => setDeleteItemId(null)}>
                        {copy.cancel}
                      </button>
                      <button
                        type="button"
                        disabled={busy}
                        onClick={() => void confirmDelete(item)}
                      >
                        {copy.remove}
                      </button>
                    </div>
                  </div>
                ) : null}

                {failed ? (
                  <p className="timeline-planning-card__error" role="alert">
                    {copy.failed}
                  </p>
                ) : null}
              </article>
            );
          })
        )}
      </div>

      {items.length > 0 ? (
        <footer className="timeline-planning-tray__footer">
          <span aria-hidden="true">↕</span>
          <p>{copy.dragHint}</p>
        </footer>
      ) : null}
    </aside>
  ) : null;

  return (
    <>
      {actionsHost ? createPortal(trigger, actionsHost) : null}
      {typeof document !== 'undefined' && panel
        ? createPortal(panel, document.body)
        : null}
      {dragActive && typeof document !== 'undefined'
        ? createPortal(
            <div className="timeline-planning-scrim" aria-hidden="true" />,
            document.body,
          )
        : null}
      {dragVisual && typeof document !== 'undefined'
        ? createPortal(
            <div
              className="timeline-planning-drag-card"
              data-timeline-planning-drag-card="true"
              data-timeline-tone={dragVisual.item.tone}
              style={{
                left: dragVisual.left,
                top: dragVisual.top,
                width: dragVisual.width,
              }}
              aria-hidden="true"
            >
              <span className="timeline-planning-card__grip">⠿</span>
              <span className="timeline-planning-card__copy">
                <strong>{dragVisual.item.title}</strong>
                <span className="timeline-planning-card__meta">
                  <i />
                  {dragVisual.item.contextLabel}
                  <b>·</b>
                  {dragVisual.item.durationMinutes} min
                </span>
              </span>
            </div>,
            document.body,
          )
        : null}
      {candidate
        ? createPortal(
            <div
              className="timeline-planning-drop-preview"
              data-timeline-planning-drop-preview="true"
              data-timeline-tone={candidate.tone}
              style={candidate.style}
              aria-hidden="true"
            >
              <strong>{copy.dropHere}</strong>
              <span>
                {formatMinute(candidate.startMinute)}–
                {formatMinute(candidate.endMinute)}
              </span>
            </div>,
            candidate.host,
          )
        : null}
    </>
  );
}
