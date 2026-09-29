import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { PlanWork } from './remote-plan-work-data-source';

const { assess } = vi.hoisted(() => ({ assess: vi.fn() }));
vi.mock('./remote-plan-execution-data-source', () => ({
  createRemotePlanExecutionDataSource: () => ({ assess }),
}));

import { PlanExecutionPanel } from './plan-execution-panel';

const plan: PlanWork = {
  planRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
  stateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e',
  title: 'Album', createdAt: '2026-09-29T12:00:00Z', replayed: false,
  steps: [{
    stepRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f',
    position: 0, title: 'Record',
    activityRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56180',
    divisible: null, maxPlannedSlices: null, mergeCompatible: null,
    executionStrengthCode: null,
  }],
};

describe('Plan execution structure', () => {
  afterEach(cleanup);
  it('persists an indivisible policy as a Plan Step revision intent', () => {
    const update = vi.fn();
    render(<PlanExecutionPanel plan={plan} pending={false} update={update} />);
    fireEvent.click(screen.getByLabelText('Divisibile'));
    fireEvent.click(screen.getByRole('button', { name: 'Salva policy nello Step' }));
    expect(update).toHaveBeenCalledWith(plan.steps[0]?.stepRef, {
      divisible: false, maxPlannedSlices: 1, mergeCompatible: false,
      executionStrengthCode: 'hard',
    });
  });

  it('assesses an explicit snapshot without authoring Schedule or Session', async () => {
    assess.mockReset().mockResolvedValue({
      basis: 'explicit_proposed_slices', proposedCount: 1,
      countStatus: 'satisfied', countReason: 'within_proposed_count_limit',
      mergeStatus: 'not_requested', mergeReason: 'no_pair',
      mergedTemporalStatus: null, mergedTemporalRules: [], sliceAssessments: [],
    });
    render(<PlanExecutionPanel plan={plan} pending={false} update={vi.fn()} />);
    fireEvent.click(screen.getByRole('button', { name: 'Aggiungi segmento' }));
    fireEvent.change(screen.getByLabelText('Inizio'), { target: { value: '2026-09-29T12:00' } });
    fireEvent.change(screen.getByLabelText('Fine'), { target: { value: '2026-09-29T13:00' } });
    fireEvent.click(screen.getByRole('button', { name: 'Valuta proposta' }));
    await waitFor(() => expect(assess).toHaveBeenCalledOnce());
    expect(assess.mock.calls[0]?.[0]).toBe(plan);
    expect(assess.mock.calls[0]?.[2]).toHaveLength(1);
    expect(await screen.findByText(/Snapshot proposto: 1 segmenti/)).toBeTruthy();
  });
});
