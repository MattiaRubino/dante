export const worldFocus = {
  kicker: 'Mondo',
  back: 'Torna indietro',
  mainLabel: 'Mondo {{world}}',
  canvasLabel: 'Spazio del Mondo {{world}}',
  lens: {
    label: 'Contesto del Mondo',
    timeLabel: 'Periodo',
    presets: {
      last7Days: '7 giorni',
      last30Days: '30 giorni',
      last90Days: '90 giorni',
      lastYear: '1 anno',
      allTime: 'Tutto',
    },
  },
  states: {
    loading: 'Caricamento del Mondo {{world}}',
    error: 'Impossibile aprire il Mondo {{world}}',
    unavailable: 'Mondo {{world}} non disponibile',
    routeErrorTitle: 'Impossibile aprire questo Mondo',
    routeErrorBody:
      'Si è verificato un errore inatteso. Puoi riprovare senza esporre dettagli tecnici.',
    retry: 'Riprova',
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
