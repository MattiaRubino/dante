import './temporal-create-product-flow.css';

export type TemporalCreateProductCopy = Readonly<{
  typeLabel: string;
  advanced: string;
  hideAdvanced: string;
  backToQuick: string;
  activity: Readonly<{
    placement: string;
    timed: string;
    allDay: string;
    coarse: string;
    toPlace: string;
    coarsePeriod: string;
    morning: string;
    afternoon: string;
    evening: string;
    timeZone: string;
    dstResolution: string;
    dstReject: string;
    dstEarlier: string;
    dstLater: string;
  }>;
  event: Readonly<{
    when: string;
    timed: string;
    allDay: string;
    end: string;
    repeat: string;
    repeatNever: string;
    repeatDaily: string;
    repeatWeekly: string;
    repeatMonthly: string;
    repeatYearly: string;
    repeatCustom: string;
  }>;
  futureTypesHint: string;
}>;

const IT: TemporalCreateProductCopy = Object.freeze({
  typeLabel: 'Tipo',
  advanced: 'Opzioni avanzate',
  hideAdvanced: 'Nascondi opzioni avanzate',
  backToQuick: 'Torna alla creazione rapida',
  activity: Object.freeze({
    placement: 'Collocazione',
    timed: 'Orario',
    allDay: 'Tutto il giorno',
    coarse: 'Fascia',
    toPlace: 'Da collocare',
    coarsePeriod: 'Fascia',
    morning: 'Mattina',
    afternoon: 'Pomeriggio',
    evening: 'Sera',
    timeZone: 'Fuso orario',
    dstResolution: 'Ora ambigua/non esistente',
    dstReject: 'Chiedi correzione',
    dstEarlier: 'Usa la soluzione precedente',
    dstLater: 'Usa la soluzione successiva',
  }),
  event: Object.freeze({
    when: 'Quando',
    timed: 'Orario',
    allDay: 'Tutto il giorno',
    end: 'Fine',
    repeat: 'Ripeti',
    repeatNever: 'Mai',
    repeatDaily: 'Ogni giorno',
    repeatWeekly: 'Ogni settimana',
    repeatMonthly: 'Ogni mese',
    repeatYearly: 'Ogni anno',
    repeatCustom: 'Personalizzata…',
  }),
  futureTypesHint:
    'Altri tipi potranno essere aggiunti qui senza cambiare il flusso.',
});

const EN: TemporalCreateProductCopy = Object.freeze({
  typeLabel: 'Type',
  advanced: 'Advanced options',
  hideAdvanced: 'Hide advanced options',
  backToQuick: 'Back to quick create',
  activity: Object.freeze({
    placement: 'Placement',
    timed: 'Timed',
    allDay: 'All day',
    coarse: 'Period',
    toPlace: 'To place',
    coarsePeriod: 'Period',
    morning: 'Morning',
    afternoon: 'Afternoon',
    evening: 'Evening',
    timeZone: 'Time zone',
    dstResolution: 'Ambiguous/nonexistent time',
    dstReject: 'Require correction',
    dstEarlier: 'Use earlier resolution',
    dstLater: 'Use later resolution',
  }),
  event: Object.freeze({
    when: 'When',
    timed: 'Timed',
    allDay: 'All day',
    end: 'End',
    repeat: 'Repeat',
    repeatNever: 'Never',
    repeatDaily: 'Every day',
    repeatWeekly: 'Every week',
    repeatMonthly: 'Every month',
    repeatYearly: 'Every year',
    repeatCustom: 'Custom…',
  }),
  futureTypesHint: 'More types can be added here without changing the flow.',
});

export function temporalCreateProductCopy(
  language: string,
): TemporalCreateProductCopy {
  return language.toLowerCase().startsWith('en') ? EN : IT;
}
