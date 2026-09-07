import {
  Temporal,
  detectDeviceTimeZone,
  type PlainDate,
} from '@dante/time';

import {
  addTimelineDays,
  parseTimelineDate,
  timelineDateKey,
} from './timeline-temporal';
import type { TimelineEvent, TimelineGroup } from './timeline-types';

const TIMELINE_TEST_MODE = 'test';
const TIMELINE_PROTOTYPE_ANCHOR = parseTimelineDate('2026-08-04');
const TIMELINE_PROTOTYPE_NOW_MINUTE_VALUE = 14 * 60 + 20;

export function timelinePrototypeFixturesEnabled(mode: string): boolean {
  return mode === TIMELINE_TEST_MODE;
}

const PROTOTYPE_GROUPS: readonly TimelineGroup[] = [
  { id: 'focus', label: 'Focus / lavoro profondo', tone: 'focus' },
  { id: 'riunioni', label: 'Riunioni', tone: 'meeting' },
  { id: 'salute', label: 'Salute', tone: 'health' },
  { id: 'creativita', label: 'Creatività', tone: 'creative' },
  { id: 'personale', label: 'Personale', tone: 'personal' },
  { id: 'urgenze', label: 'Urgenze', tone: 'urgent' },
];

export function timelinePrototypeGroupsForMode(
  mode: string = import.meta.env.MODE,
): readonly TimelineGroup[] {
  return timelinePrototypeFixturesEnabled(mode)
    ? PROTOTYPE_GROUPS.map((group) => ({ ...group }))
    : [];
}

export const TIMELINE_GROUPS: readonly TimelineGroup[] =
  timelinePrototypeGroupsForMode();

export const TIMELINE_PROTOTYPE_EVENTS: Readonly<
  Record<string, readonly TimelineEvent[]>
> = {
  '2026-08-04': [
    {
      id: '1',
      startMinute: 8 * 60,
      endMinute: 8 * 60 + 30,
      title: 'Routine mattutina',
      groupId: 'personale',
      meta: 'Casa',
    },
    {
      id: '2',
      startMinute: 9 * 60,
      endMinute: 11 * 60,
      title: 'Redesign LifeOS — sessione focus',
      groupId: 'focus',
      meta: 'Progetto LifeOS',
      subitems: [
        'Rivedi layout Home',
        'Verifica componenti',
        'Aggiorna note UX',
      ],
    },
    {
      id: '3',
      startMinute: 9 * 60 + 30,
      endMinute: 10 * 60 + 15,
      title: 'Team sync',
      groupId: 'riunioni',
      meta: 'Google Meet',
    },
    {
      id: '4',
      startMinute: 11 * 60 + 45,
      endMinute: 12 * 60 + 30,
      title: 'Call cliente — revisione onboarding',
      groupId: 'riunioni',
      meta: 'Cliente · Preparazione',
    },
    {
      id: '5',
      startMinute: 12 * 60 + 30,
      endMinute: 13 * 60 + 15,
      title: 'Pausa pranzo',
      groupId: 'personale',
      meta: 'Ricarica',
    },
    {
      id: '6',
      startMinute: 13 * 60 + 15,
      endMinute: 14 * 60,
      title: 'Allenamento — mobilità',
      groupId: 'salute',
      meta: '20 min',
    },
    {
      id: '7',
      startMinute: 14 * 60,
      endMinute: 15 * 60,
      title: 'Studio — grammatica avanzata',
      groupId: 'focus',
      meta: 'Certificazione B2',
    },
    {
      id: '8',
      startMinute: 14 * 60 + 30,
      endMinute: 15 * 60 + 15,
      title: 'Revisione concept',
      groupId: 'creativita',
      meta: 'Nuove funzionalità',
    },
    {
      id: '12',
      startMinute: 14 * 60 + 45,
      endMinute: 15 * 60,
      title: 'Promemoria',
      groupId: 'personale',
      meta: 'Entro oggi',
    },
    {
      id: '9',
      startMinute: 15 * 60 + 15,
      endMinute: 16 * 60 + 15,
      title: 'Ideazione concept — nuove funzionalità',
      groupId: 'creativita',
      meta: 'Sessione libera',
    },
    {
      id: '10',
      startMinute: 16 * 60 + 30,
      endMinute: 17 * 60 + 30,
      title: 'Scrittura documentazione',
      groupId: 'focus',
      meta: 'Specifiche e linee guida',
    },
    {
      id: '11',
      startMinute: 17 * 60 + 30,
      endMinute: 18 * 60,
      title: 'Debrief attività & next steps',
      groupId: 'riunioni',
      meta: 'Chiusura giornata',
    },
    {
      id: '13',
      startMinute: 18 * 60 + 30,
      endMinute: 19 * 60 + 30,
      title: 'Allenamento — corsa',
      groupId: 'salute',
      meta: 'Circuito parco',
      subitems: ['Riscaldamento', 'Corsa intensa', 'Recupero', 'Stretching'],
    },
  ],
  '2026-08-05': [
    {
      id: '101',
      startMinute: 9 * 60,
      endMinute: 10 * 60,
      title: 'Standup settimanale',
      groupId: 'riunioni',
      meta: 'Google Meet',
    },
    {
      id: '102',
      startMinute: 10 * 60 + 30,
      endMinute: 12 * 60,
      title: 'Lavoro su proposta cliente',
      groupId: 'focus',
      meta: 'Nuovo cliente',
    },
    {
      id: '103',
      startMinute: 14 * 60,
      endMinute: 15 * 60,
      title: 'Palestra',
      groupId: 'salute',
      meta: 'Sala pesi',
    },
    {
      id: '104',
      startMinute: 16 * 60,
      endMinute: 16 * 60 + 30,
      title: 'Lettura e pianificazione',
      groupId: 'personale',
      meta: 'Obiettivi',
    },
  ],
  '2026-08-06': [
    {
      id: '201',
      startMinute: 8 * 60 + 30,
      endMinute: 10 * 60,
      title: 'Focus — implementazione',
      groupId: 'focus',
      meta: 'LifeOS',
    },
    {
      id: '202',
      startMinute: 11 * 60,
      endMinute: 11 * 60 + 45,
      title: 'Review tecnica',
      groupId: 'riunioni',
      meta: 'Team',
    },
    {
      id: '203',
      startMinute: 15 * 60,
      endMinute: 16 * 60,
      title: 'Fotografia — selezione scatti',
      groupId: 'creativita',
      meta: 'Archivio',
    },
  ],
  '2026-08-07': [
    {
      id: '301',
      startMinute: 9 * 60,
      endMinute: 11 * 60,
      title: 'Deep work',
      groupId: 'focus',
      meta: 'Progetto',
    },
    {
      id: '302',
      startMinute: 18 * 60,
      endMinute: 19 * 60,
      title: 'Camminata',
      groupId: 'salute',
      meta: 'Outdoor',
    },
  ],
};

function cloneTimelineEvent(event: TimelineEvent): TimelineEvent {
  const base = {
    id: event.id,
    startMinute: event.startMinute,
    endMinute: event.endMinute,
    title: event.title,
    groupId: event.groupId,
  };

  const withMeta = event.meta ? { ...base, meta: event.meta } : base;
  return event.subitems
    ? { ...withMeta, subitems: [...event.subitems] }
    : withMeta;
}

export function createTimelinePrototypeEventsForDate(
  dateKey: string,
  mode: string = import.meta.env.MODE,
): readonly TimelineEvent[] {
  if (!timelinePrototypeFixturesEnabled(mode)) {
    return [];
  }

  const configured = TIMELINE_PROTOTYPE_EVENTS[dateKey];
  if (configured) {
    return configured.map(cloneTimelineEvent);
  }

  return [
    {
      id: `gen-${dateKey}-1`,
      startMinute: 9 * 60,
      endMinute: 10 * 60 + 30,
      title: 'Focus programmato',
      groupId: 'focus',
      meta: 'Pianificazione',
    },
    {
      id: `gen-${dateKey}-2`,
      startMinute: 14 * 60,
      endMinute: 14 * 60 + 45,
      title: 'Attività personale',
      groupId: 'personale',
      meta: 'Promemoria',
    },
  ];
}

export function createTimelinePrototypeStore(
  anchorDate: PlainDate = TIMELINE_PROTOTYPE_TODAY,
  mode: string = import.meta.env.MODE,
): Readonly<Record<string, readonly TimelineEvent[]>> {
  if (!timelinePrototypeFixturesEnabled(mode)) {
    return {};
  }

  return Object.fromEntries(
    Object.entries(TIMELINE_PROTOTYPE_EVENTS).map(([sourceKey, events]) => {
      const sourceDate = parseTimelineDate(sourceKey);
      const dayOffset = TIMELINE_PROTOTYPE_ANCHOR.until(sourceDate).days;
      const targetKey = timelineDateKey(addTimelineDays(anchorDate, dayOffset));
      return [targetKey, events.map(cloneTimelineEvent)];
    }),
  );
}

function currentTimelineClock(): Readonly<{
  today: PlainDate;
  nowMinute: number;
}> {
  if (timelinePrototypeFixturesEnabled(import.meta.env.MODE)) {
    return {
      today: TIMELINE_PROTOTYPE_ANCHOR,
      nowMinute: TIMELINE_PROTOTYPE_NOW_MINUTE_VALUE,
    };
  }

  const now = Temporal.Now.zonedDateTimeISO(detectDeviceTimeZone());
  return {
    today: now.toPlainDate(),
    nowMinute: now.hour * 60 + now.minute,
  };
}

const TIMELINE_CLOCK = currentTimelineClock();

/**
 * Legacy T1 export names are retained to avoid coupling accepted interaction
 * tests to the production clock. Outside explicit test mode these values come
 * from the real device-zone wall clock and never from the frozen prototype.
 */
export const TIMELINE_PROTOTYPE_TODAY = TIMELINE_CLOCK.today;
export const TIMELINE_PROTOTYPE_NOW_MINUTE = TIMELINE_CLOCK.nowMinute;
