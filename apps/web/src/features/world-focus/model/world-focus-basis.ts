import {
  normalizeWorldFocusContextReference,
  type WorldFocusContextReference,
} from './world-focus-context-reference';

export const WORLD_FOCUS_FRESHNESS_STATES = [
  'current',
  'stale',
  'unknown',
] as const;

export type WorldFocusFreshnessState =
  (typeof WORLD_FOCUS_FRESHNESS_STATES)[number];

export type WorldFocusFreshnessFacet =
  | Readonly<{
      status: 'current' | 'stale';
      asOf: string;
    }>
  | Readonly<{
      status: 'unknown';
    }>;

export const WORLD_FOCUS_VALIDITY_STATES = [
  'current',
  'superseded',
  'retracted',
  'unresolved',
] as const;

export type WorldFocusValidityState =
  (typeof WORLD_FOCUS_VALIDITY_STATES)[number];

export type WorldFocusValidityFacet =
  | Readonly<{
      status: 'current';
    }>
  | Readonly<{
      status: 'superseded' | 'retracted' | 'unresolved';
      reasonCode: string;
    }>;

export const WORLD_FOCUS_COVERAGE_STATES = [
  'complete',
  'incomplete',
  'conflicted',
  'unknown',
] as const;

export type WorldFocusCoverageState =
  (typeof WORLD_FOCUS_COVERAGE_STATES)[number];

export type WorldFocusCoverageFacet =
  | Readonly<{
      status: 'complete';
    }>
  | Readonly<{
      status: 'unknown';
    }>
  | Readonly<{
      status: 'incomplete';
      reasonCode: string;
    }>
  | Readonly<{
      status: 'conflicted';
      reasonCode: string;
    }>;

export const WORLD_FOCUS_MATERIAL_PAYLOAD_STATES = [
  'present',
  'retired',
] as const;

export type WorldFocusMaterialPayloadState =
  (typeof WORLD_FOCUS_MATERIAL_PAYLOAD_STATES)[number];

export type WorldFocusMaterialPayloadFacet =
  | Readonly<{
      status: 'present';
      materialStateReference: WorldFocusContextReference;
    }>
  | Readonly<{
      status: 'retired';
      materialStateReference: WorldFocusContextReference;
      reasonCode: string;
      retiredAt: string;
    }>;

function assertNonEmptyReasonCode(value: string, label: string): string {
  const reasonCode = value.trim();
  if (reasonCode.length === 0) {
    throw new Error(`${label} reason code must not be empty`);
  }
  return reasonCode;
}

function normalizeInstant(value: string, label: string): string {
  const candidate = value.trim();
  const timestamp = Date.parse(candidate);
  if (candidate.length === 0 || Number.isNaN(timestamp)) {
    throw new Error(`${label} must be a valid instant`);
  }
  return new Date(timestamp).toISOString();
}

/**
 * Freshness answers only whether a known projection/basis is current, stale or
 * not currently knowable. It does not decide validity, disclosure or provider
 * availability.
 */
export function createWorldFocusFreshnessFacet(
  input:
    | Readonly<{ status: 'current' | 'stale'; asOf: string }>
    | Readonly<{ status: 'unknown' }>,
): WorldFocusFreshnessFacet {
  if (input.status === 'unknown') {
    return Object.freeze({ status: 'unknown' as const });
  }

  return Object.freeze({
    status: input.status,
    asOf: normalizeInstant(input.asOf, 'World Focus freshness as-of'),
  });
}

/**
 * Validity remains orthogonal to freshness: stale can still be valid history,
 * while superseded/retracted material is not made current by being recent.
 */
export function createWorldFocusValidityFacet(
  input:
    | Readonly<{ status: 'current' }>
    | Readonly<{
        status: 'superseded' | 'retracted' | 'unresolved';
        reasonCode: string;
      }>,
): WorldFocusValidityFacet {
  if (input.status === 'current') {
    return Object.freeze({ status: 'current' as const });
  }

  return Object.freeze({
    status: input.status,
    reasonCode: assertNonEmptyReasonCode(input.reasonCode, 'World Focus validity'),
  });
}

/**
 * Coverage describes completeness/conflict only. Incomplete, conflicted and
 * unknown inputs must never be collapsed into false, zero, empty or a winner.
 */
export function createWorldFocusCoverageFacet(
  input:
    | Readonly<{ status: 'complete' }>
    | Readonly<{ status: 'unknown' }>
    | Readonly<{
        status: 'incomplete';
        reasonCode: string;
      }>
    | Readonly<{
        status: 'conflicted';
        reasonCode: string;
      }>,
): WorldFocusCoverageFacet {
  if (input.status === 'complete' || input.status === 'unknown') {
    return Object.freeze({ status: input.status });
  }

  return Object.freeze({
    status: input.status,
    reasonCode: assertNonEmptyReasonCode(input.reasonCode, 'World Focus coverage'),
  });
}

/**
 * Represents only whether the protected payload for an exact material-state
 * reference is present or retired. Retirement preserves reference/history
 * continuity while carrying no source payload, authorization or provider state.
 */
export function createWorldFocusMaterialPayloadFacet(
  input:
    | Readonly<{
        status: 'present';
        materialStateReference: WorldFocusContextReference;
      }>
    | Readonly<{
        status: 'retired';
        materialStateReference: WorldFocusContextReference;
        reasonCode: string;
        retiredAt: string;
      }>,
): WorldFocusMaterialPayloadFacet {
  const materialStateReference = normalizeWorldFocusContextReference(
    input.materialStateReference,
    'World Focus material-state reference',
  );

  if (input.status === 'present') {
    return Object.freeze({
      status: 'present' as const,
      materialStateReference,
    });
  }

  return Object.freeze({
    status: 'retired' as const,
    materialStateReference,
    reasonCode: assertNonEmptyReasonCode(
      input.reasonCode,
      'World Focus material payload',
    ),
    retiredAt: normalizeInstant(
      input.retiredAt,
      'World Focus material payload retired-at',
    ),
  });
}
