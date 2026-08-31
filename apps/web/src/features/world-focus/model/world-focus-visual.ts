export const WORLD_FOCUS_VISUAL_VERSION = 'wf-v4-candidate' as const;

export const WORLD_FOCUS_VISUAL_LAYER = Object.freeze({
  ambient: 'ambient',
  coronaEnergy: 'corona-energy',
  coronaReference: 'corona-reference',
} as const);

export type WorldFocusVisualLayer =
  (typeof WORLD_FOCUS_VISUAL_LAYER)[keyof typeof WORLD_FOCUS_VISUAL_LAYER];
