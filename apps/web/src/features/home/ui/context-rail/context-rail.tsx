import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from 'react';
import { useTranslation } from 'react-i18next';

import { formatDateWithCapitalizedMonth } from '../../../../platform/format-localized-date';

import { ActualRealizationControls } from '../../../temporal/actual-realization-controls';
import { ObjectiveControls } from '../../../temporal/objective-controls';
import { ReconciliationControls } from '../../../temporal/reconciliation-controls';
import { SessionSubjectControls } from '../../../temporal/session-subject-controls';
import { TemporalKindMarker } from '../../../temporal-create/ui/temporal-kind-marker';
import { subscribeTemporalTimelineInvalidation } from '../../../temporal/timeline-invalidation';
import {
  canonicalItemPresentationColor,
  canonicalOrganizationGroups,
  useTimelineOrganization,
} from '../timeline/timeline-organization';
import {
  createContextRailWorkSource,
  type PendingObjectiveWork,
} from './context-rail-work-data-source';
import {
  loadPastWorkCursorPage,
  openPastWork,
  type PastWorkCursor,
  type PastWorkItem,
} from './past-work';
import {
  createResolutionQueueSource,
  type ResolutionItem,
  type ResolutionQueue,
} from './resolution-queue-data-source';
import { REVIEW_QUEUE_INVALIDATED } from './review-events';

function resolutionItemKey(item: ResolutionItem): string {
  if (item.reasonCode === 'reconciliation_open')
    return `${item.reasonCode}:${item.reconciliationRef}`;
  if (item.reasonCode === 'session_unstarted')
    return `${item.reasonCode}:${item.subjectRef}:${item.plannedScheduleRef ?? 'main'}`;
  return `${item.reasonCode}:${item.subjectKind}:${item.subjectRef}`;
}

export function ContextRail() {
  const { t } = useTranslation('common');
  const source = useMemo(() => createResolutionQueueSource(), []);
  const workSource = useMemo(() => createContextRailWorkSource(), []);
  const [tab, setTab] = useState<'finished' | 'review' | 'objectives'>(
    'review',
  );
  const tabs = ['finished', 'review', 'objectives'] as const;
  const touchStart = useRef<{ x: number; y: number } | null>(null);
  const [past, setPast] = useState<readonly PastWorkItem[] | null>(null);
  const [pastInput, setPastInput] = useState('');
  const [pastQuery, setPastQuery] = useState('');
  const [pastLoadMore, setPastLoadMore] = useState(0);
  const [pastHasMore, setPastHasMore] = useState(true);
  const [pastRevision, setPastRevision] = useState(0);
  const [pastError, setPastError] = useState<string | null>(null);
  const [pastLoading, setPastLoading] = useState(false);
  const visiblePast = useMemo(
    () =>
      past?.filter(({ item }) =>
        item.title.toLocaleLowerCase('it-IT').includes(pastQuery),
      ),
    [past, pastQuery],
  );
  const pastCursorRef = useRef<PastWorkCursor | null>(null);
  const pastLoadedRef = useRef<readonly PastWorkItem[]>([]);
  const pastKeyRef = useRef('');
  const pastPagingRef = useRef(false);
  const pastExhaustedRef = useRef(false);
  const pastListRef = useRef<HTMLDivElement>(null);
  const pastTailRef = useRef<HTMLDivElement>(null);
  const requestPastPage = useCallback(() => {
    if (pastPagingRef.current || pastExhaustedRef.current) return;
    pastPagingRef.current = true;
    setPastLoadMore((value) => value + 1);
  }, []);
  const organization = useTimelineOrganization(true);
  const areas = useMemo(
    () =>
      organization.snapshot
        ? canonicalOrganizationGroups(organization.snapshot)
        : [],
    [organization.snapshot],
  );
  const assignments = useMemo(
    () =>
      new Map(
        organization.snapshot?.assignments.map((item) => [
          `${item.kind}:${item.itemRef}`,
          item.areaRef,
        ]) ?? [],
      ),
    [organization.snapshot],
  );
  const [objectives, setObjectives] = useState<
    readonly PendingObjectiveWork[] | null
  >(null);
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

  const refreshWork = useCallback(
    (signal?: AbortSignal) => {
      void workSource
        .listObjectives(signal)
        .then((pending) => {
          setObjectives(pending);
          setWorkError(null);
        })
        .catch((reason: unknown) => {
          if (signal?.aborted) return;
          setWorkError(
            reason instanceof Error
              ? reason.message
              : 'Riepilogo non disponibile.',
          );
        });
    },
    [workSource],
  );

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

  useEffect(
    () =>
      subscribeTemporalTimelineInvalidation(() =>
        setPastRevision((value) => value + 1),
      ),
    [],
  );

  useEffect(() => {
    const timeout = window.setTimeout(
      () => setPastQuery(pastInput.trim().toLocaleLowerCase('it-IT')),
      180,
    );
    return () => window.clearTimeout(timeout);
  }, [pastInput]);

  useEffect(() => {
    if (tab !== 'finished') return;
    const controller = new AbortController();
    const key = `${pastRevision}:${pastQuery}`;
    const changed = pastKeyRef.current !== key;
    const oldQuery = pastKeyRef.current.split(':').slice(1).join(':');
    const previousMatches = pastLoadedRef.current.filter(({ item }) =>
      item.title.toLocaleLowerCase('it-IT').includes(pastQuery),
    ).length;
    const target = changed
      ? oldQuery === pastQuery
        ? Math.max(pastQuery ? 12 : 40, previousMatches)
        : pastQuery
          ? 12
          : 40
      : previousMatches + (pastQuery ? 12 : 40);
    if (changed) {
      pastPagingRef.current = false;
      pastExhaustedRef.current = false;
      pastKeyRef.current = key;
      pastCursorRef.current = null;
      pastLoadedRef.current = [];
      setPastHasMore(true);
      if (oldQuery !== pastQuery) setPast([]);
    }
    setPastLoading(true);
    void (async () => {
      let cursor = pastCursorRef.current;
      let loaded = [...pastLoadedRef.current];
      // A query keeps advancing the owner-scoped cursor until there are
      // matches to display. Empty matches never mean "no older history".
      do {
        const page = await loadPastWorkCursorPage(cursor, controller.signal);
        if (controller.signal.aborted) return;
        const unique = new Map(
          [...loaded, ...page.items].map((entry) => [
            entry.item.scheduleRef,
            entry,
          ]),
        );
        loaded = [...unique.values()].sort(
          (a, b) =>
            b.endedAt.localeCompare(a.endedAt) ||
            b.item.scheduleRef.localeCompare(a.item.scheduleRef),
        );
        cursor = page.next;
        pastCursorRef.current = cursor;
        pastExhaustedRef.current = cursor === null;
        pastLoadedRef.current = loaded;
        setPast(loaded);
        setPastHasMore(cursor !== null);
        setPastError(null);
      } while (
        cursor &&
        loaded.filter(({ item }) =>
          item.title.toLocaleLowerCase('it-IT').includes(pastQuery),
        ).length < target
      );
    })()
      .catch((reason: unknown) => {
        if (controller.signal.aborted) return;
        setPastError(
          reason instanceof Error
            ? reason.message
            : 'Cronologia non disponibile.',
        );
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setPastLoading(false);
          pastPagingRef.current = false;
        }
      });
    return () => controller.abort();
  }, [pastLoadMore, pastQuery, pastRevision, tab]);

  useEffect(() => {
    const root = pastListRef.current;
    const tail = pastTailRef.current;
    if (
      tab !== 'finished' ||
      !root ||
      !tail ||
      !pastHasMore ||
      pastLoading ||
      typeof IntersectionObserver === 'undefined'
    )
      return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry?.isIntersecting && !pastError) requestPastPage();
      },
      { root, rootMargin: '180px' },
    );
    observer.observe(tail);
    return () => observer.disconnect();
  }, [tab, pastHasMore, pastLoading, past, pastError, requestPastPage]);

  useEffect(() => {
    const onVisible = () => {
      if (document.visibilityState === 'visible') {
        refresh();
        refreshWork();
        setPastRevision((value) => value + 1);
      }
    };
    window.addEventListener('focus', onVisible);
    window.addEventListener('dante:session-changed', onVisible);
    window.addEventListener(REVIEW_QUEUE_INVALIDATED, onVisible);
    document.addEventListener('visibilitychange', onVisible);
    const interval = window.setInterval(onVisible, 60_000);
    return () => {
      window.removeEventListener('focus', onVisible);
      window.removeEventListener('dante:session-changed', onVisible);
      window.removeEventListener(REVIEW_QUEUE_INVALIDATED, onVisible);
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
      <section className="home-resolution-panel" data-home-context="resolution">
        <header className="home-context-heading">
          <div>
            <span className="home-context-kicker">DA DANTE A TE</span>
            <h2>Attività e risultati</h2>
          </div>
          <span
            className="home-resolution-count"
            aria-label={
              tab === 'review'
                ? `${queue?.count ?? 0} elementi da verificare`
                : tab === 'finished'
                  ? `${past?.length ?? 0} elementi caricati in Cronologia`
                  : `${objectives?.length ?? 0} Obiettivi da compilare`
            }
          >
            {tab === 'review'
              ? (queue?.count ?? '…')
              : tab === 'finished'
                ? (past?.length ?? '…')
                : (objectives?.length ?? '…')}
          </span>
        </header>
        <div
          role="tablist"
          aria-label="Pagine attività e risultati"
          className="home-resolution-tabs"
        >
          {tabs.map((value) => (
            <button
              key={value}
              type="button"
              role="tab"
              id={`home-work-tab-${value}`}
              aria-selected={tab === value}
              aria-controls="home-work-tabpanel"
              className={tab === value ? 'is-active' : ''}
              onClick={() => {
                setTab(value);
                setExpanded(null);
              }}
              onKeyDown={(event) => {
                if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight')
                  return;
                event.preventDefault();
                const offset = event.key === 'ArrowRight' ? 1 : -1;
                const target =
                  tabs[
                    (tabs.indexOf(tab) + offset + tabs.length) % tabs.length
                  ];
                setTab(target ?? tab);
                document.getElementById(`home-work-tab-${target}`)?.focus();
              }}
            >
              {value === 'finished'
                ? 'Cronologia'
                : value === 'review'
                  ? 'Da verificare'
                  : 'Obiettivi'}
            </button>
          ))}
        </div>
        {tab === 'finished' && (
          <div className="home-past-toolbar">
            <input
              type="search"
              aria-label="Cerca nella Cronologia"
              placeholder="Cerca nella Cronologia…"
              value={pastInput}
              onChange={(event) => setPastInput(event.target.value)}
            />
            <button
              type="button"
              aria-label="Aggiorna Cronologia"
              title="Aggiorna Cronologia"
              aria-busy={pastLoading}
              onClick={() => setPastRevision((value) => value + 1)}
            >
              <svg
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                aria-hidden="true"
              >
                <path d="M20 11a8 8 0 1 1-2.3-5.7M20 4v5h-5" />
              </svg>
            </button>
          </div>
        )}
        <div
          className="home-resolution-list"
          ref={pastListRef}
          id="home-work-tabpanel"
          role="tabpanel"
          aria-labelledby={`home-work-tab-${tab}`}
          onScroll={(event) => {
            if (tab !== 'finished' || pastLoading || !pastHasMore || pastError)
              return;
            const node = event.currentTarget;
            if (node.scrollHeight - node.scrollTop - node.clientHeight < 180)
              requestPastPage();
          }}
          onTouchStart={(event) => {
            const touch = event.touches[0];
            if (touch)
              touchStart.current = { x: touch.clientX, y: touch.clientY };
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
            setTab(
              tabs[(tabs.indexOf(tab) + offset + tabs.length) % tabs.length] ??
                tab,
            );
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
                  {error}{' '}
                  <button type="button" onClick={() => refresh()}>
                    Riprova
                  </button>
                </p>
              ) : null}
              {queue === null && error === null ? <p>Caricamento…</p> : null}
              {queue?.count === 0 ? (
                <p className="home-resolution-empty">
                  Niente da verificare per ora.
                </p>
              ) : null}
              {queue?.items.map((item) => {
                const itemKey = resolutionItemKey(item);
                const isExpanded = expanded === itemKey;
                const isReality = item.reasonCode === 'realization_review';
                const isObjective = item.reasonCode === 'objective_review';
                const isUnstarted = item.reasonCode === 'session_unstarted';
                const label = isUnstarted
                  ? 'Sessione'
                  : isReality
                    ? 'Realtà'
                    : isObjective
                      ? 'Obiettivi'
                      : 'Decisione';
                const description = isUnstarted
                  ? item.summary
                  : isReality
                    ? item.subjectKind === 'activity'
                      ? item.sessionRef
                        ? 'Sessione conclusa · registra cosa è successo.'
                        : 'Orario passato senza Sessione · verifica se è avvenuta.'
                      : 'Evento concluso · registra cosa è successo.'
                    : isObjective
                      ? 'Registra e valuta gli obiettivi.'
                      : 'Decisione aperta sul risultato registrato.';
                return (
                  <article key={itemKey} className="home-resolution-card">
                    <div className="home-resolution-row">
                      <span className="home-resolution-status is-partial">
                        {label}
                      </span>
                      <time dateTime={item.effectiveAt}>
                        {formatDateWithCapitalizedMonth(
                          new Intl.DateTimeFormat('it-IT', {
                            day: 'numeric',
                            month: 'short',
                            hour: '2-digit',
                            minute: '2-digit',
                          }),
                          new Date(item.effectiveAt),
                        )}
                      </time>
                    </div>
                    <strong>{item.title}</strong>
                    <p>{description}</p>
                    {isUnstarted ? null : isReality ? (
                      <>
                        {item.subjectKind === 'activity' &&
                        item.sessionRef === null ? (
                          <SessionSubjectControls
                            kind="activity"
                            subjectRef={item.subjectRef}
                            label={item.title}
                            allowLive={false}
                            allowManual
                            onRecorded={ownerRecorded}
                          />
                        ) : null}
                        <ActualRealizationControls
                          kind={item.subjectKind}
                          subjectRef={item.subjectRef}
                          showObjectives={false}
                          {...(item.sessionRef &&
                          item.sessionTimingMaterialStateRef
                            ? {
                                sessionBasis: {
                                  sessionRef: item.sessionRef,
                                  sessionTimingMaterialStateRef:
                                    item.sessionTimingMaterialStateRef,
                                },
                              }
                            : {})}
                          onRecorded={ownerRecorded}
                          compactReview={item.sessionRef === null}
                        />
                      </>
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
                          {isExpanded
                            ? 'Chiudi'
                            : isObjective
                              ? 'Valuta obiettivi'
                              : 'Apri decisione'}
                        </button>
                        {isExpanded &&
                        item.reasonCode === 'reconciliation_open' ? (
                          <ReconciliationControls
                            kind={item.subjectKind}
                            subjectRef={item.subjectRef}
                            initialPurposeCode={item.purposeCode}
                            onRecorded={ownerRecorded}
                          />
                        ) : null}
                        {isExpanded &&
                        item.reasonCode === 'objective_review' ? (
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
              {pastError && (
                <p role="alert">
                  {pastError}{' '}
                  <button
                    type="button"
                    onClick={() => setPastRevision((value) => value + 1)}
                  >
                    Riprova
                  </button>
                </p>
              )}
              {visiblePast?.length === 0 && !pastLoading && !pastHasMore && (
                <p className="home-resolution-empty">
                  Nessun elemento trovato.
                </p>
              )}
              {visiblePast?.map(({ item, label }) => {
                const kind =
                  item.kind === 'scheduled_event' ||
                  (item.kind === 'scheduled_occurrence' &&
                    item.sourceKind === 'event')
                    ? 'event'
                    : 'activity';
                const color = canonicalItemPresentationColor(
                  item,
                  areas,
                  assignments,
                );
                return (
                  <article
                    key={item.scheduleRef}
                    className={`home-past-card home-past-card--${kind}`}
                    style={
                      {
                        '--home-past-accent': color ?? '#7F8B9D',
                      } as CSSProperties
                    }
                  >
                    <button
                      type="button"
                      aria-label={`Apri ${kind === 'event' ? 'Evento' : 'Attività'} ${item.title}`}
                      onClick={(event) =>
                        openPastWork(item, event.currentTarget)
                      }
                    >
                      <span className="home-past-card__title">
                        <TemporalKindMarker kind={kind} />
                        <strong>{item.title}</strong>
                      </span>
                      <span className="home-past-card__time">{label}</span>
                    </button>
                  </article>
                );
              })}
              <div
                ref={pastTailRef}
                className="home-past-tail"
                aria-hidden="true"
              />
              {pastLoading && (
                <span
                  className="home-past-progress"
                  role="status"
                  aria-label="Aggiornamento Cronologia in corso"
                />
              )}
            </>
          ) : (
            <>
              <p className="home-resolution-intro">
                Obiettivi senza risultato confermato. I valori in bozza restano
                salvati.
              </p>
              {workError && <p role="alert">{workError}</p>}
              {objectives === null && !workError && <p>Caricamento…</p>}
              {objectiveOwners.length === 0 && objectives !== null && (
                <p className="home-resolution-empty">
                  Nessun Obiettivo da compilare.
                </p>
              )}
              {objectiveOwners.map(({ key, items }) => (
                <article className="home-resolution-card" key={key}>
                  <div className="home-resolution-row">
                    <span className="home-resolution-status is-partial">
                      {items.length} Obiettivi
                    </span>
                    <span>
                      {items.some((item) => item.draft_revision !== null)
                        ? 'Bozza salvata'
                        : 'Da compilare'}
                    </span>
                  </div>
                  <strong>{items[0]?.subject_title}</strong>
                  <p>{items.map((item) => item.label).join(' · ')}</p>
                  <button
                    type="button"
                    className="home-resolution-details"
                    aria-expanded={expanded === key}
                    onClick={() =>
                      setExpanded((current) => (current === key ? null : key))
                    }
                  >
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
