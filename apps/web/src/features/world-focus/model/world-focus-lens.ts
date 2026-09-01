export const WORLD_FOCUS_TIME_PRESETS = [
  '7d',
  '30d',
  '90d',
  '1y',
  'all',
] as const;

export type WorldFocusTimePreset = (typeof WORLD_FOCUS_TIME_PRESETS)[number];

export type WorldFocusTemporalLensCapability = Readonly<{
  defaultPreset: WorldFocusTimePreset;
  presets: readonly WorldFocusTimePreset[];
}>;

export type WorldFocusTimeLens =
  | Readonly<{
      kind: 'relative';
      preset: Exclude<WorldFocusTimePreset, 'all'>;
    }>
  | Readonly<{
      kind: 'all-time';
      preset: 'all';
    }>;

export type WorldFocusLens = Readonly<{
  time?: WorldFocusTimeLens;
}>;

export function normalizeWorldFocusTimePreset(
  value: unknown,
): WorldFocusTimePreset | undefined {
  return typeof value === 'string' &&
    WORLD_FOCUS_TIME_PRESETS.includes(value as WorldFocusTimePreset)
    ? (value as WorldFocusTimePreset)
    : undefined;
}

export function createWorldFocusTemporalLensCapability(
  defaultPreset: WorldFocusTimePreset,
  presets: readonly WorldFocusTimePreset[],
): WorldFocusTemporalLensCapability {
  if (presets.length === 0) {
    throw new Error('World Focus temporal Lens requires at least one preset');
  }

  const uniquePresets = new Set(presets);
  if (uniquePresets.size !== presets.length) {
    throw new Error('World Focus temporal Lens presets must be unique');
  }

  if (!uniquePresets.has(defaultPreset)) {
    throw new Error('World Focus temporal Lens default must be available');
  }

  return Object.freeze({
    defaultPreset,
    presets: Object.freeze([...presets]),
  });
}

export function resolveWorldFocusTimePreset(
  capability: WorldFocusTemporalLensCapability | undefined,
  requestedPreset: WorldFocusTimePreset | undefined,
): WorldFocusTimePreset | undefined {
  if (capability === undefined) {
    return undefined;
  }

  return requestedPreset !== undefined && capability.presets.includes(requestedPreset)
    ? requestedPreset
    : capability.defaultPreset;
}

export function createWorldFocusLens(
  capability: WorldFocusTemporalLensCapability | undefined,
  requestedPreset: WorldFocusTimePreset | undefined,
): WorldFocusLens {
  const preset = resolveWorldFocusTimePreset(capability, requestedPreset);
  if (preset === undefined) {
    return Object.freeze({});
  }

  const time: WorldFocusTimeLens =
    preset === 'all'
      ? Object.freeze({ kind: 'all-time', preset })
      : Object.freeze({ kind: 'relative', preset });

  return Object.freeze({ time });
}
