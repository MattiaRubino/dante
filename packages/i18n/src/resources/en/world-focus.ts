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
  dante: {
    invoke: 'Open DANTE',
    invokeForWorld: 'Open DANTE for the {{world}} World',
    worldContext: 'World · {{world}}',
    inputLabel: 'Write a request for DANTE',
    placeholder: 'Ask DANTE…',
    send: 'Send request',
    close: 'Close DANTE',
    conversationTitle: 'Conversation with DANTE',
    maximizeConversation: 'Maximize',
    restoreConversation: 'Restore',
    closeConversation: 'Close DANTE conversation',
    unavailable: 'DANTE is unavailable right now.',
    submissionUnavailable:
      'DANTE is unavailable right now. Your request is still here.',
  },
  customization: {
    invoke: 'Customize composition',
    kicker: 'Composition',
    title: 'Customize {{world}}',
    revision: 'Revision {{revision}}',
    changed: 'Unapplied changes',
    unchanged: 'No changes',
    configuredTitle: 'Chosen composition',
    configuredEmpty: 'No elements have been customized yet.',
    opportunitiesTitle: 'Available in this World',
    opportunitiesLoading: 'Loading composition opportunities',
    opportunitiesError: 'Unable to load composition opportunities.',
    opportunitiesEmpty: 'No other meaningful elements are available right now.',
    retry: 'Retry',
    add: 'Add {{item}}',
    pin: 'Pin',
    unpin: 'Unpin',
    hide: 'Hide',
    show: 'Show',
    moveUp: 'Move up',
    moveDown: 'Move down',
    promote: 'Make prominent',
    restore: 'Restore',
    apply: 'Apply',
    cancel: 'Cancel',
    conflict:
      'The composition changed after customization started. Your changes were not applied.',
    invalid: 'This draft is no longer valid. No changes were applied.',
    moved: '{{item}}, position {{position}} of {{total}}',
    position: '{{item}}, position {{position}} of {{total}}',
    states: {
      pinned: 'Pinned',
      hidden: 'Hidden',
      lead: 'Prominent',
      unavailable: 'Unavailable right now',
    },
    kinds: {
      situation: 'Situation',
      continuity: 'Continuity',
      attention: 'Needs attention',
      next: 'Next',
      comparison: 'Comparison',
      trajectory: 'Trajectory',
      evidenceHistory: 'Evidence and history',
      other: 'Item',
    },
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
  presentation: {
    qualifiers: {
      basis: 'Information quality',
      disclosure: 'Availability',
      effect: 'Operation status',
      sync: 'Synchronization conditions',
    },
    basis: {
      freshness: {
        stale: 'Out of date',
        unknown: 'Freshness unknown',
      },
      validity: {
        superseded: 'Superseded',
        retracted: 'Retracted',
        unresolved: 'Validity unresolved',
      },
      coverage: {
        incomplete: 'Incomplete',
        conflicted: 'Conflicted',
        unknown: 'Coverage unknown',
      },
      material: {
        retired: 'Content retired',
      },
    },
    disclosure: {
      states: {
        restricted: 'Restricted access',
        unavailable: 'Unavailable',
      },
    },
    effect: {
      states: {
        pending: 'Pending',
        ambiguous: 'Ambiguous outcome',
        'partial-real': 'Partially real effect',
        'reconciliation-required': 'Reconciliation required',
        reversed: 'Reversed',
        compensated: 'Compensated',
      },
      revalidationRequired: 'Recheck required before execution',
    },
    sync: {
      offline: 'Offline',
      replayPending: 'Replay pending',
      providerLagging: 'Delivery lagging',
      providerUnknown: 'Delivery unknown',
      timedOut: 'Request timed out',
      timingUnknown: 'Request timing unknown',
    },
    situation: {
      title: 'Situation',
    },
    next: {
      title: 'Next',
    },
    evidenceHistory: {
      title: 'Evidence and history',
      evidence: 'Evidence',
      provenance: 'Provenance',
      integrity: 'Integrity',
      history: 'History',
    },
    attention: {
      title: 'Needs attention',
      resolution: 'Resolution:',
      states: {
        unresolved: 'Unresolved',
        'awaiting-response': 'Awaiting response',
        blocked: 'Blocked',
      },
    },
    comparison: {
      title: 'Comparison',
      basis: 'Basis:',
      modes: {
        difference: 'Difference',
        change: 'Change',
        'trade-off': 'Trade-off',
        'planned-actual': 'Planned vs actual',
      },
    },
    trajectory: {
      title: 'Trajectory',
      missing: 'Missing data',
      axes: {
        time: 'Over time',
        sequence: 'In sequence',
      },
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
