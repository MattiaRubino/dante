export type TemporalCreateProductCopy = Readonly<{
  typeLabel: string;
  advanced: string;
  hideAdvanced: string;
  activity: Readonly<{
    placement: string;
    timed: string;
    allDay: string;
    toPlace: string;
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
  activity: Object.freeze({
    placement: 'Collocazione',
    timed: 'Orario',
    allDay: 'Tutto il giorno',
    toPlace: 'Da collocare',
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
    repeatCustom: 'Personalizza…',
  }),
  futureTypesHint: 'Altri tipi potranno essere aggiunti qui senza cambiare il flusso.',
});

const EN: TemporalCreateProductCopy = Object.freeze({
  typeLabel: 'Type',
  advanced: 'Advanced options',
  hideAdvanced: 'Hide advanced options',
  activity: Object.freeze({
    placement: 'Placement',
    timed: 'Timed',
    allDay: 'All day',
    toPlace: 'To place',
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

export function temporalCreateProductCopy(language: string): TemporalCreateProductCopy {
  return language.toLowerCase().startsWith('en') ? EN : IT;
}
