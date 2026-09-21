import { Temporal } from '@dante/time';
import { useCallback, useEffect, useMemo, useState } from 'react';

import {
  createRemoteTemporalEventDataSource,
  TemporalEventRemoteError,
} from '../../../temporal/remote-event-data-source';
import type { TemporalPostponedEventRecord } from '../../../temporal/event-data-source';
import type { TemporalSchedulePlacementInput } from '../../../temporal/schedule-data-source';
import { subscribeTemporalTimelineInvalidation } from '../../../temporal/timeline-invalidation';
import type { LifeArea } from '../../../temporal/remote-organization';

type PlacementKind = 'timed' | 'all-day' | 'coarse';

function localDateTime(date: string, time: string) {
  return Temporal.PlainDateTime.from(`${date}T${time}`);
}

function placementFromForm(
  kind: PlacementKind,
  date: string,
  startsAt: string,
  endsAt: string,
  period: 'morning' | 'afternoon' | 'evening',
): TemporalSchedulePlacementInput {
  const day = Temporal.PlainDate.from(date);
  if (kind === 'all-day') {
    return {
      kind: 'date-span',
      startDate: day,
      endDateExclusive: day.add({ days: 1 }),
    };
  }
  if (kind === 'coarse') {
    return { kind: 'coarse-local-period', localDate: day, period };
  }
  const start = localDateTime(date, startsAt);
  const end = localDateTime(date, endsAt);
  if (Temporal.PlainDateTime.compare(start, end) >= 0) {
    throw new RangeError('L’orario di fine deve essere successivo all’inizio.');
  }
  return {
    kind: 'floating-local-interval',
    startsLocalAt: start,
    endsLocalAt: end,
  };
}

export function TimelinePostponedEventsPanel({
  enabled,
  areas,
}: Readonly<{
  enabled: boolean;
  areas: readonly LifeArea[];
}>) {
  const source = useMemo(() => createRemoteTemporalEventDataSource(), []);
  const [items, setItems] = useState<readonly TemporalPostponedEventRecord[]>(
    [],
  );
  const [open, setOpen] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);
  const [date, setDate] = useState(() =>
    Temporal.Now.plainDateISO().toString(),
  );
  const [kind, setKind] = useState<PlacementKind>('timed');
  const [startsAt, setStartsAt] = useState('09:00');
  const [endsAt, setEndsAt] = useState('10:00');
  const [period, setPeriod] = useState<'morning' | 'afternoon' | 'evening'>(
    'morning',
  );
  const [notice, setNotice] = useState<string | null>(null);
  const [pending, setPending] = useState(false);
  const refresh = useCallback(() => {
    if (!enabled) return;
    void source.listPostponedEvents().then(setItems, (reason: unknown) => {
      setNotice(
        reason instanceof Error
          ? reason.message
          : 'Eventi posticipati non disponibili.',
      );
    });
  }, [enabled, source]);

  useEffect(() => {
    refresh();
    return subscribeTemporalTimelineInvalidation(refresh);
  }, [refresh]);

  const selectedItem =
    items.find((item) => item.scheduleRef === selected) ?? null;
  const areaName = (item: TemporalPostponedEventRecord) => {
    if (item.lifeAreaRef === null) return 'Senza Life Area';
    return (
      areas.find((area) => area.ref === item.lifeAreaRef)?.name ??
      'Life Area non disponibile'
    );
  };
  const replan = () => {
    if (selectedItem === null || pending) return;
    setPending(true);
    setNotice(null);
    try {
      const placement = placementFromForm(kind, date, startsAt, endsAt, period);
      void source
        .replanPostponedEvent({
          eventRef: selectedItem.eventRef,
          scheduleRef: selectedItem.scheduleRef,
          unscheduleOperationId: selectedItem.unscheduleOperationId,
          operationId: `event-replan:${crypto.randomUUID()}`,
          placement,
        })
        .then(
          () => {
            setSelected(null);
            setNotice('Evento ripianificato.');
            refresh();
          },
          (reason: unknown) => {
            const conflict =
              reason instanceof TemporalEventRemoteError &&
              reason.status === 409;
            setNotice(
              conflict
                ? 'L’Evento è cambiato: aggiorna e riprova.'
                : reason instanceof Error
                  ? reason.message
                  : 'Ripianificazione non disponibile.',
            );
            refresh();
          },
        )
        .finally(() => setPending(false));
    } catch (reason) {
      setPending(false);
      setNotice(
        reason instanceof Error
          ? reason.message
          : 'Dati di ripianificazione non validi.',
      );
    }
  };

  if (!enabled) return null;
  return (
    <aside className="timeline-postponed" aria-label="Eventi posticipati">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
      >
        Eventi posticipati{items.length ? ` (${items.length})` : ''}
      </button>
      {open && (
        <section>
          {notice && <p role="status">{notice}</p>}
          {!items.length && <p>Nessun Evento posticipato.</p>}
          <ul>
            {items.map((item) => (
              <li key={item.scheduleRef}>
                <button
                  type="button"
                  onClick={() => setSelected(item.scheduleRef)}
                  aria-pressed={selected === item.scheduleRef}
                >
                  {item.title} · {areaName(item)} · da collocare
                </button>
              </li>
            ))}
          </ul>
          {selectedItem && (
            <form
              onSubmit={(event) => {
                event.preventDefault();
                replan();
              }}
            >
              <h3>Ripianifica “{selectedItem.title}”</h3>
              <label>
                Collocazione{' '}
                <select
                  value={kind}
                  onChange={(event) =>
                    setKind(event.target.value as PlacementKind)
                  }
                  disabled={pending}
                >
                  <option value="timed">Orario</option>
                  <option value="all-day">Tutto il giorno</option>
                  <option value="coarse">Fascia</option>
                </select>
              </label>
              <label>
                Data{' '}
                <input
                  type="date"
                  value={date}
                  onChange={(event) => setDate(event.target.value)}
                  required
                  disabled={pending}
                />
              </label>
              {kind === 'timed' && (
                <>
                  <label>
                    Inizio{' '}
                    <input
                      type="time"
                      value={startsAt}
                      onChange={(event) => setStartsAt(event.target.value)}
                      required
                      disabled={pending}
                    />
                  </label>
                  <label>
                    Fine{' '}
                    <input
                      type="time"
                      value={endsAt}
                      onChange={(event) => setEndsAt(event.target.value)}
                      required
                      disabled={pending}
                    />
                  </label>
                </>
              )}
              {kind === 'coarse' && (
                <label>
                  Fascia{' '}
                  <select
                    value={period}
                    onChange={(event) =>
                      setPeriod(event.target.value as typeof period)
                    }
                    disabled={pending}
                  >
                    <option value="morning">Mattina</option>
                    <option value="afternoon">Pomeriggio</option>
                    <option value="evening">Sera</option>
                  </select>
                </label>
              )}
              <button type="submit" disabled={pending}>
                Ripianifica
              </button>
            </form>
          )}
        </section>
      )}
    </aside>
  );
}
