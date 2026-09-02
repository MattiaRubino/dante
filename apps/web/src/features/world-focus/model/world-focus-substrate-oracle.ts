import type { WorldFocusContextReference } from './world-focus-workspace';

export const WORLD_FOCUS_ORACLE_BASIS_LEVELS = [
  'current',
  'superseded-retracted',
  'conflicted-incomplete',
] as const;
export type WorldFocusOracleBasis =
  (typeof WORLD_FOCUS_ORACLE_BASIS_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_DISCLOSURE_LEVELS = [
  'allowed',
  'revoked',
  'purpose-recipient-mismatch',
] as const;
export type WorldFocusOracleDisclosure =
  (typeof WORLD_FOCUS_ORACLE_DISCLOSURE_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_IDENTITY_LEVELS = [
  'stable',
  'ambiguous-candidate',
  'retired-merge-split',
] as const;
export type WorldFocusOracleIdentity =
  (typeof WORLD_FOCUS_ORACLE_IDENTITY_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_GOVERNANCE_LEVELS = [
  'none',
  'revision-bound-binding',
  'represented-delegated',
] as const;
export type WorldFocusOracleGovernance =
  (typeof WORLD_FOCUS_ORACLE_GOVERNANCE_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_EFFECT_LEVELS = [
  'read-only',
  'pending-ambiguous',
  'partial-real-compensating',
] as const;
export type WorldFocusOracleEffect =
  (typeof WORLD_FOCUS_ORACLE_EFFECT_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_SYNC_LEVELS = [
  'online',
  'offline-replay',
  'provider-lag-timeout',
] as const;
export type WorldFocusOracleSync =
  (typeof WORLD_FOCUS_ORACLE_SYNC_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_CONFIG_LEVELS = [
  'transient',
  'pinned-saved',
  'concurrent-shared',
] as const;
export type WorldFocusOracleConfig =
  (typeof WORLD_FOCUS_ORACLE_CONFIG_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_INTERACTION_LEVELS = [
  'none',
  'primary-supporting',
  'world-switch-late',
] as const;
export type WorldFocusOracleInteraction =
  (typeof WORLD_FOCUS_ORACLE_INTERACTION_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_PRESENTATION_LEVELS = [
  'normal',
  'constrained-a11y',
  'specialist-missing',
] as const;
export type WorldFocusOraclePresentation =
  (typeof WORLD_FOCUS_ORACLE_PRESENTATION_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_DANTE_LEVELS = [
  'unavailable-quiet',
  'contextual-analysis',
  'proposal-action-late',
] as const;
export type WorldFocusOracleDante =
  (typeof WORLD_FOCUS_ORACLE_DANTE_LEVELS)[number];

export const WORLD_FOCUS_ORACLE_TIME_LEVELS = [
  'simple',
  'recurrence-exception-dst',
  'ordering-effective-unclear',
] as const;
export type WorldFocusOracleTime =
  (typeof WORLD_FOCUS_ORACLE_TIME_LEVELS)[number];

export type WorldFocusOracleScenario = Readonly<{
  basis: WorldFocusOracleBasis;
  disclosure: WorldFocusOracleDisclosure;
  identity: WorldFocusOracleIdentity;
  governance: WorldFocusOracleGovernance;
  effect: WorldFocusOracleEffect;
  sync: WorldFocusOracleSync;
  config: WorldFocusOracleConfig;
  interaction: WorldFocusOracleInteraction;
  presentation: WorldFocusOraclePresentation;
  dante: WorldFocusOracleDante;
  time: WorldFocusOracleTime;
}>;

export type WorldFocusOracleOutcome = Readonly<{
  basisDisposition: 'usable' | 'invalid' | 'unresolved';
  disclosureDisposition: 'allowed' | 'reject';
  referenceDisposition: 'usable' | 'unresolved' | 'retired';
  configDisposition: 'transient' | 'revalidate-saved' | 'conflict';
  effectDisposition:
    | 'not-applicable'
    | 'revalidate-before-execution'
    | 'blocked'
    | 'reconcile-before-claim'
    | 'compensate-or-reconcile';
  danteDisposition:
    | 'quiet'
    | 'authorized-context'
    | 'rebuild-or-reject-context'
    | 'reject-late-result'
    | 'revalidate-consequential-action';
  presentationDisposition:
    | 'normal'
    | 'semantic-invariant'
    | 'safe-fallback-or-local-failure';
  timeDisposition:
    | 'simple'
    | 'domain-time-semantics'
    | 'reconcile-ordering';
  requiresExecutionRevalidation: boolean;
  requiresRecipientPurposeRecheck: boolean;
  canAttachDerivedResult: boolean;
  canReuseSavedDerivedResult: boolean;
}>;

export type WorldFocusOracleReferenceSet = Readonly<{
  primary: WorldFocusContextReference;
  supporting: readonly WorldFocusContextReference[];
}>;

function assertNonEmptyToken(value: string, label: string): string {
  const token = value.trim();
  if (token.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  return token;
}

function normalizeReference(
  reference: WorldFocusContextReference,
  label: string,
): WorldFocusContextReference {
  return Object.freeze({
    kind: assertNonEmptyToken(reference.kind, `${label} kind`),
    key: assertNonEmptyToken(reference.key, `${label} key`),
  });
}

function referenceIdentity(reference: WorldFocusContextReference): string {
  return `${reference.kind}\u0000${reference.key}`;
}

export function createWorldFocusOracleReferenceSet(input: Readonly<{
  primary: WorldFocusContextReference;
  supporting?: readonly WorldFocusContextReference[];
  maxSupportingReferences: number;
}>): WorldFocusOracleReferenceSet {
  if (
    !Number.isInteger(input.maxSupportingReferences) ||
    input.maxSupportingReferences < 0
  ) {
    throw new Error(
      'World Focus maximum supporting references must be a non-negative integer',
    );
  }

  const primary = normalizeReference(
    input.primary,
    'World Focus primary context reference',
  );
  const supportingInput = input.supporting ?? [];
  if (supportingInput.length > input.maxSupportingReferences) {
    throw new Error('World Focus supporting context references exceed policy');
  }

  const seen = new Set<string>([referenceIdentity(primary)]);
  const supporting = supportingInput.map((reference, index) => {
    const normalized = normalizeReference(
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

function resolveBasisDisposition(
  basis: WorldFocusOracleBasis,
): WorldFocusOracleOutcome['basisDisposition'] {
  if (basis === 'superseded-retracted') {
    return 'invalid';
  }
  if (basis === 'conflicted-incomplete') {
    return 'unresolved';
  }
  return 'usable';
}

function resolveReferenceDisposition(
  identity: WorldFocusOracleIdentity,
): WorldFocusOracleOutcome['referenceDisposition'] {
  if (identity === 'retired-merge-split') {
    return 'retired';
  }
  if (identity === 'ambiguous-candidate') {
    return 'unresolved';
  }
  return 'usable';
}

function resolveConfigDisposition(
  config: WorldFocusOracleConfig,
): WorldFocusOracleOutcome['configDisposition'] {
  if (config === 'concurrent-shared') {
    return 'conflict';
  }
  if (config === 'pinned-saved') {
    return 'revalidate-saved';
  }
  return 'transient';
}

function mustRevalidateExecution(scenario: WorldFocusOracleScenario): boolean {
  if (scenario.dante === 'proposal-action-late') {
    return true;
  }
  if (scenario.effect === 'read-only') {
    return false;
  }

  return (
    scenario.basis !== 'current' ||
    scenario.disclosure !== 'allowed' ||
    scenario.identity !== 'stable' ||
    scenario.governance !== 'none' ||
    scenario.sync !== 'online' ||
    scenario.time !== 'simple'
  );
}

function resolveEffectDisposition(
  scenario: WorldFocusOracleScenario,
  requiresExecutionRevalidation: boolean,
): WorldFocusOracleOutcome['effectDisposition'] {
  if (scenario.effect === 'read-only') {
    return 'not-applicable';
  }

  // Once a real effect has partially occurred, later revocation, basis change or
  // identity evolution may constrain disclosure/new action but cannot erase the
  // obligation to compensate or reconcile the real-world consequence.
  if (scenario.effect === 'partial-real-compensating') {
    return 'compensate-or-reconcile';
  }

  if (
    scenario.disclosure !== 'allowed' ||
    scenario.identity !== 'stable' ||
    scenario.basis === 'superseded-retracted'
  ) {
    return 'blocked';
  }

  return requiresExecutionRevalidation
    ? 'revalidate-before-execution'
    : 'reconcile-before-claim';
}

function resolveDanteDisposition(
  scenario: WorldFocusOracleScenario,
  canAttachDerivedResult: boolean,
  requiresExecutionRevalidation: boolean,
): WorldFocusOracleOutcome['danteDisposition'] {
  if (scenario.dante === 'unavailable-quiet') {
    return 'quiet';
  }
  if (scenario.interaction === 'world-switch-late') {
    return 'reject-late-result';
  }
  if (!canAttachDerivedResult) {
    return 'rebuild-or-reject-context';
  }
  if (
    scenario.dante === 'proposal-action-late' &&
    requiresExecutionRevalidation
  ) {
    return 'revalidate-consequential-action';
  }
  return 'authorized-context';
}

export function resolveWorldFocusSubstrateOracle(
  scenario: WorldFocusOracleScenario,
): WorldFocusOracleOutcome {
  const basisDisposition = resolveBasisDisposition(scenario.basis);
  const disclosureDisposition =
    scenario.disclosure === 'allowed' ? 'allowed' : 'reject';
  const referenceDisposition = resolveReferenceDisposition(scenario.identity);
  const configDisposition = resolveConfigDisposition(scenario.config);
  const requiresExecutionRevalidation = mustRevalidateExecution(scenario);
  const requiresRecipientPurposeRecheck =
    scenario.disclosure !== 'allowed' ||
    scenario.config !== 'transient' ||
    scenario.dante !== 'unavailable-quiet';
  const canAttachDerivedResult =
    basisDisposition !== 'invalid' &&
    disclosureDisposition === 'allowed' &&
    referenceDisposition === 'usable' &&
    scenario.interaction !== 'world-switch-late';
  const canReuseSavedDerivedResult =
    scenario.config !== 'concurrent-shared' &&
    basisDisposition === 'usable' &&
    disclosureDisposition === 'allowed' &&
    referenceDisposition === 'usable';

  const outcome: WorldFocusOracleOutcome = Object.freeze({
    basisDisposition,
    disclosureDisposition,
    referenceDisposition,
    configDisposition,
    effectDisposition: resolveEffectDisposition(
      scenario,
      requiresExecutionRevalidation,
    ),
    danteDisposition: resolveDanteDisposition(
      scenario,
      canAttachDerivedResult,
      requiresExecutionRevalidation,
    ),
    presentationDisposition:
      scenario.presentation === 'normal'
        ? 'normal'
        : scenario.presentation === 'constrained-a11y'
          ? 'semantic-invariant'
          : 'safe-fallback-or-local-failure',
    timeDisposition:
      scenario.time === 'simple'
        ? 'simple'
        : scenario.time === 'recurrence-exception-dst'
          ? 'domain-time-semantics'
          : 'reconcile-ordering',
    requiresExecutionRevalidation,
    requiresRecipientPurposeRecheck,
    canAttachDerivedResult,
    canReuseSavedDerivedResult,
  });

  const violations = auditWorldFocusSubstrateOracle(scenario, outcome);
  if (violations.length > 0) {
    throw new Error(
      `World Focus substrate oracle invariant failure: ${violations.join('; ')}`,
    );
  }

  return outcome;
}

export function auditWorldFocusSubstrateOracle(
  scenario: WorldFocusOracleScenario,
  outcome: WorldFocusOracleOutcome,
): readonly string[] {
  const violations: string[] = [];

  if (
    scenario.basis === 'superseded-retracted' &&
    outcome.basisDisposition !== 'invalid'
  ) {
    violations.push('superseded/retracted basis must be invalid');
  }
  if (
    scenario.basis === 'conflicted-incomplete' &&
    outcome.basisDisposition !== 'unresolved'
  ) {
    violations.push('conflicted/incomplete basis must remain unresolved');
  }
  if (
    scenario.disclosure !== 'allowed' &&
    outcome.disclosureDisposition !== 'reject'
  ) {
    violations.push('revoked or mismatched disclosure must reject reuse');
  }
  if (
    scenario.identity === 'retired-merge-split' &&
    outcome.referenceDisposition !== 'retired'
  ) {
    violations.push('retired/merge/split identity must not silently retarget');
  }
  if (
    scenario.identity === 'ambiguous-candidate' &&
    outcome.referenceDisposition !== 'unresolved'
  ) {
    violations.push('ambiguous identity must remain unresolved');
  }
  if (
    scenario.identity !== 'stable' &&
    outcome.canAttachDerivedResult
  ) {
    violations.push(
      'derived result cannot attach to unresolved or retired identity',
    );
  }
  if (
    scenario.config === 'concurrent-shared' &&
    outcome.configDisposition !== 'conflict'
  ) {
    violations.push(
      'concurrent shared config must not use silent last-write-wins',
    );
  }
  if (
    scenario.interaction === 'world-switch-late' &&
    scenario.dante !== 'unavailable-quiet' &&
    outcome.danteDisposition !== 'reject-late-result'
  ) {
    violations.push('late DANTE result after World switch must be rejected');
  }
  if (
    scenario.effect !== 'read-only' &&
    outcome.requiresExecutionRevalidation !== mustRevalidateExecution(scenario)
  ) {
    violations.push('consequential execution revalidation decision drifted');
  }
  if (
    scenario.effect === 'partial-real-compensating' &&
    outcome.effectDisposition !== 'compensate-or-reconcile'
  ) {
    violations.push(
      'partial real effect must retain compensation/reconciliation obligation',
    );
  }
  if (
    scenario.dante === 'proposal-action-late' &&
    !outcome.requiresExecutionRevalidation
  ) {
    violations.push(
      'DANTE consequential proposal must revalidate at execution time',
    );
  }
  if (
    scenario.dante === 'proposal-action-late' &&
    outcome.canAttachDerivedResult &&
    outcome.danteDisposition !== 'revalidate-consequential-action'
  ) {
    violations.push(
      'attachable DANTE consequential proposal must retain revalidation state',
    );
  }
  if (
    scenario.disclosure !== 'allowed' &&
    outcome.canAttachDerivedResult
  ) {
    violations.push(
      'derived result cannot attach after disclosure invalidation',
    );
  }
  if (
    outcome.canReuseSavedDerivedResult &&
    (scenario.config === 'concurrent-shared' ||
      scenario.basis !== 'current' ||
      scenario.disclosure !== 'allowed' ||
      scenario.identity !== 'stable')
  ) {
    violations.push(
      'saved derived result reuse requires current basis, allowed disclosure, stable identity and non-conflicting config',
    );
  }
  if (
    scenario.presentation === 'constrained-a11y' &&
    outcome.presentationDisposition !== 'semantic-invariant'
  ) {
    violations.push(
      'responsive/a11y pressure must not alter semantic identity',
    );
  }

  return Object.freeze(violations);
}

function readTernaryDigit(
  vector: string,
  index: number,
  expectedLength: number,
): 0 | 1 | 2 {
  if (vector.length !== expectedLength || !/^[012]+$/.test(vector)) {
    throw new Error(
      `World Focus oracle vector must contain exactly ${expectedLength} ternary digits`,
    );
  }
  return Number(vector[index]) as 0 | 1 | 2;
}

export function decodeWorldFocusGeneralOracleVector(
  vector: string,
): WorldFocusOracleScenario {
  const digit = (index: number) => readTernaryDigit(vector, index, 11);

  return Object.freeze({
    basis: WORLD_FOCUS_ORACLE_BASIS_LEVELS[digit(0)],
    disclosure: WORLD_FOCUS_ORACLE_DISCLOSURE_LEVELS[digit(1)],
    identity: WORLD_FOCUS_ORACLE_IDENTITY_LEVELS[digit(2)],
    governance: WORLD_FOCUS_ORACLE_GOVERNANCE_LEVELS[digit(3)],
    effect: WORLD_FOCUS_ORACLE_EFFECT_LEVELS[digit(4)],
    sync: WORLD_FOCUS_ORACLE_SYNC_LEVELS[digit(5)],
    config: WORLD_FOCUS_ORACLE_CONFIG_LEVELS[digit(6)],
    interaction: WORLD_FOCUS_ORACLE_INTERACTION_LEVELS[digit(7)],
    presentation: WORLD_FOCUS_ORACLE_PRESENTATION_LEVELS[digit(8)],
    dante: WORLD_FOCUS_ORACLE_DANTE_LEVELS[digit(9)],
    time: WORLD_FOCUS_ORACLE_TIME_LEVELS[digit(10)],
  });
}

export function decodeWorldFocusHighRiskOracleVector(
  vector: string,
): WorldFocusOracleScenario {
  const digit = (index: number) => readTernaryDigit(vector, index, 7);

  return Object.freeze({
    basis: WORLD_FOCUS_ORACLE_BASIS_LEVELS[digit(0)],
    disclosure: WORLD_FOCUS_ORACLE_DISCLOSURE_LEVELS[digit(1)],
    identity: WORLD_FOCUS_ORACLE_IDENTITY_LEVELS[digit(2)],
    governance: WORLD_FOCUS_ORACLE_GOVERNANCE_LEVELS[digit(3)],
    effect: WORLD_FOCUS_ORACLE_EFFECT_LEVELS[digit(4)],
    sync: WORLD_FOCUS_ORACLE_SYNC_LEVELS[digit(5)],
    config: 'transient',
    interaction: 'none',
    presentation: 'normal',
    dante: WORLD_FOCUS_ORACLE_DANTE_LEVELS[digit(6)],
    time: 'simple',
  });
}
