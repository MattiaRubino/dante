import type { CommonResource } from '../it/common';
import { access } from './access';

export const common = {
  runtime: {
    labels: {
      route: 'Route',
      purpose: 'Purpose',
    },
    web: {
      eyebrow: 'DANTE Web',
      title: 'Frontend runtime ready',
      description:
        'Minimal React, Vite, and TanStack Router diagnostic scaffold. Product UI is not materialized in this checkpoint.',
      purpose: 'FM-03 diagnostic scaffold',
    },
    mobile: {
      eyebrow: 'DANTE MOBILE',
      title: 'Native runtime ready',
      description:
        'Minimal Expo SDK 57, React Native 0.86, and Expo Router diagnostic scaffold. Product UI is not materialized in this checkpoint.',
      purpose: 'FM-04 diagnostic scaffold',
    },
  },
  gesture: {
    title: 'Gesture probe',
    description: 'Tap this surface to exercise Gesture Handler + Reanimated.',
  },
  observability: {
    failure: {
      eyebrow: 'DANTE',
      title: 'Something went wrong',
      description:
        'The interface encountered an unexpected error. You can retry without giving up control of the session, or reload the page.',
      retry: 'Try again',
      reload: 'Reload page',
    },
  },
  access,
} as const satisfies CommonResource;
