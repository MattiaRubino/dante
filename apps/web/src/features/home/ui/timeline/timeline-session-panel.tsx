import { useId, useRef } from 'react';

import {
  sessionPanelRowKey,
  type SessionPanelController,
} from '../../../temporal/use-session-panel';
import './timeline-session-panel.css';

export function useSessionPanelPresentation(
  controller: SessionPanelController,
) {
  const id = useId();
  const triggerRef = useRef<HTMLButtonElement>(null);
  const count =
    controller.snapshot?.groups.reduce(
      (sum, group) => sum + group.rows.length,
      0,
    ) ?? 0;
  const visible = count > 0 || controller.error !== null;
  const close = () => {
    controller.setOpen(false);
    triggerRef.current?.focus();
  };
  return {
    control: visible ? (
      <div className="timeline-session-panel__anchor">
        <button
          ref={triggerRef}
          type="button"
          className={`timeline-session-panel__toggle${controller.open ? ' is-active' : ''}`}
          aria-label={`Sessioni disponibili${count ? ` · ${count}` : ''}`}
          aria-expanded={controller.open}
          aria-controls={controller.open ? id : undefined}
          title="Sessioni"
          onClick={() => controller.setOpen((value) => !value)}
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <rect x="3" y="4" width="18" height="16" rx="3" />
            <path d="M15 4v16M7 9l4 3-4 3z" />
          </svg>
          <span className="timeline-session-panel__badge" aria-hidden="true">
            {count || '!'}
          </span>
        </button>
        {controller.open ? (
          <aside
            id={id}
            className="timeline-session-panel"
            aria-label="Sessioni disponibili"
            onKeyDown={(event) => {
              if (event.key === 'Escape') {
                event.stopPropagation();
                close();
              }
            }}
          >
            <header>
              <div>
                <strong>Sessioni</strong>
                <span>Pronte o in corso</span>
              </div>
              <button
                type="button"
                onClick={close}
                aria-label="Chiudi pannello sessioni"
              >
                ×
              </button>
            </header>
            {controller.error ? (
              <div className="timeline-session-panel__error" role="alert">
                {controller.error}
                <button type="button" onClick={controller.refresh}>
                  Riprova
                </button>
              </div>
            ) : null}
            <div className="timeline-session-panel__groups">
              {controller.snapshot?.groups.map((group) => (
                <section key={group.activity_ref} aria-label={group.title}>
                  <h3 title={group.title}>{group.title}</h3>
                  <ul>
                    {group.rows.map((row, index) => {
                      const key = sessionPanelRowKey(group.activity_ref, row);
                      const pending = controller.pending.has(key);
                      const disabled = pending || controller.error !== null;
                      const label = !row.execution
                        ? 'Avvia'
                        : row.execution.paused
                          ? 'Riprendi'
                          : 'Pausa';
                      return (
                        <li
                          key={`${row.planned_schedule_ref ?? 'activity'}:${index}`}
                          aria-busy={pending}
                        >
                          <div className="timeline-session-panel__row">
                            <div className="timeline-session-panel__name">
                              <span title={row.name}>{row.name}</span>
                              <small>
                                {pending
                                  ? 'Aggiornamento…'
                                  : !row.execution
                                    ? 'Pronta'
                                    : row.execution.paused
                                      ? 'In pausa'
                                      : 'In corso'}
                              </small>
                            </div>
                            <div className="timeline-session-panel__controls">
                              <button
                                type="button"
                                disabled={disabled}
                                aria-label={`${label} · ${row.name}`}
                                title={label}
                                onClick={() =>
                                  void controller.command(
                                    group.activity_ref,
                                    row,
                                    'play',
                                  )
                                }
                              >
                                <span aria-hidden="true">
                                  {label === 'Pausa' ? 'Ⅱ' : '▶'}
                                </span>
                              </button>
                              <button
                                type="button"
                                disabled={disabled || !row.execution}
                                aria-label={`Termina · ${row.name}`}
                                title="Termina"
                                onClick={() =>
                                  void controller.command(
                                    group.activity_ref,
                                    row,
                                    'stop',
                                  )
                                }
                              >
                                <span aria-hidden="true">■</span>
                              </button>
                            </div>
                          </div>
                          {controller.commandErrors[key] ? (
                            <p role="alert">{controller.commandErrors[key]}</p>
                          ) : null}
                        </li>
                      );
                    })}
                  </ul>
                </section>
              ))}
            </div>
          </aside>
        ) : null}
      </div>
    ) : null,
  };
}
