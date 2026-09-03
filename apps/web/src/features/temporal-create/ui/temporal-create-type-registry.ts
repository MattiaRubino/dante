import type { TemporalCreateKind } from '../model/temporal-create-session';

export type TemporalCreateTypeDescriptor = Readonly<{
  kind: TemporalCreateKind;
  order: number;
  supportsAllDay: boolean;
  supportsUnplaced: boolean;
  supportsQuickRecurrence: boolean;
  supportsLocation: boolean;
}>;

const REGISTRY: readonly TemporalCreateTypeDescriptor[] = Object.freeze([
  Object.freeze({
    kind: 'activity' as const,
    order: 10,
    supportsAllDay: true,
    supportsUnplaced: true,
    supportsQuickRecurrence: false,
    supportsLocation: false,
  }),
  Object.freeze({
    kind: 'event' as const,
    order: 20,
    supportsAllDay: true,
    supportsUnplaced: false,
    supportsQuickRecurrence: true,
    supportsLocation: true,
  }),
]);

/**
 * Product-facing Create registry.
 *
 * Only genuinely usable owner types belong here. Future Reminder, Routine or
 * other verticals can register when they have a truthful application boundary;
 * disabled/deferred tiles are deliberately not surfaced in the normal Create
 * flow.
 */
export function temporalCreateTypeRegistry(): readonly TemporalCreateTypeDescriptor[] {
  return REGISTRY;
}

export function temporalCreateTypeDescriptor(
  kind: TemporalCreateKind,
): TemporalCreateTypeDescriptor {
  const descriptor = REGISTRY.find((candidate) => candidate.kind === kind);
  if (!descriptor) {
    throw new Error(`Unknown Temporal Create type: ${kind}`);
  }
  return descriptor;
}
