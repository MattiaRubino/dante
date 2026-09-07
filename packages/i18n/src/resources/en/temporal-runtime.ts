import type { TemporalRuntimeResource } from '../it/temporal-runtime';

export const temporalRuntime = {
  timeline: {
    loading: 'Loading timeline…',
    errorTitle: 'Timeline unavailable',
    errorDescription:
      'DANTE cannot read temporal data right now. No fake data was shown in its place.',
    retry: 'Try again',
  },
} as const satisfies TemporalRuntimeResource;
