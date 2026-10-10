import { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import {
  createRemoteDraftVault,
  DRAFT_VAULT_UPDATED,
  type DraftVaultItem,
} from '../../../temporal-create/application/remote-draft-vault';
import { createRemoteTemporalPlanningTrayDataSource } from '../../../temporal/remote-planning-tray-data-source';
import type { TemporalPlanningTrayItem } from '../../../temporal/planning-tray-data-source';
import { subscribeTemporalPlanningInvalidation } from '../../../temporal/timeline-invalidation';

import './timeline-planning-tray.css';

export function TimelineDraftVault({
  onOpen,
  onManageExisting,
}: Readonly<{
  onOpen: (draft: DraftVaultItem, duplicate: boolean) => void;
  onManageExisting?: () => void;
}>) {
  const vault = useMemo(() => createRemoteDraftVault(), []);
  const legacySource = useMemo(
    () => createRemoteTemporalPlanningTrayDataSource(),
    [],
  );
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
  const [existing, setExisting] = useState<readonly TemporalPlanningTrayItem[]>(
    [],
  );
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
      // Legacy canonical rows are not drafts. Keep them visible as a read-only
      // migration/acceptance obligation, never misrepresenting them as inert.
      void legacySource
        .listItems()
        .then((loaded) => {
          if (active) setExisting(loaded);
        })
        .catch(() => undefined);
    };
    refresh();
    window.addEventListener(DRAFT_VAULT_UPDATED, refresh);
    const unsubscribe = subscribeTemporalPlanningInvalidation(refresh);
    return () => {
      active = false;
      window.removeEventListener(DRAFT_VAULT_UPDATED, refresh);
      unsubscribe();
    };
  }, [legacySource, vault]);

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
      title="Bozze"
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
        <div>
          <span className="timeline-planning-tray__kicker">
            DANTE · Cassaforte
          </span>
          <h2>Bozze</h2>
          <p>
            Configurazioni conservate. Nessuna Sessione, notifica o ricorrenza è
            attiva.
          </p>
        </div>
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
          placeholder="Cerca…"
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
            <strong>Nessuna bozza</strong>
            <p>Usa «Salva bozza» durante la creazione.</p>
          </div>
        ) : null}
        {filtered.map((item) => (
          <article
            key={item.draftRef}
            className="timeline-planning-card timeline-planning-card--session"
          >
            <div className="timeline-planning-card__main">
              <div className="timeline-planning-card__copy">
                <strong>{item.title || 'Senza titolo'}</strong>
                <span className="timeline-planning-card__policy">
                  {item.subjectKind === 'activity' ? 'Attività' : 'Evento'} ·
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
        {existing.length > 0 ? (
          <section aria-label="Elementi preesistenti senza orario">
            <p>Elementi creati prima delle Bozze</p>
            <p>
              Questi {existing.length} elementi sono già nel database e non sono
              bozze. Restano conservati; nessuna cancellazione o conversione
              automatica.
            </p>
            {onManageExisting ? (
              <button
                type="button"
                onClick={() => {
                  setOpen(false);
                  onManageExisting();
                }}
              >
                Gestisci elementi già creati
              </button>
            ) : null}
            {existing.map((item) => (
              <div key={`${item.kind}:${item.subjectRef}`}>
                <strong>{item.title}</strong>
                <span>
                  {' '}
                  · {item.kind === 'activity' ? 'Attività' : 'Evento'} già
                  creato
                </span>
              </div>
            ))}
          </section>
        ) : null}
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
