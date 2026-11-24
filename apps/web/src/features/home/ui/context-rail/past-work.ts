import { Temporal, detectDeviceTimeZone } from '@dante/time';

import { createWebFetch } from '../../../../platform/api/web-fetch';
import { createRemoteTemporalTimelineDataSource } from '../../../temporal/remote-timeline-read';
import type { TemporalTimelineScheduledItem } from '../../../temporal/timeline-read';

export const PAST_WORK_OPEN = 'dante:open-past-timeline-item';
export const PAST_WORK_PAGE_DAYS = 62;

export type PastWorkItem = Readonly<{
  item: TemporalTimelineScheduledItem;
  endedAt: string;
  label: string;
}>;

export type PastWorkCursor = Readonly<{
  endLocalAt: string;
  scheduleRef: string;
}>;

export type PastWorkPage = Readonly<{
  items: readonly PastWorkItem[];
  next: PastWorkCursor | null;
}>;

type Candidate = Readonly<{
  schedule_ref: string;
  end_local_at: string;
  view_date: string;
}>;

/** The server selects accepted placements before the browser reads their canonical cards. */
export async function loadPastWorkCursorPage(
  cursor: PastWorkCursor | null,
  signal?: AbortSignal,
): Promise<PastWorkPage> {
  const params = new URLSearchParams({
    limit: '40',
    view_zone_id: detectDeviceTimeZone(),
  });
  if (cursor) {
    params.set('before_end_local_at', cursor.endLocalAt);
    params.set('before_schedule_ref', cursor.scheduleRef);
  }
  const response = await createWebFetch(globalThis.fetch)(
    `/api/v1/temporal/home/chronology-candidates?${params}`,
    signal ? { signal } : undefined,
  );
  if (!response.ok) throw new Error(`Cronologia: HTTP ${response.status}`);
  const body: unknown = await response.json();
  if (!body || typeof body !== 'object' || !('items' in body))
    throw new Error('Risposta Cronologia non valida.');
  const page = body as {
    items: unknown;
    next_end_local_at?: unknown;
    next_schedule_ref?: unknown;
  };
  if (!Array.isArray(page.items) || page.items.length > 40)
    throw new Error('Risposta Cronologia non valida.');
  const candidates: Candidate[] = page.items.map((raw: unknown) => {
    if (!raw || typeof raw !== 'object')
      throw new Error('Elemento Cronologia non valido.');
    const item = raw as Partial<Candidate>;
    if (
      typeof item.schedule_ref !== 'string' ||
      typeof item.end_local_at !== 'string' ||
      typeof item.view_date !== 'string'
    )
      throw new Error('Elemento Cronologia non valido.');
    Temporal.PlainDate.from(item.view_date);
    return item as Candidate;
  });
  const next =
    page.next_end_local_at === null && page.next_schedule_ref === null
      ? null
      : typeof page.next_end_local_at === 'string' &&
          typeof page.next_schedule_ref === 'string'
        ? {
            endLocalAt: page.next_end_local_at,
            scheduleRef: page.next_schedule_ref,
          }
        : (() => {
            throw new Error('Cursore Cronologia non valido.');
          })();
  const groups = new Map<string, Set<string>>();
  for (const candidate of candidates) {
    const date = Temporal.PlainDate.from(candidate.view_date);
    const existing = [...groups.keys()].find((endKey) => {
      const end = Temporal.PlainDate.from(endKey);
      return (
        Temporal.PlainDate.compare(date, end) < 0 &&
        Temporal.PlainDate.compare(
          date,
          end.subtract({ days: PAST_WORK_PAGE_DAYS }),
        ) >= 0
      );
    });
    const endKey = existing ?? date.add({ days: 1 }).toString();
    groups.set(
      endKey,
      new Set([...(groups.get(endKey) ?? []), candidate.schedule_ref]),
    );
  }
  const pages = await Promise.all(
    [...groups].map(async ([endKey, refs]) =>
      (await loadPastWorkPage(endKey, signal)).filter(({ item }) =>
        refs.has(item.scheduleRef),
      ),
    ),
  );
  const found = new Map(
    pages.flat().map((entry) => [entry.item.scheduleRef, entry]),
  );
  return {
    items: candidates.flatMap((candidate) => {
      const item = found.get(candidate.schedule_ref);
      return item ? [item] : [];
    }),
    next,
  };
}

/** A page is a bounded read of the same accepted placements as the Timeline. */
export async function loadPastWorkPage(
  endDateExclusive: string,
  signal?: AbortSignal,
): Promise<readonly PastWorkItem[]> {
  const end = Temporal.PlainDate.from(endDateExclusive);
  const zoneId = detectDeviceTimeZone();
  const window = await createRemoteTemporalTimelineDataSource().loadWindow(
    {
      startDate: end.subtract({ days: PAST_WORK_PAGE_DAYS }).toString(),
      endDateExclusive,
      viewZoneId: zoneId,
    },
    signal,
  );
  if (window.kind === 'empty') return [];
  const now = Temporal.Now.instant();
  const localNow = now.toZonedDateTimeISO(zoneId).toPlainDateTime();
  const today = localNow.toPlainDate();
  const items: PastWorkItem[] = [];
  for (const item of window.items) {
    if (item.kind === 'expected_occurrence') continue;
    let endKey: string;
    let label: string;
    if (item.temporalForm === 'date-span') {
      if (Temporal.PlainDate.compare(item.endDateExclusive, today) > 0)
        continue;
      endKey = `${item.endDateExclusive.toString()}T00:00`;
      label = `Tutto il giorno · ${item.startDate.toString()}–${item.endDateExclusive.subtract({ days: 1 }).toString()}`;
    } else if (item.temporalForm === 'coarse-local-period') {
      if (Temporal.PlainDate.compare(item.localDate, today) >= 0) continue;
      endKey = `${item.localDate.toString()}T23:59`;
      label = `${item.period === 'morning' ? 'Mattina' : item.period === 'afternoon' ? 'Pomeriggio' : 'Sera'} · ${item.localDate.toString()}`;
    } else {
      const start =
        item.temporalForm === 'floating-local'
          ? item.startsLocalAt
          : item.displayStartsLocalAt;
      const finished =
        item.temporalForm === 'floating-local'
          ? item.endsLocalAt
          : item.displayEndsLocalAt;
      if (Temporal.PlainDateTime.compare(finished, localNow) > 0) continue;
      endKey = finished.toString();
      label = `${start.toPlainTime().toString({ smallestUnit: 'minute' })}–${finished.toPlainTime().toString({ smallestUnit: 'minute' })} · ${start.toPlainDate().toString()}`;
    }
    items.push({ item, endedAt: endKey, label });
  }
  return items.sort(
    (a, b) =>
      b.endedAt.localeCompare(a.endedAt) ||
      a.item.scheduleRef.localeCompare(b.item.scheduleRef),
  );
}

export function openPastWork(
  item: TemporalTimelineScheduledItem,
  opener: HTMLElement,
) {
  window.dispatchEvent(
    new CustomEvent(PAST_WORK_OPEN, { detail: { item, opener } }),
  );
}
