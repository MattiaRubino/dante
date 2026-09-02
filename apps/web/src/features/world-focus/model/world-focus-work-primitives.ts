import type { WorldFocusContextReference } from './world-focus-workspace';

export const WORLD_FOCUS_WORK_PRIMITIVE_KINDS = [
  'continuity',
  'attention',
  'comparison',
  'trajectory',
] as const;

export type WorldFocusWorkPrimitiveKind =
  (typeof WORLD_FOCUS_WORK_PRIMITIVE_KINDS)[number];

export const WORLD_FOCUS_CONTINUITY_STATES = [
  'active',
  'paused',
  'blocked',
] as const;

export type WorldFocusContinuityState =
  (typeof WORLD_FOCUS_CONTINUITY_STATES)[number];

export const WORLD_FOCUS_ATTENTION_STATES = [
  'unresolved',
  'awaiting-response',
  'blocked',
] as const;

export type WorldFocusAttentionState =
  (typeof WORLD_FOCUS_ATTENTION_STATES)[number];

export const WORLD_FOCUS_COMPARISON_MODES = [
  'difference',
  'change',
  'trade-off',
  'planned-actual',
] as const;

export type WorldFocusComparisonMode =
  (typeof WORLD_FOCUS_COMPARISON_MODES)[number];

export const WORLD_FOCUS_TRAJECTORY_AXES = ['time', 'sequence'] as const;

export type WorldFocusTrajectoryAxis =
  (typeof WORLD_FOCUS_TRAJECTORY_AXES)[number];

export type WorldFocusContinuityPrimitive = Readonly<{
  instanceId: string;
  kind: 'continuity';
  threadReference: WorldFocusContextReference;
  checkpointReference: WorldFocusContextReference;
  continuationReference: WorldFocusContextReference | null;
  state: WorldFocusContinuityState;
}>;

export type WorldFocusAttentionPrimitive = Readonly<{
  instanceId: string;
  kind: 'attention';
  matterReference: WorldFocusContextReference;
  reasonCode: string;
  resolutionReference: WorldFocusContextReference | null;
  state: WorldFocusAttentionState;
}>;

export type WorldFocusComparisonPrimitive = Readonly<{
  instanceId: string;
  kind: 'comparison';
  mode: WorldFocusComparisonMode;
  subjectReferences: readonly [
    WorldFocusContextReference,
    WorldFocusContextReference,
    ...WorldFocusContextReference[],
  ];
  basisReference: WorldFocusContextReference | null;
}>;

export type WorldFocusTrajectoryPrimitive = Readonly<{
  instanceId: string;
  kind: 'trajectory';
  subjectReference: WorldFocusContextReference;
  axis: WorldFocusTrajectoryAxis;
  orderedPointReferences: readonly [
    WorldFocusContextReference,
    WorldFocusContextReference,
    ...WorldFocusContextReference[],
  ];
  orderingBasisReference: WorldFocusContextReference | null;
}>;

export type WorldFocusWorkPrimitive =
  | WorldFocusContinuityPrimitive
  | WorldFocusAttentionPrimitive
  | WorldFocusComparisonPrimitive
  | WorldFocusTrajectoryPrimitive;

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

function normalizeDistinctReferences(
  references: readonly WorldFocusContextReference[],
  label: string,
  minimum: number,
): readonly WorldFocusContextReference[] {
  if (references.length < minimum) {
    throw new Error(`${label} must contain at least ${minimum} references`);
  }

  const seen = new Set<string>();
  return Object.freeze(
    references.map((reference, index) => {
      const normalized = normalizeReference(reference, `${label}[${index}]`);
      const identity = referenceIdentity(normalized);
      if (seen.has(identity)) {
        throw new Error(`${label} must not contain duplicate references`);
      }
      seen.add(identity);
      return normalized;
    }),
  );
}

function normalizeOptionalReference(
  reference: WorldFocusContextReference | null | undefined,
  label: string,
): WorldFocusContextReference | null {
  return reference == null ? null : normalizeReference(reference, label);
}

export function createWorldFocusContinuityPrimitive(
  input: Omit<WorldFocusContinuityPrimitive, 'kind'>,
): WorldFocusContinuityPrimitive {
  if (!WORLD_FOCUS_CONTINUITY_STATES.includes(input.state)) {
    throw new Error(`Unsupported World Focus continuity state: ${input.state}`);
  }

  return Object.freeze({
    instanceId: assertNonEmptyToken(
      input.instanceId,
      'World Focus continuity instance id',
    ),
    kind: 'continuity',
    threadReference: normalizeReference(
      input.threadReference,
      'World Focus continuity thread reference',
    ),
    checkpointReference: normalizeReference(
      input.checkpointReference,
      'World Focus continuity checkpoint reference',
    ),
    continuationReference: normalizeOptionalReference(
      input.continuationReference,
      'World Focus continuity continuation reference',
    ),
    state: input.state,
  });
}

export function createWorldFocusAttentionPrimitive(
  input: Omit<WorldFocusAttentionPrimitive, 'kind'>,
): WorldFocusAttentionPrimitive {
  if (!WORLD_FOCUS_ATTENTION_STATES.includes(input.state)) {
    throw new Error(`Unsupported World Focus attention state: ${input.state}`);
  }

  return Object.freeze({
    instanceId: assertNonEmptyToken(
      input.instanceId,
      'World Focus attention instance id',
    ),
    kind: 'attention',
    matterReference: normalizeReference(
      input.matterReference,
      'World Focus attention matter reference',
    ),
    reasonCode: assertNonEmptyToken(
      input.reasonCode,
      'World Focus attention reason code',
    ),
    resolutionReference: normalizeOptionalReference(
      input.resolutionReference,
      'World Focus attention resolution reference',
    ),
    state: input.state,
  });
}

export function createWorldFocusComparisonPrimitive(
  input: Omit<WorldFocusComparisonPrimitive, 'kind'>,
): WorldFocusComparisonPrimitive {
  if (!WORLD_FOCUS_COMPARISON_MODES.includes(input.mode)) {
    throw new Error(`Unsupported World Focus comparison mode: ${input.mode}`);
  }

  const subjectReferences = normalizeDistinctReferences(
    input.subjectReferences,
    'World Focus comparison subject references',
    2,
  ) as WorldFocusComparisonPrimitive['subjectReferences'];

  return Object.freeze({
    instanceId: assertNonEmptyToken(
      input.instanceId,
      'World Focus comparison instance id',
    ),
    kind: 'comparison',
    mode: input.mode,
    subjectReferences,
    basisReference: normalizeOptionalReference(
      input.basisReference,
      'World Focus comparison basis reference',
    ),
  });
}

export function createWorldFocusTrajectoryPrimitive(
  input: Omit<WorldFocusTrajectoryPrimitive, 'kind'>,
): WorldFocusTrajectoryPrimitive {
  if (!WORLD_FOCUS_TRAJECTORY_AXES.includes(input.axis)) {
    throw new Error(`Unsupported World Focus trajectory axis: ${input.axis}`);
  }

  const orderedPointReferences = normalizeDistinctReferences(
    input.orderedPointReferences,
    'World Focus trajectory point references',
    2,
  ) as WorldFocusTrajectoryPrimitive['orderedPointReferences'];

  return Object.freeze({
    instanceId: assertNonEmptyToken(
      input.instanceId,
      'World Focus trajectory instance id',
    ),
    kind: 'trajectory',
    subjectReference: normalizeReference(
      input.subjectReference,
      'World Focus trajectory subject reference',
    ),
    axis: input.axis,
    orderedPointReferences,
    orderingBasisReference: normalizeOptionalReference(
      input.orderingBasisReference,
      'World Focus trajectory ordering basis reference',
    ),
  });
}

export function getWorldFocusWorkPrimitiveReferences(
  primitive: WorldFocusWorkPrimitive,
): readonly WorldFocusContextReference[] {
  switch (primitive.kind) {
    case 'continuity':
      return Object.freeze(
        [
          primitive.threadReference,
          primitive.checkpointReference,
          primitive.continuationReference,
        ].filter(
          (reference): reference is WorldFocusContextReference =>
            reference !== null,
        ),
      );
    case 'attention':
      return Object.freeze(
        [primitive.matterReference, primitive.resolutionReference].filter(
          (reference): reference is WorldFocusContextReference =>
            reference !== null,
        ),
      );
    case 'comparison':
      return Object.freeze([
        ...primitive.subjectReferences,
        ...(primitive.basisReference === null ? [] : [primitive.basisReference]),
      ]);
    case 'trajectory':
      return Object.freeze([
        primitive.subjectReference,
        ...primitive.orderedPointReferences,
        ...(primitive.orderingBasisReference === null
          ? []
          : [primitive.orderingBasisReference]),
      ]);
  }
}
