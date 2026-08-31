export const WORLD_FOCUS_VISUAL_VERSION = 'wf-v1' as const;

export const WORLD_FOCUS_VISUAL_LAYER = Object.freeze({
  ambient: 'ambient',
  coronaField: 'corona-field',
  coronaEnergy: 'corona-energy',
  coronaGeometry: 'corona-geometry',
  coronaParticles: 'corona-particles',
} as const);

export type WorldFocusVisualLayer =
  (typeof WORLD_FOCUS_VISUAL_LAYER)[keyof typeof WORLD_FOCUS_VISUAL_LAYER];
