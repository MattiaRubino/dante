import {
  createWorldFocusCompositionConfig,
  WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
  type WorldFocusCompositionConfig,
  type WorldFocusCompositionConfigEntry,
} from '../model/world-focus-composition-config';
import {
  createWorldFocusCompositionOpportunity,
  type WorldFocusCompositionOpportunity,
} from './world-focus-composition-opportunities';

export const WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SOURCES = [
  'manual',
  'dante-proposed',
] as const;

export type WorldFocusCompositionCustomizationSource =
  (typeof WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SOURCES)[number];

type WorldFocusCompositionInstanceCommand<
  Type extends 'pin' | 'unpin' | 'hide' | 'show' | 'promote' | 'restore',
> = Readonly<{
  source: WorldFocusCompositionCustomizationSource;
  type: Type;
  instanceId: string;
}>;

type WorldFocusCompositionAdoptCommand = Readonly<{
  source: WorldFocusCompositionCustomizationSource;
  type: 'adopt';
  opportunity: WorldFocusCompositionOpportunity;
}>;

export type WorldFocusCompositionCustomizationCommand =
  | WorldFocusCompositionAdoptCommand
  | WorldFocusCompositionInstanceCommand<'pin'>
  | WorldFocusCompositionInstanceCommand<'unpin'>
  | WorldFocusCompositionInstanceCommand<'hide'>
  | WorldFocusCompositionInstanceCommand<'show'>
  | WorldFocusCompositionInstanceCommand<'promote'>
  | WorldFocusCompositionInstanceCommand<'restore'>
  | Readonly<{
      source: WorldFocusCompositionCustomizationSource;
      type: 'move';
      instanceId: string;
      beforeInstanceId: string | null;
    }>;

export type WorldFocusCompositionCustomizationOperation =
  | Readonly<{
      source: WorldFocusCompositionCustomizationSource;
      type: 'adopt';
      instanceId: string;
      kind: string;
    }>
  | Exclude<WorldFocusCompositionCustomizationCommand, WorldFocusCompositionAdoptCommand>;

export type WorldFocusCompositionCustomizationDraft = Readonly<{
  worldId: string;
  baseRevision: number;
  baseConfig: WorldFocusCompositionConfig;
  workingConfig: WorldFocusCompositionConfig;
  operations: readonly WorldFocusCompositionCustomizationOperation[];
}>;

export type WorldFocusCompositionDraftApplyResult =
  | Readonly<{
      status: 'applied';
      config: WorldFocusCompositionConfig;
    }>
  | Readonly<{
      status: 'revision-conflict';
      baseRevision: number;
      currentRevision: number;
    }>;

function normalizeToken(value: string, label: string): string {
  const token = value.trim();
  if (token.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  return token;
}

function assertCommandSource(
  source: WorldFocusCompositionCustomizationSource,
): WorldFocusCompositionCustomizationSource {
  if (source !== 'manual' && source !== 'dante-proposed') {
    throw new Error('Unsupported World Focus composition customization source');
  }
  return source;
}

function cloneCurrentConfig(config: WorldFocusCompositionConfig) {
  return createWorldFocusCompositionConfig({
    schemaVersion: config.schemaVersion,
    revision: config.revision,
    worldId: config.worldId,
    entries: config.entries,
  });
}

function createWorkingConfig(
  draft: WorldFocusCompositionCustomizationDraft,
  entries: readonly WorldFocusCompositionConfigEntry[],
) {
  return createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision: draft.baseRevision,
    worldId: draft.worldId,
    entries,
  });
}

function findRequiredEntryIndex(
  entries: readonly WorldFocusCompositionConfigEntry[],
  instanceId: string,
): number {
  const index = entries.findIndex((entry) => entry.instanceId === instanceId);
  if (index < 0) {
    throw new Error(`Missing World Focus composition instance: ${instanceId}`);
  }
  return index;
}

function replaceEntry(
  entries: readonly WorldFocusCompositionConfigEntry[],
  index: number,
  replacement: WorldFocusCompositionConfigEntry,
): readonly WorldFocusCompositionConfigEntry[] {
  return entries.map((entry, candidateIndex) =>
    candidateIndex === index ? replacement : entry,
  );
}

function freezeInstanceCommand<
  Type extends 'pin' | 'unpin' | 'hide' | 'show' | 'promote' | 'restore',
>(
  source: WorldFocusCompositionCustomizationSource,
  type: Type,
  instanceId: string,
): WorldFocusCompositionInstanceCommand<Type> {
  return Object.freeze({ source, type, instanceId });
}

function sameConfigEntry(
  left: WorldFocusCompositionConfigEntry,
  right: WorldFocusCompositionConfigEntry,
): boolean {
  return (
    left.instanceId === right.instanceId &&
    left.kind === right.kind &&
    left.visibility === right.visibility &&
    left.pinned === right.pinned &&
    left.prominenceOverride === right.prominenceOverride
  );
}

function sameConfigSnapshot(
  left: WorldFocusCompositionConfig,
  right: WorldFocusCompositionConfig,
): boolean {
  return (
    left.schemaVersion === right.schemaVersion &&
    left.revision === right.revision &&
    left.worldId === right.worldId &&
    left.entries.length === right.entries.length &&
    left.entries.every((entry, index) => {
      const other = right.entries[index];
      return other !== undefined && sameConfigEntry(entry, other);
    })
  );
}

function applyCommandToEntries(
  draft: WorldFocusCompositionCustomizationDraft,
  command: WorldFocusCompositionCustomizationCommand,
): Readonly<{
  entries: readonly WorldFocusCompositionConfigEntry[];
  operation: WorldFocusCompositionCustomizationOperation;
}> {
  const source = assertCommandSource(command.source);
  const workingEntries = draft.workingConfig.entries;

  if (command.type === 'adopt') {
    const opportunity = createWorldFocusCompositionOpportunity(command.opportunity);
    if (workingEntries.some((entry) => entry.instanceId === opportunity.instanceId)) {
      throw new Error(
        `Duplicate World Focus composition instance: ${opportunity.instanceId}`,
      );
    }

    const entry: WorldFocusCompositionConfigEntry = Object.freeze({
      instanceId: opportunity.instanceId,
      kind: opportunity.kind,
      visibility: 'visible',
      pinned: false,
      prominenceOverride: null,
    });

    return Object.freeze({
      entries: Object.freeze([...workingEntries, entry]),
      operation: Object.freeze({
        source,
        type: 'adopt' as const,
        instanceId: opportunity.instanceId,
        kind: opportunity.kind,
      }),
    });
  }

  const instanceId = normalizeToken(
    command.instanceId,
    'World Focus composition customization instance id',
  );
  const index = findRequiredEntryIndex(workingEntries, instanceId);
  const currentEntry = workingEntries[index];
  if (currentEntry === undefined) {
    throw new Error(`Missing World Focus composition instance: ${instanceId}`);
  }

  switch (command.type) {
    case 'pin': {
      return Object.freeze({
        entries: replaceEntry(
          workingEntries,
          index,
          Object.freeze({ ...currentEntry, pinned: true }),
        ),
        operation: freezeInstanceCommand(source, 'pin', instanceId),
      });
    }
    case 'unpin': {
      return Object.freeze({
        entries: replaceEntry(
          workingEntries,
          index,
          Object.freeze({ ...currentEntry, pinned: false }),
        ),
        operation: freezeInstanceCommand(source, 'unpin', instanceId),
      });
    }
    case 'hide': {
      return Object.freeze({
        entries: replaceEntry(
          workingEntries,
          index,
          Object.freeze({ ...currentEntry, visibility: 'hidden' as const }),
        ),
        operation: freezeInstanceCommand(source, 'hide', instanceId),
      });
    }
    case 'show': {
      return Object.freeze({
        entries: replaceEntry(
          workingEntries,
          index,
          Object.freeze({ ...currentEntry, visibility: 'visible' as const }),
        ),
        operation: freezeInstanceCommand(source, 'show', instanceId),
      });
    }
    case 'promote': {
      return Object.freeze({
        entries: replaceEntry(
          workingEntries,
          index,
          Object.freeze({ ...currentEntry, prominenceOverride: 'lead' as const }),
        ),
        operation: freezeInstanceCommand(source, 'promote', instanceId),
      });
    }
    case 'move': {
      const beforeInstanceId =
        command.beforeInstanceId === null
          ? null
          : normalizeToken(
              command.beforeInstanceId,
              'World Focus composition move target instance id',
            );

      if (beforeInstanceId === instanceId) {
        return Object.freeze({
          entries: workingEntries,
          operation: Object.freeze({
            source,
            type: 'move' as const,
            instanceId,
            beforeInstanceId,
          }),
        });
      }

      if (beforeInstanceId !== null) {
        findRequiredEntryIndex(workingEntries, beforeInstanceId);
      }

      const remaining = workingEntries.filter(
        (entry) => entry.instanceId !== instanceId,
      );
      const destinationIndex =
        beforeInstanceId === null
          ? remaining.length
          : findRequiredEntryIndex(remaining, beforeInstanceId);
      const entries = [...remaining];
      entries.splice(destinationIndex, 0, currentEntry);

      return Object.freeze({
        entries: Object.freeze(entries),
        operation: Object.freeze({
          source,
          type: 'move' as const,
          instanceId,
          beforeInstanceId,
        }),
      });
    }
    case 'restore': {
      const baseIndex = draft.baseConfig.entries.findIndex(
        (entry) => entry.instanceId === instanceId,
      );

      if (baseIndex < 0) {
        return Object.freeze({
          entries: Object.freeze(
            workingEntries.filter((entry) => entry.instanceId !== instanceId),
          ),
          operation: freezeInstanceCommand(source, 'restore', instanceId),
        });
      }

      const baseEntry = draft.baseConfig.entries[baseIndex];
      if (baseEntry === undefined) {
        throw new Error(`Missing World Focus base composition instance: ${instanceId}`);
      }

      const entries = workingEntries.filter(
        (entry) => entry.instanceId !== instanceId,
      );
      entries.splice(baseIndex, 0, baseEntry);

      return Object.freeze({
        entries: Object.freeze(entries),
        operation: freezeInstanceCommand(source, 'restore', instanceId),
      });
    }
    default:
      throw new Error('Unsupported World Focus composition customization command');
  }
}

/**
 * Starts an isolated customization transaction. All manual and future
 * DANTE-proposed operations mutate only this draft until explicit Apply.
 */
export function beginWorldFocusCompositionCustomization(
  currentConfig: WorldFocusCompositionConfig,
): WorldFocusCompositionCustomizationDraft {
  const baseConfig = cloneCurrentConfig(currentConfig);
  return Object.freeze({
    worldId: baseConfig.worldId,
    baseRevision: baseConfig.revision,
    baseConfig,
    workingConfig: baseConfig,
    operations: Object.freeze([]),
  });
}

export function updateWorldFocusCompositionDraft(
  draft: WorldFocusCompositionCustomizationDraft,
  command: WorldFocusCompositionCustomizationCommand,
): WorldFocusCompositionCustomizationDraft {
  const result = applyCommandToEntries(draft, command);
  const workingConfig = createWorkingConfig(draft, result.entries);

  return Object.freeze({
    worldId: draft.worldId,
    baseRevision: draft.baseRevision,
    baseConfig: draft.baseConfig,
    workingConfig,
    operations: Object.freeze([...draft.operations, result.operation]),
  });
}

export function cancelWorldFocusCompositionDraft(
  draft: WorldFocusCompositionCustomizationDraft,
): WorldFocusCompositionConfig {
  return draft.baseConfig;
}

/**
 * Apply is the only M3 operation that produces a new current revision. A stale
 * draft never merges implicitly, a same-revision draft must still prove it was
 * based on the exact current snapshot, and DANTE-proposed commands have no
 * bypass around these same guards.
 */
export function applyWorldFocusCompositionDraft(
  currentConfig: WorldFocusCompositionConfig,
  draft: WorldFocusCompositionCustomizationDraft,
): WorldFocusCompositionDraftApplyResult {
  const current = cloneCurrentConfig(currentConfig);
  const base = cloneCurrentConfig(draft.baseConfig);
  const working = cloneCurrentConfig(draft.workingConfig);

  if (
    current.worldId !== draft.worldId ||
    base.worldId !== draft.worldId ||
    working.worldId !== draft.worldId
  ) {
    throw new Error('World Focus composition draft belongs to a different World');
  }

  if (current.revision !== draft.baseRevision) {
    return Object.freeze({
      status: 'revision-conflict',
      baseRevision: draft.baseRevision,
      currentRevision: current.revision,
    });
  }

  if (
    base.revision !== draft.baseRevision ||
    working.revision !== draft.baseRevision ||
    !sameConfigSnapshot(current, base)
  ) {
    throw new Error('Invalid World Focus composition draft base snapshot');
  }

  const config = createWorldFocusCompositionConfig({
    schemaVersion: WORLD_FOCUS_COMPOSITION_CONFIG_SCHEMA_VERSION,
    revision: current.revision + 1,
    worldId: current.worldId,
    entries: working.entries,
  });

  return Object.freeze({ status: 'applied', config });
}
