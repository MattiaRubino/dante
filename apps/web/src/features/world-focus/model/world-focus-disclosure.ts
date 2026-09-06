export const WORLD_FOCUS_DISCLOSURE_STATES = Object.freeze([
  'available',
  'restricted',
  'unavailable',
] as const);

export type WorldFocusDisclosureState =
  (typeof WORLD_FOCUS_DISCLOSURE_STATES)[number];

export type WorldFocusDisclosureOutcome = Readonly<{
  status: WorldFocusDisclosureState;
}>;

function isRecord(value: unknown): value is Readonly<Record<string, unknown>> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isDisclosureState(value: unknown): value is WorldFocusDisclosureState {
  return (
    value === 'available' || value === 'restricted' || value === 'unavailable'
  );
}

/**
 * Materializes only the already-sanitized frontend disclosure result produced
 * after higher-authority recipient/purpose filtering. This boundary validates
 * the finite presentation vocabulary and deliberately copies no authorization,
 * identity, recipient, purpose, policy, payload, reference or provider detail.
 *
 * World relevance, selection and presentation state can never widen this
 * outcome. `available` is therefore a presentation result, not a frontend
 * authorization decision; `unavailable` is not an offline/provider verdict.
 */
export function createWorldFocusDisclosureOutcome(
  input: unknown,
): WorldFocusDisclosureOutcome {
  if (!isRecord(input)) {
    throw new Error('World Focus disclosure outcome must be an object');
  }

  const { status } = input;
  if (!isDisclosureState(status)) {
    throw new Error(
      'World Focus disclosure status must be available, restricted or unavailable',
    );
  }

  return Object.freeze({ status });
}
