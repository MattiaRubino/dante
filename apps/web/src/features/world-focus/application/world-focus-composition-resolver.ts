import type { WorldFocusCompositionConfig } from '../model/world-focus-composition-config';
import type {
  WorldFocusCompositionCandidate,
  WorldFocusCompositionProminence,
} from '../model/world-focus-composition-plan';
import {
  normalizeWorldFocusId,
  type WorldFocusId,
} from '../model/world-focus-identity';
import type {
  WorldFocusCompositionOpportunity,
  WorldFocusCompositionOpportunitySet,
} from './world-focus-composition-opportunities';

export const WORLD_FOCUS_COMPOSITION_VALUE_SIGNALS = [
  'material-consequence',
  'immediacy',
  'resumability',
  'meaningful-change',
  'current-intent',
] as const;

export type WorldFocusCompositionValueSignal =
  (typeof WORLD_FOCUS_COMPOSITION_VALUE_SIGNALS)[number];

export type WorldFocusCompositionValueSignalAssignment = Readonly<{
  worldId: WorldFocusId;
  instanceId: string;
  kind: string;
  signals: readonly WorldFocusCompositionValueSignal[];
}>;

export type WorldFocusCompositionCandidateOmission = Readonly<{
  instanceId: string;
  kind: string;
  reason: 'hidden-by-user';
}>;

export type WorldFocusCompositionUnresolvedPinnedIntent = Readonly<{
  instanceId: string;
  kind: string;
  reason: 'meaningful-projection-unavailable';
}>;

export type WorldFocusCompositionCandidateResolution = Readonly<{
  candidates: readonly WorldFocusCompositionCandidate[];
  omitted: readonly WorldFocusCompositionCandidateOmission[];
  unresolvedPinned: readonly WorldFocusCompositionUnresolvedPinnedIntent[];
}>;

type WorldFocusCompositionValueSignalAssignmentInput = Readonly<{
  worldId: WorldFocusId;
  instanceId: string;
  kind: string;
  signals: readonly WorldFocusCompositionValueSignal[];
}>;

type WorldFocusCompositionValueBand = 'foreground' | 'active' | 'ordinary';

const PROMINENCE_RANK: Readonly<Record<WorldFocusCompositionProminence, number>> = {
  supporting: 0,
  primary: 1,
  lead: 2,
};

const BAND_RANK: Readonly<Record<WorldFocusCompositionValueBand, number>> = {
  foreground: 0,
  active: 1,
  ordinary: 2,
};

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
    throw new Error('World Focus composition signal World id must not be empty');
  }
  return worldId;
}

function normalizeSignals(
  signals: readonly WorldFocusCompositionValueSignal[],
): readonly WorldFocusCompositionValueSignal[] {
  const seen = new Set<WorldFocusCompositionValueSignal>();
  const normalized: WorldFocusCompositionValueSignal[] = [];

  for (const signal of signals) {
    if (!WORLD_FOCUS_COMPOSITION_VALUE_SIGNALS.includes(signal)) {
      throw new Error(`Unsupported World Focus composition value signal: ${signal}`);
    }
    if (seen.has(signal)) {
      throw new Error(`Duplicate World Focus composition value signal: ${signal}`);
    }
    seen.add(signal);
    normalized.push(signal);
  }

  return Object.freeze(normalized);
}

export function createWorldFocusCompositionValueSignalAssignment(
  input: WorldFocusCompositionValueSignalAssignmentInput,
): WorldFocusCompositionValueSignalAssignment {
  return Object.freeze({
    worldId: normalizeWorldId(input.worldId),
    instanceId: normalizeNonEmptyToken(
      input.instanceId,
      'World Focus composition signal instance id',
    ),
    kind: normalizeNonEmptyToken(
      input.kind,
      'World Focus composition signal kind',
    ),
    signals: normalizeSignals(input.signals),
  });
}

function classifyValueBand(
  signals: readonly WorldFocusCompositionValueSignal[],
): WorldFocusCompositionValueBand {
  const signalSet = new Set(signals);
  if (
    signalSet.has('material-consequence') ||
    signalSet.has('immediacy') ||
    signalSet.has('current-intent')
  ) {
    return 'foreground';
  }
  if (signalSet.has('resumability') || signalSet.has('meaningful-change')) {
    return 'active';
  }
  return 'ordinary';
}

function elevatedProminence(
  defaultProminence: WorldFocusCompositionProminence,
  band: WorldFocusCompositionValueBand,
): WorldFocusCompositionProminence {
  const minimum: WorldFocusCompositionProminence =
    band === 'foreground' ? 'lead' : band === 'active' ? 'primary' : 'supporting';
  return PROMINENCE_RANK[defaultProminence] >= PROMINENCE_RANK[minimum]
    ? defaultProminence
    : minimum;
}

function makeCandidate(
  opportunity: WorldFocusCompositionOpportunity,
  input: Readonly<{
    stability: 'stable' | 'adaptive';
    origin: 'user' | 'application-derived';
    prominence: WorldFocusCompositionProminence;
    order: number;
  }>,
): WorldFocusCompositionCandidate {
  return Object.freeze({
    instanceId: opportunity.instanceId,
    kind: opportunity.kind,
    ownership: Object.freeze({
      stability: input.stability,
      origin: input.origin,
    }),
    prominence: input.prominence,
    footprint: opportunity.footprint,
    order: input.order,
  });
}

/**
 * Resolves only composition metadata. It does not authorize, inspect Domain
 * payload, retain references, select renderers, or mount UI.
 */
export function resolveWorldFocusCompositionCandidates(input: Readonly<{
  opportunitySet: WorldFocusCompositionOpportunitySet;
  config: WorldFocusCompositionConfig;
  valueSignals: readonly WorldFocusCompositionValueSignalAssignment[];
}>): WorldFocusCompositionCandidateResolution {
  const worldId = normalizeWorldId(input.opportunitySet.worldId);
  if (input.config.worldId !== worldId) {
    throw new Error('World Focus composition config belongs to another World');
  }

  const opportunitiesById = new Map<string, WorldFocusCompositionOpportunity>();
  input.opportunitySet.opportunities.forEach((opportunity) => {
    if (opportunitiesById.has(opportunity.instanceId)) {
      throw new Error(
        `Duplicate World Focus composition opportunity instance: ${opportunity.instanceId}`,
      );
    }
    opportunitiesById.set(opportunity.instanceId, opportunity);
  });

  const signalsById = new Map<string, WorldFocusCompositionValueSignalAssignment>();
  input.valueSignals.forEach((rawAssignment) => {
    const assignment = createWorldFocusCompositionValueSignalAssignment(rawAssignment);
    if (assignment.worldId !== worldId) {
      throw new Error('World Focus composition signal belongs to another World');
    }
    const opportunity = opportunitiesById.get(assignment.instanceId);
    if (opportunity === undefined) {
      throw new Error(
        `Stale World Focus composition signal assignment: ${assignment.instanceId}`,
      );
    }
    if (opportunity.kind !== assignment.kind) {
      throw new Error(
        `World Focus composition signal kind mismatch for ${assignment.instanceId}`,
      );
    }
    if (signalsById.has(assignment.instanceId)) {
      throw new Error(
        `Duplicate World Focus composition signal assignment: ${assignment.instanceId}`,
      );
    }
    signalsById.set(assignment.instanceId, assignment);
  });

  const configById = new Map(
    input.config.entries.map((entry, index) => [entry.instanceId, { entry, index }] as const),
  );
  const candidates: WorldFocusCompositionCandidate[] = [];
  const omitted: WorldFocusCompositionCandidateOmission[] = [];
  const unresolvedPinned: WorldFocusCompositionUnresolvedPinnedIntent[] = [];

  for (const { entry, index } of configById.values()) {
    const opportunity = opportunitiesById.get(entry.instanceId);
    if (opportunity === undefined) {
      if (entry.visibility === 'visible' && entry.pinned) {
        unresolvedPinned.push(
          Object.freeze({
            instanceId: entry.instanceId,
            kind: entry.kind,
            reason: 'meaningful-projection-unavailable' as const,
          }),
        );
      }
      continue;
    }

    if (opportunity.kind !== entry.kind) {
      throw new Error(
        `World Focus composition config kind mismatch for ${entry.instanceId}`,
      );
    }

    if (entry.visibility === 'hidden') {
      omitted.push(
        Object.freeze({
          instanceId: entry.instanceId,
          kind: entry.kind,
          reason: 'hidden-by-user' as const,
        }),
      );
      continue;
    }

    candidates.push(
      makeCandidate(opportunity, {
        stability: entry.pinned ? 'stable' : 'adaptive',
        origin: 'user',
        prominence: entry.prominenceOverride === 'lead' ? 'lead' : 'primary',
        order: index,
      }),
    );
  }

  const unconfigured = input.opportunitySet.opportunities
    .map((opportunity, sourceIndex) => ({
      opportunity,
      sourceIndex,
      band: classifyValueBand(signalsById.get(opportunity.instanceId)?.signals ?? []),
    }))
    .filter(({ opportunity }) => !configById.has(opportunity.instanceId))
    .sort((left, right) => {
      const bandDelta = BAND_RANK[left.band] - BAND_RANK[right.band];
      return bandDelta !== 0 ? bandDelta : left.sourceIndex - right.sourceIndex;
    });

  unconfigured.forEach(({ opportunity, band }, index) => {
    candidates.push(
      makeCandidate(opportunity, {
        stability: 'adaptive',
        origin: 'application-derived',
        prominence: elevatedProminence(opportunity.defaultProminence, band),
        order: input.config.entries.length + index,
      }),
    );
  });

  return Object.freeze({
    candidates: Object.freeze(candidates),
    omitted: Object.freeze(omitted),
    unresolvedPinned: Object.freeze(unresolvedPinned),
  });
}
