import { createWorldFocusDanteProposalReader } from './world-focus-dante-proposal';
import { worldFocusDanteProposalFixtureAdapter } from './world-focus-dante-proposal-fixture-adapter';

export const readWorldFocusDanteProposal = createWorldFocusDanteProposalReader(
  worldFocusDanteProposalFixtureAdapter,
);
