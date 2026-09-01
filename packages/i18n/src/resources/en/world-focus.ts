import type { WorldFocusResource } from '../it/world-focus';

export const worldFocus = {
  kicker: 'World',
  back: 'Go back',
  mainLabel: '{{world}} World',
  canvasLabel: '{{world}} World space',
  lens: {
    label: 'World context',
    timeLabel: 'Time range',
    presets: {
      last7Days: '7 days',
      last30Days: '30 days',
      last90Days: '90 days',
      lastYear: '1 year',
      allTime: 'All time',
    },
  },
  states: {
    loading: 'Loading the {{world}} World',
    error: 'Unable to open the {{world}} World',
    unavailable: '{{world}} World unavailable',
    routeErrorTitle: 'Unable to open this World',
    routeErrorBody:
      'An unexpected error occurred. You can retry without exposing technical details.',
    retry: 'Retry',
  },
  worlds: {
    body: {
      label: 'Body',
      description: 'Your foundation, energy, and physical continuity.',
    },
    music: {
      label: 'Music',
      description: 'Creativity, listening, and music projects.',
    },
    travel: {
      label: 'Travel',
      description: 'Experiences, places, and upcoming journeys.',
    },
    study: {
      label: 'Study',
      description: 'Learning, skills, and ongoing paths.',
    },
    finance: {
      label: 'Finance',
      description: 'Resources, savings, and financial goals.',
    },
    relationships: {
      label: 'Relationships',
      description: 'People, bonds, and time shared.',
    },
    work: {
      label: 'Work',
      description: 'Projects, outcomes, and professional growth.',
    },
    growth: {
      label: 'Growth',
      description: 'Habits, awareness, and direction.',
    },
    routine: {
      label: 'Routine',
      description: 'Rhythms, systems, and daily consistency.',
    },
    projects: {
      label: 'Projects',
      description: 'Ideas in motion and upcoming milestones.',
    },
  },
} as const satisfies WorldFocusResource;
