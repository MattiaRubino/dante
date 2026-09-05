import { access } from './access';

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
} as const;

type DeepStringResource<T> = T extends string
  ? string
  : { readonly [K in keyof T]: DeepStringResource<T[K]> };

export type CommonResource = DeepStringResource<typeof common>;
