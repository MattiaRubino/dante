import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';

import type { PlanWork } from './remote-plan-work-data-source';

const { search } = vi.hoisted(() => ({ search: vi.fn() }));
vi.mock('./remote-plan-candidate-data-source', () => ({
  createRemotePlanCandidateDataSource: () => ({ search }),
}));

import { PlanCandidatePanel } from './plan-candidate-panel';

const plan = {
  planRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617d',
  stateRef: '0199a8c0-5e74-7bc0-8ad0-a2f403f5617e',
  title: 'Album', steps: [],
} as unknown as PlanWork;
const stepRef = '0199a8c0-5e74-7bc0-8ad0-a2f403f56180';

afterEach(() => { cleanup(); search.mockReset(); });

it('shows bounded previews without an apply action or a claim of availability', async () => {
  search.mockResolvedValue({
    basisStatus: 'supported', reasonCode: 'supported_rules_only',
    solverStatus: 'OPTIMAL', movementPolicyStatus: 'blocked',
    capacityEvaluated: false,
    candidates: [{
      startsAt: '2026-10-01T11:00:00Z', endsAt: '2026-10-01T12:00:00Z',
      softViolations: 1,
    }],
  });
  render(<PlanCandidatePanel plan={plan} stepRef={stepRef} title="Mix" />);
  expect(search).not.toHaveBeenCalled();
  fireEvent.click(screen.getByRole('button', { name: 'Cerca alternative vicine per Mix' }));
  await waitFor(() => expect(search).toHaveBeenCalledWith(plan, stepRef));
  expect(await screen.findByText(/vincoli soft non soddisfatti/)).toBeTruthy();
  expect(screen.getByText(/Disponibilità e capacità non valutate/)).toBeTruthy();
  expect(screen.getByText(/movimento automatico bloccato/)).toBeTruthy();
  expect(screen.queryByRole('button', { name: /applica|accetta|sposta/i })).toBeNull();
});

it('keeps an unsatisfied prerequisite distinct from infeasibility', async () => {
  search.mockResolvedValue({
    basisStatus: 'blocked', reasonCode: 'prerequisite_unsatisfied',
    solverStatus: null, movementPolicyStatus: 'missing',
    capacityEvaluated: false, candidates: [],
  });
  render(<PlanCandidatePanel plan={plan} stepRef={stepRef} title="Mix" />);
  fireEvent.click(screen.getByRole('button', { name: 'Cerca alternative vicine per Mix' }));
  expect(await screen.findByText('Un prerequisito non è soddisfatto.')).toBeTruthy();
});
