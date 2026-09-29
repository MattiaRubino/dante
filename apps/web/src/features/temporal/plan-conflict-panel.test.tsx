import {
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import type { PlanWork } from './remote-plan-work-data-source';

const plan: PlanWork = {
  planRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
  stateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e',
  title: 'Album',
  createdAt: '2026-09-29T12:00:00Z',
  replayed: false,
  steps: [
    {
      stepRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617f',
      position: 0,
      title: 'Record',
      activityRef: null,
      divisible: null,
      maxPlannedSlices: null,
      mergeCompatible: null,
      executionStrengthCode: null,
    },
    {
      stepRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56180',
      position: 1,
      title: 'Mix',
      activityRef: null,
      divisible: null,
      maxPlannedSlices: null,
      mergeCompatible: null,
      executionStrengthCode: null,
    },
  ],
};

const { diagnose } = vi.hoisted(() => ({ diagnose: vi.fn() }));
vi.mock('./remote-plan-conflict-data-source', () => ({
  createRemotePlanConflictDataSource: () => ({ diagnose }),
}));

import { PlanConflictPanel } from './plan-conflict-panel';

afterEach(() => {
  cleanup();
  diagnose.mockReset();
});

it('requests current diagnosis only on click and names the exact limited findings', async () => {
  diagnose.mockResolvedValue({
    planRef: plan.planRef,
    planStateRef: plan.stateRef,
    title: plan.title,
    capacityEvaluated: false,
    steps: [
      {
        stepRef: plan.steps[0]!.stepRef,
        title: 'Record',
        diagnostics: ['unknown_basis'],
        dependencies: [],
      },
      {
        stepRef: plan.steps[1]!.stepRef,
        title: 'Mix',
        diagnostics: ['known_hard_violation', 'blocked_prerequisite'],
        dependencies: [
          {
            dependencyRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f56181',
            prerequisiteStepRef: plan.steps[0]!.stepRef,
            evaluationCode: 'unsatisfied',
          },
        ],
      },
    ],
  });
  render(<PlanConflictPanel plan={plan} />);
  expect(diagnose).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Analizza conflitti' }));
  await waitFor(() => expect(diagnose).toHaveBeenCalledWith(plan));
  expect(await screen.findByText(/Prerequisito non soddisfatto/)).toBeTruthy();
  expect(
    screen.getByText(/collocazione corrente viola un vincolo/),
  ).toBeTruthy();
  expect(
    screen.getByText(/disponibilità e la capacità non sono valutate/),
  ).toBeTruthy();
  expect(screen.getByText(/Dependency da Record/)).toBeTruthy();
});
