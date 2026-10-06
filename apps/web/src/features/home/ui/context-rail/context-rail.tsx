import { useCallback, useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { ActualRealizationControls } from '../../../temporal/actual-realization-controls';
import { ObjectiveControls } from '../../../temporal/objective-controls';
import { ReconciliationControls } from '../../../temporal/reconciliation-controls';
import {
  createResolutionQueueSource,
  type ResolutionItem,
  type ResolutionQueue,
} from './resolution-queue-data-source';

function resolutionItemKey(item: ResolutionItem): string {
  return item.reasonCode === 'reconciliation_open'
    ? `${item.reasonCode}:${item.reconciliationRef}`
    : `${item.reasonCode}:${item.subjectKind}:${item.subjectRef}`;
}

export function ContextRail() {
  const { t } = useTranslation('common');
  const source = useMemo(() => createResolutionQueueSource(), []);
  const [queue, setQueue] = useState<ResolutionQueue | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<string | null>(null);

  const refresh = useCallback(
    (signal?: AbortSignal) => {
      void source
        .list(signal)
        .then((next) => {
          setQueue(next);
          setError(null);
        })
        .catch((reason: unknown) => {
          if (signal?.aborted) return;
          setError(
            reason instanceof Error
              ? reason.message
              : 'Da risolvere non disponibile.',
          );
        });
    },
    [source],
  );

  const ownerRecorded = useCallback(() => {
    setExpanded(null);
    refresh();
  }, [refresh]);

  useEffect(() => {
    const controller = new AbortController();
    refresh(controller.signal);
    return () => controller.abort();
  }, [refresh]);

  useEffect(() => {
    const onVisible = () => {
      if (document.visibilityState === 'visible') refresh();
    };
    window.addEventListener('focus', onVisible);
    document.addEventListener('visibilitychange', onVisible);
    const interval = window.setInterval(onVisible, 60_000);
    return () => {
      window.removeEventListener('focus', onVisible);
      document.removeEventListener('visibilitychange', onVisible);
      window.clearInterval(interval);
    };
  }, [refresh]);
  return (
    <aside
      className="home-context-rail"
      data-home-region="context-rail"
      aria-label={t(($) => $.common.home.contextRail.label)}
    >
      <section className="home-capture-panel" data-home-context="capture">
        <header className="home-context-heading">
          <div>
            <span className="home-context-kicker">INPUT RAPIDO</span>
            <h2>{t(($) => $.common.home.contextRail.capture)}</h2>
          </div>
          <span className="home-context-state-dot" aria-hidden="true" />
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
      </section>
      <section className="home-resolution-panel" data-home-context="resolution">
        <header className="home-context-heading">
          <div>
            <span className="home-context-kicker">DA DANTE A TE</span>
            <h2>Da verificare</h2>
          </div>
          <span
            className="home-resolution-count"
            aria-label={`${queue?.count ?? 0} elementi aperti`}
          >
            {queue?.count ?? '…'}
          </span>
        </header>
        <p className="home-resolution-intro">
          Realtà, obiettivi e decisioni che aspettano una risposta.
        </p>
        <div className="home-resolution-list">
          {error ? (
            <p role="alert">
              {error} <button type="button" onClick={() => refresh()}>Riprova</button>
            </p>
          ) : null}
          {queue === null && error === null ? <p>Caricamento…</p> : null}
          {queue?.count === 0 ? (
            <p className="home-resolution-empty">Niente da verificare per ora.</p>
          ) : null}
          {queue?.items.map((item) => {
            const itemKey = resolutionItemKey(item);
            const isExpanded = expanded === itemKey;
            const isReality = item.reasonCode === 'realization_review';
            const isObjective = item.reasonCode === 'objective_review';
            const label = isReality
              ? 'Realtà'
              : isObjective
                ? 'Obiettivi'
                : 'Decisione';
            const description = isReality
              ? item.subjectKind === 'activity'
                ? 'Sessione conclusa · registra cosa è successo.'
                : 'Evento concluso · registra cosa è successo.'
              : isObjective
                ? 'Registra e valuta gli obiettivi.'
                : 'Decisione aperta sul risultato registrato.';
            return (
              <article key={itemKey} className="home-resolution-card">
                <div className="home-resolution-row">
                  <span className="home-resolution-status is-partial">{label}</span>
                  <time dateTime={item.effectiveAt}>
                    {new Intl.DateTimeFormat('it-IT', {
                      day: 'numeric',
                      month: 'short',
                      hour: '2-digit',
                      minute: '2-digit',
                    }).format(new Date(item.effectiveAt))}
                  </time>
                </div>
                <strong>{item.title}</strong>
                <p>{description}</p>
                {isReality ? (
                  <ActualRealizationControls
                    kind={item.subjectKind}
                    subjectRef={item.subjectRef}
                    showObjectives={false}
                    sessionBasis={
                      item.sessionRef && item.sessionTimingMaterialStateRef
                        ? {
                            sessionRef: item.sessionRef,
                            sessionTimingMaterialStateRef:
                              item.sessionTimingMaterialStateRef,
                          }
                        : undefined
                    }
                    onRecorded={ownerRecorded}
                  />
                ) : (
                  <>
                    <button
                      className="home-resolution-details"
                      type="button"
                      aria-expanded={isExpanded}
                      aria-label={`${isExpanded ? 'Chiudi' : isObjective ? 'Valuta obiettivi' : 'Apri decisione'}: ${item.title}`}
                      onClick={() =>
                        setExpanded((current) =>
                          current === itemKey ? null : itemKey,
                        )
                      }
                    >
                      {isExpanded ? 'Chiudi' : isObjective ? 'Valuta obiettivi' : 'Apri decisione'}
                    </button>
                    {isExpanded && item.reasonCode === 'reconciliation_open' ? (
                      <ReconciliationControls
                        kind={item.subjectKind}
                        subjectRef={item.subjectRef}
                        initialPurposeCode={item.purposeCode}
                        onRecorded={ownerRecorded}
                      />
                    ) : null}
                    {isExpanded && item.reasonCode === 'objective_review' ? (
                      <ObjectiveControls
                        kind={item.subjectKind}
                        subjectRef={item.subjectRef}
                        onRecorded={refresh}
                      />
                    ) : null}
                  </>
                )}
              </article>
            );
          })}
        </div>
      </section>
      <div className="home-create-panel-host" data-home-context-create-host />
    </aside>
  );
}
