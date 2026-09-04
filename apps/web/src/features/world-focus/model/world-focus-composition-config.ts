import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from './world-focus-identity';

export const WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION = 1 as const;

export const WORLD_FOCUS_COMPOSITION_CONFIG_VISIBILITIES = [
  'visible',
  'hidden',
] as const;

export type WorldFocusCompositionConfigVisibility =
  (typeof WORLD_FOCUS_COMPOSITION_CONFIG_VISIBILITIES)[number];

export type WorldFocusCompositionProminenceOverride = 'lead' | null;

export type WorldFocusCompositionConfigEntry = Readonly<{
  instanceId: string;
  kind: string;
  visibility: WorldFocusCompositionConfigVisibility;
  pinned: boolean;
  prominenceOverride: WorldFocusCompositionProminenceOverride;
}>;

export type WorldFocusCompositionConfig = Readonly<{
  schemaVersion: typeof WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION;
  revision: number;
  worldId: WorldFocusId;
  entries: readonly WorldFocusCompositionConfigEntry[];
}>;

export type WorldFocusCompositionConfigVersionDisposition =
  | Readonly<{ status: 'current' }>
  | Readonly<{ status: 'migration-required'; fromVersion: number }>
  | Readonly<{ status: 'unsupported'; schemaVersion: number }>;

type WorldFocusCompositionConfigInputEntry = Readonly<{
  instanceId: unknown;
  kind: unknown;
  visibility: unknown;
  pinned: unknown;
  prominenceOverride: unknown;
}>;

type WorldFocusCompositionConfigInput = Readonly<{
  schemaVersion: unknown;
  revision: unknown;
  worldId: unknown;
  entries: readonly WorldFocusCompositionConfigInputEntry[];
}>;

function normalizeNonEmptyToken(value: unknown, label: string): string {
  if (typeof value !== 'string') {
    throw new Error(`${label} must be a non-empty string`);
  }

  const token = value.trim();
  if (token.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  return token;
}

function normalizeRevision(value: unknown): number {
  if (
    typeof value !== 'number' ||
    !Number.isSafeInteger(value) ||
    value < 0
  ) {
    throw new Error('World Focus composition config revision must be a non-negative safe integer');
  }
  return value;
}

function normalizeVisibility(value: unknown): WorldFocusCompositionConfigVisibility {
  if (value !== 'visible' && value !== 'hidden') {
    throw new Error('World Focus composition config visibility must be visible or hidden');
  }
  return value;
}

function normalizePinned(value: unknown): boolean {
  if (typeof value !== 'boolean') {
    throw new Error('World Focus composition config pinned state must be boolean');
  }
  return value;
}

function normalizeProminenceOverride(
  value: unknown,
): WorldFocusCompositionProminenceOverride {
  if (value !== null && value !== 'lead') {
    throw new Error('World Focus composition prominence override must be lead or null');
  }
  return value;
}

function normalizeEntry(
  input: WorldFocusCompositionConfigInputEntry,
): WorldFocusCompositionConfigEntry {
  return Object.freeze({
    instanceId: normalizeNonEmptyToken(
      input.instanceId,
      'World Focus composition config instance id',
    ),
    kind: normalizeNonEmptyToken(
      input.kind,
      'World Focus composition config kind',
    ),
    visibility: normalizeVisibility(input.visibility),
    pinned: normalizePinned(input.pinned),
    prominenceOverride: normalizeProminenceOverride(input.prominenceOverride),
  });
}

export function inspectWorldFocusCompositionConfigVersion(
  schemaVersion: number,
): WorldFocusCompositionConfigVersionDisposition {
  if (!Number.isSafeInteger(schemaVersion) || schemaVersion < 0) {
    return Object.freeze({ status: 'unsupported', schemaVersion });
  }

  if (schemaVersion === WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION) {
    return Object.freeze({ status: 'current' });
  }

  if (schemaVersion < WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION) {
    return Object.freeze({
      status: 'migration-required',
      fromVersion: schemaVersion,
    });
  }

  return Object.freeze({ status: 'unsupported', schemaVersion });
}

/**
 * Creates a client-owned composition-configuration snapshot only. The snapshot
 * carries placement/customization metadata and never canonical Domain payload,
 * authorization state, disclosure authority, or executable renderer code.
 */
export function createWorldFocusCompositionConfig(
  input: WorldFocusCompositionConfigInput,
): WorldFocusCompositionConfig {
  if (input.schemaVersion !== WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION) {
    throw new Error('World Focus composition config schema version is not current');
  }

  const worldId = normalizeWorldFocusId(input.worldId);
  if (worldId === undefined) {
    throw new Error('World Focus composition config World id must not be empty');
  }

  const revision = normalizeRevision(input.revision);
  const seen = new Set<string>();
  const entries = input.entries.map((rawEntry) => {
    const entry = normalizeEntry(rawEntry);
    if (seen.has(entry.instanceId)) {
      throw new Error(
        `Duplicate World Focus composition config instance: ${entry.instanceId}`,
      );
    }
    seen.add(entry.instanceId);
    return entry;
  });

  return Object.freeze({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision,
    worldId,
    entries: Object.freeze(entries),
  });
}
