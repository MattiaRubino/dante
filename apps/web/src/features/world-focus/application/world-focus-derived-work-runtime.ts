import { createWorldFocusDerivedWorkReaders } from './world-focus-derived-work';
import { worldFocusDerivedWorkFixtureAdapter } from './world-focus-derived-work-fixture-adapter';

const readers = createWorldFocusDerivedWorkReaders(worldFocusDerivedWorkFixtureAdapter);

export const readWorldFocusAttention = readers.readAttention;
export const readWorldFocusComparison = readers.readComparison;
export const readWorldFocusTrajectory = readers.readTrajectory;
