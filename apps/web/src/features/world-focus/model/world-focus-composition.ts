import type { WorldFocusCompositionOwnership } from './world-focus-platform';

export type WorldFocusCompositionEntry<Kind extends string = string> = Readonly<{
  instanceId: string;
  kind: Kind;
  ownership: WorldFocusCompositionOwnership;
}>;

function assertNonEmptyToken(value: string, label: string): string {
  const token = value.trim();
  if (token.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  return token;
}

/**
 * Validates an already-resolved composition list without inventing ranking or
 * backend semantics. The future composition resolver may feed this boundary;
 * today it also lets real verticals leave WorldFocusPage hardcoding behind.
 */
export function defineWorldFocusComposition<Kind extends string = string>(
  entries: readonly WorldFocusCompositionEntry<Kind>[],
): readonly WorldFocusCompositionEntry<Kind>[] {
  const instanceIds = new Set<string>();

  const defined = entries.map((entry) => {
    const instanceId = assertNonEmptyToken(
      entry.instanceId,
      'World Focus composition instance id',
    );
    const kind = assertNonEmptyToken(
      entry.kind,
      'World Focus composition kind',
    ) as Kind;

    if (instanceIds.has(instanceId)) {
      throw new Error(`Duplicate World Focus composition instance: ${instanceId}`);
    }
    instanceIds.add(instanceId);

    return Object.freeze({
      ...entry,
      instanceId,
      kind,
      ownership: Object.freeze({ ...entry.ownership }),
    });
  });

  return Object.freeze(defined);
}
