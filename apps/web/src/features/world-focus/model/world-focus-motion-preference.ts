export const WORLD_FOCUS_MOTION_STORAGE_KEY =
  'dante.preferences.world-focus-motion.v1';

export type WorldFocusMotionPreference = 'immersive' | 'instant';

export type WorldFocusPreferenceStorage = Readonly<{
  getItem: (key: string) => string | null;
  setItem: (key: string, value: string) => void;
}>;

export const DEFAULT_WORLD_FOCUS_MOTION_PREFERENCE: WorldFocusMotionPreference =
  'immersive';

function resolveBrowserStorage(): WorldFocusPreferenceStorage | undefined {
  if (typeof window === 'undefined') {
    return undefined;
  }

  try {
    return window.localStorage;
  } catch {
    return undefined;
  }
}

export function normalizeWorldFocusMotionPreference(
  value: unknown,
): WorldFocusMotionPreference | undefined {
  return value === 'immersive' || value === 'instant' ? value : undefined;
}

export function readWorldFocusMotionPreference(
  storage: WorldFocusPreferenceStorage | undefined = resolveBrowserStorage(),
): WorldFocusMotionPreference {
  if (storage === undefined) {
    return DEFAULT_WORLD_FOCUS_MOTION_PREFERENCE;
  }

  try {
    return (
      normalizeWorldFocusMotionPreference(
        storage.getItem(WORLD_FOCUS_MOTION_STORAGE_KEY),
      ) ?? DEFAULT_WORLD_FOCUS_MOTION_PREFERENCE
    );
  } catch {
    return DEFAULT_WORLD_FOCUS_MOTION_PREFERENCE;
  }
}

export function writeWorldFocusMotionPreference(
  preference: WorldFocusMotionPreference,
  storage: WorldFocusPreferenceStorage | undefined = resolveBrowserStorage(),
) {
  if (storage === undefined) {
    return;
  }

  try {
    storage.setItem(WORLD_FOCUS_MOTION_STORAGE_KEY, preference);
  } catch {
    // Presentation preferences must never block navigation when storage is
    // unavailable, full, disabled, or sandboxed.
  }
}

export function shouldAnimateWorldFocusEntry(input: {
  hasLiveEntry: boolean;
  preference: WorldFocusMotionPreference;
  prefersReducedMotion: boolean;
}) {
  return (
    input.hasLiveEntry &&
    input.preference === 'immersive' &&
    !input.prefersReducedMotion
  );
}
