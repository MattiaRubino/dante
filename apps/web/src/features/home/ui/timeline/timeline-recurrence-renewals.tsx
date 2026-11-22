import { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

import { createWebFetch } from '../../../../platform/api/web-fetch';
import { subscribeTemporalPlanningInvalidation } from '../../../temporal/timeline-invalidation';

import './timeline-recurrence-renewals.css';

type Notice = Readonly<{
  owner: 'routine' | 'event';
  source_ref: string;
  title: string;
  material_state_ref: string;
  allowed_count: number;
  remaining_count: number;
  revision: number;
}>;

function remoteRenewals(fetchFn: typeof globalThis.fetch = globalThis.fetch) {
  const request = createWebFetch(fetchFn);
  const url = '/api/v1/temporal/open-recurrence-allowances';
  return {
    async list(): Promise<readonly Notice[]> {
      const response = await request(url, { cache: 'no-store' });
      if (!response.ok) throw new Error('Rinnovi non disponibili.');
      const payload: unknown = await response.json();
      if (!Array.isArray(payload))
        throw new Error('Elenco rinnovi non valido.');
      return payload as Notice[];
    },
    async decide(
      notice: Notice,
      decision: 'extend' | 'decline',
      operationId: string,
    ): Promise<void> {
      const sessionResponse = await request('/api/v1/auth/session');
      if (!sessionResponse.ok) throw new Error('Sessione scaduta.');
      const session = (await sessionResponse.json()) as {
        authenticated?: boolean;
        csrf_token?: string;
      };
      if (!session.authenticated || !session.csrf_token)
        throw new Error('Sessione scaduta.');
      const response = await request(
        `${url}/${notice.owner}/${encodeURIComponent(notice.source_ref)}/decision`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Dante-CSRF': session.csrf_token,
          },
          body: JSON.stringify({
            operation_id: operationId,
            expected_material_state_ref: notice.material_state_ref,
            expected_revision: notice.revision,
            decision,
          }),
        },
      );
      if (!response.ok)
        throw new Error(
          response.status === 409
            ? 'La serie è cambiata. Aggiorna l’avviso.'
            : 'Scelta non salvata. Riprova.',
        );
    },
  };
}

export function TimelineRecurrenceRenewals() {
  const remote = useMemo(() => remoteRenewals(), []);
  const [host, setHost] = useState<HTMLElement | null>(null);
  const [notices, setNotices] = useState<readonly Notice[]>([]);
  const [open, setOpen] = useState(false);
  const [failure, setFailure] = useState('');
  const [pending, setPending] = useState<string | null>(null);
  const operations = useRef(new Map<string, string>());
  const trigger = useRef<HTMLButtonElement | null>(null);
  const panel = useRef<HTMLElement | null>(null);

  useEffect(() => {
    const frame = requestAnimationFrame(() =>
      setHost(document.querySelector<HTMLElement>('.dante-timeline-actions')),
    );
    return () => cancelAnimationFrame(frame);
  }, []);
  useEffect(() => {
    let active = true;
    const refresh = () => {
      void remote
        .list()
        .then((items) => {
          if (active) {
            setNotices(items);
            setFailure('');
          }
        })
        .catch(() => {
          if (active) setFailure('Rinnovi non disponibili.');
        });
    };
    refresh();
    const unsubscribe = subscribeTemporalPlanningInvalidation(refresh);
    const timer = window.setInterval(refresh, 60 * 60 * 1000);
    const onVisibility = () => {
      if (document.visibilityState === 'visible') refresh();
    };
    document.addEventListener('visibilitychange', onVisibility);
    return () => {
      active = false;
      unsubscribe();
      window.clearInterval(timer);
      document.removeEventListener('visibilitychange', onVisibility);
    };
  }, [remote]);
  useEffect(() => {
    if (!open) return;
    const outside = (event: PointerEvent) => {
      if (
        event.target instanceof Node &&
        !trigger.current?.contains(event.target) &&
        !panel.current?.contains(event.target)
      )
        setOpen(false);
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') setOpen(false);
    };
    document.addEventListener('pointerdown', outside, true);
    document.addEventListener('keydown', escape, true);
    return () => {
      document.removeEventListener('pointerdown', outside, true);
      document.removeEventListener('keydown', escape, true);
    };
  }, [open]);

  const decide = async (notice: Notice, decision: 'extend' | 'decline') => {
    const key = `${notice.owner}:${notice.source_ref}:${notice.revision}:${decision}`;
    const operationId = operations.current.get(key) ?? crypto.randomUUID();
    operations.current.set(key, operationId);
    setPending(key);
    setFailure('');
    try {
      await remote.decide(notice, decision, operationId);
      operations.current.delete(key);
      setNotices((current) =>
        current.filter(
          (item) =>
            item.source_ref !== notice.source_ref ||
            item.owner !== notice.owner,
        ),
      );
      void remote
        .list()
        .then(setNotices)
        .catch(() => undefined);
    } catch (error) {
      setFailure(
        error instanceof Error ? error.message : 'Scelta non salvata.',
      );
    } finally {
      setPending(null);
    }
  };

  if (!host || notices.length === 0) return null;
  return createPortal(
    <div className="timeline-renewals">
      <button
        ref={trigger}
        type="button"
        aria-label={`Serie da rinnovare: ${notices.length}`}
        data-timeline-tooltip="Rinnovi"
        aria-expanded={open}
        onClick={() => setOpen(!open)}
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.6"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M4 12a8 8 0 1 1 2.3 5.7M4 17v-5h5" />
          <path d="M12 7v5l3 2" />
        </svg>
        <span className="timeline-renewals__badge" aria-hidden="true">
          +{notices.length}
        </span>
      </button>
      {open ? (
        <aside
          ref={panel}
          className="timeline-renewals__panel"
          aria-label="Serie da rinnovare"
        >
          <header>
            <strong>Serie da rinnovare</strong>
            <button
              type="button"
              onClick={() => setOpen(false)}
              aria-label="Chiudi rinnovi"
            >
              ×
            </button>
          </header>
          {notices.map((notice) => (
            <section key={`${notice.owner}:${notice.source_ref}`}>
              <strong>{notice.title}</strong>
              <p>
                {notice.owner === 'routine' ? 'Attività' : 'Evento'} ·{' '}
                {notice.remaining_count} occorrenze rimaste su{' '}
                {notice.allowed_count}
              </p>
              <div>
                <button
                  type="button"
                  disabled={pending !== null}
                  onClick={() => void decide(notice, 'extend')}
                >
                  Continua
                </button>
                <button
                  type="button"
                  disabled={pending !== null}
                  onClick={() => void decide(notice, 'decline')}
                >
                  Termina
                </button>
              </div>
            </section>
          ))}
          {failure ? <p role="alert">{failure}</p> : null}
        </aside>
      ) : null}
    </div>,
    host,
  );
}
