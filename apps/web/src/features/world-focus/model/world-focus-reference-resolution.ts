import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from './world-focus-context-reference';

export const WORLD_FOCUS_REFERENCE_RESOLUTION_STATES = [
  'usable',
  'unresolved',
  'retired',
] as const;

export type WorldFocusReferenceResolutionState =
  (typeof WORLD_FOCUS_REFERENCE_RESOLUTION_STATES)[number];

export type WorldFocusReferenceResolution =
  | Readonly<{
      status: 'usable';
      reference: WorldFocusContextReference;
    }>
  | Readonly<{
      status: 'unresolved';
      reference: WorldFocusContextReference;
      reasonCode: string;
    }>
  | Readonly<{
      status: 'retired';
      reference: WorldFocusContextReference;
      reasonCode: string;
    }>;

export type WorldFocusReferenceResolutionInput =
  | Readonly<{
      status: 'usable';
      reference: WorldFocusContextReference;
    }>
  | Readonly<{
      status: 'unresolved' | 'retired';
      reference: WorldFocusContextReference;
      reasonCode: string;
    }>;

function assertNonEmptyReasonCode(value: string): string {
  const reasonCode = value.trim();
  if (reasonCode.length === 0) {
    throw new Error('World Focus reference resolution reason code must not be empty');
  }
  return reasonCode;
}

/**
 * Materializes only the safe frontend disposition of an already-authoritative
 * reference-resolution attempt. It never chooses merge/split successors,
 * authorizes disclosure, copies source payload or embeds provider state.
 */
export function createWorldFocusReferenceResolution(
  input: WorldFocusReferenceResolutionInput,
): WorldFocusReferenceResolution {
  const reference = normalizeWorldFocusContextReference(
    input.reference,
    'World Focus reference resolution reference',
  );

  if (input.status === 'usable') {
    return Object.freeze({
      status: 'usable' as const,
      reference,
    });
  }

  return Object.freeze({
    status: input.status,
    reference,
    reasonCode: assertNonEmptyReasonCode(input.reasonCode),
  });
}
