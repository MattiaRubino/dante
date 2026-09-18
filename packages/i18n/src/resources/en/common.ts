import type { CommonResource } from '../it/common';
import { access } from './access';
import { home } from './home';
import { shell } from './shell';
import { temporalRuntime } from './temporal-runtime';
import { worldFocus } from './world-focus';

const homeWithB02D = {
  ...home,
  timeline: {
    ...home.timeline,
    create: {
      ...home.timeline.create,
      eventDetails: {
        ...home.timeline.create.eventDetails,
        agendaSave: 'Save',
        agendaCancel: 'Cancel',
      },
    },
    detail: {
      ...home.timeline.detail,
      unschedule: 'Return to Planning Tray',
      unscheduling: 'Returning…',
      eventPostpone: 'Postpone / date TBD',
      eventPostponing: 'Updating…',
    },
    feedback: {
      ...home.timeline.feedback,
      scheduleRevisionUpdated:
        'Schedule updated. Timeline is reloading the current state.',
      scheduleRevisionConflict:
        'The Schedule changed elsewhere. No change was overwritten.',
      scheduleRevisionUnavailable: 'This Schedule could not be updated safely.',
      scheduleUndoAvailable: 'Change saved.',
      scheduleUnscheduled:
        'Placement removed from Timeline. Current state is reloading.',
      scheduleUnscheduleConflict:
        'The Schedule changed elsewhere. It was not removed.',
      scheduleUnscheduleUnavailable:
        'This placement could not be removed safely.',
      scheduleUndoUpdated: 'Previous Schedule change restored.',
      scheduleUndoConflict:
        'A later Schedule change prevents this undo. Nothing was overwritten.',
      scheduleUndoUnavailable: 'This Schedule change could not be undone.',
      eventAgendaConflict:
        'The Agenda changed elsewhere. The current version was reloaded without overwriting anything.',
      eventAgendaUnavailable:
        'The Agenda could not be updated safely. The current version was reloaded.',
    },
  },
} as const;

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
  shell,
  home: homeWithB02D,
  temporalRuntime,
  worldFocus,
} as const satisfies CommonResource;
