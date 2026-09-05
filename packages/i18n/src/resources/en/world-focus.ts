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
