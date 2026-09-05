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
  dante: {
    invoke: 'Apri DANTE',
    invokeForWorld: 'Apri DANTE per il Mondo {{world}}',
    worldContext: 'Mondo · {{world}}',
    contextualAction: 'Chiedi a DANTE: {{prompt}}',
    contextChangedBeforeSubmit:
      'Il contesto da cui hai aperto DANTE è cambiato. La richiesta non è stata inviata.',
    contextual: {
      why: 'Perché?',
      compare: 'Confronta',
      continue: 'Continua da qui',
      openSource: 'Apri fonte',
    },
    inputLabel: 'Scrivi una richiesta per DANTE',
    placeholder: 'Chiedi a DANTE…',
    send: 'Invia richiesta',
    close: 'Chiudi DANTE',
    conversationTitle: 'Conversazione con DANTE',
    maximizeConversation: 'Massimizza',
    restoreConversation: 'Ripristina',
    closeConversation: 'Chiudi conversazione DANTE',
    unavailable: 'DANTE non è disponibile al momento.',
    submissionUnavailable:
      'DANTE non è disponibile al momento. La richiesta è rimasta qui.',
    messages: 'Messaggi della conversazione con DANTE',
    you: 'Tu',
    localPending: 'Elaborazione locale della richiesta in corso.',
    localUnavailable: 'La modalità locale non è disponibile al momento.',
    localError: 'Non riesco a completare questa richiesta locale.',
    localCancelled: 'Richiesta annullata. Nessuna risposta è stata aggiunta.',
    localSuperseded:
      'Il contesto del Mondo è cambiato. La risposta precedente non è stata aggiunta.',
    followUpLabel: 'Continua la conversazione',
    followUpPlaceholder: 'Scrivi un seguito…',
    cancelRequest: 'Annulla richiesta',
  },
  customization: {
    invoke: 'Personalizza composizione',
    kicker: 'Composizione',
    title: 'Personalizza {{world}}',
    revision: 'Revisione {{revision}}',
    changed: 'Modifiche non applicate',
    unchanged: 'Nessuna modifica',
    configuredTitle: 'Composizione scelta',
    configuredEmpty: 'Nessun elemento è stato ancora personalizzato.',
    opportunitiesTitle: 'Disponibile in questo Mondo',
    opportunitiesLoading: 'Recupero delle possibilità di composizione',
    opportunitiesError: 'Non riesco a recuperare le possibilità di composizione.',
    opportunitiesEmpty: 'Nessun altro elemento significativo è disponibile adesso.',
    retry: 'Riprova',
    add: 'Aggiungi {{item}}',
    pin: 'Fissa',
    unpin: 'Sblocca',
    hide: 'Nascondi',
    show: 'Mostra',
    moveUp: 'Sposta su',
    moveDown: 'Sposta giù',
    promote: 'Metti in evidenza',
    restore: 'Ripristina',
    apply: 'Applica',
    cancel: 'Annulla',
    conflict:
      'La composizione è cambiata da quando hai iniziato. Le modifiche non sono state applicate.',
    invalid:
      'Questa bozza non è più valida. Nessuna modifica è stata applicata.',
    moved: '{{item}}, posizione {{position}} di {{total}}',
    position: '{{item}}, posizione {{position}} di {{total}}',
    states: {
      pinned: 'Fissato',
      hidden: 'Nascosto',
      lead: 'In evidenza',
      unavailable: 'Non disponibile adesso',
    },
    kinds: {
      situation: 'Situazione',
      continuity: 'Continuità',
      attention: 'Da vedere',
      next: 'Prossimo',
      comparison: 'Confronto',
      trajectory: 'Andamento',
      evidenceHistory: 'Evidenze e cronologia',
      other: 'Elemento',
    },
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
  presentation: {
    qualifiers: {
      basis: 'Qualità delle informazioni',
      disclosure: 'Disponibilità',
      effect: 'Stato dell’operazione',
      sync: 'Condizioni di sincronizzazione',
    },
    basis: {
      freshness: {
        stale: 'Non aggiornato',
        unknown: 'Aggiornamento sconosciuto',
      },
      validity: {
        superseded: 'Superato',
        retracted: 'Ritirato',
        unresolved: 'Validità non risolta',
      },
      coverage: {
        incomplete: 'Incompleto',
        conflicted: 'In conflitto',
        unknown: 'Copertura sconosciuta',
      },
      material: {
        retired: 'Contenuto ritirato',
      },
    },
    disclosure: {
      states: {
        restricted: 'Accesso limitato',
        unavailable: 'Non disponibile',
      },
    },
    effect: {
      states: {
        pending: 'In attesa',
        ambiguous: 'Esito ambiguo',
        'partial-real': 'Effetto parzialmente reale',
        'reconciliation-required': 'Riconciliazione richiesta',
        reversed: 'Reverso',
        compensated: 'Compensato',
      },
      revalidationRequired: 'Ricontrollo richiesto prima di eseguire',
    },
    sync: {
      offline: 'Offline',
      replayPending: 'Riproduzione in attesa',
      providerLagging: 'Consegna in ritardo',
      providerUnknown: 'Consegna sconosciuta',
      timedOut: 'Richiesta scaduta',
      timingUnknown: 'Tempi della richiesta sconosciuti',
    },
    situation: {
      title: 'Situazione',
    },
    next: {
      title: 'Prossimo',
    },
    evidenceHistory: {
      title: 'Evidenze e cronologia',
      evidence: 'Evidenze',
      provenance: 'Provenienza',
      integrity: 'Integrità',
      history: 'Cronologia',
    },
    attention: {
      title: 'Da vedere',
      resolution: 'Risoluzione:',
      states: {
        unresolved: 'Da risolvere',
        'awaiting-response': 'In attesa',
        blocked: 'Bloccato',
      },
    },
    comparison: {
      title: 'Confronto',
      basis: 'Base:',
      modes: {
        difference: 'Differenza',
        change: 'Cambiamento',
        'trade-off': 'Compromesso',
        'planned-actual': 'Pianificato vs reale',
      },
    },
    trajectory: {
      title: 'Andamento',
      missing: 'Dati mancanti',
      axes: {
        time: 'Nel tempo',
        sequence: 'In sequenza',
      },
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
