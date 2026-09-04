import type { WorldFocusCompositionOwnership } from './world-focus-platform';

export const WORLD_FOCUS_COMPOSITION_PROMINENCES = [
  'lead',
  'primary',
  'supporting',
] as const;

export type WorldFocusCompositionProminence =
  (typeof WORLD_FOCUS_COMPOSITION_PROMINENCES)[number];

export const WORLD_FOCUS_COMPOSITION_FOOTPRINTS = [
  'wide',
  'standard',
  'compact',
] as const;

export type WorldFocusCompositionFootprint =
  (typeof WORLD_FOCUS_COMPOSITION_FOOTPRINTS)[number];

export type WorldFocusCompositionCandidate<Kind extends string = string> =
  Readonly<{
    instanceId: string;
    kind: Kind;
    ownership: WorldFocusCompositionOwnership;
    prominence: WorldFocusCompositionProminence;
    footprint: WorldFocusCompositionFootprint;
    order: number;
  }>;

export type WorldFocusCompositionGridSpan = 4 | 6 | 12;

export type WorldFocusCompositionPlanEntry<Kind extends string = string> =
  WorldFocusCompositionCandidate<Kind> &
    Readonly<{
      gridSpan: WorldFocusCompositionGridSpan;
      row: number;
    }>;

export type WorldFocusCompositionOmission = Readonly<{
  instanceId: string;
  reason: 'adaptive-budget' | 'ephemeral-budget';
}>;

export type WorldFocusCompositionPolicy = Readonly<{
  maxAdaptiveEntries: number;
  maxEphemeralEntries: number;
}>;

export type WorldFocusCompositionPlan<Kind extends string = string> = Readonly<{
  entries: readonly WorldFocusCompositionPlanEntry<Kind>[];
  omitted: readonly WorldFocusCompositionOmission[];
  rowCount: number;
}>;

const PROMINENCE_RANK: Readonly<Record<WorldFocusCompositionProminence, number>> = {
  lead: 0,
  primary: 1,
  supporting: 2,
};

const PREFERRED_SPAN: Readonly<
  Record<WorldFocusCompositionFootprint, WorldFocusCompositionGridSpan>
> = {
  wide: 12,
  standard: 6,
  compact: 4,
};

const MAX_SPAN: Readonly<
  Record<WorldFocusCompositionFootprint, WorldFocusCompositionGridSpan>
> = {
  wide: 12,
  standard: 12,
  compact: 6,
};

const VALID_SPANS: readonly WorldFocusCompositionGridSpan[] = [4, 6, 12];

function assertNonNegativeInteger(value: number, label: string): number {
  if (!Number.isInteger(value) || value < 0) {
    throw new Error(`${label} must be a non-negative integer`);
  }
  return value;
}

function assertCandidate(candidate: WorldFocusCompositionCandidate): void {
  if (candidate.instanceId.trim().length === 0) {
    throw new Error('World Focus composition instance id must not be empty');
  }
  if (candidate.kind.trim().length === 0) {
    throw new Error('World Focus composition kind must not be empty');
  }
  if (!Number.isInteger(candidate.order) || candidate.order < 0) {
    throw new Error('World Focus composition order must be a non-negative integer');
  }
}

function compareCandidates(
  left: WorldFocusCompositionCandidate,
  right: WorldFocusCompositionCandidate,
): number {
  const prominenceDelta =
    PROMINENCE_RANK[left.prominence] - PROMINENCE_RANK[right.prominence];
  return prominenceDelta !== 0 ? prominenceDelta : left.order - right.order;
}

/**
 * M3-4 combines several independently valid ordering laws:
 * - explicit user move order must survive pin/promote classification;
 * - stable entries keep their established relative order;
 * - non-user dynamic leads keep the platform lead policy;
 * - stable content still precedes non-user dynamic non-lead content.
 *
 * A positional slot replacement can satisfy one law while silently breaking
 * another. Resolve the selected membership as a deterministic partial order
 * instead. The previous platform-policy order is only the tie-break between
 * candidates that are not otherwise constrained.
 */
function orderSelectedCandidates<Kind extends string>(
  selectedByPolicy: readonly WorldFocusCompositionCandidate<Kind>[],
): readonly WorldFocusCompositionCandidate<Kind>[] {
  if (selectedByPolicy.length <= 1) {
    return selectedByPolicy;
  }

  const policyIndex = new Map(
    selectedByPolicy.map((candidate, index) => [candidate.instanceId, index]),
  );
  const outgoing = new Map<string, Set<string>>();
  const indegree = new Map<string, number>();
  const byId = new Map<string, WorldFocusCompositionCandidate<Kind>>();

  for (const candidate of selectedByPolicy) {
    outgoing.set(candidate.instanceId, new Set());
    indegree.set(candidate.instanceId, 0);
    byId.set(candidate.instanceId, candidate);
  }

  const getPolicyIndex = (candidate: WorldFocusCompositionCandidate<Kind>) =>
    policyIndex.get(candidate.instanceId) ?? Number.MAX_SAFE_INTEGER;
  const compareByOrderThenPolicy = (
    left: WorldFocusCompositionCandidate<Kind>,
    right: WorldFocusCompositionCandidate<Kind>,
  ) => left.order - right.order || getPolicyIndex(left) - getPolicyIndex(right);
  const compareByPolicy = (
    left: WorldFocusCompositionCandidate<Kind>,
    right: WorldFocusCompositionCandidate<Kind>,
  ) => getPolicyIndex(left) - getPolicyIndex(right);

  const addEdge = (
    from: WorldFocusCompositionCandidate<Kind>,
    to: WorldFocusCompositionCandidate<Kind>,
  ) => {
    if (from.instanceId === to.instanceId) {
      return;
    }
    const targets = outgoing.get(from.instanceId);
    if (targets === undefined) {
      throw new Error('World Focus composition ordering source is missing');
    }
    if (targets.has(to.instanceId)) {
      return;
    }
    targets.add(to.instanceId);
    indegree.set(to.instanceId, (indegree.get(to.instanceId) ?? 0) + 1);
  };

  const connectChain = (
    candidates: readonly WorldFocusCompositionCandidate<Kind>[],
  ) => {
    for (let index = 1; index < candidates.length; index += 1) {
      const previous = candidates[index - 1];
      const current = candidates[index];
      if (previous !== undefined && current !== undefined) {
        addEdge(previous, current);
      }
    }
  };

  const userOrdered = selectedByPolicy
    .filter((candidate) => candidate.ownership.origin === 'user')
    .sort(compareByOrderThenPolicy);
  const stableOrdered = selectedByPolicy
    .filter((candidate) => candidate.ownership.stability === 'stable')
    .sort(compareByOrderThenPolicy);
  connectChain(userOrdered);
  connectChain(stableOrdered);

  const nonUserDynamicLeads = selectedByPolicy.filter(
    (candidate) =>
      candidate.ownership.origin !== 'user' &&
      candidate.ownership.stability !== 'stable' &&
      candidate.prominence === 'lead',
  );
  const nonUserDynamicNonLeads = selectedByPolicy.filter(
    (candidate) =>
      candidate.ownership.origin !== 'user' &&
      candidate.ownership.stability !== 'stable' &&
      candidate.prominence !== 'lead',
  );

  for (const lead of nonUserDynamicLeads) {
    for (const candidate of selectedByPolicy) {
      if (!nonUserDynamicLeads.includes(candidate)) {
        addEdge(lead, candidate);
      }
    }
  }

  for (const stable of stableOrdered) {
    for (const dynamic of nonUserDynamicNonLeads) {
      addEdge(stable, dynamic);
    }
  }

  const ready = selectedByPolicy
    .filter((candidate) => (indegree.get(candidate.instanceId) ?? 0) === 0)
    .sort(compareByPolicy);
  const ordered: WorldFocusCompositionCandidate<Kind>[] = [];

  while (ready.length > 0) {
    const current = ready.shift();
    if (current === undefined) {
      break;
    }
    ordered.push(current);

    const targets = outgoing.get(current.instanceId);
    if (targets === undefined) {
      continue;
    }
    for (const targetId of targets) {
      const nextIndegree = (indegree.get(targetId) ?? 0) - 1;
      indegree.set(targetId, nextIndegree);
      if (nextIndegree !== 0) {
        continue;
      }
      const target = byId.get(targetId);
      if (target === undefined) {
        throw new Error('World Focus composition ordering target is missing');
      }
      ready.push(target);
      ready.sort(compareByPolicy);
    }
  }

  if (ordered.length !== selectedByPolicy.length) {
    throw new Error('World Focus composition ordering constraints conflict');
  }

  return ordered;
}

function selectCandidates<Kind extends string>(
  candidates: readonly WorldFocusCompositionCandidate<Kind>[],
  policy: WorldFocusCompositionPolicy,
): Readonly<{
  selected: readonly WorldFocusCompositionCandidate<Kind>[];
  omitted: readonly WorldFocusCompositionOmission[];
}> {
  const maxAdaptiveEntries = assertNonNegativeInteger(
    policy.maxAdaptiveEntries,
    'World Focus max adaptive entries',
  );
  const maxEphemeralEntries = assertNonNegativeInteger(
    policy.maxEphemeralEntries,
    'World Focus max ephemeral entries',
  );
  const seen = new Set<string>();
  const stable: WorldFocusCompositionCandidate<Kind>[] = [];
  const adaptive: WorldFocusCompositionCandidate<Kind>[] = [];
  const ephemeral: WorldFocusCompositionCandidate<Kind>[] = [];

  for (const candidate of candidates) {
    assertCandidate(candidate);
    if (seen.has(candidate.instanceId)) {
      throw new Error(
        `Duplicate World Focus composition instance: ${candidate.instanceId}`,
      );
    }
    seen.add(candidate.instanceId);

    if (candidate.ownership.stability === 'stable') {
      stable.push(candidate);
    } else if (candidate.ownership.stability === 'adaptive') {
      adaptive.push(candidate);
    } else {
      ephemeral.push(candidate);
    }
  }

  stable.sort((left, right) => left.order - right.order);
  adaptive.sort(compareCandidates);
  ephemeral.sort(compareCandidates);

  const selectedAdaptive = adaptive.slice(0, maxAdaptiveEntries);
  const selectedEphemeral = ephemeral.slice(0, maxEphemeralEntries);
  const omitted: WorldFocusCompositionOmission[] = [
    ...adaptive.slice(maxAdaptiveEntries).map((candidate) => ({
      instanceId: candidate.instanceId,
      reason: 'adaptive-budget' as const,
    })),
    ...ephemeral.slice(maxEphemeralEntries).map((candidate) => ({
      instanceId: candidate.instanceId,
      reason: 'ephemeral-budget' as const,
    })),
  ];

  const selectedByPolicy = [
    ...selectedAdaptive.filter((candidate) => candidate.prominence === 'lead'),
    ...selectedEphemeral.filter((candidate) => candidate.prominence === 'lead'),
    ...stable,
    ...selectedAdaptive.filter((candidate) => candidate.prominence !== 'lead'),
    ...selectedEphemeral.filter((candidate) => candidate.prominence !== 'lead'),
  ];
  const selected = orderSelectedCandidates(selectedByPolicy);

  return Object.freeze({
    selected: Object.freeze(selected),
    omitted: Object.freeze(omitted),
  });
}

type MutablePlannedRowItem<Kind extends string> = {
  candidate: WorldFocusCompositionCandidate<Kind>;
  span: WorldFocusCompositionGridSpan;
};

function getNextValidSpan(
  current: WorldFocusCompositionGridSpan,
  max: WorldFocusCompositionGridSpan,
  remaining: number,
): WorldFocusCompositionGridSpan | null {
  for (const candidate of VALID_SPANS) {
    if (candidate <= current || candidate > max) {
      continue;
    }
    if (candidate - current <= remaining) {
      return candidate;
    }
  }
  return null;
}

function expandRowToFill<Kind extends string>(
  row: readonly Readonly<MutablePlannedRowItem<Kind>>[],
): readonly Readonly<MutablePlannedRowItem<Kind>>[] {
  let used = row.reduce((total, item) => total + item.span, 0);
  if (used >= 12) {
    return row;
  }

  const expanded: MutablePlannedRowItem<Kind>[] = row.map((item) => ({
    ...item,
  }));

  while (used < 12) {
    const remaining = 12 - used;
    let changed = false;

    for (let index = 0; index < expanded.length; index += 1) {
      const current = expanded[index];
      if (current === undefined) {
        continue;
      }
      const nextSpan = getNextValidSpan(
        current.span,
        MAX_SPAN[current.candidate.footprint],
        remaining,
      );
      if (nextSpan === null) {
        continue;
      }

      used += nextSpan - current.span;
      expanded[index] = {
        candidate: current.candidate,
        span: nextSpan,
      };
      changed = true;
      break;
    }

    if (!changed) {
      break;
    }
  }

  return expanded;
}

function planGrid<Kind extends string>(
  selected: readonly WorldFocusCompositionCandidate<Kind>[],
): Readonly<{
  entries: readonly WorldFocusCompositionPlanEntry<Kind>[];
  rowCount: number;
}> {
  const rows: Array<Array<MutablePlannedRowItem<Kind>>> = [];
  let currentRow: Array<MutablePlannedRowItem<Kind>> = [];
  let used = 0;

  const flush = () => {
    if (currentRow.length === 0) {
      return;
    }
    rows.push([...expandRowToFill(currentRow)]);
    currentRow = [];
    used = 0;
  };

  for (const candidate of selected) {
    const preferred =
      candidate.prominence === 'lead' ? 12 : PREFERRED_SPAN[candidate.footprint];

    if (preferred === 12) {
      flush();
      rows.push([{ candidate, span: 12 }]);
      continue;
    }

    if (used + preferred > 12) {
      flush();
    }

    currentRow.push({ candidate, span: preferred });
    used += preferred;

    if (used === 12) {
      flush();
    }
  }
  flush();

  const entries: WorldFocusCompositionPlanEntry<Kind>[] = [];
  rows.forEach((row, rowIndex) => {
    row.forEach(({ candidate, span }) => {
      entries.push(
        Object.freeze({
          ...candidate,
          ownership: Object.freeze({ ...candidate.ownership }),
          gridSpan: span,
          row: rowIndex,
        }),
      );
    });
  });

  return Object.freeze({
    entries: Object.freeze(entries),
    rowCount: rows.length,
  });
}

/**
 * Resolves a bounded first-surface composition without knowing the World
 * identity or canonical Domain semantics. Product/application code supplies
 * already-classified prominence/footprint; this planner owns only predictable
 * stable-vs-dynamic selection and spatial packing.
 */
export function resolveWorldFocusCompositionPlan<Kind extends string = string>(
  candidates: readonly WorldFocusCompositionCandidate<Kind>[],
  policy: WorldFocusCompositionPolicy,
): WorldFocusCompositionPlan<Kind> {
  const { selected, omitted } = selectCandidates(candidates, policy);
  const grid = planGrid(selected);

  return Object.freeze({
    entries: grid.entries,
    omitted,
    rowCount: grid.rowCount,
  });
}
