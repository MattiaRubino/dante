import type { WorldFocusResource } from '../it/world-focus';

export const worldFocus = {
  kicker: 'World',
  back: 'Go back',
  mainLabel: '{{world}} World',
  canvasLabel: '{{world}} World space',
  states: {
    loading: 'Loading the {{world}} World',
    error: 'Unable to open the {{world}} World',
    unavailable: '{{world}} World unavailable',
    routeErrorTitle: 'Unable to open this World',
    routeErrorBody:
      'An unexpected error occurred. You can retry without exposing technical details.',
    retry: 'Retry',
  },
  surfaces: {
    unavailable: 'This content is unavailable.',
    error: 'Unable to display this content.',
    close: 'Close',
  },
  continuity: {
    title: 'In motion',
    loading: 'Recovering what is in motion',
    partial: 'Some continuity information is unavailable.',
    stale: 'This view is using information that may be out of date.',
    error: 'Unable to recover what is in motion.',
    unavailable: 'What is in motion is unavailable right now.',
    retry: 'Retry',
    states: {
      active: 'Active',
      paused: 'Paused',
      blocked: 'Blocked',
    },
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
