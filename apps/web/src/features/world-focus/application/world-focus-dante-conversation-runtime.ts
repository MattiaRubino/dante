import { createWorldFocusDanteConversationReader } from './world-focus-dante-conversation';
import { worldFocusDanteConversationFixtureAdapter } from './world-focus-dante-conversation-fixture-adapter';

export const readWorldFocusDanteConversation =
  createWorldFocusDanteConversationReader(
    worldFocusDanteConversationFixtureAdapter,
  );
