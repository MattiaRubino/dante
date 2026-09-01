import { createWorldFocusContinuityReader } from './world-focus-continuity';
import { worldFocusContinuityFixtureAdapter } from './world-focus-continuity-fixture-adapter';

/**
 * Pre-backend composition root for the Continuity read. The UI depends on the
 * intent-specific reader, not on fixture storage. The final backend vertical
 * replaces this adapter binding without changing the Continuity surface API.
 */
export const readWorldFocusContinuity = createWorldFocusContinuityReader(
  worldFocusContinuityFixtureAdapter,
);
