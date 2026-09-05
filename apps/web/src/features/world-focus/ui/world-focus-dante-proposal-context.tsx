import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import { useTranslation } from 'react-i18next';

import {
  createWorldFocusDanteProposalRequest,
  WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION,
  type WorldFocusDanteProposal,
  type WorldFocusDanteProposalReader,
  type WorldFocusDanteProposalRequest,
} from '../application/world-focus-dante-proposal';
import { readWorldFocusDanteProposal } from '../application/world-focus-dante-proposal-runtime';
import { WorldFocusLatestReadCoordinator } from '../application/world-focus-foundation';
import type { WorldFocusId } from '../model/world-focus-identity';
import {
  WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
  useWorldFocusDanteInsight,
} from './world-focus-dante-insight-context';
import { useWorldFocusWorkspace } from './world-focus-workspace-host';

export const WORLD_FOCUS_DANTE_PROPOSAL_KIND = 'dante-proposal' as const;
export const WORLD_FOCUS_DANTE_PROPOSAL_INSTANCE_ID = 'dante:proposal' as const;
export const WORLD_FOCUS_DANTE_CONFIRMATION_KIND = 'dante-confirmation' as const;
export const WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID =
  'dante:confirmation' as const;
export const WORLD_FOCUS_DANTE_RECEIPT_KIND = 'dante-receipt' as const;
export const WORLD_FOCUS_DANTE_RECEIPT_INSTANCE_ID = 'dante:receipt' as const;
export const WORLD_FOCUS_DANTE_RECEIPT_SCHEMA_VERSION = 1 as const;

export const WORLD_FOCUS_DANTE_DECISIONS = ['confirmed', 'declined'] as const;
export type WorldFocusDanteDecision =
  (typeof WORLD_FOCUS_DANTE_DECISIONS)[number];

export type WorldFocusDanteDecisionReceipt = Readonly<{
  schemaVersion: typeof WORLD_FOCUS_DANTE_RECEIPT_SCHEMA_VERSION;
  receiptId: string;
  proposalId: string;
  worldId: WorldFocusId;
  workspaceGeneration: number;
  decision: WorldFocusDanteDecision;
}>;

export type WorldFocusDanteProposalRequestState =
  | Readonly<{ status: 'idle' }>
  | Readonly<{
      status: 'pending';
      requestId: string;
      sourceInsightId: string;
      workspaceGeneration: number;
    }>
  | Readonly<{
      status: 'unavailable';
      requestId: string;
      sourceInsightId: string;
      retryable: boolean;
    }>
  | Readonly<{
      status: 'error';
      requestId: string;
      sourceInsightId: string;
    }>
  | Readonly<{
      status: 'superseded';
      requestId: string;
      sourceInsightId: string;
    }>;

type WorldFocusDanteProposalContextValue = Readonly<{
  proposal: WorldFocusDanteProposal | null;
  receipt: WorldFocusDanteDecisionReceipt | null;
  requestState: WorldFocusDanteProposalRequestState;
  canRequestProposal: boolean;
  requestProposal: () => boolean;
  requestConfirmation: () => boolean;
  recordDecision: (decision: WorldFocusDanteDecision) => boolean;
}>;

const WorldFocusDanteProposalContext =
  createContext<WorldFocusDanteProposalContextValue | null>(null);

type WorldFocusDanteProposalProviderProps = Readonly<{
  worldId: WorldFocusId;
  children: ReactNode;
  reader?: WorldFocusDanteProposalReader;
}>;

function hasD6Surface(instanceId: string): boolean {
  return (
    instanceId === WORLD_FOCUS_DANTE_PROPOSAL_INSTANCE_ID ||
    instanceId === WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID ||
    instanceId === WORLD_FOCUS_DANTE_RECEIPT_INSTANCE_ID
  );
}

/**
 * D6 route-scoped pre-backend owner. It materializes a Proposal only from the
 * exact validated D5 Insight currently owned by the enclosing D5 provider,
 * owns the explicit confirmation decision, and records a local receipt. It
 * never executes, authorizes or infers any effect.
 */
export function WorldFocusDanteProposalProvider({
  worldId,
  children,
  reader = readWorldFocusDanteProposal,
}: WorldFocusDanteProposalProviderProps) {
  const { i18n } = useTranslation('common');
  const workspace = useWorldFocusWorkspace();
  const { insight } = useWorldFocusDanteInsight();
  const [proposal, setProposal] = useState<WorldFocusDanteProposal | null>(null);
  const [receipt, setReceipt] =
    useState<WorldFocusDanteDecisionReceipt | null>(null);
  const [requestState, setRequestState] =
    useState<WorldFocusDanteProposalRequestState>({ status: 'idle' });
  const [readCoordinator] = useState(() => new WorldFocusLatestReadCoordinator());
  const requestSerialRef = useRef(0);
  const generationRef = useRef(workspace.state.generation);

  useEffect(() => {
    generationRef.current = workspace.state.generation;
  }, [workspace.state.generation]);

  if (workspace.state.worldId !== worldId) {
    throw new Error('World Focus DANTE Proposal owner belongs to another World');
  }

  const d6SurfaceIsOpen = workspace.state.surfaces.some((surface) =>
    hasD6Surface(surface.instanceId),
  );
  const insightSurface = workspace.state.surfaces.find(
    (surface) => surface.instanceId === WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
  );
  const canRequestProposal =
    requestState.status !== 'pending' &&
    !d6SurfaceIsOpen &&
    insight !== null &&
    insight.worldId === worldId &&
    insight.workspaceGeneration === workspace.state.generation &&
    insightSurface !== undefined &&
    insightSurface.boundGeneration === workspace.state.generation;

  const requestProposal = useCallback((): boolean => {
    const sourceInsight = insight;
    const sourceSurface = workspace.state.surfaces.find(
      (surface) => surface.instanceId === WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
    );
    if (
      requestState.status === 'pending' ||
      d6SurfaceIsOpen ||
      sourceInsight === null ||
      sourceSurface === undefined ||
      sourceSurface.boundGeneration !== workspace.state.generation ||
      sourceInsight.worldId !== worldId ||
      sourceInsight.workspaceGeneration !== workspace.state.generation
    ) {
      return false;
    }

    const nextSerial = requestSerialRef.current + 1;
    const requestId = `${worldId}:local-proposal:${nextSerial}`;
    let request: WorldFocusDanteProposalRequest;
    try {
      request = createWorldFocusDanteProposalRequest({
        requestId,
        worldId,
        workspaceGeneration: sourceInsight.workspaceGeneration,
        sourceInsightId: sourceInsight.insightId,
        sourceInsightKind: sourceInsight.kind,
        sourceTitle: sourceInsight.title,
        sourceSummary: sourceInsight.summary,
        locale: i18n.resolvedLanguage ?? i18n.language ?? 'en',
        contextReferences: sourceInsight.basisReferences,
      });
    } catch {
      return false;
    }

    requestSerialRef.current = nextSerial;
    setRequestState({
      status: 'pending',
      requestId,
      sourceInsightId: sourceInsight.insightId,
      workspaceGeneration: request.workspaceGeneration,
    });

    const lease = readCoordinator.begin();
    void reader(request, lease.signal)
      .then((result) => {
        lease.commit(() => {
          if (generationRef.current !== request.workspaceGeneration) {
            setRequestState({
              status: 'superseded',
              requestId,
              sourceInsightId: sourceInsight.insightId,
            });
            return;
          }

          if (result.status === 'unavailable') {
            setRequestState({
              status: 'unavailable',
              requestId,
              sourceInsightId: sourceInsight.insightId,
              retryable: result.retryable,
            });
            return;
          }

          setProposal(result.proposal);
          setReceipt(null);
          workspace.openSurface({
            instanceId: WORLD_FOCUS_DANTE_PROPOSAL_INSTANCE_ID,
            kind: WORLD_FOCUS_DANTE_PROPOSAL_KIND,
            depth: 'explore',
            presentation: sourceSurface.presentation,
            origin: 'dante',
            contextReference: result.proposal.basisReferences.primary,
            dismissible: true,
            blocksWorkspaceInteraction:
              sourceSurface.blocksWorkspaceInteraction ?? false,
            expectedWorkspace: {
              worldId: workspace.state.worldId,
              generation: request.workspaceGeneration,
            },
          });
          setRequestState({ status: 'idle' });
        });
      })
      .catch(() => {
        if (lease.signal.aborted) return;
        lease.commit(() =>
          setRequestState({
            status: 'error',
            requestId,
            sourceInsightId: sourceInsight.insightId,
          }),
        );
      })
      .finally(() => lease.release());

    return true;
  }, [
    d6SurfaceIsOpen,
    i18n.language,
    i18n.resolvedLanguage,
    insight,
    readCoordinator,
    reader,
    requestState.status,
    workspace,
    worldId,
  ]);

  const requestConfirmation = useCallback((): boolean => {
    if (proposal === null || proposal.workspaceGeneration !== workspace.state.generation) {
      return false;
    }
    const proposalSurface = workspace.state.surfaces.find(
      (surface) => surface.instanceId === WORLD_FOCUS_DANTE_PROPOSAL_INSTANCE_ID,
    );
    if (
      proposalSurface === undefined ||
      workspace.state.surfaces.some(
        (surface) =>
          surface.instanceId === WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID ||
          surface.instanceId === WORLD_FOCUS_DANTE_RECEIPT_INSTANCE_ID,
      )
    ) {
      return false;
    }

    workspace.openSurface({
      instanceId: WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID,
      kind: WORLD_FOCUS_DANTE_CONFIRMATION_KIND,
      depth: 'explore',
      presentation: 'route',
      origin: 'user',
      contextReference: proposal.basisReferences.primary,
      dismissible: false,
      blocksWorkspaceInteraction: true,
      expectedWorkspace: {
        worldId: workspace.state.worldId,
        generation: proposal.workspaceGeneration,
      },
    });
    return true;
  }, [proposal, workspace]);

  const recordDecision = useCallback(
    (decision: WorldFocusDanteDecision): boolean => {
      if (
        proposal === null ||
        proposal.workspaceGeneration !== workspace.state.generation ||
        !WORLD_FOCUS_DANTE_DECISIONS.includes(decision)
      ) {
        return false;
      }
      const confirmationSurface = workspace.state.surfaces.find(
        (surface) => surface.instanceId === WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID,
      );
      const proposalSurface = workspace.state.surfaces.find(
        (surface) => surface.instanceId === WORLD_FOCUS_DANTE_PROPOSAL_INSTANCE_ID,
      );
      if (confirmationSurface === undefined || proposalSurface === undefined) {
        return false;
      }

      const nextReceipt = Object.freeze({
        schemaVersion: WORLD_FOCUS_DANTE_RECEIPT_SCHEMA_VERSION,
        receiptId: `${proposal.proposalId}:decision:${decision}`,
        proposalId: proposal.proposalId,
        worldId: proposal.worldId,
        workspaceGeneration: proposal.workspaceGeneration,
        decision,
      });
      setReceipt(nextReceipt);
      workspace.replaceSurface(WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID, {
        instanceId: WORLD_FOCUS_DANTE_RECEIPT_INSTANCE_ID,
        kind: WORLD_FOCUS_DANTE_RECEIPT_KIND,
        depth: 'explore',
        presentation: proposalSurface.presentation,
        origin: 'user',
        contextReference: proposal.basisReferences.primary,
        dismissible: true,
        blocksWorkspaceInteraction:
          proposalSurface.blocksWorkspaceInteraction ?? false,
        expectedWorkspace: {
          worldId: workspace.state.worldId,
          generation: proposal.workspaceGeneration,
        },
      });
      return true;
    },
    [proposal, workspace],
  );

  useEffect(() => {
    if (
      requestState.status !== 'pending' ||
      requestState.workspaceGeneration === workspace.state.generation
    ) {
      return;
    }

    const requestId = requestState.requestId;
    const sourceInsightId = requestState.sourceInsightId;
    readCoordinator.cancelCurrent();
    queueMicrotask(() =>
      setRequestState({ status: 'superseded', requestId, sourceInsightId }),
    );
  }, [readCoordinator, requestState, workspace.state.generation]);

  useEffect(() => {
    if (
      proposal === null ||
      proposal.workspaceGeneration === workspace.state.generation
    ) {
      return;
    }

    readCoordinator.cancelCurrent();
    queueMicrotask(() => {
      workspace.closeSurface(WORLD_FOCUS_DANTE_RECEIPT_INSTANCE_ID);
      workspace.closeSurface(WORLD_FOCUS_DANTE_CONFIRMATION_INSTANCE_ID);
      workspace.closeSurface(WORLD_FOCUS_DANTE_PROPOSAL_INSTANCE_ID);
      setProposal(null);
      setReceipt(null);
    });
  }, [proposal, readCoordinator, workspace]);

  useEffect(
    () => () => {
      readCoordinator.cancelCurrent();
    },
    [readCoordinator],
  );

  const value = useMemo<WorldFocusDanteProposalContextValue>(
    () => ({
      proposal,
      receipt,
      requestState,
      canRequestProposal,
      requestProposal,
      requestConfirmation,
      recordDecision,
    }),
    [
      canRequestProposal,
      proposal,
      receipt,
      recordDecision,
      requestConfirmation,
      requestProposal,
      requestState,
    ],
  );

  return (
    <WorldFocusDanteProposalContext.Provider value={value}>
      {children}
    </WorldFocusDanteProposalContext.Provider>
  );
}

export function useOptionalWorldFocusDanteProposal(): WorldFocusDanteProposalContextValue | null {
  return useContext(WorldFocusDanteProposalContext);
}

export function useWorldFocusDanteProposal(): WorldFocusDanteProposalContextValue {
  const value = useOptionalWorldFocusDanteProposal();
  if (value === null) {
    throw new Error(
      'useWorldFocusDanteProposal must be used inside WorldFocusDanteProposalProvider',
    );
  }
  return value;
}

export { WORLD_FOCUS_DANTE_PROPOSAL_SCHEMA_VERSION };
