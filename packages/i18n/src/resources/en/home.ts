import type { HomeResource } from '../it/home';

export const home = {
  shell: {
    mainLabel: 'DANTE Home',
  },
  topbar: {
    brandLabel: 'DANTE',
    navigationLabel: 'Primary navigation',
    home: 'Home',
    worlds: 'Worlds',
    today: 'Today',
    search: 'Search',
    create: 'Create',
    review: 'Review',
    launcher: 'Open launcher',
    account: 'Account',
  },
  orientation: {
    title: 'Your situation',
    greeting: 'Good afternoon.',
    dayKicker: 'Today',
    dayTitle: 'Your day',
    dayMeta: 'Sunrise · Sunset',
    nowNext: 'Now and next',
    highlight: 'Highlighted',
    forYou: 'For you',
  },
  ai: {
    label: 'DANTE assistant',
    title: 'DANTE',
    collapse: 'Collapse assistant',
    expand: 'Expand assistant',
  },
  stage: {
    label: 'Central workspace',
    continuity: 'Worlds',
    signals: 'Signals',
  },
  timeline: {
    label: 'Today timeline',
    title: 'Today',
    expand: 'Expand timeline',
    collapse: 'Collapse timeline',
  },
  contextRail: {
    label: 'Context',
    capture: 'Capture',
    resolution: 'Resolution',
  },
} as const satisfies HomeResource;
