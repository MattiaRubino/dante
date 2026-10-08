// @vitest-environment jsdom
import { cleanup, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { TimelineInspectorReality } from './timeline-inspector-reality';

const policy = vi.hoisted(() => ({ getRealityMode: vi.fn() }));
vi.mock('../../../temporal/remote-reality-objective-data-source', () => ({
  createRemoteRealityObjectiveDataSource: () => policy,
}));
vi.mock('../../../temporal/actual-realization-controls', () => ({
  ActualRealizationControls: () => <div data-testid="review">Verifica</div>,
}));
vi.mock('../../../temporal/objective-controls', () => ({
  ObjectiveControls: () => <div data-testid="objectives">Obiettivi</div>,
}));

afterEach(() => { cleanup(); policy.getRealityMode.mockReset(); });

describe('Inspector optional reality sections', () => {
  it('shows review actions only when the canonical policy requests review', async () => {
    policy.getRealityMode.mockResolvedValue('review_on_end');
    render(<TimelineInspectorReality kind="activity" subjectRef="ref-1" />);
    expect(await screen.findByTestId('review')).toBeTruthy();
    expect(screen.getByTestId('objectives')).toBeTruthy();
  });

  it('does not show a fictional review for manual mode', async () => {
    policy.getRealityMode.mockResolvedValue('manual');
    render(<TimelineInspectorReality kind="event" subjectRef="ref-2" />);
    await waitFor(() => expect(policy.getRealityMode).toHaveBeenCalledWith('event', 'ref-2'));
    expect(screen.queryByTestId('review')).toBeNull();
  });
});
