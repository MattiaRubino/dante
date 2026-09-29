import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import type { PlanDependency } from './remote-plan-dependency-data-source';
import type { PlanWork } from './remote-plan-work-data-source';

const PLAN = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d';
const FIRST = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e';
const SECOND = '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f';
const STATE = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';
const DEPENDENCY = '0199a8c0-5e74-7bc0-8ad0-a2f403f56181';
const plan: PlanWork = {
  planRef: PLAN, stateRef: STATE, title: 'Album',
  createdAt: '2026-09-28T17:00:00Z', replayed: false,
  steps: [
    { stepRef: FIRST, title: 'Record', activityRef: DEPENDENCY, position: 0,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null, executionStrengthCode: null },
    { stepRef: SECOND, title: 'Mix', activityRef: STATE, position: 1,
      divisible: null, maxPlannedSlices: null, mergeCompatible: null, executionStrengthCode: null },
  ],
};
const relation: PlanDependency = {
  dependencyRef: DEPENDENCY, planRef: PLAN,
  prerequisiteStepRef: FIRST, prerequisiteActivityRef: DEPENDENCY,
  dependentStepRef: SECOND, dependentActivityRef: STATE,
  stateRef: STATE, purposeCode: 'dependent_activity_admissibility',
  qualifierCode: 'outcome_code', dispositionCode: 'work.completed',
  active: true, recordedAt: '2026-09-28T17:01:00Z',
  evaluationCode: 'unknown', cycle: true, replayed: false,
};

const { list, create, revise } = vi.hoisted(() => ({
  list: vi.fn(), create: vi.fn(), revise: vi.fn(),
}));
vi.mock('./remote-plan-dependency-data-source', () => ({
  createRemotePlanDependencyDataSource: () => ({ list, create, revise }),
}));

import { PlanDependencyPanel } from './plan-dependency-panel';

describe('Plan qualified Dependency panel', () => {
  beforeEach(() => {
    list.mockReset().mockResolvedValue([relation]);
    create.mockReset().mockResolvedValue(relation);
    revise.mockReset().mockResolvedValue({ ...relation, active: false, evaluationCode: null });
  });

  it('shows typed condition, unknown truth and cycle without inferring order', async () => {
    render(<PlanDependencyPanel plan={plan} />);
    expect(await screen.findByText(/Outcome = work.completed/)).toBeTruthy();
    expect(screen.getByText(/sconosciuta/)).toBeTruthy();
    expect(screen.getByText(/Ciclo nel Plan/)).toBeTruthy();
    expect(create).not.toHaveBeenCalled();
  });

  it('retires the selected assertion with its exact current revision', async () => {
    render(<PlanDependencyPanel plan={plan} />);
    fireEvent.click(await screen.findByRole('button', { name: 'Modifica' }));
    fireEvent.click(screen.getByRole('button', { name: 'Ritira Dependency' }));
    await waitFor(() => expect(revise).toHaveBeenCalledOnce());
    expect(revise.mock.calls[0]?.[0]).toMatchObject({
      dependencyRef: DEPENDENCY, stateRef: STATE,
    });
    expect(revise.mock.calls[0]?.[2]).toBe(false);
  });
});
