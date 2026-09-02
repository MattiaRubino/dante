export type WorldFocusId = string;

export type WorldFocusIdentityDescriptor = Readonly<{
  id: WorldFocusId;
  label: string;
  description: string;
}>;

function normalizeNonEmptyString(value: unknown): string | undefined {
  if (typeof value !== 'string') {
    return undefined;
  }

  const normalized = value.trim();
  return normalized.length === 0 ? undefined : normalized;
}

/**
 * Normalizes only the frontend identity token. It deliberately does not decide
 * whether a World exists, is authorized, or is routable. Those decisions stay
 * with the application/route resolver that owns the concrete descriptor.
 */
export function normalizeWorldFocusId(value: unknown): WorldFocusId | undefined {
  return normalizeNonEmptyString(value);
}

export function createWorldFocusIdentityDescriptor(input: Readonly<{
  id: unknown;
  label: unknown;
  description: unknown;
}>): WorldFocusIdentityDescriptor {
  const id = normalizeWorldFocusId(input.id);
  const label = normalizeNonEmptyString(input.label);
  const description = normalizeNonEmptyString(input.description);

  if (id === undefined) {
    throw new Error('World Focus id must not be empty');
  }
  if (label === undefined) {
    throw new Error('World Focus label must not be empty');
  }
  if (description === undefined) {
    throw new Error('World Focus description must not be empty');
  }

  return Object.freeze({ id, label, description });
}
