export const home = {
  shell: {
    mainLabel: 'Home DANTE',
  },
  topbar: {
    brandLabel: 'DANTE',
    navigationLabel: 'Navigazione principale',
    home: 'Home',
    worlds: 'Mondi',
    today: 'Oggi',
    search: 'Cerca',
    create: 'Crea',
    review: 'Review',
    launcher: 'Apri launcher',
    account: 'Account',
  },
  orientation: {
    title: 'La tua situazione',
    greeting: 'Buon pomeriggio.',
    dayKicker: 'Oggi',
    dayTitle: 'La tua giornata',
    dayMeta: 'Alba · Tramonto',
    nowNext: 'Ora e prossimo',
    highlight: 'In evidenza',
    forYou: 'Per te',
  },
  ai: {
    label: 'Assistente DANTE',
    title: 'DANTE',
    collapse: 'Comprimi assistente',
    expand: 'Espandi assistente',
  },
  stage: {
    label: 'Spazio centrale',
    continuity: 'Mondi',
    signals: 'Segnali',
  },
  timeline: {
    label: 'Timeline di oggi',
    title: 'Oggi',
    expand: 'Espandi timeline',
    collapse: 'Riduci timeline',
  },
  contextRail: {
    label: 'Contesto',
    capture: 'Cattura',
    resolution: 'Risoluzione',
  },
} as const;

type DeepStringResource<T> = T extends string
  ? string
  : { readonly [K in keyof T]: DeepStringResource<T[K]> };

export type HomeResource = DeepStringResource<typeof home>;
