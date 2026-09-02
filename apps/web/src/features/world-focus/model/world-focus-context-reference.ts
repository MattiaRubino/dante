export type WorldFocusContextReference = Readonly<{
  kind: string;
  key: string;
}>;

export type WorldFocusContextReferenceSet = Readonly<{
  primary: WorldFocusContextReference;
  supporting: readonly WorldFocusContextReference[];
}>;

export const WORLD_FOCUS_DEFAULT_MAX_SUPPORTING_REFERENCES = 4;

function assertNonEmptyToken(value: string, label: string): string {
  const token = value.trim();
  if (token.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  return token;
}

export function normalizeWorldFocusContextReference(
  reference: WorldFocusContextReference,
  label = 'World Focus context reference',
): WorldFocusContextReference {
  return Object.freeze({
    kind: assertNonEmptyToken(reference.kind, `${label} kind`),
    key: assertNonEmptyToken(reference.key, `${label} key`),
  });
}

function referenceIdentity(reference: WorldFocusContextReference): string {
  return `${reference.kind}\u0000${reference.key}`;
}

export function sameWorldFocusContextReference(
  left: WorldFocusContextReference | null,
  right: WorldFocusContextReference | null,
): boolean {
  return left?.kind === right?.kind && left?.key === right?.key;
}

export function createWorldFocusContextReferenceSet(input: Readonly<{
  primary: WorldFocusContextReference;
  supporting?: readonly WorldFocusContextReference[] | undefined;
  maxSupportingReferences?: number;
}>): WorldFocusContextReferenceSet {
  const maximum =
    input.maxSupportingReferences ?? WORLD_FOCUS_DEFAULT_MAX_SUPPORTING_REFERENCES;
  if (!Number.isInteger(maximum) || maximum < 0) {
    throw new Error(
      'World Focus maximum supporting references must be a non-negative integer',
    );
  }

  const primary = normalizeWorldFocusContextReference(
    input.primary,
    'World Focus primary context reference',
  );
  const supportingInput = input.supporting ?? [];
  if (supportingInput.length > maximum) {
    throw new Error('World Focus supporting context references exceed policy');
  }

  const seen = new Set<string>([referenceIdentity(primary)]);
  const supporting = supportingInput.map((reference, index) => {
    const normalized = normalizeWorldFocusContextReference(
      reference,
      `World Focus supporting context reference[${index}]`,
    );
    const identity = referenceIdentity(normalized);
    if (seen.has(identity)) {
      throw new Error(
        'World Focus context reference set must not contain duplicates',
      );
    }
    seen.add(identity);
    return normalized;
  });

  return Object.freeze({
    primary,
    supporting: Object.freeze(supporting),
  });
}

export function sameWorldFocusContextReferenceSet(
  left: WorldFocusContextReferenceSet | null,
  right: WorldFocusContextReferenceSet | null,
): boolean {
  if (left === null || right === null) {
    return left === right;
  }
  if (!sameWorldFocusContextReference(left.primary, right.primary)) {
    return false;
  }
  if (left.supporting.length !== right.supporting.length) {
    return false;
  }

  return left.supporting.every((reference, index) =>
    sameWorldFocusContextReference(reference, right.supporting[index] ?? null),
  );
}
