import './timeline-planning-tray-v2.css';

export type TimelinePlanningLocale = 'it' | 'en';

export type TimelinePlanningCopy = Readonly<{
  title: string;
  trigger: string;
  description: string;
  emptyTitle: string;
  emptyBody: string;
  search: string;
  searchPlaceholder: string;
  dragHint: string;
  place: string;
  placeTitle: string;
  date: string;
  time: string;
  duration: string;
  confirmPlace: string;
  cancel: string;
  remove: string;
  removeTitle: string;
  removeBody: string;
  close: string;
  dropHere: string;
  placing: string;
  failed: string;
  splittable: string;
  constraint: Readonly<{
    none: string;
    open: string;
    boundedWindow: string;
    deadline: string;
    preferredWindow: string;
  }>;
}>;

const IT: TimelinePlanningCopy = Object.freeze({
  title: 'Da collocare',
  trigger: 'Apri attività da collocare',
  description:
    'Attività già definite, ma senza uno slot accettato. Trascinale nella Timeline oppure scegli data e ora.',
  emptyTitle: 'Niente da collocare',
  emptyBody:
    'Le attività create senza collocazione compariranno qui, senza essere inventate dentro una fascia oraria.',
  search: 'Cerca attività da collocare',
  searchPlaceholder: 'Cerca…',
  dragHint: 'Trascina nella Timeline',
  place: 'Colloca',
  placeTitle: 'Colloca attività',
  date: 'Data',
  time: 'Ora',
  duration: 'Durata',
  confirmPlace: 'Colloca nella Timeline',
  cancel: 'Annulla',
  remove: 'Elimina',
  removeTitle: 'Eliminare questa attività?',
  removeBody:
    'Verrà rimossa dall’ambiente locale. Non viene simulata alcuna cancellazione backend.',
  close: 'Chiudi attività da collocare',
  dropHere: 'Rilascia qui',
  placing: 'Collocazione…',
  failed: 'Non è stato possibile applicare la collocazione.',
  splittable: 'Divisibile',
  constraint: Object.freeze({
    none: 'Senza vincoli aggiuntivi',
    open: 'Aperta',
    boundedWindow: 'Finestra vincolata',
    deadline: 'Con scadenza',
    preferredWindow: 'Finestra preferita',
  }),
});

const EN: TimelinePlanningCopy = Object.freeze({
  title: 'To place',
  trigger: 'Open activities to place',
  description:
    'Activities that already exist but have no accepted slot. Drag them onto the Timeline or choose a date and time.',
  emptyTitle: 'Nothing to place',
  emptyBody:
    'Activities created without a placement will live here instead of being invented inside a time slot.',
  search: 'Search activities to place',
  searchPlaceholder: 'Search…',
  dragHint: 'Drag onto the Timeline',
  place: 'Place',
  placeTitle: 'Place activity',
  date: 'Date',
  time: 'Time',
  duration: 'Duration',
  confirmPlace: 'Place on Timeline',
  cancel: 'Cancel',
  remove: 'Delete',
  removeTitle: 'Delete this activity?',
  removeBody:
    'It will be removed from the local workspace. No backend deletion is simulated.',
  close: 'Close activities to place',
  dropHere: 'Drop here',
  placing: 'Placing…',
  failed: 'The placement could not be applied.',
  splittable: 'Splittable',
  constraint: Object.freeze({
    none: 'No additional constraint',
    open: 'Open',
    boundedWindow: 'Bounded window',
    deadline: 'Deadline',
    preferredWindow: 'Preferred window',
  }),
});

export function timelinePlanningCopy(language: string): TimelinePlanningCopy {
  return language.toLowerCase().startsWith('en') ? EN : IT;
}
