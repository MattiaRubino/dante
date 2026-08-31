import { describe, expect, it } from 'vitest';

import {
  DEFAULT_WORLD_FOCUS_MOTION_PREFERENCE,
  readWorldFocusMotionPreference,
  shouldAnimateWorldFocusEntry,
  WORLD_FOCUS_MOTION_STORAGE_KEY,
  writeWorldFocusMotionPreference,
  type WorldFocusPreferenceStorage,
} from './world-focus-motion-preference';

function createStorage(initial?: string) {
  const values = new Map<string, string>();
  if (initial !== undefined) {
    values.set(WORLD_FOCUS_MOTION_STORAGE_KEY, initial);
  }

  const storage: WorldFocusPreferenceStorage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => {
      values.set(key, value);
    },
  };

  return { storage, values };
}

describe('World Focus motion preference', () => {
  it('defaults safely to immersive when no valid preference exists', () => {
    expect(readWorldFocusMotionPreference(undefined)).toBe(
      DEFAULT_WORLD_FOCUS_MOTION_PREFERENCE,
    );
    expect(readWorldFocusMotionPreference(createStorage('unknown').storage)).toBe(
      DEFAULT_WORLD_FOCUS_MOTION_PREFERENCE,
    );
  });

  it('persists and reads the explicit instant preference', () => {
    const { storage, values } = createStorage();

    writeWorldFocusMotionPreference('instant', storage);

    expect(values.get(WORLD_FOCUS_MOTION_STORAGE_KEY)).toBe('instant');
    expect(readWorldFocusMotionPreference(storage)).toBe('instant');
  });

  it('keeps navigation independent from the presentation effect', () => {
    expect(
      shouldAnimateWorldFocusEntry({
        hasLiveEntry: true,
        preference: 'immersive',
        prefersReducedMotion: false,
      }),
    ).toBe(true);
    expect(
      shouldAnimateWorldFocusEntry({
        hasLiveEntry: true,
        preference: 'instant',
        prefersReducedMotion: false,
      }),
    ).toBe(false);
    expect(
      shouldAnimateWorldFocusEntry({
        hasLiveEntry: true,
        preference: 'immersive',
        prefersReducedMotion: true,
      }),
    ).toBe(false);
    expect(
      shouldAnimateWorldFocusEntry({
        hasLiveEntry: false,
        preference: 'immersive',
        prefersReducedMotion: false,
      }),
    ).toBe(false);
  });
});
