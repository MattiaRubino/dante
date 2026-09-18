import { access } from './access';
import { home } from './home';
import { shell } from './shell';
import { temporalRuntime } from './temporal-runtime';
import { worldFocus } from './world-focus';

const homeWithB02D = {
  ...home,
  timeline: {
    ...home.timeline,
    create: {
      ...home.timeline.create,
      eventDetails: {
        ...home.timeline.create.eventDetails,
        agendaSave: 'Salva',
        agendaCancel: 'Annulla',
      },
    },
    detail: {
      ...home.timeline.detail,
      unschedule: 'Riporta nel Planning Tray',
      unscheduling: 'Ritorno in corso…',
      eventPostpone: 'Posticipa / data da definire',
      eventPostponing: 'Aggiornamento in corso…',
    },
    feedback: {
      ...home.timeline.feedback,
      scheduleRevisionUpdated:
        'Pianificazione aggiornata. La Timeline sta rileggendo lo stato corrente.',
      scheduleRevisionConflict:
        'La pianificazione è cambiata altrove. Nessuna modifica è stata sovrascritta.',
      scheduleRevisionUnavailable:
        'Impossibile aggiornare questa pianificazione in sicurezza.',
      scheduleUndoAvailable: 'Modifica salvata.',
      scheduleUnscheduled:
        'Collocazione rimossa dalla Timeline. Lo stato corrente si sta aggiornando.',
      scheduleUnscheduleConflict:
        'La pianificazione è cambiata altrove. Non è stata rimossa.',
      scheduleUnscheduleUnavailable:
        'Impossibile rimuovere questa collocazione in sicurezza.',
      scheduleUndoUpdated: 'Modifica precedente della pianificazione ripristinata.',
      scheduleUndoConflict:
        'Una modifica successiva impedisce l’annullamento. Nulla è stato sovrascritto.',
      scheduleUndoUnavailable:
        'Impossibile annullare questa modifica della pianificazione.',
      eventAgendaConflict:
        'L’Agenda è cambiata altrove. È stata ricaricata la versione corrente senza sovrascrivere nulla.',
      eventAgendaUnavailable:
        'Impossibile aggiornare l’Agenda in sicurezza. È stata ricaricata la versione corrente.',
    },
  },
} as const;

export const common = {
  runtime: {
    labels: {
      route: 'Percorso',
      purpose: 'Scopo',
    },
    web: {
      eyebrow: 'DANTE Web',
      title: 'Frontend pronto',
      description:
        "Scaffold diagnostico minimo con React, Vite e TanStack Router. L'interfaccia prodotto non è ancora materializzata in questo checkpoint.",
      purpose: 'Scaffold diagnostico FM-03',
    },
    mobile: {
      eyebrow: 'DANTE MOBILE',
      title: 'Runtime nativo pronto',
      description:
        "Scaffold diagnostico minimo con Expo SDK 57, React Native 0.86 ed Expo Router. L'interfaccia prodotto non è ancora materializzata in questo checkpoint.",
      purpose: 'Scaffold diagnostico FM-04',
    },
  },
  gesture: {
    title: 'Test gesto',
    description:
      'Tocca questa superficie per verificare Gesture Handler + Reanimated.',
  },
  observability: {
    failure: {
      eyebrow: 'DANTE',
      title: 'Qualcosa non ha funzionato',
      description:
        "L'interfaccia ha incontrato un errore inatteso. Puoi riprovare senza perdere il controllo della sessione oppure ricaricare la pagina.",
      retry: 'Riprova',
      reload: 'Ricarica pagina',
    },
  },
  access,
  shell,
  home: homeWithB02D,
  temporalRuntime,
  worldFocus,
} as const;

type DeepStringResource<T> = T extends string
  ? string
  : { readonly [K in keyof T]: DeepStringResource<T[K]> };

export type CommonResource = DeepStringResource<typeof common>;
