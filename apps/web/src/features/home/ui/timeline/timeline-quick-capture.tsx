import { useEffect, useId, useRef, useState } from 'react';

import './timeline-quick-capture.css';

/** The existing capture preview, moved into the Timeline's transient controls. */
export function useTimelineQuickCapture() {
  const [open, setOpen] = useState(false);
  const id = useId();
  const triggerRef = useRef<HTMLButtonElement>(null);
  const panelRef = useRef<HTMLElement>(null);

  const close = () => {
    setOpen(false);
    triggerRef.current?.focus();
  };

  useEffect(() => {
    if (!open) return;
    const outside = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !triggerRef.current?.contains(event.target) &&
        !panelRef.current?.contains(event.target)
      )
        setOpen(false);
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') close();
    };
    document.addEventListener('pointerdown', outside, true);
    document.addEventListener('keydown', escape, true);
    return () => {
      document.removeEventListener('pointerdown', outside, true);
      document.removeEventListener('keydown', escape, true);
    };
  }, [open]);

  return {
    control: (
      <button
        ref={triggerRef}
        type="button"
        aria-label="Apri Cattura rapida"
        aria-expanded={open}
        aria-controls={id}
        data-timeline-tooltip="Cattura rapida"
        className={open ? 'is-active' : ''}
        onClick={() => setOpen((current) => !current)}
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
          fill="none"
          stroke="currentColor"
        >
          <path d="M5 5h14v14H5zM8 9h8M8 12h8M8 15h5" />
        </svg>
      </button>
    ),
    panel: open ? (
      <aside
        id={id}
        ref={panelRef}
        className="timeline-quick-capture home-capture-panel"
        data-timeline-quick-capture="true"
        aria-label="Cattura rapida"
      >
        <header className="home-context-heading">
          <div>
            <span className="home-context-kicker">INPUT RAPIDO</span>
            <h2>Cattura</h2>
          </div>
          <button
            type="button"
            className="timeline-quick-capture__close"
            aria-label="Chiudi Cattura rapida"
            onClick={close}
          >
            ×
          </button>
        </header>
        <div className="home-capture-composer">
          <textarea
            aria-label="Cattura rapida"
            placeholder="Scrivi qualcosa…"
            readOnly
          />
          <div className="home-capture-actions">
            <button type="button" disabled aria-label="Allega alla cattura">
              +
            </button>
            <button type="button" disabled aria-label="Registra voce">
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3Z" />
                <path d="M5.5 11.5a6.5 6.5 0 0 0 13 0M12 18v3M9 21h6" />
              </svg>
            </button>
            <button
              className="home-capture-send"
              type="button"
              disabled
              aria-label="Registra cattura"
            >
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 19V5M6.5 10.5 12 5l5.5 5.5" />
              </svg>
            </button>
          </div>
        </div>
        <div className="home-capture-history">
          <div>
            <span className="home-capture-history-dot" aria-hidden="true" />
            <p>
              <strong>Idea per il prossimo brano</strong>
              <small>Registrato · 12 min fa</small>
            </p>
          </div>
          <div>
            <span className="home-capture-history-dot" aria-hidden="true" />
            <p>
              <strong>Controllare itinerario weekend</strong>
              <small>Registrato · 46 min fa</small>
            </p>
          </div>
        </div>
        <button className="home-context-link" type="button" disabled>
          Registro completo <span aria-hidden="true">›</span>
        </button>
      </aside>
    ) : null,
  };
}
