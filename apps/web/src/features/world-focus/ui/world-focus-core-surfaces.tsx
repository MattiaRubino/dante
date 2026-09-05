import {
  WorldFocusCompositionCustomizationSurface,
} from './world-focus-composition-customization-surface';
import {
  WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_KIND,
} from './world-focus-composition-customization-context';
import {
  WorldFocusDanteConversation,
  WORLD_FOCUS_DANTE_CONVERSATION_KIND,
} from './world-focus-dante-conversation';
import {
  WorldFocusDanteComposer,
  WORLD_FOCUS_DANTE_COMPOSER_KIND,
} from './world-focus-dante-entry';
import {
  WorldFocusDanteInsight,
  WORLD_FOCUS_DANTE_INSIGHT_KIND,
} from './world-focus-dante-insight';
import {
  WorldFocusDanteConfirmation,
  WorldFocusDanteProposal,
  WorldFocusDanteReceipt,
  WORLD_FOCUS_DANTE_CONFIRMATION_KIND,
  WORLD_FOCUS_DANTE_PROPOSAL_KIND,
  WORLD_FOCUS_DANTE_RECEIPT_KIND,
} from './world-focus-dante-proposal';
import {
  WorldFocusSurfaceRegistry,
  type WorldFocusSurfaceRegistration,
} from './world-focus-surface-registry';

const CORE_WORLD_FOCUS_SURFACE_REGISTRY = new WorldFocusSurfaceRegistry<
  WorldFocusSurfaceRegistration
>([
  {
    kind: WORLD_FOCUS_DANTE_COMPOSER_KIND,
    render: ({ onRequestClose }) => (
      <WorldFocusDanteComposer onRequestClose={onRequestClose} />
    ),
  },
  {
    kind: WORLD_FOCUS_DANTE_CONVERSATION_KIND,
    render: (props) => <WorldFocusDanteConversation {...props} />,
  },
  {
    kind: WORLD_FOCUS_DANTE_INSIGHT_KIND,
    render: (props) => <WorldFocusDanteInsight {...props} />,
  },
  {
    kind: WORLD_FOCUS_DANTE_PROPOSAL_KIND,
    render: (props) => <WorldFocusDanteProposal {...props} />,
  },
  {
    kind: WORLD_FOCUS_DANTE_CONFIRMATION_KIND,
    render: (props) => <WorldFocusDanteConfirmation {...props} />,
  },
  {
    kind: WORLD_FOCUS_DANTE_RECEIPT_KIND,
    render: (props) => <WorldFocusDanteReceipt {...props} />,
  },
  {
    kind: WORLD_FOCUS_COMPOSITION_CUSTOMIZATION_SURFACE_KIND,
    render: () => <WorldFocusCompositionCustomizationSurface />,
  },
]);

/**
 * Finite shipped World surface registry. Concrete kinds are added only by real
 * product verticals; remote/model-generated executable UI never enters here.
 */
export function getCoreWorldFocusSurfaceRegistry() {
  return CORE_WORLD_FOCUS_SURFACE_REGISTRY;
}
