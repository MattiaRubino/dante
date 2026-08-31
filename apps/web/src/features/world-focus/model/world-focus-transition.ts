import type { WorldFocusId } from './world-focus-fixtures';

export type WorldFocusEntrySource = 'home' | 'worlds';

export type WorldFocusOriginRect = Readonly<{
  left: number;
  top: number;
  width: number;
  height: number;
}>;

export type WorldFocusEntrySnapshot = Readonly<{
  token: number;
  worldId: WorldFocusId;
  source: WorldFocusEntrySource;
  origin: WorldFocusOriginRect;
  createdAt: number;
}>;

const WORLD_FOCUS_ENTRY_TTL_MS = 5_000;

let sequence = 0;
let pendingEntry: WorldFocusEntrySnapshot | null = null;

function finiteOr(value: number, fallback: number) {
  return Number.isFinite(value) ? value : fallback;
}

function normalizeOrigin(origin: WorldFocusOriginRect): WorldFocusOriginRect {
  return {
    left: finiteOr(origin.left, 0),
    top: finiteOr(origin.top, 0),
    width: Math.max(1, finiteOr(origin.width, 1)),
    height: Math.max(1, finiteOr(origin.height, 1)),
  };
}

/**
 * Stores only one short-lived, in-memory visual handoff from an opener to the
 * route-backed World Focus surface. It is transient UI state, never durable
 * product state and never browser persistence.
 */
export function primeWorldFocusEntry(input: {
  worldId: WorldFocusId;
  source: WorldFocusEntrySource;
  origin: WorldFocusOriginRect;
}) {
  sequence += 1;
  pendingEntry = {
    token: sequence,
    worldId: input.worldId,
    source: input.source,
    origin: normalizeOrigin(input.origin),
    createdAt: Date.now(),
  };

  return pendingEntry;
}

export function readWorldFocusEntry(
  worldId: WorldFocusId,
  source: WorldFocusEntrySource,
): WorldFocusEntrySnapshot | null {
  if (pendingEntry === null) {
    return null;
  }

  if (Date.now() - pendingEntry.createdAt > WORLD_FOCUS_ENTRY_TTL_MS) {
    pendingEntry = null;
    return null;
  }

  if (pendingEntry.worldId !== worldId || pendingEntry.source !== source) {
    return null;
  }

  return pendingEntry;
}

export function clearWorldFocusEntry(token?: number) {
  if (pendingEntry === null) {
    return;
  }

  if (token === undefined || pendingEntry.token === token) {
    pendingEntry = null;
  }
}
