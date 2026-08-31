export const WORLD_FOCUS_VISUAL_VERSION = 'wf-v2-candidate' as const;

export const WORLD_FOCUS_VISUAL_LAYER = Object.freeze({
  ambient: 'ambient',
  coronaFallback: 'corona-fallback',
  coronaEnergy: 'corona-energy',
  coronaReference: 'corona-reference',
} as const);

export type WorldFocusVisualLayer =
  (typeof WORLD_FOCUS_VISUAL_LAYER)[keyof typeof WORLD_FOCUS_VISUAL_LAYER];
