import {
  createTemporalCreateFields,
  type TemporalCreateFields,
} from '../model/temporal-create-session';

export type TemporalCreateHandoffTarget =
  | 'project'
  | 'goal'
  | 'routine'
  | 'program'
  | 'world'
  | 'template'
  | 'reminder'
  | 'block'
  | 'asset';

export type TemporalCreateHandoffAvailability = 'deferred' | 'available';

export type TemporalCreateHandoffDescriptor = Readonly<{
  target: TemporalCreateHandoffTarget;
  availability: TemporalCreateHandoffAvailability;
  preservesDraft: true;
}>;

export type TemporalCreateHandoffIntent = Readonly<{
  source: 'timeline-create';
  target: TemporalCreateHandoffTarget;
  availability: TemporalCreateHandoffAvailability;
  draftSnapshot: TemporalCreateFields;
}>;

const HANDOFF_TARGETS: readonly TemporalCreateHandoffTarget[] = Object.freeze([
  'project',
  'goal',
  'routine',
  'program',
  'world',
  'template',
  'reminder',
  'block',
  'asset',
]);

const HANDOFF_REGISTRY: readonly TemporalCreateHandoffDescriptor[] = Object.freeze(
  HANDOFF_TARGETS.map((target) =>
    Object.freeze({
      target,
      availability: 'deferred' as const,
      preservesDraft: true as const,
    }),
  ),
);

/**
 * Authoritative Create-side registry for objects owned by another vertical.
 *
 * C1 deliberately does not contain routes, CRUD callbacks or provider actions:
 * a target becomes actionable only when its owning vertical supplies that
 * integration. Keeping availability explicit prevents disabled UI from being
 * mistaken for an implemented navigation path.
 */
export function temporalCreateHandoffRegistry(): readonly TemporalCreateHandoffDescriptor[] {
  return HANDOFF_REGISTRY;
}

/**
 * Builds the immutable application payload that an owning vertical may consume
 * later. The snapshot is re-normalized through Create before transfer so a
 * future keyboard/import/DANTE seed cannot bypass ownership invariants such as
 * Activity -> Routine for persistent recurrence.
 */
export function prepareTemporalCreateHandoff(
  target: TemporalCreateHandoffTarget,
  fields: TemporalCreateFields,
): TemporalCreateHandoffIntent {
  const descriptor = HANDOFF_REGISTRY.find((candidate) => candidate.target === target);
  if (!descriptor) {
    throw new Error(`Unknown Temporal Create handoff target: ${target}`);
  }

  return Object.freeze({
    source: 'timeline-create' as const,
    target: descriptor.target,
    availability: descriptor.availability,
    draftSnapshot: createTemporalCreateFields(fields),
  });
}
