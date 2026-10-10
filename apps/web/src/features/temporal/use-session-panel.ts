import { SessionPanelResponse, type SessionPanelRow } from '@dante/api-client';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import { createWebFetch } from '../../platform/api/web-fetch';
import { createRemoteTemporalSessionDataSource } from './remote-session-data-source';
import { subscribeTemporalTimelineInvalidation } from './timeline-invalidation';

export type SessionPanelSnapshot = SessionPanelResponse;
export type SessionPanelCommand = 'play' | 'stop';

// Applies to both CSRF and mutation requests; no permanently disabled controls.
const boundedFetch: typeof fetch = (input, init) =>
  globalThis.fetch(input, {
    ...init,
    signal: init?.signal
      ? AbortSignal.any([init.signal, AbortSignal.timeout(12_000)])
      : AbortSignal.timeout(12_000),
  });

export const sessionPanelRowKey = (activityRef: string, row: SessionPanelRow) =>
  `${activityRef}:${row.planned_schedule_ref ?? 'activity'}:${row.execution?.session_ref ?? 'ready'}`;

export function useSessionPanel(enabled = true) {
  const [snapshot, setSnapshot] = useState<SessionPanelSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState<ReadonlySet<string>>(new Set());
  const [open, setOpen] = useState(true);
  const refreshRef = useRef<() => void>(() => undefined);
  const locks = useRef(new Set<string>());
  const commandVersion = useRef(0);
  const retryOperations = useRef(new Map<string, string>());
  const mounted = useRef(false);
  const source = useMemo(
    () => createRemoteTemporalSessionDataSource(boundedFetch),
    [],
  );

  useEffect(() => {
    if (!enabled) return;
    mounted.current = true;
    let disposed = false;
    let controller: AbortController | null = null;
    let timer: ReturnType<typeof setTimeout> | undefined;
    let queued = false;
    const webFetch = createWebFetch(boundedFetch);
    const read = async () => {
      if (disposed || document.visibilityState === 'hidden') return;
      if (controller) {
        queued = true;
        return;
      }
      clearTimeout(timer);
      controller = new AbortController();
      const version = commandVersion.current;
      let delay = 30_000;
      try {
        const response = await webFetch('/api/v1/temporal/session-panel', {
          signal: controller.signal,
        });
        if (!response.ok) throw new Error('Sessioni non disponibili.');
        const next = SessionPanelResponse.parse(await response.json());
        if (disposed) return;
        if (version !== commandVersion.current) {
          queued = true;
          return;
        }
        setSnapshot(next);
        setError(null);
        if (next.next_change_at) {
          // Server-relative scheduling avoids dependence on a skewed device clock.
          delay = Math.min(
            delay,
            Math.max(
              100,
              Date.parse(next.next_change_at) - Date.parse(next.evaluated_at),
            ),
          );
        }
      } catch {
        if (!disposed) setError('Impossibile aggiornare le sessioni. Riprova.');
      } finally {
        controller = null;
        if (!disposed) {
          if (queued) {
            queued = false;
            timer = setTimeout(() => void read(), 0);
          } else timer = setTimeout(() => void read(), delay);
        }
      }
    };
    const refresh = () => {
      void read();
    };
    const visibility = () => {
      clearTimeout(timer);
      if (document.visibilityState !== 'hidden') refresh();
    };
    refreshRef.current = refresh;
    const unsubscribe = subscribeTemporalTimelineInvalidation(refresh);
    window.addEventListener('dante:session-changed', refresh);
    window.addEventListener('focus', refresh);
    window.addEventListener('online', refresh);
    document.addEventListener('visibilitychange', visibility);
    refresh();
    return () => {
      disposed = true;
      mounted.current = false;
      clearTimeout(timer);
      controller?.abort();
      unsubscribe();
      window.removeEventListener('dante:session-changed', refresh);
      window.removeEventListener('focus', refresh);
      window.removeEventListener('online', refresh);
      document.removeEventListener('visibilitychange', visibility);
      refreshRef.current = () => undefined;
    };
  }, [enabled]);

  const [commandErrors, setCommandErrors] = useState<
    Readonly<Record<string, string>>
  >({});
  const command = useCallback(
    async (
      activityRef: string,
      row: SessionPanelRow,
      action: SessionPanelCommand,
    ) => {
      const key = sessionPanelRowKey(activityRef, row);
      if (locks.current.has(key)) return;
      locks.current.add(key);
      setPending(new Set(locks.current));
      setCommandErrors((value) => ({ ...value, [key]: '' }));
      const intent = `${key}:${row.execution?.timing_material_state_ref ?? 'new'}:${action}`;
      const operationId =
        retryOperations.current.get(intent) ?? crypto.randomUUID();
      retryOperations.current.set(intent, operationId);
      try {
        const execution = row.execution;
        let result;
        if (execution) {
          const transition =
            action === 'stop'
              ? source.end
              : execution.paused
                ? source.resume
                : source.pause;
          result = await transition(
            execution.session_ref,
            execution.timing_material_state_ref,
            operationId,
          );
        } else if (action === 'play') {
          if (row.planned_schedule_ref)
            result = await source.startPlanned(
              activityRef,
              row.planned_schedule_ref,
              operationId,
            );
          else
            result = await source.start('activity', activityRef, operationId);
        }
        retryOperations.current.delete(intent);
        commandVersion.current += 1;
        if (result && mounted.current) {
          const accepted = result;
          setSnapshot((value) =>
            value === null
              ? null
              : {
                  ...value,
                  groups: value.groups.map((group) =>
                    group.activity_ref !== activityRef
                      ? group
                      : {
                          ...group,
                          rows: group.rows.map((current) =>
                            sessionPanelRowKey(activityRef, current) !== key
                              ? current
                              : {
                                  ...current,
                                  execution: accepted.open
                                    ? {
                                        session_ref: accepted.sessionRef,
                                        timing_material_state_ref:
                                          accepted.timingMaterialStateRef,
                                        paused: accepted.paused,
                                      }
                                    : null,
                                },
                          ),
                        },
                  ),
                },
          );
        }
        window.dispatchEvent(
          new CustomEvent('dante:session-changed', { detail: activityRef }),
        );
      } catch (cause) {
        if (mounted.current)
          setCommandErrors((value) => ({
            ...value,
            [key]:
              cause instanceof Error
                ? cause.message
                : 'Comando non riuscito. Aggiorna e riprova.',
          }));
      } finally {
        locks.current.delete(key);
        if (mounted.current) {
          setPending(new Set(locks.current));
          refreshRef.current();
        }
      }
    },
    [source],
  );

  return {
    snapshot,
    error,
    commandErrors,
    pending,
    open,
    setOpen,
    command,
    refresh: useCallback(() => refreshRef.current(), []),
  };
}

export type SessionPanelController = ReturnType<typeof useSessionPanel>;
