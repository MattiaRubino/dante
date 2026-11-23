import { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import {
  createRemoteDraftVault,
  DRAFT_VAULT_UPDATED,
  type DraftVaultItem,
} from '../../../temporal-create/application/remote-draft-vault';
import { TemporalKindMarker } from '../../../temporal-create/ui/temporal-kind-marker';
import { subscribeTemporalPlanningInvalidation } from '../../../temporal/timeline-invalidation';

import './timeline-planning-tray.css';

const draftDateFormatter = new Intl.DateTimeFormat('it-IT', {
  day: 'numeric',
  month: 'short',
  timeZone: 'UTC',
});

function draftDateLabel(value: string): string | null {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return null;
  const date = new Date(`${value}T12:00:00Z`);
  return Number.isNaN(date.getTime()) ? null : draftDateFormatter.format(date);
}

function draftScheduleLabel(item: DraftVaultItem): string {
  const fields = item.payload.fields;
  if (fields.timeSemantics === 'unscheduled') return 'Senza orario';
  const date = draftDateLabel(fields.date);
  if (!date) return 'Data da definire';

  if (fields.timeSemantics === 'all-day') {
    const end =
      item.subjectKind === 'event'
        ? draftDateLabel(fields.event.allDayEndDate)
        : null;
    return end && end !== date
      ? `Tutto il giorno · ${date}–${end}`
      : `Tutto il giorno · ${date}`;
  }
  if (fields.timeSemantics === 'coarse') {
    const period = {
      morning: 'Mattina',
      afternoon: 'Pomeriggio',
      evening: 'Sera',
    }[fields.coarsePeriod];
    return `${period ?? 'Periodo indicativo'} · ${date}`;
  }

  const match = /^(\d{2}):(\d{2})$/.exec(fields.startTime);
  if (
    !match ||
    !Number.isSafeInteger(fields.durationMinutes) ||
    fields.durationMinutes < 0
  )
    return date;
  const startMinute = Number(match[1]) * 60 + Number(match[2]);
  if (startMinute >= 1440 || Number(match[2]) >= 60) return date;
  const endMinute = startMinute + fields.durationMinutes;
  if (endMinute < startMinute) return date;
  const clock = (minute: number) =>
    `${String(Math.floor(minute / 60) % 24).padStart(2, '0')}:${String(minute % 60).padStart(2, '0')}`;
  const endDayOffset = Math.floor(endMinute / 1440);
  if (endDayOffset === 0) {
    return `${fields.startTime}–${clock(endMinute)} · ${date}`;
  }
  const endDate = new Date(`${fields.date}T12:00:00Z`);
  endDate.setUTCDate(endDate.getUTCDate() + endDayOffset);
  return `${fields.startTime}–${clock(endMinute)} · ${date}–${draftDateFormatter.format(endDate)}`;
}

export function TimelineDraftVault({
  onOpen,
}: Readonly<{
  onOpen: (draft: DraftVaultItem, duplicate: boolean) => void;
}>) {
  const vault = useMemo(() => createRemoteDraftVault(), []);
  const [open, setOpen] = useState(false);
  const triggerRef = useRef<HTMLButtonElement | null>(null);
  const panelRef = useRef<HTMLElement | null>(null);
  const [actionsHost, setActionsHost] = useState<HTMLElement | null>(null);

  useEffect(() => {
    const frame = requestAnimationFrame(() => {
      setActionsHost(
        document.querySelector<HTMLElement>('.dante-timeline-actions'),
      );
    });
    return () => cancelAnimationFrame(frame);
  }, []);

  useEffect(() => {
    if (!open) return;
    const closeOutside = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !triggerRef.current?.contains(event.target) &&
        !panelRef.current?.contains(event.target)
      )
        setOpen(false);
    };
    const closeEsc = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false);
    };
    document.addEventListener('pointerdown', closeOutside, true);
    document.addEventListener('keydown', closeEsc, true);
    return () => {
      document.removeEventListener('pointerdown', closeOutside, true);
      document.removeEventListener('keydown', closeEsc, true);
    };
  }, [open]);
  const [items, setItems] = useState<readonly DraftVaultItem[]>([]);
  const [query, setQuery] = useState('');
  const [failure, setFailure] = useState('');
  const [pendingRef, setPendingRef] = useState<string | null>(null);
  const [confirmRef, setConfirmRef] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const refresh = () => {
      void vault
        .list()
        .then((loaded) => {
          if (active) {
            setItems(loaded);
            setFailure('');
          }
        })
        .catch((reason: unknown) => {
          if (active)
            setFailure(
              reason instanceof Error
                ? reason.message
                : 'Bozze non disponibili.',
            );
        });
    };
    refresh();
    window.addEventListener(DRAFT_VAULT_UPDATED, refresh);
    const unsubscribe = subscribeTemporalPlanningInvalidation(refresh);
    return () => {
      active = false;
      window.removeEventListener(DRAFT_VAULT_UPDATED, refresh);
      unsubscribe();
    };
  }, [vault]);

  const filtered = items.filter((draft) =>
    draft.title.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()),
  );

  const remove = async (item: DraftVaultItem) => {
    setPendingRef(item.draftRef);
    setFailure('');
    try {
      await vault.remove(item);
      setItems((current) =>
        current.filter((draft) => draft.draftRef !== item.draftRef),
      );
      setConfirmRef(null);
    } catch (reason) {
      setFailure(
        reason instanceof Error ? reason.message : 'Bozza non eliminata.',
      );
    } finally {
      setPendingRef(null);
    }
  };

  const trigger = (
    <button
      ref={triggerRef}
      type="button"
      className="timeline-planning-trigger"
      aria-label="Apri Bozze"
      aria-expanded={open}
      data-timeline-tooltip="Bozze"
      onClick={() => setOpen((value) => !value)}
    >
      <svg
        viewBox="0 0 24 24"
        aria-hidden="true"
        fill="none"
        stroke="currentColor"
      >
        <rect x="4" y="5" width="16" height="15" rx="2" />
        <path d="M8 10h8M8 14h6" />
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
      className="timeline-planning-tray"
      data-timeline-draft-vault="true"
      aria-label="Bozze"
    >
      <header className="timeline-planning-tray__header">
        <h2>Bozze</h2>
        <button
          type="button"
          aria-label="Chiudi Bozze"
          className="timeline-planning-tray__close"
          onClick={() => setOpen(false)}
        >
          ×
        </button>
      </header>
      <label className="timeline-planning-tray__search">
        <span className="home-visually-hidden">Cerca Bozze</span>
        <input
          type="search"
          placeholder="Cerca bozze…"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      </label>
      <div className="timeline-planning-tray__body">
        {failure ? (
          <div className="timeline-planning-empty is-search" role="alert">
            {failure}
            <button
              type="button"
              onClick={() =>
                window.dispatchEvent(new Event(DRAFT_VAULT_UPDATED))
              }
            >
              Riprova
            </button>
          </div>
        ) : null}
        {filtered.length === 0 && !failure ? (
          <div className="timeline-planning-empty">
            <strong>
              {items.length ? 'Nessuna bozza trovata' : 'Nessuna bozza'}
            </strong>
            {items.length ? null : (
              <p>Usa «Salva bozza» durante la creazione.</p>
            )}
          </div>
        ) : null}
        {filtered.map((item) => (
          <article
            key={item.draftRef}
            className="timeline-planning-card timeline-planning-card--draft"
            data-timeline-tone={
              item.payload.fields.appearanceTone ?? 'personal'
            }
          >
            <div className="timeline-planning-card__main">
              <div className="timeline-planning-card__copy">
                <strong>
                  <TemporalKindMarker kind={item.subjectKind} />
                  <span>{item.title || 'Senza titolo'}</span>
                </strong>
                <span className="timeline-planning-card__schedule">
                  {draftScheduleLabel(item)}
                </span>
                <span className="timeline-planning-card__policy">
                  Non attiva
                </span>
              </div>
            </div>
            <div className="timeline-planning-card__actions">
              <button
                type="button"
                disabled={pendingRef !== null}
                onClick={() => {
                  setOpen(false);
                  onOpen(item, false);
                }}
              >
                Riprendi
              </button>
              <button
                type="button"
                disabled={pendingRef !== null}
                onClick={() => {
                  setOpen(false);
                  onOpen(item, true);
                }}
              >
                Duplica
              </button>
              <button
                type="button"
                disabled={pendingRef !== null}
                onClick={() => setConfirmRef(item.draftRef)}
              >
                Elimina
              </button>
            </div>
            {confirmRef === item.draftRef ? (
              <div>
                <p>Eliminare definitivamente questa bozza?</p>
                <button type="button" onClick={() => setConfirmRef(null)}>
                  Annulla
                </button>
                <button
                  type="button"
                  disabled={pendingRef !== null}
                  onClick={() => void remove(item)}
                >
                  Conferma eliminazione
                </button>
              </div>
            ) : null}
          </article>
        ))}
      </div>
    </aside>
  ) : null;
  return actionsHost
    ? createPortal(
        <div
          className={`timeline-draft-vault__anchor${open ? ' is-open' : ''}`}
        >
          {trigger}
          {panel}
        </div>,
        actionsHost,
      )
    : null;
}
