export const WORLD_FOCUS_IDS = [
  'body',
  'music',
  'travel',
  'study',
  'finance',
  'relationships',
  'work',
  'growth',
  'routine',
  'projects',
] as const;

export type WorldFocusId = (typeof WORLD_FOCUS_IDS)[number];

export type WorldFocusMotionCharacter =
  | 'pulse'
  | 'orbit'
  | 'drift'
  | 'steady';

export type WorldFocusTexture = 'soft' | 'wave' | 'stellar' | 'grid';

export type WorldFocusThemeProfile = Readonly<{
  motionCharacter: WorldFocusMotionCharacter;
  texture: WorldFocusTexture;
  orbitalDensity: 3 | 4 | 5;
  particleDensity: number;
  ambientIntensity: number;
}>;

export type WorldFocusWorld = Readonly<{
  id: WorldFocusId;
  accent: string;
  theme: WorldFocusThemeProfile;
}>;

/**
 * Synthetic pre-backend presentation catalog.
 *
 * These IDs/colors/theme profiles are frontend fixture identity only. They are
 * not Domain identities, backend DTOs, database rows, persisted World entities,
 * relevance definitions, or authorization boundaries. Later product verticals
 * replace direct fixture use with explicit frontend application/projection
 * boundaries without changing the frozen World Focus shell.
 */
export const WORLD_FOCUS_WORLDS: readonly WorldFocusWorld[] = [
  {
    id: 'body',
    accent: '#b060ff',
    theme: {
      motionCharacter: 'pulse',
      texture: 'soft',
      orbitalDensity: 4,
      particleDensity: 0.56,
      ambientIntensity: 0.72,
    },
  },
  {
    id: 'music',
    accent: '#ffad34',
    theme: {
      motionCharacter: 'pulse',
      texture: 'wave',
      orbitalDensity: 5,
      particleDensity: 0.72,
      ambientIntensity: 0.88,
    },
  },
  {
    id: 'travel',
    accent: '#27d9f5',
    theme: {
      motionCharacter: 'orbit',
      texture: 'stellar',
      orbitalDensity: 5,
      particleDensity: 0.94,
      ambientIntensity: 0.92,
    },
  },
  {
    id: 'study',
    accent: '#4288ff',
    theme: {
      motionCharacter: 'steady',
      texture: 'grid',
      orbitalDensity: 4,
      particleDensity: 0.42,
      ambientIntensity: 0.7,
    },
  },
  {
    id: 'finance',
    accent: '#8bdc47',
    theme: {
      motionCharacter: 'steady',
      texture: 'grid',
      orbitalDensity: 3,
      particleDensity: 0.34,
      ambientIntensity: 0.64,
    },
  },
  {
    id: 'relationships',
    accent: '#d85bff',
    theme: {
      motionCharacter: 'drift',
      texture: 'soft',
      orbitalDensity: 4,
      particleDensity: 0.5,
      ambientIntensity: 0.74,
    },
  },
  {
    id: 'work',
    accent: '#ff9e43',
    theme: {
      motionCharacter: 'steady',
      texture: 'grid',
      orbitalDensity: 3,
      particleDensity: 0.38,
      ambientIntensity: 0.66,
    },
  },
  {
    id: 'growth',
    accent: '#39e6d0',
    theme: {
      motionCharacter: 'drift',
      texture: 'soft',
      orbitalDensity: 4,
      particleDensity: 0.6,
      ambientIntensity: 0.76,
    },
  },
  {
    id: 'routine',
    accent: '#ff6c7c',
    theme: {
      motionCharacter: 'orbit',
      texture: 'wave',
      orbitalDensity: 4,
      particleDensity: 0.46,
      ambientIntensity: 0.7,
    },
  },
  {
    id: 'projects',
    accent: '#8a74ff',
    theme: {
      motionCharacter: 'orbit',
      texture: 'stellar',
      orbitalDensity: 5,
      particleDensity: 0.68,
      ambientIntensity: 0.82,
    },
  },
] as const;

const WORLD_BY_ID = new Map(
  WORLD_FOCUS_WORLDS.map((world) => [world.id, world] as const),
);

const WORLD_ID_BY_LABEL = new Map<string, WorldFocusId>([
  ['corpo', 'body'],
  ['body', 'body'],
  ['musica', 'music'],
  ['music', 'music'],
  ['viaggi', 'travel'],
  ['travel', 'travel'],
  ['studio', 'study'],
  ['study', 'study'],
  ['finanza', 'finance'],
  ['finance', 'finance'],
  ['relazioni', 'relationships'],
  ['relationships', 'relationships'],
  ['lavoro', 'work'],
  ['work', 'work'],
  ['crescita', 'growth'],
  ['growth', 'growth'],
  ['routine', 'routine'],
  ['progetti', 'projects'],
  ['projects', 'projects'],
]);

export function normalizeWorldFocusId(value: unknown): WorldFocusId | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }

  return WORLD_BY_ID.has(value as WorldFocusId)
    ? (value as WorldFocusId)
    : undefined;
}

export function getWorldFocusWorld(
  id: WorldFocusId,
): WorldFocusWorld | undefined {
  return WORLD_BY_ID.get(id);
}

export function resolveWorldFocusWorldByLabel(
  label: string,
): WorldFocusWorld | undefined {
  const id = WORLD_ID_BY_LABEL.get(label.trim().toLocaleLowerCase());
  return id === undefined ? undefined : getWorldFocusWorld(id);
}
