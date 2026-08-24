import type { CommonResource } from '../it/common';

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
} as const satisfies CommonResource;
