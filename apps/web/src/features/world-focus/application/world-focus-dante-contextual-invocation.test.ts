import { describe, expect, it } from 'vitest';

import type { WorldFocusContinuityItem } from '../model/world-focus-continuity';
import type {
  WorldFocusAttentionPrimitive,
  WorldFocusComparisonPrimitive,
} from '../model/world-focus-work-primitives';
import {
  createWorldFocusDanteAttentionContext,
  createWorldFocusDanteComparisonContext,
  createWorldFocusDanteContinuityContext,
  createWorldFocusDanteEvidenceContext,
} from './world-focus-dante-contextual-invocation';

describe('World Focus D4 bounded contextual invocation mapping', () => {
  it('maps Attention to matter primary plus the optional resolution reference only', () => {
    const primitive: WorldFocusAttentionPrimitive = {
      instanceId: 'attention:release-risk',
      kind: 'attention',
      matterReference: { kind: 'release', key: 'neon-static' },
      resolutionReference: { kind: 'decision', key: 'release-next-step' },
      reasonCode: 'blocked',
      state: 'blocked',
    };

    expect(createWorldFocusDanteAttentionContext(primitive)).toEqual({
      primary: { kind: 'release', key: 'neon-static' },
      supporting: [{ kind: 'decision', key: 'release-next-step' }],
    });
  });

  it('maps Continuity to thread primary plus checkpoint and optional continuation', () => {
    const item: WorldFocusContinuityItem = {
      key: 'neon-static',
      title: 'Neon Static',
      context: 'Release',
      checkpoint: 'Master v3',
      threadReference: { kind: 'project', key: 'neon-static' },
      checkpointReference: { kind: 'checkpoint', key: 'master-v3' },
      continuationReference: { kind: 'next', key: 'release-plan' },
      presentationState: 'active',
    };

    expect(createWorldFocusDanteContinuityContext(item)).toEqual({
      primary: { kind: 'project', key: 'neon-static' },
      supporting: [
        { kind: 'checkpoint', key: 'master-v3' },
        { kind: 'next', key: 'release-plan' },
      ],
    });
  });

  it('maps complete Comparison meaning without truncating subjects or basis', () => {
    const primitive: WorldFocusComparisonPrimitive = {
      instanceId: 'comparison:masters',
      kind: 'comparison',
      mode: 'difference',
      subjectReferences: [
        { kind: 'master', key: 'v1' },
        { kind: 'master', key: 'v2' },
        { kind: 'master', key: 'v3' },
      ],
      basisReference: { kind: 'basis', key: 'mix-review' },
    };

    expect(createWorldFocusDanteComparisonContext(primitive)).toEqual({
      primary: { kind: 'master', key: 'v1' },
      supporting: [
        { kind: 'master', key: 'v2' },
        { kind: 'master', key: 'v3' },
        { kind: 'basis', key: 'mix-review' },
      ],
    });
  });

  it('fails closed when complete Comparison meaning exceeds the bounded supporting-reference policy', () => {
    const primitive: WorldFocusComparisonPrimitive = {
      instanceId: 'comparison:overflow',
      kind: 'comparison',
      mode: 'difference',
      subjectReferences: [
        { kind: 'subject', key: '1' },
        { kind: 'subject', key: '2' },
        { kind: 'subject', key: '3' },
        { kind: 'subject', key: '4' },
        { kind: 'subject', key: '5' },
        { kind: 'subject', key: '6' },
      ],
      basisReference: null,
    };

    expect(createWorldFocusDanteComparisonContext(primitive)).toBeNull();
  });

  it('keeps Evidence as one exact primary reference and admits no semantic payload bag', () => {
    const context = createWorldFocusDanteEvidenceContext({
      kind: 'observation',
      key: 'mix-review',
    });

    expect(context).toEqual({
      primary: { kind: 'observation', key: 'mix-review' },
      supporting: [],
    });
    expect(context === null ? [] : Object.keys(context)).toEqual([
      'primary',
      'supporting',
    ]);
  });

  it('fails closed on duplicate semantic coordinates rather than silently widening or rewriting them', () => {
    const item: WorldFocusContinuityItem = {
      key: 'duplicate',
      title: 'Duplicate',
      context: 'Project',
      checkpoint: 'Checkpoint',
      threadReference: { kind: 'project', key: 'same' },
      checkpointReference: { kind: 'project', key: 'same' },
      continuationReference: null,
      presentationState: 'active',
    };

    expect(createWorldFocusDanteContinuityContext(item)).toBeNull();
  });
});
