import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';

import { ActualRealizationControls } from '../../../temporal/actual-realization-controls';
import { ObjectiveControls } from '../../../temporal/objective-controls';
import { ReconciliationControls } from '../../../temporal/reconciliation-controls';
import {
  createContextRailWorkSource,
  type FinishedWorkItem,
  type PendingObjectiveWork,
} from './context-rail-work-data-source';
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
  const workSource = useMemo(() => createContextRailWorkSource(), []);
  const [tab, setTab] = useState<'finished' | 'review' | 'objectives'>('review');
  const tabs = ['finished', 'review', 'objectives'] as const;
  const touchStart = useRef<{ x: number; y: number } | null>(null);
  const [finished, setFinished] = useState<readonly FinishedWorkItem[] | null>(null);
  const [objectives, setObjectives] = useState<readonly PendingObjectiveWork[] | null>(null);
  const [workError, setWorkError] = useState<string | null>(null);
  const objectiveOwners = useMemo(() => {
    const owners = new Map<string, PendingObjectiveWork[]>();
    for (const objective of objectives ?? []) {
      const key = `${objective.subject_kind}:${objective.subject_ref}`;
      owners.set(key, [...(owners.get(key) ?? []), objective]);
    }
    return [...owners.entries()].map(([key, items]) => ({ key, items }));
  }, [objectives]);
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

  const refreshWork = useCallback((signal?: AbortSignal) => {
    void Promise.all([
      workSource.listFinished(signal), workSource.listObjectives(signal),
    ]).then(([history, pending]) => {
      setFinished(history);
      setObjectives(pending);
      setWorkError(null);
    }).catch((reason: unknown) => {
      if (signal?.aborted) return;
      setWorkError(reason instanceof Error ? reason.message : 'Riepilogo non disponibile.');
    });
  }, [workSource]);

  const ownerRecorded = useCallback(() => {
    setExpanded(null);
    refresh();
    refreshWork();
  }, [refresh, refreshWork]);

  useEffect(() => {
    const controller = new AbortController();
    refresh(controller.signal);
    refreshWork(controller.signal);
    return () => controller.abort();
  }, [refresh, refreshWork]);

  useEffect(() => {
    const onVisible = () => {
      if (document.visibilityState === 'visible') {
        refresh();
        refreshWork();
      }
    };
    window.addEventListener('focus', onVisible);
    document.addEventListener('visibilitychange', onVisible);
    const interval = window.setInterval(onVisible, 60_000);
    return () => {
      window.removeEventListener('focus', onVisible);
      document.removeEventListener('visibilitychange', onVisible);
      window.clearInterval(interval);
    };
  }, [refresh, refreshWork]);
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
            <h2>Attività e risultati</h2>
          </div>
          <span
            className="home-resolution-count"
            aria-label={`${queue?.count ?? 0} elementi da verificare`}
          >
            {tab === 'review' ? queue?.count ?? '…'
              : tab === 'finished' ? finished?.length ?? '…'
              : objectives?.length ?? '…'}
          </span>
        </header>
        <div role="tablist" aria-label="Pagine attività e risultati"
          className="home-resolution-tabs">
          {tabs.map((value) => (
            <button key={value} type="button" role="tab"
              id={`home-work-tab-${value}`}
              aria-selected={tab === value}
              aria-controls="home-work-tabpanel"
              className={tab === value ? 'is-active' : ''}
              onClick={() => { setTab(value); setExpanded(null); }}
              onKeyDown={(event) => {
                if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
                event.preventDefault();
                const offset = event.key === 'ArrowRight' ? 1 : -1;
                const target = tabs[(tabs.indexOf(tab) + offset + tabs.length) % tabs.length];
                setTab(target);
                document.getElementById(`home-work-tab-${target}`)?.focus();
              }}
            >
              {value === 'finished' ? 'Conclusi'
                : value === 'review' ? 'Da verificare' : 'Obiettivi'}
            </button>
          ))}
        </div>
        <div className="home-resolution-list" id="home-work-tabpanel"
          role="tabpanel" aria-labelledby={`home-work-tab-${tab}`}
          onTouchStart={(event) => {
            const touch = event.touches[0];
            if (touch) touchStart.current = { x: touch.clientX, y: touch.clientY };
          }}
          onTouchEnd={(event) => {
            const origin = touchStart.current;
            const touch = event.changedTouches[0];
            touchStart.current = null;
            if (!origin || !touch) return;
            const dx = touch.clientX - origin.x;
            const dy = touch.clientY - origin.y;
            if (Math.abs(dx) <= 65 || Math.abs(dx) < Math.abs(dy) * 1.5) return;
            const offset = dx < 0 ? 1 : -1;
            setTab(tabs[(tabs.indexOf(tab) + offset + tabs.length) % tabs.length]);
            setExpanded(null);
          }}
        >
          {tab === 'review' ? (
            <>
          <p className="home-resolution-intro">
            Realtà, verifiche e decisioni che aspettano una risposta.
          </p>
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
                    {...(item.sessionRef && item.sessionTimingMaterialStateRef
                      ? {
                          sessionBasis: {
                            sessionRef: item.sessionRef,
                            sessionTimingMaterialStateRef:
                              item.sessionTimingMaterialStateRef,
                          },
                        }
                      : {})}
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
            </>
          ) : tab === 'finished' ? (
            <>
              <p className="home-resolution-intro">Esecuzioni e realizzazioni effettivamente concluse negli ultimi 90 giorni.</p>
              {workError && <p role="alert">{workError}</p>}
              {finished === null && !workError && <p>Caricamento…</p>}
              {finished?.length === 0 && <p className="home-resolution-empty">Nessuna esecuzione conclusa.</p>}
              {finished?.map((item, index) => (
                <article className="home-resolution-card"
                  key={`${item.record_kind}:${item.session_ref ?? item.subject_ref}:${index}`}>
                  <div className="home-resolution-row">
                    <span className="home-resolution-status is-partial">
                      {item.record_kind === 'session_ended'
                        ? 'Sessione conclusa' : 'Realtà registrata'}
                    </span>
                    <time dateTime={item.ended_at}>
                      {new Intl.DateTimeFormat('it-IT', {
                        day:'numeric',month:'short',hour:'2-digit',minute:'2-digit',
                      }).format(new Date(item.ended_at))}
                    </time>
                  </div>
                  <strong>{item.title}</strong>
                  <p>{item.record_kind === 'session_ended'
                    ? 'La Sessione è terminata; non implica automaticamente Attività completata.'
                    : item.subject_kind === 'event'
                      ? 'Evento confermato come avvenuto.'
                      : 'Attività registrata come svolta.'}</p>
                </article>
              ))}
            </>
          ) : (
            <>
              <p className="home-resolution-intro">
                Obiettivi senza risultato confermato. I valori in bozza restano salvati.
              </p>
              {workError && <p role="alert">{workError}</p>}
              {objectives === null && !workError && <p>Caricamento…</p>}
              {objectiveOwners.length === 0 && objectives !== null &&
                <p className="home-resolution-empty">Nessun Obiettivo da compilare.</p>}
              {objectiveOwners.map(({key, items}) => (
                <article className="home-resolution-card" key={key}>
                  <div className="home-resolution-row">
                    <span className="home-resolution-status is-partial">
                      {items.length} Obiettivi
                    </span>
                    <span>{items.some(item => item.draft_revision !== null)
                      ? 'Bozza salvata' : 'Da compilare'}</span>
                  </div>
                  <strong>{items[0]?.subject_title}</strong>
                  <p>{items.map((item) => item.label).join(' · ')}</p>
                  <button type="button" className="home-resolution-details"
                    aria-expanded={expanded === key}
                    onClick={() => setExpanded((current) => current === key ? null : key)}>
                    {expanded === key ? 'Chiudi' : 'Compila obiettivi'}
                  </button>
                  {expanded === key && items[0] ? (
                    <ObjectiveControls
                      kind={items[0].subject_kind}
                      subjectRef={items[0].subject_ref}
                      onRecorded={ownerRecorded}
                    />
                  ) : null}
                </article>
              ))}
            </>
          )}
        </div>
      </section>
      <div className="home-create-panel-host" data-home-context-create-host />
    </aside>
  );
}
