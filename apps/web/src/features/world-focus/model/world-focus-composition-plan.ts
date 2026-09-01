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

  // Stable content keeps its user/application-defined relative order. Dynamic
  // content can lead when explicitly classified as lead, but never silently
  // reorders stable entries relative to each other.
  const selected = [
    ...selectedAdaptive.filter((candidate) => candidate.prominence === 'lead'),
    ...selectedEphemeral.filter((candidate) => candidate.prominence === 'lead'),
    ...stable,
    ...selectedAdaptive.filter((candidate) => candidate.prominence !== 'lead'),
    ...selectedEphemeral.filter((candidate) => candidate.prominence !== 'lead'),
  ];

  return Object.freeze({
    selected: Object.freeze(selected),
    omitted: Object.freeze(omitted),
  });
}

function expandRowToFill<Kind extends string>(
  row: readonly Readonly<{
    candidate: WorldFocusCompositionCandidate<Kind>;
    span: WorldFocusCompositionGridSpan;
  }>[],
): readonly Readonly<{
  candidate: WorldFocusCompositionCandidate<Kind>;
  span: WorldFocusCompositionGridSpan;
}>[] {
  let used = row.reduce((total, item) => total + item.span, 0);
  if (used >= 12) {
    return row;
  }

  const expanded = row.map((item) => ({ ...item }));
  while (used < 12) {
    const candidateIndex = expanded.findIndex(
      (item) => item.span < MAX_SPAN[item.candidate.footprint],
    );
    if (candidateIndex < 0) {
      break;
    }

    const current = expanded[candidateIndex];
    if (current === undefined) {
      break;
    }
    const max = MAX_SPAN[current.candidate.footprint];
    const delta = Math.min(max - current.span, 12 - used);
    if (delta !== 2 && delta !== 4 && delta !== 6 && delta !== 8) {
      break;
    }
    const nextSpan = current.span + delta;
    if (nextSpan !== 4 && nextSpan !== 6 && nextSpan !== 12) {
      break;
    }

    expanded[candidateIndex] = {
      candidate: current.candidate,
      span: nextSpan,
    };
    used += delta;
  }

  return expanded;
}

function planGrid<Kind extends string>(
  selected: readonly WorldFocusCompositionCandidate<Kind>[],
): Readonly<{
  entries: readonly WorldFocusCompositionPlanEntry<Kind>[];
  rowCount: number;
}> {
  const rows: Array<
    Array<{
      candidate: WorldFocusCompositionCandidate<Kind>;
      span: WorldFocusCompositionGridSpan;
    }>
  > = [];
  let currentRow: Array<{
    candidate: WorldFocusCompositionCandidate<Kind>;
    span: WorldFocusCompositionGridSpan;
  }> = [];
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
