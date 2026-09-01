import {
  createWorldFocusLens,
  type WorldFocusLens,
  type WorldFocusTemporalLensCapability,
  type WorldFocusTimePreset,
} from '../model/world-focus-lens';

export type WorldFocusSessionSnapshot = Readonly<{
  activeWorldId: string;
  lens: WorldFocusLens;
  scopeKey: string;
}>;

export function createWorldFocusSessionSnapshot(input: Readonly<{
  worldId: string;
  timeCapability: WorldFocusTemporalLensCapability | undefined;
  requestedTimePreset: WorldFocusTimePreset | undefined;
}>): WorldFocusSessionSnapshot {
  const lens = createWorldFocusLens(
    input.timeCapability,
    input.requestedTimePreset,
  );
  const timeKey = lens.time?.preset ?? 'none';

  return Object.freeze({
    activeWorldId: input.worldId,
    lens,
    scopeKey: `${input.worldId}|time:${timeKey}`,
  });
}
