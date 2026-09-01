export const worldFocus = {
  kicker: 'Mondo',
  back: 'Torna indietro',
  mainLabel: 'Mondo {{world}}',
  canvasLabel: 'Spazio del Mondo {{world}}',
  states: {
    loading: 'Caricamento del Mondo {{world}}',
    error: 'Impossibile aprire il Mondo {{world}}',
    unavailable: 'Mondo {{world}} non disponibile',
    routeErrorTitle: 'Impossibile aprire questo Mondo',
    routeErrorBody:
      'Si è verificato un errore inatteso. Puoi riprovare senza esporre dettagli tecnici.',
    retry: 'Riprova',
  },
  surfaces: {
    unavailable: 'Questo contenuto non è disponibile.',
    error: 'Non riesco a mostrare questo contenuto.',
    close: 'Chiudi',
  },
  continuity: {
    title: 'In movimento',
    loading: 'Recupero di ciò che è in movimento',
    partial: 'Alcune informazioni di continuità non sono disponibili.',
    stale: 'Questa vista usa informazioni non aggiornate.',
    error: 'Non riesco a recuperare ciò che è in movimento.',
    unavailable: 'Ciò che è in movimento non è disponibile al momento.',
    retry: 'Riprova',
    states: {
      active: 'Attivo',
      paused: 'In pausa',
      blocked: 'Bloccato',
    },
  },
  worlds: {
    body: {
      label: 'Corpo',
      description: 'La tua base. La tua energia. Il tuo veicolo.',
    },
    music: {
      label: 'Musica',
      description: 'Creatività, ascolto e progetti musicali.',
    },
    travel: {
      label: 'Viaggi',
      description: 'Esperienze, luoghi e prossime partenze.',
    },
    study: {
      label: 'Studio',
      description: 'Apprendimento, competenze e percorsi.',
    },
    finance: {
      label: 'Finanza',
      description: 'Risorse, risparmio e obiettivi economici.',
    },
    relationships: {
      label: 'Relazioni',
      description: 'Persone, legami e tempo condiviso.',
    },
    work: {
      label: 'Lavoro',
      description: 'Progetti, risultati e crescita professionale.',
    },
    growth: {
      label: 'Crescita',
      description: 'Abitudini, consapevolezza e direzione.',
    },
    routine: {
      label: 'Routine',
      description: 'Ritmi, sistemi e consistenza quotidiana.',
    },
    projects: {
      label: 'Progetti',
      description: 'Idee in movimento e prossimi traguardi.',
    },
  },
} as const;

type DeepStringResource<T> = T extends string
  ? string
  : { readonly [K in keyof T]: DeepStringResource<T[K]> };

export type WorldFocusResource = DeepStringResource<typeof worldFocus>;
