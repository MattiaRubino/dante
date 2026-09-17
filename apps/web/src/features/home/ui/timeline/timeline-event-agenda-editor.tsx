import { useCallback, useEffect, useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';

import type {
  TemporalEventAgendaDataSource,
  TemporalEventDetailRecord,
} from '../../../temporal/event-data-source';
import { systemTemporalIdFactory, type TemporalIdFactory } from '../../../temporal/model';
import {
  createRemoteTemporalEventAgendaDataSource,
  TemporalEventAgendaRemoteError,
} from '../../../temporal/remote-event-agenda-data-source';

import './timeline-event-agenda-editor.css';

type AgendaState =
  | Readonly<{ status: 'loading' }>
  | Readonly<{ status: 'error' }>
  | Readonly<{ status: 'ready'; record: TemporalEventDetailRecord }>;

type TimelineEventAgendaEditorProps = Readonly<{
  eventRef: string;
  dataSource?: TemporalEventAgendaDataSource;
  ids?: TemporalIdFactory;
}>;

export function TimelineEventAgendaEditor({
  eventRef,
  dataSource,
  ids = systemTemporalIdFactory,
}: TimelineEventAgendaEditorProps) {
  const { t } = useTranslation('common');
  const source = useMemo(
    () => dataSource ?? createRemoteTemporalEventAgendaDataSource(),
    [dataSource],
  );
  const [state, setState] = useState<AgendaState>({ status: 'loading' });
  const [draft, setDraft] = useState('');
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editingValue, setEditingValue] = useState('');
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<'conflict' | 'error' | null>(null);

  const load = useCallback(
    async (signal?: AbortSignal) => {
      try {
        const record = await source.loadEvent(eventRef, signal);
        setState({ status: 'ready', record });
        setNotice(null);
      } catch (error) {
        if (signal?.aborted) {
          return;
        }
        setState({ status: 'error' });
        setNotice('error');
      }
    },
    [eventRef, source],
  );

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: 'loading' });
    void load(controller.signal);
    return () => controller.abort();
  }, [load]);

  const replace = useCallback(
    async (agendaParts: readonly string[]) => {
      if (state.status !== 'ready' || busy) {
        return;
      }
      setBusy(true);
      setNotice(null);
      try {
        const result = await source.replaceAgenda({
          eventRef,
          operationId: ids.operationId(),
          expectedRevision: state.record.agendaRevision,
          agendaParts,
        });
        setState({
          status: 'ready',
          record: Object.freeze({
            ...state.record,
            agendaRevision: result.agendaRevision,
            agendaParts: result.agendaParts,
          }),
        });
        setEditingIndex(null);
        setEditingValue('');
      } catch (error) {
        const conflict =
          error instanceof TemporalEventAgendaRemoteError &&
          error.status === 409 &&
          error.code === 'temporal.event.agenda_revision_conflict';
        setNotice(conflict ? 'conflict' : 'error');
        await load();
      } finally {
        setBusy(false);
      }
    },
    [busy, eventRef, ids, load, source, state],
  );

  if (state.status === 'loading') {
    return (
      <section className="timeline-event-agenda" aria-busy="true">
        <strong>{t(($) => $.common.home.timeline.create.eventDetails.agenda)}</strong>
        <p>{t(($) => $.common.temporalRuntime.timeline.loading)}</p>
      </section>
    );
  }

  if (state.status === 'error') {
    return (
      <section className="timeline-event-agenda">
        <strong>{t(($) => $.common.home.timeline.create.eventDetails.agenda)}</strong>
        <div role="alert">
          {t(($) => $.common.temporalRuntime.timeline.errorDescription)}
        </div>
        <button type="button" onClick={() => void load()}>
          {t(($) => $.common.temporalRuntime.timeline.retry)}
        </button>
      </section>
    );
  }

  const parts = state.record.agendaParts;
  const add = () => {
    const value = draft.trim();
    if (!value || busy) {
      return;
    }
    void replace([...parts, value]);
    setDraft('');
  };

  return (
    <section className="timeline-event-agenda" aria-busy={busy}>
      <div className="timeline-event-agenda__heading">
        <strong>{t(($) => $.common.home.timeline.create.eventDetails.agenda)}</strong>
        <span aria-label={`revision ${state.record.agendaRevision}`}>
          r{state.record.agendaRevision}
        </span>
      </div>
      <p>{t(($) => $.common.home.timeline.create.eventDetails.agendaDescription)}</p>

      {notice === 'conflict' ? (
        <div role="status" className="timeline-event-agenda__notice">
          Agenda aggiornata altrove: ho ricaricato la versione corrente.
        </div>
      ) : notice === 'error' ? (
        <div role="alert" className="timeline-event-agenda__notice">
          Impossibile salvare l’Agenda. Ho ricaricato la versione corrente.
        </div>
      ) : null}

      {parts.length === 0 ? (
        <p>{t(($) => $.common.home.timeline.create.eventDetails.agendaEmpty)}</p>
      ) : (
        <ol className="timeline-event-agenda__list">
          {parts.map((part, index) => {
            const position = index + 1;
            const editing = editingIndex === index;
            return (
              <li key={`${position}:${part}`}>
                {editing ? (
                  <input
                    value={editingValue}
                    maxLength={1000}
                    disabled={busy}
                    aria-label={t(
                      ($) => $.common.home.timeline.create.eventDetails.agendaEdit,
                      { position },
                    )}
                    onChange={(event) => setEditingValue(event.currentTarget.value)}
                    onKeyDown={(event) => {
                      if (event.key === 'Enter') {
                        event.preventDefault();
                        const next = editingValue.trim();
                        if (next) {
                          void replace(
                            parts.map((candidate, candidateIndex) =>
                              candidateIndex === index ? next : candidate,
                            ),
                          );
                        }
                      } else if (event.key === 'Escape') {
                        setEditingIndex(null);
                        setEditingValue('');
                      }
                    }}
                  />
                ) : (
                  <button
                    type="button"
                    className="timeline-event-agenda__value"
                    disabled={busy}
                    onClick={() => {
                      setEditingIndex(index);
                      setEditingValue(part);
                    }}
                  >
                    {part}
                  </button>
                )}
                <div className="timeline-event-agenda__actions">
                  <button
                    type="button"
                    disabled={busy || index === 0}
                    aria-label={t(
                      ($) => $.common.home.timeline.create.eventDetails.agendaMoveUp,
                      { position },
                    )}
                    onClick={() => {
                      if (index === 0) return;
                      const next = [...parts];
                      [next[index - 1], next[index]] = [next[index]!, next[index - 1]!];
                      void replace(next);
                    }}
                  >
                    ↑
                  </button>
                  <button
                    type="button"
                    disabled={busy || index === parts.length - 1}
                    aria-label={t(
                      ($) => $.common.home.timeline.create.eventDetails.agendaMoveDown,
                      { position },
                    )}
                    onClick={() => {
                      if (index >= parts.length - 1) return;
                      const next = [...parts];
                      [next[index], next[index + 1]] = [next[index + 1]!, next[index]!];
                      void replace(next);
                    }}
                  >
                    ↓
                  </button>
                  <button
                    type="button"
                    disabled={busy}
                    aria-label={t(
                      ($) => $.common.home.timeline.create.eventDetails.agendaRemove,
                      { position },
                    )}
                    onClick={() =>
                      void replace(parts.filter((_, candidateIndex) => candidateIndex !== index))
                    }
                  >
                    ×
                  </button>
                </div>
              </li>
            );
          })}
        </ol>
      )}

      <div className="timeline-event-agenda__add">
        <input
          value={draft}
          maxLength={1000}
          disabled={busy || parts.length >= 100}
          aria-label={t(($) => $.common.home.timeline.create.eventDetails.agendaNewItem)}
          placeholder={t(
            ($) => $.common.home.timeline.create.eventDetails.agendaNewItemPlaceholder,
          )}
          onChange={(event) => setDraft(event.currentTarget.value)}
          onKeyDown={(event) => {
            if (event.key === 'Enter') {
              event.preventDefault();
              add();
            }
          }}
        />
        <button
          type="button"
          disabled={busy || parts.length >= 100 || draft.trim().length === 0}
          onClick={add}
        >
          {t(($) => $.common.home.timeline.create.eventDetails.agendaAdd)}
        </button>
      </div>
    </section>
  );
}
