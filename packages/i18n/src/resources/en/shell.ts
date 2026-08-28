import type { ShellResource } from '../it/shell';

export const shell = {
  actions: {
    skipToContent: 'Skip to content',
    close: 'Close',
  },
  topbar: {
    brandHomeLabel: 'DANTE — go to Home',
    navigationLabel: 'Primary navigation',
    search: 'Search',
    searchLabel: 'Search DANTE',
    searchShortcut: '/',
    create: 'Create',
    review: 'Review',
    launcher: 'Open launcher',
    account: 'Account',
  },
  destinations: {
    home: {
      label: 'Home',
      description: 'Situation, AI, Worlds, and timeline',
    },
    worlds: {
      label: 'Worlds',
      description: 'Open the dedicated Worlds area',
    },
    today: {
      label: 'Today',
      description: 'Open the dedicated temporal view for today',
    },
    profile: {
      label: 'Profile',
      description: 'Profile identity and information',
    },
    settings: {
      label: 'Settings',
      description: 'DANTE preferences and configuration',
    },
  },
  search: {
    title: 'Search DANTE',
    placeholder: 'Search pages and functions…',
    navigationSection: 'Navigation',
    noResults: 'No local destination matches this search.',
    remoteUnavailable:
      'Search across personal data will be connected when the relevant backend is available.',
  },
  create: {
    kicker: 'Creation',
    title: 'What do you want to create?',
    description:
      'Choose the type. The specific flow will open only when its vertical is ready.',
    menuLabel: 'Create',
    deferred: 'Creation flow is not connected yet',
    items: {
      event: {
        label: 'Event',
        description: 'Put something on the timeline or calendar.',
      },
      task: {
        label: 'Task',
        description: 'Create a commitment or something to do.',
      },
      capture: {
        label: 'Capture',
        description: 'Quickly record a fact, idea, or input.',
      },
    },
  },
  launcher: {
    kicker: 'DANTE',
    title: 'Areas',
    description: 'Quick navigation between available areas.',
    menuLabel: 'DANTE launcher',
  },
  account: {
    title: 'Account',
    menuLabel: 'Account menu',
    identityUnavailable: 'Real identity connects with Access/Auth',
    profile: 'Profile',
    settings: 'Settings',
    language: 'Language',
    languageValue: 'English',
    logout: 'Sign out',
    logoutUnavailable: 'Available when the real session is connected',
  },
  review: {
    legacyHint:
      'Review is a legacy function awaiting reconciliation with Resolution.',
  },
  placeholder: {
    eyebrow: 'DANTE · application area',
    status: 'Shell and routing ready',
    worlds:
      'This is a real navigable destination. The Worlds vertical will be materialized in its dedicated pass without changing the global shell.',
    today:
      'This is a real navigable destination. The Today view will be materialized in its dedicated pass without duplicating the Topbar.',
    profile:
      'The profile page is prepared in the shell; real data and behavior will arrive with the identity/session contract.',
    settings:
      'Settings are prepared in the shell; real preferences will be added by responsibility without simulating persistence.',
  },
} as const satisfies ShellResource;
