import type { WorldFocusContextReference } from './world-focus-context-reference';
import type { WorldFocusId } from './world-focus-identity';
import type { WorldFocusVersionedPayload } from './world-focus-platform';
import {
  WORLD_FOCUS_CONTINUITY_STATES,
  type WorldFocusContinuityState,
} from './world-focus-work-primitives';

export const WORLD_FOCUS_CONTINUITY_PRESENTATION_STATES =
  WORLD_FOCUS_CONTINUITY_STATES;

export type WorldFocusContinuityPresentationState = WorldFocusContinuityState;

export const WORLD_FOCUS_CONTINUITY_FIRST_OPEN_LIMIT = 4;

export type WorldFocusContinuityItem = Readonly<{
  key: string;
  title: string;
  context: string;
  checkpoint: string;
  threadReference: WorldFocusContextReference;
  checkpointReference: WorldFocusContextReference;
  continuationReference: WorldFocusContextReference | null;
  presentationState: WorldFocusContinuityPresentationState;
}>;

export type WorldFocusContinuityProjection = WorldFocusVersionedPayload<1> &
  Readonly<{
    worldId: WorldFocusId;
    orderedItems: readonly WorldFocusContinuityItem[];
  }>;

export type WorldFocusContinuityReadResult =
  | Readonly<{
      status: 'ready';
      projection: WorldFocusContinuityProjection;
    }>
  | Readonly<{
      status: 'empty';
      worldId: WorldFocusId;
    }>
  | Readonly<{
      status: 'partial';
      projection: WorldFocusContinuityProjection;
      reasonCode: string;
    }>
  | Readonly<{
      status: 'stale';
      projection: WorldFocusContinuityProjection;
      asOf: string;
    }>
  | Readonly<{
      status: 'unavailable';
      worldId: WorldFocusId;
      reasonCode: string;
      retryable: boolean;
    }>;

export function isWorldFocusContinuityPresentationState(
  value: unknown,
): value is WorldFocusContinuityPresentationState {
  return (
    typeof value === 'string' &&
    WORLD_FOCUS_CONTINUITY_PRESENTATION_STATES.includes(
      value as WorldFocusContinuityPresentationState,
    )
  );
}
