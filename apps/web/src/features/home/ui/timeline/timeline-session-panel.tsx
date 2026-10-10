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
          data-timeline-tooltip="Sessioni"
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
                <span>Imminenti, in corso o in pausa</span>
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
              {controller.snapshot?.groups.map((group) => {
                const mainIsRunning = group.rows.some((candidate) =>
                  candidate.planned_schedule_ref === null &&
                  candidate.execution !== null && !candidate.execution.paused
                );
                return (
                <section key={group.activity_ref} aria-label={group.title}>
                  <h3 title={group.title}>{group.title}</h3>
                  <ul>
                    {group.rows.map((row, index) => {
                      const key = sessionPanelRowKey(group.activity_ref, row);
                      const pending = controller.pending.has(key);
                      const internal = row.planned_schedule_ref !== null;
                      const futureInternal = internal && !row.execution &&
                        row.starts_at !== null &&
                        Date.parse(row.starts_at) > Date.parse(
                          controller.snapshot?.evaluated_at ?? '',
                        );
                      const requiresMain = internal && !row.execution && !mainIsRunning;
                      const pausedWithoutMain = internal && row.execution?.paused &&
                        !mainIsRunning;
                      const disabled = pending || controller.error !== null ||
                        Boolean(futureInternal || requiresMain || pausedWithoutMain);
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
                              <span title={row.name}>{internal ? row.name : 'Sessione principale'}</span>
                              <small>
                                {pending
                                  ? 'Aggiornamento…'
                                  : !row.execution
                                    ? futureInternal
                                      ? 'Imminente · attende orario'
                                      : requiresMain
                                        ? 'Avvia prima la principale'
                                        : 'Pronta'
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
                );
              })}
            </div>
          </aside>
        ) : null}
      </div>
    ) : null,
  };
}
