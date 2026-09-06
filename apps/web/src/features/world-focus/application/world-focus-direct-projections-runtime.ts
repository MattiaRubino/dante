import { createWorldFocusDirectProjectionReaders } from './world-focus-direct-projections';
import { worldFocusDirectProjectionFixtureAdapter } from './world-focus-direct-projections-fixture-adapter';

const readers = createWorldFocusDirectProjectionReaders(
  worldFocusDirectProjectionFixtureAdapter,
);

export const readWorldFocusSituation = readers.readSituation;
export const readWorldFocusNext = readers.readNext;
export const readWorldFocusEvidenceHistory = readers.readEvidenceHistory;
