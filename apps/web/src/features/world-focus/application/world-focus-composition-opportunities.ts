import type { WorldFocusContinuityReadResult } from '../model/world-focus-continuity';
import {
  WORLD_FOCUS_COMPOSITION_FOOTPRINTS,
  WORLD_FOCUS_COMPOSITION_PROMINENCES,
  type WorldFocusCompositionFootprint,
  type WorldFocusCompositionProminence,
} from '../model/world-focus-composition-plan';
import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from '../model/world-focus-identity';
import type {
  WorldFocusAttentionReadResult,
  WorldFocusComparisonReadResult,
  WorldFocusTrajectoryReadResult,
} from './world-focus-derived-work';
import type {
  WorldFocusEvidenceHistoryReadResult,
  WorldFocusNextReadResult,
  WorldFocusSituationReadResult,
} from './world-focus-direct-projections';

export const WORLD_FOCUS_COMPOSITION_OPPORTUNITY_LIMIT = 16;

export type WorldFocusCompositionOpportunity = Readonly<{
  instanceId: string;
  kind: string;
  defaultProminence: WorldFocusCompositionProminence;
  footprint: WorldFocusCompositionFootprint;
}>;

export type WorldFocusCompositionOpportunitySet = Readonly<{
  worldId: WorldFocusId;
  opportunities: readonly WorldFocusCompositionOpportunity[];
}>;

type WorldFocusCompositionOpportunityInput = Readonly<{
  instanceId: string;
  kind: string;
  defaultProminence: WorldFocusCompositionProminence;
  footprint: WorldFocusCompositionFootprint;
}>;

type WorldFocusCompositionProjectionSetInput = Readonly<{
  worldId: WorldFocusId;
  situation: WorldFocusSituationReadResult;
  continuity: WorldFocusContinuityReadResult;
  attention: WorldFocusAttentionReadResult;
  next: WorldFocusNextReadResult;
  comparison: WorldFocusComparisonReadResult;
  trajectory: WorldFocusTrajectoryReadResult;
  evidenceHistory: WorldFocusEvidenceHistoryReadResult;
}>;

function normalizeNonEmptyToken(value: string, label: string): string {
  const token = value.trim();
  if (token.length === 0) {
    throw new Error(`${label} must not be empty`);
  }
  return token;
}

function normalizeWorldId(value: WorldFocusId): WorldFocusId {
  const worldId = normalizeWorldFocusId(value);
  if (worldId === undefined) {
    throw new Error('World Focus composition opportunity World id must not be empty');
  }
  return worldId;
}

function normalizeProminence(
  value: WorldFocusCompositionProminence,
): WorldFocusCompositionProminence {
  if (!WORLD_FOCUS_COMPOSITION_PROMINENCES.includes(value)) {
    throw new Error(`Unsupported World Focus opportunity prominence: ${value}`);
  }
  return value;
}

function normalizeFootprint(
  value: WorldFocusCompositionFootprint,
): WorldFocusCompositionFootprint {
  if (!WORLD_FOCUS_COMPOSITION_FOOTPRINTS.includes(value)) {
    throw new Error(`Unsupported World Focus opportunity footprint: ${value}`);
  }
  return value;
}

export function createWorldFocusCompositionOpportunity(
  input: WorldFocusCompositionOpportunityInput,
): WorldFocusCompositionOpportunity {
  return Object.freeze({
    instanceId: normalizeNonEmptyToken(
      input.instanceId,
      'World Focus composition opportunity instance id',
    ),
    kind: normalizeNonEmptyToken(
      input.kind,
      'World Focus composition opportunity kind',
    ),
    defaultProminence: normalizeProminence(input.defaultProminence),
    footprint: normalizeFootprint(input.footprint),
  });
}

export function createWorldFocusCompositionOpportunitySet(input: Readonly<{
  worldId: WorldFocusId;
  opportunities: readonly WorldFocusCompositionOpportunity[];
}>): WorldFocusCompositionOpportunitySet {
  const worldId = normalizeWorldId(input.worldId);
  if (input.opportunities.length > WORLD_FOCUS_COMPOSITION_OPPORTUNITY_LIMIT) {
    throw new Error(
      `World Focus composition opportunities exceed limit ${WORLD_FOCUS_COMPOSITION_OPPORTUNITY_LIMIT}`,
    );
  }

  const seen = new Set<string>();
  const opportunities = input.opportunities.map((rawOpportunity) => {
    const opportunity = createWorldFocusCompositionOpportunity(rawOpportunity);
    if (seen.has(opportunity.instanceId)) {
      throw new Error(
        `Duplicate World Focus composition opportunity instance: ${opportunity.instanceId}`,
      );
    }
    seen.add(opportunity.instanceId);
    return opportunity;
  });

  return Object.freeze({
    worldId,
    opportunities: Object.freeze(opportunities),
  });
}

function resultWorldId(
  result:
    | WorldFocusSituationReadResult
    | WorldFocusNextReadResult
    | WorldFocusEvidenceHistoryReadResult
    | WorldFocusAttentionReadResult
    | WorldFocusComparisonReadResult
    | WorldFocusTrajectoryReadResult,
): WorldFocusId {
  return result.status === 'ready' ? result.projection.worldId : result.worldId;
}

function continuityWorldId(result: WorldFocusContinuityReadResult): WorldFocusId {
  return result.status === 'ready' || result.status === 'partial' || result.status === 'stale'
    ? result.projection.worldId
    : result.worldId;
}

function assertWorldMatch(
  expectedWorldId: WorldFocusId,
  actualWorldId: WorldFocusId,
  label: string,
): void {
  const normalizedActual = normalizeWorldId(actualWorldId);
  if (normalizedActual !== expectedWorldId) {
    throw new Error(`${label} belongs to another World`);
  }
}

function hasMeaningfulEvidenceHistory(
  result: WorldFocusEvidenceHistoryReadResult,
): boolean {
  if (result.status !== 'ready') {
    return false;
  }

  const { evidence, orderedHistoryReferences } = result.projection;
  return (
    evidence.evidenceReferences.length > 0 ||
    evidence.provenanceReferences.length > 0 ||
    evidence.integrityAttestationReferences.length > 0 ||
    orderedHistoryReferences.length > 0
  );
}

function addSingleton(
  target: WorldFocusCompositionOpportunity[],
  meaningful: boolean,
  input: WorldFocusCompositionOpportunityInput,
): void {
  if (meaningful) {
    target.push(createWorldFocusCompositionOpportunity(input));
  }
}

/**
 * Converts already-validated M1 application results into bounded composition
 * opportunities only. Source payload, references, reason codes, disclosure and
 * authorization never cross this boundary.
 */
export function collectWorldFocusCompositionOpportunities(
  input: WorldFocusCompositionProjectionSetInput,
): WorldFocusCompositionOpportunitySet {
  const worldId = normalizeWorldId(input.worldId);

  assertWorldMatch(worldId, resultWorldId(input.situation), 'World Focus Situation result');
  assertWorldMatch(worldId, continuityWorldId(input.continuity), 'World Focus Continuity result');
  assertWorldMatch(worldId, resultWorldId(input.attention), 'World Focus Attention result');
  assertWorldMatch(worldId, resultWorldId(input.next), 'World Focus Next result');
  assertWorldMatch(worldId, resultWorldId(input.comparison), 'World Focus Comparison result');
  assertWorldMatch(worldId, resultWorldId(input.trajectory), 'World Focus Trajectory result');
  assertWorldMatch(
    worldId,
    resultWorldId(input.evidenceHistory),
    'World Focus Evidence/History result',
  );

  const opportunities: WorldFocusCompositionOpportunity[] = [];

  addSingleton(
    opportunities,
    input.situation.status === 'ready' &&
      input.situation.projection.orderedSituationReferences.length > 0,
    {
      instanceId: 'situation',
      kind: 'situation',
      defaultProminence: 'primary',
      footprint: 'standard',
    },
  );

  addSingleton(
    opportunities,
    (input.continuity.status === 'ready' ||
      input.continuity.status === 'partial' ||
      input.continuity.status === 'stale') &&
      input.continuity.projection.orderedItems.length > 0,
    {
      instanceId: 'continuity',
      kind: 'continuity',
      defaultProminence: 'primary',
      footprint: 'standard',
    },
  );

  if (input.attention.status === 'ready') {
    input.attention.projection.orderedItems.forEach((primitive) => {
      opportunities.push(
        createWorldFocusCompositionOpportunity({
          instanceId: `attention:${primitive.instanceId}`,
          kind: 'attention',
          defaultProminence: 'primary',
          footprint: 'standard',
        }),
      );
    });
  }

  addSingleton(
    opportunities,
    input.next.status === 'ready' && input.next.projection.orderedNextReferences.length > 0,
    {
      instanceId: 'next',
      kind: 'next',
      defaultProminence: 'primary',
      footprint: 'standard',
    },
  );

  if (input.comparison.status === 'ready') {
    input.comparison.projection.orderedItems.forEach((primitive) => {
      opportunities.push(
        createWorldFocusCompositionOpportunity({
          instanceId: `comparison:${primitive.instanceId}`,
          kind: 'comparison',
          defaultProminence: 'supporting',
          footprint: 'standard',
        }),
      );
    });
  }

  if (input.trajectory.status === 'ready') {
    input.trajectory.projection.orderedItems.forEach((primitive) => {
      opportunities.push(
        createWorldFocusCompositionOpportunity({
          instanceId: `trajectory:${primitive.instanceId}`,
          kind: 'trajectory',
          defaultProminence: 'supporting',
          footprint: 'standard',
        }),
      );
    });
  }

  addSingleton(opportunities, hasMeaningfulEvidenceHistory(input.evidenceHistory), {
    instanceId: 'evidence-history',
    kind: 'evidence-history',
    defaultProminence: 'supporting',
    footprint: 'standard',
  });

  return createWorldFocusCompositionOpportunitySet({ worldId, opportunities });
}
