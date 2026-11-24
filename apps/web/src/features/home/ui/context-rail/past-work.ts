import { Temporal, detectDeviceTimeZone } from '@dante/time';

import { createRemoteTemporalTimelineDataSource } from '../../../temporal/remote-timeline-read';
import type { TemporalTimelineScheduledItem } from '../../../temporal/timeline-read';

export const PAST_WORK_OPEN = 'dante:open-past-timeline-item';
export const PAST_WORK_PAGE_DAYS = 62;

export type PastWorkItem = Readonly<{
  item: TemporalTimelineScheduledItem;
  endedAt: string;
  label: string;
}>;

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
