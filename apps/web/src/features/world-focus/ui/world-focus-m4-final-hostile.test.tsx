import { useState } from 'react';
import { cleanup, fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeAll, describe, expect, it, vi } from 'vitest';

import { i18n } from '../../../bootstrap/i18n';
import type { WorldFocusDanteInsight } from '../application/world-focus-dante-insight';
import type {
  WorldFocusDanteProposalReader,
  WorldFocusDanteProposalRequest,
} from '../application/world-focus-dante-proposal';
import {
  WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
  WORLD_FOCUS_DANTE_INSIGHT_KIND,
} from './world-focus-dante-insight-context';
import {
  WorldFocusDanteProposalProvider,
  useWorldFocusDanteProposal,
} from './world-focus-dante-proposal-context';
import {
  WorldFocusWorkspaceHost,
  useWorldFocusWorkspace,
} from './world-focus-workspace-host';

const VALIDATED_INSIGHT: WorldFocusDanteInsight = Object.freeze({
  schemaVersion: 1,
  insightId: 'validated-d5-insight',
  worldId: 'music',
  workspaceGeneration: 0,
  kind: 'observation',
  title: 'Insight validato',
  summary: 'Questo è il solo Insight D5 associato alla surface corrente.',
  basisReferences: Object.freeze({
    primary: Object.freeze({ kind: 'continuity', key: 'validated-primary' }),
    supporting: Object.freeze([]),
  }),
});

const FORGED_SAME_GENERATION_INSIGHT: WorldFocusDanteInsight = Object.freeze({
  schemaVersion: 1,
  insightId: 'forged-same-generation-insight',
  worldId: 'music',
  workspaceGeneration: 0,
  kind: 'change',
  title: 'Insight non validato',
  summary: 'Questo oggetto non è il D5 Insight associato alla surface corrente.',
  basisReferences: Object.freeze({
    primary: Object.freeze({ kind: 'continuity', key: 'forged-primary' }),
    supporting: Object.freeze([
      Object.freeze({ kind: 'project', key: 'forged-supporting' }),
    ]),
  }),
});

const d5InsightState = vi.hoisted(() => ({
  current: null as WorldFocusDanteInsight | null,
}));

vi.mock('./world-focus-dante-insight-context', async (importOriginal) => {
  const actual = await importOriginal<
    typeof import('./world-focus-dante-insight-context')
  >();
  return {
    ...actual,
    useWorldFocusDanteInsight: () => ({
      insight: d5InsightState.current,
      requestState: { status: 'idle' as const },
      isOpen: d5InsightState.current !== null,
      canRequestInsight: false,
      requestInsight: () => false,
    }),
  };
});

beforeAll(async () => {
  await i18n.changeLanguage('it');
});

afterEach(() => {
  d5InsightState.current = null;
  cleanup();
});

function D5ToD6BindingHarness() {
  const workspace = useWorldFocusWorkspace();
  const proposal = useWorldFocusDanteProposal();
  const [accepted, setAccepted] = useState<boolean | null>(null);

  return (
    <div>
      <output data-testid="proposal-accepted">
        {accepted === null ? 'unattempted' : String(accepted)}
      </output>
      <button
        type="button"
        onClick={() =>
          workspace.openSurface({
            instanceId: WORLD_FOCUS_DANTE_INSIGHT_INSTANCE_ID,
            kind: WORLD_FOCUS_DANTE_INSIGHT_KIND,
            depth: 'insight',
            presentation: 'sidecar',
            origin: 'dante',
            contextReference: VALIDATED_INSIGHT.basisReferences.primary,
            expectedWorkspace: {
              worldId: workspace.state.worldId,
              generation: workspace.state.generation,
            },
          })
        }
      >
        Open validated D5 Insight surface
      </button>
      <button
        type="button"
        onClick={() => {
          const hostileRuntimeCall = proposal.requestProposal as unknown as (
            insight: WorldFocusDanteInsight,
          ) => boolean;
          setAccepted(hostileRuntimeCall(FORGED_SAME_GENERATION_INSIGHT));
        }}
      >
        Try forged D6 Proposal
      </button>
    </div>
  );
}

describe('World Focus M4 final hostile sequencing', () => {
  it('binds D6 to the exact current validated D5 artifact even when runtime code supplies a forged same-generation Insight argument', () => {
    d5InsightState.current = VALIDATED_INSIGHT;
    let capturedRequest: WorldFocusDanteProposalRequest | undefined;
    const reader = vi.fn<WorldFocusDanteProposalReader>(
      (request) => {
        capturedRequest = request;
        return new Promise(() => {
          // Keep the read pending; this test only proves request ownership/binding.
        });
      },
    );

    render(
      <WorldFocusWorkspaceHost worldId="music">
        <WorldFocusDanteProposalProvider worldId="music" reader={reader}>
          <D5ToD6BindingHarness />
        </WorldFocusDanteProposalProvider>
      </WorldFocusWorkspaceHost>,
    );

    fireEvent.click(
      screen.getByRole('button', { name: 'Open validated D5 Insight surface' }),
    );
    fireEvent.click(
      screen.getByRole('button', { name: 'Try forged D6 Proposal' }),
    );

    expect(screen.getByTestId('proposal-accepted').textContent).toBe('true');
    expect(reader).toHaveBeenCalledTimes(1);
    expect(capturedRequest).toMatchObject({
      sourceInsightId: VALIDATED_INSIGHT.insightId,
      sourceInsightKind: VALIDATED_INSIGHT.kind,
      sourceTitle: VALIDATED_INSIGHT.title,
      sourceSummary: VALIDATED_INSIGHT.summary,
      contextReferences: VALIDATED_INSIGHT.basisReferences,
    });
    expect(JSON.stringify(capturedRequest)).not.toContain(
      FORGED_SAME_GENERATION_INSIGHT.insightId,
    );
    expect(JSON.stringify(capturedRequest)).not.toContain('forged-primary');
  });
});
