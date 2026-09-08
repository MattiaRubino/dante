export const temporalRuntime = {
  timeline: {
    loading: 'Caricamento timeline…',
    errorTitle: 'Timeline non disponibile',
    errorDescription:
      'DANTE non riesce a leggere i dati temporali in questo momento. Nessun dato finto è stato mostrato al loro posto.',
    retry: 'Riprova',
  },
} as const;

type DeepStringResource<T> = T extends string
  ? string
  : { readonly [K in keyof T]: DeepStringResource<T[K]> };

export type TemporalRuntimeResource = DeepStringResource<
  typeof temporalRuntime
>;
