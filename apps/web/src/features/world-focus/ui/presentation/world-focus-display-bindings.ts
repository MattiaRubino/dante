import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from '../../model/world-focus-context-reference';

const WORLD_FOCUS_DISPLAY_LABEL_MAX_LENGTH = 512;
const WORLD_FOCUS_DISPLAY_SUPPORTING_TEXT_MAX_LENGTH = 2048;

export type WorldFocusDisplayBinding = Readonly<{
  reference: WorldFocusContextReference;
  label: string;
  supportingText?: string;
}>;

export type WorldFocusDisplayBindingSet = readonly WorldFocusDisplayBinding[];

function normalizeDisplayText(
  value: string,
  label: string,
  maxLength: number,
): string {
  const normalized = value.trim();
  if (normalized.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  if (normalized.length > maxLength) {
    throw new Error(`${label} must not exceed ${maxLength} characters`);
  }
  return normalized;
}

function referenceIdentity(reference: WorldFocusContextReference): string {
  return `${reference.kind}\u0000${reference.key}`;
}

export function createWorldFocusDisplayBinding(
  input: Readonly<{
    reference: WorldFocusContextReference;
    label: string;
    supportingText?: string;
  }>,
): WorldFocusDisplayBinding {
  const reference = normalizeWorldFocusContextReference(
    input.reference,
    'World Focus display binding reference',
  );
  const label = normalizeDisplayText(
    input.label,
    'World Focus display binding label',
    WORLD_FOCUS_DISPLAY_LABEL_MAX_LENGTH,
  );
  const supportingText =
    input.supportingText === undefined
      ? undefined
      : normalizeDisplayText(
          input.supportingText,
          'World Focus display binding supporting text',
          WORLD_FOCUS_DISPLAY_SUPPORTING_TEXT_MAX_LENGTH,
        );

  return Object.freeze({
    reference,
    label,
    ...(supportingText === undefined ? {} : { supportingText }),
  });
}

export function createWorldFocusDisplayBindingSet(
  inputs: readonly Readonly<{
    reference: WorldFocusContextReference;
    label: string;
    supportingText?: string;
  }>[],
): WorldFocusDisplayBindingSet {
  const seen = new Set<string>();
  const bindings = inputs.map((input) => {
    const binding = createWorldFocusDisplayBinding(input);
    const identity = referenceIdentity(binding.reference);
    if (seen.has(identity)) {
      throw new Error('Duplicate World Focus display binding reference');
    }
    seen.add(identity);
    return binding;
  });

  return Object.freeze(bindings);
}

export function worldFocusDisplayBindingMatchesReference(
  binding: WorldFocusDisplayBinding,
  reference: WorldFocusContextReference,
): boolean {
  const normalized = normalizeWorldFocusContextReference(
    reference,
    'World Focus display binding comparison reference',
  );
  return referenceIdentity(binding.reference) === referenceIdentity(normalized);
}

export function assertWorldFocusDisplayBindingMatchesReference(
  binding: WorldFocusDisplayBinding,
  reference: WorldFocusContextReference,
  label: string,
): void {
  if (!worldFocusDisplayBindingMatchesReference(binding, reference)) {
    throw new Error(`${label} display binding does not match semantic reference`);
  }
}

export function requireWorldFocusDisplayBinding(
  bindings: WorldFocusDisplayBindingSet,
  reference: WorldFocusContextReference,
): WorldFocusDisplayBinding {
  const normalized = normalizeWorldFocusContextReference(
    reference,
    'World Focus display binding lookup reference',
  );
  const identity = referenceIdentity(normalized);
  const binding = bindings.find(
    (candidate) => referenceIdentity(candidate.reference) === identity,
  );

  if (binding === undefined) {
    throw new Error('World Focus display binding is unavailable for reference');
  }
  return binding;
}
