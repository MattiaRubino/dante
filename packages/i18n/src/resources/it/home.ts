export const home = {
  shell: { mainLabel: 'Home DANTE' },
  topbar: { brandLabel: 'DANTE', navigationLabel: 'Navigazione principale', home: 'Home', worlds: 'Mondi', today: 'Oggi', search: 'Cerca', create: 'Crea', review: 'Review', launcher: 'Apri launcher', account: 'Account' },
  orientation: { title: 'La tua situazione', greeting: 'Buon pomeriggio.', greetings: { morning: 'Buongiorno', afternoon: 'Buon pomeriggio', evening: 'Buonasera', night: 'Buonanotte' }, dayKicker: 'Oggi', dayTitle: 'La tua giornata', dayMeta: 'Alba · Tramonto', dayContext: { regionLabel: 'Contesto della giornata', routeLabel: 'Percorso della giornata', sunrise: 'Alba', sunset: 'Tramonto', weatherPanelLabel: 'Meteo della settimana', weatherPreview: 'METEO · ANTEPRIMA FRONTEND', closeWeather: 'Chiudi meteo', weatherTitle: 'Meteo', precipitation: 'Precipitazioni', sevenDayForecast: 'Previsioni per sette giorni', maximum: 'massima', minimum: 'minima', degrees: 'gradi', percent: 'percento', sourceDemo: 'Dati demo · provider meteo non collegato', conditions: { clear: 'Sereno', partlyCloudy: 'Parzialmente nuvoloso', cloudy: 'Nuvoloso', rain: 'Pioggia', storm: 'Temporali' } }, nowNext: 'Ora e prossimo', highlight: 'In evidenza', forYou: 'Per te' },
  ai: { label: 'Assistente DANTE', title: 'DANTE', collapse: 'Comprimi assistente', expand: 'Espandi assistente' },
  stage: { label: 'Spazio centrale', continuity: 'Mondi', signals: 'Segnali' },
  timeline: {
    label: 'Timeline di oggi', title: 'Oggi', expand: 'Espandi timeline', collapse: 'Riduci timeline', quickAdd: 'Aggiungi alla timeline',
    create: {
      draft: 'Bozza', title: 'Aggiungi', titleLabel: 'Titolo', titlePlaceholder: 'Cosa vuoi aggiungere?', close: 'Chiudi creazione', discardTitle: 'Scartare questa bozza?', discardBody: 'Le modifiche inserite andranno perse.', continueEditing: 'Continua a modificare', discard: 'Scarta', cancel: 'Annulla', submit: 'Aggiungi', creating: 'Aggiungo…', failure: 'Non è stato possibile applicare la creazione. La bozza è ancora qui.', date: 'Data', start: 'Ora', duration: 'Durata', context: 'Contesto', notes: 'Note', notesPlaceholder: 'Contesto utile, senza trasformarlo in una descrizione obbligatoria…', timeZone: 'Fuso orario',
      kind: { label: 'Tipo', activity: 'Attività', event: 'Evento' },
      timeSemantics: { label: 'Collocazione', timed: 'Orario', allDay: 'Tutto il giorno', unscheduled: 'Da pianificare' },
      timeMode: { label: 'Semantica oraria', floating: 'Ora locale', zoned: 'Fuso orario' },
      details: { show: '+ Dettagli', hide: '− Nascondi dettagli' },
      preview: { unscheduled: 'Da pianificare' },
      validation: { title: 'Inserisci un titolo.', date: 'Inserisci una data valida.', time: 'Inserisci un orario valido.', duration: 'Scegli una durata valida.', timeZone: 'Inserisci un fuso orario IANA valido.', eventPlacement: 'Un evento richiede una collocazione temporale.', generic: 'Controlla questo campo.' }
    },
    weekLabel: 'Settimana visualizzata', todayPrefix: 'Oggi', streamHint: 'Scorri in alto per i giorni precedenti · in basso per i successivi', undo: 'Annulla',
    calendar: { open: 'Apri il calendario', dialogLabel: 'Vai a una data', previousMonth: 'Mese precedente', nextMonth: 'Mese successivo', previousYear: 'Anno precedente', nextYear: 'Anno successivo', previousPeriod: 'Periodo precedente', nextPeriod: 'Periodo successivo', chooseMonth: 'Scegli il mese', chooseYear: "Scegli l'anno", close: 'Chiudi', today: 'Vai a oggi' },
    now: { label: 'Ora', go: 'Torna a ora', visible: 'Ora corrente già visibile' },
    viewOptions: { label: 'Vista e legenda', margins: 'Margini tra impegni', now: 'Ora corrente', milestones: 'Milestone sul percorso', reset: 'Ripristina vista predefinita' },
    groups: { split: 'Separa per gruppi', merge: 'Riunisci nella timeline', reset: 'Ripristina gruppi e focus', reorderHint: 'Trascina per riordinare · Alt+freccia da tastiera', position: 'Posizione {{position}} di {{total}}' },
    zoom: { label: 'Zoom timeline', out: 'Riduci zoom', in: 'Aumenta zoom' },
    timeEditor: { title: 'Modifica orario', start: 'Inizio', end: 'Fine', open: 'Modifica orario di {{title}}', hourPart: '{{label}} ore', minutePart: '{{label}} minuti', increase: 'Aumenta {{label}} di 5 minuti', decrease: 'Riduci {{label}} di 5 minuti', invalid: 'Inserisci un orario valido.', cancel: 'Annulla', save: 'Conferma' },
    detail: { subitems: '{{count}} sotto-attività collegate', aiNote: 'DANTE può usare questo contesto per proporre modifiche, ma le variazioni operative restano confermabili.', close: 'Chiudi', subitemParent: 'Sotto-attività di' },
    event: { hideSubitems: 'Nascondi sotto-attività', showSubitems: '{{count}} sotto-attività · espandi' },
    feedback: { moved: 'Spostato:', movedDay: 'Evento spostato al giorno adiacente.', movedTime: 'Orario evento aggiornato.', timeUpdated: 'Orario aggiornato:', created: 'Creato:', createUndone: 'Creazione annullata.' }
  },
  contextRail: { label: 'Contesto', capture: 'Cattura', resolution: 'Risoluzione' }
} as const;

type DeepStringResource<T> = T extends string ? string : { readonly [K in keyof T]: DeepStringResource<T[K]> };
export type HomeResource = DeepStringResource<typeof home>;
