export const shell = {
  actions: {
    skipToContent: 'Vai al contenuto',
    close: 'Chiudi',
  },
  topbar: {
    brandHomeLabel: 'DANTE — vai alla Home',
    navigationLabel: 'Navigazione principale',
    search: 'Cerca',
    searchLabel: 'Cerca in DANTE',
    searchShortcut: '/',
    create: 'Crea',
    review: 'Review',
    launcher: 'Apri launcher',
    account: 'Account',
  },
  destinations: {
    home: {
      label: 'Home',
      description: 'Situazione, AI, Mondi e timeline',
    },
    worlds: {
      label: 'Mondi',
      description: 'Apri l’area dedicata ai tuoi Mondi',
    },
    today: {
      label: 'Oggi',
      description: 'Apri la vista temporale dedicata a oggi',
    },
    profile: {
      label: 'Profilo',
      description: 'Identità e informazioni del profilo',
    },
    settings: {
      label: 'Impostazioni',
      description: 'Preferenze e configurazione di DANTE',
    },
  },
  search: {
    kicker: 'Ricerca globale',
    title: 'Cerca in DANTE',
    description: 'Raggiungi rapidamente pagine e funzioni disponibili.',
    placeholder: 'Cerca pagine e funzioni…',
    navigationSection: 'Navigazione',
    noResults: 'Nessuna destinazione locale corrisponde alla ricerca.',
    remoteUnavailable:
      'La ricerca nei dati personali sarà collegata quando sarà disponibile il relativo backend.',
  },
  create: {
    kicker: 'Creazione',
    title: 'Cosa vuoi creare?',
    description:
      'Scegli il tipo. Il flusso specifico verrà aperto solo quando il relativo vertical è pronto.',
    menuLabel: 'Crea',
    deferred: 'Flusso di creazione non ancora collegato',
    items: {
      event: {
        label: 'Evento',
        description: 'Inserisci qualcosa nel tempo o nel calendario.',
      },
      task: {
        label: 'Attività',
        description: 'Crea un impegno o una cosa da fare.',
      },
      capture: {
        label: 'Cattura',
        description: 'Registra rapidamente un fatto, un’idea o un input.',
      },
    },
  },
  launcher: {
    kicker: 'DANTE',
    title: 'Aree',
    description: 'Navigazione rapida tra le aree disponibili.',
    menuLabel: 'Launcher DANTE',
  },
  account: {
    title: 'Account',
    menuLabel: 'Menu account',
    identityUnavailable: 'Identità reale collegata con Access/Auth',
    profile: 'Profilo',
    settings: 'Impostazioni',
    language: 'Lingua',
    languageValue: 'Italiano',
    logout: 'Esci',
    logoutUnavailable: 'Disponibile quando la sessione reale sarà collegata',
  },
  review: {
    legacyHint:
      'Review è una funzione legacy in attesa di riconciliazione con Risoluzione.',
  },
  placeholder: {
    eyebrow: 'DANTE · area applicativa',
    status: 'Shell e routing pronti',
    worlds:
      'La destinazione è reale e navigabile. Il vertical Mondi verrà materializzato nel suo pass dedicato senza modificare la shell globale.',
    today:
      'La destinazione è reale e navigabile. La vista Oggi verrà materializzata nel suo pass dedicato senza duplicare la Topbar.',
    profile:
      'La pagina di profilo è predisposta nella shell; dati e comportamento reali arriveranno con il contratto di identità/sessione.',
    settings:
      'La pagina Impostazioni è predisposta nella shell; preferenze reali verranno aggiunte per responsabilità, senza simulare persistenza.',
  },
} as const;

type DeepStringResource<T> = T extends string
  ? string
  : { readonly [K in keyof T]: DeepStringResource<T[K]> };

export type ShellResource = DeepStringResource<typeof shell>;
